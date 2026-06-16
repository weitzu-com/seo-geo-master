# PDCA State Machine Specification

Six JSON/NDJSON files form the cross-session persistent state layer. All files carry `schema_version` for migration compatibility.

---

## File overview

| File | Type | Write mode | Owner phase |
|------|------|------------|-------------|
| `pdca-state.json` | JSON | Overwrite | All |
| `content-queue.json` | JSON | Overwrite | Plan/Do |
| `keyword-bank.json` | JSON | Overwrite | Plan |
| `change-history.ndjson` | NDJSON | Append | Act |
| `hypotheses.json` | JSON | Overwrite | Check/Act |
| `run-history.ndjson` | NDJSON | Append | All |

---

## 1. pdca-state.json

Master state: site info, PDCA cycle, per-phase workflows, triple safety gates, five-dimension scorecard, metrics snapshot.

```json
{
  "schema_version": "1.0.0",
  "site": { "url": "", "wp_connected": false, "gsc_connected": false, "last_audit_at": null },
  "pdca_cycle": { "cycle_id": "", "phase": "plan", "phase_started_at": null, "iterations_completed": 0, "phase_history": [] },
  "workflows": {
    "plan": { "keyword_research": {}, "competitor_analysis": {}, "serp_analysis": {}, "content_gap_analysis": {}, "gsc_opportunity_discovery": {} },
    "do": { "content_queue": {}, "geo_optimization": {}, "meta_tags": {}, "schema_markup": {}, "internal_linking": {} },
    "check": { "on_page_audit": {}, "technical_check": {}, "rank_tracking": {}, "gsc_performance": {}, "content_quality_audit": {}, "domain_authority_audit": {}, "wp_site_audit": {} },
    "act": { "fixes_applied": {}, "performance_report": {}, "alerts_configured": false }
  },
  "safety": {
    "governor": { "mode": "audit_only", "change_budget_total": 0, "change_budget_used": 0, "change_budget_remaining": 0, "hard_stops_triggered": [] },
    "settlement_gate": { "active": false, "reason": null, "started_at": null, "minimum_until": null },
    "hypothesis_verification": { "active_hypotheses": [], "verified_count": 0 }
  },
  "scorecard": { "道_intent": 0, "天_timing": 0, "地_tech": 0, "将_auth": 0, "法_system": 0, "combined": 0, "last_updated": null },
  "metrics_snapshot": { "taken_at": null, "gsc_clicks_7d": 0, "gsc_impressions_7d": 0, "gsc_avg_position": 0, "gsc_ctr": 0, "wp_posts_count": 0, "wp_pages_count": 0 }
}
```

## 2. content-queue.json

6-status lifecycle: `queued → in_progress → written/needs_review/skipped → published`

```json
{
  "schema_version": "1.0.0",
  "site_url": "",
  "items": [
    { "id": "cq-001", "status": "queued", "primary_keyword": "", "keyword_volume": 0, "keyword_difficulty": 0, "intent": "informational", "target_url_slug": "", "wp_category_ids": [], "wp_tag_ids": [], "geo_targets": [], "fan_out_cluster": [], "wp_post_id": null, "wp_published_at": null, "geo_optimized_at": null }
  ]
}
```

## 3. keyword-bank.json

```json
{
  "schema_version": "1.0.0",
  "keywords": [ { "keyword": "", "volume": 0, "difficulty": 0, "intent": "", "geo_relevance": "medium", "clusters": [], "used_in_post": null } ],
  "clusters": {}
}
```

## 4. change-history.ndjson (append-only)

One JSON object per line:
```json
{"change_id":"","timestamp":"","mode":"","type":"","wp_post_id":0,"url":"","change_category":"","description":"","before_state":"","after_state":"","risk_points":0,"data_sources":[],"confidence":"","hypothesis_id":null,"rollback_method":"","qa_status":"","settlement_gate_triggered":false}
```

## 5. hypotheses.json

5-stage lifecycle: `suspected → likely → verified → fixed → monitored`

```json
{
  "schema_version": "1.0.0",
  "hypotheses": [ { "id": "", "status": "suspected", "title": "", "urls_affected": [], "evidence_stack": [], "verification_source": null, "verification_source_tier": null, "verified_at": null, "fix_scope": [], "scope_matches_verified": false } ]
}
```

## 6. run-history.ndjson (append-only)

```json
{"run_id":"","timestamp":"","phase":"","sub_phase":"","skill_routed_to":"","result":"","artifacts":[],"warnings":[],"errors":[]}
```

---

## Atomic write convention

All JSON overwrites use: write to `.tmp` → `os.replace(.tmp, target)`. Never direct overwrite.
NDJSON uses `append` mode (`open(file, 'a')`).
