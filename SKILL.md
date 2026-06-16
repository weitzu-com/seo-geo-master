---
name: seo-geo-master
description: |
  Platform-agnostic SEO+GEO PDCA optimization pipeline v2.1. Single entry point —
  say "check my site" or "write an article" and it routes to the right phase.
  Four-stage PDCA: Plan→Do→Check→Act. Supports WordPress (WP MCP) AND static sites
  (Astro/Vercel/GitHub/Cloudflare). Triple safety gates. Five-Dimension Scorecard (道天地将法).
  触发词：SEO审计、全站检查、发布文章、帮我看看网站、GEO优化、AI引用优化
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

# SEO-GEO-Master v2.1 — Platform-Agnostic Optimization Pipeline

> **上善若水。** Like water, it flows where needed. Speak naturally; it understands.
> Built on three streams: **Laozi** (formlessness) · **Sun Tzu** (strategy) · **Inamori** (altruism).
> **v2.1**: Platform-agnostic — works for WordPress, Astro, Vercel, any static site. Multi-language first.

---

## v2.1 What's New (from leisa.com 15-push PDCA session)

| Change | Type | Why |
|--------|------|-----|
| Platform-agnostic: WP + Static (Astro/Vercel/GitHub) | 🔧 | Proven on Astro+Vercel 4-language site |
| Multi-language-first: hreflang × 4, sitemap per locale | 🆕 | Every fix ×4 languages, 12 articles |
| Security-compliance baseline: P0-P1 DNS/Headers/Privacy | 🆕 | 6 P0 items in CHECK phase |
| Brand vs non-brand traffic analysis (GSC) | 🆕 | Zero non-branded = key insight |
| Competitor analysis: 五事七计 framework | 🆕 | Sun Tzu for global top-10 mapping |
| Content internal-linking network (triangular) | 🆕 | Articles → Services → Standards |
| Kimi WebBridge: GSC/Bing/Cloudflare dashboard | 🆕 | Browser automation for dashboards |
| DNS security: SPF + DKIM + DMARC as ground CHECK | 🆕 | Email auth = trust signal |

## Before anything: safety check

This skill defaults to **audit_only** mode. It never writes to your site unless you explicitly authorize.

For WordPress: triple safety gates apply.
For static sites: git-commit + push is the deployment path; always show diff before committing.

> "As a person, what is the right thing to do?" — If a change would show wrong info to a searcher, don't do it.

---

## Platform Detection (auto)

| Signal | Platform | Deploy Path |
|--------|----------|-------------|
| `wp-config.php` / WP MCP available | **WordPress** | WP MCP write ops |
| `astro.config.mjs` / `vercel.json` / `package.json` | **Static (Astro/Vercel)** | `git add → commit → push → Vercel auto-deploy` |
| `next.config.js` / `netlify.toml` | **Static (Next/Netlify)** | git push → auto-deploy |
| None detected | **Manual** | User provides deploy method |

---

## Phase 0: Read state

For WordPress: `state/pdca-state.json`, `state/content-queue.json`, `state/keyword-bank.json`
For static sites: read project `CLAUDE.md` + `vercel.json` + `astro.config.*` for context.

---

## Routing: speak naturally

| You say | It does |
|---------|---------|
| "check my site" / "SEO audit" | Full site audit → on-page → technical → security compliance → GSC → scorecard |
| "write about X" / "create article" | Research → draft → GEO optimize → meta → schema → multi-language → publish |
| "how are my rankings" / "visibility" | GSC analytics + brand/non-brand split + rank tracking |
| "fix the issues" / "deploy" | Priority matrix → fixes → QA → zero-residue verify |
| "competitor / top 10" | 五事七计 analysis → global ranking →避实击虚 strategy |
| "full cycle" / "complete workflow" | PLAN → DO → CHECK → ACT four stages |
| "report" / "summary" | Aggregate state → scorecard → top-5 priorities |
| "map / sitemap" | Sitemap audit + locale coverage + GSC submission |

---

## Phase 1: PLAN — 道·天

> Sun Tzu: "Know the enemy and know yourself."

### Competitor analysis (五事七计)
```
1. Identify top-10 global competitors by business alignment
2. Score each on 五事: 道(purpose) 天(timing) 地(geography) 将(talent) 法(systems)
3. Score on 七计: 主孰有道 天地孰得 法令孰行 兵众孰强 士卒孰练 赏罚孰明
4. Output: 避实击虚 strategy matrix
```

### Brand vs non-brand traffic audit (GSC)
**Critical metric**: brand clicks ÷ total clicks. >80% brand = SEO is not working — people only find you when they already know your name.

### Multi-language audit
For each locale: sitemap presence, hreflang correctness, meta tag completeness, content depth parity.

---

## Phase 2: DO — 地·将

> Sun Tzu: "First win, then go to war."

### Pre-publish self-check (every article)
1. If I searched this keyword and found this article, would I be satisfied?
2. Does it offer something competitors don't?
3. Can I vouch for every cited source?
**All three must be YES.**

