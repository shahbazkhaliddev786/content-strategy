# Carousel renderer (format v3)

Turns one post's JSON into 1080×1350 PNG slides, one PDF (the LinkedIn document carousel) and a check report. It renders with headless Chrome through Playwright, using the fonts in `renderer/fonts/` (Archivo and JetBrains Mono, both under the SIL Open Font License).

```
python3 renderer/render.py ai_engineering/rag/slides/RAG15.json --out out/RAG15
python3 renderer/render.py ai_engineering/rag/slides/RAG16.json --out out/RAG16 --cover-labels ai_engineering/rag/COVER_LABELS.md
```

Output: `slide_01.png` … `slide_NN.png`, `<post>.pdf`, `report.json`, `deck.html`. The script exits with code 1 when any check fails, and `report.json` lists the failures.

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
- `slides`: 6 to 8 slides. The first is the cover and the last is the cheat sheet.

### Slide types

| Type | Fields | Rules |
|---|---|---|
| `cover` | `title`, `hook` | `title` is copied exactly from `COVER_LABELS.md`: `[word]` is the yellow highlight and ` / ` is a line break. `hook` is one sentence naming the problem and what the slides give. |
| `body` | `title`, `text`, `visuals`, `after` | `title` states the slide's point, at most 2 lines with one `[highlight]`. `text` and `after` together are at most 40 words. Wrap code in backticks. |
| `cheatsheet` | `title`, `rows` | `title` is `[Cheat] sheet`, `[Checklist]` or `Decision [rule]`. 3 to 6 rows, each 8 words or fewer where possible. |

### Visuals (body slides)

| Kind | Fields | Use it for |
|---|---|---|
| `code` | `label` (optional), `code` | A real call or config. `{{x}}` highlights the part the slide is about. Use `\n` for line breaks and keep lines under about 44 characters. |
| `chunks` | `state` (`bad` or `good`), `caption`, `chunks`, `cut` (optional), `cut_label`, `verdict` (optional) | Showing how text gets split. `!!x!!` emphasises x, in red on a bad cut and green on a good one. `cut: 1` draws the cut line after chunk 1. |
| `cascade` | `steps`: `[{"code", "label", "note"}]` | An ordered fallback or pipeline, drawn top to bottom with arrows. |

A body slide can stack two visuals, for example a `code` block followed by a `good` `chunks` view.

## Checks

The renderer fails the post when:

- it has fewer than 6 or more than 8 slides
- a title doesn't fit its lines at the minimum size (cover 120px, body 76px)
- the content doesn't fit, even after shrinking to 80%
- any text is smaller than 24px, or crosses the slide margins
- a body slide has more than 40 words of text
- with `--cover-labels`: the cover title or the mini-series line differs from `COVER_LABELS.md`

## Design tokens

| Token | Value | Used for |
|---|---|---|
| Paper | `#ffffff` | Slide background |
| Ink | `#000000` | Titles, code panels, the module label |
| Graphite | `#45454d` | Body text, labels, footers |
| Mist | `#f2f2f0` | Chunk panels, inline code |
| Highlight | `#ffde59` | The one highlighted word, code strings, the current mini-series part |
| Signal red / green | `#d4312b` / `#1d8048` | Bad cut / good result, only in chunk views |

Type: Archivo (variable; titles at weight 850–860 and 74–76% width, body at 430), JetBrains Mono for code. One highlighted word per title, sentence case everywhere, no doodles, progress strip at the bottom right.
