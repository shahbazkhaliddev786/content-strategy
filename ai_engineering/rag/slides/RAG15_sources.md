# RAG #15 (format v3, dense draft): sources (not posted)

Every example output on the slides is real output from `langchain-text-splitters` 1.1.3. `RAG15_verify.py` re-runs each one and checks the slide text against it (21 checks).

- **LangChain docs** call `RecursiveCharacterTextSplitter` "the recommended one for generic text" and give the default list `["\n\n", "\n", " ", ""]`: https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter
- **How it recurses (slide 3):** read from the 1.1.3 source: `RecursiveCharacterTextSplitter._split_text`, `TextSplitter._merge_splits`, `_split_text_with_regex`.
  - First separator in the list found in the text is used; pieces at or over `chunk_size` recurse with the remaining separators; pieces under it are merged up to `chunk_size`.
  - Overlap is whole trailing pieces up to `chunk_overlap`: with sentence pieces and `chunk_size=100`, `chunk_overlap=50` repeats a 45-character sentence and `chunk_overlap=40` repeats nothing.
  - With no separator left (no `""` in the list), an oversized piece is appended as is, without the "Created a chunk of size …" warning.
- **Defaults (slides 2, 7):** `chunk_size=4000`, `chunk_overlap=200`, `length_function=len`, `keep_separator=True` (same as `"start"`).
- **Token sizing (slide 7):** `from_tiktoken_encoder(encoding_name="gpt2", model_name=None, …)`; `model_name` overrides the encoding. tiktoken 0.14.0 maps `text-embedding-3-small`, `text-embedding-3-large` and `text-embedding-ada-002` to `cl100k_base`.
- **"4,000 characters is roughly 1,000 tokens of English":** measured with cl100k_base (gpt-tokenizer 4.1.0, token IDs checked against tiktoken) on three English docs in this repo: 3.88 to 4.46 characters per token, so 4,000 characters is about 900 to 1,030 tokens.
- **Markdown preset (slide 8):** `get_separators_for_language(Language.MARKDOWN)` starts with headings (`\n#{1,6} `), then code fences, horizontal rules, paragraphs. `from_language` sets `is_separator_regex=True`. The `Language` enum has 28 values in 1.1.3.
- **Abbreviations (slide 9):** with `". "` in the list and `chunk_size=40`, "For refunds over $500, e.g. laptops, ask Dr. Patel." is cut after "e.g." `NLTKTextSplitter` and `SpacyTextSplitter` ship in the same package.
