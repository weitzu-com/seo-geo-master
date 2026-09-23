#!/usr/bin/env python3
"""Jev link-graph reference: inventory → decide → NDJSON → printable plan.

First principles:
  Facts in code. Judgments via TypeSafe System One (Jev). Writing is out of scope here.
  Default is audit_only: never mutates a CMS.

Usage:
  python scripts/jev_link_graph.py --fixture examples/fixtures/link-inventory.example.json
  python scripts/jev_link_graph.py --fixture ... --out /tmp/link-decisions.ndjson
  TYPESAFE_API_KEY=... python scripts/jev_link_graph.py --fixture ... --live

Without TYPESAFE_API_KEY (or without --live): runs deterministic retrieval + dry-run
policy using heuristic scores, and refuses to pretend a frontier chat model decided.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TYPESAFE_URL = "https://api.typesafe.ai/v1/systemone"
DEFAULT_MODEL = "jev-latest"
CONFIDENCE_FLOOR = 0.6
TOKEN_RE = re.compile(r"[a-z0-9]+", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in TOKEN_RE.findall(text or "") if len(t) > 2}


def cosine_bow(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    return inter / math.sqrt(len(a) * len(b))


def load_inventory(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "pages" not in data:
        raise SystemExit(f"inventory missing 'pages': {path}")
    return data


def eligible_pages(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for p in pages:
        if p.get("http_status", 200) != 200:
            continue
        if p.get("noindex"):
            continue
        if p.get("canonical") and p["canonical"] != p.get("url"):
            continue
        if p.get("thin"):
            continue
        out.append(p)
    return out


def existing_targets(page: dict[str, Any]) -> set[str]:
    links = page.get("existing_internal_links") or []
    return {link.get("href") for link in links if link.get("href")}


def retrieve_candidates(
    source: dict[str, Any],
    passage: dict[str, Any],
    pool: list[dict[str, Any]],
    k: int = 5,
) -> list[dict[str, Any]]:
    src_url = source["url"]
    already = existing_targets(source)
    query = tokenize(
        " ".join(
            [
                passage.get("heading") or "",
                passage.get("text") or "",
                source.get("purpose") or "",
                source.get("title") or "",
            ]
        )
    )
    scored: list[tuple[float, dict[str, Any]]] = []
    for cand in pool:
        if cand["url"] == src_url:
            continue
        if cand["url"] in already:
            continue
        blob = tokenize(
            " ".join([cand.get("title") or "", cand.get("purpose") or "", " ".join(cand.get("topic_tags") or [])])
        )
        score = cosine_bow(query, blob)
        if score <= 0:
            continue
        scored.append((score, cand))
    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for score, cand in scored[:k]:
        results.append(
            {
                "id": cand.get("id") or cand["url"].rstrip("/").split("/")[-1].replace("-", "_"),
                "url": cand["url"],
                "title": cand.get("title") or cand["url"],
                "purpose": cand.get("purpose") or "",
                "retrieval_score": round(score, 4),
            }
        )
    return results


def ensure_no_link(criteria: dict[str, str]) -> None:
    if "no_link" not in criteria:
        raise SystemExit("HARD STOP: Choice criteria missing required no_link option")


def policy_action(
    choice: str,
    confidence: float,
    money_page: bool,
) -> str:
    if choice == "no_link":
        return "refuse"
    if money_page:
        return "review"
    if confidence < CONFIDENCE_FLOOR:
        return "review"
    return "auto"


def suggest_anchor(passage_text: str, target_title: str) -> str | None:
    """Prefer an existing phrase; never invent marketing copy."""
    if not passage_text or not target_title:
        return None
    title_l = target_title.lower()
    text_l = passage_text.lower()
    if title_l in text_l:
        start = text_l.index(title_l)
        return passage_text[start : start + len(target_title)]
    # longest overlapping title token sequence of length >= 2
    words = title_l.split()
    for n in range(min(4, len(words)), 1, -1):
        for i in range(0, len(words) - n + 1):
            phrase = " ".join(words[i : i + n])
            if phrase in text_l:
                start = text_l.index(phrase)
                return passage_text[start : start + len(phrase)]
    return None


def system_one(state: Any, questions: dict[str, Any], api_key: str, model: str) -> dict[str, Any]:
    payload = {"model": model, "state": state, "questions": questions}
    req = urllib.request.Request(
        TYPESAFE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"TypeSafe HTTP {e.code}: {body}") from e


def heuristic_decide(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    """Offline stand-in when --live is off. Not a chat-model substitute."""
    if not candidates:
        probs = {"no_link": 1.0}
        return {
            "model": "heuristic-dry-run",
            "choice": "no_link",
            "confidence": 1.0,
            "probabilities": probs,
            "anchor_already_present": None,
        }
    best = max(candidates, key=lambda c: c.get("retrieval_score", 0))
    score = float(best.get("retrieval_score") or 0)
    # Weak overlap → refuse; mid → review-ish confidence; strong → auto-ish
    if score < 0.15:
        choice = "no_link"
        confidence = 0.9
        probs = {c["id"]: 0.05 for c in candidates}
        probs["no_link"] = 0.85
    else:
        choice = best["id"]
        confidence = min(0.95, 0.4 + score)
        remain = max(0.0, 1.0 - confidence)
        probs = {c["id"]: round(remain / max(len(candidates), 1), 4) for c in candidates}
        probs[choice] = round(confidence * 0.85, 4)
        probs["no_link"] = round(1.0 - sum(probs.values()) + probs.get("no_link", 0), 4)
        probs["no_link"] = max(0.0, min(1.0, probs["no_link"]))
    return {
        "model": "heuristic-dry-run",
        "choice": choice,
        "confidence": round(confidence, 4),
        "probabilities": probs,
        "anchor_already_present": None,
    }


def build_questions(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    criteria = {
        c["id"]: (c.get("purpose") or c.get("title") or c["id"]) for c in candidates
    }
    criteria["no_link"] = "None of the candidates is a useful, honest next step."
    ensure_no_link(criteria)
    return {
        "best_target": {
            "type": "choice",
            "instructions": "Which candidate best continues the reader's task in this passage?",
            "criteria": criteria,
        },
        "anchor_already_present": {
            "type": "noul",
            "instructions": "The passage already contains natural anchor text for the chosen target.",
        },
    }


def parse_live_answers(resp: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    answers = resp.get("answers") or {}
    best = answers.get("best_target") or {}
    choice = best.get("choice") or "no_link"
    confidence = float(best.get("confidence") or 0)
    probs = best.get("probabilities") or {}
    noul = answers.get("anchor_already_present") or {}
    anchor_p = noul.get("noul")
    return {
        "model": resp.get("model") or DEFAULT_MODEL,
        "choice": choice,
        "confidence": confidence,
        "probabilities": probs,
        "anchor_already_present": anchor_p,
    }


def decide_one(
    source: dict[str, Any],
    passage: dict[str, Any],
    candidates: list[dict[str, Any]],
    live: bool,
    api_key: str | None,
    model: str,
    decision_id: str,
) -> dict[str, Any]:
    money = bool(source.get("money_page") or False)
    if live:
        if not api_key:
            raise SystemExit(
                "HARD STOP: --live requires TYPESAFE_API_KEY. "
                "Do not substitute a frontier chat model for full-site link decisions."
            )
        state = {
            "source_url": source["url"],
            "heading": passage.get("heading"),
            "passage": passage.get("text"),
            "source_intent": source.get("purpose") or source.get("title"),
            "candidates": [
                {"id": c["id"], "title": c["title"], "purpose": c.get("purpose") or ""}
                for c in candidates
            ],
        }
        questions = build_questions(candidates)
        resp = system_one(state, questions, api_key, model)
        parsed = parse_live_answers(resp, candidates)
    else:
        parsed = heuristic_decide(candidates)

    choice = parsed["choice"]
    action = policy_action(choice, float(parsed["confidence"]), money)
    target_url = None
    suggested = None
    if choice != "no_link":
        for c in candidates:
            if c["id"] == choice:
                target_url = c["url"]
                suggested = suggest_anchor(passage.get("text") or "", c.get("title") or "")
                break

    return {
        "decision_id": decision_id,
        "ts": utc_now(),
        "source_url": source["url"],
        "passage_id": passage.get("id") or "p-0",
        "heading": passage.get("heading"),
        "passage": passage.get("text"),
        "candidates": [
            {"id": c["id"], "url": c["url"], "title": c["title"], "purpose": c.get("purpose") or ""}
            for c in candidates
        ],
        "choice": choice,
        "confidence": parsed["confidence"],
        "probabilities": parsed["probabilities"],
        "anchor_already_present": parsed.get("anchor_already_present"),
        "action": action,
        "model": parsed["model"],
        "money_page": money,
        "target_url": target_url,
        "suggested_anchor": suggested,
        "notes": None if live else "dry-run heuristic (not Jev); set TYPESAFE_API_KEY and --live for real decisions",
    }


def render_plan(decisions: list[dict[str, Any]]) -> str:
    auto = [d for d in decisions if d["action"] == "auto"]
    review = [d for d in decisions if d["action"] == "review"]
    refuse = [d for d in decisions if d["action"] == "refuse"]
    lines = [
        "# Internal link plan (audit_only — no CMS writes)",
        "",
        f"Total decisions: {len(decisions)}",
        f"  auto:   {len(auto)}",
        f"  review: {len(review)}",
        f"  refuse: {len(refuse)}",
        "",
        "## AUTO (eligible after explicit approval + governor mode)",
    ]
    if not auto:
        lines.append("(none)")
    for d in auto:
        lines.append(
            f"- {d['source_url']} → {d.get('target_url')} "
            f"(conf={d['confidence']}, anchor={d.get('suggested_anchor')!r})"
        )
    lines.append("")
    lines.append("## REVIEW (human or money-page gate)")
    if not review:
        lines.append("(none)")
    for d in review:
        lines.append(
            f"- {d['source_url']} ?→ {d.get('target_url') or d['choice']} "
            f"(conf={d['confidence']}, money={d.get('money_page')})"
        )
    lines.append("")
    lines.append("## REFUSE (honest no_link)")
    if not refuse:
        lines.append("(none)")
    for d in refuse:
        lines.append(f"- {d['source_url']}#{d['passage_id']} → no_link (conf={d['confidence']})")
    lines.append("")
    lines.append("Apply only after approval; batch under Change Governor (see SAFETY_GOVERNOR.md).")
    return "\n".join(lines)


def run(inventory_path: Path, out_path: Path | None, live: bool, model: str) -> int:
    inv = load_inventory(inventory_path)
    pages = eligible_pages(inv["pages"])
    api_key = os.environ.get("TYPESAFE_API_KEY")
    if live and not api_key:
        print(
            "HARD STOP: TYPESAFE_API_KEY missing. Inventory-only / dry-run allowed; "
            "do not use Opus as full-site link decider.",
            file=sys.stderr,
        )
        return 2

    decisions: list[dict[str, Any]] = []
    n = 0
    for source in pages:
        passages = source.get("passages") or [
            {
                "id": "p-body",
                "heading": source.get("title"),
                "text": source.get("purpose") or source.get("title") or "",
            }
        ]
        for passage in passages:
            cands = retrieve_candidates(source, passage, pages)
            n += 1
            decisions.append(
                decide_one(
                    source=source,
                    passage=passage,
                    candidates=cands,
                    live=live,
                    api_key=api_key,
                    model=model,
                    decision_id=f"ld-{n:04d}",
                )
            )

    ndjson = "\n".join(json.dumps(d, ensure_ascii=False) for d in decisions) + ("\n" if decisions else "")
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(ndjson, encoding="utf-8")
        print(f"Wrote {len(decisions)} decisions → {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(ndjson)

    print(render_plan(decisions), file=sys.stderr)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Jev link-graph reference pipeline")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=Path("examples/fixtures/link-inventory.example.json"),
        help="Page inventory JSON",
    )
    parser.add_argument("--out", type=Path, default=None, help="Write NDJSON decisions here")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call TypeSafe Jev (requires TYPESAFE_API_KEY)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    raise SystemExit(run(args.fixture, args.out, args.live, args.model))


if __name__ == "__main__":
    main()
