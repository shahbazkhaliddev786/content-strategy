# Pillar 2 — Content Calendar: Module 0 (Prerequisites & Mental Model)

**Source:** `RAG_Curriculum (1).md` → Module 0
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 0 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 0 has 3 concepts → 5 posts (1 mini-series).**
**Key terms to cover (8):** `Parametric knowledge` · `Non-parametric/external knowledge` · `Grounding` · `Hallucination` · `Context window` · `In-context learning` · `Retrieval-Augmented Generation (RAG)` · `Closed-book vs. open-book QA`

---

## Post 1 — What problem does RAG actually solve?

**Concept:** What problem RAG solves — parametric knowledge limits, hallucination, staleness, and the cost of fine-tuning.

**Angle:** Why we needed RAG at all. An LLM only "knows" what's baked into its weights — frozen at training time, impossible to audit, and expensive to update. Frame RAG as the shift from making the model *memorize* to letting it *look things up*.

**Key terms covered here:**
- `Parametric knowledge` *(primary)* — knowledge stored in the model's weights.
- `Non-parametric/external knowledge` *(primary)* — knowledge kept outside the model, in a retrievable store.
- `Hallucination` *(primary)* — confident, ungrounded output; the core failure RAG attacks.
- `Grounding` *(primary)* — tying generated answers to retrieved source evidence.
- `Retrieval-Augmented Generation (RAG)` *(primary)* — the pattern itself, defined here first.
- `Closed-book vs. open-book QA` *(primary)* — the mental model: memory-only vs. answer-with-sources.

**Senior-level tie-in:** set up the ability to argue *against* RAG — plant the seed that it's one tool, not the default.

---

## Post 2 — The two pipelines: how a RAG system is actually wired

**Concept:** The two-path architecture — ingestion pipeline vs. query pipeline.

**Angle:** Most people picture RAG as one flow; it's really two. The **ingestion pipeline** (offline: load → chunk → embed → index) and the **query pipeline** (online: embed query → retrieve → stuff context → generate). Show that retrieved evidence enters the model at inference time, not training time.

**Key terms covered here:**
- `Retrieval-Augmented Generation (RAG)` *(reinforced)* — now shown as a wiring diagram, not a definition.
- `Non-parametric/external knowledge` *(reinforced)* — this is what the ingestion pipeline builds and the query pipeline reads.
- `Context window` *(primary)* — the finite space retrieved chunks are injected into.
- `In-context learning` *(primary)* — how the model uses retrieved context at inference without weight updates.
- `Grounding` *(reinforced)* — shown mechanically: retrieval is what makes grounding possible.

**Senior-level tie-in:** emphasize that retrieval quality upstream caps answer quality downstream — the whole curriculum hangs off this.

---

## Post 3 — RAG vs. long-context vs. fine-tuning vs. knowledge graphs *(mini-series · 3 parts)*

**Concept:** Decision criteria — when RAG is right, and when it isn't.

**Angle:** The honest comparison. Long-context = just paste it in the `Context window`. Fine-tuning = rewrite `Parametric knowledge`. Knowledge graphs = structured relationships. RAG = retrieve external knowledge on demand. Give a decision rubric (freshness, scale, auditability, cost, structure).

**Series structure:** each alternative to RAG gets its own post (full Problem → Intuition → How it works → Trade-offs → When to use → When NOT to use), then a decision-guide post ties them together. Knowledge graphs get their own deep dive in Module 11, so here they appear inside the decision guide.

**Senior-level tie-in (series):** deliver the module's bar — can argue *against* RAG with specifics (e.g., small/stable corpus → long-context; need reasoning over relationships → knowledge graph).

### Post 3.1 — Long-context: just paste it all in

**Concept:** Long-context prompting as an alternative to retrieval.

**Angle:** If the whole corpus fits in the `Context window`, skip retrieval entirely and paste it in — the model reads everything via in-context learning. No chunking, no index, no retrieval misses. The catch: every query pays for every token, latency grows with context size, and models attend unevenly across very long inputs.

**Key terms covered here:**
- `Context window` *(reinforced)* — the long-context alternative; its size/cost limits.
- `In-context learning` *(reinforced)* — the mechanism RAG and long-context share.

**Senior-level tie-in:** small, stable corpus that fits comfortably in the window → long-context often beats RAG on simplicity; large or fast-growing corpus → per-query token cost makes it a non-starter.

### Post 3.2 — Fine-tuning: rewrite the model's memory

**Concept:** Fine-tuning as an alternative to retrieval.

**Angle:** Fine-tuning changes `Parametric knowledge` itself — you train the weights on your data. It's strong for teaching style, format, or behavior, but a poor way to inject facts: updating requires another training run, you can't easily audit or cite where an answer came from, and the model can still hallucinate confidently.

**Key terms covered here:**
- `Parametric knowledge` *(reinforced)* — what fine-tuning changes, and why that's costly/opaque.
- `Hallucination` *(reinforced)* — fine-tuning doesn't remove it; there are still no sources to ground against.

**Senior-level tie-in:** fine-tune for *skills and behavior*, retrieve for *knowledge* — and know that many production systems do both.

### Post 3.3 — The decision guide: RAG vs. long-context vs. fine-tuning vs. knowledge graphs

**Concept:** A decision rubric across all four approaches.

**Angle:** Put the options side by side on freshness, scale, auditability, cost, and structure. Long-context = paste it in. Fine-tuning = rewrite memory (closed-book). Knowledge graphs = structured relationships. RAG = look it up on demand (open-book). Show which question points to which tool.

**Key terms covered here:**
- `Closed-book vs. open-book QA` *(reinforced)* — maps cleanly onto fine-tune (closed) vs. RAG (open).
- `Hallucination` *(reinforced)* — compare how each approach does/doesn't reduce it.
- `Context window` *(reinforced)* — the constraint that decides when long-context is viable.
- `Parametric knowledge` *(reinforced)* — the thing fine-tuning changes and RAG leaves alone.

**Senior-level tie-in:** production systems often combine approaches — fine-tune for format and behavior, RAG for facts, long-context for a few always-needed documents. The skill is naming which problem each one solves, not crowning a single winner.

---

## Coverage check (all 8 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Parametric knowledge` | Post 1 | Posts 3.2, 3.3 |
| `Non-parametric/external knowledge` | Post 1 | Post 2 |
| `Grounding` | Post 1 | Post 2 |
| `Hallucination` | Post 1 | Posts 3.2, 3.3 |
| `Retrieval-Augmented Generation (RAG)` | Post 1 | Post 2 |
| `Closed-book vs. open-book QA` | Post 1 | Post 3.3 |
| `Context window` | Post 2 | Posts 3.1, 3.3 |
| `In-context learning` | Post 2 | Post 3.1 |

✅ All 8 Module 0 key terms covered across the 5 posts.
