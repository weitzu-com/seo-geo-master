---
name: seo-geo-master
description: |
  WordPress SEO+GEO PDCA optimization pipeline. Single entry point — say "check my site"
  or "write an article about X" and it routes to the right phase. Four-stage PDCA:
  Plan→Do→Check→Act. Routes to aaron-seo-geo + WordPress MCP + Google Search Console.
  Triple safety gates: Change Governor + Settlement Gate + Hypothesis Verification.
  触发词：优化WordPress站点、SEO审计、全站检查、发布文章、帮我看看网站
allowed-tools: Read, Write, Edit, Bash, WebFetch, WebSearch,
  Skill, TaskCreate, TaskUpdate, TaskGet, TaskList,
  mcp__wordpress__wp_get_post, mcp__wordpress__wp_get_page,
  mcp__wordpress__wp_list_posts, mcp__wordpress__wp_list_pages,
  mcp__wordpress__wp_create_post, mcp__wordpress__wp_create_full_post,
  mcp__wordpress__wp_update_post, mcp__wordpress__wp_update_page,
  mcp__wordpress__wp_get_yoast_seo, mcp__wordpress__wp_update_yoast_seo,
  mcp__wordpress__wp_site_audit, mcp__wordpress__wp_inspect_url,
  mcp__wordpress__wp_list_sitemaps, mcp__wordpress__wp_get_settings,
  mcp__wordpress__wp_update_settings, mcp__wordpress__wp_list_plugins,
  mcp__wordpress__wp_list_themes, mcp__wordpress__wp_list_categories,
  mcp__wordpress__wp_list_tags, mcp__wordpress__wp_create_category,
  mcp__wordpress__wp_create_tag, mcp__wordpress__wp_upload_media,
  mcp__wordpress__wp_update_media, mcp__wordpress__wp_list_media,
  mcp__wordpress__wp_search, mcp__wordpress__wp_bulk_update_posts,
  mcp__wordpress__wp_detect_page_builder, mcp__wordpress__wp_get_post_type,
  mcp__google-searchconsole__query_search_analytics,
  mcp__google-searchconsole__get_top_pages,
  mcp__google-searchconsole__find_keyword_opportunities,
  mcp__google-searchconsole__compare_performance,
  mcp__google-searchconsole__get_keyword_trend,
  mcp__google-searchconsole__analyze_brand_queries,
  mcp__google-searchconsole__list_sites, mcp__google-searchconsole__list_sitemaps,
  mcp__google-searchconsole__export_analytics
argument-hint: "<action> [site-url] [keyword|post-id]"
---

# SEO-GEO-Master — WordPress Optimization Pipeline

> **上善若水。** Like water, it flows where needed. Speak naturally; it understands.
> Built on three streams: **Laozi** (formlessness) · **Sun Tzu** (strategy) · **Inamori** (altruism).

---

## Before anything: safety check

This skill defaults to **audit_only** mode. It never writes to your site unless you explicitly authorize.

Every WordPress write operation passes through **three gates**:
1. **Change Governor** — risk-point budget (0-10 per change × risk multipliers). 26 hard stops.
2. **Settlement Gate** — after batch changes, forces 5-14 day data accumulation before next round.
3. **Hypothesis Verification** — fixes only execute when root cause is `verified` against real WP/GSC data.

> "As a person, what is the right thing to do?" — If a change would show wrong info to a searcher, don't do it.

---

## Phase 0: Read state

Before any action, read these files (init from `examples/` if missing):

```
state/pdca-state.json         — current phase + safety gates + metrics
state/content-queue.json      — content pipeline (6-status lifecycle)
state/keyword-bank.json        — deduplicated keyword inventory
```

---

## Routing: speak naturally

The skill matches your intent, not your exact words:

| You say | It does |
|---------|---------|
| "check my site" / "SEO audit" / "what's wrong" | Full site audit → on-page check → technical scan → GSC pull → scorecard |
| "write about X" / "create article" | Keyword research → draft → GEO optimize → meta → schema → publish to WP |
| "how are my rankings" / "visibility" | GSC analytics + rank tracking + period comparison |
| "fix the issues" / "deploy" | Triple gate check → WP write ops → QA → change log |
| "full cycle" / "complete workflow" | PLAN → DO → CHECK → ACT four stages |
| "report" / "summary" | Aggregate state → performance report → top-5 priorities |

Ambiguous? Routes to `/aaron:auto`.

---

## Phase 1: PLAN — Intent alignment & timing

> Sun Tzu: "Know the enemy and know yourself."

