# Pillar 2 — Content Calendar: Module 1 (Document Ingestion & Parsing)

**Source:** `RAG_Curriculum (1).md` → Module 1
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 1 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 1 has 5 concepts → 7 posts (2 mini-series).**
**Key terms to cover (8):** `OCR (Optical Character Recognition)` · `Layout parsing` · `Document AI / structure extraction` · `Table serialization` · `Multi-modal RAG` · `Change data capture (CDC)` · `Incremental ingestion` · `ETL/ELT for unstructured data`

---

## Post 1 — Getting content in: source connectors

**Concept:** Source connectors — file systems, wikis, DBs, APIs, crawlers.

**Angle:** Before any clever retrieval, you have to *get the content in*. This is the front door of ingestion: pulling raw documents from wherever they live (shared drives, Confluence/Notion, SQL tables, SaaS APIs, web crawls) and landing them in your pipeline. Frame it as the extract/load step adapted for messy, unstructured sources — not clean rows.

**Key terms covered here:**
- `ETL/ELT for unstructured data` *(primary)* — the extract → (transform) → load pattern, reframed for documents instead of database rows; connectors are the "extract."

**Senior-level tie-in:** the connector layer decides your freshness ceiling and what you can *ever* answer — you can't retrieve what you never ingested.

---

## Post 2 — Every file format breaks differently *(mini-series · 2 parts)*

**Concept:** Parsing heterogeneous formats — PDF (text vs. scanned/OCR), HTML, DOCX, code, tables, images.

**Angle:** A RAG pipeline eats PDFs, HTML, DOCX, source code, spreadsheets, scans — and each fails in its own way. A digital PDF has extractable text; a scanned one is just pixels and needs OCR. Tables flatten into gibberish unless you serialize them deliberately. The parser you choose silently decides what's even answerable downstream.

**Series structure:** the two format problems that most often destroy answerability each get their own post — scanned content (OCR) and tables (serialization).

**Senior-level tie-in (series):** this is the module's bar — explain why a PDF parser choice changes retrieval quality (lose table structure → lose answerability).

### Post 2.1 — Scanned PDFs are just pixels: OCR

**Concept:** OCR for scanned and image-based documents.

**Angle:** A digital PDF carries a text layer; a scanned PDF, a photo, or a fax is only an image — a text extractor returns nothing, and the document silently vanishes from your index. OCR turns those pixels back into machine-readable text. Cover how to detect when a page needs it, and the failure modes it brings (misread characters, broken reading order, lost tables).

**Key terms covered here:**
- `OCR (Optical Character Recognition)` *(primary)* — turning scanned/image documents into machine-readable text.
- `Document AI / structure extraction` *(reinforced)* — introduce it as the smarter alternative to naive text dumps (developed fully in Post 3).

**Senior-level tie-in:** check for a text layer before running OCR — OCR on a digital PDF adds cost and errors; skipping it on a scanned one silently drops the document.

### Post 2.2 — Tables turn into word soup: table serialization

**Concept:** Serializing tables so their meaning survives into embeddings.

**Angle:** Extract a table as plain text and the rows and columns collapse into a stream of numbers with no headers attached — "42" no longer knows it means Q3 revenue for the EU. Table serialization rewrites the 2-D structure as text (Markdown, CSV, HTML, or one sentence per row with its headers) so each value keeps its meaning when embedded and retrieved.

**Key terms covered here:**
- `Table serialization` *(primary)* — converting a 2-D table into a text form (Markdown/CSV/HTML) that preserves row–column meaning for embedding.

**Senior-level tie-in:** lose table structure → lose answerability; pick a serialization that keeps headers attached to each value, and test it against real table questions.

---

## Post 3 — Layout-aware parsing vs. naive text extraction

**Concept:** Layout-aware parsing vs. naive text extraction.

**Angle:** Naive `getText()` reads a document like a firehose — it drops reading order, merges columns, and turns tables into word soup. Layout-aware parsing understands the *page*: headings, columns, reading order, table cells, figure captions. Show a side-by-side of the same PDF parsed both ways.

**Key terms covered here:**
- `Layout parsing` *(primary)* — parsing that preserves the visual/structural layout (reading order, columns, blocks), not just raw characters.
- `Document AI / structure extraction` *(primary)* — model-driven extraction of document structure (titles, sections, tables, key-value pairs) into a usable schema.
- `Table serialization` *(reinforced)* — shown as a payoff of layout awareness: correct cell boundaries → clean serialization.

