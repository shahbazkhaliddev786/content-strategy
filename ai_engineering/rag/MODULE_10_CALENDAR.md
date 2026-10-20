# Pillar 2 — Content Calendar: Module 10 (Agentic & Advanced RAG)

**Source:** `RAG_Curriculum (1).md` → Module 10
**Rule:** 1 concept = 1 post; a multi-strategy concept = 1 mini-series (one post per strategy, sub-numbered N.1, N.2, …). Every Module 10 key term must be explained across these posts. Key terms may repeat across posts; each post explicitly lists the terms it covers.

**Module 10 has 7 concepts → 8 posts (1 mini-series).**
**Key terms to cover (13):** `Agentic RAG` · `Self-RAG` · `Corrective RAG (CRAG)` · `Multi-hop retrieval` · `Iterative retrieval` · `Adaptive retrieval` · `Tool-use / function calling` · `Verifier/critic agent` · `Grounding verification loop` · `Retrieval-augmented reasoning` · `ReAct (Reason+Act) pattern` · `Plan-and-execute agents` · `Query decomposition`

---

## Post 1 — From fixed pipeline to decision-maker: retrieval as a tool call

**Concept:** Retrieval as an agent tool call (dynamic retrieval decisions).

**Angle:** Everything up to now assumed a fixed pipeline: query in → always retrieve → generate. Agentic RAG breaks that assumption. Retrieval becomes a *tool* the model can choose to call — deciding whether to search, what to search for, and when it has enough. The model reasons, acts (calls retrieval), observes the result, and reasons again. That loop is what turns a pipeline into an agent.

**Key terms covered here:**
- `Agentic RAG` *(primary)* — RAG where an LLM agent dynamically decides when/what/how to retrieve, rather than running a fixed retrieve-then-generate pipeline.
- `Tool-use / function calling` *(primary)* — exposing retrieval (and other capabilities) as callable functions the model can invoke with structured arguments.
- `ReAct (Reason+Act) pattern` *(primary)* — the interleaved loop of Reason → Act (call a tool) → Observe → repeat, letting the model drive multi-step retrieval.

**Senior-level tie-in:** the unlock is *control flow moves into the model* — it can skip, repeat, or reformulate retrieval based on what it sees, which a static pipeline structurally cannot do.

---

## Post 2 — One lookup isn't enough: multi-hop & iterative retrieval

**Concept:** Multi-hop / iterative retrieval for chained reasoning.

**Angle:** Ask "Which hospital employs the doctor who pioneered procedure X?" and single-pass RAG dies: no one chunk contains the answer. You need hop one (who pioneered X?) to *produce* the query for hop two (where do they work?). Break the question down, retrieve iteratively, reason across hops, and synthesize. This is the signature capability of agentic RAG.

**Key terms covered here:**
- `Query decomposition` *(primary)* — splitting a complex question into answerable sub-questions.
- `Multi-hop retrieval` *(primary)* — answering questions that require chaining facts across multiple documents/lookups.
- `Iterative retrieval` *(primary)* — repeated retrieve→reason cycles where each round's output shapes the next query.
- `Retrieval-augmented reasoning` *(primary)* — interleaving retrieval with reasoning so the model's intermediate conclusions drive what it fetches next.

**Senior-level tie-in:** the module bar — sketch the full loop (retrieve → reason → identify the gap → retrieve again → synthesize) and explain *why naive single-pass RAG structurally fails* on multi-hop: it retrieves once off the original query, so the bridge fact needed for hop two is never searched for.

---

## Post 3 — Let it grade itself: self-critique & corrective loops *(mini-series · 2 parts)*

**Concept:** Self-critique and corrective retrieval loops.

**Angle:** What if the system could notice its *own* bad retrieval and fix it? Two named approaches do exactly this. One lets the model emit reflection tokens judging whether retrieved context is relevant and whether its answer is supported. The other grades retrieval quality and, when it's weak, corrects course — re-retrieving or falling back to web search. Both close the quality gap without a human in the loop.

**Series structure:** one post per named approach — Self-RAG judges itself while generating; CRAG grades retrieval and corrects course.

**Senior-level tie-in (series):** these are concrete mechanisms, not vibes — Self-RAG gates on reflection tokens, CRAG gates on an evaluator score; know what each actually measures and when the extra passes are worth the latency.

### Post 3.1 — Self-RAG: the model critiques itself while it writes

**Concept:** Self-RAG — self-reflective retrieval and generation.

**Angle:** A model trained to emit special reflection tokens decides, as it generates, whether it needs to retrieve, whether each retrieved passage is relevant, and whether its own output is supported by the evidence. Those judgments steer retrieval and generation without an external checker.

**Key terms covered here:**
- `Self-RAG` *(primary)* — the model self-reflects during generation (via special tokens) on whether to retrieve, whether context is relevant, and whether its output is supported.

**Senior-level tie-in:** Self-RAG needs a model trained to produce those reflection tokens — you can't switch it on with a prompt on any LLM.

### Post 3.2 — Corrective RAG (CRAG): grade the retrieval, then fix it

**Concept:** CRAG — evaluating retrieved documents and correcting course.

