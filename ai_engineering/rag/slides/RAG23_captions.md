Status: draft (not posted 23 Nov 2026: second rubric review returned revise; its 3 fixes applied, needs a fresh review)

## LinkedIn

BM25 ranked the answer to "ACME Corp's Q2 2023 revenue growth" in a 16-way tie for 5th.
Contextual retrieval adds context to each chunk before indexing, so the chunk says which company and quarter.

The test: 16 made-up quarterly reports, 96 chunks, BM25 search for "What was the revenue growth for ACME Corp in Q2 2023?" ACME's four Overview chunks came first. The answer chunk says "the company's revenue grew by 3%" and never names ACME or Q2, so it tied with all 16 Results chunks.

The document title and section heading on every chunk, with no LLM call, moved the answer to 1st.

Anthropic's Contextual Retrieval goes further: a small LLM reads the whole document and writes 50 to 100 tokens of context for each chunk. In Anthropic's tests, relevant chunks missing from the top 20 fell from 5.7% to 3.7% with contextual embeddings, 2.9% with contextual BM25 added, and 1.9% with reranking. You pay one LLM call per chunk at ingest and no extra LLM call per query.

Test the lines it writes: a correct template line for ACME's Q3 report named "Q2 2023" and tied with the answer.

The slides have the prompt, the caching code and the runs.

What do you put in front of your chunks before you embed them?

Tomorrow: tuning chunk size

#AIEngineering #RAG #ContextualRetrieval

## Instagram

BM25 ranked the answer to "ACME Corp's Q2 2023 revenue growth" in a 16-way tie for 5th.
Contextual retrieval adds context to each chunk before indexing, so the chunk says which company and quarter.

The test: 16 made-up quarterly reports, 96 chunks, BM25 search for "What was the revenue growth for ACME Corp in Q2 2023?" ACME's four Overview chunks came first. The answer chunk says "the company's revenue grew by 3%" and never names ACME or Q2, so it tied with all 16 Results chunks.

The document title and section heading on every chunk, with no LLM call, moved the answer to 1st.

Anthropic's Contextual Retrieval goes further: a small LLM reads the whole document and writes 50 to 100 tokens of context for each chunk. In Anthropic's tests, relevant chunks missing from the top 20 fell from 5.7% to 3.7% with contextual embeddings, 2.9% with contextual BM25 added, and 1.9% with reranking. You pay one LLM call per chunk at ingest and no extra LLM call per query.

Test the lines it writes: a correct template line for ACME's Q3 report named "Q2 2023" and tied with the answer.

The slides have the BM25 runs and Anthropic's numbers.

What do you put in front of your chunks before you embed them?

Tomorrow: tuning chunk size

#AIEngineering #RAG #ContextualRetrieval #Chunking #VectorSearch

## Facebook

Contextual retrieval: put a short line of context on each chunk before you embed it, so a chunk that says "the company's revenue grew by 3%" also says which company.
In a BM25 test, adding just the document title and section heading moved the answer from a tie for 5th to 1st.

What do you put in front of your chunks before you embed them?

#RAG #AIEngineering

## X thread

Tweet 1 (200 chars):
Contextual retrieval: put a short line of context on each chunk before you embed and index it.

A chunk that says "the company's revenue grew by 3%" never tells search which company, or which quarter.

Tweet 2 (268 chars):
Test: 16 made-up quarterly reports, 96 chunks, BM25.

Query: "What was the revenue growth for ACME Corp in Q2 2023?"

Top 4 hits: ACME's Overview chunks. The answer tied for 5th with all 16 Results chunks.

Title + section heading on every chunk: the answer ranks 1st.

Tweet 3 (266 chars):
Anthropic's version has a small LLM write 50-100 tokens of context per chunk.

Share of relevant chunks missing from the top 20:
plain 5.7%
contextual embeddings 3.7%
+ contextual BM25 2.9%
+ reranking 1.9%

One LLM call per chunk at ingest; no extra call per query.

Tweet 4 (212 chars):
Test your context lines: a correct template line for ACME's Q3 report said "growth over Q2 2023" and tied with the real answer.

What do you put in front of your chunks before you embed them?

#RAG #AIEngineering

## Document title

Contextual retrieval | RAG series

## hooks_log row

| RAG #23 | ACME's Q2 2023 revenue growth sits in a chunk that never names ACME or Q2. Put a short line of context on each chunk before you index it. | BM25 ranked the answer to "ACME Corp's Q2 2023 revenue growth" in a 16-way tie for 5th. | A (story) |

## Caption shape

A (story)
