"""Re-run every example on the RAG #17 slides (parent-document retriever) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG17_verify.py
Installs what it needs on first run: langchain-classic, langchain-text-splitters, llama-index-core, spacy and the
en_core_web_md vectors (from GitHub). The embeddings are spaCy's average word vectors, as the slide says.
"""
import importlib, json, re, subprocess, sys, tempfile, uuid, warnings
from pathlib import Path

MODEL_URL = "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl"
def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("langchain_classic", "langchain-classic==1.0.8"), ("langchain_text_splitters", "langchain-text-splitters"),
                 ("llama_index.core", "llama-index-core==0.14.25"), ("spacy", "spacy"), ("en_core_web_md", MODEL_URL)):
    ensure(mod, pkg)
warnings.filterwarnings("ignore")

import inspect, spacy
import importlib.metadata as md
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.stores import InMemoryStore
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.retrievers.multi_vector import MultiVectorRetriever
from langchain_classic.storage import LocalFileStore

S = json.loads(Path(__file__).with_name("RAG17.json").read_text())["slides"]
slide = lambda title: next(s for s in S if s.get("title") == title)
plain = lambda s: re.sub(r"!!(.+?)!!", r"\1", s)
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

nlp = spacy.load("en_core_web_md")
class SpacyEmb(Embeddings):
    """Sentence vector = spaCy's average word vector."""
    def embed_documents(self, texts): return [nlp(t).vector.tolist() for t in texts]
    def embed_query(self, text): return nlp(text).vector.tolist()

HANDBOOK = """# Customer support handbook

## Refunds
Refunds are accepted within 30 days of purchase. After 30 days, a refund needs manager approval. Refunds go back to the original payment method.
Refunds over $500 follow a separate rule. They need a second approval from the finance team. Finance replies within 2 business days.
Partial refunds apply to opened items. Every refund request needs the order number.

## Shipping
Orders ship within 2 business days. Express shipping arrives in 1 to 2 days. Standard shipping arrives in 3 to 7 days.
Shipping is free on orders over $50. International orders pay customs fees on delivery. Tracking links are emailed when the order ships.
Damaged parcels are replaced at no cost when the customer sends a photo within 7 days.

## Warranty
Every device has a 1-year warranty from the delivery date. The warranty covers manufacturing faults. It does not cover water damage or drops.
Warranty claims need the serial number. Approved claims get a repair or a replacement. Repairs take about 10 business days.
An extended 3-year warranty can be bought within 30 days of delivery.

## Accounts
Customers can change their email address in account settings. Password resets expire after 1 hour. Two-factor login can be turned on in settings.
Closed accounts are deleted after 90 days. Order history is kept for 7 years for tax records.
"""
DOC = Document(HANDBOOK, metadata={"source": "handbook.md"})
W, R = "How long do warranty repairs take?", "Who has to approve refunds over $500?"
child = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0, separators=["\n\n", "\n", ". ", " ", ""], keep_separator="end")
parent = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0, separators=["\n## ", "\n\n", "\n", ". ", " ", ""], keep_separator="start")
def build(ps=parent, **kw):
    vs, st = InMemoryVectorStore(SpacyEmb()), InMemoryStore()
    r = ParentDocumentRetriever(vectorstore=vs, docstore=st, child_splitter=child, parent_splitter=ps, **kw)
    r.add_documents([DOC])
    return r, vs, st
section = lambda d: re.search(r"## (\w+)", d.page_content).group(1)
nkeys = lambda st: len(list(st.yield_keys()))

# versions named on the slides
check("versions: langchain-classic 1.0.8, llama-index-core 0.14.25",
      md.version("langchain-classic") == "1.0.8" and md.version("llama-index-core") == "0.14.25")

# slide 2: how it works (library source)
src = inspect.getsource(ParentDocumentRetriever) + inspect.getsource(MultiVectorRetriever)
check("s2: children carry the parent id in doc_id; ids deduped in rank order; parents from docstore",
      MultiVectorRetriever.model_fields["id_key"].default == "doc_id" and "not in ids" in src and "self.docstore.mget(ids)" in src
      and "self.child_splitter.split_documents" in src and "self.parent_splitter.split_documents" in src)

# slide 3: the real run
r, vs, st = build()
s3 = slide("The parent held / the [answer]")
check("s3: 4 sections, 23 children of up to 100 chars", nkeys(st) == 4 and len(vs.store) == 23
      and max(len(v["text"]) for v in vs.store.values()) <= 100 and "23 children of up to 100 characters" in s3["text"])
hits = vs.similarity_search_with_score(W)
shown = s3["visuals"][0]["chunks"]
check("s3: top 4 children and scores match the slide",
      [(d.page_content, f"{sc:.3f}") for d, sc in hits] == [(c["text"], c["meta"]) for c in shown])
check("s3: none of the 4 children says how long repairs take", not any("Repairs take" in d.page_content for d, _ in hits))
out = r.invoke(W)
check("s3: first parent returned is Warranty, 347 chars, and holds the answer",
      section(out[0]) == "Warranty" and len(out[0].page_content) == 347 and "Repairs take about 10 business days." in out[0].page_content
      and "347 characters" in s3["visuals"][1]["label"])

# slide 4: parent_splitter=None
sig = ParentDocumentRetriever.model_fields
s4 = slide("No parent splitter: / the whole [document]")["visuals"][0]["options"]
r0, vs0, st0 = build(None)
outs0 = [r0.invoke(q) for q in (W, R)]
check("s4: parent_splitter defaults to None", sig["parent_splitter"].default is None)
check("s4: None -> 1 parent of 1,360 chars for every query, 23 children",
      len(HANDBOOK) == 1360 and nkeys(st0) == 1 and len(vs0.store) == 23
      and all(len(o) == 1 and len(o[0].page_content) == 1360 for o in outs0) and "1 parent, 1,360 characters" in plain(s4[0]["output"]))
