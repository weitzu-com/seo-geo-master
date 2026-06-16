# Change History NDJSON Format

## Format

One JSON object per line, append-only. No file size limit — user rotates periodically.

## Fields

```json
{
  "change_id": "wp-change-001",
  "timestamp": "2026-06-16T10:30:00Z",
  "mode": "micro_fix",
  "type": "yoast_title_update",
  "wp_post_id": 42,
  "url": "/blog/example/",
  "change_category": "repair_hygiene",
  "description": "Fixed title tag to include primary keyword",
  "before_state": "Old Title | Site Name",
  "after_state": "Primary Keyword: Old Title | Site Name",
  "risk_points": 1,
  "data_sources": ["wp_get_post", "wp_get_yoast_seo"],
  "confidence": "high",
  "hypothesis_id": null,
  "hypothesis_status": null,
  "rollback_method": "wp_update_yoast_seo with original title",
  "qa_status": "success",
  "settlement_gate_triggered": false
}
```

## Change type enum

| Type | Description |
|------|-------------|
| `yoast_title_update` | SEO title update |
| `yoast_description_update` | Meta description update |
| `yoast_focus_keyword_update` | Focus keyword update |
| `yoast_full_update` | Multiple Yoast fields |
| `post_content_update` | Post content update |
| `post_title_update` | Post title update |
| `post_slug_update` | Post slug/URL update |
| `post_status_change` | Post status change |
| `post_publish` | New post published |
| `category_create` / `tag_create` | Category/tag creation |
| `category_update` / `tag_update` | Category/tag update |
| `media_alt_update` | Image alt text update |
| `internal_link_add` | Internal link addition |
| `schema_add` | Schema markup addition |
| `plugin_activate` / `plugin_deactivate` | Plugin status change |
| `theme_update` | Theme update |
| `settings_update` | Site settings change |
| `bulk_operation` | Batch operation |

## Change category enum

| Category | Description |
|----------|-------------|
| `repair_hygiene` | Repair/hygiene change |
| `structural` | Structural change |
| `emergency` | Emergency stabilization |

## QA status enum

| Status | Description |
|--------|-------------|
| `pending` | Awaiting QA |
| `success` | QA passed |
| `partial` | Partially successful |
| `failed` | QA failed, rollback needed |
| `rolled_back` | Successfully rolled back |
