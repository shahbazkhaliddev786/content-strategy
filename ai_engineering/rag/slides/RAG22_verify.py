"""Re-run every example on the RAG #22 slides (chunking transcripts) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG22_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, rank_bm25.
The sample support call is below; the exchange chunker and meta() are exec'd from the slides.
"""
import importlib, json, re, subprocess, sys
from pathlib import Path

def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("langchain_text_splitters", "langchain-text-splitters==1.1.3"), ("rank_bm25", "rank_bm25")):
    ensure(mod, pkg)

import importlib.metadata as md_
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi

HERE = Path(__file__).parent
POST = json.loads((HERE / "RAG22.json").read_text())
S = POST["slides"]
slide = lambda t: next(s for s in S if s.get("title") == t)
plain = lambda x: x.replace("{{", "").replace("}}", "").replace("!!", "")
codes = lambda sl: [plain(v["code"]) for v in sl["visuals"] if v["kind"] == "code"]
flat = lambda t: " ".join(t.split())   # undo slide wrapping
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

check("langchain-text-splitters 1.1.3", md_.version("langchain-text-splitters") == "1.1.3")

# ---- sample support call (made up for the demo), one turn per line ----
CALL = """[00:00] Agent: Thanks for calling Northwind Cloud support, this is Priya. How can I help?
[00:06] Customer: Hi, I'm on the annual Team plan and we're moving to a smaller tool next month.
[00:14] Agent: Sorry to hear that. I can help you cancel today or set it to end at renewal.
[00:21] Customer: Before I decide, if I cancel now, do I get any money back for the months we haven't used?
[00:29] Agent: Yes. On annual plans you get a prorated refund for every full unused month, as long as you cancel within 90 days of the renewal date.
[00:41] Customer: We renewed in March, so that works. How long does the refund take?
[00:47] Agent: It goes back to the original card in 5 to 10 business days.
[00:55] Customer: OK. And what happens to our files?
[00:59] Agent: Your workspace stays read-only for 30 days, so you can export everything. Go to Settings, then Data, then Export, and pick a format. The export runs in the background and emails a download link to the workspace owner. After the 30 days, the workspace and its files are deleted and we can't restore them.
[01:24] Customer: Got it. Please cancel it now."""

# ---- slide: The question loses its answer ----
R = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
check("default separators", R._separators == ["\n\n", "\n", " ", ""])
BASE = R.split_text(CALL)
check("recursive 300: 6 chunks", len(BASE) == 6)
sl = slide("The question / loses its [answer]"); c = codes(sl)
check("chunk 3 ends with the slide lines", flat(BASE[2]).endswith(flat(c[0])))
check("chunk 3 ends at the files question", BASE[2].endswith("And what happens to our files?"))
check("chunk 4 starts with the slide lines", flat(BASE[3]).startswith(flat(c[1]).rstrip(".")))
check("chunk 4 is the 00:59 answer", BASE[3].startswith("[00:59] Agent:"))
check("every base chunk boundary but one is a line end", sum(not CALL.split(b, 1)[1].startswith("\n") for b in BASE[:-1]) == 1)
check("labels 'of 6'", all("of 6" in v["label"] for v in sl["visuals"]))

# ---- slide: A long turn drops its speaker ----
sl = slide("A long turn / drops its [speaker]")
check("chunk 5 is the slide text", BASE[4] == codes(sl)[0])
check("chunk 5 is 19 characters", len(BASE[4]) == 19 and "19 characters" in sl["bullets"][0])
L0059 = next(l for l in CALL.splitlines() if l.startswith("[00:59]"))
check("00:59 line runs past 300", len(L0059) > 300)
check("chunk 4 ends mid-sentence (split at a space)", BASE[3].endswith("and we"))

# ---- exchange chunker (exec'd from the slide) ----
ns = {"re": re}; exec(codes(slide("The exchange / [chunker]"))[0], ns)
X = ns["chunk"](CALL)
check("exchange chunks: 7", len(X) == 7)
lens = [len(x) for x in X]
check("sizes 47 to 285", min(lens) == 47 and max(lens) == 285 and "47 to 285" in slide("Group the / [exchange]")["bullets"][2])
check("every line keeps speaker and timestamp", all(re.match(r"\[\d\d:\d\d\] \w+: ", l) for x in X for l in x.splitlines()))
sl = slide("Group the / [exchange]")
check("exchange chunk 4 is the slide text", flat(X[3]) == flat(codes(sl)[0]) and "4 of 7" in sl["visuals"][0]["label"])
sl = slide("Repeat the / [question]")
check("exchange chunk 6 is the slide text", flat(X[5]) == flat(codes(sl)[0]) and "6 of 7" in sl["visuals"][0]["label"])
Q0055 = "[00:55] Customer: OK. And what happens to our files?"
check("chunks 5 and 6 both start with the question", X[4].startswith(Q0055 + "\n") and X[5].startswith(Q0055 + "\n"))
check("files exchange runs over 300", len(Q0055 + "\n" + L0059) > 300)

# ---- slide: Search finds the question ----
tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
def ranks(chunks, q):
    sc = BM25Okapi([tok(x) for x in chunks]).get_scores(tok(q))
    return sorted(range(len(chunks)), key=lambda i: -sc[i])
Q1 = "What happens to our files after we cancel?"
check("query on slide", Q1 in slide("Search finds / the [question]")["text"])
rb, rx = ranks(BASE, Q1), ranks(X, Q1)
check("recursive: top hit chunk 3 (ends at the question)", rb[0] == 2)
check("recursive: chunk 4 ranked 2nd", rb[1] == 3)
check("exchange: top hit chunk 6 (deleted after 30 days)", rx[0] == 5 and "deleted" in X[5] and "After the 30 days" in X[5])
check("exchange: export steps chunk ranked 2nd", rx[1] == 4 and "Export" in X[4])
Q2 = "Can you restore our files after we cancel?"
check("restore query on slide", Q2 in " ".join(slide("A long turn / drops its [speaker]")["bullets"]))
check("restore query: recursive top hit is chunk 5", ranks(BASE, Q2)[0] == 4)

# ---- slide: Keep the timestamps ----
sl = slide("Keep the / [timestamps]"); code = codes(sl)[0]
ns2 = {"re": re}; exec(code.split("\n\nmeta(")[0], ns2)
M = ns2["meta"](X[5])
check("meta(chunks[5]) matches slide", M == {"start": "00:55", "speakers": ["Agent", "Customer"]}
      and "'start': '00:55'" in code and "'speakers': ['Agent', 'Customer']" in code)

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
