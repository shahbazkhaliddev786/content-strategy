# Pillar 2 — Content Calendar: Module 4 (Indexing & Vector Search)

**Source:** `RAG_Curriculum (1).md` → Module 4
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 4 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 4 has 7 concepts → 16 posts (3 mini-series).**
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

## Post 2 — A field guide to the core ANN algorithms *(mini-series · 6 parts)*

**Concept:** Core ANN algorithms — HNSW, IVF, IVF-PQ, LSH, ScaNN.

**Angle:** Three families solve "find neighbors fast" differently: **graphs** (navigate a proximity graph), **clustering** (only search the nearest buckets), and **hashing** (collide similar vectors into the same bucket). Quantization then compresses vectors to fit memory. Give one crisp mental model per algorithm and when each wins.

**Series structure:** one post per algorithm (full Problem → Intuition → How it works → Trade-offs → When to use → When NOT to use), then a comparison post that puts all five side by side.

**Senior-level tie-in (series):** be able to reach for IVF-PQ when memory is the constraint and HNSW when recall/latency is — and say *why* in one sentence each.

### Post 2.1 — HNSW: search by walking a graph

**Concept:** HNSW — graph-based approximate nearest neighbor search.

**Angle:** Build a graph where each vector links to its near neighbors, stacked in layers: sparse upper layers with long-range links, a dense bottom layer with short ones. A query enters at the top, greedily hops toward closer nodes, and drops down a layer each time it can't improve — like zooming in on a map. Few distance computations, high recall.

**Key terms covered here:**
- `HNSW (Hierarchical Navigable Small World)` *(primary)* — a layered proximity graph you greedily navigate; the default for high recall at low latency, at a memory cost.

**Senior-level tie-in:** HNSW's cost is memory — it stores full vectors *plus* the graph's edges — so it's the default when recall and latency matter and the index fits in RAM. Its tuning knobs come in Post 3.

### Post 2.2 — IVF: only search the nearest buckets

**Concept:** IVF — clustering-based approximate nearest neighbor search.

**Angle:** Cluster all vectors into buckets (k-means), each with a centroid. At query time, find the few centroids closest to the query and search only inside those buckets, skipping the rest of the corpus. How many buckets you probe is the recall-vs-speed dial.

**Key terms covered here:**
- `IVF (Inverted File Index)` *(primary)* — cluster vectors, search only the few nearest clusters; fast and memory-light, tunable via how many clusters you probe.

**Senior-level tie-in:** the failure mode is a true neighbor sitting in an unprobed bucket near a cluster border; IVF also needs a training step on representative data, and clusters can go stale if your data distribution shifts.

### Post 2.3 — Product Quantization: shrink every vector to a few bytes

**Concept:** Product Quantization — compressing vectors to fit memory.

**Angle:** Split each vector into sub-vectors and replace every sub-vector with the ID of its nearest entry in a small learned codebook. A 768-dim float32 vector (3,072 bytes) can shrink to tens of bytes, and distances are computed approximately from the codes. Usually paired with IVF (IVF-PQ): IVF picks the buckets, PQ keeps them small.

**Key terms covered here:**
- `Product Quantization (PQ)` *(primary)* — compress vectors into compact codes (often paired as IVF-PQ) to shrink memory, trading some precision.
- `IVF (Inverted File Index)` *(reinforced)* — the usual partner, combined as IVF-PQ.

**Senior-level tie-in:** compression costs precision — a common fix is to over-fetch candidates with PQ distances, then re-score the top ones with full vectors.

### Post 2.4 — LSH: hash similar vectors into the same bucket

**Concept:** Locality-Sensitive Hashing for approximate search.

**Angle:** Design hash functions where similar vectors are *likely* to get the same hash — for example, random hyperplanes: which side of each plane a vector falls on becomes its bucket code. Search only the query's bucket(s), and use several hash tables to raise the chance a true neighbor collides.

**Key terms covered here:**
- `LSH (Locality-Sensitive Hashing)` *(primary)* — hash functions that map similar vectors to the same bucket; simple, less dominant today.

**Senior-level tie-in:** LSH is simple and needs no training, but for dense embeddings graph and quantization methods usually reach higher recall at the same memory — know it, and know why it's rarely the default today.

### Post 2.5 — ScaNN: quantization tuned for ranking

