"""Re-run every example on the RAG #22 slides (chunking transcripts) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG22_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, rank_bm25.
The sample call is below; exchanges(), chunk() and pack() are exec'd from the slides.
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
S = json.loads((HERE / "RAG22.json").read_text())["slides"]
slide = lambda t: next(s for s in S if s.get("title") == t)
plain = lambda x: x.replace("{{", "").replace("}}", "").replace("!!", "")
codes = lambda sl: [plain(v["code"]) for v in sl["visuals"] if v["kind"] == "code"]
flat = lambda t: " ".join(t.split())   # undo slide wrapping
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

check("langchain-text-splitters 1.1.3", md_.version("langchain-text-splitters") == "1.1.3")

# ---- sample support call (made up for the demo) ----
T = """[00:00:04] Agent: Acme support, this is Priya. How can I help?
[00:00:09] Customer: Hi, I'm on the Free plan and my CSV export stopped at 10,000 rows.
[00:00:15] Agent: That's the Free plan limit. Exports are capped at 10,000 rows per file.
[00:00:21] Customer: Is there a way to export the full table, about 250,000 rows?
[00:00:27] Agent: Yes. On the Pro plan the limit goes up to 1,000,000 rows, or you can use the API with pagination on any plan.
[00:00:36] Customer: Does the API count against my monthly quota?
[00:00:40] Agent: It does. Each API page counts as one request, and a page holds up to 5,000 rows. The Free plan includes 1,000 requests a month, so your 250,000-row table takes 50 requests. Pass the cursor from each response to get the next page, and stop when the response has no cursor.
[00:00:58] Customer: OK.
[00:00:59] Customer: And if I upgrade mid-month, what happens to the bill?
[00:01:04] Agent: You pay the difference for the rest of the month, prorated by day. Your next invoice shows the Pro price.
[00:01:12] Customer: Great, thanks."""
LINES = T.split("\n")
QS = [i for i, l in enumerate(LINES) if " Customer: " in l and l.endswith("?")]
check("3 questions on the call", len(QS) == 3)
def together(C):   # questions that share a chunk with the start of their answer
    return sum(any(LINES[i] in c and LINES[i + 1][:40] in c for c in C) for i in QS)
R = lambda size, ov=0: RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=ov).split_text(T)
tok = lambda s: re.findall(r"\w+", s.lower())
def ranking(C, q):
    sc = BM25Okapi([tok(c) for c in C]).get_scores(tok(q))
    return sorted(range(len(C)), key=lambda i: -sc[i])

# ---- slide: The reply lands one chunk later ----
B = R(200)
sl = slide("The reply lands / one chunk [later]"); c = codes(sl)
check("default separators", RecursiveCharacterTextSplitter()._separators == ["\n\n", "\n", " ", ""])
check("recursive 200: 7 chunks", len(B) == 7)
check("chunk 6 is the slide text", flat(B[5]) == flat(c[0]))
check("chunk 7 is the slide text", flat(B[6]) == flat(c[1]))
check("labels 'of 7'", all("of 7" in v["label"] for v in sl["visuals"]))
ends = all(any(c_.endswith(LINES[i]) for c_ in B) and any(c_.startswith(LINES[i + 1][:40]) for c_ in B) for i in QS)
check("every question ends a chunk; every answer starts the next", ends and together(B) == 0)

# ---- slide: Search returns the question ----
Q = "What happens to the bill if I upgrade mid-month?"
check("query on slide", Q in slide("Search returns / the [question]")["text"])
rk = ranking(B, Q)
check("recursive 200 top hit is chunk 6 (question, no answer)", rk[0] == 5 and "prorated" not in B[5])
check("answer chunk 7 ranks 5th of 7", rk.index(6) == 4)

ns = {"re": re}
exec(codes(slide("Group turns into / [exchanges]"))[0].split("\n\n[(e[0][0]")[0], ns)
exec(codes(slide("The exchange / [chunker]"))[0], ns)
exec(codes(slide("Long replies keep / the [question]"))[0], ns)
EX = ns["exchanges"](T)
CH = ns["chunk"](T, "Acme support call", "Customer")
rk = ranking(CH, Q)
check("exchange top hit has question + 'prorated by day'", "what happens to the bill?" in CH[rk[0]] and "prorated by day" in CH[rk[0]])

# ---- slide: A bigger size moves the cut ----
sl = slide("A bigger size / [moves] the cut")
for size, want, n in ((200, 0, 7), (300, 2, 4), (400, 0, 4)):
    opt = next(o for o in sl["visuals"][0]["options"] if o["setting"] == f"chunk_size={size}")
    C = R(size)
    check(f"size {size}: {want} of 3 together, {n} chunks", together(C) == want and len(C) == n
          and opt["output"] == f"{want} of 3 questions" and opt["note"] == f"{n} chunks")
sizes = list(range(150, 701, 10))
split_any = [s for s in sizes if together(R(s)) < 3]
check("55 of 56 sizes split at least one pair", len(sizes) == 56 and len(split_any) == 55)
check("only 450 keeps all three", [s for s in sizes if together(R(s)) == 3] == [450])

# ---- slide: Overlap skips whole turns ----
qa_lens = [len(LINES[j]) for i in QS for j in (i, i + 1)] + [len(LINES[1]), len(LINES[2])]
check("every question and answer turn over 60 characters", min(qa_lens) > 60)
check("overlap 50: 0 of 3, one chunk changed (inside the long reply)",
      together(R(200, 50)) == 0 and len(R(200, 50)) == 7
      and [i for i, (a, b) in enumerate(zip(B, R(200, 50))) if a != b] == [4])
check("overlap 100: 1 of 3 in 9 chunks", together(R(200, 100)) == 1 and len(R(200, 100)) == 9)

# ---- slide: Monologues lose the speaker ----
sl = slide("Monologues lose / the [speaker]"); c = codes(sl)
check("long turn is 289 characters", len(LINES[6]) == 289 and "289-character" in sl["text"])
check("chunk 4 ends with slide text", flat(B[3]).endswith(flat(c[0]).lstrip(".")))
check("chunk 5 is slide text", flat(B[4]) == flat(c[1]))
check("chunk 5: no speaker, no timestamp, no question", "Agent" not in B[4] and "[" not in B[4] and "?" not in B[4])

# ---- slide: Group turns into exchanges ----
out = [(e[0][0], len(e)) for e in EX]
check("exchanges output on slide", out == [('00:00:04', 3), ('00:00:21', 2), ('00:00:36', 2), ('00:00:58', 4)])
check("slide comment matches output", flat(codes(slide("Group turns into / [exchanges]"))[0].split("exchanges(T)]\n", 1)[1].replace("# ", "")) == flat(str(out)))

# ---- slides: chunker + Long replies keep the question ----
check("exchange chunks: 5", len(CH) == 5)
check("all exchange chunks <= 300", max(len(x) for x in CH) <= 300)
sl = slide("Long replies keep / the [question]"); c = codes(sl)
check("chunk 4 of 5 is the slide text", flat(CH[3]) == flat(c[1]))
check("long turn -> two chunks, both under 300", sum("[00:00:40] Agent:" in x for x in CH) == 2
      and all(len(x) < 300 for x in CH if "[00:00:40] Agent:" in x))
check("both pieces carry the question", all("Does the API count against my monthly quota?" in x for x in CH if "[00:00:40]" in x))
check("every exchange chunk starts with its header", all(x.startswith("Acme support call · 00:") for x in CH))

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
