# Pillar 2 — Content Calendar: Module 2 (Chunking Strategies)

**Source:** `RAG_Curriculum (1).md` → Module 2
**Rule:** 1 concept = 1 post. Every Module 2 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 2 has 7 concepts → 7 posts.**
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

## Post 4 — Small-to-big: retrieve precise, return rich

**Concept:** Hierarchical / parent-child chunking (small-to-big retrieval).

**Angle:** There's a tension: small chunks retrieve *precisely* (tight embeddings) but give the LLM too little context; big chunks give context but retrieve fuzzily. Small-to-big resolves it — index small, then hand the model the larger parent the match came from. Cover the family of techniques that do this.

**Key terms covered here:**
- `Parent-document retriever` *(primary)* — index small child chunks for matching, but return their larger parent document/section to the LLM.
- `Small-to-big retrieval` *(primary)* — the general pattern: match on small units, expand to bigger context before generation.
- `Sentence-window retrieval` *(primary)* — a specific variant: embed single sentences, then return a window of surrounding sentences around each hit.

**Senior-level tie-in:** this is where you decouple *what you match on* from *what you feed the model* — a defining move of production-grade retrieval.

---

## Post 5 — One chunker doesn't fit all: document-type-specific chunking

**Concept:** Document-type-specific chunking — code, tables, legal clauses, conversation transcripts.

**Angle:** A strategy tuned for prose wrecks a codebase. Code has functions and classes; tables have rows; legal docs have numbered clauses; transcripts have turns. The natural unit changes with the document type, and so should the splitter. Walk through each type and its right boundary.

**Key terms covered here:**
- `Recursive character/token splitting` *(reinforced)* — adapt the separator list per type (e.g. split code on function/class boundaries, legal text on clause markers).
- `Chunk boundary problem` *(reinforced)* — type-specific: splitting mid-function or mid-clause is the same failure in a new costume.

**Senior-level tie-in:** directly the module bar — be able to *pick and justify* a chunking strategy per document type on the spot.

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
| `Recursive character/token splitting` | Post 2 | Post 5 |
| `Chunk boundary problem` | Post 2 | Posts 3, 5 |
| `Semantic chunking` | Post 3 | — |
| `Parent-document retriever` | Post 4 | — |
| `Small-to-big retrieval` | Post 4 | — |
| `Sentence-window retrieval` | Post 4 | — |
| `Contextual Retrieval` | Post 6 | — |

✅ All 11 Module 2 key terms covered across the 7 posts.
