# RAG #18 (format v3): sources (not posted)

Every example output on the slides is real. `RAG18_verify.py` re-runs each one and checks the slide text against it (34 checks).

- **Library:** `llama-index-core` 0.14.25, read from the installed source.
  - `SentenceWindowNodeParser` (`llama_index.core.node_parser`): `window_size` default 3 ("The number of sentences on each side of a sentence to capture"), `window_metadata_key="window"`, `original_text_metadata_key="original_text"`. Default `sentence_splitter` is `split_by_sentence_tokenizer()`, which uses NLTK's `PunktSentenceTokenizer` (`llama_index.core.utils.GlobalsHelper`, downloads `punkt_tab`).
  - Windows are built per input document or node: `nodes[max(0, i - window_size) : min(i + window_size + 1, len(nodes))]`, joined with spaces, stored in `node.metadata["window"]`. Both keys are added to `excluded_embed_metadata_keys` and `excluded_llm_metadata_keys`.
  - `MetadataReplacementPostProcessor(target_metadata_key=...)` replaces each node's content with `metadata[target_key]` (falls back to the node's own content when the key is missing).
  - `DEFAULT_SIMILARITY_TOP_K = 2` (`llama_index.core.constants`).
  - `MarkdownNodeParser` + `SentenceWindowNodeParser` in an `IngestionPipeline`: the window parser runs per section node, so windows stay inside a section.
- **Embeddings in the examples:** spaCy 3.8 `en_core_web_md` 3.8.0 (average word vectors), wrapped as a LlamaIndex `BaseEmbedding`. `Settings.llm = None` (MockLLM) for the query-engine check; only retrieval is measured.
- **Corpus:** the 4-section support handbook from RAG #17 (1,360 characters), read from `RAG17_verify.py`.
- **Measurements:**
  - 27 sentence nodes (Punkt keeps each heading attached to the first sentence under it). Stored window text: 8,973 characters at `window_size=3` (6.6× the handbook), 3,992 at `window_size=1`.
  - "Who has to approve refunds over $500?": top hit "Refunds over $500 follow a separate rule." (score 0.903); its window (363 characters) contains "They need a second approval from the finance team." Window lengths for the same hit: 143 / 233 / 363 characters at window_size 1 / 2 / 3, all containing the answer. Without the postprocessor the retriever returns only the sentence; `get_content(MetadataMode.LLM)` leaves the window out.
  - "Do international orders pay customs fees?": top hit is the customs sentence; with the whole handbook as one Document its window ends with "## Warranty Every device has a 1-year warranty from the delivery date."; with `MarkdownNodeParser` first it ends with the "Damaged parcels…" sentence.
  - "How long do warranty repairs take?", `similarity_top_k=4`: hits are sentences 15, 18, 20 and 3; their windows total 1,438 characters (handbook: 1,360); sentence 18 appears in 3 of them. Dropping hits whose sentence is already inside a higher-ranked window leaves 3 windows, 1,066 characters, still containing "Repairs take about 10 business days."
- **Part 1 comparison:** RAG #17's setup indexed 23 children of up to 100 characters (see `RAG17_sources.md`).
