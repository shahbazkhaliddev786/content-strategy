"""Re-run every example on the RAG #24 slides (tuning chunk size and overlap) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG24_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, rank_bm25 0.2.2, spaCy and
en_core_web_md 3.8.0 (from the spaCy models release on GitHub), tiktoken.
The six help-centre sections and the 20 questions are made up for the test and built below.
Embeddings: spaCy en_core_web_md document vectors (the average of the word vectors), normalised; cosine.
"""
import importlib, json, re, subprocess, sys
from pathlib import Path
MODEL_URL = "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl"
def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("langchain_text_splitters", "langchain-text-splitters==1.1.3"), ("rank_bm25", "rank_bm25==0.2.2"),
                 ("spacy", "spacy"), ("en_core_web_md", MODEL_URL), ("tiktoken", "tiktoken")):
    ensure(mod, pkg)

import inspect, importlib.metadata as md
import numpy as np, spacy
from rank_bm25 import BM25Okapi
from langchain_text_splitters import RecursiveCharacterTextSplitter as R, TextSplitter
from tiktoken.model import MODEL_TO_ENCODING

HERE = Path(__file__).parent
S = json.loads((HERE / "RAG24.json").read_text())["slides"]
slide = lambda t: next(s for s in S if s.get("title") == t)
plain = lambda x: re.sub(r"\{\{(.+?)\}\}", r"\1", x).replace("!!", "")
vis = lambda sl, kind, k=0: [v for v in sl["visuals"] if v["kind"] == kind][k]
alltext = lambda sl: plain(json.dumps(sl, ensure_ascii=False))
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

check("langchain-text-splitters 1.1.3", md.version("langchain-text-splitters") == "1.1.3")
check("rank_bm25 0.2.2", md.version("rank_bm25") == "0.2.2")
check("en_core_web_md 3.8.0", md.version("en_core_web_md") == "3.8.0")

DOCS = {
"Refunds": """## Refunds
Annual plans can be refunded within 30 days of purchase. After that window, the plan runs to the end of its term and is not refunded. Monthly plans are never refunded, but you can cancel at any time and keep access until the period ends.

To request a refund, open a ticket from the billing page. Refunds go back to the original card and take 5 to 10 business days to appear. If the card has expired, the bank usually forwards the money to the new card.

Partial refunds are not offered for unused seats. Removing seats lowers the next invoice instead.""",
"Seats and billing": """## Seats and billing
Each workspace is billed per seat. A seat is any member who has logged in during the billing period; invited members who never log in are free.

Adding a seat mid-cycle is charged pro rata on the next invoice. Invoices are issued on the 1st of each month and are due within 14 days.

If an invoice is unpaid after 30 days, the workspace becomes read-only. It is unlocked as soon as the payment clears. Workspaces that stay unpaid for 90 days are scheduled for deletion.""",
"Data retention": """## Data retention
Deleted files stay in the trash for 30 days. Admins can restore them from the trash during that time. After 30 days they are purged and cannot be recovered.

Audit logs are kept for 1 year on the Business plan and 3 years on Enterprise. Logs can be exported as CSV from the admin console.

When a workspace is deleted, all its data is removed from primary storage within 7 days. Backups that contain it expire within 35 days.""",
"Security": """## Security
Single sign-on with SAML is available on the Enterprise plan. Okta, Azure AD and Google Workspace are supported as identity providers.

Two-factor authentication can be enforced for the whole workspace by an admin. Members who have not set it up are asked to do so at their next login.

Sessions expire after 12 hours of inactivity. Admins can shorten this to as little as 15 minutes. All data is encrypted at rest with AES-256 and in transit with TLS 1.2 or later.""",
"API limits": """## API limits
The REST API allows 100 requests per minute per token. Bursts above that return HTTP 429 with a Retry-After header.

Enterprise workspaces can ask support to raise the limit to 1,000 requests per minute. Webhooks are not counted against the limit.

Each request body can be at most 10 MB. File uploads larger than that must use the multipart upload endpoint, which accepts files up to 5 GB.""",
"Support": """## Support
Standard support answers by email within 2 business days. Business plans get a first reply within 8 business hours.

Enterprise plans include 24/7 phone support for outages, with a 1-hour response target for severity 1 incidents. Each Enterprise workspace also gets a named account manager.

Status updates during an incident are posted on the status page every 30 minutes until it is resolved.""",
}
QA = [
("How long do I have to get a refund on an annual plan?", "within 30 days of purchase"),
("Can I get a refund on a monthly plan?", "Monthly plans are never refunded"),
("How long does a refund take to show up on my card?", "5 to 10 business days"),
("Do I get money back for seats I am not using?", "Partial refunds are not offered for unused seats"),
("Do invited members who never log in count as a seat?", "invited members who never log in are free"),
("When are invoices due?", "due within 14 days"),
("What happens if an invoice is not paid?", "the workspace becomes read-only"),
("How long are deleted files kept in the trash?", "stay in the trash for 30 days"),
("How long are audit logs kept on Enterprise?", "3 years on Enterprise"),
("When do backups of a deleted workspace expire?", "expire within 35 days"),
("Which identity providers work with SAML single sign-on?", "Okta, Azure AD and Google Workspace"),
("Can an admin require two-factor authentication?", "Two-factor authentication can be enforced"),
("How long before an inactive session expires?", "Sessions expire after 12 hours of inactivity"),
("What is the API rate limit?", "100 requests per minute per token"),
("Can the API rate limit be raised?", "raise the limit to 1,000 requests per minute"),
("What is the largest file I can upload?", "files up to 5 GB"),
("How fast does standard support reply?", "within 2 business days"),
("Is there phone support for outages?", "24/7 phone support for outages"),
("How often is the status page updated during an incident?", "every 30 minutes"),
("What is the maximum request body size for the API?", "at most 10 MB"),
]

