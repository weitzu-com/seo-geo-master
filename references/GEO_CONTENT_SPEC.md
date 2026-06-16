# GEO Content Specification

> The essence of GEO: make AI assistants cite your content as a trusted source when answering user questions.

---

## Why AI cites you (first principles)

AI citation decisions follow one logic: **"Does this information help me answer the user's question better?"**

GEO starts NOT with format tricks, but with:
1. **Information density** — do you have unique information competitors lack?
2. **Fact accuracy** — can every stat be traced to an authoritative source?
3. **Structure clarity** — can AI determine in 2 seconds what kind of question this answers?
4. **Recency** — is the content recently updated with visible timestamps?

Format techniques serve credibility. Without substance, they're deception — and AI will learn to detect them.

---

## Four GEO elements

### 1. Citeable statistics (≥3 per article)
Format: number + unit + timeframe + source linked inline.

✅ Good: "According to [Backlinko 2025 study](url), the average #1 result also ranks in the top 10 for ~1,000 additional keywords."

❌ Bad: "Many sites struggle with rankings." (no number, no source)

### 2. Definition paragraphs (25-50 words)
For every core term, a crisp definition at its first occurrence.

✅ Good: "**GEO (Generative Engine Optimization)** is the practice of optimizing content structure, authority signals, and citation formats so AI platforms (ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude) cite and recommend it in their generated answers."

### 3. Content Capsules (≥60% of H2s)
Structure: question-title H2 → first sentence directly answers → remaining space expands.

✅ Good:
```
## How to improve WordPress AI citation rates?

The core method is combining structured data markup with citeable statistics and optimized llms.txt.

First, [detail expansion]...
```

### 4. Structured lists (≥1 per article)
Use ordered lists (steps, rankings), unordered lists (features, options), or tables (comparison data).

---

## AI platform citation factors

| Platform | Crawler | Highest citation preference |
|----------|---------|---------------------------|
| ChatGPT | GPTBot | Recency, clear sources, comparative data |
| Perplexity | PerplexityBot | Fact precision, direct answers, recent timestamps |
| Google AIO | Googlebot | E-E-A-T completeness, correct Schema, multi-source corroboration |
| Gemini | Google-Extended | Strong entity associations, knowledge graph alignment, depth |
| Claude | ClaudeBot | Logical rigor, traceable citations, clear methodology |

---

## GEO readiness checklist (per article)

- [ ] ≥3 citeable statistics with sources
- [ ] Core terms have 25-50 word definitions
- [ ] ≥60% H2s in Content Capsule format
- [ ] ≥1 structured list or table
- [ ] JSON-LD Schema correct (Article/FAQPage/HowTo)
- [ ] Open Graph + Twitter Card metadata complete
- [ ] Author page has Person Schema
- [ ] Internal link anchor text is contextual keywords
- [ ] Cited sources are authoritative domains
- [ ] llms.txt updated if site uses one
