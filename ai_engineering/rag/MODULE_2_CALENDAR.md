# Pillar 2 — Content Calendar: Module 2 (Chunking Strategies)

**Source:** `RAG_Curriculum (1).md` → Module 2
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 2 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 2 has 7 concepts → 11 posts (2 mini-series).**
**Key terms to cover (11):** `Chunk` · `Chunk overlap` · `Sliding window` · `Semantic chunking` · `Recursive character/token splitting` · `Parent-document retriever` · `Small-to-big retrieval` · `Contextual Retrieval` (Anthropic technique) · `Chunk boundary problem` · `Token-based vs. character-based splitting` · `Sentence-window retrieval`

---

## Post 1 — Fixed-size chunking: the simplest cut (and the vocabulary everything builds on)

**Concept:** Fixed-size chunking with overlap.

**Angle:** Start at the floor. The simplest chunker slices a document into equal-size pieces and lets consecutive pieces overlap so context isn't severed at the seam. It's crude, but it defines the vocabulary the whole module depends on — so nail the terms here before anything fancier.

**Key terms covered here:**
- `Chunk` *(primary)* — the unit of text that gets embedded and retrieved; the atom of a RAG index.
- `Chunk overlap` *(primary)* — repeating a tail of one chunk at the head of the next so meaning that straddles a boundary survives.
- `Sliding window` *(primary)* — the mechanism itself: a fixed-size window advanced by a fixed stride (stride < size ⇒ overlap).
- `Token-based vs. character-based splitting` *(primary)* — what "size" is measured in; tokens align with how the embedding model actually reads text, characters are simpler but model-agnostic.

**Senior-level tie-in:** fixed-size is the baseline every other strategy is justified *against* — know exactly what it costs you before you reach for something smarter.

---

## Post 2 — Recursive / structure-aware splitting: cut along the seams

**Concept:** Recursive / structure-aware splitting.

**Angle:** Documents already have structure — sections, paragraphs, sentences. Recursive splitting respects it: try to split on the biggest natural separator first, and only fall back to finer ones when a piece is still too big. This directly attacks the thing fixed-size ignores — cutting through the middle of an idea.

**Key terms covered here:**
- `Recursive character/token splitting` *(primary)* — split on an ordered list of separators (e.g. `\n\n` → `\n` → `. ` → ` `), recursing only when a chunk still exceeds the size limit.
- `Chunk boundary problem` *(primary)* — the core failure recursive splitting mitigates: a split that lands mid-sentence or mid-idea strands meaning on both sides and degrades retrieval.

**Senior-level tie-in:** first of the module's "≥2 boundary-problem mitigations" — recursive splitting is mitigation #1.

---

## Post 3 — Semantic chunking: let meaning decide the boundaries

**Concept:** Semantic chunking (embedding-based boundary detection).

**Angle:** Structure-aware splitting trusts punctuation and whitespace. Semantic chunking goes further — it embeds sentences and cuts where the *meaning* shifts (a large jump in embedding distance between adjacent sentences signals a topic change). Boundaries land where the content actually turns, not where a newline happens to be.

**Key terms covered here:**
- `Semantic chunking` *(primary)* — detecting chunk boundaries from embedding similarity between adjacent units, splitting at points of low similarity (topic shift).
- `Chunk boundary problem` *(reinforced)* — mitigation #2: boundaries follow meaning, so fewer ideas get split.

**Senior-level tie-in:** completes the module bar's "name ≥2 mitigations" — recursive (Post 2) + semantic (here); also flag the cost (extra embedding passes at ingest time).

---

## Post 4 — Small-to-big: retrieve precise, return rich *(mini-series · 2 parts)*

**Concept:** Hierarchical / parent-child chunking (small-to-big retrieval).

**Angle:** There's a tension: small chunks retrieve *precisely* (tight embeddings) but give the LLM too little context; big chunks give context but retrieve fuzzily. Small-to-big resolves it — index small, then hand the model the larger parent the match came from. Cover the family of techniques that do this.