**Concept:** ScaNN — Google's approach to large-scale vector search.

**Angle:** Standard quantization tries to minimize overall reconstruction error. ScaNN's anisotropic quantization instead preserves accuracy where it matters for ranking — on the inner products of high-scoring query–vector pairs. Combined with partitioning and a final re-scoring step, it sits strongly on the accuracy/speed frontier at scale.

**Key terms covered here:**
- `ScaNN` *(primary)* — Google's anisotropic-quantization approach, strong on the accuracy/speed frontier at scale.
- `Product Quantization (PQ)` *(reinforced)* — the baseline ScaNN improves on.

**Senior-level tie-in:** ScaNN is available as an open-source library and powers Google Cloud's managed vector search; outside that ecosystem, most teams meet HNSW or IVF-PQ first.

### Post 2.6 — HNSW vs. IVF vs. PQ vs. LSH vs. ScaNN: which one, when?

**Concept:** Comparing the core ANN algorithms.

**Angle:** Put all five side by side on recall, latency, memory, build cost, and update behavior. Graph (HNSW) for recall and latency when RAM allows; clustering (IVF) for a lighter footprint; quantization (PQ, ScaNN) when memory is the hard constraint; hashing (LSH) mostly as background. Every option is measured by the same yardstick: recall at a given latency.

**Key terms covered here:**
- `HNSW (Hierarchical Navigable Small World)` *(reinforced)*
- `IVF (Inverted File Index)` *(reinforced)*
- `Product Quantization (PQ)` *(reinforced)*
- `LSH (Locality-Sensitive Hashing)` *(reinforced)*
- `ScaNN` *(reinforced)*
- `Recall@k` *(reinforced)* — the metric every one of these trades against speed.

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

## Post 5 — Filtering strategies and the filtered-ANN trap *(mini-series · 4 parts)*

**Concept:** Filtering strategies — pre-filter, post-filter, filtered ANN.

**Angle:** "Only search this clinic's documents" sounds trivial, but naive filtering quietly breaks ANN. Post-filtering can return too few results (the ANN top-k gets filtered away); pre-filtering can be slow or bypass the index; and filtered-HNSW has a specific pitfall where restrictive filters strand the graph traversal. Walk the three approaches and their failure modes.

**Series structure:** one post per filtering approach, then a comparison post built around one variable — how selective the filter is.

**Senior-level tie-in (series):** hits the module bar — describe the filtered-HNSW pitfall from memory: a highly selective filter can disconnect the graph walk so it misses valid matches, which is why engines implement dedicated filtered-search (not just post-filter).

### Post 5.1 — Pre-filtering: narrow the set, then search

**Concept:** Pre-filtering — apply metadata filters before the vector search.

**Angle:** First select only the vectors that match the filter (this tenant, this date range), then run similarity search over that subset. Every result is guaranteed to match. The catch: the ANN index was built over the whole corpus, so searching an arbitrary subset either falls back to brute force over the matches or can't use the index efficiently.

**Key terms covered here:**
- `Metadata filtering` *(primary)* — constraining results by stored attributes (tenant, date, type) alongside vector similarity.
- `Pre-filtering vs. post-filtering` *(primary)* — filter the candidate set *before* the ANN search vs. *after* the top-k is returned; each trades correctness, recall, and speed differently.

**Senior-level tie-in:** pre-filtering shines when the filter is very selective (few matches → brute force is cheap and exact) and gets expensive when the filter matches a large share of the corpus.

### Post 5.2 — Post-filtering: search first, filter after

**Concept:** Post-filtering — run ANN, then drop results that fail the filter.

**Angle:** Run the normal ANN search for the top-k, then throw away results that don't match the filter. Fast and simple, because the index is used as built. The failure: with a selective filter, most of the top-k gets thrown away, and you return 2 results — or none — when 10 valid matches exist further down.

**Key terms covered here:**
- `Pre-filtering vs. post-filtering` *(reinforced)* — the "after" side of the trade.
- `Metadata filtering` *(reinforced)*

**Senior-level tie-in:** over-fetching (ask for top-100 to keep 10) helps, but it's a guess — it can't guarantee results under a highly selective filter.

### Post 5.3 — Filtered ANN: filter during the search (and its trap)

**Concept:** Filtered ANN — applying filters inside the index traversal.

