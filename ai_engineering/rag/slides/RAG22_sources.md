# RAG #22 sources: Chunking transcripts

Logged, not posted. Every example on the slides is re-run by `RAG22_verify.py` (prints ALL PASS).

## Libraries (run on 20 Nov 2026)
- `langchain-text-splitters` 1.1.3: `RecursiveCharacterTextSplitter`. Default separators `["\n\n", "\n", " ", ""]` read from `_separators` in the installed source; `chunk_size=300`, `chunk_overlap=0`. Docs: https://python.langchain.com/docs/how_to/recursive_text_splitter/
- `rank_bm25` (`BM25Okapi`), tokenised with `re.findall(r"[a-z0-9]+", text.lower())`, the same setup as RAG #20 and #21. https://github.com/dorianbrown/rank_bm25

## Sample data
- The support call (Northwind Cloud, agent Priya) is made up for the demo; it's in `RAG22_verify.py`. One turn per line, `[mm:ss] Speaker: text`.

## How each number was measured
- Recursive split at 300: 6 chunks (278, 256, 212, 298, 19, 47 characters). Chunk 3 ends at "[00:55] Customer: OK. And what happens to our files?"; chunk 4 starts with the 00:59 answer and ends mid-sentence at "and we"; chunk 5 is "can't restore them." (19 characters).
- The 00:59 turn is 318 characters, so the splitter fell back to the " " separator inside it.
- Exchange chunker (the slide code, exec'd): 7 chunks, 47 to 285 characters. Chunks 5 and 6 both start with the 00:55 question line.
- BM25, query "What happens to our files after we cancel?": recursive top hit chunk 3 (the question), chunk 4 second; exchange top hit chunk 6 ("After the 30 days ... deleted"), chunk 5 (export steps) second.
- BM25, query "Can you restore our files after we cancel?": recursive top hit chunk 5 ("can't restore them.").
- `meta(chunks[5])` returns `{'start': '00:55', 'speakers': ['Agent', 'Customer']}`.

## Terms
- Speaker diarization: labelling which speaker talks when in an audio recording (named in the "Move on when" card as the step before turn-based chunking when a transcript has no speaker labels).
- Semantic chunking: RAG #16. Clause chunks and the repeated lead-in: RAG #21.
