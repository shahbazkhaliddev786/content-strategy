# Carousel renderer (format v3)

Turns one post's JSON into the LinkedIn document (one PDF, 10–15 pages), the Instagram slide set (at most 10 PNGs) and a check report. It renders with headless Chrome through Playwright, using the fonts in `renderer/fonts/` (Archivo and JetBrains Mono, both under the SIL Open Font License).

```
python3 renderer/render.py ai_engineering/rag/slides/RAG15.json --out out/RAG15
python3 renderer/render.py ai_engineering/rag/slides/RAG16.json --out out/RAG16 --cover-labels ai_engineering/rag/COVER_LABELS.md
```

Output:

- `linkedin/`: every slide as `slide_01.png` … plus `<post>.pdf`, the file posted to LinkedIn as a document.
- `instagram/`: at most 10 slides, re-rendered so the progress strip counts only them. Buffer publishes at most 10 images per Instagram carousel (Instagram's own app allows 20).
- `report.json`: the checks for both sets.

The script exits with code 1 when any check fails, and `report.json` lists the failures.

## Post JSON

```json
{
  "post": "RAG #16",
  "module": "RAG chunking",
  "topic": "Semantic chunking",
  "series": null,
  "slides": []
}
```

- `module`: the module label, the section heading in `COVER_LABELS.md`.
- `topic`: the post's topic in plain words. It appears in the body-slide footers and on the cheat sheet.
- `series`: `null`, or `{"name": "Small-to-big", "part": 1, "of": 2}` for a mini-series post.
- `slides`: 10 to 15 for LinkedIn, in this order: the cover, body slides, the cheat sheet, then the next-day teaser. Use 12–15 only when the topic needs it.
- `"instagram": false` on a body slide leaves it out of the Instagram set. Leave out enough body slides that Instagram has at most 10; the cover, cheat sheet and teaser always stay. Don't leave out a slide the cover's `inside` list promises.

### Slide types

| Type | Fields | Rules |
|---|---|---|
| `cover` | `title`, `hook`, `inside` (optional) | `title` is copied exactly from `COVER_LABELS.md`: `[word]` is the yellow highlight and ` / ` is a line break. `hook` is one or two short sentences: the answer first, then the problem. `inside` is 3 short lines saying what the slides cover. |
| `body` | `title`, `text`, `visuals`, `bullets`, `after` | `title` states the slide's point, at most 2 lines with one `[highlight]`. `text` is the lead (1 to 3 lines). All reading text on the slide (lead, bullets, steps, notes, card items, after) is at most 85 words; code and example chunks don't count. Wrap code in backticks. |
| `cheatsheet` | `title`, `rows` | `title` is `[Cheat] sheet`, `[Checklist]` or `Decision [rule]`. 4 to 7 rows, each one line where possible. |
| `teaser` | `label`, `module`, `series`, `title`, `line` | The next post. With `--cover-labels`, `module`, `series` and `title` are filled from the next row of `COVER_LABELS.md` and checked against it. `label` is "Tomorrow" by default; set it to the day (for example "Monday") when the next post isn't the next day. `line` is one or two short sentences linking today's topic to the next one. No post numbers. |

### Visuals (body slides)

| Kind | Fields | Use it for |
|---|---|---|
| `code` | `label` (optional), `code` | A real call or config. `{{x}}` highlights the part the slide is about. Use `\n` for line breaks and keep lines under about 44 characters. |
| `chunks` | `state` (`bad` or `good`), `caption`, `chunks`, `cut` (optional), `cut_label`, `verdict` (optional) | Showing how text gets split. `!!x!!` emphasises x, in red on a bad cut and green on a good one. `cut: 1` draws the cut line after chunk 1. |
| `cascade` | `steps`: `[{"code", "label", "note"}]` | An ordered fallback or pipeline, drawn top to bottom with arrows. |
| `steps` | `steps`: list of strings | A real sequence (an algorithm, a setup), numbered and joined by a line. 3 to 6 steps. |
| `variants` | `caption`, `options`: `[{"setting", "tag", "output", "state", "note"}]` | The same input under different settings, each with its real output. `state` is `good`, `bad` or `neutral`. |
| `cards` | `cards`: `[{"state", "title", "items"}]` | "Use it when" / "Move on when" lists. 2 cards, 3 or 4 items each. |

`chunks` also takes `label` (above the panel), `cut` as a list (`[1, 2]` draws a cut after chunks 1 and 2), chunks as `{"text", "meta"}`, line breaks inside a chunk (`\n`), and `"compact": true` for slides with two panels.

A body slide can stack two visuals, for example a `code` block followed by a `variants` view. `bullets` (2 or 3 lines) go below the visuals.

## Checks

The renderer fails the post when:

- LinkedIn has fewer than 10 or more than 15 slides, or Instagram has more than 10
- the slides aren't in the order cover → body → cheat sheet → teaser
- with `--cover-labels`: the teaser is missing while `COVER_LABELS.md` has a next post, or its module, mini-series line or title differ from that row
- a title doesn't fit its lines at the minimum size (cover 120px, body 72px)
- the content doesn't fit, even after shrinking to 80%
- any text is smaller than 24px, or crosses the slide margins
- a body slide has more than 85 words of reading text
- with `--cover-labels`: the cover title or the mini-series line differs from `COVER_LABELS.md`

## Design tokens

| Token | Value | Used for |
|---|---|---|
| Paper | `#ffffff` | Slide background |
| Ink | `#000000` | Titles, code panels, the module label |
| Graphite | `#45454d` | Body text, labels, footers |
| Mist | `#f2f2f0` | Chunk panels, inline code |
| Highlight | `#ffde59` | The one highlighted word, code strings, the current mini-series part |
| Signal red / green | `#d4312b` / `#1d8048` | Bad / good results: chunk views, variants, cards |

Type: Archivo (variable; titles at weight 850–860 and 74–76% width, body at 430), JetBrains Mono for code. Body sizes: lead 38px, bullets and steps 35–37px, code 30px, labels 26–30px; the fitter shrinks a crowded slide to 80% at most, and nothing goes under 24px. Hyphenated words never break at the hyphen. One highlighted word per title, sentence case everywhere, no doodles, progress strip at the bottom right.
