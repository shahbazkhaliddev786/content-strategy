# Pillar 2 — Technical RAG Content Calendars

The master index for Pillar 2 (technical content). Each module of the RAG curriculum is mapped into a standalone content calendar; together they lay out **114 planned posts** (77 concepts, 18 of them expanded into mini-series) that take a reader from RAG foundations to production and agentic systems.

**Source curriculum:** [RAG_Curriculum (1).md](RAG_Curriculum%20%281%29.md)
**Posting order:** [SERIES_ORDER.md](SERIES_ORDER.md) (RAG #01–#114) · **Publish log:** [posted.md](posted.md)

---

## How these calendars work

Every module calendar follows the same contract:

- **1 concept = 1 post** — except when a concept covers several distinct strategies.
- **Multi-strategy concept = 1 mini-series** — one post per strategy, sub-numbered under the original post (`Post 2` → `Post 2.1`, `2.2`, …), often closing with a comparison post. Original post numbers never change, so every existing cross-reference stays valid.
- **Key terms are mapped to posts explicitly**, flagged *primary* (defined in that post) vs. *reinforced* (reused from a post where it was already defined).
- **A key term may appear in multiple posts** — coverage rule: every module key term lands in **≥1** post.
- A post may consist only of *reinforced* terms when its concept has no dedicated new term.
- Each calendar ends with a **coverage-check table** proving every key term is accounted for, and each post carries a **senior-level tie-in** toward that module's bar.

---

## Modules

| Module | Topic | Posts | Mini-series | Key terms | Calendar |
|---|---|---|---|---|---|
| 0 | Prerequisites & Mental Model | 5 | 1: RAG vs. Alternatives | 8 | [MODULE_0_CALENDAR.md](MODULE_0_CALENDAR.md) |
| 1 | Document Ingestion & Parsing | 8 | 2: File Formats, Multi-modal Content | 8 | [MODULE_1_CALENDAR.md](MODULE_1_CALENDAR.md) |
| 2 | Chunking Strategies | 11 | 2: Small-to-Big, Chunking by Doc Type | 11 | [MODULE_2_CALENDAR.md](MODULE_2_CALENDAR.md) |
| 3 | Embeddings | 9 | 1: Embeddings 101 | 13 | [MODULE_3_CALENDAR.md](MODULE_3_CALENDAR.md) |
| 4 | Indexing & Vector Search | 16 | 3: ANN Algorithms, Filtering, Scaling the Index | 15 | [MODULE_4_CALENDAR.md](MODULE_4_CALENDAR.md) |
| 5 | Retrieval Strategies | 12 | 2: Hybrid Fusion, Query Transformation | 15 | [MODULE_5_CALENDAR.md](MODULE_5_CALENDAR.md) |
| 6 | Reranking | 8 | 1: Choosing a Reranker | 6 | [MODULE_6_CALENDAR.md](MODULE_6_CALENDAR.md) |
| 7 | Context Construction & Generation | 10 | 2: Abstention, Conflicting Evidence | 9 | [MODULE_7_CALENDAR.md](MODULE_7_CALENDAR.md) |
| 8 | Evaluation | 7 | — | 16 | [MODULE_8_CALENDAR.md](MODULE_8_CALENDAR.md) |
| 9 | Production Engineering | 10 | 2: Caching, Production Failures | 14 | [MODULE_9_CALENDAR.md](MODULE_9_CALENDAR.md) |
| 10 | Agentic & Advanced RAG | 8 | 1: Self-Correcting RAG | 13 | [MODULE_10_CALENDAR.md](MODULE_10_CALENDAR.md) |
| 11 | Knowledge Graphs & Structured Retrieval | 5 | 1: Hybrid Graph + Vector | 7 | [MODULE_11_CALENDAR.md](MODULE_11_CALENDAR.md) |
| 12 | System Design Practice | 5 | — | 0* | [MODULE_12_CALENDAR.md](MODULE_12_CALENDAR.md) |
| | **Total** | **114** | **18** | **135** | |

\* Module 12 is an integrative capstone — it introduces **no new key terms**; every post reinforces terms from earlier modules.

---

## Status & next steps

✅ **Planning complete** — all 13 module calendars are written and term-coverage verified, including the 18 mini-series (77 → 114 posts).

**Next:** publish daily in the order set by [SERIES_ORDER.md](SERIES_ORDER.md), starting at RAG #01 (Module 0 foundations). The calendars are the outline (concept, angle, key terms, senior-level tie-in per post); each published post is logged in [posted.md](posted.md).
