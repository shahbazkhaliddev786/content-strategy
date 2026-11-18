Status: posted 18 Nov 2026 (rubric review: 1st returned revise (8.3(b) overclaim in captions and slide 4 note, hook pattern repeating #17/#19/#20, "default splitter" in tweet 1); fixes applied; 2nd review passed, minor fix applied: slide 3 "after" line)

## LinkedIn

A 300-character split cut a contract clause off from its exceptions.
Chunking legal documents: split on clause numbers, put the section path on every chunk, repeat a long clause's lead-in.

A sample services agreement went through LangChain's RecursiveCharacterTextSplitter at chunk_size=300, no overlap. Chunk 3 ended at "8.3 The limits in Sections 8.1 and 8.2 do not apply to:". The three exceptions, including loss of Customer Data, landed in chunk 4 without 8.3 or its lead-in.

For "Does the liability cap apply to loss of Customer Data?", BM25 search ranked chunk 3 first: the cap of fees paid in the 12 months before the claim, without its exceptions.

With one clause per chunk, the path on top (MASTER SERVICES AGREEMENT > 8. Limitation of Liability > 8.3(b)) and the lead-in repeated on each sub-clause, the top hit became 8.3(b), which lifts the limits for Customer Data lost through Supplier's missed backups.

The slides show the real chunks, a 20-line clause chunker, and how to fetch the clauses a chunk cites ("the backups required by Section 5.2").

How do you handle cross-references when you chunk contracts?

Tomorrow: chunking transcripts

#AIEngineering #RAG #LegalTech

## Instagram

A 300-character split cut a contract clause off from its exceptions.
Chunking legal documents: split on clause numbers, put the section path on every chunk, repeat a long clause's lead-in.

A sample services agreement went through LangChain's RecursiveCharacterTextSplitter at chunk_size=300, no overlap. Chunk 3 ended at "8.3 The limits in Sections 8.1 and 8.2 do not apply to:". The three exceptions, including loss of Customer Data, landed in chunk 4 without 8.3 or its lead-in.

For "Does the liability cap apply to loss of Customer Data?", BM25 search ranked chunk 3 first: the cap of fees paid in the 12 months before the claim, without its exceptions.

With one clause per chunk, the path on top (MASTER SERVICES AGREEMENT > 8. Limitation of Liability > 8.3(b)) and the lead-in repeated on each sub-clause, the top hit became 8.3(b), which lifts the limits for Customer Data lost through Supplier's missed backups.

The slides show the real chunks, a 20-line clause chunker, and how to fetch the clauses a chunk cites ("the backups required by Section 5.2").

How do you handle cross-references when you chunk contracts?

Tomorrow: chunking transcripts

#AIEngineering #RAG #LegalTech #Chunking #LangChain

## Facebook

Chunking legal documents for RAG: split on clause numbers and keep each clause's lead-in with its sub-clauses.
In a test, a 300-character split put "do not apply to:" in one chunk and the exceptions in the next, so a search about lost Customer Data returned the liability cap first.

How do you handle cross-references when you chunk contracts?

#RAG #AIEngineering

## X thread

Tweet 1 (276 chars):
Chunking legal documents for RAG: one clause per chunk, with its section path and lead-in on top.

LangChain's RecursiveCharacterTextSplitter (300 chars, no overlap) ended a chunk at "8.3 The limits in Sections 8.1 and 8.2 do not apply to:" and put the exceptions in the next.

Tweet 2 (240 chars):
Query: "Does the liability cap apply to loss of Customer Data?"

BM25's top hit was the chunk with the cap: fees paid in the 12 months before the claim. The exception for lost Customer Data sat in the next chunk, without 8.3 or its lead-in.

Tweet 3 (233 chars):
Each clause chunk starts with its path: MASTER SERVICES AGREEMENT > 8. Limitation of Liability > 8.3(b).

Clause 8.3 ran over 300 characters, so it split at (a), (b), (c), with the lead-in repeated on each piece. New top hit: 8.3(b).

Tweet 4 (209 chars):
Store the clause numbers each chunk cites. 8.3(b) depends on "the backups required by Section 5.2", so fetch 5.2 with the hit.

How do you handle cross-references when you chunk contracts?

#RAG #AIEngineering

## Document title

Chunking legal documents | RAG series

## hooks_log row

| RAG #21 | Ask whether the liability cap covers lost Customer Data, and search hands back the cap, cut off at "do not apply to:". | A 300-character split cut a contract clause off from its exceptions. | A (story) |

## Caption shape

A (story)
