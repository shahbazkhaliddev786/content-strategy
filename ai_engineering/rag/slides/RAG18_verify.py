"""Re-run every example on the RAG #18 slides (sentence-window retrieval) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG18_verify.py
Installs what it needs on first run: llama-index-core 0.14.25, spacy and the en_core_web_md vectors (from GitHub).
The embeddings are spaCy's average word vectors, as the slide says. The handbook is the one from RAG #17 (Part 1).
"""
import copy, importlib, inspect, json, re, subprocess, sys, warnings
from pathlib import Path

MODEL_URL = "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl"
def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("llama_index.core", "llama-index-core==0.14.25"), ("spacy", "spacy"), ("en_core_web_md", MODEL_URL)):
    ensure(mod, pkg)
warnings.filterwarnings("ignore")

import spacy
import importlib.metadata as md
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.constants import DEFAULT_SIMILARITY_TOP_K
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import MarkdownNodeParser, SentenceWindowNodeParser
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.schema import MetadataMode
import llama_index.core.utils as li_utils

HERE = Path(__file__).parent
S = json.loads((HERE / "RAG18.json").read_text())["slides"]
slide = lambda title: next(s for s in S if s.get("title") == title)
plain = lambda s: re.sub(r"!!(.+?)!!", r"\1", s)
squash = lambda s: re.sub(r"\s+", " ", s.replace("## ", "## ")).strip()
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# Same handbook as RAG #17
HANDBOOK = re.search(r'HANDBOOK = """(.*?)"""', (HERE / "RAG17_verify.py").read_text(), re.S).group(1)

nlp = spacy.load("en_core_web_md")
class SpacyEmb(BaseEmbedding):
    """Sentence vector = spaCy's average word vector."""
    def _get_query_embedding(self, q): return nlp(q).vector.tolist()
    async def _aget_query_embedding(self, q): return self._get_query_embedding(q)
    def _get_text_embedding(self, t): return nlp(t).vector.tolist()
Settings.embed_model = SpacyEmb(); Settings.llm = None
pp = MetadataReplacementPostProcessor(target_metadata_key="window")

def build(window_size=3, markdown_first=False):
    parser = SentenceWindowNodeParser.from_defaults(window_size=window_size)
    if markdown_first:
        nodes = IngestionPipeline(transformations=[MarkdownNodeParser(), parser]).run(documents=[Document(text=HANDBOOK)])
    else:
        nodes = parser.get_nodes_from_documents([Document(text=HANDBOOK)])
    return nodes, VectorStoreIndex(nodes)

REFUND = "Who has to approve refunds over $500?"
CUSTOMS = "Do international orders pay customs fees?"
WARRANTY = "How long do warranty repairs take?"

# ---- versions and defaults (slide 2, cheat sheet, config)
check("llama-index-core 0.14.25", md.version("llama-index-core") == "0.14.25" and "0.14.25" in slide("One sentence in, / a [window] out")["text"])
f = SentenceWindowNodeParser.model_fields
check("window_size default 3, key 'window', 'original_text'", f["window_size"].default == 3 and f["window_metadata_key"].default == "window" and f["original_text_metadata_key"].default == "original_text")
check("sentence splitter is NLTK Punkt", "PunktSentenceTokenizer" in inspect.getsource(li_utils))
check("similarity_top_k default 2", DEFAULT_SIMILARITY_TOP_K == 2)
src = inspect.getsource(SentenceWindowNodeParser.build_window_nodes_from_documents)
check("window excluded from embed and LLM metadata", "excluded_embed_metadata_keys.extend" in src and "excluded_llm_metadata_keys.extend" in src)

nodes, index = build()
check("27 sentence nodes", len(nodes) == 27 and "27 sentence" in slide("The next sentence / held the [answer]")["text"])
check("embedding text leaves the window out", "finance team" not in nodes[3].get_content(metadata_mode=MetadataMode.EMBED))

# ---- slide 3: refund query
hits = index.as_retriever().retrieve(REFUND)
top = hits[0]
s3 = slide("The next sentence / held the [answer]")
check("top hit sentence", top.node.text.strip() == s3["visuals"][0]["chunks"][0]["text"])
check("top hit score 0.903", f"{top.score:.3f}" == s3["visuals"][0]["chunks"][0]["meta"])
check("top hit alone lacks the answer", "finance" not in top.node.text)
win = top.node.metadata["window"]
check("window 363 characters", len(win) == 363 and "363 characters" in s3["visuals"][1]["label"])
shown = plain(s3["visuals"][1]["chunks"][0]).replace("… ", "").replace(" …", "")
check("slide window text is inside the real window", shown in squash(win))
check("window holds the answer", "They need a second approval from the finance team." in win)

