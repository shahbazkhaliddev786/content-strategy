# RAG #23 sources: Contextual chunk augmentation (contextual retrieval)

Logged, not posted. Checked 23 Nov 2026.

## Anthropic, "Introducing Contextual Retrieval" (published 19 Sep 2024)
URL: https://www.anthropic.com/engineering/contextual-retrieval (canonical: https://www.anthropic.com/research/contextual-retrieval)
- The SEC filing example (slide 2): original chunk "The company's revenue grew by 3% over the previous quarter." and the contextualized chunk "This chunk is from an SEC filing on ACME corp's performance in Q2 2023; the previous quarter's revenue was $314 million. ..." The query "What was the revenue growth for ACME Corp in Q2 2023?" is also theirs.
- The contextualizer prompt (slide 6), given for Claude 3 Haiku: `<document>{{WHOLE_DOCUMENT}}</document>` + "Here is the chunk we want to situate within the whole document" + `<chunk>{{CHUNK_CONTENT}}</chunk>` + "Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else." On the slide the placeholders are Python format fields `{doc}` and `{chunk}`.
- "usually 50-100 tokens", prepended before embedding and before building the BM25 index (slide 3, cheat sheet).
- Metric: 1 minus recall@20, averaged across their datasets, Gemini Text 004 embeddings. Top-20 failure rate 5.7% → 3.7% (contextual embeddings, −35%) → 2.9% (+ contextual BM25, −49%) → 1.9% (+ reranking with Cohere's reranker, 150 candidates to top 20, −67%) (slide 8).
- Cost: "$1.02 per million document tokens", assuming 800-token chunks, 8k-token documents, 50-token context instructions and 100 tokens of context per chunk, with prompt caching (slide 9).
- Knowledge bases under 200,000 tokens (~500 pages): include the whole knowledge base in the prompt (slide 11).

## Anthropic Python SDK (anthropic 2.12.0)
- `client.messages.create(model=..., max_tokens=..., messages=[...])`; text blocks accept `cache_control: {"type": "ephemeral"}` (checked in `anthropic.types.TextBlockParam`). RAG23_verify.py runs `context_for()` from slide 7 against a fake client and checks the request: the document block carries `cache_control`, the chunk block doesn't.
- Prompt caching docs: https://docs.claude.com/en/docs/build-with-claude/prompt-caching

## Test run (slides 4, 5, 10)
- 16 made-up quarterly reports (ACME Corp, Globex, Halvar Labs, Brightline Foods × Q1–Q4 2023), 7 sections each, built in RAG23_verify.py.
- LangChain `RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=0)` (langchain-text-splitters 1.1.3) → 96 chunks, one section each.
- BM25: `rank_bm25.BM25Okapi` 0.2.2 (default k1=1.5, b=0.75), tokens = lowercase `\w+`.
- Plain: ACME's 4 Overview chunks 7.65; all 16 Results chunks tie at 3.62 (ranks 5–20; the answer is 6th in index order).
- Title + heading prefix (no LLM): answer 1st at 6.81; ACME Q1, Q3, Q4 Results 5.89.
- Template context line on all 96 chunks (no LLM call; written in the style of Anthropic's example): ACME Q2 and Q3 Results tie at 9.06, because Q3's line says "growth over Q2 2023".
- No embedding model was run (model downloads are blocked in this environment); the embedding numbers on slide 8 are Anthropic's.
