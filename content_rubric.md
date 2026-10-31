# Content rubric — review before publishing (format v2)

Used by the daily run from RAG #14 onward. A reviewer that did not write the post (a fresh subagent where available) scores the draft from the slide text and captions only, as a working software/ML engineer or technical founder scrolling LinkedIn on a phone.

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
| Mobile read | walls of text | readable | 2–3 seconds per slide |
| Standalone | needs other posts | mostly | complete for someone seeing it cold |
| Save-worthy | nothing to keep | one takeaway | a reusable checklist, decision table or snippet |

**Accuracy (gate):** any wrong or overclaimed technical statement, invented number or unverifiable API name fails the post. Quote it and give the correction.

## Mechanical checks (each must pass)
- 6–8 slides; cover has a kicker naming the technique; hook ≤ 8 words.
- Each body slide 25–40 words; last slide is a cheat sheet, checklist or decision rule.
- No agenda slide, glossary slide or "Next:" teaser slide.
- None of the banned patterns in carousel-prompt-v2.md (VOICE).
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
