# Pillar 2 — RAG Series Posting Order

The single source of truth for **what gets posted, in what order**. One row = one daily post (**114 posts**).

- **RAG #** is the public series number shown on the carousel (top-right) and in captions.
- **Module / Post** point to the post's full brief in `MODULE_<N>_CALENDAR.md` (concept, angle, key terms, senior-level tie-in). Sub-numbered posts (e.g. `Post 2.1`) are parts of a mini-series.
- **Next post to publish** = the row after the last entry in [posted.md](posted.md). Its **teaser** names the row after that.
- Module calendars keep their original post numbering; this file adds the global order on top, so the two never conflict.

| RAG # | Module | Post | Title | Mini-series |
|---|---|---|---|---|
| RAG #01 | M0 | Post 1 | What problem does RAG actually solve? | — |
| RAG #02 | M0 | Post 2 | The two pipelines: how a RAG system is actually wired | — |
| RAG #03 | M0 | Post 3.1 | Long-context: just paste it all in | RAG vs. Alternatives · Part 1/3 |
| RAG #04 | M0 | Post 3.2 | Fine-tuning: rewrite the model's memory | RAG vs. Alternatives · Part 2/3 |
| RAG #05 | M0 | Post 3.3 | The decision guide: RAG vs. long-context vs. fine-tuning vs. knowledge graphs | RAG vs. Alternatives · Part 3/3 |
| RAG #06 | M1 | Post 1 | Getting content in: source connectors | — |
| RAG #07 | M1 | Post 2.1 | Scanned PDFs are just pixels: OCR | File Formats · Part 1/3 |
| RAG #08 | M1 | Post 2.2 | Tables turn into word soup: table serialization | File Formats · Part 2/3 |
| RAG #09 | M1 | Post 2.3 | Digital files break too: format-aware parsing for HTML, DOCX & code | File Formats · Part 3/3 |
| RAG #10 | M1 | Post 3 | Layout-aware parsing vs. naive text extraction | — |
| RAG #11 | M1 | Post 4.1 | Describe it in words: captioning images with a vision model | Multi-modal Content · Part 1/2 |
| RAG #12 | M1 | Post 4.2 | Embed the image itself: direct multi-modal retrieval | Multi-modal Content · Part 2/2 |
| RAG #13 | M1 | Post 5 | Ingestion is never "done": versioning & change detection | — |
| RAG #14 | M2 | Post 1 | Fixed-size chunking: the simplest cut (and the vocabulary everything builds on) | — |
| RAG #15 | M2 | Post 2 | Recursive / structure-aware splitting: cut along the seams | — |
| RAG #16 | M2 | Post 3 | Semantic chunking: let meaning decide the boundaries | — |
| RAG #17 | M2 | Post 4.1 | Match small, return the parent: the parent-document retriever | Small-to-Big · Part 1/2 |
| RAG #18 | M2 | Post 4.2 | One sentence in, a window out: sentence-window retrieval | Small-to-Big · Part 2/2 |
| RAG #19 | M2 | Post 5.1 | Chunking code: split on functions, not characters | Chunking by Doc Type · Part 1/4 |
| RAG #20 | M2 | Post 5.2 | Chunking tables: never separate a row from its headers | Chunking by Doc Type · Part 2/4 |
| RAG #21 | M2 | Post 5.3 | Chunking legal documents: the clause is the unit | Chunking by Doc Type · Part 3/4 |
| RAG #22 | M2 | Post 5.4 | Chunking transcripts: keep the conversation turns together | Chunking by Doc Type · Part 4/4 |
| RAG #23 | M2 | Post 6 | Contextual chunk augmentation: give each chunk its bearings | — |
| RAG #24 | M2 | Post 7 | Tuning the knobs: chunk size, overlap, and embedding quality | — |
| RAG #25 | M3 | Post 1.1 | Meaning as geometry: text becomes a point in space | Embeddings 101 · Part 1/2 |
| RAG #26 | M3 | Post 1.2 | How close is close? Cosine vs. dot product vs. L2 | Embeddings 101 · Part 2/2 |
| RAG #27 | M3 | Post 2 | Two encoders, one offline job: the bi-encoder | — |
| RAG #28 | M3 | Post 3 | Symmetric vs. asymmetric: a question is not a passage | — |
| RAG #29 | M3 | Post 4 | Don't trust the leaderboard: choosing & benchmarking embeddings | — |
| RAG #30 | M3 | Post 5 | When general models miss your jargon: fine-tuning embeddings | — |
| RAG #31 | M3 | Post 6 | One embedding, many sizes: Matryoshka & dimensionality trade-offs | — |
| RAG #32 | M3 | Post 7 | One space for text and images: cross-modal embeddings | — |
| RAG #33 | M3 | Post 8 | You can't mix spaces: embedding drift & re-indexing on upgrade | — |
| RAG #34 | M4 | Post 1 | Exact vs. approximate: why search gets "good enough" on purpose | — |
| RAG #35 | M4 | Post 2.1 | HNSW: search by walking a graph | ANN Algorithms · Part 1/6 |
| RAG #36 | M4 | Post 2.2 | IVF: only search the nearest buckets | ANN Algorithms · Part 2/6 |
| RAG #37 | M4 | Post 2.3 | Product Quantization: shrink every vector to a few bytes | ANN Algorithms · Part 3/6 |
| RAG #38 | M4 | Post 2.4 | LSH: hash similar vectors into the same bucket | ANN Algorithms · Part 4/6 |
| RAG #39 | M4 | Post 2.5 | ScaNN: quantization tuned for ranking | ANN Algorithms · Part 5/6 |
| RAG #40 | M4 | Post 2.6 | HNSW vs. IVF vs. PQ vs. LSH vs. ScaNN: which one, when? | ANN Algorithms · Part 6/6 |
| RAG #41 | M4 | Post 3 | The knobs: build-time vs. query-time tuning | — |
| RAG #42 | M4 | Post 4 | Choosing a vector database (it's not about raw QPS) | — |
| RAG #43 | M4 | Post 5.1 | Pre-filtering: narrow the set, then search | Filtering · Part 1/4 |
| RAG #44 | M4 | Post 5.2 | Post-filtering: search first, filter after | Filtering · Part 2/4 |
| RAG #45 | M4 | Post 5.3 | Filtered ANN: filter during the search (and its trap) | Filtering · Part 3/4 |
| RAG #46 | M4 | Post 5.4 | Pre vs. post vs. filtered ANN: choose by filter selectivity | Filtering · Part 4/4 |
| RAG #47 | M4 | Post 6.1 | Sharding: when the index no longer fits on one node | Scaling the Index · Part 1/2 |
| RAG #48 | M4 | Post 6.2 | Replication: when one copy can't serve the traffic | Scaling the Index · Part 2/2 |
| RAG #49 | M4 | Post 7 | One system or several? The hybrid-storage question | — |
| RAG #50 | M5 | Post 1 | Retrieving by meaning: dense retrieval | — |
| RAG #51 | M5 | Post 2 | The keyword classic that refuses to die: sparse retrieval | — |
| RAG #52 | M5 | Post 3.1 | Hybrid search with Reciprocal Rank Fusion: merge by rank | Hybrid Fusion · Part 1/2 |
| RAG #53 | M5 | Post 3.2 | Score normalization: merge by rescaled scores | Hybrid Fusion · Part 2/2 |
| RAG #54 | M5 | Post 4.1 | Query expansion: add the words the user didn't type | Query Transformation · Part 1/6 |
| RAG #55 | M5 | Post 4.2 | Query rewriting: turn "what about the second one?" into a real query | Query Transformation · Part 2/6 |
| RAG #56 | M5 | Post 4.3 | HyDE: search with a fake answer | Query Transformation · Part 3/6 |
| RAG #57 | M5 | Post 4.4 | Multi-query retrieval: ask the question several ways | Query Transformation · Part 4/6 |
| RAG #58 | M5 | Post 4.5 | Step-back prompting: zoom out before you zoom in | Query Transformation · Part 5/6 |
| RAG #59 | M5 | Post 4.6 | Which query transformation, when? | Query Transformation · Part 6/6 |
| RAG #60 | M5 | Post 5 | One vector per token: multi-vector / late interaction | — |
| RAG #61 | M5 | Post 6 | Stop retrieving the same thing five times: diversity-aware retrieval | — |
| RAG #62 | M6 | Post 1 | Cast a wide net, then be picky: the two-stage pattern | — |
| RAG #63 | M6 | Post 2 | Why cross-encoders out-rank bi-encoders | — |
| RAG #64 | M6 | Post 3.1 | API or open-source: choosing a reranker model | Choosing a Reranker · Part 1/4 |
| RAG #65 | M6 | Post 3.2 | Pointwise ranking: score each document on its own | Choosing a Reranker · Part 2/4 |
| RAG #66 | M6 | Post 3.3 | Pairwise ranking: which of these two is better? | Choosing a Reranker · Part 3/4 |
| RAG #67 | M6 | Post 3.4 | Listwise ranking: order the whole list at once | Choosing a Reranker · Part 4/4 |
| RAG #68 | M6 | Post 4 | The latency tax: when reranking is worth it (and when it isn't) | — |
| RAG #69 | M6 | Post 5 | The model as judge: LLM-as-reranker | — |
| RAG #70 | M7 | Post 1 | The context window is a budget, not a bucket | — |
| RAG #71 | M7 | Post 2 | Where you put a chunk changes whether the model reads it | — |
| RAG #72 | M7 | Post 3 | The prompt that makes the model answer from the docs, not its memory | — |
| RAG #73 | M7 | Post 4 | Make it cite its sources (and check that it did) | — |
| RAG #74 | M7 | Post 5.1 | Abstain before generating: the score threshold | Abstention · Part 1/3 |
| RAG #75 | M7 | Post 5.2 | Abstain while generating: the refusal instruction | Abstention · Part 2/3 |
| RAG #76 | M7 | Post 5.3 | Abstain after generating: the grounding-check veto | Abstention · Part 3/3 |
| RAG #77 | M7 | Post 6.1 | Let metadata decide: recency and authority precedence | Conflicting Evidence · Part 1/3 |
| RAG #78 | M7 | Post 6.2 | Say it out loud: surfacing the conflict | Conflicting Evidence · Part 2/3 |
| RAG #79 | M7 | Post 6.3 | Show both sides: present both with attribution | Conflicting Evidence · Part 3/3 |
| RAG #80 | M8 | Post 1 | Two layers you must measure separately: retrieval vs. generation metrics | — |
| RAG #81 | M8 | Post 2 | The thing you can't skip: building a golden dataset from scratch | — |
| RAG #82 | M8 | Post 3 | Faster but biased: synthetic eval-set generation | — |
| RAG #83 | M8 | Post 4 | Scoring quality at scale: LLM-as-judge & the RAGAS metrics | — |
| RAG #84 | M8 | Post 5 | Stop shipping silent regressions: regression testing for RAG | — |
| RAG #85 | M8 | Post 6 | Lab vs. reality: online vs. offline evaluation signals | — |
| RAG #86 | M8 | Post 7 | The average is lying to you: query-type segmentation | — |
| RAG #87 | M9 | Post 1 | Where the milliseconds go: decomposing the latency budget | — |
| RAG #88 | M9 | Post 2.1 | Embedding cache: never embed the same text twice | Caching · Part 1/2 |
| RAG #89 | M9 | Post 2.2 | Semantic cache: reuse answers for questions that mean the same thing | Caching · Part 2/2 |
| RAG #90 | M9 | Post 3 | Keeping the index alive: upserts, deletes & versioning | — |
| RAG #91 | M9 | Post 4 | Know your cost per query before scale punishes you | — |
| RAG #92 | M9 | Post 5 | You can't debug what you can't see: retrieval observability | — |
| RAG #93 | M9 | Post 6 | One index, many customers: multi-tenancy & access control | — |
| RAG #94 | M9 | Post 7.1 | Five copies of the same chunk: deduplication & near-duplicate detection | Production Failures · Part 1/3 |
| RAG #95 | M9 | Post 7.2 | The outdated doc wins: recency boosting | Production Failures · Part 2/3 |
| RAG #96 | M9 | Post 7.3 | Nothing relevant came back: the empty-retrieval fallback | Production Failures · Part 3/3 |
| RAG #97 | M10 | Post 1 | From fixed pipeline to decision-maker: retrieval as a tool call | — |
| RAG #98 | M10 | Post 2 | One lookup isn't enough: multi-hop & iterative retrieval | — |
| RAG #99 | M10 | Post 3.1 | Self-RAG: the model critiques itself while it writes | Self-Correcting RAG · Part 1/2 |
| RAG #100 | M10 | Post 3.2 | Corrective RAG (CRAG): grade the retrieval, then fix it | Self-Correcting RAG · Part 2/2 |
| RAG #101 | M10 | Post 4 | The smartest retrieval is sometimes none: adaptive retrieval | — |
| RAG #102 | M10 | Post 5 | Retrieval is just one tool: tool-augmented RAG | — |
| RAG #103 | M10 | Post 6 | Divide the labor: multi-agent RAG architectures | — |
| RAG #104 | M10 | Post 7 | Trust, then verify: post-generation grounding loops | — |
| RAG #105 | M11 | Post 1 | When "similar" isn't enough: GraphRAG | — |
| RAG #106 | M11 | Post 2 | Turning text into nodes and edges: entity & relationship extraction | — |
| RAG #107 | M11 | Post 3 | When the answer is a row, not a paragraph: Text-to-SQL | — |
| RAG #108 | M11 | Post 4.1 | Routing: send each query to the right retriever | Hybrid Graph + Vector · Part 1/2 |
| RAG #109 | M11 | Post 4.2 | Blending: ask several retrievers and merge the evidence | Hybrid Graph + Vector · Part 2/2 |
| RAG #110 | M12 | Post 1 | Don't design yet: the requirements-clarification framework | — |
| RAG #111 | M12 | Post 2 | The 2-minute skeleton: sketching an end-to-end architecture | — |
| RAG #112 | M12 | Post 3 | Design against named failures (out loud) | — |
| RAG #113 | M12 | Post 4 | What breaks at 1000×: scaling from 10K to 10M docs | — |
| RAG #114 | M12 | Post 5 | Build vs. buy: managed vs. self-hosted | — |
