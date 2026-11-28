Status: draft (not posted 28 Nov: both rubric reviews returned revise; second review's fixes applied, needs a fresh review)

## LinkedIn

"How do I get my money back?" scored 0 against the refund doc in BM25. An embedding ranked that doc 1st of 5.
Embeddings place text as points in space, so search can match meaning when words differ.

In a small test with 5 made-up help-centre docs, "How do I get my money back?" shares no word with "Refunds are issued to the original card within 5 business days." BM25, a keyword ranker, scored all 5 docs 0.0.

Embedded with spaCy's en_core_web_md word vectors (300 numbers per text), the same question ranked the refund doc 1st of 5 by cosine similarity (0.636). Three more questions sharing no content word with their answer each found it.

OpenAI's embeddings guide: "An embedding is a vector (list) of floating point numbers." all-MiniLM-L6-v2 gives 384; text-embedding-3-small, 1,536 by default.

Test two things before you trust the nearest hit. Averaged word vectors with stop words dropped scored "can be refunded" against "cannot be refunded" at 1.000. And distances only mean something inside one model's space: mixing two spaCy models moved a question's top answer from Seats to Invoices.

Where has keyword search missed a question in your system that an embedding would have caught?

Tomorrow: cosine vs dot product vs L2

#AIEngineering #RAG #Embeddings

## Instagram

"How do I get my money back?" scored 0 against the refund doc in BM25. An embedding ranked that doc 1st of 5.
Embeddings place text as points in space, so search can match meaning when words differ.

In a small test with 5 made-up help-centre docs, "How do I get my money back?" shares no word with "Refunds are issued to the original card within 5 business days." BM25, a keyword ranker, scored all 5 docs 0.0.

Embedded with spaCy's en_core_web_md word vectors (300 numbers per text), the same question ranked the refund doc 1st of 5 by cosine similarity (0.636). Three more questions sharing no content word with their answer each found it.

OpenAI's embeddings guide: "An embedding is a vector (list) of floating point numbers." all-MiniLM-L6-v2 gives 384; text-embedding-3-small, 1,536 by default.

Test two things before you trust the nearest hit. Averaged word vectors with stop words dropped scored "can be refunded" against "cannot be refunded" at 1.000. And distances only mean something inside one model's space: mixing two spaCy models moved a question's top answer from Seats to Invoices.

Where has keyword search missed a question in your system that an embedding would have caught?

Tomorrow: cosine vs dot product vs L2

#AIEngineering #RAG #Embeddings #SemanticSearch #VectorSearch

## Facebook

"How do I get my money back?" scored 0 against the refund doc in BM25. An embedding ranked that doc 1st of 5.
Embeddings place text as points in space, so search can match meaning when words differ.

Where has keyword search missed a question in your system that an embedding would have caught?

#RAG #AIEngineering

## X thread

Tweet 1 (214 chars):
"How do I get my money back?" shares no word with the refund doc. BM25 scored it 0. An embedding ranked the refund doc 1st of 5.

An embedding is a fixed-length list of numbers that places text as a point in space.

Tweet 2 (249 chars):
5 made-up help-centre docs, spaCy en_core_web_md word vectors (300 numbers per text), cosine similarity.

Four questions with no content word in common with their answers:
money back → Refunds
spreadsheet → Export
billed → Invoices
colleague → Seats

Tweet 3 (247 chars):
Sparse vs dense: the refund question's keyword vector over the docs' 34-word vocabulary is all zeros. Its dense vector has 300 of 300 slots non-zero.

Sizes vary by model: all-MiniLM-L6-v2 gives 384, OpenAI text-embedding-3-small 1,536 by default.

Tweet 4 (280 chars):
Two things to test before you trust the nearest hit:
- with stop words dropped, "can be refunded" vs "cannot be refunded" scored 1.000
- near only counts inside one model: mixing two spaCy models moved an answer

What has keyword search missed in your system?

#RAG #AIEngineering

## Document title

What an embedding is | RAG series

## hooks_log row

| RAG #25 | "How do I get my money back?" shares no word with the refund doc. BM25 scored it 0; an embedding, which turns text into a point, ranked it 1st of 5. | "How do I get my money back?" scored 0 against the refund doc in BM25. An embedding ranked that doc 1st of 5. | A (story) |

## Caption shape

A (story)
