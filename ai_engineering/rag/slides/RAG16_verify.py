"""Re-run every example on the RAG #16 slides (semantic chunking) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG16_verify.py
Installs what it needs on first run: langchain-experimental, langchain-text-splitters, spacy and the
en_core_web_md vectors (from GitHub). The embeddings are spaCy's average word vectors, as the slide says.
"""
import importlib, json, re, subprocess, sys, warnings
from pathlib import Path

MODEL_URL = "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl"
def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("langchain_experimental", "langchain-experimental==0.4.2"), ("langchain_text_splitters", "langchain-text-splitters"),
                 ("spacy", "spacy"), ("en_core_web_md", MODEL_URL)):
    ensure(mod, pkg)
warnings.filterwarnings("ignore")

import inspect, numpy as np, spacy
import importlib.metadata as md
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker, BREAKPOINT_DEFAULTS
from langchain_text_splitters import RecursiveCharacterTextSplitter

S = json.loads(Path(__file__).with_name("RAG16.json").read_text())["slides"]
slide = lambda title: next(s for s in S if s.get("title") == title)
plain = lambda s: re.sub(r"!!(.+?)!!", r"\1", s)
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

nlp = spacy.load("en_core_web_md")
class SpacyEmb(Embeddings):
    """Sentence vector = spaCy's average word vector. Counts what gets embedded."""
    def __init__(self): self.calls, self.texts, self.chars = 0, 0, 0
    def embed_documents(self, texts):
        self.calls += 1; self.texts += len(texts); self.chars += sum(map(len, texts))
        return [nlp(t).vector.tolist() for t in texts]
    def embed_query(self, text): return self.embed_documents([text])[0]

ONE = ("Refunds are accepted within 30 days of purchase. After 30 days, refunds need manager approval. "
       "Refunds go back to the original payment method. Store credit is offered when the card has expired. "
       "Partial refunds apply to opened items. Refund requests need the order number. "
       "Refunds over $500 need a second approval. Approved refunds settle within 5 business days.")
LONG = " ".join([
 "Refunds are accepted within 30 days of purchase.", "After 30 days, refunds need manager approval.",
 "Refunds go back to the original payment method.", "Store credit is offered when the card has expired.",
 "Partial refunds apply to opened items.", "Refund requests need the order number.",
 "Refunds over $500 need a second approval.", "Approved refunds settle within 5 business days.",
 "Gift cards are refunded as store credit only.", "Shipping fees are refunded when the item arrived damaged.",
 "Customers attach a photo when they report damage.", "The support team replies to refund requests within one business day.",
 "Refunds for bundles are split across the items in the bundle.", "A restocking fee of 10% applies to large appliances.",
 "Refunds for subscriptions cover the unused months only.", "Cancelled subscriptions stay active until the period ends.",
 "Refunds in a different currency use the exchange rate on the refund date.", "Duplicate charges are refunded in full without approval.",
 "Chargebacks pause any open refund request.", "Refund status is shown on the order page.",
 "Customers get an email when a refund is approved.", "Rejected refund requests list the reason.",
 "Customers can appeal a rejected refund once.", "Appeals are reviewed by a team lead within 3 business days."])

# slide 2: how it works (library source and defaults)
sig = inspect.signature(SemanticChunker.__init__).parameters
check("s2: buffer_size=1, percentile, regex (?<=[.?!])\\s+",
      sig["buffer_size"].default == 1 and sig["breakpoint_threshold_type"].default == "percentile"
      and sig["sentence_split_regex"].default == r"(?<=[.?!])\s+")
check("s4: default amounts 95 / 3 / 1.5 / 95", BREAKPOINT_DEFAULTS == {"percentile": 95, "standard_deviation": 3, "interquartile": 1.5, "gradient": 95})
check("s5: min_chunk_size exists, no maximum size setting", "min_chunk_size" in sig and not any(k in sig for k in ("chunk_size", "max_chunk_size")))

# slide 3: the distances and both thresholds
ch = SemanticChunker(SpacyEmb())
dist, _ = ch._calculate_sentence_distances(ch._get_single_sentences_list(ONE))
bars = slide("The default cuts / the top [5%]")["visuals"][0]
check("s3: 8 sentences, 7 distances match the bars", len(dist) == 7 and [f"{d:.3f}" for d in dist] == [r["text"] for r in bars["rows"]])
p95, sd3 = np.percentile(dist, 95), np.mean(dist) + 3 * np.std(dist)
check("s3: threshold lines at the 95th percentile and mean + 3 x std", abs(p95 - bars["lines"][0]["value"]) < 5e-4 and abs(sd3 - bars["lines"][1]["value"]) < 5e-4)
check("s3: only gap 5-6 is above the 95th percentile; nothing above mean + 3 x std",
      [i for i, d in enumerate(dist) if d > p95] == [4] and not any(d > sd3 for d in dist))
