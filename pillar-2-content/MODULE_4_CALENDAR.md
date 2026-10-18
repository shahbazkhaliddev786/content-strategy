# Pillar 2 — Content Calendar: Module 4 (Indexing & Vector Search)

**Source:** `RAG_Curriculum (1).md` → Module 4
**Rule:** 1 concept = 1 post. Every Module 4 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 4 has 7 concepts → 7 posts.**
**Key terms to cover (15):** `Approximate Nearest Neighbor (ANN)` · `k-Nearest Neighbor (kNN)` · `HNSW (Hierarchical Navigable Small World)` · `ef_construction` / `ef_search` · `M (graph connectivity parameter)` · `IVF (Inverted File Index)` · `Product Quantization (PQ)` · `LSH (Locality-Sensitive Hashing)` · `ScaNN` · `Recall@k` · `Vector database` · `Metadata filtering` · `Pre-filtering vs. post-filtering` · `Index sharding` · `Replication factor`

---

## Post 1 — Exact vs. approximate: why search gets "good enough" on purpose

**Concept:** Exact (brute-force) vs. approximate nearest neighbor (ANN) search.

**Angle:** Finding the closest vectors *exactly* means comparing the query against every stored vector — correct, but linear in corpus size, so it collapses at millions of docs. ANN deliberately trades a sliver of accuracy for orders-of-magnitude speed. The whole module is about that trade, so define it precisely and introduce the metric that quantifies it.

**Key terms covered here:**
- `k-Nearest Neighbor (kNN)` *(primary)* — exact, brute-force search for the k closest vectors; the correct-but-unscalable baseline.
- `Approximate Nearest Neighbor (ANN)` *(primary)* — algorithms that find *most* of the true nearest neighbors far faster by not checking everything.
- `Recall@k` *(primary)* — the quality metric: of the true top-k (per exact kNN), what fraction did ANN actually return? The number you trade away for speed.

**Senior-level tie-in:** frame every later choice as a point on the recall/latency/memory surface — there is no "best" index, only the right trade for your SLA.

---

## Post 2 — A field guide to the core ANN algorithms

**Concept:** Core ANN algorithms — HNSW, IVF, IVF-PQ, LSH, ScaNN.

**Angle:** Three families solve "find neighbors fast" differently: **graphs** (navigate a proximity graph), **clustering** (only search the nearest buckets), and **hashing** (collide similar vectors into the same bucket). Quantization then compresses vectors to fit memory. Give one crisp mental model per algorithm and when each wins.

**Key terms covered here:**
- `HNSW (Hierarchical Navigable Small World)` *(primary)* — a layered proximity graph you greedily navigate; the default for high recall at low latency, at a memory cost.
- `IVF (Inverted File Index)` *(primary)* — cluster vectors, search only the few nearest clusters; fast and memory-light, tunable via how many clusters you probe.
- `Product Quantization (PQ)` *(primary)* — compress vectors into compact codes (often paired as IVF-PQ) to shrink memory, trading some precision.
- `LSH (Locality-Sensitive Hashing)` *(primary)* — hash functions that map similar vectors to the same bucket; simple, less dominant today.
- `ScaNN` *(primary)* — Google's anisotropic-quantization approach, strong on the accuracy/speed frontier at scale.

**Senior-level tie-in:** be able to reach for IVF-PQ when memory is the constraint and HNSW when recall/latency is — and say *why* in one sentence each.

---

## Post 3 — The knobs: build-time vs. query-time tuning

**Concept:** Index build-time vs. query-time tuning knobs.

**Angle:** An index isn't "set it and forget it" — it has dials, and they split into two groups. Build-time knobs are baked in when you construct the index (expensive to change); query-time knobs can be adjusted per request. Using HNSW as the worked example, show which is which and how each moves recall vs. latency/memory.

**Key terms covered here:**
- `ef_construction` / `ef_search` *(primary)* — `ef_construction` (build-time) sets how thoroughly the graph is built; `ef_search` (query-time) sets how widely each query explores — higher = better recall, higher latency.
- `M (graph connectivity parameter)` *(primary)* — build-time: edges per node; higher M = better recall and more memory.
- `HNSW` *(reinforced)* — the index these knobs belong to.
- `Recall@k` *(reinforced)* — the needle every knob moves, against latency/memory.

**Senior-level tie-in:** hits the module bar — explain the `ef_search` recall/latency tradeoff from memory: raise it to recover recall at the cost of query latency, with no rebuild required.

---

## Post 4 — Choosing a vector database (it's not about raw QPS)

**Concept:** Vector database landscape and selection criteria.

