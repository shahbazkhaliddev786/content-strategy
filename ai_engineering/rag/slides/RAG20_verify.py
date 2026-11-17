"""Re-run every example on the RAG #20 slides (chunking tables) and check the slide text against it.

Run: python3 ai_engineering/rag/slides/RAG20_verify.py
Installs what it needs on first run: langchain-text-splitters 1.1.3, docling-core[chunking] 2.107.1, rank_bm25.
The sample table, the row-group chunker (exec'd from the slide), the BM25 setup and the SQLite query are below.
"""
import importlib, json, re, sqlite3, subprocess, sys, warnings
from itertools import groupby
from pathlib import Path

def ensure(mod, pkg):
    try:
        importlib.import_module(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", pkg], check=True)
for mod, pkg in (("langchain_text_splitters", "langchain-text-splitters==1.1.3"),
                 ("docling_core", "docling-core[chunking]==2.107.1"),
                 ("tree_sitter", "docling-core[chunking]==2.107.1"),
                 ("rank_bm25", "rank_bm25")):
    ensure(mod, pkg)
warnings.filterwarnings("ignore")

import importlib.metadata as md_
from langchain_text_splitters import RecursiveCharacterTextSplitter as R
from rank_bm25 import BM25Okapi
from docling_core.types.doc import DoclingDocument, TableData, TableCell
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.transforms.chunker.hierarchical_chunker import ChunkingDocSerializer, ChunkingSerializerProvider
from docling_core.transforms.chunker.tokenizer.base import BaseTokenizer
from docling_core.transforms.serializer.markdown import MarkdownTableSerializer

HERE = Path(__file__).parent
S = json.loads((HERE / "RAG20.json").read_text())["slides"]
slide = lambda t: next(s for s in S if s.get("title") == t)
plain = lambda x: x.replace("{{", "").replace("}}", "").replace("!!", "")
codes = lambda sl: [plain(v["code"]) for v in sl["visuals"] if v["kind"] == "code"]
def text_of(sl):
    return plain(json.dumps(sl, ensure_ascii=False))
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

check("langchain-text-splitters 1.1.3", md_.version("langchain-text-splitters") == "1.1.3")
check("docling-core 2.107.1", md_.version("docling-core") == "2.107.1")

# ---- sample table (made up for the demo) ----
TITLE = "Table 4: Storage prices per GB, 2026"
HEADER = ["Region", "Tier", "Storage", "Egress", "Days"]
P = {"Virginia": [("0.021", "0.09"), ("0.012", "0.09"), ("0.004", "0.09")],
     "Oregon": [("0.021", "0.09"), ("0.012", "0.09"), ("0.004", "0.09")],
     "Frankfurt": [("0.024", "0.08"), ("0.014", "0.10"), ("0.005", "0.12")],
     "London": [("0.024", "0.08"), ("0.014", "0.10"), ("0.005", "0.12")],
     "Mumbai": [("0.022", "0.11"), ("0.013", "0.11"), ("0.005", "0.13")],
     "Tokyo": [("0.025", "0.11"), ("0.015", "0.12"), ("0.006", "0.14")]}
ROWS = [[reg, tier, s, e, days] for reg, v in P.items()
        for (tier, days), (s, e) in zip([("Hot", "0"), ("Cool", "30"), ("Cold", "90")], v)]
mdrow = lambda cells: "| " + " | ".join(cells) + " |"
SEP = "|" + "---|" * len(HEADER)
MD = TITLE + "\n\n" + "\n".join([mdrow(HEADER), SEP] + [mdrow(r) for r in ROWS])
HTML = ("<table><caption>" + TITLE + "</caption><tr>" + "".join(f"<th>{h}</th>" for h in HEADER) + "</tr>"
        + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in ROWS) + "</table>")
check("18 rows", len(ROWS) == 18)

# ---- slide: Chunk 3 has no header ----
LC = R(chunk_size=300, chunk_overlap=0).split_text(MD)
sl = slide("Chunk 3 has / no [header]"); c = codes(sl)
check("recursive: 4 chunks", len(LC) == 4)
check("recursive: chunk 1 is the title alone", LC[0] == TITLE == c[0])
check("recursive: chunk 2 starts with the header", LC[1].startswith(mdrow(HEADER)))
check("recursive: chunk 3 starts with the slide rows", LC[2].startswith(c[1]))
check("recursive: chunks 3 and 4 have no header or title", all("Egress" not in x and "Table 4" not in x for x in LC[2:]))
check("chunk 3 holds Frankfurt Cold 0.005 0.12 90", "| Frankfurt | Cold | 0.005 | 0.12 | 90 |" in LC[2])

# ---- slide: One-line HTML ----
HC = R(chunk_size=300, chunk_overlap=0).split_text(HTML)
sl = slide("One-line HTML / cuts [mid-row]"); c = codes(sl)
check("html: no newline, no space between cells", "\n" not in HTML and "> <" not in HTML)
check("html: end of chunk 2 matches", HC[1].endswith(c[0].replace("\n", "")))
check("html: start of chunk 3 matches", HC[2].startswith(c[1]))
check("html: chunk 1 ends at 'per GB,'", HC[0].endswith("per GB,"))
check("html: 0.09 is Virginia Cold egress", ROWS[2][:2] == ["Virginia", "Cold"] and ROWS[2][3] == "0.09")

