# RAG #14 — Fixed-size chunking: the simplest cut (and the vocabulary everything builds on)

- Status: approved by Shahbaz on Oct 31 2026. Rubric review passed on the second pass (stop_power 4, topic 4, insight 4, proof 3, voice 3, structure 4, mobile 3, standalone 4, save-worthy 4).
- Canva design: DAHZkN_7xHg, already built and saved (6 slides). Reuse it as is.
- Post type: mechanism (opened on a failure) · caption shape: B (claim)
- The daily run posts this file verbatim: no rewriting, no new review.

## Slides
1. Kicker: RAG CHUNKING · FIXED-SIZE + OVERLAP — Hook: Where did the refund [rule] go?
2. Where it [breaks] — A 500-token window slices every 500 tokens, wherever it lands. / A refund rule starts at token 480 and ends at 530. / 20 tokens land in chunk one, 30 in chunk two. Neither chunk holds the whole rule.
3. Add [overlap] — Overlap repeats the tail of one chunk at the head of the next. / Size 500, overlap 100: each window starts 400 tokens after the last. / The rule at 480–530 now sits whole in chunk two.
4. Measure in [tokens] — Size is measured in characters or tokens. / Characters are simpler; tokens match what the embedding model reads. / By default, all-MiniLM-L6-v2 truncates input past 256 word pieces, so the rest of a longer chunk is never embedded.
5. What it [costs] — Overlap re-embeds the shared tokens. Size 500 with overlap 100 stores up to 1.25 times your corpus. / A sentence longer than the overlap can still be split in every chunk. / Keep it as the baseline to beat.
6. [Cheat] sheet — • Size in the embedder's own tokens / • Chunk ≤ the model's max input / • Overlap ≥ longest span to keep whole / • Storage grows up to size ÷ stride / • The baseline for every smarter splitter

## LinkedIn caption
```
Fixed-size chunking with overlap comes with one guarantee: any fact shorter than the overlap lands whole in at least one chunk.

With size 500 and overlap 100, a 50-token refund rule straddling the cut at token 500 still sits complete in the second chunk.

Two practical details: count size in your embedding model's tokens (by default, all-MiniLM-L6-v2 truncates anything past 256 word pieces), and budget for storage, since overlap 100 on size 500 stores up to 1.25 times your corpus.

The last slide is a 5-line cheat sheet.

What chunk size and overlap are you running in production, and how did you pick them?

Tomorrow: recursive splitting, which cuts along the document's own structure.

#RAG #AIEngineering #LLM
```

## Instagram caption
```
Fixed-size chunking with overlap comes with one guarantee: any fact shorter than the overlap lands whole in at least one chunk.

With size 500 and overlap 100, a 50-token refund rule straddling the cut at token 500 still sits complete in the second chunk.

Two practical details: count size in your embedding model's tokens (by default, all-MiniLM-L6-v2 truncates anything past 256 word pieces), and budget for storage, since overlap 100 on size 500 stores up to 1.25 times your corpus.

The last slide is a 5-line cheat sheet.

What chunk size and overlap are you running in production, and how did you pick them?

Tomorrow: recursive splitting, which cuts along the document's own structure.

#RAG #AIEngineering #LLM #MachineLearning
```

## Facebook caption
```
Fixed-size chunking cuts your documents every N tokens, wherever the cut lands. Overlap keeps a fact at the seam in one piece, as long as the fact fits inside the overlap.

What chunk size are you running, and why? #RAG
```

## X thread
1. `Where did the refund rule go? Fixed-size chunking cut it at token 500. Overlap fixes that, and it comes with a guarantee.` (slide 1 image)
2. `Size 500, overlap 100: each window starts 400 tokens after the last. A rule spanning tokens 480–530 now sits whole in the second chunk. Any span up to the overlap length always lands whole in some chunk.`
3. `Count size in your embedding model's tokens. By default, all-MiniLM-L6-v2 truncates input past 256 word pieces, so the rest of a longer chunk is never embedded.`
4. `Overlap costs storage: size 500 with overlap 100 stores up to 1.25× your corpus. Fixed-size chunking is the baseline every smarter splitter has to beat. What size and overlap do you run? #RAG #LLM`

## hooks_log row (append after posting)
`| RAG #14 | Where did the refund rule go? | Fixed-size chunking with overlap comes with one guarantee: any fact shorter than the overlap lands whole in at least one chunk. | B (claim) |`

## Sources (not posted)
- all-MiniLM-L6-v2 model card: "By default, input text longer than 256 word pieces is truncated." — https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- Overlap guarantee (derived): with size S and overlap O the stride is S − O; any span of length ≤ O lies wholly inside some window. Storage factor ≤ S ÷ (S − O) = 1.25.