### Multi-language content pipeline
```
1. Write primary language version (usually EN, highest traffic)
2. Add internal links (triangular: articles ←→ services ←→ standards)
3. Create ZH / RU / AR translations (keep structure, adapt cultural references)
4. Verify hreflang + canonical per locale
5. Verify all 4 language URLs return 200
```

### Internal linking strategy
```
Article A ←→ Article B ←→ Article C    (triangular inter-link)
      ↓             ↓             ↓
  /services     /standards     /industries   (hub pages)
      ↓             ↓             ↓
  /contact       /about        /blog         (conversion/trust)
```

### Security-compliance baseline (for EVERY site, before SEO)
| Priority | Item | Verify |
|:--:|------|--------|
| P0 | Privacy policy (all locales) | `curl -sI /privacy` = 200 |
| P0 | Cookie policy + banner | `grep cookie-banner` exists |
| P1 | CSP header | `curl -sI / \| grep content-security` |
| P1 | HSTS preload | `max-age=63072000; includeSubDomains; preload` |
| P1 | SPF + DKIM + DMARC | `dig +short _dmarc.domain TXT` |
| P1 | About page trust signals | Team photo/bio + credentials + equipment |

---

## Phase 3: CHECK — 知彼知己

> Sun Tzu: "If you know yourself but not the enemy, for every victory you will suffer a defeat."

### GSC data-driven diagnosis
```
1. Pull 3-month performance: clicks, impressions, CTR, avg position
2. Split brand vs non-brand queries
3. If non-brand <10% → flag as CRITICAL: content strategy needed
4. Check index coverage: indexed vs not-indexed + reasons
5. Submit sitemaps for all locales
```

### Site audit layers by platform
**WordPress**: `wp_site_audit` → on-page → technical → content-quality (80-EEAT)
**Static**: `curl` + `dig` + `grep` → DNS/SSL/Headers/Schema/hreflang/speed → manual content review

### Output: Five-Dimension Scorecard
```
┌──────────┬──────┬──────┬──────────────────────────────────────┐
│ 五事      │ Score │Grade │ Key Finding                           │
├──────────┼──────┼──────┼──────────────────────────────────────┤
│ 道 Intent│  85  │ 良   │ FAQ answers user questions directly    │
│ 天 Timing│  75  │ 中   │ Zero non-branded traffic              │
│ 地 Tech  │  95  │ 优   │ CSP+HSTS+Schema+hreflang+speed 0.3s   │
│ 将 Auth  │  80  │ 良   │ Team SVG+credentials+cases, needs photo│
│ 法 System│  88  │ 良   │ PDCA complete, monthly cron set        │
├──────────┼──────┼──────┼──────────────────────────────────────┤
│ Combined │  85  │ A-   │ 地从优→固, 将→照片, 天→内容驱动       │
└──────────┴──────┴──────┴──────────────────────────────────────┘
```

### GEO AI Citation Readiness
```
ChatGPT    ████████████████████░  90%  llms-full.txt + BlogPosting Schema
Perplexity ████████████████████░  90%  same
Google AIO █████████████████████  95%  FAQPage + Service + Organization Schema
Gemini     ████████████████████   85%  needs Knowledge Graph entity
Claude     ████████████████████░  90%  llms-full.txt + source citations
```

---

## Phase 4: ACT — 法

### Priority matrix (Sun Tzu: "First win, then go to war")
```
High impact × Low difficulty  → Execute now (P0 security, P1 headers)
High impact × High difficulty → Plan (content strategy, competitor campaigns)
Low impact  × Low difficulty  → Batch (meta tag tweaks, alt text)
Low impact  × High difficulty → Defer or skip
```

### Static site deploy flow
```
1. git add -A
2. git diff --cached --stat   ← show what's changing
3. git commit -m "descriptive message"
4. git push origin main
5. sleep 25 && verify URLs return 200
```

### Zero-residue verification (举一反三)
After every fix:
```bash
grep -rn "old_pattern" src/ | wc -l  # MUST be 0
curl -sI "fixed_url" | head -1        # MUST be 200
```
发现 1 个 bug → grep 全仓找同类 → 批量修复 → 零残留验证。

---

## Integration cheatsheet

### Platform-specific tools
| Activity | WordPress | Static (Astro/Vercel) |
|----------|-----------|----------------------|
| Audit | `wp_site_audit` | `curl` + `dig` + `grep` |
| Write | `wp_create_full_post` | Write `.md` / `.astro` files |
| Meta | `wp_update_yoast_seo` | Edit `<Base>` component props |
| Schema | Schema plugin or manual | JSON-LD in `<script>` or `set:html` |
| Deploy | WP save | `git push` → Vercel |
| Sitemap | `wp_list_sitemaps` | Check `sitemap-index.xml` |
| DNS | WP or manual | Cloudflare API / dashboard |

### Six inviolable rules
1. ❌ Vague approval → Stop. Require specific plan.
2. ❌ Write operation during Settlement Gate → Block.
3. ❌ Fix without `verified` hypothesis → Block.
4. ❌ Unused budget ≠ new authorization.
5. ❌ 404 after change → Stop all subsequent.
6. ❌ Publish without CORE-EEAT gate → Block.
