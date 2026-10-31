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
