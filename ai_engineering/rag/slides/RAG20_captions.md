Status: posted 17 Nov 2026 (rubric review: 1st returned revise (slide 6 header-cost overclaim, "X, not Y" cheat-sheet row, hook pattern repeated #19); fixes applied; 2nd review passed, minor fixes applied)

## LinkedIn

When chunking tables for RAG, a 300-character split stripped the column names from 12 of 18 rows.
Keep whole rows, and put the table's title and header on top of every chunk.

An 18-row Markdown price table went through LangChain's RecursiveCharacterTextSplitter at chunk_size=300. The title landed alone in chunk 1 and the header in chunk 2. BM25 search for Frankfurt's cold-tier egress price found the right chunk, but nothing in it said which number was the egress price.

From the cheat sheet:
• Title and header rows on top of every chunk, with rows for the same key kept together.
• Docling's HybridChunker has repeat_table_header=True by default. With its Markdown table serializer, the caption stayed in the first chunk only (docling-core 2.107.1).
• Totals and rankings across rows need every row: load the table into a database and use Text-to-SQL.

The slides show each splitter's real chunks and a short Python chunker that groups rows by key.

What do you do with tables wider than your chunk size?

Tomorrow: chunking legal documents

#AIEngineering #RAG #Chunking

## Instagram

When chunking tables for RAG, a 300-character split stripped the column names from 12 of 18 rows.
Keep whole rows, and put the table's title and header on top of every chunk.

An 18-row Markdown price table went through LangChain's RecursiveCharacterTextSplitter at chunk_size=300. The title landed alone in chunk 1 and the header in chunk 2. BM25 search for Frankfurt's cold-tier egress price found the right chunk, but nothing in it said which number was the egress price.

From the cheat sheet:
• Title and header rows on top of every chunk, with rows for the same key kept together.
• Docling's HybridChunker has repeat_table_header=True by default. With its Markdown table serializer, the caption stayed in the first chunk only (docling-core 2.107.1).
• Totals and rankings across rows need every row: load the table into a database and use Text-to-SQL.

The slides show each splitter's real chunks and a short Python chunker that groups rows by key.

What do you do with tables wider than your chunk size?

Tomorrow: chunking legal documents

#AIEngineering #RAG #Chunking #LangChain #Docling

## Facebook

Chunking tables for RAG: keep whole rows and repeat the header row in every chunk.
In a test, a 300-character split left a price row as 0.005, 0.12 and 90 with no column names, so nothing said which number was the egress price.

What do you do with tables wider than your chunk size?

#RAG #AIEngineering

## X thread

Tweet 1 (255 chars):
Chunking tables for RAG: split by whole rows and repeat the header row in every chunk.

A 300-character split of an 18-row price table left Frankfurt's cold-tier row as 0.005, 0.12 and 90, with no column names. Nothing said which one was the egress price.

Tweet 2 (252 chars):
LangChain's RecursiveCharacterTextSplitter at chunk_size=300: the title landed alone in chunk 1, the header in chunk 2, and chunks 3 and 4 were bare rows.

The same table as one-line HTML was cut mid-row: Virginia's egress price started the next chunk.

Tweet 3 (250 chars):
Docling's HybridChunker repeats header rows by default (repeat_table_header=True). With its Markdown serializer, the caption stayed in chunk 1 only.

When a row is too wide, it splits the table by columns, and the key column stays in the first split.

Tweet 4 (218 chars):
Totals and rankings across rows need every row, and top-k retrieval returns a few chunks. Load the table into a database and use Text-to-SQL.

What do you do with tables wider than your chunk size?

#RAG #AIEngineering

## Document title

Chunking tables for RAG | RAG series

## hooks_log row

| RAG #20 | 0.005, 0.12 and 90, with no column names: Frankfurt's cold-tier row after a 300-character split. Keep whole rows, with the title and header on every chunk. | When chunking tables for RAG, a 300-character split stripped the column names from 12 of 18 rows. | C (checklist preview) |

## Caption shape

C (checklist preview)
