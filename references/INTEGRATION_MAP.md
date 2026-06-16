# Integration Map — aaron-seo-geo + WordPress MCP + Google Search Console

## aaron-seo-geo skills (20 sub-skills)

| Phase | Activity | Shortcut | Full Skill |
|-------|----------|----------|------------|
| PLAN | Keyword research | `/aaron:discover` | `keyword-research` |
| PLAN | Competitor analysis | `/aaron:compete` | `competitor-analysis` |
| PLAN | SERP analysis | — | `serp-analysis` |
| PLAN | Content gap | — | `content-gap-analysis` |
| PLAN | Content brief | `/aaron:map` `/aaron:brief` | — |
| DO | SEO writing | `/aaron:write` | `seo-content-writer` |
| DO | GEO optimization | — | `geo-content-optimizer` |
| DO | Meta tags | — | `meta-tags-optimizer` |
| DO | Schema | — | `schema-markup-generator` |
| DO | Content refresh | `/aaron:refresh` | `content-refresher` |
| DO | Internal linking | — | `internal-linking-optimizer` |
| CHECK | Page audit | `/aaron:audit` | `on-page-seo-auditor` |
| CHECK | Technical check | `/aaron:tech` | `technical-seo-checker` |
| CHECK | Rank tracking | `/aaron:visibility` | `rank-tracker` |
| CHECK | Backlink analysis | — | `backlink-analyzer` |
| CHECK | Content quality (80-CORE-EEAT) | — | `content-quality-auditor` |
| CHECK | Domain authority (40-CITE) | `/aaron:authority` | `domain-authority-auditor` |
| ACT | Performance report | `/aaron:report` | `performance-reporter` |
| ACT | Alert management | `/aaron:watch` | `alert-manager` |
| CROSS | Intent routing | `/aaron:auto` | — |

## WordPress MCP

| Operation | Tool | Risk |
|-----------|------|------|
| Site audit | `wp_site_audit` | 0 (read) |
| Create full post | `wp_create_full_post` | 2-5 (write) |
| Get Yoast SEO | `wp_get_yoast_seo` | 0 (read) |
| Update Yoast SEO | `wp_update_yoast_seo` | 1-3 (write) |
| Update post | `wp_update_post` | 2-5 (write) |
| Index check | `wp_inspect_url` | 0 (read) |
| List sitemaps | `wp_list_sitemaps` | 0 (read) |
| Upload media | `wp_upload_media` | 1 (write) |
| Detect editor | `wp_detect_page_builder` | 0 (read) |
| Site settings get | `wp_get_settings` | 0 (read) |
| Site settings update | `wp_update_settings` | 5-10 (write, sitewide) |
| Plugin activate/deactivate | `wp_update_plugin` | 8 (write, sitewide) |

## Google Search Console

| Operation | Tool |
|-----------|------|
| Performance query | `query_search_analytics` |
| Top pages | `get_top_pages` |
| Keyword opportunities | `find_keyword_opportunities` |
| Period comparison | `compare_performance` |
| Keyword trend | `get_keyword_trend` |
| Brand analysis | `analyze_brand_queries` |
| Export | `export_analytics` |
| Site list | `list_sites` |

All GSC operations are read-only, 0 risk points.

## Safety model integration

| Mechanism | Source file | Applied to |
|-----------|------------|------------|
| Change Governor | `references/SAFETY_GOVERNOR.md` | All WP write operations |
| Settlement Gate | `references/SETTLEMENT_GATE.md` | After batch changes |
| Hypothesis Verification | `references/HYPOTHESIS_VERIFICATION.md` | Before fix execution |
| CORE-EEAT Gate (80-item) | aaron-seo-geo:content-quality-auditor | Before publish |
| CITE Gate (40-item) | aaron-seo-geo:domain-authority-auditor | Domain-level assessment |
