# Keyword and AI search playbook

Applies to **every post on every channel**: carousels, text posts, LinkedIn articles, X threads. The daily run reads this file before writing anything.

Based on the research doc [AI engineering on LinkedIn: trending keywords and AI search](https://claude.ai/artifact/VedncmQoYK8jx8WLCrsq4e) (5 Nov 2026). Keyword trends move fast: re-check this file every 3 months.

_Last updated: 5 Nov 2026_

---

## 1. Pick one primary keyword before writing

- Every post has **one primary keyword**: the concept it teaches. For the RAG series, it's the cover title in `ai_engineering/rag/COVER_LABELS.md`.
- **Concept first, framework second.** Lead with "RAG chunking", "AI agents", "LLM evals"; use LangChain, LangGraph and LangSmith as supporting terms. AI engineer job posts name concepts about twice as often as frameworks.
- **One term per idea.** Use the same words on the cover, in the caption, in the article and in the hashtags. Don't swap synonyms inside one post.
- Say **"context engineering"**, not "prompt engineering", to engineers. Use "prompt engineering" only for non-engineer audiences (for example, clinic owners).

| Tier | Keywords | Why |
|---|---|---|
| Lead | AI agents, RAG | The most-requested skills in AI engineer job posts after ML and LLMs (47% and 40% of 4,155 postings, June 2026) |
| Rising, own them early | LLM evals, LLM-as-judge, context engineering, MCP, LangGraph | Growing fast, and few creators explain them well. Only 52% of teams run offline evals, while 89% have observability |
| Supporting | LangChain, LangSmith, vector databases, observability, tracing, fine-tuning | Use as secondary terms and tags |

### Keyword clusters

| Cluster | Keywords to use |
|---|---|
| Agents | AI agents, agentic AI, tool calling, function calling, multi-agent systems, human-in-the-loop, agent memory, guardrails |
| RAG and retrieval | RAG, chunking strategies, hybrid search, BM25, reranking, embeddings, vector database, semantic search, agentic RAG, GraphRAG, contextual retrieval |
| Context engineering | context engineering, context window, long context, context rot, memory, compaction |
| Evals and observability | LLM evals, golden dataset, LLM-as-judge, regression testing, tracing, LLM observability, LangSmith, hallucination |
| Frameworks and protocols | LangChain, LangGraph, LangSmith, LlamaIndex, MCP, A2A, OpenAI Agents SDK, Claude Agent SDK |
| Fine-tuning and models | fine-tuning, LoRA, distillation, small language models, open-weight models |
| Production (LLMOps) | latency, cost per query, semantic cache, rate limits, multi-tenancy, deployment |
| AI search | AI search, query fan-out, agentic search, web search API, citations, grounding |

## 2. Where the primary keyword must appear

1. **Cover:** the module label and topic title, exactly as written in `COVER_LABELS.md` (RAG series).
2. **Caption, first 2 lines (≤ 200 characters):** the keyword and the problem it solves, in plain words. These lines must make sense on their own.
3. **X thread:** tweet 1.
4. **LinkedIn article:** the headline and the first paragraph, when a post is repurposed as an article.

## 3. Write for AI search (every post)

AI search engines (ChatGPT Search, Google AI Mode, Perplexity) cite LinkedIn in 11% of answers, and they cite small accounts as often as big ones.

- **Answer first.** Put the main claim or answer in the first lines; don't save it for the last slide.
- **Evidence in every post:** at least one verified number, one short quote from a named source, or one named source (a person, paper or official doc). Name the source in the text; no links in the LinkedIn post body. In the GEO study (KDD 2024), quotations raised AI visibility by about 41%, statistics by 31% and cited sources by 27%.
- **Original content only.** No reshares as posts; 95% of the LinkedIn posts AI cites are original.
- **Knowledge or practical advice:** what to do, when, and why.
- **No keyword stuffing.** Use the primary keyword naturally; stuffing lowered AI visibility by about 8% in the same study.

## 4. Hashtags

LinkedIn hashtags are topic labels now; they no longer push posts into anyone's feed.

- **LinkedIn: exactly 3,** in this pattern: one broad (`#AIEngineering`), one cluster (`#RAG`, `#AIAgents`, `#LLMEvals`, `#MCP`, `#ContextEngineering`, `#AISearch`) and one specific to the post (for example `#Reranking`, `#LangGraph`, `#HybridSearch`).
- **Instagram:** the same 3, plus up to 2 more on-topic tags.
- **X:** 1–2 in the last tweet. **Facebook:** 1–2.
- No generic tags such as `#AI` or `#Tech`.

## 5. LinkedIn articles: the way into AI search

Articles make up 50–66% of the LinkedIn content AI search cites; feed posts make up 15–28%.

- Each week's posts (or each finished mini-series) become **one LinkedIn article of 500–2,000 words**, with the answer in the first paragraph and the same primary keywords.
- Keep a **hub article** in Featured that lists every article by module.

## 6. Profile alignment

Posts must stay inside the profile's topics: AI agents, RAG, evals, context engineering, MCP, LLMs in production.

- **Headline:** AI Engineer · RAG and AI agents in production · LangGraph, LangSmith, evals
- **About, first 3 lines:** the problem solved, in the words a client or recruiter would type.
- **Pinned skills:** RAG, AI Agents, LangGraph, LLM Evaluation, Model Context Protocol.

## 7. Checks before publishing

The daily run stops and reports if any of these fail:

- The primary keyword is missing from the cover title or the first 2 caption lines.
- The post has no verified number, quote or named source.
- The LinkedIn hashtags aren't exactly 3 in the broad, cluster, specific pattern.
- The caption or slides contain banned phrasing (see the VOICE section of the carousel prompt).

## 8. Monthly AI-citation check

Once a month, ask ChatGPT, Perplexity and Google AI Mode five questions readers ask, and log whether Shahbaz is cited. Starting questions:

1. How do I stop my RAG system cutting sentences in half?
2. Fixed-size vs recursive vs semantic chunking: which should I use?
3. How do I evaluate a RAG system?
4. What is context engineering for AI agents?
5. Who explains RAG for engineers on LinkedIn?
