# Settlement Gate

> Adapted from [seo-survival-kit](https://github.com/maxschottke-spec/seo-survival-kit) under MIT License.

After significant batch changes, the Settlement Gate forces a mandatory data accumulation period. Core principle: **Measure first, then act.**

---

## Triggers (any one activates the gate)

| Trigger | Threshold |
|---------|-----------|
| WP live changes in one session | >10 |
| Posts created/updated/deleted | >5 |
| Internal links added/removed | >10 |
| Categories/tags created or deleted | >=2 |
| Plugin activated/deactivated/configured (sitewide) | >=1 |
| Theme changed or template part updated (multi-page) | >=1 |
| Any change producing 404, redirect chain, or requiring rollback | >=1 |
| Yoast SEO config change (sitewide) | >=1 |
| Permalink structure change | >=1 |

---

## Duration

| Level | Duration | Purpose |
|-------|----------|---------|
| **Minimum** | 5 days (120h) | Initial crawl/index feedback |
| **Recommended** | 7 days (168h) | Full GSC weekly data |
| **Full evaluation** | 10-14 days | Complete click/impression assessment |

---

## Allowed during gate

- All WP REST API GETs
- All GSC queries
- aaron-seo-geo audit skills (read-only)
- Content planning and brief writing
- Draft posts (status: draft, not published)

## Blocked during gate

- Publishing new posts
- Updating published posts (title, content, meta)
- Adding new internal links (on published posts)
- Category/tag changes (affecting published posts)
- Plugin/theme changes
- Schema deployments (on published posts)
- Yoast SEO sitewide config changes
- Permalink changes
- Index/noindex operations
- Bulk operations

---

## Emergency exception (Technical Emergency)

During gate, emergency stabilization is allowed if ALL of:
1. Problem is a **technical emergency** (e.g., sitewide 404, index crisis, security issue affecting SEO)
2. Problem is **fixing breakage**, NOT optimizing
3. Clear diagnostic evidence exists
4. Each change is individually listed with rollback

**NOT qualifying:** "optimize the titles now", "add a few more internal links", "rankings dropped let's change meta"

---

## Re-evaluation after settlement

At least **3 of 5** must be completed:
1. GSC data pull (clicks/impressions/position vs pre-settlement baseline)
2. Live HTTP check on top 10-20 affected URLs
3. Yoast SEO field verification per affected post
4. New broken link scan
5. Content index status check

---

## Reference

Original model: [seo-survival-kit/SEO_SETTLEMENT_GATE.md](https://github.com/maxschottke-spec/seo-survival-kit)
