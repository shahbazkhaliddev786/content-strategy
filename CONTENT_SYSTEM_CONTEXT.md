# Content System — Context & Decisions

Single source of context for Shahbaz Khalid's daily AI-engineering content system. Upload this file to the project, alongside `carousel-prompt.md`.

_Last updated: 20 Oct 2026_

---

## 1. Goal & positioning
- **Pillar 2 (technical content):** build authority, a following and inbound opportunities with founders and engineers.
- **Positioning:** "The AI engineer who explains the WHY, not just the HOW." Every post covers the intuition, why the technique exists, how it works, its trade-offs, when to use it and when NOT to.
- **Audience:** software/ML engineers and technical founders building with LLMs.
- **Voice:** confident practitioner, plain language, specific examples, no hype words, never begging for follows or likes.

## 2. Content source (GitHub)
- Repo: `shahbazkhaliddev786/content-strategy`, folder `ai_engineering/rag/`
- `MODULE_0…12_CALENDAR.md`: brief for each post (concept, angle, key terms, senior-level tie-in)
- `SERIES_ORDER.md`: **posting order, RAG #01 → RAG #114**
- `posted.md`: publish log. Next post = the row after the last logged one.
- `MASTER_INDEX.md`: module overview and counts
- **Mini-series rule:** a concept with several strategies (e.g. ANN: HNSW, IVF, PQ, LSH, ScaNN) becomes one post per strategy, sub-numbered `Post 2.1, 2.2…`, usually ending in a comparison post. 18 mini-series, 114 posts in total.
- Original post numbering never changes; `SERIES_ORDER.md` adds the global order on top.

## 3. Carousel format
- Canva template: **"My final content template"** (1080×1350, 4:5), design ID `DAHUJv5JM8k`
- Each post = a copy of the template, with body slides added or removed to fit the topic (6–10 slides, max 10; longer topics split into Part 1/Part 2).
- **Structure:** Hook → What You'll Learn → Problem → Intuition → How It Works → Key Terms → Trade-offs → When To Use It → When To Skip It → Teaser ("Next: …")
- **Design rules:** only "Shahbaz Khalid" top-left; no series label; no website; one yellow-highlighted word per title; one gold phrase per body (at the end); body 45–60 words; no big empty areas; no orphan words.
- **Delivery:** every slide is its own image, in swipe order; LinkedIn gets the slides as one PDF.
- Full writing rules: see `carousel-prompt.md`.

## 4. Captions
- **LinkedIn:** hook within ~200 characters, 3 takeaways, the insight, a practitioner question, 3–5 hashtags, no links
- **Instagram:** same as LinkedIn, plus "Save this for your next build.", 3–5 hashtags
- **Facebook:** short and warm, ending in the question, 1–3 hashtags
- **X:** 5–8 tweet thread, **each tweet ≤280 characters**, slide 1 image on tweet 1, 1–2 hashtags

## 5. Publishing stack (all free tiers)
| Platform | Posted via | Format |
|---|---|---|
| X (@shahbazkhalid78) | Buffer | Thread |
| LinkedIn (Shahbaz Khalid) | Buffer | PDF document carousel |
| Instagram (@shahbazkhalid007, Business) | Buffer | Image carousel |
| Facebook Page | Metricool (brand "Agentic AI Systems") | Image post |

- Buffer free plan: 3 channels, 10 queued posts per channel, ~3,000 API calls/month. The Buffer MCP connector is connected.
- Instagram posts made through Buffer do **not** auto-share to Facebook, which is why Facebook goes through Metricool.
- Canva export links expire after 24h, so each run exports and posts immediately.
- Typefully is connected but not needed (its free tier allows 10 posts/month).

## 6. Schedule
- Daily at **8:00 AM PKT**, fully automatic once approved.
- Each run: read the next topic from `SERIES_ORDER.md` → write slides and captions with `carousel-prompt.md` → build in Canva → export → post to all 4 platforms → append a row to `posted.md`.
- Failure alerts go out by push/email. A warning comes about a week before the topic queue runs out.

## 7. Status (20 Oct 2026)
- ✅ Repo restructured and merged (PR #1: mini-series, 114 posts)
- ✅ Buffer, Metricool and Canva connected and tested (draft posts only)
- ✅ RAG #01 sample built in Canva: "RAG #01 — What problem does RAG actually solve?"
- ⏳ Approve the RAG #01 sample → save and export → first live post
- ⏳ Create the daily 8 AM scheduled task → turn on "Automatically approve"

## 8. Decisions log
- Slides use the 7-part body structure for every strategy; mini-series for multi-strategy topics
- X Premium: test after 2–3 weeks of free-account data (payouts likely unavailable in Pakistan via Stripe)
- Slide 10's subtext uses a different font (a Canva connector limit); fix manually or drop the line