### Intent research
```
/aaron:discover <seed keyword>
/aaron:compete <domain or industry>
/aaron-seo-geo:serp-analysis
/aaron-seo-geo:content-gap-analysis
```

### Timing analysis
```
mcp__google-searchconsole__find_keyword_opportunities
mcp__google-searchconsole__get_keyword_trend
mcp__google-searchconsole__analyze_brand_queries
```

### Decision matrix
| Trend | Competition | Strategy |
|-------|------------|----------|
| Rising + Low | Publish now |
| Rising + High | Differentiate angle |
| Stable + Low | Normal schedule |
| Stable + High | Find subtopics (避实击虚) |
| Declining | Don't invest |

Output: `state/keyword-bank.json` + `state/content-queue.json`

---

## Phase 2: DO — Content + GEO + Publish

> Sun Tzu: "First win, then go to war."

### Pre-publish self-check (every article)
1. If I searched this keyword and found this article, would I be satisfied?
2. Does it offer something competitors don't? (Unique data? Experience? Angle?)
3. Can I vouch for every cited source?

**All three must be YES.**

### Content pipeline
```
1. /aaron:write "<primary keyword>"                    → SEO draft (Three Kings)
2. /aaron-seo-geo:geo-content-optimizer                → AI citation optimization
3. /aaron-seo-geo:meta-tags-optimizer                  → title + meta + OG
4. /aaron-seo-geo:schema-markup-generator              → JSON-LD
5. mcp__wordpress__wp_create_full_post                 → publish to WP + Yoast SEO
6. mcp__wordpress__wp_update_yoast_seo                 → fine-tune Yoast fields
```

### GEO content spec (summary)
- ≥3 citeable statistics with sources
- 25-50 word definitions for core terms
- ≥60% H2s in Content Capsule format (question + direct answer + expansion)
- ≥1 structured list or table

### E-E-A-T checklist
| Signal | Check |
|--------|-------|
| Author page | Real name, photo, credentials, Person Schema |
| Source citations | Every stat/claim links to authoritative source |
| Fact accuracy | No outdated data, no contradictions |
| Trust pages | About, Contact, Privacy, Terms exist |
| Date visibility | `dateModified` on every article |

### Content refresh (existing articles)
```
/aaron:refresh <post-id>
```

---

## Phase 3: CHECK — Audit + Analytics

> Sun Tzu: "If you know yourself but not the enemy, for every victory you will suffer a defeat."

### WP audit
```
mcp__wordpress__wp_site_audit
mcp__wordpress__wp_inspect_url
mcp__wordpress__wp_list_sitemaps
```

### SEO audit layers
```
/aaron:audit <url>                                      → page-level 11-step
/aaron:tech <domain>                                    → 9-step technical + LLM crawlers
/aaron-seo-geo:content-quality-auditor                   → 80-item CORE-EEAT gate
/aaron-seo-geo:domain-authority-auditor                  → 40-item CITE authority gate
```

### Performance
```
/aaron:visibility <domain>
mcp__google-searchconsole__query_search_analytics
mcp__google-searchconsole__get_top_pages
mcp__google-searchconsole__compare_performance
```

### Output: Five-Dimension Scorecard
```
┌──────────┬──────┬──────┬────────────────────────────┐
│ Dimension│Score │Grade │ Key Finding                  │
├──────────┼──────┼──────┼────────────────────────────┤
│ 道 Intent│  85  │ Good │ Intent aligned, 2 gaps      │
│ 天 Timing│  70  │  Mid │ Missed Q2 window             │
│ 地 Tech  │  90  │  Top │ CWV all green               │
│ 将 Auth  │  65  │  Mid │ 3 top posts lack author     │
│ 法 System│  80  │ Good │ PDCA cadence healthy         │
├──────────┼──────┼──────┼────────────────────────────┤
│ Combined │  78  │ Good │ Fix 将 first, then 天        │
└──────────┴──────┴──────┴────────────────────────────┘
```

---

## Phase 4: ACT — Fix + Refresh + Report

### Priority matrix (Sun Tzu: "First win, then go to war")
```
High impact × Low difficulty  → Execute now
High impact × High difficulty → Plan
Low impact  × Low difficulty  → Batch
Low impact  × High difficulty → Defer or skip
```

### Execute (after triple gate clearance)
```
mcp__wordpress__wp_update_post
mcp__wordpress__wp_update_yoast_seo
/aaron-seo-geo:internal-linking-optimizer
```

Every fix: before-snapshot → execute → after-snapshot → QA → log change-history.ndjson

### Report
```
/aaron:report <domain>
/aaron:watch <domain>
```

