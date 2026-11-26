# RAG #24 (format v3): sources (not posted)

Every example output on the slides is real. `RAG24_verify.py` re-runs each one and checks the slide text against it.

- **Test set:** 6 made-up help-centre sections (Refunds, Seats and billing, Data retention, Security, API limits, Support), 2,782 characters, and 20 questions, each paired with the exact text that answers it (each answer text appears in one section only). Built inside `RAG24_verify.py`.
- **Splitter:** `langchain-text-splitters` 1.1.3, `RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""], keep_separator="end")`, each section split on its own. `TextSplitter` defaults read from the installed signature: `chunk_size=4000`, `chunk_overlap=200`, `length_function=len`.
- **Embeddings:** spaCy 3.8 `en_core_web_md` 3.8.0 (downloaded from the spaCy models release on GitHub; Hugging Face models can't be downloaded from the build environment). A text's vector is the mean of its word vectors (checked in the script), normalised; cosine similarity. A weak embedding, named on the slides; the post says the sizes will differ for other models.
- **BM25:** `rank_bm25` 0.2.2 `BM25Okapi`, lower-cased `\w+` tokens.
- **"Found":** the answer text appears whole inside one retrieved chunk. Top-3: the 3 best-scoring chunks. 400-character cap: whole chunks added in rank order while they fit in 400 characters, always at least one (so 300 and 500 send only their top chunk).
- **Results (spaCy vectors, top-3):** 60: 7, 100: 9, 150: 13, 200: 14, 300: 16, 500: 19 of 20. At 500 the index holds 7 chunks.
- **Results (spaCy vectors, 400-character budget):** 60: 10, 100: 13, 150: 13, 200: 12, 300: 12, 500: 9.
- **Results (BM25, 400-character budget):** 60: 11, 100: 15, 150: 17, 200: 18, 300: 18, 500: 17.
- **Overlap:** 200 with overlap 0 or 40: 21 chunks, 2,755 characters either way (every piece is a paragraph longer than 40). 60 with overlap 12: 68 → 70 chunks, 2,708 → 2,925 characters (+8%); top-3 found 7 → 8. Overlap mechanism (whole pieces) matches RAG #15.
- **Small/big examples:** at 60, "How long are audit logs kept on Enterprise?" → "years on Enterprise." first; "When are invoices due?" → "invoice." first. "Can I get a refund on a monthly plan?": at 150 the monthly-plan sentence ranks 1st (0.925); at 500 the Seats and billing section ranks 1st (0.918) and Refunds 2nd (0.916).
- **all-MiniLM-L6-v2 model card** (Intended uses): "By default, input text longer than 256 word pieces is truncated." https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- **OpenAI embeddings guide:** text-embedding-3-small and text-embedding-3-large, max input 8192 tokens. https://developers.openai.com/api/docs/guides/embeddings ; cookbook: "OpenAI's embedding models cannot embed text that exceeds a maximum length." https://developers.openai.com/cookbook/examples/embedding_long_inputs/
- **Token sizing:** `TextSplitter.from_tiktoken_encoder(encoding_name="gpt2", model_name=None, ...)`; tiktoken maps `text-embedding-3-small` to `cl100k_base` (checked in the script; see RAG #15).