**Senior-level tie-in:** structure preserved at parse time is structure you can chunk and retrieve on later; structure lost here is unrecoverable downstream.

---

## Post 4 — When the answer is in the chart, not the text *(mini-series · 2 parts)*

**Concept:** Handling multi-modal content — images, charts, tables embedded in documents.

**Angle:** Half the signal in real documents isn't prose — it's a chart, a diagram, a screenshot, a scanned figure. Text-only pipelines silently throw it away, so the model can never answer questions about it. Cover the options: OCR the text inside images, caption/describe images with a vision model, or embed images directly for multi-modal retrieval.

**Series structure:** the OCR route is covered in Post 2.1; this series gives the two image-native routes their own posts — describe the image as text, or embed the image itself.

**Senior-level tie-in (series):** decide *per content type* whether to OCR, caption, or embed — there's no single right answer, and the wrong one drops answerable content.

### Post 4.1 — Describe it in words: captioning images with a vision model

**Concept:** Converting images and charts into text descriptions with a vision model at ingest time.

**Angle:** A chart has almost no extractable text, but a vision model can describe it: "Bar chart: Q3 revenue up 18%, EU largest region." Store that description as a regular text chunk and the image becomes searchable through your existing text pipeline — no new index needed. The trade-off: the description is only as good as the captioner, and details it skips are gone.

**Key terms covered here:**
- `Multi-modal RAG` *(primary)* — RAG that ingests and retrieves over non-text modalities (images, charts, tables) alongside text.
- `OCR` *(reinforced)* — the cheaper route when an image is mostly text (a screenshot of a paragraph); captioning is for when meaning lives in the visual.
- `Table serialization` *(reinforced)* — embedded tables are a multi-modal case; serialize them so they survive into retrieval.

**Senior-level tie-in:** captioning keeps one text index and one retrieval path — the simplest multi-modal option — but you pay a vision-model call per image at ingest.

### Post 4.2 — Embed the image itself: direct multi-modal retrieval

**Concept:** Embedding images directly into a shared text–image vector space.

**Angle:** Instead of turning an image into words, embed the image itself with a multi-modal embedding model, so a text query like "diagram of the ingestion pipeline" lands near the matching picture. Nothing is lost to a captioner's summary, but you now run a second embedding model, and the generator needs to be able to read images when they're retrieved.

**Key terms covered here:**
- `Multi-modal RAG` *(reinforced)* — the full version: retrieval over images as images, not as text proxies.

**Senior-level tie-in:** choose direct embedding when visual detail matters and a caption would lose it; choose captioning when you want one simple text pipeline (embedding models covered in Module 3).

---

## Post 5 — Ingestion is never "done": versioning & change detection

**Concept:** Document versioning and change detection at the source.

**Angle:** Documents change — pages get edited, rows update, files get deleted. A pipeline that only does a one-time bulk load goes stale fast and serves outdated answers. The fix is detecting *what changed* at the source and updating only those pieces, instead of re-crawling and re-embedding everything nightly.

**Key terms covered here:**
- `Change data capture (CDC)` *(primary)* — detecting and streaming source-side changes (inserts/updates/deletes) so the index can react.
- `Incremental ingestion` *(primary)* — re-processing only new/changed documents rather than the whole corpus.
- `ETL/ELT for unstructured data` *(reinforced)* — close the loop from Post 1: the pipeline runs continuously, not once.

**Senior-level tie-in:** freshness-at-scale is a cost problem — full re-indexing doesn't scale, so CDC + incremental ingestion is what keeps a production index both current and affordable.

---

## Coverage check (all 8 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `OCR (Optical Character Recognition)` | Post 2.1 | Post 4.1 |
| `Table serialization` | Post 2.2 | Posts 3, 4.1 |
| `Layout parsing` | Post 3 | — |
| `Document AI / structure extraction` | Post 3 | Post 2.1 |
| `Multi-modal RAG` | Post 4.1 | Post 4.2 |
| `Change data capture (CDC)` | Post 5 | — |
| `Incremental ingestion` | Post 5 | — |
| `ETL/ELT for unstructured data` | Post 1 | Post 5 |

✅ All 8 Module 1 key terms covered across the 7 posts.
