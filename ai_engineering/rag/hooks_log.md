# Hooks log

One row per published post, appended by the daily run after posting (format v2 onward). The run reads the last 10 rows so a new hook doesn't repeat an old opening word or pattern, and so the caption shape rotates.

Rows for RAG #01–#11 were backfilled from the published posts on Oct 31 2026 (caption shape was the v1 template for all of them).

| RAG # | Cover hook | Caption opener (first line) | Caption shape |
|---|---|---|---|
| RAG #01 | Your LLM Is Making It Up. | Your LLM is making it up, and it isn't a bug. It's answering from memory that froze the day training ended. | v1 template |
| RAG #02 | RAG Is Two Systems, Not One. | Most people picture RAG as one flow: question in, answer out. It's actually two pipelines, and most bugs hide in the one nobody watches. | v1 template |
| RAG #03 | Your RAG Might Be Overkill. | Your RAG pipeline might be overkill. If the whole corpus fits in the context window, you can skip retrieval and paste it all in. | v1 template |
| RAG #04 | Teach Skills. Fetch Facts. | Fine-tuning won't teach your model facts. It teaches habits. | v1 template |
| RAG #05 | Ask What's Missing First. | RAG, long-context, fine-tuning or a knowledge graph? Wrong question. Ask what your model is missing first. | v1 template |
| RAG #06 | The Bot Never Saw The Doc. | Your RAG bot didn't hallucinate. It never saw the document. | v1 template |
| RAG #07 | Your Scans Are Missing. | Your RAG pipeline can't read a scanned PDF. It doesn't fail loudly. The document just never makes it into the index. | v1 template |
| RAG #08 | Your Tables Lost Meaning. | Your RAG found the right table. It still gave the wrong number. | v1 template |
| RAG #09 | Your Parser Indexed Cookies. | Your RAG app indexed the cookie banner. The text was already there, so nobody thought to parse it. | v1 template |
| RAG #10 | Your Parser Ignores Layout. | Your PDF parser can read every character and still hand your RAG system garbage. | v1 template |
| RAG #11 | Your RAG Is Blind to Charts. | Your RAG pipeline can't see charts. Half the answers in a board deck live in pixels, and your parser just drops them. | v1 template |
| RAG #12 | CLIP reads 77 tokens of text. | CLIP's text encoder has a context length of 77 tokens. That one number shapes how you build direct multi-modal retrieval for RAG. | B (claim) |
| RAG #13 | Deleted docs still answer | Change detection in RAG ingestion has a blind spot: deleted files. | A (story) |
| RAG #14 | Where did the refund rule go? | Fixed-size chunking with overlap comes with one guarantee: any fact shorter than the overlap lands whole in at least one chunk. | B (claim) |
| RAG #15 | Periods aren't a default separator | Recursive splitting can still cut a sentence in half. | C (checklist preview) |
| RAG #16 | Cut where the meaning jumps between sentences. | Semantic chunking cuts where the meaning jumps between sentences. | B (claim) |
| RAG #17 | The top 4 chunks all missed the answer. Return the section around the top hit, and size that section yourself. | The top 4 chunks for a warranty question all missed the sentence that answers it. | A (story) |
| RAG #18 | One sentence reached the model three times, inside overlapping windows. | Sentence-window retrieval in LlamaIndex needs MetadataReplacementPostProcessor, or the model gets one bare sentence. | B (claim) |
| RAG #19 | Chunk code per function, with its file, class and constants on top. At 250 characters, three splitters sent a search for the refund limit to the imports block. | Chunking code by function, with file, class and constants on top, fixed a search three splitters missed at 250 characters. | A (story) |
| RAG #20 | 0.005, 0.12 and 90, with no column names: Frankfurt's cold-tier row after a 300-character split. Keep whole rows, with the title and header on every chunk. | When chunking tables for RAG, a 300-character split stripped the column names from 12 of 18 rows. | C (checklist preview) |
| RAG #21 | Ask whether the liability cap covers lost Customer Data, and search hands back the cap, cut off at "do not apply to:". | A 300-character split cut a contract clause off from its exceptions. | A (story) |
| RAG #22 | Customer: "And if I upgrade mid-month, what happens to the bill?" A 200-character split puts the agent's answer in the next chunk. | BM25 ranked the answer to "What happens to the bill if I upgrade mid-month?" 5th of 7 chunks. | B (claim) |
| RAG #23 | BM25 put the answer to ACME's Q2 growth question in a 16-way tie for 5th, behind four chunks that never mention revenue. | The chunk that answers "ACME's revenue growth in Q2 2023?" says only "the company's revenue grew by 3%". | A (story) |
