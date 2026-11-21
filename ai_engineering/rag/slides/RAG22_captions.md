Status: draft (not posted 21 Nov 2026: second rubric review returned revise; its 3 fixes applied, needs a fresh review)

## LinkedIn

BM25 ranked the answer to "What happens to the bill if I upgrade mid-month?" 5th of 7 chunks.
Chunking transcripts by exchange keeps each question, its replies and timestamps together.

LangChain's RecursiveCharacterTextSplitter at chunk_size=200, no overlap, ended a chunk at "And if I upgrade mid-month, what happens to the bill?" The answer, "prorated by day", opened the next chunk. BM25 search for that question ranked the question-only chunk first.

Tuning only moved the cut. Of 56 chunk sizes from 150 to 700, 55 split at least one question from its answer, and the one that didn't (450) fits this call's turn lengths only. chunk_overlap=50 changed one chunk, inside the long reply: the splitter carries a turn over only if it fits inside the overlap, and every question and answer here is over 60 characters.

Exchange chunks put the call title and time span on top, keep every speaker label, and repeat the question on each piece of a long reply. The upgrade question and its answer now come back as one hit.

The slides have the real chunks and the full exchange chunker.

What do you use as the chunk unit for call or meeting transcripts?

Tomorrow: contextual retrieval

#AIEngineering #RAG #Transcription

## Instagram

BM25 ranked the answer to "What happens to the bill if I upgrade mid-month?" 5th of 7 chunks.
Chunking transcripts by exchange keeps each question, its replies and timestamps together.

LangChain's RecursiveCharacterTextSplitter at chunk_size=200, no overlap, ended a chunk at "And if I upgrade mid-month, what happens to the bill?" The answer, "prorated by day", opened the next chunk. BM25 search for that question ranked the question-only chunk first.

Tuning only moved the cut. Of 56 chunk sizes from 150 to 700, 55 split at least one question from its answer, and the one that didn't (450) fits this call's turn lengths only. chunk_overlap=50 changed one chunk, inside the long reply: the splitter carries a turn over only if it fits inside the overlap, and every question and answer here is over 60 characters.

Exchange chunks put the call title and time span on top, keep every speaker label, and repeat the question on each piece of a long reply. The upgrade question and its answer now come back as one hit.

The slides have the real chunks and the full exchange chunker.

What do you use as the chunk unit for call or meeting transcripts?

Tomorrow: contextual retrieval

#AIEngineering #RAG #Transcription #Chunking #LangChain

## Facebook

Chunking transcripts for RAG: keep each question in the same chunk as its answer, with speaker labels and timestamps.
In a test, a 200-character split put all three answers on a support call in the chunk after the question.

What do you use as the chunk unit for call or meeting transcripts?

#RAG #AIEngineering

## X thread

Tweet 1 (252 chars):
Chunking transcripts for RAG: one exchange per chunk, a question with its replies, speaker labels and timestamps.

LangChain's RecursiveCharacterTextSplitter (200 chars, no overlap) split all three questions on a sample support call from their answers.

Tweet 2 (189 chars):
Query: "What happens to the bill if I upgrade mid-month?"

BM25's top hit was the chunk holding only that question. The answer, "prorated by day", sat in the next chunk and ranked 5th of 7.

Tweet 3 (230 chars):
On this call, tuning only moved the cut. Of 56 chunk sizes from 150 to 700, 55 split at least one question from its answer.

chunk_overlap=50 changed one chunk: the splitter carries over only the turns that fit inside the overlap.

Tweet 4 (221 chars):
Exchange chunks: call title and time span on top, every speaker label kept, and the question repeated on each piece of a long reply.

What do you use as the chunk unit for call or meeting transcripts?

#RAG #AIEngineering

## Document title

Chunking transcripts | RAG series

## hooks_log row

| RAG #22 | Customer: "And if I upgrade mid-month, what happens to the bill?" A 200-character split puts the agent's answer in the next chunk. | BM25 ranked the answer to "What happens to the bill if I upgrade mid-month?" 5th of 7 chunks. | B (claim) |

## Caption shape

B (claim)
