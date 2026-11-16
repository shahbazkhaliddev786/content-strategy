"""Re-run every example on the RAG #19 slides (chunking code) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG19_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, llama-index-core 0.14.25,
tree-sitter-language-pack and rank_bm25. The sample file, the ast chunker and the BM25 setup are below.
"""
import ast, importlib, inspect, json, re, subprocess, sys, warnings
from pathlib import Path
from textwrap import dedent, indent

def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("langchain_text_splitters", "langchain-text-splitters==1.1.3"),
                 ("llama_index.core", "llama-index-core==0.14.25"),
                 ("tree_sitter_language_pack", "tree-sitter-language-pack"),
                 ("rank_bm25", "rank_bm25")):
    ensure(mod, pkg)
warnings.filterwarnings("ignore")

import importlib.metadata as md
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter as R
from llama_index.core.node_parser import CodeSplitter
import llama_index.core.node_parser.text.code as li_code
from rank_bm25 import BM25Okapi

HERE = Path(__file__).parent
S = json.loads((HERE / "RAG19.json").read_text())["slides"]
slide = lambda title: next(s for s in S if s.get("title") == title)
codes = lambda sl: [v["code"].replace("{{", "").replace("}}", "") for v in sl["visuals"] if v["kind"] == "code"]
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

SAMPLE = '''import logging
from decimal import Decimal

from .gateway import Gateway

log = logging.getLogger(__name__)
LIMIT = Decimal("500")


class RefundService:
    def __init__(self, gw: Gateway):
        self.gw = gw

    def refund(self, order, amount):
        if amount <= 0:
            raise ValueError("amount <= 0")
        if amount > order.paid:
            raise ValueError("over paid")

        if amount > LIMIT:
            raise ValueError("needs approval")
        rid = self.gw.refund(order, amount)
        order.refunded += amount
        log.info("refund %s", rid)
        return rid

    def left(self, order):
        return order.paid - order.refunded


@retry(times=3)
def sync_refunds(service, orders):
    for order in orders:
        service.gw.sync(order)
'''
PATH = "billing/refunds.py"

def chunk_python(path, src, max_chars=1500):
    """One chunk per function or method, decorators included, with a header:
    file path, class name and the module constants the code reads.
    A function over max_chars is split between top-level statements of its body,
    and every part repeats the signature."""
    tree, lines = ast.parse(src), src.splitlines()
    get = lambda a, b: dedent("\n".join(lines[a - 1:b]))
    consts = {t.id: get(n.lineno, n.end_lineno)
              for n in tree.body if isinstance(n, ast.Assign)
              for t in n.targets if getattr(t, "id", "").isupper()}
    defs = [(None, n) for n in tree.body]
    defs += [(c.name, m) for c in tree.body if isinstance(c, ast.ClassDef) for m in c.body]
    defs = sorted([d for d in defs if isinstance(d[1], ast.FunctionDef)], key=lambda d: d[1].lineno)
    out = []
    for cls, fn in defs:
        title = f"# {path}" + (f" · class {cls}" if cls else "")
        def header(nodes):
            used = {n.id for x in nodes for n in ast.walk(x) if isinstance(n, ast.Name)}
            return "\n".join([title] + [consts[k] for k in consts if k in used])
        head = header([fn])
        top = min([fn.lineno] + [d.lineno for d in fn.decorator_list])
        whole = get(top, fn.end_lineno)
        if len(head) + 1 + len(whole) <= max_chars:
            out.append(f"{head}\n{whole}")
            continue
        sig = get(top, fn.body[0].lineno - 1)
        budget = max_chars - len(head) - len(sig) - len("  # part 1/1") - 2
        parts, cur = [], []
        for st in fn.body:
            s = indent(get(st.lineno, st.end_lineno), "    ")
            if cur and len("\n".join([t for _, t in cur] + [s])) > budget:
                parts.append(cur); cur = []
            cur.append((st, s))
        parts.append(cur)
        for i, p in enumerate(parts, 1):
            h = header(fn.decorator_list + [fn.args] + [st for st, _ in p])
            out.append(f"{h}\n{sig}  # part {i}/{len(parts)}\n" + "\n".join(t for _, t in p))
    return out

