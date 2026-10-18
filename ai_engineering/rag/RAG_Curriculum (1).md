# RAG Mastery Curriculum
### A structured, terminology-complete learning path — foundations to production/agentic RAG

Each module lists: **concepts to understand**, **key terms you must be able to define on the spot**, and **what "senior-level" understanding looks like** for that module. Work top to bottom — later modules assume earlier ones.

---

## Module 0 — Prerequisites & Mental Model

**Concepts**
- What problem RAG solves (parametric knowledge limits, hallucination, staleness, cost of fine-tuning)
- The two-path architecture: ingestion pipeline vs. query pipeline
- RAG vs. long-context vs. fine-tuning vs. knowledge graphs — decision criteria

**Key terms**
`Parametric knowledge` · `Non-parametric/external knowledge` · `Grounding` · `Hallucination` · `Context window` · `In-context learning` · `Retrieval-Augmented Generation (RAG)` · `Closed-book vs. open-book QA`

**Senior-level bar:** can argue *against* using RAG when it's the wrong tool, with specifics.

---

## Module 1 — Document Ingestion & Parsing

**Concepts**
- Source connectors (file systems, wikis, DBs, APIs, crawlers)
- Parsing heterogeneous formats: PDF (text vs. scanned/OCR), HTML, DOCX, code, tables, images
- Layout-aware parsing vs. naive text extraction
- Handling multi-modal content (images, charts, tables embedded in documents)
- Document versioning and change detection at the source

**Key terms**
`OCR (Optical Character Recognition)` · `Layout parsing` · `Document AI / structure extraction` · `Table serialization` · `Multi-modal RAG` · `Change data capture (CDC)` · `Incremental ingestion` · `ETL/ELT for unstructured data`

**Senior-level bar:** can explain why a PDF parser choice changes downstream retrieval quality (e.g., losing table structure = losing answerability).

---

## Module 2 — Chunking Strategies

**Concepts**
- Fixed-size chunking with overlap
- Recursive/structure-aware splitting
- Semantic chunking (embedding-based boundary detection)
- Hierarchical / parent-child chunking (small-to-big retrieval)
- Document-type-specific chunking (code, tables, legal clauses, conversation transcripts)
- Contextual chunk augmentation (prepending summaries/context to chunks before embedding)
- Chunk size/overlap tuning and its effect on embedding quality

**Key terms**
`Chunk` · `Chunk overlap` · `Sliding window` · `Semantic chunking` · `Recursive character/token splitting` · `Parent-document retriever` · `Small-to-big retrieval` · `Contextual Retrieval` (Anthropic technique) · `Chunk boundary problem` · `Token-based vs. character-based splitting` · `Sentence-window retrieval`

**Senior-level bar:** can pick and justify a chunking strategy per document type, and name at least two mitigations for the boundary-split problem.

---

## Module 3 — Embeddings

**Concepts**
- What an embedding model actually does (dense vector compression of meaning)
- Bi-encoder architecture
- Symmetric vs. asymmetric embedding models (query/passage prefixing)
- Embedding model selection and benchmarking (MTEB, domain-specific eval)
- Domain adaptation / fine-tuning embeddings
- Dimensionality tradeoffs and truncation (Matryoshka embeddings)
- Multi-modal / cross-modal embeddings (text-to-image, CLIP-style)
- Embedding drift and re-indexing on model upgrade

**Key terms**
`Bi-encoder` · `Dense vector` · `Cosine similarity` · `Dot product similarity` · `Euclidean/L2 distance` · `Embedding space` · `MTEB (Massive Text Embedding Benchmark)` · `Asymmetric search (query vs. passage encoding)` · `Matryoshka Representation Learning (MRL)` · `Fine-tuned embeddings / contrastive learning` · `Triplet loss` · `Embedding drift` · `Re-embedding / re-indexing migration`

**Senior-level bar:** can explain why symmetric embedding models underperform on query-to-document search, and describe a safe embedding-model migration plan.

