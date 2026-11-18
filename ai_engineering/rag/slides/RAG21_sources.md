# RAG #21 sources: Chunking legal documents (Chunking by doc type · Part 3/4)

Logged, not posted. Every example on the slides is re-run by `RAG21_verify.py` (prints ALL PASS).

## Libraries (installed and read with `inspect`, 18 Nov 2026)
- langchain-text-splitters 1.1.3
  - `RecursiveCharacterTextSplitter.__init__(separators=None, keep_separator=True, is_separator_regex=False, **kwargs)`; default separators `["\n\n", "\n", " ", ""]`.
  - `_split_text` picks the first separator found in the text, splits on it, recurses into pieces over `chunk_size`, and merges small pieces up to `chunk_size` (`_merge_splits`). This merging is why the regex-separator run packs Section 5 and Section 7 into one chunk at 400.
  - With `is_separator_regex=True` the separators are used as regex patterns (otherwise `re.escape`d). Lookahead patterns such as `\n(?=\d+\.\d+ )` split before a clause number and keep the number with its clause.
  - Source: https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters
- rank_bm25 (`BM25Okapi`, default k1/b), tokens = lowercase `[a-z0-9]+`.

## Test setup (all numbers on the slides)
- Sample contract (made up for the demo): "MASTER SERVICES AGREEMENT" excerpt with sections 5 (Data Protection), 7 (Fees and Payment), 8 (Limitation of Liability) and 9 (Term and Termination); 8.3 has a lead-in and sub-clauses (a)–(c). Full text in `RAG21_verify.py`.
- Recursive splitter, `chunk_size=300`, `chunk_overlap=0`, default separators: 5 chunks. Chunk 3 = heading 8 + 8.1 + 8.2 + the 8.3 lead-in, ending "do not apply to:"; chunk 4 = (a), (b), (c) only (no "8.3", no "apply", no "liability").
- Regex clause separators, `chunk_size=400`: 4 chunks. Chunk 1 holds the title, Section 5 and Section 7; 8.3 stays whole in chunk 3, without the "Limitation of Liability" heading.
- Clause chunker (code on slide 8, exec'd by the verify script): 11 chunks at `max_chars=300`, 114–222 characters. Whole 8.3 with its path = 305 characters, so it splits into 8.3(a), 8.3(b), 8.3(c), each with the 55-character lead-in.
- BM25, query "Does the liability cap apply to loss of Customer Data?": recursive chunks rank chunk 3 first (cap in 8.2), chunk 4 second; clause chunks rank 8.3(b) first.
- `refs()` (slide 9) on chunk 8 (8.3(b)) returns `['8.1', '8.2', '5.2']`; it misses "Section 10" in 8.3(a) (no dot).
- The chunker reads one line per clause; lines that start with no clause number are dropped (checked in the verify script).

## Series consistency
- Same splitter version and 300-character limit as RAG #20 (tables); the lead-in plays the role the header row played there.
- Multi-hop retrieval is Module 10 (RAG #98), referred to as "a later post".
