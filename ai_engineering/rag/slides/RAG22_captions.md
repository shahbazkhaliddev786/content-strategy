Status: draft (rubric review: 1st revise, fixes applied)

## LinkedIn

Chunking transcripts: open a new chunk at each question, and an answer in the next turn stays with it.
A 300-character split of a support call left 2 questions cut off from their answers.

LangChain's RecursiveCharacterTextSplitter (chunk_size=300, no overlap) cut the call only between speaker turns. It still ended chunk 3 on "Can we raise that limit without changing plans?" and opened chunk 4 with "Not on Starter."

For "Can we raise the export limit without changing plans?", BM25 search ranked chunk 3 first: the 5 GB limit and the question, with no answer.

With exchange chunks (open at each question, run to the next one, call title and time range on top), the top hit became the question, the answer and both workarounds in one 296-character chunk.

A long answer still gets split. Repeat the question and the speaker label on every piece.

The slides show the real chunks, a 21-line exchange chunker, and the case where a question hides mid-turn ("Which plan is the account on? I can check.").

How do you chunk meetings where one question gets answered across several turns?

Tomorrow: contextual retrieval

#AIEngineering #RAG #Transcripts

## Instagram

Chunking transcripts: open a new chunk at each question, and an answer in the next turn stays with it.
A 300-character split of a support call left 2 questions cut off from their answers.

LangChain's RecursiveCharacterTextSplitter (chunk_size=300, no overlap) cut the call only between speaker turns. It still ended chunk 3 on "Can we raise that limit without changing plans?" and opened chunk 4 with "Not on Starter."

For "Can we raise the export limit without changing plans?", BM25 search ranked chunk 3 first: the 5 GB limit and the question, with no answer.

With exchange chunks (open at each question, run to the next one, call title and time range on top), the top hit became the question, the answer and both workarounds in one 296-character chunk.

A long answer still gets split. Repeat the question and the speaker label on every piece.

The slides show the real chunks, a 21-line exchange chunker, and the case where a question hides mid-turn ("Which plan is the account on? I can check.").

How do you chunk meetings where one question gets answered across several turns?

Tomorrow: contextual retrieval

#AIEngineering #RAG #Transcripts #Chunking #LangChain

## Facebook

Chunking transcripts for RAG: open a new chunk at each question, so a reply in the next turn stays in the same chunk.
In a test, a 300-character split ended one chunk on a customer's question and put the agent's answer in the next, so search returned the question without its answer.

How do you chunk meetings where one question gets answered across several turns?

#RAG #AIEngineering

## X thread

Tweet 1 (278 chars):
Chunking transcripts: open a new chunk at each question, and a reply in the next turn stays with it.

LangChain's RecursiveCharacterTextSplitter (300 chars, no overlap) ended a chunk on "Can we raise that limit without changing plans?" and opened the next with "Not on Starter."

Tweet 2 (189 chars):
Query: "Can we raise the export limit without changing plans?"

BM25's top hit was the chunk ending on the question: the 5 GB limit, no answer. The answer sat in the next chunk, ranked 2nd.

Tweet 3 (253 chars):
Exchange chunks: open at each question, run to the next one, with the call title and time range on top.

New top hit: the question, "Not on Starter." and both workarounds in one 296-char chunk. A long answer gets split, with the question on every piece.

Tweet 4 (262 chars):
Watch for questions mid-turn. "Which plan is the account on? I can check." doesn't end in "?", so the chunker filed "Starter, I think." under "How can I help?"

How do you chunk meetings where one question gets answered across several turns?

#RAG #AIEngineering

## Document title

Chunking transcripts | RAG series

## hooks_log row

| RAG #22 | When a split lands between a question and its reply, search finds the question and loses the answer. Open each chunk at a question. | Chunking transcripts: open a new chunk at each question, and an answer in the next turn stays with it. | B (claim) |

## Caption shape

B (claim)