---

## Module 4 — Indexing & Vector Search

**Concepts**
- Exact (brute-force) vs. approximate nearest neighbor (ANN) search
- Core ANN algorithms: HNSW, IVF, IVF-PQ, LSH, ScaNN
- Index build-time vs. query-time tuning knobs
- Vector database landscape and selection criteria
- Filtering strategies (pre-filter, post-filter, filtered ANN)
- Sharding, replication, and scaling indexes
- Hybrid storage (vector + metadata + full-text in one system vs. separate systems)

**Key terms**
`Approximate Nearest Neighbor (ANN)` · `k-Nearest Neighbor (kNN)` · `HNSW (Hierarchical Navigable Small World)` · `ef_construction` / `ef_search` · `M (graph connectivity parameter)` · `IVF (Inverted File Index)` · `Product Quantization (PQ)` · `LSH (Locality-Sensitive Hashing)` · `ScaNN` · `Recall@k` (as an index quality metric, distinct from retrieval eval) · `Vector database` (Pinecone, Weaviate, Qdrant, Milvus, pgvector, Chroma) · `Metadata filtering` · `Pre-filtering vs. post-filtering` · `Index sharding` · `Replication factor`

**Senior-level bar:** can explain the `ef_search` recall/latency tradeoff and the filtered-HNSW pitfall from memory.

---

## Module 5 — Retrieval Strategies

**Concepts**
- Dense (semantic) retrieval
- Sparse (lexical/keyword) retrieval
- Hybrid retrieval and fusion methods
- Query understanding and transformation before retrieval
- Multi-vector retrieval (e.g., late-interaction models)
- Diversity-aware retrieval (avoiding redundant top-k)

**Key terms**
`Dense retrieval` · `Sparse retrieval` · `BM25` · `TF-IDF` · `Hybrid search` · `Reciprocal Rank Fusion (RRF)` · `Score normalization` · `Query expansion` · `Query rewriting` · `HyDE (Hypothetical Document Embeddings)` · `Multi-query retrieval` · `Step-back prompting` · `ColBERT / late interaction` · `Maximal Marginal Relevance (MMR)` · `Diversity-aware reranking`

**Senior-level bar:** can explain *why* RRF (not score averaging) is used to fuse dense + sparse rankings, and knows when hybrid search matters most (exact-match-heavy domains) vs. least.

---

## Module 6 — Reranking

**Concepts**
- Two-stage retrieval pattern (broad recall → precise rerank)
- Cross-encoder architecture and why it outperforms bi-encoders for ranking
- Reranking model options (open-source vs. API-based)
- Cost/latency tradeoffs of reranking
- LLM-based reranking (using a generative model itself as a judge/reranker)

**Key terms**
`Cross-encoder` · `Two-stage retrieval` · `Reranker` (Cohere Rerank, BGE-reranker, Jina Reranker) · `Listwise vs. pointwise vs. pairwise ranking` · `LLM-as-reranker` · `Candidate set / top-k retrieval before rerank`

**Senior-level bar:** can justify when reranking is worth the added latency and when it isn't (hard-SLA scenarios).

---

## Module 7 — Context Construction & Generation

**Concepts**
- Context window budgeting across system prompt, retrieved chunks, history, query
- Chunk ordering strategies (relevance-to-position mapping)
- Prompt templates for grounded generation
- Citation/attribution enforcement
- Abstention and refusal design ("I don't know" paths)
- Handling conflicting information across retrieved chunks

**Key terms**
`Lost-in-the-middle` · `Context window budget` · `Grounded generation` · `Citation enforcement` · `Attribution` · `Abstention` · `Confidence thresholding` · `Prompt template / system prompt design` · `Conflicting evidence resolution`

**Senior-level bar:** can describe a concrete abstention mechanism (not "the model would probably know not to answer").

---

## Module 8 — Evaluation