sizes = [len(p) for p in parent.split_text(HANDBOOK)]
check("s4: 500-char splitter on \\n## gives 4 parents 401, 354, 347, 251", sizes == [401, 354, 347, 251]
      and "401, 354, 347 and 251" in s4[1]["output"])

# slide 5: k counts children
s5 = slide("`k` counts / [children]")
check("s5: search_kwargs empty by default; vector store k=4",
      MultiVectorRetriever.model_fields["search_kwargs"].default_factory() == {}
      and inspect.signature(VectorStore.similarity_search).parameters["k"].default == 4)
res = {}
for k in (1, 4, 10):
    r.search_kwargs = {"k": k}
    o = r.invoke(W); res[k] = (len(o), sum(len(d.page_content) for d in o), [section(d) for d in o])
r.search_kwargs = {}
opts = s5["visuals"][0]["options"]
check("s5: k=1 -> 1 parent 347 (Warranty)", res[1] == (1, 347, ["Warranty"]) and "1 parent, 347" in opts[0]["output"])
check("s5: k=4 -> 3 parents 1,102 (Warranty, Shipping, Refunds)", res[4] == (3, 1102, ["Warranty", "Shipping", "Refunds"])
      and "3 parents, 1,102" in opts[1]["output"])
check("s5: k=10 -> 4 parents 1,353 (every section)", res[10][0] == 4 and res[10][1] == 1353 and len(set(res[10][2])) == 4
      and "4 parents, 1,353" in plain(opts[2]["output"]))
check("s5: refund query at k=4 -> 2 parents", len(r.invoke(R)) == 2 and "returns 2 parents" in s5["after"])

# slide 6: re-ingest
r.add_documents([DOC])
o = r.invoke(W)
code6 = slide("Re-ingest [doubles] / every parent")["visuals"][0]["code"]
check("s6: uuid4 ids", "uuid.uuid4()" in inspect.getsource(ParentDocumentRetriever._split_docs_for_adding))
check("s6: 23 -> 46 children, 4 -> 8 parents, returns Warranty twice",
      len(vs.store) == 46 and nkeys(st) == 8 and [section(d) for d in o] == ["Warranty", "Warranty"]
      and "23 → 46" in code6 and "4 → 8" in code6)
check("s6: no delete method on the retriever", not [m for m in dir(ParentDocumentRetriever) if "delete" in m.lower()])
try:
    ParentDocumentRetriever(vectorstore=InMemoryVectorStore(SpacyEmb()), docstore=InMemoryStore(), child_splitter=child,
                            parent_splitter=parent).add_documents([DOC], ids=["handbook"])
    failed = False
except ValueError:
    failed = True
check("s6: ids with a parent_splitter fail unless one id per parent", failed)

# slide 7: in-memory parents vanish
r1, vs1, _ = build()
fresh = ParentDocumentRetriever(vectorstore=vs1, docstore=InMemoryStore(), child_splitter=child, parent_splitter=parent)
check("s7: new process (empty docstore), 23 children -> []", len(vs1.store) == 23 and fresh.invoke(W) == [])

# slide 8: scores stay behind
check("s8: parent metadata is only the source", r1.invoke(W)[0].metadata == {"source": "handbook.md"})
try:
    build(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.9})[0].invoke(W); raised = False
except NotImplementedError:
    raised = True
check("s8: InMemoryVectorStore raises NotImplementedError in score-threshold mode", raised)

# slide 9: LlamaIndex defaults
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.retrievers import AutoMergingRetriever
hsrc = inspect.getsource(HierarchicalNodeParser.from_defaults)
check("s9: simple_ratio_thresh=0.5, merge when ratio > thresh; chunk_sizes [2048, 512, 128]",
      inspect.signature(AutoMergingRetriever.__init__).parameters["simple_ratio_thresh"].default == 0.5
      and "ratio > self._simple_ratio_thresh" in inspect.getsource(AutoMergingRetriever._get_parents_and_merge)
      and "[2048, 512, 128]" in hsrc)

# slide 10: the config runs and survives a restart
code10 = slide("Put it all / [together]")["visuals"][0]["code"]
d = tempfile.mkdtemp()
vsx = InMemoryVectorStore(SpacyEmb())
cfg_parent = RecursiveCharacterTextSplitter(chunk_size=2000, separators=["\n## ", "\n\n", "\n", ". ", " "])
cfg_child = RecursiveCharacterTextSplitter(chunk_size=400)
rx = ParentDocumentRetriever(vectorstore=vsx, byte_store=LocalFileStore(d), child_splitter=cfg_child, parent_splitter=cfg_parent, search_kwargs={"k": 4})
rx.add_documents([DOC])
ry = ParentDocumentRetriever(vectorstore=vsx, byte_store=LocalFileStore(d), child_splitter=cfg_child)
check("s10: config runs; parents survive a new retriever on the same LocalFileStore", len(ry.invoke(W)) >= 1)
doc_src = inspect.getsource(ParentDocumentRetriever)
check("s10: 2000 / 400 are the sizes in LangChain's docstring example", "chunk_size=2000" in doc_src and "chunk_size=400" in doc_src
      and "chunk_size=2000" in code10 and "chunk_size=400" in code10)

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
