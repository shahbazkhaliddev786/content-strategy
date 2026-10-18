# Pillar 2 — Content Calendar: Module 9 (Production Engineering)

**Source:** `RAG_Curriculum (1).md` → Module 9
**Rule:** 1 concept = 1 post. Every Module 9 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 9 has 7 concepts → 7 posts.**
**Key terms to cover (14):** `Latency budget` · `Semantic caching` · `Embedding cache` · `Upsert` · `Index versioning` · `Cost per query` · `Observability / retrieval tracing` · `Multi-tenancy` · `Access control at retrieval time` · `Row-level security` · `Deduplication` · `Near-duplicate detection` · `Recency boosting` · `Empty-retrieval fallback`

---

## Post 1 — Where the milliseconds go: decomposing the latency budget

**Concept:** Latency budget decomposition across the pipeline.

**Angle:** A RAG response that takes 6 seconds feels broken, but "it's slow" isn't actionable. Every stage — embed the query, vector search, rerank, generate — spends part of a fixed, user-facing time budget. Decompose it, measure each stage, and you find the real bottleneck (usually generation or an over-deep rerank), instead of optimizing the part that was already fast.

**Key terms covered here:**
- `Latency budget` *(primary)* — the total end-to-end time target for a response, explicitly allocated across pipeline stages (embed → retrieve → rerank → generate) so each has a measurable ceiling.

**Senior-level tie-in:** budget top-down from the UX requirement (e.g. "P95 under 2s"), then attribute measured time per stage — you can't fix a bottleneck you haven't isolated.

---

## Post 2 — Don't recompute what you've already seen: caching

**Concept:** Caching strategies (embedding cache, semantic query cache).

**Angle:** Two expensive things repeat constantly in production: embedding the same text, and answering the same (or nearly the same) question. Caching attacks both. An embedding cache skips re-encoding identical content; a semantic query cache returns a stored answer when a *new* query is close enough in meaning to a past one — cutting both latency and cost dramatically on repetitive traffic.

**Key terms covered here:**
- `Embedding cache` *(primary)* — store and reuse embeddings for already-seen text (keyed by content hash) instead of re-encoding.
- `Semantic caching` *(primary)* — serve a cached response when an incoming query is semantically similar (above a threshold) to a previously answered one, not just byte-identical.
- `Latency budget` *(reinforced)* — caching is the cheapest way to claw back time from the budget in Post 1.

**Senior-level tie-in:** know the risk of semantic caching — too loose a similarity threshold returns a stale/wrong cached answer; tune it against your eval set and expire entries when the index changes.

---

## Post 3 — Keeping the index alive: upserts, deletes & versioning

**Concept:** Incremental indexing, upserts, deletes, and document versioning at the index level.

**Angle:** Real corpora change every day — docs get edited, added, deleted. Rebuilding the whole index each time is wasteful and causes downtime. Production systems update in place (upsert changed docs, remove deleted ones) and version the index so you can roll forward or back safely. This is the operational cousin of Module 1's change-detection, applied at the index.