**Concepts**
- Retrieval-only metrics vs. end-to-end generation metrics
- Building a labeled evaluation/golden dataset
- Synthetic eval-set generation and its biases
- LLM-as-judge evaluation and its failure modes
- Regression testing pipelines for RAG changes
- Online vs. offline evaluation signals
- Query-type segmentation in evaluation

**Key terms**
`Recall@k` · `Precision@k` · `MRR (Mean Reciprocal Rank)` · `nDCG (normalized Discounted Cumulative Gain)` · `Faithfulness` · `Answer relevance` · `Context precision` · `Context recall` · `RAGAS` · `Golden dataset` · `LLM-as-judge` · `Synthetic Q&A generation` · `Regression testing` · `Online metrics` (CTR on citations, thumbs up/down, escalation rate) · `Offline metrics` · `Human-in-the-loop evaluation`

**Senior-level bar:** knows the difference between faithfulness and answer relevance, and can describe how to build a golden dataset from scratch.

---

## Module 9 — Production Engineering

**Concepts**
- Latency budget decomposition across the pipeline
- Caching strategies (embedding cache, semantic query cache)
- Incremental indexing, upserts, deletes, and document versioning at index level
- Cost modeling (embedding, storage, retrieval, generation)
- Observability and logging for retrieval debugging
- Multi-tenancy and access control enforcement point
- Failure modes: duplicate/near-duplicate crowding, stale document ranking, empty retrieval

**Key terms**
`Latency budget` · `Semantic caching` · `Embedding cache` · `Upsert` · `Index versioning` · `Cost per query` · `Observability / retrieval tracing` · `Multi-tenancy` · `Access control at retrieval time` · `Row-level security` · `Deduplication` · `Near-duplicate detection` · `Recency boosting` · `Empty-retrieval fallback`

**Senior-level bar:** has a concrete story for at least 3 production failure modes and their fixes.

---

## Module 10 — Agentic & Advanced RAG

**Concepts**
- Retrieval as an agent tool call (dynamic retrieval decisions)
- Multi-hop / iterative retrieval for chained reasoning
- Self-critique and corrective retrieval loops
- Adaptive retrieval (deciding retrieval is unnecessary for a given query)
- Tool-augmented RAG (retrieval combined with calculators, APIs, code execution)
- Multi-agent RAG architectures (specialized retriever agents, verifier agents)
- Post-generation grounding verification loops

**Key terms**
`Agentic RAG` · `Self-RAG` · `Corrective RAG (CRAG)` · `Multi-hop retrieval` · `Iterative retrieval` · `Adaptive retrieval` · `Tool-use / function calling` · `Verifier/critic agent` · `Grounding verification loop` · `Retrieval-augmented reasoning` · `ReAct (Reason+Act) pattern` · `Plan-and-execute agents` · `Query decomposition`

**Senior-level bar:** can sketch the full loop (retrieve → reason → identify gap → retrieve again → synthesize) and explain why naive single-pass RAG structurally fails on multi-hop questions.

---

## Module 11 — Knowledge Graphs & Structured Retrieval (adjacent but frequently tested)

**Concepts**
- GraphRAG (combining knowledge graphs with vector retrieval)
- Entity extraction and relationship modeling
- Text-to-SQL as an alternative/complement to vector RAG
- Hybrid graph + vector retrieval architectures

**Key terms**
`GraphRAG` · `Knowledge graph` · `Entity extraction` · `Relation extraction` · `Text-to-SQL` · `Structured retrieval` · `Ontology`

**Senior-level bar:** knows when relational/multi-hop factual queries need a graph instead of (or alongside) vector search.

---

## Module 12 — System Design Practice

**Concepts**
- Requirements clarification framework for RAG system design questions
- End-to-end architecture sketching under time pressure
- Explicitly naming failure modes you're designing around
- Scaling considerations (10K → 10M docs)
- Build-vs-buy decisions (managed vector DB vs. self-hosted)

