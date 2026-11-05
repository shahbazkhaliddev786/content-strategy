# Content rubric — review before publishing (format v3)

Used by the daily run from RAG #16 onward (format v3; RAG #12–#15 used the v2 checks). A reviewer that did not write the post (a fresh subagent where available) scores the draft from the slide text and captions only, as a working software/ML engineer or technical founder scrolling LinkedIn on a phone.

Calibration: 3 = a competent, average technical LinkedIn post · 5 = among the best technical posts of the year · 1 = actively weak.

## Criteria (score 1–5)

| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| Stop power (cover + first 2 caption lines) | a line anyone could post | a clear claim with some tension | a pain the target reader has felt, with an open loop |
| Topic in 1 second (cover alone) | can't tell which technique | implied | names the technique and the problem it solves |
| Insight | restates top search results | one non-obvious point | several points a working engineer would save |
| Proof | abstract prose | a concrete example in words | shows it: code, output, before/after, diagram |
| Human voice | many AI tells; could be anyone | a few tells, some opinion | a specific engineer: concrete detail, a stance with reasons |
| Structure fit | template forces filler slides | mostly fits | every slide earns its place |
| Mobile read | walls of text | readable | each slide scans as title → lead → visual → up to 3 bullets |
| Standalone | needs other posts | mostly | complete for someone seeing it cold |
| Save-worthy | nothing to keep | one takeaway | a reusable checklist, decision table or snippet |

**Accuracy (gate):** any wrong or overclaimed technical statement, invented number or unverifiable API name fails the post. Quote it and give the correction.

## Mechanical checks (each must pass)
- 10–15 slides for LinkedIn and at most 10 for Instagram, in the order cover → body → cheat sheet → teaser.
- The cover's module label, mini-series line and title match COVER_LABELS.md; the teaser matches the next row.
- Each body slide has at most 85 words of reading text and at least one visual; every example output comes from a real run (RAG<NN>_verify.py prints ALL PASS).
- The cover's "Inside" list only promises slides that Instagram also gets.
- No agenda slide or glossary slide.
- None of the banned patterns in carousel-prompt-v3.md (VOICE).
- Hook differs from the last 10 in hooks_log.md (opening word and pattern).
- Caption has no "In this carousel:"; exactly 3 LinkedIn hashtags, all on-topic; every tweet ≤ 280 characters.

## Pass rule
Pass = every criterion ≥ 3, accuracy pass, all mechanical checks pass. Otherwise return the top 3 fixes; the writer revises once and the review runs again. Two failed reviews → post nothing and report the failure.

## Reviewer output
```
SCORES: stop_power=_ topic_1s=_ insight=_ proof=_ human_voice=_ structure_fit=_ mobile_read=_ standalone=_ save_worthy=_
ACCURACY: pass | fail — <quote> → <correction>
MECHANICAL: pass | fail — <which>
VERDICT: pass | revise
TOP FIXES: 1. … 2. … 3. …
```
