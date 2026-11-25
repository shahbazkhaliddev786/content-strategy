"""Re-run every example on the RAG #23 slides (contextual retrieval) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG23_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, rank_bm25 0.2.2, anthropic.
The 16 sample quarterly reports are made up for the test and built below. No LLM is called:
the "context" run uses a template in the style of Anthropic's example, and context_for()
is run against a fake client to check the request it builds.
"""
import importlib, json, re, subprocess, sys
from pathlib import Path

def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("langchain_text_splitters", "langchain-text-splitters==1.1.3"), ("rank_bm25", "rank_bm25==0.2.2"), ("anthropic", "anthropic")):
    ensure(mod, pkg)

import importlib.metadata as md_
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi

HERE = Path(__file__).parent
S = json.loads((HERE / "RAG23.json").read_text())["slides"]
slide = lambda t: next(s for s in S if s.get("title") == t)
plain = lambda x: re.sub(r"\{\{(.+?)\}\}", r"\1", x).replace("!!", "")
codes = lambda sl: [plain(v["code"]) for v in sl["visuals"] if v["kind"] == "code"]
opts = lambda sl, k=0: [v for v in sl["visuals"] if v["kind"] == "variants"][k]["options"]
flat = lambda t: " ".join(t.split())
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

check("langchain-text-splitters 1.1.3", md_.version("langchain-text-splitters") == "1.1.3")
check("rank_bm25 0.2.2", md_.version("rank_bm25") == "0.2.2")

# ---- 16 sample quarterly reports (made up for the test) ----
CO = {"ACME Corp": ("makes industrial sensors for factories", [-2, 3, 1, 4], "Poland"),
      "Globex": ("builds warehouse robots for retailers", [5, 9, 2, -3], "Texas"),
      "Halvar Labs": ("sells lab software to hospitals", [4, -1, 6, 2], "Ireland"),
      "Brightline Foods": ("packages frozen meals for supermarkets", [1, 2, -2, 5], "Ohio")}
QN = {1: ("first", "January to March"), 2: ("second", "April to June"),
      3: ("third", "July to September"), 4: ("fourth", "October to December")}
PREV = {1: "Q4 2022", 2: "Q1 2023", 3: "Q2 2023", 4: "Q3 2023"}
def doc(name, q):
    what, g, site = CO[name]; d = g[q - 1]
    verb = "grew" if d > 0 else "fell"
    return "\n\n".join([
        f"## Overview\n{name} {what}. This report covers the {QN[q][0]} quarter of 2023, {QN[q][1]}.",
        f"## Results\nThe company's revenue {verb} by {abs(d)}% over the previous quarter.",
        f"## Margin\nGross margin was {38 + q}%, and operating costs were in line with plan.",
        f"## Customers\nThe largest customer accounted for {10 + q}% of sales in the quarter.",
        f"## Hiring\nHeadcount rose to {200 + 10 * q} people, mostly in engineering and support.",
        "## Risks\nSupplier delays and currency moves are the main risks for the next two quarters.",
        f"## Outlook\nThe new site in {site} is on track to open next year."])
DOCS = {(n, q): doc(n, q) for n in CO for q in (1, 2, 3, 4)}
sp = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=0)
tok = lambda s: re.findall(r"\w+", s.lower())
SUM = {"Overview": "says what the company does and which months the report covers",
       "Results": "gives the quarter's revenue growth over {prev}",
       "Margin": "gives the quarter's gross margin and costs",
       "Customers": "gives the share of sales from the largest customer",
       "Hiring": "gives the headcount at the end of the quarter",
       "Risks": "lists the main risks for the next two quarters",
       "Outlook": "covers plans for next year"}
def chunks(mode):
    out = []
    for (n, q), text in DOCS.items():
        for c in sp.split_text(text):
            sec = re.match(r"## (\w+)", c).group(1)
            pre = {"plain": "",
                   "header": f"{n} · Q{q} 2023 quarterly report · {sec}\n",
                   "context": f"This chunk is from {n}'s Q{q} 2023 quarterly report and {SUM[sec].format(prev=PREV[q])}.\n"}[mode]
            out.append(((n, q, sec), pre + c))
    return out
Q = "What was the revenue growth for ACME Corp in Q2 2023?"
T = ("ACME Corp", 2, "Results")
def run(mode):
    ch = chunks(mode)
    sc = BM25Okapi([tok(t) for _, t in ch]).get_scores(tok(Q))
    order = sorted(range(len(ch)), key=lambda i: -sc[i])
    keys = [ch[i][0] for i in order]
    return ch, keys, {ch[i][0]: round(float(sc[i]), 2) for i in order}

# ---- slide "The answer ties for 5th" ----
s3 = slide("The answer ties / for [5th]")
ch, keys, sc = run("plain")
check("96 chunks", len(ch) == 96 and "96 chunks" in s3["text"])
check("16 reports, 4 companies", len(DOCS) == 16 and "16 made-up quarterly reports (4 companies" in s3["text"])
check("query on slide", Q in s3["visuals"][0]["caption"])
check("hits 1-4: ACME Overview chunks at 7.65",
      keys[:4] == [("ACME Corp", q, "Overview") for q in (1, 2, 3, 4)] and all(sc[k] == 7.65 for k in keys[:4])
      and "7.65 each" in opts(s3)[0]["output"])
