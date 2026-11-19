"""Re-run every example on the RAG #22 slides (chunking transcripts) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG22_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, rank_bm25.
The sample call, the exchange chunker (exec'd from the slide), split() as the slide describes it, and the BM25 setup are below.
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
CALL = """Support call: nightly export failures, 12 Nov

[00:00] Agent: Thanks for calling, this is Maya. How can I help?
[00:04] Customer: Our nightly export to S3 has failed three nights in a row.
[00:09] Agent: Sorry about that. Which plan is the account on?
[00:12] Customer: Starter, I think.
[00:15] Agent: That explains it. On Starter, an export over 5 GB is rejected, and your last three were 6.2, 6.4 and 6.1 GB.
[00:26] Customer: Can we raise that limit without changing plans?
[00:30] Agent: Not on Starter. You can add the --per-table flag so each table exports as its own file, and each file stays under 5 GB. Business raises the limit to 50 GB.
[00:44] Customer: Does --per-table change the file names?
[00:48] Agent: Yes. Each file gets the table name as a suffix, so update any job that reads the old single file.
[00:56] Customer: OK, we'll try the flag tonight."""
CALL2 = CALL.replace("Which plan is the account on?", "Which plan is the account on? I can check.")

# ---- slide: Questions lose their answers ----
R = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
check("default separators", R._separators == ["\n\n", "\n", " ", ""])
BASE = R.split_text(CALL)
sl = slide("Questions lose / their [answers]"); c = codes(sl)
check("recursive 300: 5 chunks", len(BASE) == 5)
check("chunk 3 ends with the slide lines", flat(BASE[2]).endswith(flat(c[0])))
check("chunk 4 starts with the slide lines", flat(BASE[3]).startswith(flat(c[1])))
check("labels 'of 5'", all("of 5" in v["label"] for v in sl["visuals"]))
turn_starts = {l for l in CALL.splitlines() if l}
check("every cut falls between turns (chunks are whole lines)", all(set(x.splitlines()) <= turn_starts for x in BASE))
check("two of four cuts leave a question at a chunk end", sum(x.endswith("?") for x in BASE[:-1]) == 2 and len(BASE) - 1 == 4)
check("chunk 4 holds the answer 'Not on Starter.'", "Not on Starter." in BASE[3] and "Not on Starter." not in BASE[2])

# ---- slide: Turn separators still pack ----
sl = slide("Turn separators / still [pack]")
ns0 = {"RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter}
code0 = codes(sl)[0]
exec(code0.split("RecursiveCharacterTextSplitter(")[0], ns0)
RX = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0, separators=ns0["seps"], is_separator_regex=True).split_text(CALL)
check("regex 300: 4 chunks", len(RX) == 4)
check("regex: chunks 2 and 3 end on a question", RX[1].endswith("?") and RX[2].endswith("?") and not RX[0].endswith("?"))
check("regex: the answers open the next chunk", RX[2].startswith("[00:30] Agent: Not on Starter.") and RX[3].startswith("[00:48] Agent: Yes."))

# ---- exchange chunker (exec'd from the slide); split() as the slide's note says ----
def split(said, n):
    return RecursiveCharacterTextSplitter(chunk_size=n, chunk_overlap=0, separators=[". ", " "], keep_separator="end").split_text(said)
sl = slide("The exchange / [chunker]")
check("split() note on slide", 'separators=[". ", " "]' in sl["after"])
ns = {"split": split}; exec(codes(sl)[0], ns)
EX = ns["chunk"](CALL)
check("exchange chunks: 4", len(EX) == 4)
lens = [len(x) for x in EX]
check("exchanges 201 to 296 characters", min(lens) == 201 and max(lens) == 296)
check("every exchange chunk starts with the title and a time range", all(re.match(r"Support call: nightly export failures, 12 Nov \[\d\d:\d\d-\d\d:\d\d\]\n", x) for x in EX))
check("every exchange opens at a question (after the header)", all(x.split("\n")[1].endswith("?") for x in EX))

