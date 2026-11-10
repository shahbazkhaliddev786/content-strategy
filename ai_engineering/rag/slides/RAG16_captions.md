Status: approved by Shahbaz 10 Nov 2026 (built as the format v3 test run)

## LinkedIn (1086 chars)

Semantic chunking cuts where the meaning jumps between sentences. With LangChain's defaults, it also cuts documents that stay on one topic.

SemanticChunker cuts wherever the distance between neighbouring sentence groups is above the 95th percentile of all those distances. A percentile is relative, so about the top 5% of gaps get cut, whether the topic changes or not. On 8 sentences about refunds, it cut once. With breakpoint_threshold_type="standard_deviation" (mean + 3 × std), it didn't cut at all.

Two more defaults to know:
• There's no maximum chunk size, only min_chunk_size. Cap it with a recursive splitter afterwards.
• Finding the cuts embeds about 3x your text at ingest, before a single chunk is indexed.

A 2024 study from Vectara and UW–Madison found the extra compute "not justified by consistent performance gains" over fixed-size chunking.

The slides show the real distances, a fix for each default, and one config with all of them.

Have you measured semantic chunking against fixed-size on your own questions? What did you find?

#AIEngineering #RAG #LangChain

## Instagram

Semantic chunking cuts where the meaning jumps between sentences. With LangChain's defaults, it also cuts documents that stay on one topic.

SemanticChunker cuts wherever the distance between neighbouring sentence groups is above the 95th percentile of all those distances. A percentile is relative, so about the top 5% of gaps get cut, whether the topic changes or not. On 8 sentences about refunds, it cut once. With breakpoint_threshold_type="standard_deviation" (mean + 3 × std), it didn't cut at all.

Two more defaults to know:
• There's no maximum chunk size, only min_chunk_size. Cap it with a recursive splitter afterwards.
• Finding the cuts embeds about 3x your text at ingest, before a single chunk is indexed.

A 2024 study from Vectara and UW–Madison found the extra compute "not justified by consistent performance gains" over fixed-size chunking.

The slides show the real distances, a fix for each default, and one config with all of them.

Have you measured semantic chunking against fixed-size on your own questions? What did you find?

#AIEngineering #RAG #LangChain #SemanticChunking #LLM

## Facebook

Semantic chunking cuts where the meaning jumps between sentences. With LangChain's defaults, it also cuts documents that stay on one topic. The slides show why, with real distances and a fix for each default.

Have you compared it with fixed-size chunking on your own data?

#RAG #AIEngineering

## X thread

Tweet 1 (140 chars):
Semantic chunking cuts where the meaning jumps between sentences.

With LangChain's defaults, it also cuts documents that stay on one topic.

Tweet 2 (274 chars):
SemanticChunker embeds each sentence with its neighbours, then cuts where the distance to the next group is above the 95th percentile.

That's relative: about the top 5% of gaps get cut, topic change or not. breakpoint_threshold_type="standard_deviation" cuts only outliers.

Tweet 3 (184 chars):
Two more defaults:

• No maximum chunk size, only min_chunk_size. Cap it with a recursive splitter.
• Finding the cuts embeds about 3x your text at ingest, before any chunk is indexed.

Tweet 4 (216 chars):
A 2024 Vectara / UW–Madison study found semantic chunking's extra compute "not justified by consistent performance gains".

Have you measured it against fixed-size chunking on your own questions?

#RAG #AIEngineering

## Document title

Semantic chunking | RAG series

## hooks_log row

| RAG #16 | Cut where the meaning jumps between sentences. | Semantic chunking cuts where the meaning jumps between sentences. | B (claim) |

## Caption shape

B (claim)
