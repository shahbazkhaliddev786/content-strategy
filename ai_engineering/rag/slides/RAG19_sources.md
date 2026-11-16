# RAG #19 sources: Chunking code (Chunking by doc type · Part 1/4)

Logged, not posted. Every example on the slides is re-run by `RAG19_verify.py` (prints ALL PASS).

## Libraries (installed and read with `inspect`, 16 Nov 2026)
- langchain-text-splitters 1.1.3 (langchain-core 1.8.1)
  - `RecursiveCharacterTextSplitter.get_separators_for_language(Language.PYTHON)` returns `["\nclass ", "\ndef ", "\n\tdef ", "\n\n", "\n", " ", ""]`.
  - `from_language()` passes `is_separator_regex=True`; `RecursiveCharacterTextSplitter.__init__` defaults `keep_separator=True` (separator kept at the start of the next piece). `TextSplitter` defaults: `chunk_size=4000`, `chunk_overlap=200`, `strip_whitespace=True`.
  - Source: https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters
- llama-index-core 0.14.25 with tree-sitter 0.26.1 and tree-sitter-language-pack 1.25.2
  - `llama_index/core/node_parser/text/code.py`: `DEFAULT_CHUNK_LINES = 40`, `DEFAULT_LINES_OVERLAP = 15`, `DEFAULT_MAX_CHARS = 1500`, `DEFAULT_MAX_TOKENS = 512`; `count_mode` "char" (default) or "token".
  - `split_text` and `_chunk_node` read only `max_chars` / `max_tokens`; `chunk_lines` and `chunk_lines_overlap` are stored as fields but not read by the split code. Checked by output too: changing them leaves the chunks identical.
  - `_chunk_node` packs whole child nodes up to the limit and recurses into a child bigger than the limit.
  - The class docstring: "Thank you to Kevin Lu / SweepAI for suggesting this elegant code splitting solution. https://docs.sweep.dev/blogs/chunking-2m-files"
- rank_bm25 0.2.2 (`BM25Okapi`, default k1/b), tokens = lowercase `[a-z0-9]+`.
- Python `ast` (3.x): `FunctionDef.lineno` is the `def` line; decorators are in `decorator_list`; `end_lineno` available from 3.8.

## Other sources
- PEP 8, Indentation: "Use 4 spaces per indentation level." https://peps.python.org/pep-0008/#indentation

## Test setup (all numbers on the slides)
- Sample: a 34-line, 778-character `billing/refunds.py` (in `RAG19_verify.py`): imports, `LIMIT = Decimal("500")`, class `RefundService` with `__init__`, `refund`, `left`, and a decorated `sync_refunds`. 4-space indentation.
- Chunk size 250 characters, overlap 0, for all four approaches: LangChain default separators (4 chunks), LangChain Python separators (6 chunks), LlamaIndex `CodeSplitter(language="python", max_chars=250)` (8 chunks), the `ast` chunker in the verify script (6 chunks; `refund` in 3 parts).
- `ast` chunker at 1,500 characters: 4 chunks. Default `CodeSplitter` (1,500): 1 chunk.
- Query "Where is the 500 refund limit checked?" with BM25 over each set: the imports block ranks first for the three library splitters; `refund` part 2/3 ranks first for the `ast` chunker with header.
