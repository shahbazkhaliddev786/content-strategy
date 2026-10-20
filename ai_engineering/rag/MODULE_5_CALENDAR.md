# Pillar 2 — Content Calendar: Module 5 (Retrieval Strategies)

**Source:** `RAG_Curriculum (1).md` → Module 5
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 5 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 5 has 6 concepts → 12 posts (2 mini-series).**
**Key terms to cover (15):** `Dense retrieval` · `Sparse retrieval` · `BM25` · `TF-IDF` · `Hybrid search` · `Reciprocal Rank Fusion (RRF)` · `Score normalization` · `Query expansion` · `Query rewriting` · `HyDE (Hypothetical Document Embeddings)` · `Multi-query retrieval` · `Step-back prompting` · `ColBERT / late interaction` · `Maximal Marginal Relevance (MMR)` · `Diversity-aware reranking`

---

## Post 1 — Retrieving by meaning: dense retrieval

**Concept:** Dense (semantic) retrieval.

**Angle:** The RAG default from Modules 3–4 in action: embed the query, find the nearest document vectors, retrieve by *meaning*. Its superpower is paraphrase — "heart attack" finds "myocardial infarction." Its blind spot is the thing it's great at masking: exact tokens. A dense retriever can sail right past a part number, an error code, or a surname because those carry little semantic signal. Name the strength and the weakness honestly — it sets up why Posts 2–3 exist.

**Key terms covered here:**
- `Dense retrieval` *(primary)* — retrieval over learned embeddings using vector similarity; matches on semantics, not surface words.

**Senior-level tie-in:** state the failure mode out loud — dense retrieval under-performs on exact-match-heavy content (codes, IDs, rare proper nouns), which is the whole motivation for sparse and hybrid.

---

## Post 2 — The keyword classic that refuses to die: sparse retrieval

**Concept:** Sparse (lexical/keyword) retrieval.

**Angle:** Before embeddings, search was lexical — and it's still the right tool for exact matches. Sparse retrieval scores documents on term overlap with the query. Walk from TF-IDF (term frequency × inverse document frequency) to BM25, the battle-tested refinement that adds term saturation and length normalization. Show exactly where it beats dense: literal tokens, acronyms, part numbers, legal citations.

**Key terms covered here:**
- `Sparse retrieval` *(primary)* — ranking by lexical term overlap; vectors are high-dimensional and mostly zero (one dim per vocabulary term).
- `TF-IDF` *(primary)* — weight terms by how often they appear in a doc vs. how rare they are across the corpus.
- `BM25` *(primary)* — the modern lexical standard: TF-IDF plus term-frequency saturation and document-length normalization.

**Senior-level tie-in:** know *why* BM25 beats raw TF-IDF (diminishing returns on repeated terms + length correction) — it's the sparse half of every serious hybrid system.

---

## Post 3 — Best of both: hybrid retrieval & fusion *(mini-series · 2 parts)*

**Concept:** Hybrid retrieval and fusion methods.

**Angle:** Dense catches meaning, sparse catches exact tokens — so run both and merge. The catch is *how* you merge: dense cosine scores and BM25 scores live on completely different scales, so averaging raw scores is meaningless. The robust answer is to fuse by **rank**, not score. Explain RRF, contrast it with score-normalization approaches, and give the rule for when hybrid earns its complexity.

**Series structure:** the two ways to merge dense and sparse results each get their own post — fuse by rank (RRF) or fuse by normalized score.

**Senior-level tie-in (series):** the module bar — explain *why RRF, not averaging*: raw dense/sparse scores aren't comparable, but ranks are, so rank fusion is stable without tuning; and note hybrid matters **most** in exact-match-heavy domains (code, legal, medical codes) and **least** in smooth natural-language domains where dense alone suffices.

### Post 3.1 — Hybrid search with Reciprocal Rank Fusion: merge by rank

**Concept:** Hybrid retrieval fused with RRF.

**Angle:** Run dense and sparse retrieval in parallel, then merge the two ranked lists by position, not score: each document gets 1/(k + rank) from every list it appears in, and the sums decide the final order (k is a small constant, commonly 60). A document ranked high by both retrievers rises to the top, and the incompatible score scales never matter.

**Key terms covered here:**
- `Hybrid search` *(primary)* — combining dense and sparse retrieval and merging their results.
- `Reciprocal Rank Fusion (RRF)` *(primary)* — fuse ranked lists by summing 1/(k + rank) per item; uses only positions, so incompatible score scales never matter.
- `Dense retrieval` *(reinforced)* — one input stream of the fusion.
- `Sparse retrieval` *(reinforced)* — the other input stream.

