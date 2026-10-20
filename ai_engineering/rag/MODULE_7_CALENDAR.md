# Pillar 2 — Content Calendar: Module 7 (Context Construction & Generation)

**Source:** `RAG_Curriculum (1).md` → Module 7
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 7 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 7 has 6 concepts → 10 posts (2 mini-series).**
**Key terms to cover (9):** `Lost-in-the-middle` · `Context window budget` · `Grounded generation` · `Citation enforcement` · `Attribution` · `Abstention` · `Confidence thresholding` · `Prompt template / system prompt design` · `Conflicting evidence resolution`

---

## Post 1 — The context window is a budget, not a bucket

**Concept:** Context window budgeting across system prompt, retrieved chunks, history, query.

**Angle:** Retrieval is done — now you have to *assemble* what the model sees, and the window is finite. The system prompt, retrieved chunks, conversation history, and the user query all compete for the same token budget. Stuff in too many chunks and you crowd out history or blow the limit; too few and you starve the answer. Treat it as explicit allocation, not "dump everything and hope."

**Key terms covered here:**
- `Context window budget` *(primary)* — the fixed token allowance for a request, deliberately partitioned across system prompt, retrieved context, history, and query (plus headroom for the output).

**Senior-level tie-in:** budget top-down — reserve tokens for the answer and system instructions *first*, then spend what's left on the highest-value chunks; more context is not free and not always better (sets up Post 2).

---

## Post 2 — Where you put a chunk changes whether the model reads it

**Concept:** Chunk ordering strategies (relevance-to-position mapping).

**Angle:** Counter-intuitive but well documented: LLMs attend most strongly to the *start* and *end* of a long context and can skim the middle. So two systems with the identical retrieved chunks get different answers depending purely on *order*. The practical move is to place the most relevant chunks at the edges, not bury your best evidence in the middle.

**Key terms covered here:**
- `Lost-in-the-middle` *(primary)* — the empirical tendency of LLMs to use information at the beginning and end of a long context more reliably than information in the middle.
- `Context window budget` *(reinforced)* — ordering is how you spend the budget well: position matters as much as inclusion.

**Senior-level tie-in:** a concrete heuristic — rank by relevance, then interleave so top chunks sit first and last; verify with an eval, because the effect size varies by model and context length.

---

## Post 3 — The prompt that makes the model answer from the docs, not its memory

**Concept:** Prompt templates for grounded generation.

**Angle:** RAG's whole point is answering from *retrieved* evidence, but a model will happily fall back on its parametric memory unless you instruct it not to. The template is where you enforce that: label the context, state "answer only using the context below," and define what to do when the context is silent. Small wording changes here move hallucination rates measurably.

**Key terms covered here:**
- `Prompt template / system prompt design` *(primary)* — the reusable scaffold that slots retrieved chunks, query, and instructions into a consistent structure the model handles reliably.
- `Grounded generation` *(primary)* — generating answers constrained to (and supported by) the retrieved context rather than the model's internal knowledge.

**Senior-level tie-in:** grounding is a *design* property, not a hope — the template must explicitly forbid outside knowledge and define the no-evidence path (which Posts 5–6 build on).

---

## Post 4 — Make it cite its sources (and check that it did)

**Concept:** Citation/attribution enforcement.

**Angle:** "Trust me" isn't acceptable in production. Grounded answers should point to *which* retrieved chunk backs each claim, so users (and you) can verify. Cover how to make the model emit citations (chunk IDs / inline markers) via the template, and — crucially — how to *validate* them post-hoc, because models will cite sources that don't actually support the claim.

**Key terms covered here:**
- `Citation enforcement` *(primary)* — requiring (and validating) that the model attach source references to its claims, e.g. chunk IDs the generation must include.
- `Attribution` *(primary)* — the mapping from a generated statement back to the specific source span that supports it.
- `Grounded generation` *(reinforced)* — citations are how grounding becomes *verifiable* rather than just asserted.

**Senior-level tie-in:** enforcement ≠ asking nicely — the mature pattern is to parse the citations and check each cited chunk actually entails the claim, flagging or dropping unsupported sentences.

---

## Post 5 — Knowing when NOT to answer: abstention design *(mini-series · 3 parts)*

**Concept:** Abstention and refusal design ("I don't know" paths).

**Angle:** The most dangerous RAG failure is a confident answer when retrieval found nothing relevant. A production system needs an explicit "I don't know" path — and it must be a *mechanism*, not a vibe. Walk through concrete triggers: a retrieval-score threshold, an explicit instruction to output a refusal token when the context lacks the answer, or a secondary grounding check that vetoes ungrounded output.

**Series structure:** one post per abstention trigger — before generation (score threshold), during generation (refusal instruction), after generation (grounding check).

**Senior-level tie-in (series):** the module bar — describe a *concrete* mechanism, e.g. "if the top reranker score < τ, or a grounding-verifier call returns 'unsupported,' return the abstention response" — never "the model would probably know not to answer."

### Post 5.1 — Abstain before generating: the score threshold

**Concept:** Abstaining when retrieval confidence is below a threshold.

**Angle:** Before calling the LLM at all, check the evidence: if the top retrieval or reranker score is below a threshold τ, return "I don't know" instead of generating. It's the cheapest trigger — no generation call is wasted — but τ has to be calibrated on real queries, and scores aren't equally reliable across query types.

