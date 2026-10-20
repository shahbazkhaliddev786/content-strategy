# Pillar 2 — Content Calendar: Module 12 (System Design Practice) — FINAL MODULE

**Source:** `RAG_Curriculum (1).md` → Module 12
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). **Special case — integrative module: NO new key terms.** The curriculum states this is "where every term above gets used together," so every post here *reinforces* terms from earlier modules rather than introducing new ones. Term-coverage is therefore N/A by design; the bottom table maps each post to the modules it integrates instead.

**Module 12 has 5 concepts → 5 posts (0 mini-series).**
**New key terms:** none (integrative capstone).

---

## Post 1 — Don't design yet: the requirements-clarification framework

**Concept:** Requirements clarification framework for RAG system design questions.

**Angle:** The fastest way to fail a RAG design question (or a real project) is to start drawing boxes before asking what you're building. Seniors interrogate the requirements first: What *kinds* of queries (lookup vs. multi-hop vs. aggregation)? How many documents, changing how often? What's the latency budget and cost ceiling? How bad is a wrong answer — do we need citations and an abstention path? Those answers determine every downstream choice.

**Terms reinforced here (all from earlier modules):**
- `Query-type segmentation` (M8) — nail the query mix up front; it dictates retrieval strategy.
- `Latency budget` (M9) — the user-facing time target that constrains reranking and generation.
- `Cost per query` (M9) — the unit economics that decide managed-vs-self-hosted and model choices.
- `Faithfulness` / `Abstention` (M7) — accuracy and guardrail requirements set the generation design.

**Senior-level tie-in:** spend the first ~90 seconds on requirements — a design that states its assumptions (query types, scale, latency, accuracy bar) reads as senior; one that jumps to "we'll use a vector DB" reads as junior.

---

## Post 2 — The 2-minute skeleton: sketching an end-to-end architecture

**Concept:** End-to-end architecture sketching under time pressure.

**Angle:** You need a repeatable skeleton you can draw fast and adapt — not a blank-page scramble. The spine is always: **ingestion** (parse → chunk → embed → index) → **retrieval path** (hybrid search → rerank) → **grounded generation** (context assembly → cited answer → guardrails). Draw that, then justify each box from the Post-1 requirements. This post lays out the full capstone template the whole curriculum has been building toward.

**Terms reinforced here (all from earlier modules):**
- `Chunk` (M2) — the ingestion unit and its strategy choice.
- `Bi-encoder` / embeddings (M3) — how chunks and queries become vectors.
- `Vector database` / `HNSW` (M4) — where vectors live and how they're searched.
- `Hybrid search` (M5) — dense + sparse on the retrieval path.
- `Cross-encoder` / reranking (M6) — the precision second stage.
- `Grounded generation` / `Citation enforcement` (M7) — the answer layer and its guardrails.

**Senior-level tie-in:** the module bar — deliver a full answer in ~8–10 min following the structure **requirements → ingestion → retrieval path → guardrails → eval/observability → scaling/cost → named failure modes**. Memorize this skeleton; it's the backbone every other post plugs into.

---

## Post 3 — Design against named failures (out loud)

**Concept:** Explicitly naming the failure modes you're designing around.

**Angle:** The single strongest signal of seniority in a design discussion is proactively naming what will go wrong and showing the mitigation — before anyone asks. Juniors present a happy path; seniors say "here's where this breaks, and here's the guard." Walk the catalog assembled across the curriculum and attach a fix to each.

**Terms reinforced here (all from earlier modules):**
- `Hallucination` (M0) — mitigated by grounded generation + citation checks.
- `Chunk boundary problem` (M2) — mitigated by recursive/semantic chunking + overlap.
- `Lost-in-the-middle` (M7) — mitigated by relevance-aware chunk ordering.
- `Empty-retrieval fallback` / `Deduplication` / `Recency boosting` (M9) — guards for empty, redundant, and stale retrieval.
- `Embedding drift` (M3) — handled by a safe re-index migration on model upgrades.

**Senior-level tie-in:** keep a mental checklist of 5–6 failure→fix pairs and volunteer them — "I'm designing around hallucination with citation enforcement, around stale results with recency boosting…" — this is what separates a senior answer from a textbook one.

---

## Post 4 — What breaks at 1000×: scaling from 10K to 10M docs

**Concept:** Scaling considerations (10K → 10M docs).

**Angle:** A design that's fine for 10K documents quietly falls over at 10M. Exact search becomes impossible, a single index node runs out of memory, re-embedding the corpus becomes a project, and per-query cost balloons. Walk the specific things that break as the corpus grows three orders of magnitude — and the knobs that fix each.

**Terms reinforced here (all from earlier modules):**
- `ANN` / `HNSW` / `IVF-PQ` (M4) — approximate search and quantization become mandatory at scale.
- `Index sharding` / `Replication factor` (M4, M9) — split for size/parallelism, replicate for throughput/HA.
- `Semantic caching` / `Embedding cache` (M9) — absorb repetitive traffic to protect latency and cost.
- `Cost per query` / `Latency budget` (M9) — the two ceilings that force every scaling trade-off.

**Senior-level tie-in:** answer scaling as "what breaks and the knob that fixes it" — exact→ANN, memory→sharding+quantization, throughput→replication, cost/latency→caching — not just "we'll add more servers."

---

## Post 5 — Build vs. buy: managed vs. self-hosted

**Concept:** Build-vs-buy decisions (managed vector DB vs. self-hosted).

**Angle:** The closing trade every RAG project faces. Managed services (e.g. Pinecone) get you shipping fast with no ops, but cost more at scale and cede control. Self-hosted (Milvus, Qdrant, pgvector) means control, data residency, and cheaper-at-scale — at the price of running it yourself. There's no universal answer; derive it from the Post-1 requirements (scale, team, budget, compliance).

**Terms reinforced here (all from earlier modules):**
- `Vector database` — managed vs. self-hosted vs. Postgres-extension (M4).
- `Cost per query` (M9) — the crossover point where self-hosting starts to pay off.
- `Observability / retrieval tracing` (M9) — easier to get managed, must be built if self-hosted.
- `Multi-tenancy` (M9) — compliance/isolation needs that can force a self-hosted or enterprise-tier choice.

**Senior-level tie-in:** give a *decision rule*, not a favorite — "managed to validate fast and while small; revisit self-hosting when per-query cost at projected scale, data-residency, or deep customization outweighs the ops burden."

---

## Coverage note (integrative module — no new terms)

This module introduces no new key terms, so term-coverage is N/A by design. Instead, the five posts
collectively re-integrate the full curriculum arc — ingestion, retrieval, reranking,
generation/guardrails, eval/observability, scaling, and cost.

| Post | Concept | Modules integrated |
|---|---|---|
| 1 | Requirements clarification | M7, M8, M9 |
| 2 | Architecture sketching | M2, M3, M4, M5, M6, M7 |
| 3 | Named failure modes | M0, M2, M3, M7, M9 |
| 4 | Scaling 10K→10M | M4, M9 |
| 5 | Build-vs-buy | M4, M9 |

✅ All 5 Module 12 concepts covered; the capstone design skeleton lives in Post 2. (No new terms — by design.)
