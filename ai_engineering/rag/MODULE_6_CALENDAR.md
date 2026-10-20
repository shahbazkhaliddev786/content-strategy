# Pillar 2 — Content Calendar: Module 6 (Reranking)

**Source:** `RAG_Curriculum (1).md` → Module 6
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 6 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 6 has 5 concepts → 8 posts (1 mini-series).**
**Key terms to cover (6):** `Cross-encoder` · `Two-stage retrieval` · `Reranker` (Cohere Rerank, BGE-reranker, Jina Reranker) · `Listwise vs. pointwise vs. pairwise ranking` · `LLM-as-reranker` · `Candidate set / top-k retrieval before rerank`

---

## Post 1 — Cast a wide net, then be picky: the two-stage pattern

**Concept:** Two-stage retrieval pattern (broad recall → precise rerank).

**Angle:** Fast retrieval (Modules 4–5) optimizes for *recall* — get the right docs *somewhere* in the top 50 — but its ordering is rough. Reranking is stage two: take that cheap, broad shortlist and re-score it precisely so the best few rise to the top. The architecture is "recall cheaply, then rank precisely," and it only works because stage one hands stage two a small candidate set.

**Key terms covered here:**
- `Two-stage retrieval` *(primary)* — a cheap, high-recall first pass (vector/hybrid) followed by a slower, high-precision reranking pass over its results.
- `Candidate set / top-k retrieval before rerank` *(primary)* — the shortlist stage one returns (e.g. top 50–100) that stage two re-scores; its size is the key dial between quality and cost.

**Senior-level tie-in:** the whole value of reranking hinges on stage one having *recall* — if the right doc isn't in the candidate set, no reranker can recover it; tune retrieval depth before blaming the reranker.

---

## Post 2 — Why cross-encoders out-rank bi-encoders

**Concept:** Cross-encoder architecture and why it outperforms bi-encoders for ranking.

**Angle:** Callback to Module 3's bi-encoder: it embeds query and document *separately*, so they never "see" each other — fast and precomputable, but coarse. A cross-encoder feeds query + document *together* through the model, letting every query token attend to every document token. That full interaction captures relevance a dot product can't — at the cost of being impossible to precompute.

**Key terms covered here:**
- `Cross-encoder` *(primary)* — a model that jointly encodes (query, document) as one input and outputs a single relevance score; maximal accuracy, no precomputation possible.