**Series structure:** the two main small-to-big techniques each get their own post.

**Senior-level tie-in (series):** this is where you decouple *what you match on* from *what you feed the model* — a defining move of production-grade retrieval.

### Post 4.1 — Match small, return the parent: the parent-document retriever

**Concept:** Parent-document retrieval — index child chunks, return their parent section.

**Angle:** Split each section into small child chunks and embed only those, but keep a link from every child to its parent. When a child matches, return the whole parent section to the LLM. You get the precision of small embeddings with the context of a full section.

**Key terms covered here:**
- `Small-to-big retrieval` *(primary)* — the general pattern: match on small units, expand to bigger context before generation.
- `Parent-document retriever` *(primary)* — index small child chunks for matching, but return their larger parent document/section to the LLM.

**Senior-level tie-in:** watch parent size — several hits from different parents can blow the context budget fast; dedupe parents when multiple children from the same one match.

### Post 4.2 — One sentence in, a window out: sentence-window retrieval

**Concept:** Sentence-window retrieval — embed single sentences, return their neighbors.

**Angle:** Go even smaller: embed individual sentences, so each vector is about exactly one idea. On a hit, return a window of the surrounding sentences (e.g. 2–3 on each side) so the model sees the context that sentence depends on.

**Key terms covered here:**
- `Sentence-window retrieval` *(primary)* — a specific variant: embed single sentences, then return a window of surrounding sentences around each hit.
- `Small-to-big retrieval` *(reinforced)* — the same pattern at sentence granularity.

**Senior-level tie-in:** choose sentence-window for dense, fact-heavy text where one sentence holds the answer; choose parent-document when answers need the whole section's structure. Sentence-level indexing also means many more vectors to store.

---

## Post 5 — One chunker doesn't fit all: document-type-specific chunking *(mini-series · 4 parts)*

**Concept:** Document-type-specific chunking — code, tables, legal clauses, conversation transcripts.

**Angle:** A strategy tuned for prose wrecks a codebase. Code has functions and classes; tables have rows; legal docs have numbered clauses; transcripts have turns. The natural unit changes with the document type, and so should the splitter. Walk through each type and its right boundary.

**Series structure:** one post per document type, each answering: what's the natural unit, how does a prose chunker break it, and what's the right boundary.

**Senior-level tie-in (series):** directly the module bar — be able to *pick and justify* a chunking strategy per document type on the spot.

### Post 5.1 — Chunking code: split on functions, not characters

**Concept:** Chunking source code along syntactic boundaries.

**Angle:** A character-count splitter cuts a function in half, separating its signature from its body. Code's natural unit is the function or class: split on those boundaries using language-aware separators, and keep enough surrounding context (file path, class name, imports) that a chunk still makes sense on its own.

**Key terms covered here:**
- `Recursive character/token splitting` *(reinforced)* — adapt the separator list per type (e.g. split code on function/class boundaries).
- `Chunk boundary problem` *(reinforced)* — splitting mid-function is the same failure in a new costume.

**Senior-level tie-in:** very long functions still need splitting — fall back to logical blocks inside them, and carry the signature into each piece.

### Post 5.2 — Chunking tables: never separate a row from its headers

**Concept:** Chunking tabular data by rows while keeping headers attached.

**Angle:** Split a long table by character count and later chunks lose the header row — a column of numbers with no labels. Chunk by groups of whole rows instead, and repeat the header (and table title) in every chunk so each one is self-describing.

**Key terms covered here:**
- `Chunk boundary problem` *(reinforced)* — cutting mid-row or dropping headers is the table version of the failure.
- `Recursive character/token splitting` *(reinforced)* — row boundaries become the separator.

**Senior-level tie-in:** for questions that aggregate across a whole table ("total by region"), chunking won't help — that's a Text-to-SQL problem (Module 11).

### Post 5.3 — Chunking legal documents: the clause is the unit

**Concept:** Chunking legal and contractual text on clause boundaries.

