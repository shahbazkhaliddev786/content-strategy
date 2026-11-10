#!/usr/bin/env python3
"""Render a carousel post (JSON) into the LinkedIn PDF and the Instagram slide set, with headless Chrome.

Usage:
    python3 renderer/render.py ai_engineering/rag/slides/RAG15.json --out out/RAG15
    python3 renderer/render.py POST.json --out DIR --cover-labels ai_engineering/rag/COVER_LABELS.md

Writes to DIR:
    linkedin/slide_01.png ... and linkedin/<post>.pdf   every slide (10-15), posted as a LinkedIn document
    instagram/slide_01.png ...                           at most 10 slides (Buffer's Instagram limit):
                                                         slides marked "instagram": false are left out
    report.json                                          checks for both sets
Exits with code 1 when any check fails; report.json says which.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
MIN_FONT_PX = 24          # smallest text allowed anywhere on a slide
MAX_BODY_WORDS = 85       # all prose on a body slide (code and example chunks don't count)
SLIDES_MIN, SLIDES_MAX = 10, 15   # LinkedIn document, teaser included
INSTAGRAM_MAX = 10                # Buffer publishes at most 10 images per Instagram carousel

# ---------- text filters ----------

def _keep_hyphens(html: str) -> str:
    """Hyphenated words (GPT-2, parent-document) never break at the hyphen."""
    return re.sub(r"(?<![\w-])(\w+(?:-\w+)+)", r'<span class="nw">\1</span>', html)


def _code_spans(s: str, nowrap: bool = False) -> str:
    """Escape text and turn `code` into inline code spans."""
    plain = (lambda t: _keep_hyphens(str(escape(t)))) if nowrap else (lambda t: str(escape(t)))
    out, pos = [], 0
    for m in re.finditer(r"`([^`]+)`", s):
        out.append(plain(s[pos:m.start()]))
        out.append(f'<code class="ic">{escape(m.group(1))}</code>')
        pos = m.end()
    out.append(plain(s[pos:]))
    return "".join(out)


def inline(s) -> Markup:
    return Markup(_code_spans(str(s or ""), nowrap=True))


def titlehl(s) -> Markup:
    """[word] -> highlight, ' / ' -> line break, `x` -> inline code."""
    lines = []
    for line in str(s or "").split(" / "):
        parts, pos = [], 0
        for m in re.finditer(r"\[([^\]]+)\]", line):
            parts.append(_code_spans(line[pos:m.start()]))
            parts.append(f"<mark>{_code_spans(m.group(1))}</mark>")
            pos = m.end()
        parts.append(_code_spans(line[pos:]))
        lines.append("".join(parts))
    return Markup("<br>".join(lines))


def chunktext(s) -> Markup:
    """!!x!! -> emphasised span (red on a bad cut, green on a good one)."""
    s = str(s or "")
    out, pos = [], 0
    for m in re.finditer(r"!!(.+?)!!", s):
        out.append(_code_spans(s[pos:m.start()]))
        out.append(f'<span class="em">{_code_spans(m.group(1))}</span>')
        pos = m.end()
    out.append(_code_spans(s[pos:]))
    return Markup("".join(out))


_TOKEN = re.compile(
    r'(?P<c>#[^\n]*)'
    r'|(?P<s>"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')'
    r'|(?P<n>\b\d+(?:\.\d+)?\b)'
)


def _tokens(src: str) -> str:
    out, pos = [], 0
    for m in _TOKEN.finditer(src):
        out.append(str(escape(src[pos:m.start()])))
        out.append(f'<span class="{m.lastgroup}">{escape(m.group())}</span>')
        pos = m.end()
    out.append(str(escape(src[pos:])))
    return "".join(out)


def codehl(src) -> Markup:
    """Light syntax colouring; {{x}} marks the part of the code the slide is about."""
    src = str(src or "")
    out, pos = [], 0
    for m in re.finditer(r"\{\{(.+?)\}\}", src):
        out.append(_tokens(src[pos:m.start()]))
        out.append(f'<mark class="cm">{_tokens(m.group(1))}</mark>')
        pos = m.end()
    out.append(_tokens(src[pos:]))
    return Markup("".join(out))


# ---------- in-page fitting and measuring ----------

FIT_JS = r"""
async () => {
  await document.fonts.ready;
  const out = [];
  for (const slide of document.querySelectorAll('.slide')) {
    const r = {id: slide.id, type: slide.dataset.type};
    const t = slide.querySelector('[data-max-lines]');
    if (t) {
      const max = +t.dataset.maxLines, min = +t.dataset.min;
      let size = parseFloat(getComputedStyle(t).fontSize);
      const lines = () => Math.round(t.getBoundingClientRect().height / parseFloat(getComputedStyle(t).lineHeight));
      const fits = () => lines() <= max && t.scrollWidth <= t.clientWidth + 1;
      while (!fits() && size > min) { size -= 4; t.style.fontSize = size + 'px'; }
      r.title_px = size; r.title_lines = lines(); r.title_max_lines = max; r.title_fits = fits();
    }
    const stage = slide.querySelector('.stage');
    const pres = [...slide.querySelectorAll('pre.code')];
    const over = () => stage.scrollHeight > stage.clientHeight + 1 || pres.some(p => p.scrollWidth > p.clientWidth + 1);
    let s = 1;
    while (over() && s > 0.8) { s = Math.round((s - 0.04) * 100) / 100; slide.style.setProperty('--s', s); }
    if (t && over()) {
      // still too tall at the smallest scale: shrink the big title too, down to its minimum
      let size = parseFloat(getComputedStyle(t).fontSize);
      const min = +t.dataset.min;
      while (over() && size > min) { size -= 6; t.style.fontSize = size + 'px'; }
      r.title_px = size;
      r.title_lines = Math.round(t.getBoundingClientRect().height / parseFloat(getComputedStyle(t).lineHeight));
    }
    r.scale = s;
    r.overflow = over();
    const sb = slide.getBoundingClientRect();
    let minFont = 999, outside = false;
    const w = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const n = w.currentNode;
      if (!n.textContent.trim()) continue;
      minFont = Math.min(minFont, parseFloat(getComputedStyle(n.parentElement).fontSize));
      const range = document.createRange(); range.selectNodeContents(n);
      for (const b of range.getClientRects()) {
        if (b.right > sb.right - 40 || b.left < sb.left + 40 || b.bottom > sb.bottom - 30) outside = true;
      }
    }
    r.min_font_px = minFont;
    r.text_outside_margins = outside;
    out.push(r);
  }
  return out;
}
"""


def _launch(p):
    for kwargs in ({"channel": "chrome"}, {}):
        try:
            return p.chromium.launch(**kwargs)
        except Exception:
            continue
    return p.chromium.launch(executable_path="/usr/bin/google-chrome")


def _words(s: str) -> int:
    return len(re.findall(r"[\w'\"().=,\\-]+", re.sub(r"`[^`]*`", "x", s or "")))


def _prose(slide: dict) -> list[str]:
    """Every piece of reading text on a body slide (not code, not example chunks)."""
    out = [slide.get("text", ""), slide.get("after", ""), *slide.get("bullets", [])]
    for v in slide.get("visuals", []):
        kind = v.get("kind")
        if kind == "steps":
            out += v.get("steps", [])
        elif kind == "variants":
            out += [o.get("note", "") for o in v.get("options", [])]
        elif kind == "cards":
            for c in v.get("cards", []):
                out += [c.get("title", ""), *c.get("items", [])]
        elif kind == "chunks":
            out.append(v.get("verdict", ""))
        elif kind == "cascade":
            out += [s.get("note", "") for s in v.get("steps", [])]
        elif kind == "bars":
            out += [l.get("label", "") for l in v.get("lines", [])]
    return out


def _cover_labels(path: Path) -> dict[int, dict]:
    """COVER_LABELS.md rows by post number, with the module label (the section heading) they sit under."""
    rows, module = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            module = line[3:].strip()
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"RAG #\d+", cells[0]):
            rows[int(cells[0][5:])] = {"module": module, "series_line": cells[1], "title": cells[2]}
    return rows


def _series_line(series) -> str:
    return f"{series['name']} · Part {series['part']}/{series['of']}" if series else "—"


def _parse_series_line(line: str):
    m = re.fullmatch(r"(.+?) · Part (\d+)/(\d+)", line or "")
    return {"name": m.group(1), "part": int(m.group(2)), "of": int(m.group(3))} if m else None


def _fill_teaser(post: dict, labels: dict[int, dict]) -> None:
    """Fill the teaser's module, mini-series line and title from the next post's COVER_LABELS row."""
    teaser = next((s for s in post["slides"] if s.get("type") == "teaser"), None)
    nxt = labels.get(int(re.sub(r"\D", "", post.get("post", "")) or 0) + 1)
    if teaser is None or nxt is None:
        return
    teaser.setdefault("module", nxt["module"])
    teaser.setdefault("title", nxt["title"])
    if "series" not in teaser:
        teaser["series"] = _parse_series_line(nxt["series_line"])


def _check_slides(specs: list[dict], fits: list[dict], label: str) -> list[str]:
    failures = []
    for spec, r in zip(specs, fits):
        sid = f"{label} {r['id']}"
        if r.get("title_lines", 0) > r.get("title_max_lines", 99):
            failures.append(f"{sid}: title runs to {r['title_lines']} lines (max {r['title_max_lines']})")
        if r.get("title_fits") is False:
            failures.append(f"{sid}: title is too wide even at {r['title_px']}px; shorten it or add a ' / ' break")
        if r["overflow"]:
            failures.append(f"{sid}: content doesn't fit the slide even at {int(r['scale'] * 100)}% size")
        if r["min_font_px"] < MIN_FONT_PX:
            failures.append(f"{sid}: text at {r['min_font_px']}px is under the {MIN_FONT_PX}px minimum")
        if r["text_outside_margins"]:
            failures.append(f"{sid}: text crosses the slide margins")
        if spec.get("type") == "body":
            words = sum(_words(t) for t in _prose(spec))
            r["body_words"] = words
            if words > MAX_BODY_WORDS:
                failures.append(f"{sid}: {words} words of body text (max {MAX_BODY_WORDS})")
    return failures


def _check_order(slides: list[dict], label: str) -> list[str]:
    """Cover first; then body slides; then the cheat sheet; then the teaser, if there is one."""
    types = [s.get("type") for s in slides]
    failures = []
    if not types or types[0] != "cover":
        failures.append(f"{label}: the first slide must be the cover")
    closing = ["cheatsheet", "teaser"] if "teaser" in types else ["cheatsheet"]
    if types[-len(closing):] != closing:
        failures.append(f"{label}: must end with {' then '.join(closing)}")
    if types.count("cheatsheet") != 1 or types.count("teaser") > 1 or types.count("cover") != 1:
        failures.append(f"{label}: needs one cover, one cheat sheet and at most one teaser")
    return failures


def render(post_path: Path, out_dir: Path, cover_labels: Path | None) -> dict:
    post = json.loads(post_path.read_text(encoding="utf-8"))
    labels = _cover_labels(cover_labels) if cover_labels else {}
    if labels:
        _fill_teaser(post, labels)

    cuts = {
        "linkedin": post["slides"],
        "instagram": [s for s in post["slides"] if s.get("instagram", True)],
    }
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)
    env.filters.update(inline=inline, titlehl=titlehl, chunktext=chunktext, codehl=codehl)
    css_uri = (ROOT / "templates" / "style.css").as_uri()
    slug = re.sub(r"\W+", "", post.get("post", "post")) or "post"

    fits = {}
    with sync_playwright() as p:
        browser = _launch(p)
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, slides in cuts.items():
            d = out_dir / name
            d.mkdir(parents=True, exist_ok=True)
            for old in d.glob("slide_*.png"):
                old.unlink()
            html = env.get_template("deck.html.j2").render(post=dict(post, slides=slides))
            deck = d / "deck.html"
            deck.write_text(html.replace('href="style.css"', f'href="{css_uri}"'), encoding="utf-8")
            page.goto(deck.as_uri())
            fits[name] = page.evaluate(FIT_JS)
            for i, el in enumerate(page.query_selector_all(".slide"), start=1):
                el.screenshot(path=str(d / f"slide_{i:02d}.png"))
            if name == "linkedin":
                page.pdf(path=str(d / f"{slug}.pdf"), width="1080px", height="1350px", print_background=True)
        browser.close()

    failures = []
    n, n_ig = len(cuts["linkedin"]), len(cuts["instagram"])
    if not SLIDES_MIN <= n <= SLIDES_MAX:
        failures.append(f"LinkedIn has {n} slides; allowed {SLIDES_MIN}-{SLIDES_MAX}, teaser included")
    if n_ig > INSTAGRAM_MAX:
        failures.append(f"Instagram has {n_ig} slides; max {INSTAGRAM_MAX}. Mark more body slides \"instagram\": false")
    for name, slides in cuts.items():
        failures += _check_order(slides, name)
        failures += _check_slides(slides, fits[name], name)

    if labels:
        num = int(re.sub(r"\D", "", post.get("post", "")) or 0)
        row = labels.get(num)
        cover = next((s for s in post["slides"] if s.get("type") == "cover"), {})
        if row is None:
            failures.append(f"{post.get('post')}: no row in {cover_labels.name}")
        else:
            if cover.get("title") != row["title"]:
                failures.append(f"cover title '{cover.get('title')}' doesn't match COVER_LABELS '{row['title']}'")
            if _series_line(post.get("series")) != row["series_line"]:
                failures.append(f"mini-series line '{_series_line(post.get('series'))}' doesn't match COVER_LABELS '{row['series_line']}'")
        nxt = labels.get(num + 1)
        teaser = next((s for s in post["slides"] if s.get("type") == "teaser"), None)
        if nxt and teaser is None:
            failures.append(f"missing the next-day teaser (next post: RAG #{num + 1:02d})")
        if nxt and teaser:
            if teaser.get("title") != nxt["title"]:
                failures.append(f"teaser title '{teaser.get('title')}' doesn't match COVER_LABELS '{nxt['title']}'")
            if _series_line(teaser.get("series")) != nxt["series_line"]:
                failures.append(f"teaser mini-series line doesn't match COVER_LABELS '{nxt['series_line']}'")
            if teaser.get("module") != nxt["module"]:
                failures.append(f"teaser module '{teaser.get('module')}' doesn't match COVER_LABELS '{nxt['module']}'")

    report = {"post": post.get("post"), "ok": not failures, "failures": failures,
              "counts": {"linkedin": n, "instagram": n_ig},
              "slides": fits["linkedin"], "instagram_slides": fits["instagram"]}
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--cover-labels", type=Path)
    a = ap.parse_args()
    report = render(a.post, a.out, a.cover_labels)
    print(json.dumps({"ok": report["ok"], "counts": report["counts"], "failures": report["failures"]}, indent=2))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
