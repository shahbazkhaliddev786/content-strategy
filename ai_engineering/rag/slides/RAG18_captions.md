Status: draft (not posted 13 Nov 2026: second rubric review returned revise; its fixes are applied here and need Shahbaz's approval)

## LinkedIn (1190 chars)

Sentence-window retrieval in LlamaIndex needs MetadataReplacementPostProcessor, or the model gets one bare sentence.
Here: "Refunds over $500 follow a separate rule.", with the approver cut off.

In LlamaIndex, SentenceWindowNodeParser embeds each sentence alone and stores 3 sentences on each side (window_size=3) in the node's metadata, outside the embedding. The window stays in metadata until MetadataReplacementPostProcessor swaps it into the node text. Without that step, the model gets the bare sentence.

The run used Part 1's support handbook. The answer, "They need a second approval from the finance team.", sits right after the top hit, inside its window.

Two more things to watch:
• A window stops only at the edge of its document, so a Shipping hit pulled in the Warranty heading.
• Nearby hits overlap. At similarity_top_k=4, four windows came to 1,438 characters, more than the 1,360-character handbook.

The slides have the real outputs, a fix for each and a config for the postprocessor and heading fixes.

How much context do you hand the model around a hit: a few sentences, a token budget or the whole section?

Tomorrow: chunking code

#AIEngineering #RAG #LlamaIndex

## Instagram

Sentence-window retrieval in LlamaIndex needs MetadataReplacementPostProcessor, or the model gets one bare sentence.
Here: "Refunds over $500 follow a separate rule.", with the approver cut off.

In LlamaIndex, SentenceWindowNodeParser embeds each sentence alone and stores 3 sentences on each side (window_size=3) in the node's metadata, outside the embedding. The window stays in metadata until MetadataReplacementPostProcessor swaps it into the node text. Without that step, the model gets the bare sentence.

The run used Part 1's support handbook. The answer, "They need a second approval from the finance team.", sits right after the top hit, inside its window.

Two more things to watch:
• A window stops only at the edge of its document, so a Shipping hit pulled in the Warranty heading.
• Nearby hits overlap. At similarity_top_k=4, four windows came to 1,438 characters, more than the 1,360-character handbook.

The slides have the real outputs and a fix for each.

How much context do you hand the model around a hit: a few sentences, a token budget or the whole section?

Tomorrow: chunking code

#AIEngineering #RAG #LlamaIndex #Chunking #VectorSearch

## Facebook

Sentence-window retrieval embeds each sentence alone, then hands the model the sentences around the hit.
In a real run, the top hit for "Who has to approve refunds over $500?" was "Refunds over $500 follow a separate rule." The answer sat in the next sentence, which the window included.

How much context do you hand the model around a hit?

#RAG #AIEngineering

## X thread

Tweet 1 (211 chars):
Sentence-window retrieval embeds each sentence alone, then hands the model the sentences around the hit.

In LlamaIndex, that window lives in metadata. MetadataReplacementPostProcessor swaps it in at query time.

Tweet 2 (237 chars):
A real run: "Who has to approve refunds over $500?"

Top hit: "Refunds over $500 follow a separate rule."

The answer is the next sentence: "They need a second approval from the finance team." The window (3 sentences each side) holds it.

Tweet 3 (242 chars):
Two defaults to watch:

• A window stops only at the edge of its document, so a Shipping hit pulled in the Warranty heading. Split on headings first.
• Nearby hits overlap: 4 windows = 1,438 characters, more than the 1,360-character handbook.

Tweet 4 (139 chars):
Drop hits whose sentence already sits in a higher-ranked window.

How much context do you hand the model around a hit?

#RAG #AIEngineering

## Document title

Sentence-window retrieval | RAG series

## hooks_log row

| RAG #18 | Sentence windows ignore headings and overlap: at top_k=4, they sent more text than the whole handbook. | Sentence-window retrieval in LlamaIndex needs MetadataReplacementPostProcessor, or the model gets one bare sentence. | B (claim) |

## Caption shape

B (claim)