**Angle:** After retrieval, a lightweight evaluator grades the retrieved documents. Confident and relevant → proceed. Low confidence → take corrective action: refine the retrieved knowledge, re-retrieve, or fall back to a broader search such as the web.

**Key terms covered here:**
- `Corrective RAG (CRAG)` *(primary)* — a retrieval-evaluator grades retrieved docs and triggers corrective action (re-retrieve, refine, or fall back to broader search) when confidence is low.

**Senior-level tie-in:** CRAG wraps any existing pipeline without retraining the generator; its quality depends on the evaluator, and every correction adds latency — know the threshold that triggers it.

---

## Post 4 — The smartest retrieval is sometimes none: adaptive retrieval

**Concept:** Adaptive retrieval (deciding retrieval is unnecessary for a given query).

**Angle:** "What's 2+2?" or "Rewrite this politely" needs no document search — yet a naive RAG retrieves anyway, adding latency, cost, and irrelevant context that can *degrade* the answer. Adaptive retrieval decides per query whether to retrieve at all, routing simple/parametric questions straight to generation and reserving retrieval for queries that actually need external knowledge.

**Key terms covered here:**
- `Adaptive retrieval` *(primary)* — dynamically deciding whether (and how much) to retrieve based on the query, skipping retrieval when the model's parametric knowledge suffices.

**Senior-level tie-in:** retrieval isn't free — unnecessary context costs tokens and can inject noise that lowers answer quality; a classifier or the model itself gating retrieval is a real production optimization.

---

## Post 5 — Retrieval is just one tool: tool-augmented RAG

**Concept:** Tool-augmented RAG (retrieval combined with calculators, APIs, code execution).

**Angle:** Once retrieval is a tool (Post 1), add more tools: a calculator for math, an API for live data, a code sandbox for computation. Now "What's our Q3 growth vs. the figures in this report?" means retrieve the report *and* call a calculator. The agent plans a sequence of tool calls and executes them — RAG becomes one capability inside a broader tool-using agent.

**Key terms covered here:**
- `Plan-and-execute agents` *(primary)* — agents that first draft a multi-step plan (which tools, in what order) and then execute it, contrasting with ReAct's step-by-step reactivity.
- `Tool-use / function calling` *(reinforced)* — now spanning retrieval *and* calculators/APIs/code, not retrieval alone.

**Senior-level tie-in:** know the trade between the two agent styles — ReAct (Post 1) adapts step-by-step but can wander; plan-and-execute is more efficient and auditable but less flexible when reality diverges from the plan.

---

## Post 6 — Divide the labor: multi-agent RAG architectures

**Concept:** Multi-agent RAG architectures (specialized retriever agents, verifier agents).

**Angle:** Instead of one model doing everything, split the job across specialized agents: a retriever agent that's great at finding evidence, a verifier/critic agent that checks the draft against sources, maybe a synthesizer that composes the final answer. Separation of concerns improves quality and makes each step independently debuggable — at the cost of more orchestration and latency.

**Key terms covered here:**
- `Verifier/critic agent` *(primary)* — a dedicated agent whose only job is to critique another agent's output (is this answer supported? complete? correct?) and send it back for revision if not.

**Senior-level tie-in:** a separate critic beats self-critique when independence matters — a fresh agent with a narrow verification prompt is less likely to rubber-stamp the generator's mistakes; weigh that against the added cost/latency.

---

## Post 7 — Trust, then verify: post-generation grounding loops

**Concept:** Post-generation grounding verification loops.

**Angle:** The last line of defense against hallucination. After the answer is drafted, a verification pass decomposes it into claims and checks each one against the retrieved sources. If a claim isn't supported, the loop rejects the answer and triggers a fix — re-retrieve, regenerate, or strip the unsupported claim. This is Module 7's citation-checking promoted into a closed feedback loop.

**Key terms covered here:**
- `Grounding verification loop` *(primary)* — a post-generation cycle that verifies each answer claim against sources and loops back to correct/regenerate when verification fails.
- `Verifier/critic agent` *(reinforced)* — typically the agent that runs the verification step inside this loop.

**Senior-level tie-in:** this is how you get near-zero unsupported claims — verification as a *gate* (block/revise on failure), not a passive score; budget for the extra pass on high-stakes answers and skip it where latency rules.

---

## Coverage check (all 13 terms accounted for)

| Key term | Primary post | Also appears in |
|---|---|---|
| `Agentic RAG` | Post 1 | — |
| `Tool-use / function calling` | Post 1 | Post 5 |
| `ReAct (Reason+Act) pattern` | Post 1 | — |
| `Multi-hop retrieval` | Post 2 | — |
| `Iterative retrieval` | Post 2 | — |
| `Query decomposition` | Post 2 | — |
| `Retrieval-augmented reasoning` | Post 2 | — |
| `Self-RAG` | Post 3.1 | — |
| `Corrective RAG (CRAG)` | Post 3.2 | — |
| `Adaptive retrieval` | Post 4 | — |
| `Plan-and-execute agents` | Post 5 | — |
| `Verifier/critic agent` | Post 6 | Post 7 |
| `Grounding verification loop` | Post 7 | — |

✅ All 13 Module 10 key terms covered across the 8 posts.
