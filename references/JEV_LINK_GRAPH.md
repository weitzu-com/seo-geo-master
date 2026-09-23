# Jev Link Graph — First-Principles Internal Linking Pipeline

> **Facts belong to code. Judgments belong to a decision model. Writing belongs to a frontier model.**
> Default mode: `audit_only` — produce a link plan. Never write to the CMS until the user approves a batch.

This pipeline replicates the *decision layer* demonstrated in site-wide internal-link rebuilds (classification at scale), not Distribb's distribution SaaS. It uses TypeSafe **Jev** (`POST https://api.typesafe.ai/v1/systemone`) for bounded Choice / Noul decisions.

---

## Four axioms

1. **Facts ≠ judgments** — HTTP status, canonical, noindex, existing links, indexability are deterministic. Never ask a model.
2. **Internal linking is classification, not writing** — each candidate is a bounded yes/no or choice, not a prose suggestion.
3. **Refusal is first-class** — every Choice must include `no_link`. Honest refuse beats forced mutual linking.
4. **Confidence gates action** — the answer is *what*; confidence is *whether*. Low confidence → human or frontier cascade, never silent write.

Frontier chat models write new articles or rewrite one sentence for an anchor when no phrase exists. They do **not** scan hundreds of pages for link decisions.

---

## Ten-step pipeline

| Step | Name | Owner | Risk points |
|:----:|------|-------|:-----------:|
| 1 | Inventory | Code / CMS / crawl | 0 |
| 2 | Extract | Code | 0 |
| 3 | Retrieve candidates | Code (light retrieval) | 0 |
| 4 | Deterministic filter | Code | 0 |
| 5 | Jev decide | TypeSafe System One | 0 |
| 6 | Persist decisions | State file | 0 |
| 7 | Policy gate | Code thresholds | 0 |
| 8 | Anchor text | Match first; frontier only if needed | 0 (plan) / write pts on apply |
| 9 | Apply batch | Change Governor | ≥2 per link; batch caps |
| 10 | Verify | Recrawl / HTTP | 0 |

### 1. Inventory

Collect indexable, canonical pages:

- **WordPress**: `wp_list_posts` / `wp_list_pages` (+ sitemap cross-check)
- **Static**: parse sitemap(s), `curl` each URL

Persist a page inventory (URL, title, status, canonical, robots, type, locale).

### 2. Extract

Per page, extract:

- headings and body passages (sentence/paragraph units)
- existing internal links (`href` + anchor text)
- one-sentence **purpose** (title + first meaningful paragraph, or CMS excerpt)

### 3. Retrieve candidates

For each source passage, shortlist **3–10** targets via light retrieval (v1):

- title + purpose token overlap / simple cosine on bag-of-words
- optional topic tags or hub membership (articles ↔ services ↔ standards)

Do **not** pass hundreds of loose URLs to Jev. Retrieval quality bounds decision quality.

### 4. Deterministic filter

Remove candidates that:

- are not HTTP 200, or redirect
- are `noindex` or non-canonical
- are the source URL itself
- already receive a contextual link from this source page
- are thin / scheduled for removal / duplicate purpose

Jev must never guess status codes from copy.

### 5. Jev decide

For each `(source_passage, candidates)` call System One with **Choice** (required `no_link`) and optional **Noul** (anchor already present).

Requires `TYPESAFE_API_KEY`. If missing: **inventory + deterministic gaps + retrieval shortlist only**; every record stays `review` or fact-`refuse` — **never `auto`**. Do **not** substitute Opus for full-site decisions.

### 6. Persist

Append one NDJSON line per decision to `state/link-decisions.ndjson` (see `schemas/link-decisions.schema.json`). Store model version, probabilities, confidence, candidate set, and policy `action`.

### 7. Policy gate (code)