# ---- slide 4: no postprocessor
s4 = slide("The window needs / a [postprocessor]")
code4 = s4["visuals"][0]["code"]
raw = index.as_retriever().retrieve(REFUND)[0]
check("retriever returns the bare sentence", repr(raw.node.text) in code4 and "# 363" in code4)
check("LLM view of the node has no window", "finance" not in raw.node.get_content(metadata_mode=MetadataMode.LLM))
after = pp.postprocess_nodes(copy.deepcopy(index.as_retriever().retrieve(REFUND)))
check("postprocessor swaps in the window", after[0].node.text == win)

# ---- slide 5: windows cross headings
s5 = slide("Windows [cross] / headings")
bad = index.as_retriever().retrieve(CUSTOMS)[0].node.metadata["window"]
check("customs: top hit is the customs sentence", "International orders pay customs" in index.as_retriever().retrieve(CUSTOMS)[0].node.text)
check("customs window ends in the Warranty heading", squash(bad).endswith("## Warranty Every device has a 1-year warranty from the delivery date."))
for part in plain(s5["visuals"][0]["chunks"][0]).split(" … "):
    check(f"bad window shows real text: {part[:30]}", part.strip("… ").strip() in squash(bad))
nodes_md, index_md = build(markdown_first=True)
good = index_md.as_retriever().retrieve(CUSTOMS)[0].node.metadata["window"]
check("MarkdownNodeParser first: no Warranty in window", "Warranty" not in good)
check("good window ends with Damaged parcels sentence", squash(good).endswith("Damaged parcels are replaced at no cost when the customer sends a photo within 7 days."))
check("good window slide text real", plain(s5["visuals"][1]["chunks"][0]).lstrip("… ") in squash(good))

# ---- slide 6: overlapping windows
s6 = slide("Nearby hits / [repeat] lines")
pos = {n.node_id: i for i, n in enumerate(nodes)}
hits4 = index.as_retriever(similarity_top_k=4).retrieve(WARRANTY)
nums = [pos[h.node.node_id] + 1 for h in hits4]
check("hits are sentences 15, 18, 20, 3", nums == [15, 18, 20, 3] and "15, 18, 20, 3" in s6["visuals"][0]["code"])
total = sum(len(h.node.metadata["window"]) for h in hits4)
check("windows 1,438 > handbook 1,360", total == 1438 and len(HANDBOOK) == 1360 and "1,438" in s6["visuals"][0]["code"] and "1,360" in s6["visuals"][0]["code"])
s18 = nodes[17].text
check("sentence 18 sent 3 times", sum(s18 in h.node.metadata["window"] for h in hits4) == 3)
seen, kept = "", []
for h in hits4:
    if h.node.metadata["original_text"] in seen: continue
    seen += h.node.metadata["window"]; kept.append(h)
kc = sum(len(h.node.metadata["window"]) for h in kept)
check("dedupe: 3 windows, 1,066 characters, answer kept", len(kept) == 3 and kc == 1066 and any("Repairs take about 10 business days." in h.node.metadata["window"] for h in kept) and "1,066" in s6["bullets"][1])

# ---- slide 7: window sizes
s7 = slide("Size the window / in [sentences]")
for opt, w in zip(s7["visuals"][0]["options"], (1, 2, 3)):
    _, idx_w = build(window_size=w)
    t = idx_w.as_retriever().retrieve(REFUND)[0].node.metadata["window"]
    check(f"window_size={w}: {len(t)} characters, answer included", f"{len(t)} characters" in plain(opt["output"]) and "finance team" in t)

# ---- slide 8: storage
s8 = slide("Every node stores / its [window]")
w3 = sum(len(n.metadata["window"]) for n in nodes)
n1, _ = build(window_size=1)
w1 = sum(len(n.metadata["window"]) for n in n1)
check("8,973 and 3,992 stored window characters", w3 == 8973 and w1 == 3992 and "8,973" in s8["visuals"][0]["code"] and "3,992" in s8["visuals"][0]["code"])
check("6.6 times the text", f"{w3 / len(HANDBOOK):.1f}" == "6.6" and "6.6" in s8["bullets"][0])
check("docstore keeps the window", all("window" in d.metadata for d in index.docstore.docs.values()))

# ---- slide 9: the config runs and returns windows
_, index_cfg = build(window_size=2, markdown_first=True)
eng = index_cfg.as_query_engine(similarity_top_k=4, node_postprocessors=[MetadataReplacementPostProcessor(target_metadata_key="window")])
check("config: query engine returns windows", "finance team" in eng.query(REFUND).source_nodes[0].node.text)

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
