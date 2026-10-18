# Pillar 2 — Content Calendar: Module 8 (Evaluation)

**Source:** `RAG_Curriculum (1).md` → Module 8
**Rule:** 1 concept = 1 post. Every Module 8 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 8 has 7 concepts → 7 posts.**
**Key terms to cover (16):** `Recall@k` · `Precision@k` · `MRR (Mean Reciprocal Rank)` · `nDCG (normalized Discounted Cumulative Gain)` · `Faithfulness` · `Answer relevance` · `Context precision` · `Context recall` · `RAGAS` · `Golden dataset` · `LLM-as-judge` · `Synthetic Q&A generation` · `Regression testing` · `Online metrics` · `Offline metrics` · `Human-in-the-loop evaluation`

---

## Post 1 — Two layers you must measure separately: retrieval vs. generation metrics

**Concept:** Retrieval-only metrics vs. end-to-end generation metrics.

**Angle:** "Our RAG is 80% good" is meaningless until you say *which half*. A RAG system can retrieve perfectly and still answer badly — or answer well despite weak retrieval (luck). Measure them as two layers. **Retrieval** asks "did the right documents come back, and high up?" **Generation** asks "given that context, was the answer faithful and on-point?" Define the classic ranking metrics, then the two generation metrics that anchor everything later.

**Key terms covered here:**
- `Recall@k` *(primary)* — of all relevant docs, what fraction appear in the top-k. Did we get the right docs *at all*?
- `Precision@k` *(primary)* — of the top-k returned, what fraction are actually relevant. How much noise?
- `MRR (Mean Reciprocal Rank)` *(primary)* — averages 1/(rank of first relevant hit); rewards putting a correct doc *near the top*.
- `nDCG (normalized Discounted Cumulative Gain)` *(primary)* — rank-aware quality with graded relevance, discounting hits further down the list.
- `Faithfulness` *(primary)* — is every claim in the answer *supported by the retrieved context* (no hallucination)? A property of answer-vs-context.
- `Answer relevance` *(primary)* — does the answer actually *address the user's question*? A property of answer-vs-query.

**Senior-level tie-in:** the module bar, half one — faithfulness ≠ answer relevance: an answer can be perfectly faithful to the context yet not address the question (relevant-but-unfaithful and faithful-but-irrelevant are *different* failures needing *different* fixes).

---

## Post 2 — The thing you can't skip: building a golden dataset from scratch

**Concept:** Building a labeled evaluation/golden dataset.

**Angle:** Every metric in Post 1 needs ground truth to score against. That's the golden dataset, and building it is unglamorous but decisive. Walk the from-scratch process: mine real user queries (or draft representative ones), retrieve/label the relevant chunks, write reference answers, and have humans review — covering the easy, hard, and adversarial cases so the set reflects reality, not wishful thinking.

**Key terms covered here:**
- `Golden dataset` *(primary)* — a curated, labeled set of queries paired with their relevant documents and/or reference answers; the ground truth all offline metrics are computed against.
- `Human-in-the-loop evaluation` *(primary)* — humans labeling relevance and judging answers, both to build the golden set and to spot-audit automated scores.

**Senior-level tie-in:** the module bar, half two — describe it concretely: collect real queries → retrieve candidate chunks → humans label relevance + write reference answers → review for coverage across query types → version it. Start with 50–100 high-quality examples, not thousands of noisy ones.

---

## Post 3 — Faster but biased: synthetic eval-set generation

**Concept:** Synthetic eval-set generation and its biases.

**Angle:** Hand-labeling is slow, so teams bootstrap a dataset by prompting an LLM to read documents and generate Q&A pairs. It's a legitimate accelerant — but a trap if trusted blindly. Synthetic questions tend to be phrased like the source text (unlike real messy user queries), skew toward extractive/easy lookups, and inherit the generator's blind spots. Use it to *seed*, then correct with human review.

**Key terms covered here:**
- `Synthetic Q&A generation` *(primary)* — using an LLM to auto-create query→answer pairs from your corpus to bootstrap an eval set at scale.
- `Golden dataset` *(reinforced)* — synthetic data is a fast first draft of the golden set, not a replacement for human-validated ground truth.

**Senior-level tie-in:** name the biases out loud — vocabulary overlap with sources, easy-question skew, and missing the adversarial/ambiguous queries real users send; mitigate by paraphrasing, mixing difficulty, and human-auditing a sample.

---

## Post 4 — Scoring quality at scale: LLM-as-judge & the RAGAS metrics

**Concept:** LLM-as-judge evaluation and its failure modes.

**Angle:** You can't hand-score thousands of answers per pipeline change, so you delegate judging to an LLM — the engine behind frameworks like RAGAS. It scores faithfulness, answer relevance, and the retrieval-quality pair context precision/recall automatically. Powerful, but it has real failure modes: position/verbosity/self-preference bias and shaky calibration. Trust it for *trends*, validate against humans for *truth*.