**Key terms**
*(Integrative module — no new terms; this is where every term above gets used together.)*

**Senior-level bar:** can complete a full system design answer in ~8–10 minutes with the structure: requirements → ingestion → retrieval path → guardrails → eval/observability → scaling/cost → named failure modes.

---

## Full Glossary (Quick-Reference — Alphabetical)

Use this as a self-test: cover the right column, see if you can define each term in one sentence.

| Term | One-line definition to nail |
|---|---|
| Abstention | Model declines to answer when retrieval confidence is too low |
| Adaptive retrieval | System decides whether retrieval is needed at all for a given query |
| ANN | Approximate Nearest Neighbor search — sub-linear vector search trading exact recall for speed |
| Asymmetric embedding | Query and document encoded with different objectives/prefixes for better search alignment |
| BM25 | Classic sparse/lexical ranking function based on term frequency and document length |
| Bi-encoder | Encodes query and document independently into vectors, enabling fast ANN search |
| Chunk | A segment of a document sized for embedding and retrieval |
| Contextual Retrieval | Prepending doc/section-level context to a chunk before embedding to preserve meaning |
| Corrective RAG (CRAG) | Agent critiques retrieved context and triggers fallback retrieval if insufficient |
| Cross-encoder | Jointly encodes query+document pair for high-accuracy relevance scoring; used in reranking |
| Embedding drift | Old and new embedding model outputs are not comparable in the same vector space |
| Faithfulness | Whether generated claims are supported by retrieved context (vs. hallucinated) |
| GraphRAG | RAG architecture that retrieves from a knowledge graph in addition to/instead of vectors |
| HNSW | Graph-based ANN algorithm; dominant production vector index structure |
| Hybrid search | Combining dense and sparse retrieval, fused via a method like RRF |
| HyDE | Generate a hypothetical answer, embed that instead of the raw query, then retrieve |
| Lost-in-the-middle | LLMs attend less reliably to information placed in the middle of long context |
| MMR | Maximal Marginal Relevance — reranking for diversity, avoiding redundant top-k results |
| MRR | Mean Reciprocal Rank — how high the first relevant result ranks, averaged over queries |
| MTEB | Standard benchmark suite for comparing embedding models |
| Multi-hop retrieval | Chained retrieval where an intermediate fact drives a follow-up retrieval |
| nDCG | Ranking quality metric accounting for graded relevance and position discounting |
| Parent-document retriever | Retrieve small precise chunks, return larger parent chunk for context completeness |
| Query expansion | Generating multiple rephrasings of a query to improve retrieval recall |
| RAGAS | Popular framework/library for automated RAG evaluation metrics |
| Reciprocal Rank Fusion (RRF) | Method for fusing ranked lists from multiple retrievers without score normalization |
| Self-RAG | Model reflects on and critiques its own retrieval and generation during inference |
| Semantic caching | Caching query results keyed by embedding similarity, not exact string match |
| Step-back prompting | Retrieve for the broader underlying concept before answering a specific question |

---

## Suggested Study Order & Pacing

1. **Days 1–2:** Modules 0–2 (foundations, ingestion, chunking) — get the "why" solid before mechanics.
2. **Days 3–4:** Modules 3–4 (embeddings, indexing/vector search) — the most technically dense modules; expect these to take longest.
3. **Day 5:** Modules 5–6 (retrieval strategies, reranking).
4. **Day 6:** Module 7 (context/generation) + Module 8 (evaluation).
5. **Day 7:** Module 9 (production) + Module 11 (knowledge graphs, lighter pass).
6. **Day 8:** Module 10 (agentic RAG) — your strength, but make sure terminology is precise, not just conceptual.
7. **Day 9–10:** Module 12 — run full system design mocks daily, drill the glossary until every term is a one-sentence reflex.

---

Want me to turn any single module into a deep drill session (rapid-fire Q&A on just that module), or build a mock system design prompt to run through right now?