tied = [k for k in keys if sc[k] == 3.62]
check("answer 3.62, tied with all 16 Results chunks at ranks 5-20",
      sc[T] == 3.62 and len(tied) == 16 and all(k[2] == "Results" for k in tied)
      and keys[4:20] == tied and sc[keys[20]] < 3.62
      and "the other 15 Results chunks" in opts(s3)[1]["output"] and "Ranks 5 to 20" in opts(s3)[1]["note"])
check("overview chunks say nothing about revenue", all("revenue" not in t for k, t in ch if k[2] == "Overview"))
target_text = dict(ch)[T]
check("every Results chunk shares only the, revenue, was, in with the query",
      all(set(tok(t)) & set(tok(Q)) == {"the", "revenue", "was", "in"} for k, t in ch if k[2] == "Results")
      and '"the", "revenue", "was" and "in"' in s3["after"])
check("answer chunk names neither ACME nor Q2", "acme" not in tok(target_text) and "q2" not in tok(target_text))

# ---- slide "Title and heading come free" ----
s4 = slide("Title and heading / come [free]")
ch, keys, sc = run("header")
check("header + full chunk on slide", flat(codes(s4)[0]) == flat(dict(ch)[T]))
check("header: answer ranks 1st at 6.81", keys[0] == T and sc[T] == 6.81 and "1st (6.81)" in opts(s4)[1]["output"])
check("header: next ACME Q1, Q3 and Q4 Results at 5.89", set(keys[1:4]) == {("ACME Corp", q, "Results") for q in (1, 3, 4)}
      and all(sc[k] == 5.89 for k in keys[1:4]) and sc[keys[4]] < 5.89 and "Q1, Q3 and Q4 Results, 5.89" in opts(s4)[1]["note"])
check("no prefix: ties for 5th (3.62)", "5th (3.62)" in opts(s4)[0]["output"])

# ---- slide "Context can pull the wrong chunk" ----
s10 = slide("Context can pull / the [wrong] chunk")
ch, keys, sc = run("context")
Q3 = ("ACME Corp", 3, "Results")
check("context: Q2 and Q3 Results tie at 9.06 for the top", set(keys[:2]) == {T, Q3} and sc[T] == sc[Q3] == 9.06 and sc[keys[2]] < 9.06)
for k, o in ((T, opts(s10)[0]), (Q3, opts(s10)[1])):
    line = dict(ch)[k].split("\n")[0]
    check(f"context line Q{k[1]} on slide", line.endswith(plain(o["output"]).strip('"').lstrip(".")) and "9.06" in o["note"])

# ---- Anthropic's numbers (Contextual Retrieval, 19 Sep 2024) ----
s8 = slide("Failed retrievals / [down] 49%")
vals = [r["value"] for r in s8["visuals"][0]["rows"]]
check("bars 5.7 / 3.7 / 2.9 / 1.9", vals == [5.7, 3.7, 2.9, 1.9])
red = [round(100 * (1 - v / 5.7)) for v in vals[1:]]
check("35%, 49%, 67% reductions", red == [35, 49, 67] and "35% and 49% fewer failures; 67% with the reranker" in s8["bullets"][2])

# ---- prompt + context_for(): build the request against a fake client ----
s6, s7 = slide("The context / [prompt]"), slide("Cache the / [document]")
ns = {}
exec(codes(s6)[0], ns)
ANTHROPIC_PROMPT = ("Here is the chunk we want to situate within the whole document <chunk> {chunk} </chunk> "
                    "Please give a short succinct context to situate this chunk within the overall document "
                    "for the purposes of improving search retrieval of the chunk. Answer only with the succinct "
                    "context and nothing else.")
check("prompt text matches Anthropic's", flat(ns["CHUNK"]) == ANTHROPIC_PROMPT and ns["DOC"] == "<document>\n{doc}\n</document>")
import anthropic
seen = {}
class FakeMsgs:
    def create(self, **kw):
        seen.update(kw)
        return type("R", (), {"content": [type("B", (), {"text": "CTX"})()]})()
class FakeClient:
    messages = FakeMsgs()
anthropic.Anthropic = lambda: FakeClient()
code7 = codes(s7)[0]
check("CACHE label on slide", [v for v in s7["visuals"] if v["kind"] == "code"][0].get("label") == 'CACHE = {"type": "ephemeral"}')
check("lead says to index context + newline + chunk", 'index `context + "\\n" + chunk`' in s7["text"])
exec("import anthropic\nclient = anthropic.Anthropic()\nCACHE = {\"type\": \"ephemeral\"}\n" + code7
     + "\nd, c, m = 'DOCTEXT', 'CHUNKTEXT', 'model-x'\ntext = context_for(d, c, m) + \"\\n\" + c", ns)
blocks = seen["messages"][0]["content"]
check("request: doc block cached, chunk block not",
      blocks[0]["cache_control"] == {"type": "ephemeral"} and "DOCTEXT" in blocks[0]["text"]
      and "cache_control" not in blocks[1] and "CHUNKTEXT" in blocks[1]["text"] and seen["max_tokens"] == 150)
check("context prepended to the chunk", ns["text"] == "CTX\nCHUNKTEXT")
from anthropic.types import TextBlockParam
check("cache_control is a TextBlockParam field", "cache_control" in TextBlockParam.__annotations__)

# ---- slide text checks ----
check("code lines under 46 characters", all(len(l) <= 46 for sl in S for v in sl.get("visuals", []) if v["kind"] == "code" for l in plain(v["code"]).split("\n")))
check("$1.02 estimate on slide", "with prompt caching: $1.02 per million document tokens, for 800-token chunks and 8k-token documents" in slide("You pay once, / at [ingest]")["after"])
print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