# --- versions and the sample
check("langchain-text-splitters 1.1.3", md.version("langchain-text-splitters") == "1.1.3")
check("llama-index-core 0.14.25", md.version("llama-index-core") == "0.14.25")
check("sample is 34 lines, 778 characters", len(SAMPLE.splitlines()) == 34 and len(SAMPLE) == 778)
check("sample: lines fit the code panel (<= 46 chars)", max(map(len, SAMPLE.splitlines())) <= 46)
check("sample uses 4-space indentation, no tabs", "\t" not in SAMPLE and "\n    def " in SAMPLE)

# --- slide: Characters cut the method
default = R(chunk_size=250, chunk_overlap=0).split_text(SAMPLE)
sl = slide("Characters cut / the [method]")
c = codes(sl)
check("default splitter: 4 chunks", len(default) == 4 and "Chunk 2 of 4" == sl["visuals"][0]["label"])
check("default splitter: chunk 2 on slide matches", default[1] == c[0])
check("default splitter: chunk 3 on slide matches", default[2] == c[1])
check("default separators", R(chunk_size=250)._separators == ["\n\n", "\n", " ", ""])
check("cut fell on the blank line inside refund", "raise ValueError(\"over paid\")\n\n        if amount > LIMIT:" in SAMPLE)
check("chunk 3 has no def/class/file name", not re.search(r"def |class |refunds\.py", default[2]))
check("default chunk_overlap is 200 (we set 0)", inspect.signature(R.__mro__[1].__init__).parameters["chunk_overlap"].default == 200)

# --- slide: The method split needs a tab
seps = R.get_separators_for_language(Language.PYTHON)
check("Python separators list", seps == ["\nclass ", "\ndef ", "\n\tdef ", "\n\n", "\n", " ", ""])
sl = slide("The method split / needs a [tab]")
shown = codes(sl)[0].replace("\n", " ")
check("separators on slide match", [eval(x) for x in re.findall(r'"(?:[^"\\]|\\.)*"', shown)] == seps)
check("from_language treats separators as regex", "is_separator_regex=True" in inspect.getsource(R.from_language))
check("no tab-indented def in the sample", re.search("\n\tdef ", SAMPLE) is None)
py = R.from_language(Language.PYTHON, chunk_size=250, chunk_overlap=0).split_text(SAMPLE)
check("python separators: 6 chunks, chunk 4 starts at the limit check",
      len(py) == 6 and py[3].startswith("if amount > LIMIT:") and py[3] == default[2])
check("tab-indented copy: methods split at \\n\\tdef",
      any(x.startswith("def refund") for x in R.from_language(Language.PYTHON, chunk_size=250, chunk_overlap=0).split_text(SAMPLE.replace("    ", "\t"))))
check("PEP 8 quote", "Use 4 spaces per indentation level" in " ".join(sl["bullets"]))

# --- slide: Decorators get left behind
sl = slide("Decorators get / [left] behind")
c = codes(sl)
check("chunk 5 of 6 on slide matches", py[4] == c[0] and py[4].endswith("@retry(times=3)"))
check("chunk 6 of 6 on slide matches", py[5] == c[1] and "retry" not in py[5])
check("RecursiveCharacterTextSplitter keeps separators (keep_separator=True default)",
      inspect.signature(R.__init__).parameters["keep_separator"].default is True)
route = SAMPLE.replace("@retry(times=3)", '@app.get("/refunds")')
rc = R.from_language(Language.PYTHON, chunk_size=250, chunk_overlap=0).split_text(route)
check("route decorator stranded the same way", rc[4].endswith('@app.get("/refunds")') and rc[5].startswith("def sync_refunds"))

# --- slide: Tree-sitter keeps the decorator
cs = CodeSplitter(language="python", max_chars=250).split_text(SAMPLE)
sl = slide("Tree-sitter keeps / the [decorator]")
check("CodeSplitter 250: 8 chunks, chunk 8 on slide matches", len(cs) == 8 and cs[7] == codes(sl)[0])
check("CodeSplitter: class line and signature alone",
      "class RefundService:" in cs and "def refund(self, order, amount):" in cs)
check("CodeSplitter: body after the signature has no function name",
      cs[cs.index("def refund(self, order, amount):") + 1].startswith("if amount <= 0:"))
check("CodeSplitter recurses into children of an oversized node", "self._chunk_node(child" in inspect.getsource(li_code.CodeSplitter._chunk_node))
check("count_mode defaults to char, token mode uses max_tokens", li_code.CodeSplitter.model_fields["count_mode"].default == "char" and "self.max_tokens" in inspect.getsource(li_code.CodeSplitter._chunk_node))
check("LlamaIndex credits Sweep AI", "SweepAI" in (li_code.CodeSplitter.__doc__ or ""))

