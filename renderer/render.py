#!/usr/bin/env python3
"""Render a carousel post (JSON) into PNG slides and one PDF with headless Chrome.

Usage:
    python3 renderer/render.py ai_engineering/rag/slides/RAG15.json --out out/RAG15
    python3 renderer/render.py POST.json --out DIR --cover-labels ai_engineering/rag/COVER_LABELS.md

Writes slide_01.png ... slide_NN.png (1080x1350), <post>.pdf and report.json to DIR.
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
MAX_BODY_WORDS = 40       # text + after, per body slide
SLIDES_MIN, SLIDES_MAX = 6, 8

# ---------- text filters ----------

def _code_spans(s: str) -> str:
    """Escape text and turn `code` into inline code spans."""
    out, pos = [], 0
    for m in re.finditer(r"`([^`]+)`", s):
        out.append(str(escape(s[pos:m.start()])))
        out.append(f'<code class="ic">{escape(m.group(1))}</code>')
        pos = m.end()
    out.append(str(escape(s[pos:])))
    return "".join(out)


def inline(s) -> Markup:
    return Markup(_code_spans(str(s or "")))


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


def _cover_label_row(path: Path, post_id: str):
    num = re.sub(r"\D", "", post_id)
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.sub(r"\D", "", cells[0]) == num and cells[0].startswith("RAG"):
            return cells
    return None


def render(post_path: Path, out_dir: Path, cover_labels: Path | None) -> dict:
    post = json.loads(post_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)
    env.filters.update(inline=inline, titlehl=titlehl, chunktext=chunktext, codehl=codehl)
    html = env.get_template("deck.html.j2").render(post=post)
    html = html.replace('href="style.css"', f'href="{(ROOT / "templates" / "style.css").as_uri()}"')
    deck = out_dir / "deck.html"
    deck.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        browser = _launch(p)
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        page.goto(deck.as_uri())
        slides = page.evaluate(FIT_JS)
        for i, el in enumerate(page.query_selector_all(".slide"), start=1):
            el.screenshot(path=str(out_dir / f"slide_{i:02d}.png"))
        slug = re.sub(r"\W+", "", post.get("post", "post")) or "post"
        page.pdf(path=str(out_dir / f"{slug}.pdf"), width="1080px", height="1350px", print_background=True)
        browser.close()

    failures = []
    n = len(post["slides"])
    if not SLIDES_MIN <= n <= SLIDES_MAX:
        failures.append(f"post has {n} slides; allowed {SLIDES_MIN}-{SLIDES_MAX}")
    for spec, r in zip(post["slides"], slides):
        sid = r["id"]
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
            words = _words(spec.get("text", "")) + _words(spec.get("after", ""))
            r["body_words"] = words
            if words > MAX_BODY_WORDS:
                failures.append(f"{sid}: {words} words of body text (max {MAX_BODY_WORDS})")

    if cover_labels:
        row = _cover_label_row(cover_labels, post.get("post", ""))
        cover = next((s for s in post["slides"] if s.get("type") == "cover"), {})
        if row is None:
            failures.append(f"{post.get('post')}: no row in {cover_labels.name}")
        else:
            expected_series = row[1]
            expected_title = row[2]
            if cover.get("title") != expected_title:
                failures.append(f"cover title '{cover.get('title')}' doesn't match COVER_LABELS '{expected_title}'")
            series = post.get("series")
            got_series = f"{series['name']} · Part {series['part']}/{series['of']}" if series else "—"
            if got_series != expected_series:
                failures.append(f"mini-series line '{got_series}' doesn't match COVER_LABELS '{expected_series}'")

    report = {"post": post.get("post"), "ok": not failures, "failures": failures, "slides": slides}
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--cover-labels", type=Path)
    a = ap.parse_args()
    report = render(a.post, a.out, a.cover_labels)
    print(json.dumps({"ok": report["ok"], "failures": report["failures"]}, indent=2))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
