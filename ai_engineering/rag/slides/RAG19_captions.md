Status: posted 16 Nov 2026 (rubric review: 1st returned revise on two overclaims (decorator split wording, CodeSplitter decorator claim); fixes applied; 2nd review passed, its minor fixes 1 and 3 applied)

## LinkedIn

Chunking code by function, with file, class and constants on top, fixed a search three splitters missed at 250 characters.
"Where is the 500 refund limit checked?" kept returning the imports block.

The test: a 34-line billing/refunds.py, chunked at 250 characters, searched with BM25. The number 500 lives in LIMIT = Decimal("500") at the top of the file. The check, if amount > LIMIT:, landed in a chunk with no function, class or file name.

Two gotchas in LangChain's Python separators (langchain-text-splitters 1.1.3):
• The method separator is "\n\tdef ", with a tab. PEP 8 says "Use 4 spaces per indentation level", so methods fall back to cuts at blank lines.
• Splitting on "\ndef " leaves @retry(times=3) in the chunk above its function.

LlamaIndex's CodeSplitter parses with tree-sitter and keeps a decorator with its function when the whole definition fits in max_chars. A method over max_chars still loses its signature to a chunk of its own.

The slides show each splitter's real chunks, and a small chunker on Python's ast that keeps each function whole with its file, class and constants.

How do you chunk a codebase for RAG: by file, by function or by token count?

Tomorrow: chunking tables

#AIEngineering #RAG #CodeSearch

## Instagram

Chunking code by function, with file, class and constants on top, fixed a search three splitters missed at 250 characters.
"Where is the 500 refund limit checked?" kept returning the imports block.

The test: a 34-line billing/refunds.py, chunked at 250 characters, searched with BM25. The number 500 lives in LIMIT = Decimal("500") at the top of the file. The check, if amount > LIMIT:, landed in a chunk with no function, class or file name.

Two gotchas in LangChain's Python separators (langchain-text-splitters 1.1.3):
• The method separator is "\n\tdef ", with a tab. PEP 8 says "Use 4 spaces per indentation level", so methods fall back to cuts at blank lines.
• Splitting on "\ndef " leaves @retry(times=3) in the chunk above its function.

LlamaIndex's CodeSplitter parses with tree-sitter and keeps a decorator with its function when the whole definition fits in max_chars. A method over max_chars still loses its signature to a chunk of its own.

The slides show each splitter's real chunks, and a small chunker on Python's ast that keeps each function whole with its file, class and constants.

How do you chunk a codebase for RAG: by file, by function or by token count?

Tomorrow: chunking tables

#AIEngineering #RAG #CodeSearch #Python #LangChain

## Facebook

Chunking code by function keeps a method's signature, decorators and class together.
In a test, three common splitters at 250 characters sent the search "Where is the 500 refund limit checked?" to the imports block. Chunks with the file, class and constants on top found the check.

How do you chunk a codebase for RAG?

#RAG #AIEngineering

## X thread

Tweet 1 (272 chars):
Chunking code: split on functions, and put the file, class and constants on top of each chunk.

In a test, three splitters at 250 characters sent "Where is the 500 refund limit checked?" to the imports block. The 500 lived in a constant; the check sat in an unnamed chunk.

Tweet 2 (260 chars):
LangChain's Python separators (langchain-text-splitters 1.1.3):

• The method separator is "\n\tdef ", with a tab. PEP 8 uses 4 spaces, so methods fall back to cuts at blank lines.
• Splitting on "\ndef " leaves @retry(times=3) in the chunk above its function.

Tweet 3 (273 chars):
LlamaIndex's CodeSplitter uses tree-sitter and keeps a decorator with its function if the whole definition fits. A method over max_chars splits, leaving its signature as a chunk alone.

In 0.14.25 its chunk_lines setting isn't read; max_chars (default 1,500) sets the size.

Tweet 4 (251 chars):
A small chunker on Python's ast fixed it: one chunk per function, a header with file, class and the constants it reads, and long functions split between statements with the signature repeated.

How do you chunk a codebase for RAG?

#RAG #AIEngineering

## Document title

Chunking code for RAG | RAG series

## hooks_log row

| RAG #19 | Chunk code per function, with its file, class and constants on top. At 250 characters, three splitters sent a search for the refund limit to the imports block. | Chunking code by function, with file, class and constants on top, fixed a search three splitters missed at 250 characters. | A (story) |

## Caption shape

A (story)
