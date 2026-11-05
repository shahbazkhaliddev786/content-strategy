# Cover labels and titles (format v3)

What the cover of each post shows, top to bottom. Written once, **approved by Shahbaz on 5 Nov 2026**, copied exactly by the daily run. Covers RAG #16 onward (RAG #01–#15 are already posted): 99 posts in 11 modules.

1. **Module label** (black pill): the section heading below. Same wording on every post in the module.
2. **Mini-series line** (only in a mini-series): `<name> · Part n/N`.
3. **Cover title** (big): the post's topic. ` / ` marks the line breaks; the word in [brackets] gets the yellow highlight.
4. **Hook line** (medium): written by the daily run for each post. Not in this file.

The **next-day teaser** (the last slide of each post) shows the next row's module label, mini-series line and cover title, copied exactly; the renderer fills and checks them with `--cover-labels`.

**Size:** L = 120px (max 2 lines, 11 characters each). M = 100px (max 3 lines, 13 characters each). The daily run must not post a cover whose title doesn't match this file.


## RAG chunking

Module 2: Chunking Strategies

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #16 | — | [Semantic] / chunking | L | Semantic chunking: let meaning decide the boundaries |
| RAG #17 | Small-to-big · Part 1/2 | [Parent] / document / retriever | M | Match small, return the parent: the parent-document retriever |
| RAG #18 | Small-to-big · Part 2/2 | [Sentence] / window / retrieval | M | One sentence in, a window out: sentence-window retrieval |
| RAG #19 | Chunking by doc type · Part 1/4 | Chunking / [code] | L | Chunking code: split on functions, not characters |
| RAG #20 | Chunking by doc type · Part 2/4 | Chunking / [tables] | L | Chunking tables: never separate a row from its headers |
| RAG #21 | Chunking by doc type · Part 3/4 | Chunking / [legal] docs | L | Chunking legal documents: the clause is the unit |
| RAG #22 | Chunking by doc type · Part 4/4 | Chunking / [transcripts] | L | Chunking transcripts: keep the conversation turns together |
| RAG #23 | — | [Contextual] / retrieval | L | Contextual chunk augmentation: give each chunk its bearings |
| RAG #24 | — | Tuning / [chunk] size | L | Tuning the knobs: chunk size, overlap, and embedding quality |

## RAG embeddings

Module 3: Embeddings

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #25 | Embeddings 101 · Part 1/2 | What is an / [embedding]? | L | Meaning as geometry: text becomes a point in space |
| RAG #26 | Embeddings 101 · Part 2/2 | [Cosine] vs / dot vs L2 | L | How close is close? Cosine vs. dot product vs. L2 |
| RAG #27 | — | [Bi-encoders] | L | Two encoders, one offline job: the bi-encoder |
| RAG #28 | — | [Symmetric] vs / asymmetric | M | Symmetric vs. asymmetric: a question is not a passage |
| RAG #29 | — | [Choosing] / embeddings | L | Don't trust the leaderboard: choosing & benchmarking embeddings |
| RAG #30 | — | [Fine-tuning] / embeddings | L | When general models miss your jargon: fine-tuning embeddings |
| RAG #31 | — | [Matryoshka] / embeddings | L | One embedding, many sizes: Matryoshka & dimensionality trade-offs |
| RAG #32 | — | [Cross-modal] / embeddings | L | One space for text and images: cross-modal embeddings |
| RAG #33 | — | Embedding / [drift] | L | You can't mix spaces: embedding drift & re-indexing on upgrade |

## RAG vector search

Module 4: Indexing & Vector Search

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #34 | — | Exact vs / [approximate] | L | Exact vs. approximate: why search gets "good enough" on purpose |
| RAG #35 | ANN algorithms · Part 1/6 | [HNSW] | L | HNSW: search by walking a graph |
| RAG #36 | ANN algorithms · Part 2/6 | [IVF] | L | IVF: only search the nearest buckets |
| RAG #37 | ANN algorithms · Part 3/6 | [Product] / quantization | M | Product Quantization: shrink every vector to a few bytes |
| RAG #38 | ANN algorithms · Part 4/6 | [LSH] | L | LSH: hash similar vectors into the same bucket |
| RAG #39 | ANN algorithms · Part 5/6 | [ScaNN] | L | ScaNN: quantization tuned for ranking |
| RAG #40 | ANN algorithms · Part 6/6 | Which ANN / index, [when]? | M | HNSW vs. IVF vs. PQ vs. LSH vs. ScaNN: which one, when? |
| RAG #41 | — | [Tuning] the / index | L | The knobs: build-time vs. query-time tuning |
| RAG #42 | — | Choosing a / [vector] DB | L | Choosing a vector database (it's not about raw QPS) |
| RAG #43 | Filtering · Part 1/4 | [Pre-] / filtering | L | Pre-filtering: narrow the set, then search |
| RAG #44 | Filtering · Part 2/4 | [Post-] / filtering | L | Post-filtering: search first, filter after |
| RAG #45 | Filtering · Part 3/4 | [Filtered] / ANN | L | Filtered ANN: filter during the search (and its trap) |
| RAG #46 | Filtering · Part 4/4 | Pre vs post / vs [filtered] | L | Pre vs. post vs. filtered ANN: choose by filter selectivity |
| RAG #47 | Scaling the index · Part 1/2 | [Sharding] | L | Sharding: when the index no longer fits on one node |
| RAG #48 | Scaling the index · Part 2/2 | [Replication] | L | Replication: when one copy can't serve the traffic |
| RAG #49 | — | [Hybrid] / storage | L | One system or several? The hybrid-storage question |