# --- slide: Size it with max_chars
check("defaults: max_chars 1500, max_tokens 512, chunk_lines 40, overlap 15",
      (li_code.DEFAULT_MAX_CHARS, li_code.DEFAULT_MAX_TOKENS, li_code.DEFAULT_CHUNK_LINES, li_code.DEFAULT_LINES_OVERLAP) == (1500, 512, 40, 15))
a = CodeSplitter(language="python").split_text(SAMPLE)
b = CodeSplitter(language="python", chunk_lines=5, chunk_lines_overlap=2).split_text(SAMPLE)
check("default CodeSplitter: 778-character file -> 1 chunk; chunk_lines changes nothing", len(a) == 1 and a == b)
check("chunk_lines changes nothing at 250 either",
      CodeSplitter(language="python", max_chars=250, chunk_lines=3, chunk_lines_overlap=1).split_text(SAMPLE) == cs)
src = inspect.getsource(li_code.CodeSplitter._chunk_node) + inspect.getsource(li_code.CodeSplitter.split_text)
check("split code doesn't read chunk_lines", "chunk_lines" not in src)
check("no overlap between CodeSplitter chunks", all(not (x and y and x[-20:] in y) for x, y in zip(cs, cs[1:])))

# --- slide: Give each chunk its address
mine = chunk_python(PATH, SAMPLE)
sl = slide("Give each chunk / its [address]")
c = codes(sl)
check("ast chunker at 1500: 4 chunks, chunks 3 and 4 match the slide", len(mine) == 4 and mine[2] == c[0] and mine[3] == c[1])
check("refund chunk carries LIMIT in its header", mine[1].splitlines()[1] == 'LIMIT = Decimal("500")')
fn = [n for n in ast.parse(SAMPLE).body if isinstance(n, ast.FunctionDef)][0]
check("ast: lineno is the def line, decorators in decorator_list",
      SAMPLE.splitlines()[fn.lineno - 1].startswith("def sync_refunds") and fn.decorator_list[0].lineno == fn.lineno - 1)

# --- slide: Split long ones, keep the signature
m250 = chunk_python(PATH, SAMPLE, 250)
parts = [x for x in m250 if "# part " in x]
sl = slide("Split long ones, / keep the [signature]")
check("refund splits into 3 parts at 250", len(parts) == 3 and all("def refund(self, order, amount):  # part" in p for p in parts))
check("part 2 of 3 matches the slide", parts[1] == codes(sl)[0])
check("parts 1 and 3 leave LIMIT out", "LIMIT =" not in parts[0] and "LIMIT =" not in parts[2])
check("every chunk fits 250", all(len(x) <= 250 for x in m250))
check("if stays with its raise", all(not p.rstrip().split("\n")[-1].lstrip().startswith("if ") for p in parts))

# --- slide: Search found the imports
tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
Q = "Where is the 500 refund limit checked?"
def ranked(chunks):
    sc = BM25Okapi([tok(x) for x in chunks]).get_scores(tok(Q))
    return [chunks[i] for i in sorted(range(len(chunks)), key=lambda i: -sc[i])]
sl = slide("Search found / the [imports]")
check("query on slide", Q in sl["text"])
for name, chunks, second in (("characters", default, None), ("python separators", py, py[3]), ("CodeSplitter", cs, "def refund(self, order, amount):")):
    r = ranked(chunks)
    check(f"{name}: top hit is the imports block", r[0].startswith("import logging") and 'LIMIT = Decimal("500")' in r[0] and "if amount" not in r[0])
    if second:
        check(f"{name}: 2nd hit as on slide", r[1] == second)
r = ranked(m250)
check("ast + header: top hit is refund part 2/3 with the check and the 500",
      r[0] == parts[1] and "if amount > LIMIT" in r[0] and '"500"' in r[0])

# --- slide text sanity
check("cover inside lines are on Instagram slides", all(s.get("instagram", True) for s in S if s.get("title") in (
    "Characters cut / the [method]", "The method split / needs a [tab]", "Decorators get / [left] behind",
    "Give each chunk / its [address]", "Search found / the [imports]", "Per-function [chunks]: / use or move on")))

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
