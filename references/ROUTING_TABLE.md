# Complete Routing Decision Tree

## Intent extraction

From user input, extract:
1. **Action verb**: check/write/publish/research/find/fix/optimize/report
2. **Target object**: site/page/post/keyword/domain/rankings
3. **Scope**: full-site/single-page/batch/specific-URL
4. **GEO intent**: does it involve AI citation/ChatGPT/Perplexity/GEO?

## Phase match table

| Intent signal | Phase | Route |
|--------------|-------|-------|
| audit/check + site | CHECK | `wp_site_audit` → `/aaron:audit` |
| audit/check + tech/performance | CHECK | `/aaron:tech` + GSC |
| audit/check + content/article | CHECK | `/aaron-seo-geo:content-quality-auditor` |
| audit/check + domain/authority | CHECK | `/aaron-seo-geo:domain-authority-auditor` |
| audit/check + index/crawl | CHECK | `wp_inspect_url` + `wp_list_sitemaps` |
| write/create/publish + article/content | DO | §2.1→2.2→2.3→2.4 pipeline |
| refresh/update + existing post | DO | `/aaron:refresh` |
| research/discover + keyword | PLAN | `/aaron:discover` |
| research/discover + competitor | PLAN | `/aaron:compete` |
| track/rank/visibility | CHECK | `/aaron:visibility` + GSC |
| fix/repair/optimize/improve | ACT | Triple gate → WP MCP |
| report/summary | ACT | `/aaron:report` |
| GEO/AI citation | CROSS | `/aaron-seo-geo:geo-content-optimizer` |
| full/complete/cycle/workflow | FULL | PLAN→DO→CHECK→ACT |

## Safety gate check (for phases with write operations)

| Write type | Gates required |
|-----------|---------------|
| WP content publish | Settlement Gate + Change Governor |
| WP content update | Settlement Gate + Change Governor |
| WP SEO config change | Settlement + Governor + Hypothesis Verification |
| WP plugin/theme operation | Settlement + Governor (explicit approval required) |
| GSC read-only query | None |
| State file write | None |

## Fallback

Ambiguous intent → route to `/aaron:auto <original user input>`

## Full pipeline sequence (when "complete cycle" requested)

```
PLAN → keyword_research → competitor_analysis → content_gap → GSC opportunities → populate queues
DO → for each queued item: write → GEO → meta → schema → publish → Yoast → mark done
CHECK → wp_audit → page_audit → tech_check → visibility → GSC → metrics snapshot → scorecard
ACT → triple gate → fix criticals → report → increment iteration
```