default = SemanticChunker(SpacyEmb()).split_text(ONE)
check("s3/s4: default cuts after sentence 5", len(default) == 2 and default[0].endswith("Partial refunds apply to opened items."))

# slide 4: each threshold type at its default amount
counts = {t: len(SemanticChunker(SpacyEmb(), breakpoint_threshold_type=t).split_text(ONE)) for t in BREAKPOINT_DEFAULTS}
grad = SemanticChunker(SpacyEmb(), breakpoint_threshold_type="gradient").split_text(ONE)
check("s4: percentile 2, gradient 2 (cut after sentence 4), standard_deviation 1, interquartile 1",
      counts == {"percentile": 2, "gradient": 2, "standard_deviation": 1, "interquartile": 1}
      and grad[0].endswith("Store credit is offered when the card has expired."))
d = np.array(dist)
q1, q3 = np.percentile(d, [25, 75])
check("s4: interquartile is mean + 1.5 x IQR", abs(SemanticChunker(SpacyEmb(), breakpoint_threshold_type="interquartile")._calculate_breakpoint_threshold(dist)[0] - (d.mean() + 1.5 * (q3 - q1))) < 1e-12)

# slide 5: no size cap, then the recursive cap
sd = SemanticChunker(SpacyEmb(), breakpoint_threshold_type="standard_deviation").split_text(LONG)
check("s5: 24 sentences, 1,227 characters, one chunk", len(ch._get_single_sentences_list(LONG)) == 24 and len(LONG) == 1227 and sd == [LONG])
cap = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0, separators=["\n\n", "\n", ". ", " ", ""], keep_separator="end")
capped = [piece for c in sd for piece in cap.split_text(c)]
shown = slide("No [size] cap")["visuals"][1]["chunks"]
check("s5: capped to 465, 479, 281 characters, each ending on a full sentence",
      [len(c) for c in capped] == [int(c["meta"]) for c in shown] == [465, 479, 281] and all(c.endswith(".") for c in capped))
check("s5: shown excerpts match the starts and ends", all(c.startswith(s["text"].split("…")[0].strip()) and c.endswith(s["text"].split("…")[-1].strip())
      for c, s in zip(capped, shown)))

# slide 6: the sentence regex
sents = ch._get_single_sentences_list("For refunds over $500, e.g. laptops, ask Dr. Patel. She approves them within 2 days.")
check("s6: regex splits after e.g. and Dr.", sents == [plain(c) for c in slide("Sentences come / from a [regex]")["visuals"][0]["chunks"]])
check("s6: no . ? ! means one sentence", len(ch._get_single_sentences_list("so the refund window is thirty days and after that you need approval")) == 1)

# slide 7: what finding the cuts costs
e = SpacyEmb(); SemanticChunker(e).split_text(LONG)
check("s7: 24 sentences, 24 embedding inputs, 3,551 chars embedded (2.9x)", e.calls == 1 and e.texts == 24 and e.chars == 3551 and round(e.chars / len(LONG), 1) == 2.9)

# the 95th percentile cuts about 5% of gaps, whatever the embeddings
rng = np.random.default_rng(0)
check("s3: about 1 gap in 20 gets cut (random distances)", [int((x > np.percentile(x, 95)).sum()) for x in (rng.random(n - 1) for n in (21, 41, 101))] == [1, 2, 5])

# slide 9: the package warning
w = subprocess.run([sys.executable, "-W", "always", "-c", "import langchain_experimental.text_splitter"], capture_output=True, text=True).stderr
check("s9: langchain-experimental 0.4.2 warns it is being sunset", md.version("langchain-experimental") == "0.4.2"
      and "is being sunset and is no longer actively maintained" in w)

# slide 10: the config runs and gives the same chunks as slide 5
code = slide("Put it all / [together]")["visuals"][0]["code"]
scope = {"SemanticChunker": SemanticChunker, "RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter, "embeddings": SpacyEmb(), "text": LONG}
exec(code, scope)
check("s10: config runs and returns the 3 capped chunks", scope["chunks"] == capped)

print("langchain-experimental", md.version("langchain-experimental"), "| spacy", spacy.__version__, "| en_core_web_md", md.version("en_core_web_md"))
print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
