# Hypothesis Verification Gate

> Adapted from [seo-survival-kit](https://github.com/maxschottke-spec/seo-survival-kit) under MIT License.

Every live WordPress change must be based on a verified root cause. No executing on "suspected" or "likely" guesses.

---

## 5-stage lifecycle

| Status | Meaning | Allowed actions |
|--------|---------|-----------------|
| `suspected` | Hypothesis formed, no verification | Read-only data pulls, planning |
| `likely` | Indirect evidence (GSC data, HTML inspection) | Same as suspected |
| `verified` | Confirmed against real WP data | Live fix permitted (subject to Governor + Settlement) |
| `fixed` | Fix deployed, QA passed | Monitoring |
| `monitored` | T+7 to T+14 post-deploy observation | Monitoring, follow-up |

---

## WP verification source hierarchy

### Strongest tier (single source sufficient for `verified`)
1. WP REST API direct state read (e.g., `wp_get_yoast_seo` confirming empty focus keyword)
2. GSC URL Inspection showing indexed state matching hypothesis
3. Server file direct inspection (operator/developer): plugin versions, theme config, `.htaccess` rules
4. Staging environment reproduction

### Strong tier (need 2+ sources)
5. Live HTTP check cross-validated against WP API state
6. WP Site Audit (`wp_site_audit`) output confirming issue
7. Screaming Frog / DataForSEO crawl data cross-validated against WP state

### Medium tier (need 3+ sources + operator confirmation)
8. Live HTML cross-check across 3+ page types
9. GSC performance data showing keyword/page-level anomaly
10. Plugin source code inspection (for open-source plugins)

### Weak tier (alone insufficient for `verified`, only supports `likely`)
11. Open-source code reading not verified on user's server
12. AI pattern matching ("looks like typical Yoast issue")
13. Timing correlation ("ranking drop happened right after plugin update")
14. AI reasoning chain (even if internally consistent)

---

## Verification workflow

```
Issue discovery (suspected)
  → Data collection: WP API, GSC, HTTP → likely
  → Cross-verification: WP API actual values vs GSC index state
    │ Match → verified │ Mismatch → stay at likely or drop to suspected
  → Deploy fix + QA → fixed
  → T+7~T+14 monitoring → monitored
    │ Recovery matches expectation → closed
    │ Partial recovery → open new hypothesis for remainder
    │ No recovery → re-open at suspected
```

---

## Scope expansion rule

If verified scope is specific URLs, planned changes beyond that:
- Over-scope portion → auto-reset to `likely`, blocked
- Verified-scope portion → may proceed

Example: verified that `/blog/seo-tips/` lacks focus keyword. Planned to also fix `/blog/schema-guide/` and `/blog/wp-speed/`. Result: only `/blog/seo-tips/` proceeds; others need independent verification.

---

## Integration with hard stops

From `SAFETY_GOVERNOR.md` 26 hard stops:
- **Stop 22**: Hypothesis not at `verified` → block fix
- **Stop 23**: Fix scope exceeds verified scope → block
- **Stop 24**: Verification from weak-tier sources only → block

---

## Reference

Original model: [seo-survival-kit/HYPOTHESIS_VERIFICATION_GATE.md](https://github.com/maxschottke-spec/seo-survival-kit)
