# Pillar 2 — Content Calendar: Module 11 (Knowledge Graphs & Structured Retrieval)

**Source:** `RAG_Curriculum (1).md` → Module 11
**Rule:** 1 concept = 1 post. Every Module 11 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 11 has 4 concepts → 4 posts.**
**Key terms to cover (7):** `GraphRAG` · `Knowledge graph` · `Entity extraction` · `Relation extraction` · `Text-to-SQL` · `Structured retrieval` · `Ontology`

---

## Post 1 — When "similar" isn't enough: GraphRAG

**Concept:** GraphRAG (combining knowledge graphs with vector retrieval).

**Angle:** Vector search is brilliant at finding *similar* text but blind to *connections*. Ask "What do all the companies founded by ex-employees of X have in common?" and similarity search flails — the answer lives in relationships, not in any single passage. A knowledge graph stores facts as entities and the links between them, so you can traverse connections. GraphRAG combines the two: vectors to find entry points, graph traversal to follow the relationships.

**Key terms covered here:**
- `Knowledge graph` *(primary)* — a structured store of entities (nodes) and the typed relationships between them (edges); facts as a traversable network, not free text.
- `GraphRAG` *(primary)* — RAG that retrieves over a knowledge graph (often seeded by vector search), traversing relationships and aggregating connected facts rather than returning isolated chunks.

**Senior-level tie-in:** the module bar, part one — name the query shape that breaks pure vector RAG: relational and multi-hop factual questions ("how is A connected to C?") where the answer is a *path*, not a passage.

---

## Post 2 — Turning text into nodes and edges: entity & relationship extraction

**Concept:** Entity extraction and relationship modeling.

**Angle:** A knowledge graph isn't free — you have to *build* it from unstructured text. Two extraction steps do the heavy lifting: pull out the entities (people, companies, drugs, parts), then identify how they relate (founded, treats, supplies). An ontology defines the allowed types and relationships up front, so the graph stays consistent instead of becoming a tangle of synonyms and one-off edges.

**Key terms covered here:**
- `Entity extraction` *(primary)* — identifying and normalizing the real-world entities (nodes) mentioned in text, often with coreference resolution so "the company" and its name map to one node.
- `Relation extraction` *(primary)* — detecting the typed relationships (edges) between extracted entities, e.g. (Person)-[FOUNDED]->(Company).
- `Ontology` *(primary)* — the schema defining which entity types and relationship types are allowed; the blueprint that keeps the graph coherent and queryable.

**Senior-level tie-in:** graph quality is capped by extraction quality — a loose or missing ontology yields duplicate nodes and inconsistent edges that make traversal unreliable; design the schema before you extract at scale.

---

## Post 3 — When the answer is a row, not a paragraph: Text-to-SQL

**Concept:** Text-to-SQL as an alternative/complement to vector RAG.

**Angle:** A huge class of questions — "What was our average order value in Q3 by region?" — has an exact answer sitting in a database, and embedding table rows to retrieve them is the wrong tool entirely. Text-to-SQL translates the natural-language question into a precise query the database executes, returning exact, aggregatable, always-current answers. It's structured retrieval: query the data, don't fuzzy-match it.

**Key terms covered here:**
- `Text-to-SQL` *(primary)* — using an LLM to translate a natural-language question into a SQL query against a known schema, then running it for an exact answer.
- `Structured retrieval` *(primary)* — retrieving from structured sources (databases, tables, APIs) via precise queries rather than semantic similarity over text.

**Senior-level tie-in:** know the failure modes — Text-to-SQL is only as good as schema grounding; it needs the schema, sample values, and guardrails against invalid/expensive queries, and it shines exactly where vector RAG is weakest (aggregations, exact filters, numeric facts).

---

## Post 4 — Pick the right tool per query: hybrid graph + vector architectures

**Concept:** Hybrid graph + vector retrieval architectures.

**Angle:** Real systems rarely pick one retriever — they route or blend. Semantic recall over documents (vectors), relational/multi-hop facts (graph), exact aggregates (SQL): different question types want different backends. The architecture either *routes* each query to the right retriever or *blends* their results, so you get fuzzy semantic coverage and precise structured answers from one system.

**Key terms covered here:**
- `GraphRAG` *(reinforced)* — the graph retriever in the hybrid, handling relational/multi-hop queries.
- `Knowledge graph` *(reinforced)* — the structured backend traversed for connected facts.
- `Structured retrieval` *(reinforced)* — the database/SQL path in the blend, for exact and aggregate answers.

**Senior-level tie-in:** the module bar, part two — the senior move is a *router*: classify the query (semantic lookup vs. relational vs. aggregation) and dispatch to vector, graph, or SQL — graph *alongside* vectors, not instead of, chosen by query shape.

---

## Coverage check (all 7 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `GraphRAG` | Post 1 | Post 4 |
| `Knowledge graph` | Post 1 | Post 4 |
| `Entity extraction` | Post 2 | — |
| `Relation extraction` | Post 2 | — |
| `Ontology` | Post 2 | — |
| `Text-to-SQL` | Post 3 | — |
| `Structured retrieval` | Post 3 | Post 4 |

✅ All 7 Module 11 key terms covered across the 4 posts.
