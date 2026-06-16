# Safety Governor — 6 Modes / Risk Points / 26 Hard Stops

> Adapted from [seo-survival-kit](https://github.com/maxschottke-spec/seo-survival-kit) under MIT License.

The skill must not execute unbounded live changes. Every session starts in `audit_only` mode with zero change budget.

---

## Operating modes

| Mode | Budget | Purpose |
|------|--------|---------|
| `audit_only` | 0 | Read-only analysis, crawls, GSC queries, WP API GETs |
| `micro_fix` | 3 | One very small fix (one Yoast field, one broken link) |
| `low_risk_fix` | 10 | Small technical corrections with clear rollback |
| `controlled_recovery` | 20 | Bounded batch with pre/post QA |
| `emergency_rollback` | 30 | Stabilization and rollback only |
| `high_risk_requires_approval` | 0 | Plan only, no execution without explicit per-change approval |

Default: `audit_only`. Mode escalation requires explicit user instruction.

## When Settlement Gate is active

| Mode | Status |
|------|--------|
| `audit_only` | Allowed, 0 budget |
| `emergency_rollback` | Allowed, up to 30 points, stabilization only |
| All other modes | **Blocked** |

---

## Risk points

### 0 points (always allowed)
Read-only WP API calls, GSC queries, WP site audit, plugin/theme lists, content exports, HTTP health checks, plan generation, state file reads/writes.

### 1 point
Single Yoast field update, single alt text, single tag/category, broken link fix, typo correction.

### 2 points
Post title/slug change (low traffic), meta rewrite, schema addition, internal link, redirect, status change.

### 3 points
Post content rewrite (non-ranking), multiple Yoast fields, template update, menu item change, up to 3 internal links added, category restructure.

### 5 points
Post change with 3+ internal links, change on post with GSC impressions, change on page with backlinks, tag/category merge, widget/sidebar change, site settings change.

### 8 points
Top-10 ranking post change, significant traffic post change, plugin activation/deactivation (sitewide), theme update, 3-5 posts batch update, navigation restructure.

### 10 points
Mass change (>10 posts), >10 internal links in one run, batch publish, slug changes on indexed posts, SEO plugin config change (sitewide), core update, permalink structure change.

## Risk multipliers

| Condition | Multiplier |
|-----------|-----------|
| Top-20 GSC ranking | x2 |
| External backlinks | x2 |
| No staging environment | x2 |
| Medium confidence data only | x1.5 |
| Medical/health claims (YMYL) | x2 |
| No documented rollback | x3 |
| Post <30 days old | x1.5 |
| Money page (commercial intent) | x1.5 |

**Final = base × all applicable multipliers, rounded up.**

---

## 26 hard stops

Claude must immediately stop when:

1. User gives vague approval ("do everything", "fix all", "just do it") — requires specific plan
2. Change budget exceeded for current session
3. >3 structural posts per calendar day without batch plan; >5 absolute ceiling
4. >10 repair-hygiene changes in one run without batch plan
5. >3 new internal links to a single post without specific approval
6. Live HTTP check after change returns 404
7. Redirect chain created (slug change on already-redirected post)
8. Post target is not HTTP 200
9. Post has noindex or blocked robots meta
10. WP REST API returns error (500/403/401)
11. WP state contradicts Yoast SEO state while contradicting live HTTP
12. Category/tag deletion without checking post count, keywords, traffic
13. Medical/health claim without authoritative source verification
14. Sitewide plugin/theme change without explicit approval
15. Post publish/major edit without `wp_get_post` pre-check
16. Permalink change without redirect verification
17. Batch category/tag change without backup
18. New medical/health claim introduced without source citation
19. Settlement Gate active and attempted mode not in allowed_modes
20. Attempt to spend unused budget as permission (Reserve stays reserve)
21. Operator pressure phrases during active Settlement Gate without Technical Emergency
22. Hypothesis not at `verified` for the cause being addressed
23. Fix scope exceeds verified scope
24. Verification relies exclusively on weak-tier sources
25. Content update on post never crawled since last update (<7 days)
26. Publish/update without CORE-EEAT gate for competitive keywords

### Stop output format
1. Why execution was stopped
2. Which changes have already been executed
3. Which changes were still planned
4. Current live status of all affected URLs
5. Risks
6. Rollback plan
7. What explicit approval would be needed to continue

---

## Reserve stays reserve

Unused change budget does not roll forward. A week with 1 of 7 points spent does not authorize 6 more points next week. Every additional measure needs a new change plan with its own risk points, data basis, rollback plan, and explicit approval.

If the operator uses pressure phrases implying unused budget is permission:

> **Stop.** New change plan and explicit approval required.

Stop reason: `unused_budget_is_not_permission`.

---

## Post-change QA format

```json
{
  "change_id": "wp-change-001",
  "status": "success|partial|failed",
  "live_checks": {
    "http_status": 200,
    "wp_post_id": 42,
    "slug": "post-slug",
    "yoast_title_present": true,
    "yoast_description_present": true,
    "canonical": "self",
    "og_image_present": true
  },
  "unexpected_effects": [],
  "rollback_needed": false
}
```

---

## Reference

Original model: [seo-survival-kit/SEO_CHANGE_GOVERNOR.md](https://github.com/maxschottke-spec/seo-survival-kit)
