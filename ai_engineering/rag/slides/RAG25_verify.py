"""Re-run every example on the RAG #25 slides (what an embedding is) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG25_verify.py
Installs what it needs on first run: spaCy, en_core_web_md 3.8.0 and en_core_web_lg 3.8.0 (from the spaCy
models release on GitHub), rank_bm25 0.2.2, scikit-learn.
The five help-centre docs and the four questions are made up for the test and built below.
Embedding: the average of the word vectors of a text's content words (spaCy stop words and punctuation
dropped); cosine similarity.
"""
import importlib, json, re, subprocess, sys
from pathlib import Path
REL = "https://github.com/explosion/spacy-models/releases/download/"
def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("spacy", "spacy"), ("rank_bm25", "rank_bm25==0.2.2"), ("sklearn", "scikit-learn"),
                 ("en_core_web_md", REL + "en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl"),
                 ("en_core_web_lg", REL + "en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl")):
    ensure(mod, pkg)

import importlib.metadata as im
import numpy as np, spacy
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import CountVectorizer

HERE = Path(__file__).parent
S = json.loads((HERE / "RAG25.json").read_text())["slides"]
slide = lambda t: next(s for s in S if s.get("title") == t)
plain = lambda x: re.sub(r"\{\{(.+?)\}\}", r"\1", x).replace("!!", "")
alltext = lambda sl: plain(json.dumps(sl, ensure_ascii=False))
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

check("en_core_web_md 3.8.0", im.version("en_core_web_md") == "3.8.0")
check("en_core_web_lg 3.8.0", im.version("en_core_web_lg") == "3.8.0")
check("rank_bm25 0.2.2", im.version("rank_bm25") == "0.2.2")
MD, LG = spacy.load("en_core_web_md"), spacy.load("en_core_web_lg")

def embed(text, nlp=MD):
    doc = nlp(text)
    return np.mean([t.vector for t in doc if not t.is_stop and not t.is_punct and t.has_vector], axis=0)
def cos(a, b):
    return float(a @ b / np.linalg.norm(a) / np.linalg.norm(b))

DOCS = {
    "Refunds": "Refunds are issued to the original card within 5 business days.",
    "Password": "Reset your password from the login page.",
    "Invoices": "Invoices are emailed on the first day of each month.",
    "Export": "Export your data as a CSV file from Settings.",
    "Seats": "Add team members from the Seats page.",
}
Q = {"How do I get my money back?": "Refunds", "Can I download everything as a spreadsheet?": "Export",
     "When will I be billed?": "Invoices", "How do I invite a colleague?": "Seats"}
f3 = lambda x: f"{x:.3f}"

# Cover
cover = S[0]
for q, ans in Q.items():
    sc = {k: cos(embed(q), embed(d)) for k, d in DOCS.items()}
    if q.startswith("How do I get"):
        check("cover: refund question ranks the refund doc 1st of 5, BM25 0", max(sc, key=sc.get) == "Refunds" and "1st of 5" in cover["hook"])

# Slide 2: text in, numbers out
s2 = slide("Text becomes / [numbers]"); code = s2["visuals"][0]["code"]
v = embed("refund")
check("slide 2: shape (300,)", v.shape == (300,) and "(300,)" in code)
check("slide 2: first 4 values", all(f"{x:.2f}" in code for x in v[:4]))
check("slide 2: md vectors are 300-wide", MD.vocab.vectors.shape[1] == 300 and "300 numbers" in s2["text"])

# Slide 3: any length
s3 = slide("Every text gets / [300] numbers")
check("slide 3: word, sentence, all docs -> (300,)",
      embed("refund").shape == embed(DOCS["Refunds"]).shape == embed(" ".join(DOCS.values())).shape == (300,))

# Slide 4: sparse vs dense
s4 = slide("Sparse vs / [dense] vectors"); t4 = alltext(s4)
cv = CountVectorizer().fit(DOCS.values()); qx = cv.transform(["How do I get my money back?"])
check("slide 4: 34-word vocabulary", len(cv.vocabulary_) == 34 and "34 slots" in t4 and "0 of 34" in t4)
check("slide 4: query keyword vector all zeros", qx.nnz == 0)
check("slide 4: dense 300 of 300 non-zero", int((embed("How do I get my money back?") != 0).sum()) == 300 and "300 of 300" in t4)