nlp = spacy.load("en_core_web_md")
_cache = {}
def emb(t):
    if t not in _cache:
        v = nlp(t).vector; _cache[t] = v / np.linalg.norm(v)
    return _cache[t]
words = lambda t: re.findall(r"\w+", t.lower())
SEPS = ["\n\n", "\n", ". ", " ", ""]
def split(size, overlap):
    sp = R(chunk_size=size, chunk_overlap=overlap, separators=SEPS, keep_separator="end")
    return [c for d in DOCS.values() for c in sp.split_text(d)]
def ranked(C, q, mode):
    if mode == "vec":
        s = np.array([emb(c) for c in C]) @ emb(q)
    else:
        s = BM25Okapi([words(c) for c in C]).get_scores(words(q))
    return s, list(np.argsort(-s, kind="stable"))
def top_k(C, order, k): return [C[i] for i in order[:k]]
def top_budget(C, order, budget):
    got, used = [], 0
    for i in order:
        if got and used + len(C[i]) > budget: break
        got.append(C[i]); used += len(C[i])
    return got
def found(size, overlap=0, mode="vec", k=None, budget=None):
    C = split(size, overlap); n = 0
    for q, a in QA:
        _, o = ranked(C, q, mode)
        got = top_k(C, o, k) if k else top_budget(C, o, budget)
        n += any(a in g for g in got)
    return n

SIZES = (60, 100, 150, 200, 300, 500)
check("corpus: 6 sections, 2,782 characters, 20 questions, each answer in one section",
      len(DOCS) == 6 and sum(map(len, DOCS.values())) == 2782 and len(QA) == 20
      and all(sum(a in d for d in DOCS.values()) == 1 for _, a in QA))

# ---- cover ----
cov = S[0]
K3 = {s: found(s, k=3) for s in SIZES}
B4 = {s: found(s, budget=400) for s in SIZES}
BM = {s: found(s, mode="bm25", budget=400) for s in SIZES}
print("top-3, vectors:", K3); print("400-char budget, vectors:", B4); print("400-char budget, BM25:", BM)
check("cover: 500 finds 19 of 20 at top-3, the most", K3[500] == 19 and max(K3.values()) == 19 and "19 of 20" in cov["hook"])
check("cover: 500 finds 9 at a 400-char budget, the fewest of six sizes", B4[500] == 9 and min(B4.values()) == 9
      and list(B4.values()).count(9) == 1 and "found 9" in cov["hook"] and "six sizes" in cov["hook"])

# ---- one chunk, one vector ----
sl = slide("One chunk, / one [vector]")
ops = vis(sl, "variants")["options"]
n = {s: len(split(s, 0)) for s in (60, 150, 500)}
check("s2: 68 / 27 / 7 chunks at 60 / 150 / 500", n == {60: 68, 150: 27, 500: 7}
      and [o["output"].split()[0] for o in ops] == ["68", "27", "7"])
nlp_avg = nlp("deleted files stay"); manual = np.mean([t.vector for t in nlp_avg], axis=0)
check("s2: spaCy doc vector is the mean of its word vectors", np.allclose(nlp_avg.vector, manual, atol=1e-5))

# ---- small chunks ----
sl = slide("Small chunks / lose the [subject]")
C60 = split(60, 0)
ch = vis(sl, "chunks")["chunks"]
check("s3: the 60-char split cuts '3 | years on Enterprise.'", all(plain(c) in C60 for c in ch)
      and C60.index(plain(ch[1])) == C60.index(plain(ch[0])) + 1)