# ---- slide: Open at each question ----
sl = slide("Open at each / [question]")
check("exchange chunk 3 is the slide text", flat(EX[2]) == flat(codes(sl)[0]))
check("label 3 of 4", "3 of 4" in sl["visuals"][0]["label"])
check("chunk 3 is 296 characters with both workarounds", len(EX[2]) == 296 and "--per-table" in EX[2] and "Business raises the limit to 50 GB" in EX[2])

# ---- slide: Repeat the question ----
sl = slide("Repeat the / [question]")
E250 = ns["chunk"](CALL, size=250)
check("size=250: 8 chunks", len(E250) == 8 and "of 8" in sl["visuals"][0]["label"])
check("chunk 5 of 8 is the slide text", flat(E250[4]) == flat(codes(sl)[0]))
check("all 250 chunks within the limit", all(len(x) <= 250 for x in E250))
q26 = "[00:26] Customer: Can we raise that limit without changing plans?"
pieces = [x for x in E250 if "[00:26-00:30]" in x]
check("00:26 exchange splits in 3 pieces, each with the question and 'Agent:' label",
      len(pieces) == 3 and all(x.split("\n")[1] == q26 and x.split("\n")[2].startswith("[00:30] Agent: ") for x in pieces))
check("pieces split at sentence ends", [x.split("\n")[2] for x in pieces] == [
    "[00:30] Agent: Not on Starter.",
    "[00:30] Agent: You can add the --per-table flag so each table exports as its own file, and each file stays under 5 GB.",
    "[00:30] Agent: Business raises the limit to 50 GB."])

# ---- slide: Search finds the question ----
tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
Q = "Can we raise the export limit without changing plans?"
check("query on slide", Q in slide("Search finds / the [question]")["text"])
def ranks(chunks):
    sc = BM25Okapi([tok(x) for x in chunks]).get_scores(tok(Q))
    return sorted(range(len(chunks)), key=lambda i: -sc[i])
rb, re_ = ranks(BASE), ranks(EX)
check("recursive: top hit chunk 3, ends on the question", rb[0] == 2 and BASE[2].endswith("without changing plans?"))
check("recursive: chunk 4 (the answer) ranked 2nd", rb[1] == 3)
check("recursive chunk 3 holds the 5 GB limit and no answer", "5 GB" in BASE[2] and "Not on Starter" not in BASE[2])
check("exchange: top hit has question + 'Not on Starter.' + both workarounds",
      "without changing plans?" in EX[re_[0]] and "Not on Starter." in EX[re_[0]] and "--per-table" in EX[re_[0]] and "Business" in EX[re_[0]])

# ---- slide: When a question hides ----
sl = slide("When a question / [hides]")
check("chunker on slide tests '?' anywhere", '"?" in t' in codes(slide("The exchange / [chunker]"))[0])
nsE = {"split": split}; exec(codes(slide("The exchange / [chunker]"))[0].replace('"?" in t', 't.endswith("?")'), nsE)
check("endswith version: same 4 chunks on the original call", nsE["chunk"](CALL) == EX)
C2 = nsE["chunk"](CALL2)
starter = next(x for x in C2 if "Starter, I think." in x)
check("endswith: 'Starter, I think.' filed under 'How can I help?'", starter.split("\n")[1].endswith("How can I help?"))
check("endswith: no new chunk at 00:09", not any(x.split("\n")[1].startswith("[00:09]") for x in C2))
src = codes(slide("The exchange / [chunker]"))[0]
check("variant setting strings on slide", [o["setting"] for o in sl["visuals"][0]["options"]] == ['t.endswith("?")', '"?" in t'])
C3 = ns["chunk"](CALL2)
check("'?' in t: 4 exchange chunks again", len(C3) == 4)
check("'?' in t: 'Starter, I think.' stays with 'Which plan'", "Which plan is the account on? I can check." in next(x for x in C3 if "Starter, I think." in x))
check("CALL2 changed text on slide", "Which plan is the account on? I can check." in sl["text"] and 't.endswith("?")' in sl["text"])

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
