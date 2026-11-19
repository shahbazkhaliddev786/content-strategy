# RAG #22 sources: Chunking transcripts (Chunking by doc type · Part 4/4)

Logged, not posted. Every example on the slides is re-run by `RAG22_verify.py` (prints ALL PASS).

## Libraries (installed and run, 19 Nov 2026)
- langchain-text-splitters 1.1.3
  - `RecursiveCharacterTextSplitter` default separators `["\n\n", "\n", " ", ""]` (checked in the verify script). It splits on the first separator found, recurses into pieces over `chunk_size`, and merges small pieces up to `chunk_size`. With one turn per line, that merging packs whole turns up to 300 characters, so cuts fall between turns but not between exchanges.
  - `is_separator_regex=True` uses the separators as regex patterns; the lookahead `\n(?=\[\d\d:\d\d\])` splits before each timestamp.
  - `keep_separator="end"` keeps ". " at the end of the previous piece (used by `split()` in the exchange chunker).
  - Source: https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters
- rank_bm25 (`BM25Okapi`, default k1/b), tokens = lowercase `[a-z0-9]+`.

## Test setup (all numbers on the slides)
- Sample support call (made up for the demo): title line "Support call: nightly export failures, 12 Nov", then 10 turns `[mm:ss] Agent|Customer: text`. Full text in `RAG22_verify.py`.
- Recursive splitter, `chunk_size=300`, `chunk_overlap=0`, default separators: 5 chunks; every chunk is whole lines (cuts between turns); chunks 3 and 4 end on a customer question, so 2 of the 4 cuts separate a question from its answer. Chunk 3 ends "Can we raise that limit without changing plans?"; chunk 4 starts "[00:30] Agent: Not on Starter."
- Timestamp-regex separators, `chunk_size=300`: 4 chunks; chunks 2 and 3 end on a question; the answers open chunks 3 and 4.
- Exchange chunker (code on slide 8, exec'd by the verify script; `split()` = RecursiveCharacterTextSplitter with `separators=[". ", " "]`, `keep_separator="end"`, `chunk_overlap=0`): 4 chunks at `size=300`, 201–296 characters; chunk 3 (00:26–00:30) is 296 characters. At `size=250`: 8 chunks; the 00:26 exchange splits into 3 pieces at sentence ends, each with the question and the "[00:30] Agent:" label.
- BM25, query "Can we raise the export limit without changing plans?": recursive chunks rank chunk 3 first (5 GB limit + the question, no answer), chunk 4 (the answer) second; exchange chunks rank the 00:26–00:30 chunk first (question, "Not on Starter." and both workarounds).
- Hidden question: with turn 00:09 changed to "Which plan is the account on? I can check.", `t.endswith("?")` starts no chunk at 00:09 and the 00:00–00:15 exchange runs over 300, so "Starter, I think." is filed under "How can I help?". With `"?" in t`: 4 exchange chunks again.

## Other claims
- WebVTT caption files are made of timed cues (W3C WebVTT spec, https://www.w3.org/TR/webvtt1/); a speaker's turn can span several cues, hence "merge lines from the same speaker first".
- Speaker diarization (who spoke when) is the standard step that adds speaker labels to an unlabeled transcript; named as the move-on step, no product claims.

## Series consistency
- Same splitter version, BM25 setup and 300-character limit as RAG #20 (tables) and #21 (legal); the repeated question plays the role of #21's repeated lead-in.
- Semantic/topic splitting for monologues refers back to RAG #16 without new claims.