# ---- slide: Whole rows, grouped by key (exec the slide code) ----
sl = slide("Whole rows, / grouped by [key]")
ns = {"groupby": groupby}; exec(codes(sl)[0], ns)
RG = ns["chunk_table"](TITLE, HEADER, ROWS)
check("row groups: 6 chunks at 300", len(RG) == 6)
check("repeat slide: chunk 3 matches", RG[2] == codes(slide("Repeat the / [header]"))[0])
check("every row-group chunk has title and header", all(x.startswith(TITLE + "\n" + mdrow(HEADER)) for x in RG))
top = len("\n".join([TITLE, mdrow(HEADER), SEP]))  # the three lines, newlines between them
check("title+header cost 102 chars", top == 102)
share = [top / len(x) for x in RG]
check("about a third of the 300-character limit", 0.32 <= top / 300 <= 0.35)
big = ns["chunk_table"](TITLE, HEADER, ROWS, max_chars=150)
check("a key bigger than max_chars stays one oversized chunk", len(big) == 6 and all(len(x) > 150 for x in big))

# ---- slide: Docling ----
class Words(BaseTokenizer):
    max_tokens: int = 100
    def count_tokens(self, text): return len(text.split())
    def get_max_tokens(self): return self.max_tokens
    def get_tokenizer(self): return None
class MDTables(ChunkingSerializerProvider):
    def get_serializer(self, doc):
        return ChunkingDocSerializer(doc=doc, table_serializer=MarkdownTableSerializer())
def build(caption, header, rows):
    doc = DoclingDocument(name="prices")
    cells = [TableCell(text=v, start_row_offset_idx=r, end_row_offset_idx=r + 1, start_col_offset_idx=c,
                       end_col_offset_idx=c + 1, column_header=(r == 0))
             for r, row in enumerate([header] + rows) for c, v in enumerate(row)]
    cap = doc.add_text(label="caption", text=caption)
    doc.add_table(data=TableData(num_rows=len(rows) + 1, num_cols=len(header), table_cells=cells), caption=cap)
    return doc
check("repeat_table_header defaults to True", HybridChunker.model_fields["repeat_table_header"].default is True)
DC = [x.text for x in HybridChunker(tokenizer=Words(max_tokens=100), serializer_provider=MDTables()).chunk(build(TITLE, HEADER, ROWS))]
trim = lambda t: "\n".join(re.sub(r"-{2,}", "---", re.sub(r" +", " ", l)) for l in t.strip().splitlines())
sl = slide("Docling repeats / the [header]")
check("docling: 3 chunks", len(DC) == 3)
check("docling: chunk 2 starts with slide lines (padding trimmed)", trim(DC[1]).startswith(codes(sl)[0]))
check("docling: header in every chunk", all("| Region" in x and "Egress" in x for x in DC))
check("docling: caption in chunk 1 only", TITLE in DC[0] and all(TITLE not in x for x in DC[1:]))
check("docling: Frankfurt Hot ends chunk 1", trim(DC[0]).splitlines()[-1] == "| Frankfurt | Hot | 0.024 | 0.08 | 0 |")
tri = [x.text for x in HybridChunker(tokenizer=Words(max_tokens=100)).chunk(build(TITLE, HEADER, ROWS))]
check("default serializer writes triplets", "Virginia, Tier = Hot." in tri[0])

# ---- slide: Wide rows lose their key ----
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WR = [[reg] + [str(100 + i * 7 + j) for j in range(12)] for i, reg in enumerate(P)]
WC = [x.text for x in HybridChunker(tokenizer=Words(max_tokens=40), serializer_provider=MDTables())
      .chunk(build("Table 5: GB stored per month, 2026", ["Region"] + MON, WR))]
sl = slide("Wide rows lose / their [key]"); c = codes(sl)
check("wide: 7 chunks", len(WC) == 7)
check("wide: chunk 1 first lines", "\n".join(l for l in WC[0].strip().splitlines() if l.strip()).startswith(c[0]))
check("wide: chunk 3 first lines", WC[2].strip().startswith(c[1]))
check("wide: no Region column after chunk 1", all("Region" not in x and "Virginia" not in x for x in WC[1:]))

# ---- slide: Search finds the rows ----
tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
def top_hit(chunks, q):
    sc = BM25Okapi([tok(x) for x in chunks]).get_scores(tok(q))
    return max(range(len(chunks)), key=lambda i: sc[i])
Q1 = "What is the egress price for cold storage in Frankfurt?"
sl = slide("Search finds / the [rows]")
check("query on slide", Q1 in sl["text"])
check("recursive: top hit chunk 3, Frankfurt", top_hit(LC, Q1) == 2 and "Frankfurt" in LC[2])
check("row groups: top hit chunk 3, Frankfurt", top_hit(RG, Q1) == 2 and "Frankfurt" in RG[2])
check("recursive chunk 3 has no column names", "Egress" not in LC[2] and "Region" not in LC[2])

# ---- slide: Across rows, use SQL ----
Q2 = "Which region has the cheapest egress for the Cold tier?"
sl = slide("Across rows, / use [SQL]")
check("Q2 on slide", Q2 in sl["text"])
check("6 Cold rows, one per row-group chunk", sum(r[1] == "Cold" for r in ROWS) == 6 and [x.count("| Cold |") for x in RG] == [1] * 6)
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE prices(region, tier, storage REAL, egress REAL, days INT)")
db.executemany("INSERT INTO prices VALUES (?,?,?,?,?)", ROWS)
sql = codes(sl)[0].split("--")[0]
res = db.execute(sql).fetchall()
check("SQL result: Virginia 0.09, Oregon 0.09", res == [("Virginia", 0.09), ("Oregon", 0.09)])

check("recursive: 12 of 18 rows sit in chunks with no header", sum(x.count("\n") + 1 for x in LC[2:]) == 12)
# ---- cover numbers ----
cov = S[0]["hook"]
check("cover: 300-character split, 0.005, 0.12 and 90", "300-character" in cov and "0.005, 0.12 and 90" in cov)

print("ALL PASS" if all(ok) else f"{ok.count(False)} FAILED")