**Key terms covered here:**
- `Abstention` *(primary)* — the system deliberately declining to answer (returning "I don't know" / a refusal) when evidence is insufficient.
- `Confidence thresholding` *(primary)* — gating the answer on a measurable signal (top retrieval score, reranker score, or a grounding-check verdict) below which the system abstains instead of generating.

**Senior-level tie-in:** set τ from an eval set, not a guess — too high and you refuse answerable questions, too low and empty retrieval still reaches the model.

### Post 5.2 — Abstain while generating: the refusal instruction

**Concept:** Instructing the model to emit a fixed refusal when the context lacks the answer.

**Angle:** Tell the model explicitly: if the context doesn't contain the answer, reply with an exact refusal phrase (e.g. "I don't know based on the provided documents"). Because the phrase is fixed, your code can detect it and handle it consistently.

**Key terms covered here:**
- `Abstention` *(reinforced)*
- `Prompt template / system prompt design` *(reinforced)* — the refusal path is defined in the template.

**Senior-level tie-in:** cheap and easy, but it depends on the model following instructions — models can still answer from memory instead of refusing, so don't make it your only line of defense.

### Post 5.3 — Abstain after generating: the grounding-check veto

**Concept:** Vetoing ungrounded answers with a verification step.

**Angle:** Generate the answer, then run a second check: is every claim actually supported by the retrieved context? If the verifier says "unsupported," discard the answer and return the abstention response. The most reliable trigger — it judges the output itself — at the cost of an extra model call and added latency.

**Key terms covered here:**
- `Confidence thresholding` *(reinforced)* — the grounding-check verdict is the signal being thresholded.
- `Grounded generation` *(reinforced)* — what the check verifies.

**Senior-level tie-in:** in production, stack triggers — a cheap threshold first, a grounding check for high-stakes answers. This becomes a full feedback loop in Module 10.

---

## Post 6 — When your own sources disagree: conflicting-evidence resolution *(mini-series · 3 parts)*

**Concept:** Handling conflicting information across retrieved chunks.

**Angle:** Retrieval often surfaces chunks that contradict each other — an outdated policy next to the current one, or two sources stating different numbers. If you say nothing, the model picks arbitrarily. Define a resolution policy: prefer newer/more-authoritative sources via metadata, surface the conflict to the user, or present both with their attributions rather than silently merging them.

**Series structure:** one post per resolution policy.

**Senior-level tie-in (series):** don't let the model silently arbitrate — encode the precedence rule (e.g. prefer the chunk with the latest `date` metadata) or expose the disagreement with citations, so resolution is auditable.

### Post 6.1 — Let metadata decide: recency and authority precedence

**Concept:** Resolving conflicts with recency and authority rules.

**Angle:** When two chunks disagree, apply a rule you defined in advance: the newer document wins, or the more authoritative source wins (official policy over a forum post). The rule runs on metadata like `date` and `source`, so it's consistent and auditable — not whatever the model happens to prefer.

**Key terms covered here:**
- `Conflicting evidence resolution` *(primary)* — a defined strategy for reconciling contradictory retrieved chunks (recency/authority precedence, explicit conflict surfacing, or present-both-with-sources).
- `Attribution` *(reinforced)* — the enabler: you can only resolve or surface a conflict if each claim is tied to its source (and its metadata like date/authority).

**Senior-level tie-in:** this only works if documents carry reliable date and source metadata from ingestion — and "newer" isn't always "correct" (a draft can be newer than the approved version).

### Post 6.2 — Say it out loud: surfacing the conflict

**Concept:** Telling the user that the sources disagree.

**Angle:** When no rule can safely pick a winner, don't hide it: the answer states that the sources conflict and what each says, or asks a clarifying question ("Are you asking about the 2024 or the 2025 policy?").

**Key terms covered here:**
- `Conflicting evidence resolution` *(reinforced)* — the surfacing policy.

**Senior-level tie-in:** best when a wrong pick is costly (legal, medical, finance); annoying when used for trivial differences — reserve it for conflicts that change the answer.

### Post 6.3 — Show both sides: present both with attribution

**Concept:** Presenting each conflicting claim with its source.

**Angle:** Give both versions, each with its citation and date ("Policy A (2023) says 30 days; Policy B (2025) says 14 days"), and let the reader judge. Nothing is silently merged into one wrong blended answer.

**Key terms covered here:**
- `Conflicting evidence resolution` *(reinforced)* — the present-both policy.
- `Attribution` *(reinforced)* — each version is tied to its source.

**Senior-level tie-in:** depends entirely on reliable citations (Post 4); without attribution, presenting both just confuses the user.

---

## Coverage check (all 9 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Context window budget` | Post 1 | Post 2 |
| `Lost-in-the-middle` | Post 2 | — |
| `Prompt template / system prompt design` | Post 3 | Post 5.2 |
| `Grounded generation` | Post 3 | Posts 4, 5.3 |
| `Citation enforcement` | Post 4 | — |
| `Attribution` | Post 4 | Posts 6.1, 6.3 |
| `Abstention` | Post 5.1 | Post 5.2 |
| `Confidence thresholding` | Post 5.1 | Post 5.3 |
| `Conflicting evidence resolution` | Post 6.1 | Posts 6.2, 6.3 |

✅ All 9 Module 7 key terms covered across the 10 posts.