# Slide 5: BM25
tok = lambda t: re.findall(r"\w+", t.lower())
bm = BM25Okapi([tok(d) for d in DOCS.values()])
check("slide 5: BM25 0.0 on all 5 docs", all(s == 0 for s in bm.get_scores(tok("How do I get my money back?"))))
check("slide 5: no shared word with refund doc", not set(tok("How do I get my money back?")) & set(tok(DOCS["Refunds"])))

# Slide 6: cosine scores
s6 = slide("Close in / [meaning]"); t6 = alltext(s6)
sc = {k: cos(embed("How do I get my money back?"), embed(d)) for k, d in DOCS.items()}
check("slide 6: all five scores on the slide", all(f3(x) in t6 for x in sc.values()))
order = sorted(sc, key=sc.get, reverse=True)
check("slide 6: order Refunds, Invoices, Seats, Export, Password", order == ["Refunds", "Invoices", "Seats", "Export", "Password"])
mw = MD("money")[0].vector
rw = {t.lower_: cos(mw, t.vector) for t in MD(DOCS["Refunds"]) if not t.is_stop and not t.is_punct and t.has_vector}
check("slide 6: business, refunds, card are the refund doc's 3 words closest to 'money'",
      sorted(rw, key=rw.get, reverse=True)[:3] == ["business", "refunds", "card"])
check("slide 6: the question's content words are just 'money'",
      [t.lower_ for t in MD("How do I get my money back?") if not t.is_stop and not t.is_punct] == ["money"])

# Slide 8: four questions
s8 = slide("Four questions, / no shared [content] words"); t8 = alltext(s8)
for q, ans in Q.items():
    sc = {k: cos(embed(q), embed(d)) for k, d in DOCS.items()}
    top = max(sc, key=sc.get)
    qc = {t.lower_ for t in MD(q) if not t.is_stop and not t.is_punct}
    dc = {t.lower_ for t in MD(DOCS[ans]) if not t.is_stop and not t.is_punct}
    check(f"slide 8: {q} -> {ans} {f3(sc[top])}, no shared content word",
          top == ans and f3(sc[top]) in t8 and not qc & dc)
bs = bm.get_scores(tok("How do I invite a colleague?"))
bs2 = bm.get_scores(tok("Can I download everything as a spreadsheet?"))
check("slide 8: BM25 scores only Export for the spreadsheet question, through 'as' and 'a'",
      [k for k, s in zip(DOCS, bs2) if s > 0] == ["Export"] and set(tok("Can I download everything as a spreadsheet?")) & set(tok(DOCS["Export"])) == {"as", "a"})
check("slide 8: BM25 scores only Export for the colleague question, through 'a'",
      [k for k, s in zip(DOCS, bs) if s > 0] == ["Export"] and set(tok("How do I invite a colleague?")) & set(tok(DOCS["Export"])) == {"a"})

# Slide 9: negation and word order
c_neg = cos(embed("Monthly plans can be refunded."), embed("Monthly plans cannot be refunded."))
c_ord = cos(embed("The customer refunds the company."), embed("The company refunds the customer."))
check("slide 9: negation 1.000", f3(c_neg) == "1.000")
check("slide 9: 'can' and 'not' are stop words", [t.is_stop for t in MD("cannot")] == [True, True])
check("slide 9: word order 1.000", f3(c_ord) == "1.000")

# Slide 10: mixing models
s10 = slide("Don't mix / [models]"); t10 = alltext(s10)
q = "How do I invite a colleague?"
lgl = {k: cos(embed(q, LG), embed(d, LG)) for k, d in DOCS.items()}
mix = {k: cos(embed(q, MD), embed(d, LG)) for k, d in DOCS.items()}
r_mix = sorted(mix, key=mix.get, reverse=True)
check("slide 10: lg/lg -> Seats 0.477", max(lgl, key=lgl.get) == "Seats" and f3(lgl["Seats"]) in t10)
check("slide 10: md query vs lg docs -> Invoices 0.462, Seats 2nd", r_mix[:2] == ["Invoices", "Seats"] and f3(mix["Invoices"]) in t10)
check("slide 10: 'refund' identical in md and lg", np.allclose(MD("refund")[0].vector, LG("refund")[0].vector))

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
