Status: draft (26 Nov 2026: not posted; fresh reviews 1 and 2 both returned revise (budget-cap wording); both reviews' fixes applied, needs a fresh review)

## LinkedIn

Chunk size tuning goes wrong when you compare sizes at top-3: in a small test, bigger chunks won because each one carried more text.
Cap every size at one context budget before you compare.

In a small test (6 made-up help-centre sections, 20 questions, spaCy word-vector embeddings), top-3 retrieval found 19 of 20 answers with 500-character chunks and 7 with 60-character chunks. At 500 characters the index held 7 chunks, so the top 3 was 3 of 7.

Give every size a 400-character context budget (whole chunks while they fit, at least one) and the order changes: 100 and 150 characters found 13, and 500 found 9, the fewest of six sizes. BM25 on the same chunks did best at 200 to 300 characters (18 of 20).

Both ends fail in ways you can see. At 60 characters, "How long are audit logs kept on Enterprise?" returned "years on Enterprise." first. At 500, a monthly-refund question ranked the billing section above the Refunds section.

Count size in the embedding model's tokens: the all-MiniLM-L6-v2 model card says input longer than 256 word pieces is truncated by default.

The slides have the runs, the overlap numbers and a 5-step tuning loop.

What context budget do you tune your chunk size against?

Tomorrow: what an embedding is

#AIEngineering #RAG #Chunking

## Instagram

Chunk size tuning goes wrong when you compare sizes at top-3: in a small test, bigger chunks won because each one carried more text.
Cap every size at one context budget before you compare.

In a small test (6 made-up help-centre sections, 20 questions, spaCy word-vector embeddings), top-3 retrieval found 19 of 20 answers with 500-character chunks and 7 with 60-character chunks. At 500 characters the index held 7 chunks, so the top 3 was 3 of 7.

Give every size a 400-character context budget (whole chunks while they fit, at least one) and the order changes: 100 and 150 characters found 13, and 500 found 9, the fewest of six sizes. BM25 on the same chunks did best at 200 to 300 characters (18 of 20).

Both ends fail in ways you can see. At 60 characters, "How long are audit logs kept on Enterprise?" returned "years on Enterprise." first. At 500, a monthly-refund question ranked the billing section above the Refunds section.

Count size in the embedding model's tokens: the all-MiniLM-L6-v2 model card says input longer than 256 word pieces is truncated by default.

The slides have the runs, a when-to-sweep table and a cheat sheet.

What context budget do you tune your chunk size against?

Tomorrow: what an embedding is

#AIEngineering #RAG #Chunking #Embeddings #VectorSearch

## Facebook

Chunk size tuning: cap every size at one context budget before you compare them.
At top-3, 500-character chunks found 19 of 20 answers in a small test; at a 400-character context budget, they found 9, the fewest of six sizes.

What context budget do you tune your chunk size against?

#RAG #AIEngineering

## X thread

Tweet 1 (218 chars):
Chunk size tuning: compare sizes at the same context budget.

In a small test, top-3 retrieval with 500-character chunks found 19 of 20 answers. At a 400-character context budget, they found 9, the fewest of six sizes.

Tweet 2 (216 chars):
Why top-3 flatters big chunks: at 500 characters the test index held 7 chunks, so the top 3 was 3 of 7.

Found at a 400-character cap (spaCy vectors, 20 questions):
60 chars: 10
100: 13
150: 13
200: 12
300: 12
500: 9

Tweet 3 (233 chars):
Both ends fail in ways you can see.

60 characters: "How long are audit logs kept on Enterprise?" returned "years on Enterprise." first.

500 characters: a monthly-refund question ranked the billing section above the Refunds section.

Tweet 4 (223 chars):
BM25 on the same chunks did best at 200-300 characters (18 of 20). Each retriever has its own best size, so re-run the sweep when you change it.

What context budget do you tune your chunk size against?

#RAG #AIEngineering

## Document title

Tuning chunk size | RAG series

## hooks_log row

| RAG #24 | Top-3 retrieval made 500-character chunks look best: 19 of 20 answers found. At a 400-character context budget, they found 9, the fewest of six sizes. | Chunk size tuning goes wrong when you compare sizes at top-3: in a small test, bigger chunks won because each one carried more text. | B (claim) |

## Caption shape

B (claim)
