# RAG #20 sources: Chunking tables (Chunking by doc type · Part 2/4)

Logged, not posted. Every example on the slides is re-run by `RAG20_verify.py` (prints ALL PASS).

## Libraries (installed and read with `inspect`, 17 Nov 2026)
- langchain-text-splitters 1.1.3
  - `RecursiveCharacterTextSplitter` default separators `["\n\n", "\n", " ", ""]`; with `chunk_size=300, chunk_overlap=0` a Markdown table splits on `\n` (whole rows), and a one-line HTML table (no `\n`, no spaces between cells) falls back to `""` (character cuts).
  - Source: https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters
- docling-core 2.107.1 (`docling-core[chunking]`)
  - `docling_core/transforms/chunker/hybrid_chunker.py`: `HybridChunker.repeat_table_header: bool = True`, `omit_header_on_overflow: bool = False`.
  - Docstring of `segment`: header rows are used as a prefix "reproduced at the top of every segment"; preamble text such as a caption "is stripped from every later segment that repeats the prefix"; when a body row is too wide to fit with the header, "the table is partitioned vertically (by columns)".
  - The default chunking serializer's table serializer is `TripletTableSerializer` (rows written as `Virginia, Tier = Hot.`); the slides use `MarkdownTableSerializer` through a `ChunkingSerializerProvider` subclass.
  - Tokenizer in the test: a word-count `BaseTokenizer` subclass (`len(text.split())`), since Hugging Face and tiktoken downloads were blocked in the run environment. Limits: 100 words (price table), 40 words (wide table).
  - Docs: https://docling-project.github.io/docling/examples/hybrid_chunking/
- rank_bm25 0.2.2 (`BM25Okapi`, default k1/b), tokens = lowercase `[a-z0-9]+`.
- SQLite (Python `sqlite3`), table `prices(region, tier, storage, egress, days)`.

## Test setup (all numbers on the slides)
- Sample table (made up for the demo): "Table 4: Storage prices per GB, 2026", 6 regions × 3 tiers = 18 rows, columns Region, Tier, Storage, Egress, Days. Markdown text 787 characters.
- Recursive splitter at 300: 4 chunks; chunk 1 = the title alone, chunk 2 = header + Virginia/Oregon rows, chunks 3–4 = bare rows. Frankfurt Cold row `| Frankfurt | Cold | 0.005 | 0.12 | 90 |` in chunk 3.
- Same table as one-line HTML at 300: 6 chunks; chunk 1 ends `per GB,`; chunk 2 ends `<td>0.004</td><td>`, chunk 3 starts `0.09</td>` (Virginia Cold egress).
- Row-group chunker (code on slide 6, exec'd by the verify script): 6 chunks at `max_chars=300`, one region each, 211–223 characters; title + header + separator lines = 102 characters (46–48% of each chunk).
- Docling HybridChunker, Markdown serializer, 100 words: 3 chunks; header in all; caption only in chunk 1; Frankfurt Hot ends chunk 1, Cool and Cold open chunk 2.
- Wide table (Region + Jan–Dec, 6 rows, caption "Table 5: GB stored per month, 2026"), 40 words: 7 chunks; Region column only in chunk 1, chunks 2–7 two month columns each.
- BM25, query "What is the egress price for cold storage in Frankfurt?": top hit chunk 3 (Frankfurt) for both the recursive chunks and the row groups.
- Query "Which region has the cheapest egress for the Cold tier?": 6 Cold rows, one per row-group chunk. SQL answer: Virginia 0.09 and Oregon 0.09 (a tie).
