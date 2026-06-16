# SEO-GEO-Master — WordPress SEO/GEO Optimization Pipeline

> **上善若水。** Like water, it flows where needed. Speak naturally; it understands.

## What it does

A single Claude Code skill that orchestrates **Plan → Do → Check → Act** for any WordPress site. It merges **SEO** (search engine optimization) and **GEO** (generative engine optimization — making your content citeable by ChatGPT, Perplexity, Google AI Overviews, Gemini, and Claude).

**You don't memorize commands.** Say "check my site" or "write about X" — it routes to the right phase.

## Quick start

```
/seo-geo-master check https://example.com for SEO issues
/seo-geo-master run a full PDCA cycle on https://example.com
/seo-geo-master write and publish an article about "keyword"
/seo-geo-master how are my rankings on https://example.com
/seo-geo-master refresh old content on https://example.com
```

## Philosophy: 三经合一 (Three Streams Converge)

| Sage | Text | Principle | In this skill |
|------|------|-----------|---------------|
| **Laozi** | 道德经 | 上善若水 · 道法自然 | Formless UX: speak naturally, it adapts |
| **Sun Tzu** | 孙子兵法 | 五事七计 · 先胜后战 | Five-dimension scoring + safety-first publishing |
| **Inamori** | 原点哲学 | 作为人何谓正确 · 利他 | Origin of every piece of content: "Does this truly help the searcher?" |

Full philosophy: see `PHILOSOPHY.md`.

## Architecture

```
/seo-geo-master (single entry point)
    ├── Phase 0: Read state files
    ├── Intent router (natural language → PDCA phase)
    ├── PLAN: keyword research + competitor + SERP + GSC opportunities
    ├── DO: SEO writing + GEO optimize + meta + schema + WP publish
    ├── CHECK: WP audit + page audit + technical + ranking + GSC
    └── ACT: triple safety gate → fix → QA → report → iterate
```

### Safety: Triple Gate System

Adapted from [seo-survival-kit](https://github.com/maxschottke-spec/seo-survival-kit) (MIT).

| Gate | Function |
|------|----------|
| **Change Governor** | 6 modes (default: audit_only). Every change scored 0-10 risk points × multipliers. 26 hard stops. |
| **Settlement Gate** | After batch changes → 5-14 day mandatory waiting → data verification → next round |
| **Hypothesis Verification** | Fixes only execute when root cause is `verified` against real WP API / GSC data |

### State Persistence

Six JSON/NDJSON files track everything across sessions:
- `pdca-state.json` — phase, gates, 5-dimension scorecard
- `content-queue.json` — 6-status lifecycle (queued→in_progress→written→needs_review→skipped→published)
- `keyword-bank.json` — deduplicated keyword inventory with clusters
- `change-history.ndjson` — append-only change log with risk points
- `hypotheses.json` — 5-stage verification registry
- `run-history.ndjson` — append-only PDCA run log

## Prerequisites

- **WordPress MCP server** connected (for publishing + Yoast SEO + audit)
- **Google Search Console MCP** authenticated (recommended; degrades gracefully without)
- **aaron-seo-geo plugin** installed (recommended; for 20 specialized SEO/GEO sub-skills)

## Installation

```bash
# Option 1: Clone directly into Claude Code skills
git clone https://github.com/YOUR_USERNAME/seo-geo-master.git ~/.claude/skills/seo-geo-master

# Option 2: Clone anywhere, then symlink
git clone https://github.com/YOUR_USERNAME/seo-geo-master.git /path/to/seo-geo-master
ln -s /path/to/seo-geo-master ~/.claude/skills/seo-geo-master
```

## File structure

```
seo-geo-master/
├── SKILL.md                    # Main orchestrator
├── PHILOSOPHY.md               # Philosophical foundation
├── README.md / README_CN.md   # Documentation
├── LICENSE                     # MIT
├── references/                 # 8 deep-reference docs
├── schemas/                    # JSON Schema files
├── examples/                   # Example state templates
└── state/                      # Runtime state (gitignored)
```

## Safety model acknowledgment

The triple-gate safety model (Change Governor, Settlement Gate, Hypothesis Verification Gate) is adapted from [seo-survival-kit](https://github.com/maxschottke-spec/seo-survival-kit) by Max Schottke, used under MIT License. The content queue pattern references [the-four-systems](https://github.com/NicoSKOOL/the-four-systems). Skill routing leverages [aaron-seo-geo](https://github.com/mshojaei77/aio-seo-geo) (Apache 2.0).

## License

MIT — see `LICENSE`.
