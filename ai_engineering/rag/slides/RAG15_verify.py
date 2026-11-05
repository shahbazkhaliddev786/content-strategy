"""Re-run every LangChain example on the RAG #15 slides and check the slide text against it.

Needs: pip install langchain-text-splitters==1.1.3 tiktoken
Run:   python3 ai_engineering/rag/slides/RAG15_verify.py
"""
import io, json, logging, re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter as R, Language
import langchain_text_splitters as lts
from tiktoken.model import MODEL_TO_ENCODING

post = json.load(open(Path(__file__).with_name("RAG15.json")))
S = post["slides"]
plain = lambda s: re.sub(r"!!(.+?)!!", r"\1", s)
ok = []
def check(name, cond):
    ok.append(cond); print(("PASS " if cond else "FAIL ") + name)

TEXT = ("Refunds are accepted within 30 days of purchase. After 30 days, "
        "refunds need manager approval. Digital items are never refundable.")
SEPS = ["\n\n", "\n", ". ", " ", ""]

d = R()
check("defaults: separators, 4000/200, len", d._separators == ["\n\n", "\n", " ", ""] and d._chunk_size == 4000 and d._chunk_overlap == 200 and d._length_function is len and d._keep_separator is True)

# slide 3 after: overlap moves whole pieces
o50 = R(chunk_size=100, chunk_overlap=50, separators=SEPS, keep_separator="end").split_text(TEXT)
o40 = R(chunk_size=100, chunk_overlap=40, separators=SEPS, keep_separator="end").split_text(TEXT)
rep = "After 30 days, refunds need manager approval."
check("s3: overlap=50 repeats the 45-char sentence", len(rep) == 45 and o50[1].startswith(rep) and rep in o50[0])
check("s3: overlap=40 repeats nothing", not any(o40[1].startswith(x) for x in o40[0].split(". ")) and o40[1] == "Digital items are never refundable.")

# slide 4: default cuts
got = R(chunk_size=60, chunk_overlap=0).split_text(TEXT)
check("s4: default chunks match slide", got == [plain(c) for c in S[3]["visuals"][0]["chunks"]])

# slide 5: keep_separator variants (chunk 2)
want = {o["setting"]: plain(o["output"]) for o in S[4]["visuals"][1]["options"]}
for setting, ks in (("keep_separator=True", True), ('keep_separator="end"', "end"), ("keep_separator=False", False)):
    c2 = R(chunk_size=60, chunk_overlap=0, separators=SEPS, keep_separator=ks).split_text(TEXT)[1]
    check(f"s5: {setting} chunk 2", c2 == want[setting])
ends = R(chunk_size=60, chunk_overlap=0, separators=SEPS, keep_separator="end").split_text(TEXT)
check("s5: 'end' gives one whole sentence per chunk", all(c.endswith(".") for c in ends) and len(ends) == 3)
ab = R(chunk_size=40, chunk_overlap=0, separators=SEPS, keep_separator="end").split_text(
    "For refunds over $500, e.g. laptops, ask Dr. Patel. She approves them within 2 days.")
check("s9: '. ' splits after e.g. and Dr.", ab[0].endswith("e.g.") and ab[1].endswith("Dr. Patel."))

# slide 6: the "" last resort
URL = "https://example.com/policies/refunds/international/eu-customers-2026-update"
log = io.StringIO(); logging.getLogger("langchain_text_splitters").addHandler(logging.StreamHandler(log))
w = R(chunk_size=40, chunk_overlap=0).split_text(URL)
wo = R(chunk_size=40, chunk_overlap=0, separators=["\n\n", "\n", " "]).split_text(URL)
check("s6: URL is 75 characters", len(URL) == 75)
check("s6: with '' cut mid-word, as shown", w == [plain(c) for c in S[5]["visuals"][0]["chunks"]])
check("s6: without '' one 75-char chunk, as shown", wo == [plain(c) for c in S[5]["visuals"][1]["chunks"]] and len(wo[0]) == 75)
check("s6: no warning logged", log.getvalue() == "")

# slide 7: token sizing
import inspect
from langchain_text_splitters.base import TextSplitter
sig = inspect.signature(TextSplitter.from_tiktoken_encoder)
check("s7: from_tiktoken_encoder defaults to gpt2", sig.parameters["encoding_name"].default == "gpt2")
check("s7: text-embedding-3 uses cl100k_base", MODEL_TO_ENCODING["text-embedding-3-small"] == MODEL_TO_ENCODING["text-embedding-3-large"] == "cl100k_base")
check("s7: from_huggingface_tokenizer exists", hasattr(TextSplitter, "from_huggingface_tokenizer"))

# slide 8: Markdown preset
DOC = ("## Refunds\n\nRefunds are accepted within 30 days of purchase. After 30 days, refunds need manager approval."
       "\n\n## Shipping\n\nOrders ship within 2 business days. Express shipping costs extra.")
dm = R(chunk_size=120, chunk_overlap=0).split_text(DOC)
mm = R.from_language(Language.MARKDOWN, chunk_size=120, chunk_overlap=0).split_text(DOC)
check("s8: defaults glue '## Shipping' to the refunds chunk", dm[0].endswith("## Shipping") and dm[1].startswith("Orders ship"))
check("s8: Markdown keeps each heading with its section", mm[0].startswith("## Refunds") and mm[0].endswith("approval.") and mm[1].startswith("## Shipping"))
seps = R.get_separators_for_language(Language.MARKDOWN)
check("s8: Markdown order is headings, code fences, rules, paragraphs", seps[0] == "\n#{1,6} " and seps[1] == "```\n" and seps[5] == "\n\n")
vals = [l.value for l in Language]
check("s8: 28 presets incl. python, html, latex", len(vals) == 28 and {"python", "html", "latex", "markdown"} <= set(vals))
check("s9: NLTKTextSplitter exists", hasattr(lts, "NLTKTextSplitter"))

# slide 9: the all-in-one config (needs the cl100k_base file; tiktoken downloads it on first use)
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
code = next(v["code"] for sl in S if sl.get("title") == "Put it all / [together]" for v in sl["visuals"])
scope = {"RecursiveCharacterTextSplitter": R}
exec(code, scope)
sp = scope["splitter"]
check("s9: config runs; 500/100, keep_separator end, sentence separator", sp._chunk_size == 500 and sp._chunk_overlap == 100 and sp._keep_separator == "end" and ". " in sp._separators)
check("s9: the 28-token refund paragraph stays one chunk at 500", len(enc.encode(TEXT)) == 28 and sp.split_text(TEXT) == [TEXT])
mdt = R.from_tiktoken_encoder(model_name="text-embedding-3-small", separators=R.get_separators_for_language(Language.MARKDOWN),
                              is_separator_regex=True, chunk_size=30, chunk_overlap=0).split_text(DOC)
check("s9: Markdown separators + token sizing keep each heading", [c.split("\n")[0] for c in mdt] == ["## Refunds", "## Shipping"])
ratios = [len(t) / len(enc.encode(t)) for t in (Path(__file__).parents[1].joinpath(f).read_text() for f in ("RAG_Curriculum (1).md", "MODULE_2_CALENDAR.md"))]
check("s7: ~4 characters per cl100k token on English docs (4,000 chars ~ 1,000 tokens)", all(3.8 <= r <= 4.6 for r in ratios))

import importlib.metadata as md
print("langchain-text-splitters", md.version("langchain-text-splitters"))
print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
