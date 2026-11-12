Status: draft (format v3, daily run 12 Nov 2026; second review returned revise, reviewer fixes applied, not reviewed again, not posted)

## LinkedIn (1274 chars)

The top 4 chunks for a warranty question all missed the sentence that answers it.
The parent-document retriever returns the section around them, and its defaults decide how big it is.

The run: a support handbook split into 23 small children. Query: "How long do warranty repairs take?" The answer, "Repairs take about 10 business days.", ranked outside the top 4. The top 2 hits came from the Warranty section, which holds it.

LangChain's own docs name the tension: small chunks keep embeddings accurate ("If too long, then the embeddings can lose meaning"), while bigger parents keep the context.

Four traps in ParentDocumentRetriever:
• parent_splitter defaults to None, so the parent is the whole input document. Here: all 1,360 characters on every query.
• k counts children (4 by default), and parents get deduped, so the context size changes per query.
• Re-adding a document gives it new random ids, so the same section comes back twice.
• With the docs' in-memory docstore, a restart returns an empty list, with no error.

The slides have the real run, a fix for each one and a config that combines them.

How do you size parents in your pipeline: by section, by token count, or something else?

Tomorrow: sentence-window retrieval

#AIEngineering #RAG #LangChain

## Instagram

The top 4 chunks for a warranty question all missed the sentence that answers it.
The parent-document retriever returns the section around them, and its defaults decide how big it is.

The run: a support handbook split into 23 small children. Query: "How long do warranty repairs take?" The answer, "Repairs take about 10 business days.", ranked outside the top 4. The top 2 hits came from the Warranty section, which holds it.

LangChain's own docs name the tension: small chunks keep embeddings accurate ("If too long, then the embeddings can lose meaning"), while bigger parents keep the context.

Four traps in ParentDocumentRetriever:
• parent_splitter defaults to None, so the parent is the whole input document. Here: all 1,360 characters on every query.
• k counts children (4 by default), and parents get deduped, so the context size changes per query.
• Re-adding a document gives it new random ids, so the same section comes back twice.
• With the docs' in-memory docstore, a restart returns an empty list, with no error.

The slides have the real run and a fix for each one.

How do you size parents in your pipeline: by section, by token count, or something else?

Tomorrow: sentence-window retrieval

#AIEngineering #RAG #LangChain #Chunking #VectorSearch

## Facebook

The top 4 chunks for a warranty question all missed the sentence that answers it.
The parent-document retriever returns the section around them. With no parent splitter, that section is the whole document.

How do you size parents in your pipeline?

#RAG #AIEngineering

## X thread

Tweet 1 (230 chars):
The top 4 chunks for a warranty question all missed the sentence that answers it.

The parent-document retriever returns the section around them. Its defaults decide how big it is: with no parent splitter, it's the whole document.

Tweet 2 (224 chars):
A real run: 23 small children from a support handbook. Query: "How long do warranty repairs take?"

The top 2 children came from the Warranty section, and that section holds the answer: "Repairs take about 10 business days."

Tweet 3 (270 chars):
Four traps in ParentDocumentRetriever:

• parent_splitter=None returns the whole input document
• k=4 counts children; parents get deduped
• Re-adding a doc gives new random ids, so sections come back twice
• The docs' InMemoryStore + a restart = an empty list, no error

Tweet 4 (210 chars):
To fix them, split parents on headings, set k for your context budget, delete old children and parents before re-ingest, and persist the docstore.

How do you size parents in your pipeline?

#RAG #AIEngineering

## Document title

Parent-document retriever | RAG series

## hooks_log row

| RAG #17 | The top 4 chunks all missed the answer. Return the section around the top hit, and size that section yourself. | The top 4 chunks for a warranty question all missed the sentence that answers it. | A (story) |

## Caption shape

A (story)