**Key terms covered here:**
- `LLM-as-judge` *(primary)* — prompting an LLM to score outputs (faithfulness, relevance, etc.) as an automated stand-in for human raters.
- `RAGAS` *(primary)* — a RAG-eval framework that packages LLM-as-judge metrics (faithfulness, answer relevance, context precision/recall) into a reference-light pipeline.
- `Context precision` *(primary)* — of the retrieved context, how much is actually relevant/used (signal-to-noise of retrieval), judged by the LLM.
- `Context recall` *(primary)* — did retrieval surface *all* the context needed to answer, measured against the reference answer.
- `Faithfulness` *(reinforced)* — here operationalized: the judge checks each answer claim against the retrieved context.
- `Answer relevance` *(reinforced)* — here operationalized: the judge scores how well the answer addresses the query.

**Senior-level tie-in:** know the failure modes cold — verbosity/position/self-preference bias and poor calibration — so you anchor LLM-judge scores to a human-labeled subset rather than treating them as absolute truth.

---

## Post 5 — Stop shipping silent regressions: regression testing for RAG

**Concept:** Regression testing pipelines for RAG changes.

**Angle:** RAG is a chain of coupled choices — swap the embedding model, retune chunking, change the prompt, and you can fix one query type while silently breaking three others. Without a gate, you find out from users. The fix: run every candidate change against the golden set and compare metrics to the baseline *before* it ships, treating an eval drop like a failing unit test.

**Key terms covered here:**
- `Regression testing` *(primary)* — automatically re-running the eval suite on each change and blocking merges that degrade key metrics versus the baseline.
- `Golden dataset` *(reinforced)* — the fixed benchmark regression runs execute against, so score deltas are comparable across changes.

**Senior-level tie-in:** wire it into CI — a pipeline change that lowers Recall@k or faithfulness beyond a threshold fails the build; this is what turns "we think it's better" into "the numbers say so."

---

## Post 6 — Lab vs. reality: online vs. offline evaluation signals

**Concept:** Online vs. offline evaluation signals.

**Angle:** Offline metrics (against the golden set) are reproducible and fast but only as good as your dataset — they can't capture everything real users do. Online metrics come from production behavior and reflect reality but are noisy, lagging, and confounded. Mature teams use offline to gate changes pre-ship and online to confirm the win post-ship. Neither alone is enough.

**Key terms covered here:**
- `Offline metrics` *(primary)* — eval computed against the golden dataset before deployment (Recall@k, faithfulness, RAGAS scores); reproducible, fast, gating.
- `Online metrics` *(primary)* — real-user signals in production: click-through on citations, thumbs up/down, escalation/deflection rate; reflect true value but are noisy and delayed.

**Senior-level tie-in:** map the loop — offline to *decide what ships*, online to *validate it moved the real needle*; a change that wins offline but tanks thumbs-up online means your golden set is missing something.

---

## Post 7 — The average is lying to you: query-type segmentation

**Concept:** Query-type segmentation in evaluation.

**Angle:** A single headline number hides where you're failing. An 85% aggregate can mean you nail factual lookups but collapse on multi-hop, comparative, or time-sensitive queries — exactly the ones that matter most. Segment every metric by query type and you turn one vague score into a prioritized fix-list.

**Key terms covered here:**
- `Recall@k` *(reinforced)* — reported *per query type*, it exposes that retrieval is fine for lookups but failing on multi-hop/comparative queries.
- `Faithfulness` *(reinforced)* — segmented, it reveals answer-quality cliffs on specific query classes an average would mask.

**Senior-level tie-in:** build the golden set *with* query-type labels so segmentation is free; the senior move is reporting a metrics-by-segment table, not a single number, and attacking the worst segment first.

---

## Coverage check (all 16 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Recall@k` | Post 1 | Post 7 |
| `Precision@k` | Post 1 | — |
| `MRR (Mean Reciprocal Rank)` | Post 1 | — |
| `nDCG (normalized Discounted Cumulative Gain)` | Post 1 | — |
| `Faithfulness` | Post 1 | Posts 4, 7 |
| `Answer relevance` | Post 1 | Post 4 |
| `Context precision` | Post 4 | — |
| `Context recall` | Post 4 | — |
| `RAGAS` | Post 4 | — |
| `LLM-as-judge` | Post 4 | — |
| `Golden dataset` | Post 2 | Posts 3, 5 |
| `Human-in-the-loop evaluation` | Post 2 | — |
| `Synthetic Q&A generation` | Post 3 | — |
| `Regression testing` | Post 5 | — |
| `Online metrics` | Post 6 | — |
| `Offline metrics` | Post 6 | — |

✅ All 16 Module 8 key terms covered across the 7 posts.
