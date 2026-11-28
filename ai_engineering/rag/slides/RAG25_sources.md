# RAG #25 (format v3): sources (not posted)

Every example output on the slides is real. `RAG25_verify.py` re-runs each one and checks the slide text against it.

- **Test set:** 5 made-up help-centre docs (Refunds, Password, Invoices, Export, Seats), one sentence each, and 4 questions that share no content word with the doc that answers them. Built inside `RAG25_verify.py`.
- **Embedding:** spaCy 3.8 `en_core_web_md` 3.8.0 (300-dimensional word vectors; downloaded from the spaCy models release on GitHub, since Hugging Face models can't be downloaded from the build environment). A text's vector is the mean of the vectors of its content words (spaCy stop words and punctuation dropped). Cosine similarity. A weak embedding, named on the slides. For "How do I get my money back?" the only content word is "money".
- **Second model (slide 10):** `en_core_web_lg` 3.8.0, same method. md keeps 20,000 vectors for 684,830 keys (a pruned version of the lg table, 342,918 vectors), so this shows a pruned copy moving an answer, not two unrelated spaces. "refund" has the identical vector in md and lg (checked). With both question and docs from lg, "How do I invite a colleague?" → Seats 0.477; with the question from md and docs from lg → Invoices 0.462, Seats 2nd.
- **Sparse vector:** scikit-learn `CountVectorizer()` defaults, fitted on the 5 docs: 34-word vocabulary; the refund question's vector has 0 non-zero entries.
- **BM25:** `rank_bm25` 0.2.2 `BM25Okapi`, lower-cased `\w+` tokens. Refund question: 0.0 on all 5 docs. Colleague question: only Export scores above 0, through the shared token "a".
- **Cosine scores, refund question:** Refunds 0.636, Invoices 0.449, Seats 0.402, Export 0.279, Password 0.222. Top hits for the 4 questions: Refunds 0.636, Export 0.670, Invoices 0.475, Seats 0.453.
- **"Money" neighbours:** among the refund doc's content words, the 3 closest to "money" by cosine are business, refunds, card (business, from "5 business days", is closest: part of the 0.636 is a word association, not meaning).
- **Negation and word order:** "Monthly plans can be refunded." vs "Monthly plans cannot be refunded." → 1.000 ("cannot" tokenizes to "can" + "not", both stop words). "The customer refunds the company." vs "The company refunds the customer." → 1.000.
- **OpenAI embeddings guide:** "An embedding is a vector (list) of floating point numbers." "By default, the length of the embedding vector is 1536 for text-embedding-3-small or 3072 for text-embedding-3-large." https://developers.openai.com/api/docs/guides/embeddings
- **all-MiniLM-L6-v2 model card:** "maps sentences & paragraphs to a 384 dimensional dense vector space". https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
