# Content System — Context & Decisions

Single source of context for Shahbaz Khalid's daily AI-engineering content system. Upload this file to the project, alongside `carousel-prompt-v2.md`, `content_rubric.md` and `KEYWORD_AND_AI_SEARCH_PLAYBOOK.md`.

**Every post follows `KEYWORD_AND_AI_SEARCH_PLAYBOOK.md`** (primary keyword, AI-search writing rules, hashtags, pre-publish checks).

_Last updated: 5 Nov 2026_

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
- **Format v3 (in progress, Nov 2026; not live yet).** Slides are rendered from post JSON by `renderer/render.py` (HTML/CSS + headless Chrome), not Canva. Rules: `renderer/README.md`; covers: `ai_engineering/rag/COVER_LABELS.md`; every post follows `KEYWORD_AND_AI_SEARCH_PLAYBOOK.md`.
  - **LinkedIn: 10–15 pages** as one PDF document: cover (module label, mini-series line, topic title, hook, "Inside" list) → body slides → cheat sheet → **next-day teaser** (the next post's module label, mini-series line and cover title from `COVER_LABELS.md`, plus one linking line). LinkedIn allows up to 300 pages; 10–15 is our choice.
  - **Instagram: at most 10 slides**, because Buffer publishes at most 10 images per Instagram carousel (Instagram's own app allows 20). Body slides marked `"instagram": false` are left out; the cover, cheat sheet and teaser always stay.
  - Dense slides: a lead, a visual with real outputs (code, chunk views, settings side by side, steps, use/move-on cards) and up to 3 bullets; at most 85 words of reading text per slide; nothing under 24px.
  - Every example output is real and re-checked by a script kept next to the post (for example `ai_engineering/rag/slides/RAG15_verify.py`).
- Canva template: **"My final content template"** (1080×1350, 4:5), design ID `DAHUJv5JM8k`. Pages: 1 cover, 2–6 body, 7 teaser.
- **Format v2 (from RAG #12, Nov 1 2026; decided in the Oct 31 2026 audit).** Full writing rules: `carousel-prompt-v2.md`; review rubric: `content_rubric.md`.
  - 6–8 slides: cover (technique kicker + hook ≤ 8 words) → 4–6 body slides shaped by the post type (failure → fix, decision guide, mechanism, comparison) → a cheat sheet, checklist or decision rule last.
  - Body 25–35 words (max 40), one idea per slide, no closing slogans, no gold phrase.
  - No agenda slide, no Key Terms glossary, no "Next:" teaser slide; terms are defined inline.
  - A research step verifies every tool/API name and number against official docs; nothing invented, no first-person experience claims.
  - A separate rubric review runs before publishing; the hooks log keeps hooks from repeating.
  - Canva build: copy template pages 1–6 (never page 7); add the kicker as a text box on the cover; for 7–8 slides insert extra body pages from template page 2.
- **Format v1 (RAG #01–#11):** Hook → What You'll Learn → Problem → Intuition → How It Works → Key Terms → Trade-offs → When To Use It → When To Skip It → Teaser; body 45–60 words with a gold phrase at the end. Rules in `carousel-prompt.md`. Retired after #11: the audit found it read as a template and pushed toward overclaims.
- **Both formats:** only "Shahbaz Khalid" top-left; no series label; no website; one yellow-highlighted word per title; no orphan words.
- **Delivery:** every slide is its own image, in swipe order; LinkedIn gets the slides as one PDF.

## 4. Captions
- **v2:** the caption shape rotates (story, claim, checklist preview); never "In this carousel:". LinkedIn: the first 2 lines name the technique, one practitioner question, exactly 3 on-topic hashtags, no links. Instagram: the same text, 3–5 hashtags. Facebook: 2–3 lines + the question. X: 3–5 tweets, each ≤ 280 characters.
- **v1 (to #11):** LinkedIn hook within ~200 characters, 3 takeaways, the insight, a practitioner question, 3–5 hashtags; Instagram adds "Save this for your next build."; Facebook short and warm; X 5–8 tweet thread.

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
- Each run: read the next topic from `SERIES_ORDER.md` → write slides and captions (v1: `carousel-prompt.md`; v2 from #12: research, `carousel-prompt-v2.md`, the last 10 rows of `ai_engineering/rag/hooks_log.md`, a `content_rubric.md` review) → build in Canva → export → post → append a row to `posted.md` (and, from v2, to `hooks_log.md`).
- Failure alerts go out by push/email. A warning comes about a week before the topic queue runs out.

## 7. Status (31 Oct 2026)
- ✅ RAG #01–#11 posted daily since Oct 21 (format v1)
- ✅ Content audit done (Oct 31): [RAG Carousel Content Audit](https://claude.ai/artifact/Vc98XHW2sMrqrzvVSqoytw). Baseline: LinkedIn median 66 impressions per post; X, Facebook and Instagram close to zero; 0 profile views and 0 followers from #06–#08.
- ✅ Format v2 approved (Oct 31): runs from RAG #12 (Nov 1). RAG #14 was built and approved in advance (`ai_engineering/rag/ready/RAG14.md`, Canva DAHZkN_7xHg).
- ⏳ Profile update (banner, headline, Featured) by the user
- ⏸ Daily run paused on Nov 4 2026 (after RAG #15) while format v3 is built: topic-first covers from `ai_engineering/rag/COVER_LABELS.md` and the keyword playbook. Next post: RAG #16.

## 8. Decisions log
- Slides use the 7-part body structure for every strategy; mini-series for multi-strategy topics (v1; replaced by format v2 from #12)
- X Premium: test after 2–3 weeks of free-account data (payouts likely unavailable in Pakistan via Stripe)
- Slide 10's subtext uses a different font (a Canva connector limit); fix manually or drop the line
- Oct 31 2026 audit decisions: daily posting continues (no pause); format v2 from #12, starting Nov 1 (cover kicker, no agenda/glossary/teaser/slogans, 25–35-word slides, cheat-sheet last slide, rotating captions, research + rubric review); no creator benchmarks; no personal-experience input for now; curriculum order unchanged. Channels: keep all 4 (LinkedIn, Instagram, Facebook, X) as they are. Pending: weekend review loop, visual slides (cycle 2), posting-time test (cycle 3).
- Posts in `ai_engineering/rag/ready/RAG<NN>.md` are pre-built and reviewed (or approved by Shahbaz); the daily run posts them verbatim.
- Nov 4 2026 review: reach stayed flat (LinkedIn about 71 impressions per post; Instagram, X and Facebook near zero). Covers didn't say what the post was about, so v3 covers show the module label, the mini-series line with its part number, the post's topic as the big title, and the hook as a smaller line underneath.
- Nov 5 2026: every post follows `KEYWORD_AND_AI_SEARCH_PLAYBOOK.md`, based on the research doc [AI engineering on LinkedIn: trending keywords and AI search](https://claude.ai/artifact/VedncmQoYK8jx8WLCrsq4e).
- Nov 5 2026 (Shahbaz): `COVER_LABELS.md` approved. Keep all 4 channels (LinkedIn, Instagram, Facebook, X); fully automatic posting at 8:00 AM PKT, 7 days a week.
- Nov 5 2026 (Shahbaz): v3 slides carry more content (about 50 words per body slide instead of 20). LinkedIn documents run 10–15 pages and end with a next-day teaser slide, which brings back the teaser the Oct 31 audit removed. Instagram stays at 10 slides, Buffer's limit for Instagram carousels.
- Success measures for cycle 1 (Nov 1–14): median LinkedIn impressions at 72 h ≥ 100 (baseline 66), ≥ 1 save or send per post, engagement ≥ 4% (baseline 2.3%).
