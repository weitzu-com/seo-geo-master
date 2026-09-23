#!/usr/bin/env python3
"""Jev link-graph reference: inventory → (optional Jev decide) → NDJSON → plan.

Toyota / first principles:
  Facts in code. Judgments only from TypeSafe Jev when --live.
  Without --live: inventory + retrieval gaps only — NEVER emit action=auto.
  Default audit_only: never mutates a CMS.

Usage:
  python3 scripts/jev_link_graph.py --fixture examples/fixtures/link-inventory.example.json
  python3 scripts/jev_link_graph.py --fixture ... --out /tmp/gaps.ndjson
  TYPESAFE_API_KEY=... python3 scripts/jev_link_graph.py --fixture ... --live --out /tmp/link-decisions.ndjson
  python3 scripts/jev_link_graph.py --self-test
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
REPO_ROOT = Path(__file__).resolve().parents[1]


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


def inventory_gaps(all_pages: list[dict[str, Any]], eligible: list[dict[str, Any]]) -> list[str]:
    """Deterministic fact report — no model judgments."""
    gaps: list[str] = []
    elig_urls = {p["url"] for p in eligible}
    for p in all_pages:
        url = p.get("url") or "?"
        if p.get("http_status", 200) != 200:
            gaps.append(f"exclude {url}: http_status={p.get('http_status')}")
        elif p.get("noindex"):
            gaps.append(f"exclude {url}: noindex")
        elif p.get("canonical") and p["canonical"] != url:
            gaps.append(f"exclude {url}: non-self canonical → {p['canonical']}")
        elif p.get("thin"):
            gaps.append(f"exclude {url}: thin/deprecated")
        elif url not in elig_urls:
            gaps.append(f"exclude {url}: filtered")
    orphans = [p for p in eligible if not (p.get("existing_internal_links") or [])]
    if orphans:
        gaps.append(f"fact: {len(orphans)} eligible pages report zero existing internal links")
    return gaps


def existing_targets(page: dict[str, Any]) -> set[str]:
    links = page.get("existing_internal_links") or []
    return {link.get("href") for link in links if link.get("href")}


def page_id(page: dict[str, Any]) -> str:
    return page.get("id") or page["url"].rstrip("/").split("/")[-1].replace("-", "_")


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
            " ".join(
                [cand.get("title") or "", cand.get("purpose") or "", " ".join(cand.get("topic_tags") or [])]
            )
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
                "id": page_id(cand),
                "url": cand["url"],
                "title": cand.get("title") or cand["url"],
                "purpose": cand.get("purpose") or "",
                "money_page": bool(cand.get("money_page")),
                "retrieval_score": round(score, 4),
            }
        )
    return results


def ensure_no_link(criteria: dict[str, str]) -> None:
    if "no_link" not in criteria:
        raise SystemExit("HARD STOP: Choice criteria missing required no_link option")


def normalize_probs(probs: dict[str, float]) -> dict[str, float]:
    total = sum(max(0.0, float(v)) for v in probs.values())
    if total <= 0:
        return {k: 0.0 for k in probs}
    return {k: round(max(0.0, float(v)) / total, 6) for k, v in probs.items()}


def policy_action(
    choice: str,
    confidence: float,
    source_money: bool,
    target_money: bool,
    *,
    live: bool,
) -> str:
    """Poka-yoke: without live Jev, never auto. Money source OR target → review."""
    if not live:
        # Inventory-only / retrieval suggestion — judgment not made
        if choice == "no_link" and not source_money:
            return "refuse"  # no retrieval candidates is a fact, not a judgment
        return "review"
    if choice == "no_link":
        return "refuse"
    if source_money or target_money:
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


def retrieval_gap_record(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    """Deterministic shortlist only — not a Jev judgment."""
    if not candidates:
        return {
            "model": "inventory-only",
            "choice": "no_link",
            "confidence": 1.0,
            "probabilities": {"no_link": 1.0},
            "anchor_already_present": None,
        }
    best = max(candidates, key=lambda c: c.get("retrieval_score", 0))
    raw = {c["id"]: float(c.get("retrieval_score") or 0) for c in candidates}
    raw["no_link"] = 0.05  # keep refuse visible in distribution for plan readers
    probs = normalize_probs(raw)
    return {
        "model": "inventory-only",
        "choice": best["id"],
        "confidence": 0.0,  # no calibrated judgment without Jev
        "probabilities": probs,
        "anchor_already_present": None,
    }


def build_questions(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    criteria = {c["id"]: (c.get("purpose") or c.get("title") or c["id"]) for c in candidates}
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


def parse_live_answers(resp: dict[str, Any]) -> dict[str, Any]:
    answers = resp.get("answers") or {}
    best = answers.get("best_target") or {}
    choice = best.get("choice") or "no_link"
    confidence = float(best.get("confidence") or 0)
    probs = normalize_probs({k: float(v) for k, v in (best.get("probabilities") or {}).items()})
    if "no_link" not in probs and choice != "no_link":
        # Andon: live response omitted refuse mass — still allow choice but flag in notes upstream
        probs = normalize_probs({**probs, "no_link": 0.0})
    noul = answers.get("anchor_already_present") or {}
    return {
        "model": resp.get("model") or DEFAULT_MODEL,
        "choice": choice,
        "confidence": confidence,
        "probabilities": probs,
        "anchor_already_present": noul.get("noul"),
    }


def lookup_target_money(choice: str, candidates: list[dict[str, Any]]) -> bool:
    for c in candidates:
        if c["id"] == choice:
            return bool(c.get("money_page"))
    return False


def decide_one(
    source: dict[str, Any],
    passage: dict[str, Any],
    candidates: list[dict[str, Any]],
    live: bool,
    api_key: str | None,
    model: str,
    decision_id: str,
) -> dict[str, Any]:
    source_money = bool(source.get("money_page"))
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
        parsed = parse_live_answers(resp)
        notes = None
    else:
        parsed = retrieval_gap_record(candidates)
        notes = (
            "inventory-only: retrieval shortlist, NOT a Jev decision; "
            "action cannot be auto without --live + TYPESAFE_API_KEY"
        )

    choice = parsed["choice"]
    target_money = lookup_target_money(choice, candidates)
    action = policy_action(
        choice,
        float(parsed["confidence"]),
        source_money,
        target_money,
        live=live,
    )
    if action == "auto" and not live:
        raise SystemExit("HARD STOP / andon: inventory-only path emitted action=auto")

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
            {
                "id": c["id"],
                "url": c["url"],
                "title": c["title"],
                "purpose": c.get("purpose") or "",
            }
            for c in candidates
        ],
        "choice": choice,
        "confidence": parsed["confidence"],
        "probabilities": parsed["probabilities"],
        "anchor_already_present": parsed.get("anchor_already_present"),
        "action": action,
        "model": parsed["model"],
        "money_page": source_money or target_money,
        "target_url": target_url,
        "suggested_anchor": suggested,
        "notes": notes,
    }


def render_plan(decisions: list[dict[str, Any]], *, live: bool, gaps: list[str]) -> str:
    auto = [d for d in decisions if d["action"] == "auto"]
    review = [d for d in decisions if d["action"] == "review"]
    refuse = [d for d in decisions if d["action"] == "refuse"]
    mode = "LIVE Jev decisions" if live else "INVENTORY-ONLY (no Jev judgments; zero auto)"
    lines = [
        f"# Internal link plan — {mode}",
        "",
        "audit_only — no CMS writes",
        "",
        f"Total records: {len(decisions)}",
        f"  auto:   {len(auto)}",
        f"  review: {len(review)}",
        f"  refuse: {len(refuse)}",
        "",
        "## Deterministic inventory gaps",
    ]
    if not gaps:
        lines.append("(none)")
    else:
        lines.extend(f"- {g}" for g in gaps)
    lines.append("")
    lines.append("## AUTO (eligible only after explicit approval + governor mode)")
    if not auto:
        lines.append("(none)" if live else "(none — inventory-only cannot produce auto)")
    for d in auto:
        lines.append(
            f"- {d['source_url']} → {d.get('target_url')} "
            f"(conf={d['confidence']}, anchor={d.get('suggested_anchor')!r})"
        )
    lines.append("")
    lines.append("## REVIEW")
    if not review:
        lines.append("(none)")
    for d in review:
        label = "retrieval hint" if not live else "needs judgment"
        lines.append(
            f"- [{label}] {d['source_url']} ?→ {d.get('target_url') or d['choice']} "
            f"(conf={d['confidence']}, money={d.get('money_page')})"
        )
    lines.append("")
    lines.append("## REFUSE / no candidates")
    if not refuse:
        lines.append("(none)")
    for d in refuse:
        lines.append(f"- {d['source_url']}#{d['passage_id']} → no_link (conf={d['confidence']})")
    lines.append("")
    lines.append("Apply only after approval; batch under Change Governor (SAFETY_GOVERNOR.md).")
    if not live:
        lines.append("Re-run with TYPESAFE_API_KEY and --live to obtain calibrated decisions.")
    return "\n".join(lines)


def run(inventory_path: Path, out_path: Path | None, live: bool, model: str) -> int:
    inv = load_inventory(inventory_path)
    all_pages = inv["pages"]
    pages = eligible_pages(all_pages)
    gaps = inventory_gaps(all_pages, pages)
    api_key = os.environ.get("TYPESAFE_API_KEY")
    if live and not api_key:
        print(
            "HARD STOP: TYPESAFE_API_KEY missing. "
            "Inventory + gaps only; do not use Opus as full-site link decider.",
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

    if not live and any(d["action"] == "auto" for d in decisions):
        raise SystemExit("HARD STOP / andon: inventory-only produced auto actions")

    ndjson = "\n".join(json.dumps(d, ensure_ascii=False) for d in decisions) + ("\n" if decisions else "")
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(ndjson, encoding="utf-8")
        print(f"Wrote {len(decisions)} records → {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(ndjson)

    print(render_plan(decisions, live=live, gaps=gaps), file=sys.stderr)
    return 0


def self_test() -> int:
    """Andon / standardized work check — fail closed on invariant breaks."""
    failures: list[str] = []
    fixture = REPO_ROOT / "examples/fixtures/link-inventory.example.json"
    schema_path = REPO_ROOT / "schemas/link-decisions.schema.json"
    example_ndjson = REPO_ROOT / "examples/link-decisions.example.ndjson"
    spec = REPO_ROOT / "references/JEV_LINK_GRAPH.md"

    for p in (fixture, schema_path, example_ndjson, spec):
        if not p.is_file():
            failures.append(f"missing file: {p}")

    # no_link hard rule
    try:
        ensure_no_link({"a": "x"})
        failures.append("ensure_no_link should hard-stop without no_link")
    except SystemExit:
        pass
    ensure_no_link({"a": "x", "no_link": "refuse"})

    # probability normalization
    norm = normalize_probs({"a": 2.0, "b": 2.0, "no_link": 1.0})
    if abs(sum(norm.values()) - 1.0) > 1e-6:
        failures.append(f"normalize_probs sum={sum(norm.values())}")

    # money target forces review when live
    if policy_action("x", 0.99, False, True, live=True) != "review":
        failures.append("money target must review")
    if policy_action("x", 0.99, True, False, live=True) != "review":
        failures.append("money source must review")
    if policy_action("x", 0.99, False, False, live=True) != "auto":
        failures.append("high-conf non-money should auto when live")
    if policy_action("x", 0.99, False, False, live=False) != "review":
        failures.append("inventory-only must never auto on a choice")
    if policy_action("no_link", 1.0, False, False, live=False) != "refuse":
        failures.append("empty retrieval should refuse as fact")

    # dry-run fixture: zero auto
    inv = load_inventory(fixture)
    pages = eligible_pages(inv["pages"])
    autos = 0
    for source in pages:
        for passage in source.get("passages") or [{"id": "p", "text": source.get("purpose", "")}]:
            cands = retrieve_candidates(source, passage, pages)
            d = decide_one(source, passage, cands, False, None, DEFAULT_MODEL, "t")
            if d["action"] == "auto":
                autos += 1
    if autos:
        failures.append(f"inventory-only fixture produced {autos} auto actions")

    # example NDJSON schema required keys + money review consistency
    required = set(json.loads(schema_path.read_text())["required"])
    for i, line in enumerate(example_ndjson.read_text().splitlines(), 1):
        obj = json.loads(line)
        missing = required - set(obj)
        if missing:
            failures.append(f"example line {i} missing {missing}")
        if obj.get("money_page") and obj.get("action") == "auto":
            failures.append(f"example line {i}: money_page with auto")
        if "no_link" not in (obj.get("probabilities") or {}) and obj.get("choice") == "no_link":
            failures.append(f"example line {i}: refuse without no_link mass")

    # doc drift poka-yoke
    pdca = (REPO_ROOT / "references/PDCA_STATE_MACHINE.md").read_text()
    if "Six JSON" in pdca or "六 JSON" in pdca:
        failures.append("PDCA_STATE_MACHINE still says Six files")
    if "link-decisions.ndjson" not in pdca:
        failures.append("PDCA_STATE_MACHINE missing link-decisions")
    hyp = (REPO_ROOT / "references/HYPOTHESIS_VERIFICATION.md").read_text()
    if "26 hard stops" in hyp:
        failures.append("HYPOTHESIS_VERIFICATION still says 26 hard stops")
    safety = (REPO_ROOT / "references/SAFETY_GOVERNOR.md").read_text()
    for needle in ("no_link", "internal_link_plan", "TYPESAFE_API_KEY"):
        if needle not in safety:
            failures.append(f"SAFETY_GOVERNOR missing {needle}")

    if failures:
        print("SELF-TEST FAIL:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("SELF-TEST PASS", file=sys.stderr)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Jev link-graph reference pipeline")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=REPO_ROOT / "examples/fixtures/link-inventory.example.json",
        help="Page inventory JSON",
    )
    parser.add_argument("--out", type=Path, default=None, help="Write NDJSON here")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call TypeSafe Jev (requires TYPESAFE_API_KEY)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run andon / standardized-work invariant checks",
    )
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(self_test())
    raise SystemExit(run(args.fixture, args.out, args.live, args.model))


if __name__ == "__main__":
    main()