## RAG retrieval

Module 5: Retrieval Strategies

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #50 | — | [Dense] / retrieval | L | Retrieving by meaning: dense retrieval |
| RAG #51 | — | [Sparse] / retrieval | L | The keyword classic that refuses to die: sparse retrieval |
| RAG #52 | Hybrid fusion · Part 1/2 | [Reciprocal] / rank fusion | L | Hybrid search with Reciprocal Rank Fusion: merge by rank |
| RAG #53 | Hybrid fusion · Part 2/2 | Score / [normalization] | M | Score normalization: merge by rescaled scores |
| RAG #54 | Query transformation · Part 1/6 | Query / [expansion] | L | Query expansion: add the words the user didn't type |
| RAG #55 | Query transformation · Part 2/6 | Query / [rewriting] | L | Query rewriting: turn "what about the second one?" into a real query |
| RAG #56 | Query transformation · Part 3/6 | [HyDE] | L | HyDE: search with a fake answer |
| RAG #57 | Query transformation · Part 4/6 | [Multi-query] / retrieval | L | Multi-query retrieval: ask the question several ways |
| RAG #58 | Query transformation · Part 5/6 | [Step-back] / prompting | L | Step-back prompting: zoom out before you zoom in |
| RAG #59 | Query transformation · Part 6/6 | Which one, / [when]? | L | Which query transformation, when? |
| RAG #60 | — | Late / [interaction] | L | One vector per token: multi-vector / late interaction |
| RAG #61 | — | [MMR] for / diversity | L | Stop retrieving the same thing five times: diversity-aware retrieval |

## RAG reranking

Module 6: Reranking

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #62 | — | Retrieve, / then [rerank] | L | Cast a wide net, then be picky: the two-stage pattern |
| RAG #63 | — | [Cross-] / encoders | L | Why cross-encoders out-rank bi-encoders |
| RAG #64 | Choosing a reranker · Part 1/4 | API or / [open-source] | L | API or open-source: choosing a reranker model |
| RAG #65 | Choosing a reranker · Part 2/4 | [Pointwise] / ranking | L | Pointwise ranking: score each document on its own |
| RAG #66 | Choosing a reranker · Part 3/4 | [Pairwise] / ranking | L | Pairwise ranking: which of these two is better? |
| RAG #67 | Choosing a reranker · Part 4/4 | [Listwise] / ranking | L | Listwise ranking: order the whole list at once |
| RAG #68 | — | Reranking / [latency] | L | The latency tax: when reranking is worth it (and when it isn't) |
| RAG #69 | — | [LLM] as / reranker | L | The model as judge: LLM-as-reranker |

## RAG generation

Module 7: Context Construction & Generation

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #70 | — | Context / [budget] | L | The context window is a budget, not a bucket |
| RAG #71 | — | Lost in the / [middle] | L | Where you put a chunk changes whether the model reads it |
| RAG #72 | — | [Grounding] / prompts | L | The prompt that makes the model answer from the docs, not its memory |
| RAG #73 | — | Source / [citations] | L | Make it cite its sources (and check that it did) |
| RAG #74 | Abstention · Part 1/3 | Score / [thresholds] | L | Abstain before generating: the score threshold |
| RAG #75 | Abstention · Part 2/3 | [Refusal] / instruction | L | Abstain while generating: the refusal instruction |
| RAG #76 | Abstention · Part 3/3 | [Grounding] / checks | L | Abstain after generating: the grounding-check veto |
| RAG #77 | Conflicting evidence · Part 1/3 | [Recency] & / authority | L | Let metadata decide: recency and authority precedence |
| RAG #78 | Conflicting evidence · Part 2/3 | [Surfacing] / conflicts | L | Say it out loud: surfacing the conflict |
| RAG #79 | Conflicting evidence · Part 3/3 | Showing / [both] sides | L | Show both sides: present both with attribution |