**Senior-level tie-in:** explain *why RRF, not averaging*: raw dense/sparse scores aren't comparable, but ranks are, so rank fusion is stable without tuning. Hybrid matters **most** in exact-match-heavy domains (code, legal, medical codes) and **least** in smooth natural-language domains where dense alone suffices.

### Post 3.2 — Score normalization: merge by rescaled scores

**Concept:** Score-based fusion with normalization.

**Angle:** The alternative to RRF: rescale each retriever's raw scores onto a common range (for example min-max to 0–1), then combine them with a weighted sum. Unlike RRF it keeps *how much* better one result is than the next, and lets you weight dense vs. sparse explicitly. The cost: one outlier score or a shift in score distribution distorts the scale, and the weight needs tuning.

**Key terms covered here:**
- `Score normalization` *(primary)* — rescale each retriever's raw scores (e.g. min-max) onto a common range before combining — workable but brittle to outliers and distribution shifts.
- `Hybrid search` *(reinforced)* — the same goal, a different merge.

**Senior-level tie-in:** default to RRF; reach for normalized scores only when you have an eval set to tune the weight against and need one retriever to count more than the other.

---

## Post 4 — Fix the question before you search: query transformation *(mini-series · 6 parts)*

**Concept:** Query understanding and transformation before retrieval.

**Angle:** The user's raw query is often a bad search key — too short, ambiguous, underspecified, or phrased unlike the documents. A cheap LLM pass *before* retrieval can reshape it. Tour the family and when each applies: broaden it, clean it, hallucinate an ideal answer to embed, fan it into several, or zoom out to a more general question.

**Series structure:** one post per technique (full Problem → Intuition → How it works → Trade-offs → When to use → When NOT to use), then a comparison post mapping query problems to techniques.

**Senior-level tie-in (series):** these cost latency and LLM calls up front — know the trade: reach for them when queries are short/ambiguous/conversational, skip them when queries are already well-formed and latency-sensitive.

### Post 4.1 — Query expansion: add the words the user didn't type

**Concept:** Expanding a query with synonyms and related terms.

**Angle:** Users and documents often use different words for the same thing ("car" vs. "vehicle", "MI" vs. "heart attack"). Query expansion adds synonyms and related terms — from an LLM or a domain thesaurus — so retrieval catches documents that never use the user's exact wording. It helps keyword search the most, since sparse retrieval only matches literal terms.

**Key terms covered here:**
- `Query expansion` *(primary)* — add synonyms/related terms so retrieval catches more relevant docs.
- `Sparse retrieval` *(reinforced)* — the retriever that benefits most from extra terms.

**Senior-level tie-in:** expansion raises recall but can drag in off-topic matches — add terms carefully and measure precision, not just recall.

### Post 4.2 — Query rewriting: turn "what about the second one?" into a real query

**Concept:** Rewriting conversational queries into standalone search queries.

**Angle:** In a chat, follow-ups depend on history: "what about the second one?" is a terrible search key on its own. An LLM rewrites it into a clean, self-contained query using the conversation ("refund policy for annual plans"), and retrieval runs on that instead.

**Key terms covered here:**
- `Query rewriting` *(primary)* — rephrase a messy/conversational query into a clean, self-contained search query (e.g. resolve "what about the second one?").

**Senior-level tie-in:** in any multi-turn assistant this is close to mandatory — without it, follow-up questions retrieve garbage. Log both the original and the rewritten query for debugging (Module 9).

### Post 4.3 — HyDE: search with a fake answer

**Concept:** Hypothetical Document Embeddings.

**Angle:** A short question doesn't look like the long passage that answers it. HyDE asks an LLM to draft a hypothetical answer first, embeds *that*, and searches with it — because an answer-shaped text lands closer to real answer passages in embedding space. The draft can be wrong; it only needs to sound like the right documents.

**Key terms covered here:**
- `HyDE (Hypothetical Document Embeddings)` *(primary)* — have the LLM draft a hypothetical answer, embed *that*, and retrieve against it — answers look more like target documents than questions do.
- `Dense retrieval` *(reinforced)* — HyDE changes what gets embedded, not how retrieval works.

**Senior-level tie-in:** HyDE struggles when the LLM knows nothing about your domain — a confidently wrong draft points retrieval in the wrong direction — and it adds a generation call before every search.

### Post 4.4 — Multi-query retrieval: ask the question several ways

**Concept:** Generating several query variants and merging their results.

**Angle:** One phrasing captures one angle of the question. Multi-query has an LLM write several variants, runs retrieval for each, and merges the results (deduplicated, often with RRF), so documents phrased differently from the original query still get found.

**Key terms covered here:**
- `Multi-query retrieval` *(primary)* — generate several query variants, retrieve for each, union the results to cover more phrasings.
- `Reciprocal Rank Fusion (RRF)` *(reinforced)* — a natural way to merge the variant result lists.

