# RAG #22 sources — Chunking transcripts: keep the conversation turns together

Logged, not posted. Every example output on the slides is re-checked by `RAG22_verify.py` (prints ALL PASS).

## Libraries and versions
- `langchain-text-splitters` 1.1.3 — `RecursiveCharacterTextSplitter`. Default separators `["\n\n", "\n", " ", ""]` (checked in the verify script). Docs: https://python.langchain.com/docs/how_to/recursive_text_splitter/
- Overlap behaviour: read from the installed source, `TextSplitter._merge_splits` in `langchain_text_splitters/base.py` (1.1.3). After a chunk is emitted, it drops splits from the front while the kept total is over `chunk_overlap`, so a split (here, a whole speaker turn) carries into the next chunk only if it fits inside the overlap.
- `rank_bm25` (BM25Okapi), lowercase `\w+` tokens — the keyword search on the "Search returns the question" slide. https://github.com/dorianbrown/rank_bm25

## Sample data
- The support call (Acme Analytics, agent Priya) is made up for the demo. Its text is in `RAG22_verify.py`. 11 turns, 1,066 characters; 3 customer questions.

## Numbers on the slides and captions (all measured with the verify script)
- `chunk_size=200`, no overlap: 7 chunks; each of the 3 questions ends a chunk and its answer opens the next (0 of 3 questions share a chunk with the start of their answer).
- Query "What happens to the bill if I upgrade mid-month?": BM25 top hit is chunk 6 (the question and "OK.", no answer); the answer chunk 7 ranks 5th of 7. Over exchange chunks the top hit holds the question and "prorated by day".
- Sizes: 300 → 2 of 3 together, 4 chunks; 400 → 0 of 3, 4 chunks. Sweep 150–700 in steps of 10 (56 sizes): 55 split at least one pair; only 450 keeps all three.
- Overlap at size 200: 50 → 0 of 3, one chunk changed (chunk 5, inside the long reply); 100 → 1 of 3, 9 chunks. Every question and answer turn is over 60 characters (shortest 65).
- The long agent turn is 289 characters; at 200 it splits mid-sentence ("Pass the" / "cursor from each response…"), and chunk 5 has no speaker label, timestamp or question.
- Exchange chunker (`exchanges()`, `chunk()`, `pack()` exec'd from the slides), `max_chars=300`: 4 exchanges, 5 chunks, all ≤ 300 characters; the long turn becomes 2 chunks, both carrying the question.

## Concepts
- Speaker diarization (who spoke when) as a prerequisite when a transcript has no speaker labels: a general practice, stated as advice on the "move on" card, no product claim.
- Teaser: Contextual Retrieval (Anthropic, "Introducing Contextual Retrieval", Sept 2024): prepend a short chunk-specific context before embedding. https://www.anthropic.com/news/contextual-retrieval