_, o = ranked(C60, "How long are audit logs kept on Enterprise?", "vec")
check("s3: top hit for the audit-log question is 'years on Enterprise.'", C60[o[0]] == "years on Enterprise." and "years on Enterprise." in alltext(sl))
_, o = ranked(C60, "When are invoices due?", "vec")
check("s3: top hit for 'When are invoices due?' is 'invoice.'", C60[o[0]] == "invoice." and "\"invoice.\"" in " ".join(sl["bullets"]))

# ---- big chunks ----
sl = slide("Big chunks / [blur] facts")
q = "Can I get a refund on a monthly plan?"
C150 = split(150, 0); s, o = ranked(C150, q, "vec")
check("s4: at 150 the top hit is the monthly-plan sentence, 0.925",
      C150[o[0]].startswith("Monthly plans are never refunded") and round(float(s[o[0]]), 3) == 0.925 and "0.925" in alltext(sl))
C500 = split(500, 0); s, o = ranked(C500, q, "vec")
check("s4: at 500 'Seats and billing' ranks 1st (0.918), Refunds 2nd (0.916)",
      C500[o[0]].startswith("## Seats and billing") and C500[o[1]].startswith("## Refunds")
      and round(float(s[o[0]]), 3) == 0.918 and round(float(s[o[1]]), 3) == 0.916
      and "0.918" in alltext(sl) and "0.916" in alltext(sl))
check("s4: the Seats and billing section holds no refund rule", "refund" not in C500[o[0]].lower())

# ---- overlap ----
sl = slide("Overlap repeats / whole [pieces]")
t = alltext(sl)
a0, a1 = split(200, 0), split(200, 40)
check("s5: 200/0 and 200/40 both 21 chunks, 2,755 characters", len(a0) == len(a1) == 21 and sum(map(len, a0)) == sum(map(len, a1)) == 2755 and "2,755" in t)
b0, b1 = split(60, 0), split(60, 12)
check("s5: 60/0 -> 60/12: 68 -> 70 chunks, 2,708 -> 2,925 characters (+8%)",
      (len(b0), len(b1), sum(map(len, b0)), sum(map(len, b1))) == (68, 70, 2708, 2925)
      and round(100 * (2925 / 2708 - 1)) == 8 and "2,925" in t and "8%" in t)
check("s5: with overlap 12, 'plan and 3 years on Enterprise.' is one chunk", "plan and 3 years on Enterprise." in b1 and "plan and 3 years on Enterprise." in t)
check("s5: overlap 12 at 60: top-3 found 7 -> 8", found(60, 0, k=3) == 7 and found(60, 12, k=3) == 8 and "7 to 8" in t)

# ---- tokens ----
sl = slide("Size in the / model's [tokens]")
sig = inspect.signature(TextSplitter.from_tiktoken_encoder)
check("s6: from_tiktoken_encoder takes model_name, chunk_size, chunk_overlap",
      {"model_name", "encoding_name"} <= set(sig.parameters) and "chunk_size" in plain(vis(sl, "code")["code"]))
check("s6: text-embedding-3-small uses cl100k_base", MODEL_TO_ENCODING["text-embedding-3-small"] == "cl100k_base")
check("s6: TextSplitter defaults 4000 / 200, measured with len", inspect.signature(TextSplitter.__init__).parameters["chunk_size"].default == 4000
      and inspect.signature(TextSplitter.__init__).parameters["chunk_overlap"].default == 200)

# ---- top-3 ----
sl = slide("Top-3 makes / big chunks [win]")
rows = vis(sl, "bars")["rows"]
check("s7: top-3 bars match the run", {int(r["label"]): r["value"] for r in rows} == K3)
check("s7: at 500, top 3 is 3 of 7 chunks", "3 of 7" in alltext(sl) and len(C500) == 7)

# ---- budget ----
sl = slide("Cap the context / [budget]")
rows = vis(sl, "bars")["rows"]
check("s8: 400-char budget bars match the run", {int(r["label"]): r["value"] for r in rows} == B4)
check("s8: 100 and 150 find 13, the most", B4[100] == B4[150] == 13 == max(B4.values()))

# ---- retrievers ----
sl = slide("Each retriever / has its [own] best")
t = alltext(sl)
check("s9: BM25 at 400: 200 and 300 find 18 (the most), 500 finds 17, 60 finds 11",
      BM[200] == BM[300] == 18 == max(BM.values()) and BM[500] == 17 and BM[60] == 11 and "18 of 20" in t and "17" in t and "11" in t)
check("s9: vectors at 400: 100 and 150 find 13 of 20", "13 of 20" in t)

# ---- teaser/cheat sheet sanity ----
check("cheat sheet has 4-7 rows", 4 <= len(S[-2]["rows"]) <= 7)

print("langchain-text-splitters", md.version("langchain-text-splitters"), "| rank_bm25", md.version("rank_bm25"),
      "| spacy", spacy.__version__, "| en_core_web_md", md.version("en_core_web_md"))
print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
