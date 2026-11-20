Status: draft (failed 2 rubric reviews on 20 Nov 2026; 2nd-review fixes applied, not re-reviewed; needs Shahbaz's approval)

## LinkedIn

Transcripts answer in exchanges, one question and its reply, and a size-based split ignores where they start and end.
Chunking transcripts by exchange keeps them together, with speaker and timestamp on every line.

A sample support call went through LangChain's RecursiveCharacterTextSplitter at chunk_size=300, no overlap. It broke at line ends where it could, but it packed turns up to 300 characters: "And what happens to our files?" was the last line of chunk 3, and the agent's answer started chunk 4.

For "What happens to our files after we cancel?", BM25 search ranked the chunk ending at the question first. The answer's last sentence became a 19-character chunk, "can't restore them.", with no speaker and no subject.

Exchange chunks start at each customer turn and keep the agent's replies with it. When an exchange runs past 300 characters, the answer splits at sentences and every piece carries the question line. Both pieces of the files answer then ranked first and second.

The slides show the real chunks, the question repeated on each piece, and how to turn speaker labels and timestamps into metadata.

What rule do you use to group turns in meeting transcripts, where nobody is the single asker?

Tomorrow: contextual retrieval

#AIEngineering #RAG #Transcripts

## Instagram

Transcripts answer in exchanges, one question and its reply, and a size-based split ignores where they start and end.
Chunking transcripts by exchange keeps them together, with speaker and timestamp on every line.

A sample support call went through LangChain's RecursiveCharacterTextSplitter at chunk_size=300, no overlap. It broke at line ends where it could, but it packed turns up to 300 characters: "And what happens to our files?" was the last line of chunk 3, and the agent's answer started chunk 4.

For "What happens to our files after we cancel?", BM25 search ranked the chunk ending at the question first. The answer's last sentence became a 19-character chunk, "can't restore them.", with no speaker and no subject.

Exchange chunks start at each customer turn and keep the agent's replies with it. When an exchange runs past 300 characters, the answer splits at sentences and every piece carries the question line. Both pieces of the files answer then ranked first and second.

The slides show the real chunks, the question repeated on each piece, and how to turn speaker labels and timestamps into metadata.

What rule do you use to group turns in meeting transcripts, where nobody is the single asker?

Tomorrow: contextual retrieval

#AIEngineering #RAG #Transcripts #Chunking #LangChain

## Facebook

Chunking transcripts for RAG: keep each question in the same chunk as its answer.
In a test, a 300-character split ended one chunk at "And what happens to our files?" and put the answer in the next one, so search returned the chunk without the answer first.

What rule do you use to group turns in meeting transcripts?

#RAG #AIEngineering

## X thread

Tweet 1 (266 chars):
Chunking transcripts for RAG: one exchange per chunk, the question with its replies.

LangChain's RecursiveCharacterTextSplitter (300 chars, no overlap) ended a chunk of a support call at "And what happens to our files?". The agent's answer went into the next chunk.

Tweet 2 (226 chars):
Query: "What happens to our files after we cancel?"

BM25's top hit was the chunk ending at the question. The answer's last sentence became a 19-character chunk, "can't restore them.", with no speaker and nothing it refers to.

Tweet 3 (248 chars):
Exchange chunks start at each customer turn and keep the replies with it. Speaker label and timestamp stay on every line.

An answer over 300 characters splits at sentences, with the question line on each piece. Both pieces then ranked 1st and 2nd.

Tweet 4 (204 chars):
Store the start time and speakers as metadata, so a hit links to 00:55 in the recording.

What rule do you use to group turns in meeting transcripts, where nobody is the single asker?

#RAG #AIEngineering

## Document title

Chunking transcripts | RAG series

## hooks_log row

| RAG #22 | Your support-call RAG returns the customer's question and ranks the agent's answer second. Chunk by exchange: each question with its reply, speaker and timestamp on every line. | Transcripts answer in exchanges, one question and its reply, and a size-based split ignores where they start and end. | B (claim) |

## Caption shape

B (claim)