| Condition | `action` |
|-----------|----------|
| `choice == no_link` | `refuse` |
| `confidence < 0.6` (live Jev only) | `review` |
| money / commercial page as **source or target** | `review` (always) |
| no live Jev (`inventory-only`) | never `auto` — `review` for shortlists, `refuse` only when zero candidates |
| otherwise high confidence + live Jev | `auto` (eligible for apply plan) |

Thresholds are starting defaults; calibrate on labeled site examples when available.

### 8. Anchor text

1. Prefer an existing phrase in the passage that honestly describes the target.
2. Only if no phrase fits: one frontier rewrite of **that sentence**, then re-check honesty.
3. Jev never invents anchor strings.

### 9. Apply (gated)

1. Default: render a human-readable **link plan** from NDJSON (`auto` + approved `review`).
2. User must explicitly approve apply + escalate governor mode (typically `controlled_recovery`).
3. Split into batches: ≤10 posts per run **or** stay under session risk budget; ≤3 new links to a single post without specific approval.
4. Never one-shot 500+ links via bulk update.
5. After a batch, Settlement Gate may activate — wait before the next batch.

### 10. Verify

Recrawl or `curl` changed URLs: new `href` present, target returns 200, no redirect chains. Log QA on the change-history line.

---

## Decision request shape

```json
{
  "model": "jev-latest",
  "state": {
    "source_url": "https://example.com/technical-seo-checklist",
    "heading": "Find pages with weak internal discovery",
    "passage": "A crawl can reveal useful pages that receive few contextual internal links.",
    "source_intent": "Help an SEO specialist run a technical audit",
    "candidates": [
      {
        "id": "orphan_pages",
        "title": "How to Find and Fix Orphan Pages",
        "purpose": "Diagnose pages with no useful internal links and reconnect them"
      },
      {
        "id": "broken_links",
        "title": "How to Find Broken Links",
        "purpose": "Find links that point to unavailable destinations"
      }
    ]
  },
  "questions": {
    "best_target": {
      "type": "choice",
      "instructions": "Which candidate best continues the reader's task in this passage?",
      "criteria": {
        "orphan_pages": "The passage is about discovering and reconnecting underlinked or orphaned pages.",
        "broken_links": "The passage is about links whose destination returns an error.",
        "no_link": "None of the candidates is a useful, honest next step."
      }
    },
    "anchor_already_present": {
      "type": "noul",
      "instructions": "The passage already contains natural anchor text for the chosen target."
    }
  }
}
```

**Hard rule:** any Choice without `no_link` in `criteria` must not be sent (Safety Governor hard stop).

---

## Topology heuristic (secondary)

After decisions, prefer a readable graph shape when multiple `auto` targets tie on usefulness:

```
Article A ←→ Article B ←→ Article C
      ↓             ↓             ↓
  /services     /standards     /industries
      ↓             ↓             ↓
  /contact       /about        /blog
```

Topology never overrides a `refuse` or low-confidence `review`.

---

## Skill triggers

Route here when the user says (any language):

- rebuild internal link map / 重建内链图
- site-wide internal linking / 全站内链
- Jev link audit / Jev 内链审计
- link graph / 链接图

Single-article DO linking uses the **same primitives** at small scale (one source × few candidates), still with `no_link`.

---

## Reference implementation

See [`scripts/jev_link_graph.py`](../scripts/jev_link_graph.py): inventory fixture → gaps/decide → NDJSON → printable plan.

```bash
python3 scripts/jev_link_graph.py --self-test
python3 scripts/jev_link_graph.py --fixture examples/fixtures/link-inventory.example.json
TYPESAFE_API_KEY=... python3 scripts/jev_link_graph.py --fixture ... --live --out state/link-decisions.ndjson
```

Environment: `TYPESAFE_API_KEY` required for `--live`. Without it, inventory-only mode never emits `action=auto` and refuses to fake decisions with a chat model.

---

## Out of scope

- Distribb backlink exchange / paid GSC wrappers
- Asking Jev to crawl, write anchors, or publish
- Vector DB as a blocker for v1 (optional later)
- Opus as the default full-site decider (optional debug cascade only)