**Senior-level tie-in:** cost scales with the number of variants — N variants means N retrievals per question — so use it where recall matters more than latency.

### Post 4.5 — Step-back prompting: zoom out before you zoom in

**Concept:** Retrieving with a broader, more abstract version of the question.

**Angle:** Some questions need background the specific wording won't retrieve. Step-back prompting first asks a more general question ("what principles govern X?"), retrieves the foundational context for it, and then answers the specific question with both sets of context.

**Key terms covered here:**
- `Step-back prompting` *(primary)* — ask a broader/more abstract version first to pull in foundational context before the specific query.

**Senior-level tie-in:** useful for reasoning-heavy questions that depend on general rules; wasted effort on simple lookups, where the extra retrieval only adds noise and latency.

### Post 4.6 — Which query transformation, when?

**Concept:** Choosing a query transformation technique.

**Angle:** Match the technique to the query's problem: vocabulary mismatch → expansion; conversational follow-up → rewriting; short question vs. long passages → HyDE; many valid phrasings → multi-query; needs background principles → step-back. Every one adds an LLM call before retrieval, so compare them on cost and latency too.

**Key terms covered here:**
- `Query expansion` *(reinforced)*
- `Query rewriting` *(reinforced)*
- `HyDE (Hypothetical Document Embeddings)` *(reinforced)*
- `Multi-query retrieval` *(reinforced)*
- `Step-back prompting` *(reinforced)*

**Senior-level tie-in:** transformations stack, and so do their costs — start with rewriting for chat, and add others only when evals show the specific failure each one fixes. Every technique has to earn its extra LLM call against the latency budget.

---

## Post 5 — One vector per token: multi-vector / late interaction

**Concept:** Multi-vector retrieval (late-interaction models).

**Angle:** Single-vector bi-encoders (Module 3) squash a whole chunk into one point — lossy. Cross-encoders (Module 6) are precise but can't pre-compute. Late interaction splits the difference: embed *every token* separately, store them, and at query time score via fine-grained token-to-token matching (MaxSim). You keep most of a cross-encoder's precision while retaining pre-computable, scalable indexing — at a higher storage cost.

**Key terms covered here:**
- `ColBERT / late interaction` *(primary)* — represent query and document as per-token vectors and defer their interaction to query time via MaxSim, capturing fine-grained matches a single pooled vector loses.

**Senior-level tie-in:** place it on the spectrum — bi-encoder (cheap, coarse) → late interaction (precise, heavier storage) → cross-encoder (most precise, no pre-compute); justify the storage cost only when single-vector recall is demonstrably the bottleneck.

---

## Post 6 — Stop retrieving the same thing five times: diversity-aware retrieval

**Concept:** Diversity-aware retrieval (avoiding redundant top-k).

**Angle:** A naive top-k often returns five near-identical chunks — the model gets one idea repeated, and the context window is wasted on redundancy instead of coverage. Diversity-aware methods re-score candidates to reward relevance *and* novelty, so the final set spans more of the answer. Especially critical for multi-faceted questions.

**Key terms covered here:**
- `Maximal Marginal Relevance (MMR)` *(primary)* — greedily pick results balancing similarity to the query against dissimilarity to already-chosen results, tuned by a λ parameter.
- `Diversity-aware reranking` *(primary)* — the general idea: reorder/prune the candidate set to cut redundancy and maximize coverage before handing context to the LLM.

**Senior-level tie-in:** tie it to the context budget — redundant chunks are pure waste; MMR trades a little top-1 relevance for broader coverage, which matters most on multi-part or comparative queries.

---

## Coverage check (all 15 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Dense retrieval` | Post 1 | Posts 3.1, 4.3 |
| `Sparse retrieval` | Post 2 | Posts 3.1, 4.1 |
| `BM25` | Post 2 | — |
| `TF-IDF` | Post 2 | — |
| `Hybrid search` | Post 3.1 | Post 3.2 |
| `Reciprocal Rank Fusion (RRF)` | Post 3.1 | Post 4.4 |
| `Score normalization` | Post 3.2 | — |
| `Query expansion` | Post 4.1 | Post 4.6 |
| `Query rewriting` | Post 4.2 | Post 4.6 |
| `HyDE (Hypothetical Document Embeddings)` | Post 4.3 | Post 4.6 |
| `Multi-query retrieval` | Post 4.4 | Post 4.6 |
| `Step-back prompting` | Post 4.5 | Post 4.6 |
| `ColBERT / late interaction` | Post 5 | — |
| `Maximal Marginal Relevance (MMR)` | Post 6 | — |
| `Diversity-aware reranking` | Post 6 | — |

✅ All 15 Module 5 key terms covered across the 12 posts.