## RAG evaluation

Module 8: Evaluation

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #80 | — | [Retrieval] vs / generation | M | Two layers you must measure separately: retrieval vs. generation metrics |
| RAG #81 | — | [Golden] / datasets | L | The thing you can't skip: building a golden dataset from scratch |
| RAG #82 | — | [Synthetic] / eval sets | L | Faster but biased: synthetic eval-set generation |
| RAG #83 | — | [LLM-as-judge] / & RAGAS | M | Scoring quality at scale: LLM-as-judge & the RAGAS metrics |
| RAG #84 | — | [Regression] / testing | L | Stop shipping silent regressions: regression testing for RAG |
| RAG #85 | — | [Online] vs / offline | L | Lab vs. reality: online vs. offline evaluation signals |
| RAG #86 | — | [Query-type] / segmentation | M | The average is lying to you: query-type segmentation |

## RAG in production

Module 9: Production Engineering

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #87 | — | Latency / [budget] | L | Where the milliseconds go: decomposing the latency budget |
| RAG #88 | Caching · Part 1/2 | [Embedding] / cache | L | Embedding cache: never embed the same text twice |
| RAG #89 | Caching · Part 2/2 | [Semantic] / cache | L | Semantic cache: reuse answers for questions that mean the same thing |
| RAG #90 | — | Index / [updates] | L | Keeping the index alive: upserts, deletes & versioning |
| RAG #91 | — | [Cost] per / query | L | Know your cost per query before scale punishes you |
| RAG #92 | — | Retrieval / [observability] | M | You can't debug what you can't see: retrieval observability |
| RAG #93 | — | [Multi-] / tenancy | L | One index, many customers: multi-tenancy & access control |
| RAG #94 | Production failures · Part 1/3 | [Deduplication] | M | Five copies of the same chunk: deduplication & near-duplicate detection |
| RAG #95 | Production failures · Part 2/3 | [Recency] / boosting | L | The outdated doc wins: recency boosting |
| RAG #96 | Production failures · Part 3/3 | [Empty] / retrieval | L | Nothing relevant came back: the empty-retrieval fallback |

## Agentic RAG

Module 10: Agentic & Advanced RAG

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #97 | — | Retrieval as / a [tool] call | M | From fixed pipeline to decision-maker: retrieval as a tool call |
| RAG #98 | — | [Multi-hop] / retrieval | L | One lookup isn't enough: multi-hop & iterative retrieval |
| RAG #99 | Self-correcting RAG · Part 1/2 | [Self-RAG] | L | Self-RAG: the model critiques itself while it writes |
| RAG #100 | Self-correcting RAG · Part 2/2 | [Corrective] / RAG (CRAG) | L | Corrective RAG (CRAG): grade the retrieval, then fix it |
| RAG #101 | — | [Adaptive] / retrieval | L | The smartest retrieval is sometimes none: adaptive retrieval |
| RAG #102 | — | [Tool-] / augmented RAG | M | Retrieval is just one tool: tool-augmented RAG |
| RAG #103 | — | [Multi-agent] / RAG | L | Divide the labor: multi-agent RAG architectures |
| RAG #104 | — | Grounding / [loops] | L | Trust, then verify: post-generation grounding loops |

## Graph & SQL RAG

Module 11: Knowledge Graphs & Structured Retrieval

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #105 | — | [GraphRAG] | L | When "similar" isn't enough: GraphRAG |
| RAG #106 | — | [Entity] / extraction | L | Turning text into nodes and edges: entity & relationship extraction |
| RAG #107 | — | [Text-to-SQL] | L | When the answer is a row, not a paragraph: Text-to-SQL |
| RAG #108 | Hybrid graph + vector · Part 1/2 | Query / [routing] | L | Routing: send each query to the right retriever |
| RAG #109 | Hybrid graph + vector · Part 2/2 | [Blending] / retrievers | L | Blending: ask several retrievers and merge the evidence |

## RAG system design

Module 12: System Design Practice

| RAG # | Mini-series line | Cover title | Size | Series title (for reference) |
|---|---|---|---|---|
| RAG #110 | — | [Requirements] / first | M | Don't design yet: the requirements-clarification framework |
| RAG #111 | — | End-to-end / [architecture] | M | The 2-minute skeleton: sketching an end-to-end architecture |
| RAG #112 | — | Failure / [modes] | L | Design against named failures (out loud) |
| RAG #113 | — | [10K] to 10M / docs | L | What breaks at 1000×: scaling from 10K to 10M docs |
| RAG #114 | — | [Build] vs / buy | L | Build vs. buy: managed vs. self-hosted |