**Angle:** Check the filter *while* walking the index, so only matching vectors count as results. This is what dedicated vector databases implement. The trap with graph indexes like HNSW: when the filter is very restrictive, the matching nodes can be scattered and poorly connected, so the greedy walk gets stranded and misses valid matches.

**Key terms covered here:**
- `Metadata filtering` *(reinforced)* — enforced inside the search itself.
- `HNSW (Hierarchical Navigable Small World)` *(reinforced)* — the graph whose connectivity a restrictive filter can break.

**Senior-level tie-in:** describe the filtered-HNSW pitfall from memory, and know the common mitigation — engines detect highly selective filters and switch strategy (for example, falling back to brute force over the matches).

### Post 5.4 — Pre vs. post vs. filtered ANN: choose by filter selectivity

**Concept:** Choosing a filtering strategy.

**Angle:** One variable decides most of it: what fraction of the corpus passes the filter. Very selective → pre-filter (brute force on few matches). Broad → post-filter or filtered ANN (the index stays efficient). In between → filtered ANN with a fallback. Show the decision as a simple chart of selectivity vs. approach.

**Key terms covered here:**
- `Pre-filtering vs. post-filtering` *(reinforced)*
- `Metadata filtering` *(reinforced)*

**Senior-level tie-in:** for multi-tenant isolation, correctness beats speed — never rely on post-filtering to keep tenants apart (Module 9).

---

## Post 6 — Scaling the index: sharding & replication *(mini-series · 2 parts)*

**Concept:** Sharding, replication, and scaling indexes.

**Angle:** One node eventually runs out of RAM or throughput. Two orthogonal moves fix different problems: **sharding** splits one index across nodes so a bigger-than-memory corpus fits and queries fan out in parallel; **replication** copies the index so you can serve more concurrent queries and survive node failure. Clarify that they solve *different* bottlenecks.

**Series structure:** one post per move, each anchored to the bottleneck it fixes.

**Senior-level tie-in (series):** diagnose correctly — "index too big / queries too slow → shard; too many concurrent queries / need HA → replicate." Conflating them wastes money.

### Post 6.1 — Sharding: when the index no longer fits on one node

**Concept:** Index sharding.

**Angle:** Split the vectors across several nodes; each node searches its own slice and the results are merged into one top-k. A corpus bigger than one machine's memory now fits, and each query runs in parallel across shards.

**Key terms covered here:**
- `Index sharding` *(primary)* — partitioning vectors across nodes (by hash or segment); each shard searches its slice, results are merged. Solves size + parallelism.

**Senior-level tie-in:** every query now fans out to all shards, so the slowest shard sets your latency, and the merge step adds work — shard for size, not for more queries per second.

### Post 6.2 — Replication: when one copy can't serve the traffic

**Concept:** Index replication.

**Angle:** Keep several full copies of each shard. Reads are spread across copies, so you serve more concurrent queries, and if one node dies the others keep answering.

**Key terms covered here:**
- `Replication factor` *(primary)* — how many copies of each shard exist; raises read throughput and availability at a storage/consistency cost.

**Senior-level tie-in:** every copy multiplies storage cost, and writes must reach all copies — replicas can briefly serve slightly stale results. Replicate for throughput and availability, not for size.

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
| `Recall@k` | Post 1 | Posts 2.6, 3 |
| `HNSW (Hierarchical Navigable Small World)` | Post 2.1 | Posts 2.6, 3, 5.3 |
| `IVF (Inverted File Index)` | Post 2.2 | Posts 2.3, 2.6 |
| `Product Quantization (PQ)` | Post 2.3 | Posts 2.5, 2.6 |
| `LSH (Locality-Sensitive Hashing)` | Post 2.4 | Post 2.6 |
| `ScaNN` | Post 2.5 | Post 2.6 |
| `ef_construction` / `ef_search` | Post 3 | — |
| `M (graph connectivity parameter)` | Post 3 | — |
| `Vector database` | Post 4 | Post 7 |
| `Metadata filtering` | Post 5.1 | Posts 5.2–5.4, 7 |
| `Pre-filtering vs. post-filtering` | Post 5.1 | Posts 5.2, 5.4 |
| `Index sharding` | Post 6.1 | — |
| `Replication factor` | Post 6.2 | — |

✅ All 15 Module 4 key terms covered across the 16 posts.