**Key terms covered here:**
- `Upsert` *(primary)* — insert-or-update in one operation: add a new chunk's vector, or overwrite an existing one when its source document changes.
- `Index versioning` *(primary)* — tracking index state as discrete versions so you can validate, roll back, or cut over (ties to Module 3's re-index migration).

**Senior-level tie-in:** handle deletes and updates explicitly — an orphaned vector for a deleted doc keeps getting retrieved, serving content that no longer exists; upsert-and-tombstone, don't just add.

---

## Post 4 — Know your cost per query before scale punishes you

**Concept:** Cost modeling (embedding, storage, retrieval, generation).

**Angle:** RAG costs hide in four buckets — embedding (ingest + per-query), vector storage, retrieval compute, and generation tokens. At 100 queries/day nobody notices; at 100k/day it's the whole budget. Model cost per query up front, identify the dominant term (usually generation), and you can make informed trade-offs instead of getting a surprise bill.

**Key terms covered here:**
- `Cost per query` *(primary)* — the fully-loaded marginal cost of answering one query, summed across embedding, retrieval, rerank, and generation; the unit economics that decide whether the system scales profitably.
- `Embedding cache` *(reinforced)* — a direct cost lever: cache hits remove embedding (and often generation) spend from the per-query total.

**Senior-level tie-in:** attribute cost per stage like you did latency — generation tokens usually dominate, so context-size discipline (Module 7) and caching (Post 2) are the biggest cost levers, not the vector DB bill.

---

## Post 5 — You can't debug what you can't see: retrieval observability

**Concept:** Observability and logging for retrieval debugging.

**Angle:** When a RAG answer is wrong, the question is *where* it broke — bad retrieval, bad ranking, or bad generation from good context? Without tracing you're guessing. Log the query, its transformations, the retrieved chunks with scores, what survived reranking, and the final prompt — so any bad answer can be replayed and diagnosed to the exact stage.

**Key terms covered here:**
- `Observability / retrieval tracing` *(primary)* — end-to-end capture of each request's pipeline (query → transformed query → retrieved chunks + scores → reranked set → final prompt → answer) so failures are inspectable and reproducible.

**Senior-level tie-in:** the first debugging question is always "what was actually retrieved?" — if your logs can't answer that per request, you can't tell a retrieval failure from a generation failure, and you'll fix the wrong stage.

---

## Post 6 — One index, many customers: multi-tenancy & access control

**Concept:** Multi-tenancy and access-control enforcement point.

**Angle:** Serve multiple customers (or user roles) from shared infrastructure and you inherit a hard rule: tenant A must *never* retrieve tenant B's documents. The critical design decision is *where* you enforce it — filtering after retrieval is a data-leak waiting to happen. Enforcement must happen *at retrieval time*, baked into the query, ideally backed by row-level security so the datastore itself refuses cross-tenant reads.

**Key terms covered here:**
- `Multi-tenancy` *(primary)* — serving many isolated tenants/users from shared index infrastructure while guaranteeing data isolation.
- `Access control at retrieval time` *(primary)* — applying the permission filter *as part of* the retrieval query (not post-filtering results), so disallowed documents are never candidates.
- `Row-level security` *(primary)* — enforcing per-row access in the datastore itself, so even a buggy query can't return rows the caller isn't entitled to.

**Senior-level tie-in:** security must be the retrieval filter, not an afterthought — post-filtering can leak via counts, scores, or a missed code path; enforce at query time and defend-in-depth with row-level security.

---

## Post 7 — The three failures that bite in production (and their fixes)

**Concept:** Failure modes — duplicate/near-duplicate crowding, stale document ranking, empty retrieval.

**Angle:** Every production RAG system hits the same three failures. **Duplicate crowding:** the same content (or near-copies) fills the top-k, wasting context on redundancy. **Stale ranking:** an outdated-but-similar doc outranks the current one. **Empty retrieval:** nothing relevant comes back and the model hallucinates to fill the void. Each has a concrete, known fix — show the failure and the fix side by side.

**Key terms covered here:**
- `Deduplication` *(primary)* — removing exact-duplicate chunks at ingest/retrieval so identical content can't occupy multiple top-k slots.
- `Near-duplicate detection` *(primary)* — catching *near*-copies (same content, minor edits/boilerplate) via similarity thresholds, since exact dedup misses them.
- `Recency boosting` *(primary)* — fix for stale ranking: blend a freshness signal (document date metadata) into the score so current docs outrank outdated near-matches.
- `Empty-retrieval fallback` *(primary)* — the defined path when nothing clears the relevance bar: abstain, ask a clarifying question, or widen the search — never let the model answer from an empty context (ties to Module 7's abstention).

**Senior-level tie-in:** the module bar — carry three worked failure→fix stories: crowding → dedup/near-dup detection; stale ranking → recency boosting via date metadata; empty retrieval → explicit fallback + abstention. Naming the fix is the difference between senior and "it usually works."

---

## Coverage check (all 14 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Latency budget` | Post 1 | Post 2 |
| `Embedding cache` | Post 2 | Post 4 |
| `Semantic caching` | Post 2 | — |
| `Upsert` | Post 3 | — |
| `Index versioning` | Post 3 | — |
| `Cost per query` | Post 4 | — |
| `Observability / retrieval tracing` | Post 5 | — |
| `Multi-tenancy` | Post 6 | — |
| `Access control at retrieval time` | Post 6 | — |
| `Row-level security` | Post 6 | — |
| `Deduplication` | Post 7 | — |
| `Near-duplicate detection` | Post 7 | — |
| `Recency boosting` | Post 7 | — |
| `Empty-retrieval fallback` | Post 7 | — |

✅ All 14 Module 9 key terms covered across the 7 posts.