**Senior-level tie-in:** articulate the exact trade vs. a bi-encoder — accuracy from joint attention bought with per-query compute that scales with candidate-set size (which is why it's a *second* stage, not the first).

---

## Post 3 — Choosing a reranker, and how rerankers actually score *(mini-series · 4 parts)*

**Concept:** Reranking model options (open-source vs. API-based).

**Angle:** Two decisions here. First, the model: hosted APIs (Cohere Rerank) vs. self-hosted open weights (BGE-reranker, Jina Reranker) — trading convenience/cost/data-residency. Second, the *scoring paradigm*, which shapes quality and cost: score each doc alone, compare pairs, or order the whole list at once.

**Series structure:** one post on choosing the model, then one post per scoring paradigm.

**Senior-level tie-in (series):** pick on constraints — API for speed-to-ship and no GPU ops; open-source for cost-at-scale and data control; and match the scoring paradigm to your latency budget.

### Post 3.1 — API or open-source: choosing a reranker model

**Concept:** Hosted reranker APIs vs. self-hosted open-weight rerankers.

**Angle:** A hosted API (e.g. Cohere Rerank) means no GPUs to run and fast shipping, but you pay per call and your documents leave your infrastructure. Self-hosted open weights (e.g. BGE-reranker, Jina Reranker) mean you run the inference yourself, in exchange for lower cost at scale and full data control.

**Key terms covered here:**
- `Reranker` *(primary)* — a dedicated relevance-scoring model applied to the candidate set; options span API (Cohere) and open-source (BGE, Jina).

**Senior-level tie-in:** pick on constraints — API for speed-to-ship and no GPU ops; open-source for cost-at-scale and data control. Benchmark candidates on your own queries, not a leaderboard.

### Post 3.2 — Pointwise ranking: score each document on its own

**Concept:** Pointwise reranking.

**Angle:** The reranker looks at one (query, document) pair at a time and outputs a relevance score; sort by score and you're done. Every pair is independent, so all candidates can be scored in parallel. Most cross-encoder rerankers work this way.

**Key terms covered here:**
- `Listwise vs. pointwise vs. pairwise ranking` *(primary)* — pointwise scores each doc independently; pairwise compares docs two at a time; listwise considers the whole candidate list jointly (usually best quality, highest cost).
- `Reranker` *(reinforced)*

**Senior-level tie-in:** pointwise is the cheapest and most parallel paradigm, but each score is judged in isolation — the model never sees what the other candidates say.

### Post 3.3 — Pairwise ranking: which of these two is better?

**Concept:** Pairwise reranking.

**Angle:** Instead of an absolute score, the model answers a relative question: "for this query, is document A or document B more relevant?" Comparing pairs is often easier to judge reliably than assigning a number, and the comparisons are aggregated into a final order.

**Key terms covered here:**
- `Listwise vs. pointwise vs. pairwise ranking` *(reinforced)* — the pairwise paradigm.

**Senior-level tie-in:** the number of comparisons grows quickly with the candidate count (every pair, in the naive version), so pairwise only fits small candidate sets or a final top-few refinement.

### Post 3.4 — Listwise ranking: order the whole list at once

**Concept:** Listwise reranking.

**Angle:** The model sees all the candidates together and outputs an ordering directly, so it can judge each document against the others — spotting duplicates or a clearly better source. This is usually done with an LLM, and it's typically the highest quality and the highest cost.

**Key terms covered here:**
- `Listwise vs. pointwise vs. pairwise ranking` *(reinforced)* — the listwise paradigm.

**Senior-level tie-in:** the whole candidate list must fit in one model call, so long lists are processed in overlapping windows — and latency is that of a full generation (Post 5).

---

## Post 4 — The latency tax: when reranking is worth it (and when it isn't)

**Concept:** Cost/latency tradeoffs of reranking.

**Angle:** Reranking is never free. Because a cross-encoder can't precompute, every query pays to score every candidate inline — latency grows with candidate-set size. Sometimes that precision is decisive; under a hard real-time SLA it's a dealbreaker. Give a decision rubric: candidate-set depth, model choice, and whether the quality lift justifies the milliseconds.

**Key terms covered here:**
- `Cross-encoder` *(reinforced)* — the source of the cost: joint encoding means per-query, per-candidate compute with nothing cached.
- `Candidate set / top-k retrieval before rerank` *(reinforced)* — the primary cost lever: reranking top-100 costs ~2× reranking top-50; shrink it to hit latency targets.

**Senior-level tie-in:** the module bar — justify reranking by scenario: worth it when precision@k drives outcomes and latency budget is generous; skip or shrink it under hard real-time SLAs, and tune candidate depth as the main knob.

---

## Post 5 — The model as judge: LLM-as-reranker

**Concept:** LLM-based reranking (using a generative model itself as a judge/reranker).

**Angle:** The most powerful — and most expensive — option: give an LLM the query and the candidate set and have it judge relevance directly, often listwise (order all candidates in one pass). It can apply reasoning and instructions a trained reranker can't, but adds the latency and cost of a full generation. Cover prompt patterns and where it earns its keep.

**Key terms covered here:**
- `LLM-as-reranker` *(primary)* — prompting a generative LLM to score or reorder the candidate set as a relevance judge.
- `Listwise vs. pointwise vs. pairwise ranking` *(reinforced)* — LLMs naturally do listwise reranking (reason over all candidates together), which is where their advantage is biggest.

**Senior-level tie-in:** reserve it for high-value, low-QPS queries or offline eval where quality outranks latency/cost; for high-throughput serving, a dedicated cross-encoder reranker is the pragmatic choice.

---

## Coverage check (all 6 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Two-stage retrieval` | Post 1 | — |
| `Candidate set / top-k retrieval before rerank` | Post 1 | Post 4 |
| `Cross-encoder` | Post 2 | Post 4 |
| `Reranker` (Cohere/BGE/Jina) | Post 3.1 | Post 3.2 |
| `Listwise vs. pointwise vs. pairwise ranking` | Post 3.2 | Posts 3.3, 3.4, 5 |
| `LLM-as-reranker` | Post 5 | — |

✅ All 6 Module 6 key terms covered across the 8 posts.