### Cycle complete
- Increment `iterations_completed` in state
- Reset phase to `plan` for next round
- Report: scorecard deltas + next-cycle priorities

---

## State files

| File | Purpose | Format |
|------|---------|--------|
| `state/pdca-state.json` | Master state: phase/gates/scorecard | JSON (overwrite) |
| `state/content-queue.json` | Content pipeline: 6-status lifecycle | JSON (overwrite) |
| `state/keyword-bank.json` | Keyword inventory: dedup + clusters | JSON (overwrite) |
| `state/change-history.ndjson` | Change log: risk points + QA | NDJSON (append) |
| `state/hypotheses.json` | Hypothesis registry: 5-stage verification | JSON (overwrite) |
| `state/run-history.ndjson` | Run log: every PDCA run | NDJSON (append) |

---

## Integration cheatsheet

### aaron-seo-geo skills
| Phase | Activity | Command |
|-------|----------|---------|
| PLAN | Keyword research | `/aaron:discover` |
| PLAN | Competitor analysis | `/aaron:compete` |
| PLAN | Content brief | `/aaron:map` `/aaron:brief` |
| DO | SEO writing | `/aaron:write` |
| DO | GEO optimization | `/aaron-seo-geo:geo-content-optimizer` |
| DO | Meta tags | `/aaron-seo-geo:meta-tags-optimizer` |
| DO | Schema | `/aaron-seo-geo:schema-markup-generator` |
| DO | Content refresh | `/aaron:refresh` |
| CHECK | Page audit | `/aaron:audit` |
| CHECK | Technical check | `/aaron:tech` |
| CHECK | Rank tracking | `/aaron:visibility` |
| CHECK | Content quality (80-EEAT) | `/aaron-seo-geo:content-quality-auditor` |
| CHECK | Domain authority (40-CITE) | `/aaron-seo-geo:domain-authority-auditor` |
| ACT | Report | `/aaron:report` |
| ACT | Alerts | `/aaron:watch` |
| CROSS | Intent routing | `/aaron:auto` |

### WordPress MCP
| Operation | Tool |
|-----------|------|
| Site audit | `wp_site_audit` |
| Create post (with Yoast + image) | `wp_create_full_post` |
| Get / Update Yoast SEO | `wp_get_yoast_seo` / `wp_update_yoast_seo` |
| Update post | `wp_update_post` |
| Index status | `wp_inspect_url` |
| Sitemaps | `wp_list_sitemaps` |
| Upload media | `wp_upload_media` |
| Detect editor | `wp_detect_page_builder` |

### Google Search Console
| Operation | Tool |
|-----------|------|
| Performance | `query_search_analytics` |
| Top pages | `get_top_pages` |
| Opportunities | `find_keyword_opportunities` |
| Period compare | `compare_performance` |
| Keyword trend | `get_keyword_trend` |
| Brand analysis | `analyze_brand_queries` |

---

## Six inviolable rules

1. ❌ Vague approval ("do everything", "fix all") → Stop. Require specific plan.
2. ❌ Write operation during Settlement Gate → Block. Explain waiting period.
3. ❌ Fix without `verified` hypothesis → Block. Route to verification.
4. ❌ Unused budget ≠ new authorization → "Reserve stays reserve."
5. ❌ 404 after change → Stop all subsequent changes.
6. ❌ Publish without CORE-EEAT gate → Block.

---

## References

| File | Content |
|------|---------|
| `references/SAFETY_GOVERNOR.md` | 6 modes / risk points / 26 hard stops |
| `references/SETTLEMENT_GATE.md` | Triggers / 5-14 day waiting / exceptions |
| `references/HYPOTHESIS_VERIFICATION.md` | 5-stage lifecycle / WP verification tiers |
| `references/PDCA_STATE_MACHINE.md` | 6-file state machine spec |
| `references/ROUTING_TABLE.md` | Complete decision tree |
| `references/GEO_CONTENT_SPEC.md` | 4-element GEO spec + AI platform factors |
| `references/INTEGRATION_MAP.md` | Full integration table |
| `references/CHANGE_HISTORY.md` | NDJSON format + type enums |

---

## Philosophy

For the full philosophical foundation (三经合一: Laozi · Sun Tzu · Inamori), see `PHILOSOPHY.md`.

> **上善若水。** Water benefits all things without contention. — Laozi
> **知己知彼，百战不殆。** Know yourself, know your enemy, and you will never be defeated. — Sun Tzu
> **作为人，何谓正确？** As a person, what is the right thing to do? — Inamori Kazuo