**Angle:** Legal text is built from numbered clauses and sub-clauses, and meaning depends on both the clause and where it sits ("Section 4.2(b)"). Split on clause markers, keep the clause number and heading path in each chunk, and avoid merging unrelated clauses just to hit a size target.

**Key terms covered here:**
- `Recursive character/token splitting` *(reinforced)* — clause markers as the separator list.
- `Chunk boundary problem` *(reinforced)* — splitting mid-clause can flip a meaning ("shall" vs. an exception in the next line).

**Senior-level tie-in:** clauses reference each other ("subject to Section 7") — note that a single chunk may not carry the full answer, which motivates multi-hop retrieval later (Module 10).

### Post 5.4 — Chunking transcripts: keep the conversation turns together

**Concept:** Chunking conversation transcripts on speaker turns.

**Angle:** Meetings, support calls, and interviews are sequences of speaker turns. A size-based splitter separates a question from its answer. Split on turns, keep speaker labels (and timestamps), and group related exchanges — a question and its reply — into the same chunk.

**Key terms covered here:**
- `Chunk boundary problem` *(reinforced)* — splitting a question from its answer is the transcript version.
- `Recursive character/token splitting` *(reinforced)* — speaker turns as the separator.

**Senior-level tie-in:** long single turns (a monologue) still need sub-splitting — keep the speaker label on every piece.

---

## Post 6 — Contextual chunk augmentation: give each chunk its bearings

**Concept:** Contextual chunk augmentation — prepending summaries/context to chunks before embedding.

**Angle:** A chunk ripped out of a 50-page doc often loses what it refers to ("the company" — which one? "this approach" — to what?). Before embedding, prepend a short, chunk-specific blurb situating it in the overall document. The embedding then carries that context, so retrieval improves without changing the query side.

**Key terms covered here:**
- `Contextual Retrieval` *(primary)* — Anthropic's technique: use an LLM to generate a short context describing how each chunk fits in its source document, prepend it to the chunk before embedding (and indexing for lexical search), markedly reducing failed retrievals.

**Senior-level tie-in:** a cheap-at-ingest, no-cost-at-query upgrade — know *why* it helps (richer, disambiguated embeddings) and its trade-off (one LLM call per chunk at ingest).

---

## Post 7 — Tuning the knobs: chunk size, overlap, and embedding quality

**Concept:** Chunk size / overlap tuning and its effect on embedding quality.

**Angle:** Chunking has dials, and they interact with the embedding model. Too big: the vector averages many ideas into mush and retrieval gets vague. Too small: each vector is sharp but context is lost and you retrieve fragments. Overlap trades redundancy/cost for boundary safety. Show how to tune empirically against a retrieval eval, not by vibes.

**Key terms covered here:**
- `Chunk` *(reinforced)* — size directly shapes what a single vector can faithfully represent.
- `Chunk overlap` *(reinforced)* — the cost/safety dial: more overlap = fewer severed ideas but more storage and duplicate hits.
- `Token-based vs. character-based splitting` *(reinforced)* — why token-based sizing is safer: it respects the embedding model's real input budget.

**Senior-level tie-in:** there's no universal best size — tie the choice to document type (Post 5) and measure it; tuning is an eval-driven loop, not a constant.

---

## Coverage check (all 11 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Chunk` | Post 1 | Post 7 |
| `Chunk overlap` | Post 1 | Post 7 |
| `Sliding window` | Post 1 | — |
| `Token-based vs. character-based splitting` | Post 1 | Post 7 |
| `Recursive character/token splitting` | Post 2 | Posts 5.1–5.4 |
| `Chunk boundary problem` | Post 2 | Posts 3, 5.1–5.4 |
| `Semantic chunking` | Post 3 | — |
| `Parent-document retriever` | Post 4.1 | — |
| `Small-to-big retrieval` | Post 4.1 | Post 4.2 |
| `Sentence-window retrieval` | Post 4.2 | — |
| `Contextual Retrieval` | Post 6 | — |

✅ All 11 Module 2 key terms covered across the 11 posts.
