"""Re-run every example on the RAG #21 slides (chunking legal documents) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG21_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, rank_bm25.
The sample contract, the clause chunker and refs() (both exec'd from the slides) and the BM25 setup are below.
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
S = json.loads((HERE / "RAG21.json").read_text())["slides"]
slide = lambda t: next(s for s in S if s.get("title") == t)
plain = lambda x: x.replace("{{", "").replace("}}", "").replace("!!", "")
codes = lambda sl: [plain(v["code"]) for v in sl["visuals"] if v["kind"] == "code"]
flat = lambda t: " ".join(t.split())   # undo slide wrapping
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

check("langchain-text-splitters 1.1.3", md_.version("langchain-text-splitters") == "1.1.3")

# ---- sample contract (made up for the demo) ----
CONTRACT = """MASTER SERVICES AGREEMENT

5. Data Protection
5.1 Supplier shall process Customer Data only on Customer's written instructions.
5.2 Supplier shall keep daily backups of Customer Data for at least 30 days.

7. Fees and Payment
7.1 Customer shall pay each invoice within 30 days of the invoice date.
7.2 Late amounts accrue interest at 1% per month until paid.

8. Limitation of Liability
8.1 Neither party shall be liable for any indirect or consequential damages.
8.2 Supplier's total liability under this Agreement shall not exceed the fees paid in the 12 months before the claim.
8.3 The limits in Sections 8.1 and 8.2 do not apply to:
(a) a party's breach of Section 10 (Confidentiality);
(b) loss of Customer Data caused by Supplier's failure to keep the backups required by Section 5.2; or
(c) fraud or wilful misconduct.

9. Term and Termination
9.1 This Agreement starts on the Effective Date and continues for 24 months.
9.2 Either party may terminate this Agreement on 60 days' written notice, subject to Section 7.1."""
TITLE = "MASTER SERVICES AGREEMENT"
LEAD = "8.3 The limits in Sections 8.1 and 8.2 do not apply to:"

# ---- slide: The exceptions lose their rule ----
R = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
check("default separators", R._separators == ["\n\n", "\n", " ", ""])
BASE = R.split_text(CONTRACT)
sl = slide("The exceptions / lose their [rule]"); c = codes(sl)
check("recursive 300: 5 chunks", len(BASE) == 5)
check("chunk 3 ends with the slide lines", flat(BASE[2]).endswith(flat(c[0])))
check("chunk 3 ends at 'do not apply to:'", BASE[2].endswith("do not apply to:"))
check("chunk 4 is the slide text", flat(BASE[3]) == flat(c[1]))
check("chunk 4 has no clause number and no rule", "8.3" not in BASE[3] and "apply" not in BASE[3] and "liab" not in BASE[3].lower())
check("chunk count label 'of 5'", "of 5" in sl["visuals"][0]["label"])

# ---- clause chunker (exec'd from the slide) ----
ns = {"re": re}; exec(codes(slide("The clause / [chunker]"))[0], ns)
CL = ns["chunk"](CONTRACT, TITLE)
check("clause chunks: 11", len(CL) == 11)
lens = [len(x) for x in CL]
check("clause chunk sizes 114 to 222", min(lens) == 114 and max(lens) == 222)
check("every clause chunk starts with the path", all(x.startswith(TITLE + " > ") for x in CL))
whole83 = ns["chunk"](CONTRACT, TITLE, max_chars=10**6)
w = next(x for x in whole83 if x.startswith(TITLE + " > 8. Limitation of Liability > 8.3\n"))
check("whole 8.3 with path is 305 characters", len(w) == 305)
check("lead-in is 55 characters", len(LEAD) == 55)
check("lines with no number are dropped (lead)", "continued" not in "".join(ns["chunk"]("8. X\n8.1 A\nwrapped tail", "T")))

# ---- slide: Put the path on top ----
sl = slide("Put the [path] / on top")
check("chunk 6 is the slide text", flat(CL[5]) == flat(codes(sl)[0]))
check("label 6 of 11", "6 of 11" in sl["visuals"][0]["label"])

# ---- slide: Repeat the lead-in ----
sl = slide("Repeat the / [lead-in]")
check("chunk 8 is the slide text", flat(CL[7]) == flat(codes(sl)[0]))
check("8.3 pieces (a), (b), (c) each carry the lead-in",
      [x.split("\n")[0][-6:] for x in CL[6:9]] == ["8.3(a)", "8.3(b)", "8.3(c)"] and all(x.split("\n")[1] == LEAD for x in CL[6:9]))
check("label 8 of 11", "8 of 11" in sl["visuals"][0]["label"])

# ---- slide: Search returns the cap ----
tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
Q = "Does the liability cap apply to loss of Customer Data?"
check("query on slide", Q in slide("Search returns / the [cap]")["text"])
def ranks(chunks):
    sc = BM25Okapi([tok(x) for x in chunks]).get_scores(tok(Q))
    return sorted(range(len(chunks)), key=lambda i: -sc[i])
rb, rc = ranks(BASE), ranks(CL)
check("recursive: top hit chunk 3 (8.2 cap)", rb[0] == 2 and "8.2 Supplier's total liability" in BASE[2])
check("recursive: chunk 4 ranked second", rb[1] == 3)
check("clause: top hit is 8.3(b)", CL[rc[0]].split("\n")[0].endswith("8.3(b)") and CL[rc[0]].split("\n")[1] == LEAD)
check("cap is 12 months of fees", "fees paid in the 12 months" in BASE[2])

# ---- slide: Clause regex still merges ----
sl = slide("Clause regex / still [merges]"); c = codes(sl)
ns2 = {"RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter}
exec(c[0], ns2)
seps = ns2["seps"]
RX = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0, separators=seps, is_separator_regex=True).split_text(CONTRACT)
check("regex 400: 4 chunks", len(RX) == 4)
heads = [l for l in RX[0].splitlines() if l and not re.match(r"\d+\.\d+ ", l)]
check("chunk 1 headings = slide", heads == c[1].splitlines())
c83 = next(x for x in RX if x.startswith("8.3 "))
check("8.3 whole in one chunk", "(a)" in c83 and "(c)" in c83)
check("8.3 chunk has no Limitation of Liability heading", "Limitation of Liability" not in c83)
check("label 'of 4'", "of 4" in sl["visuals"][1]["label"])

# ---- slide: Fetch the references ----
sl = slide("Fetch the / [references]")
ns3 = {"re": re}; code = codes(sl)[0]
exec(code.split("\n\nrefs(")[0], ns3)
R8 = ns3["refs"](CL[7], "8.3")
check("refs(chunks[7]) = ['8.1', '8.2', '5.2']", R8 == ["8.1", "8.2", "5.2"] and "['8.1', '8.2', '5.2']" in code)
c52 = next(x for x in CL if x.split("\n")[0].endswith("> 5.2"))
check("5.2 text quoted on slide", "daily backups of Customer Data for at least 30 days" in c52)
check("pattern misses 'Section 10' in 8.3(a)", "10" not in ns3["refs"](CL[6], "8.3") and "Section 10" in CL[6])

# ---- slide word counts (reading text) ----
check("11 clause chunks label consistent", all("of 11" in v.get("label", "") for s in S if s.get("type") == "body"
      for v in s.get("visuals", []) if "Clause chunk" in v.get("label", "")))

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
