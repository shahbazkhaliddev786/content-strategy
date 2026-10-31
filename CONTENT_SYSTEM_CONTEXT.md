# Content System — Context & Decisions

Single source of context for Shahbaz Khalid's daily AI-engineering content system. Upload this file to the project, alongside `carousel-prompt-v2.md` and `content_rubric.md`.

_Last updated: 31 Oct 2026_

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
- Canva template: **"My final content template"** (1080×1350, 4:5), design ID `DAHUJv5JM8k`. Pages: 1 cover, 2–6 body, 7 teaser.
- **Format v2 (from RAG #14, decided in the Oct 31 2026 audit).** Full writing rules: `carousel-prompt-v2.md`; review rubric: `content_rubric.md`.
  - 6–8 slides: cover (technique kicker + hook ≤ 8 words) → 4–6 body slides shaped by the post type (failure → fix, decision guide, mechanism, comparison) → a cheat sheet, checklist or decision rule last.
  - Body 25–35 words (max 40), one idea per slide, no closing slogans, no gold phrase.
  - No agenda slide, no Key Terms glossary, no "Next:" teaser slide; terms are defined inline.
  - A research step verifies every tool/API name and number against official docs; nothing invented, no first-person experience claims.
  - A separate rubric review runs before publishing; the hooks log keeps hooks from repeating.
  - Canva build: copy template pages 1–6 (never page 7); add the kicker as a text box on the cover; for 7–8 slides insert extra body pages from template page 2.
- **Format v1 (RAG #01–#13):** Hook → What You'll Learn → Problem → Intuition → How It Works → Key Terms → Trade-offs → When To Use It → When To Skip It → Teaser; body 45–60 words with a gold phrase at the end. Rules in `carousel-prompt.md`. Retired after #13: the audit found it read as a template and pushed toward overclaims.
- **Both formats:** only "Shahbaz Khalid" top-left; no series label; no website; one yellow-highlighted word per title; no orphan words.
- **Delivery:** every slide is its own image, in swipe order; LinkedIn gets the slides as one PDF.

## 4. Captions
- **v2:** the caption shape rotates (story, claim, checklist preview); never "In this carousel:". LinkedIn: the first 2 lines name the technique, one practitioner question, exactly 3 on-topic hashtags, no links. Instagram: the same text, 3–5 hashtags. Facebook: 2–3 lines + the question. X: 3–5 tweets, each ≤ 280 characters.
- **v1 (to #13):** LinkedIn hook within ~200 characters, 3 takeaways, the insight, a practitioner question, 3–5 hashtags; Instagram adds "Save this for your next build."; Facebook short and warm; X 5–8 tweet thread.

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
- Each run: read the next topic from `SERIES_ORDER.md` → write slides and captions (v1: `carousel-prompt.md`; v2 from #14: research, `carousel-prompt-v2.md`, the last 10 rows of `ai_engineering/rag/hooks_log.md`, a `content_rubric.md` review) → build in Canva → export → post → append a row to `posted.md` (and, from v2, to `hooks_log.md`).
- Failure alerts go out by push/email. A warning comes about a week before the topic queue runs out.

## 7. Status (31 Oct 2026)
- ✅ RAG #01–#11 posted daily since Oct 21 (format v1)
- ✅ Content audit done (Oct 31): [RAG Carousel Content Audit](https://claude.ai/artifact/Vc98XHW2sMrqrzvVSqoytw). Baseline: LinkedIn median 66 impressions per post; X, Facebook and Instagram close to zero; 0 profile views and 0 followers from #06–#08.
- ⏳ Format v2 from RAG #14 (Tue Nov 3), after the user reviews a test build of #14
- ⏳ Profile update (banner, headline, Featured) by the user

## 8. Decisions log
- Slides use the 7-part body structure for every strategy; mini-series for multi-strategy topics (v1; replaced by format v2 from #14)
- X Premium: test after 2–3 weeks of free-account data (payouts likely unavailable in Pakistan via Stripe)
- Slide 10's subtext uses a different font (a Canva connector limit); fix manually or drop the line
- Oct 31 2026 audit decisions: daily posting continues (no pause); format v2 from #14 (cover kicker, no agenda/glossary/teaser/slogans, 25–35-word slides, cheat-sheet last slide, rotating captions, research + rubric review); no creator benchmarks; no personal-experience input for now; curriculum order unchanged. Pending: channel focus (Facebook/Instagram/X), weekend review loop, visual slides (cycle 2), posting-time test (cycle 3).
- Success measures for cycle 1 (Nov 3–16): median LinkedIn impressions at 72 h ≥ 100 (baseline 66), ≥ 1 save or send per post, engagement ≥ 4% (baseline 2.3%).