**Angle:** The market is a blur of options — managed services, embedded libraries, and Postgres extensions. The honest selection criteria are rarely peak QPS; they're filtering support, metadata/hybrid capability, operational burden, cost at your scale, and how it handles updates and migrations. Give a decision rubric, not a leaderboard.

**Key terms covered here:**
- `Vector database` *(primary)* — a store purpose-built to index and query vectors at scale (e.g. Pinecone, Weaviate, Qdrant, Milvus, pgvector, Chroma); spans managed, self-hosted, embedded, and SQL-extension forms.

**Senior-level tie-in:** the senior answer starts with constraints (scale, filtering needs, ops appetite, existing stack) and *derives* the DB — "pgvector if you're already on Postgres and small; a dedicated store when scale or filtering demands it."

---

## Post 5 — Filtering strategies and the filtered-ANN trap

**Concept:** Filtering strategies — pre-filter, post-filter, filtered ANN.

**Angle:** "Only search this clinic's documents" sounds trivial, but naive filtering quietly breaks ANN. Post-filtering can return too few results (the ANN top-k gets filtered away); pre-filtering can be slow or bypass the index; and filtered-HNSW has a specific pitfall where restrictive filters strand the graph traversal. Walk the three approaches and their failure modes.

**Key terms covered here:**
- `Metadata filtering` *(primary)* — constraining results by stored attributes (tenant, date, type) alongside vector similarity.
- `Pre-filtering vs. post-filtering` *(primary)* — filter the candidate set *before* the ANN search vs. *after* the top-k is returned; each trades correctness, recall, and speed differently.

**Senior-level tie-in:** hits the module bar — describe the filtered-HNSW pitfall from memory: a highly selective filter can disconnect the graph walk so it misses valid matches, which is why engines implement dedicated filtered-search (not just post-filter).

---

## Post 6 — Scaling the index: sharding & replication

**Concept:** Sharding, replication, and scaling indexes.

**Angle:** One node eventually runs out of RAM or throughput. Two orthogonal moves fix different problems: **sharding** splits one index across nodes so a bigger-than-memory corpus fits and queries fan out in parallel; **replication** copies the index so you can serve more concurrent queries and survive node failure. Clarify that they solve *different* bottlenecks.

**Key terms covered here:**
- `Index sharding` *(primary)* — partitioning vectors across nodes (by hash or segment); each shard searches its slice, results are merged. Solves size + parallelism.
- `Replication factor` *(primary)* — how many copies of each shard exist; raises read throughput and availability at a storage/consistency cost.

**Senior-level tie-in:** diagnose correctly — "index too big / queries too slow → shard; too many concurrent queries / need HA → replicate." Conflating them wastes money.

---

## Post 7 — One system or several? The hybrid-storage question

**Concept:** Hybrid storage — vector + metadata + full-text in one system vs. separate systems.

**Angle:** Real retrieval needs vectors *and* metadata filters *and* often keyword/full-text. Do you keep them in one store that does everything (simpler, transactional, consistent) or specialized systems wired together (best-of-breed, but you own the sync and consistency problem)? Lay out the trade and when each makes sense.

**Key terms covered here:**
- `Vector database` *(reinforced)* — here evaluated as a single-system home for vectors + metadata + full-text, vs. a vectors-only component in a multi-store setup.
- `Metadata filtering` *(reinforced)* — the capability that most often forces the decision: co-locating metadata with vectors makes filtered search far easier than syncing two stores.

**Senior-level tie-in:** single-system by default for consistency and operational simplicity; split only when a specialized need (scale, a mature full-text engine) outweighs the cost of keeping stores in sync.

---

## Coverage check (all 15 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `k-Nearest Neighbor (kNN)` | Post 1 | — |
| `Approximate Nearest Neighbor (ANN)` | Post 1 | — |
| `Recall@k` | Post 1 | Post 3 |
| `HNSW (Hierarchical Navigable Small World)` | Post 2 | Post 3 |
| `IVF (Inverted File Index)` | Post 2 | — |
| `Product Quantization (PQ)` | Post 2 | — |
| `LSH (Locality-Sensitive Hashing)` | Post 2 | — |
| `ScaNN` | Post 2 | — |
| `ef_construction` / `ef_search` | Post 3 | — |
| `M (graph connectivity parameter)` | Post 3 | — |
| `Vector database` | Post 4 | Post 7 |
| `Metadata filtering` | Post 5 | Post 7 |
| `Pre-filtering vs. post-filtering` | Post 5 | — |
| `Index sharding` | Post 6 | — |
| `Replication factor` | Post 6 | — |

✅ All 15 Module 4 key terms covered across the 7 posts.
