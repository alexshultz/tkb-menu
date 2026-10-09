"""Render menu pages (canvas .dc.html files) to one print-ready PDF and check them.

Setup, once, from the tools/ folder:
    npm install                      # fetches the two fonts listed in package.json
    pip install playwright pypdf && python -m playwright install chromium

Usage, from the repo root:
    python3 tools/render.py print/TKB-Diner-Menu.pdf design/Main.dc.html design/Breakfast.dc.html \\
        design/Starters.dc.html design/Burgers.dc.html design/Dinner.dc.html design/Kids.dc.html

For every page it reports:
  - "needs N px of 1056": the height the content needs. Over 1056 means the page is
    overfull; cut or move items, never shrink the type.
  - "EDGE": anything printed inside the printer's 1/4in (24px) dead zone.

Pictures the pages load from the canvas asset store (/_blob/<id>) are mapped to the repo
copies in BLOBS. A new cover picture uploaded to the canvas needs a line there, or pass
EXTRA_BLOBS="<id>=<path>;<id>=<path>".
"""
import os, re, sys, pathlib
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

TOOLS = pathlib.Path(__file__).resolve().parent
REPO = TOOLS.parent
BLOBS = {
    "940e0c31f89f681f04797625015c052e": REPO / "assets/logos/tkb-logo-print.png",
    "ea027bf410aeb5870851acef4f79a9db": REPO / "assets/seasonal/art/tkb-halloween-logo-print.png",
    "2abc776de8bc8d9254c318631aca7628": REPO / "assets/seasonal/art/tkb-thanksgiving-logo-print.png",
    "fe620ff1479fda4324bf3a8f10c4d003": REPO / "assets/seasonal/art/tkb-christmas-logo-print.png",
}
BLOBS.update({k: pathlib.Path(v) for k, v in (pair.split("=", 1) for pair in os.environ.get("EXTRA_BLOBS", "").split(";") if "=" in pair)})
SAFE_PX = 24  # 1/4 inch at 96 px/in
FONT_CSS = [
    "zilla-slab/500.css", "zilla-slab/600.css", "zilla-slab/700.css",
    "libre-franklin/400.css", "libre-franklin/500.css", "libre-franklin/600.css", "libre-franklin/400-italic.css",
]
WORK = TOOLS / ".render"


def to_html(src: str) -> str:
    styles = "\n".join(re.findall(r"<style>(.*?)</style>", src, re.S))
    body = re.search(r"</helmet>(.*)</x-dc>", src, re.S).group(1)
    for bid, p in BLOBS.items():
        body = body.replace(f"/_blob/{bid}", p.as_uri())
    links = "\n".join(f'<link rel="stylesheet" href="{(TOOLS / "node_modules/@fontsource" / f).as_uri()}">' for f in FONT_CSS)
    return f"""<!doctype html><html><head><meta charset="utf-8">{links}
<style>@page{{size:8.5in 11in;margin:0}} html,body{{margin:0;padding:0}} {styles}</style></head>
<body>{body}</body></html>"""


NEEDS_JS = """() => { const r = document.body.firstElementChild;
  const kids = [...r.children]; const prev = kids.map(k => k.style.flexShrink);
  kids.forEach(k => k.style.flexShrink = '0'); const need = r.scrollHeight;
  kids.forEach((k, i) => k.style.flexShrink = prev[i]); return need; }"""

EDGE_JS = """(z) => { const r = document.body.firstElementChild; const out = [];
  const bad = b => b.width && b.height && (b.left < z || b.top < z || b.right > 816 - z || b.bottom > 1056 - z);
  const fmt = (t, b) => t + ' ' + Math.round(b.left) + ',' + Math.round(b.top) + ' ' + Math.round(b.right) + ',' + Math.round(b.bottom);
  r.querySelectorAll('*').forEach(e => { const tag = e.tagName.toLowerCase();
    if (e.closest('svg') && tag !== 'svg') return;
    const s = getComputedStyle(e);
    const inky = tag === 'img' || tag === 'svg' || s.backgroundImage !== 'none' ||
      (s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent') ||
      ['Top','Right','Bottom','Left'].some(k => parseFloat(s['border' + k + 'Width']) > 0 && s['border' + k + 'Style'] !== 'none');
    const b = e.getBoundingClientRect(); if (inky && bad(b)) out.push(fmt(tag, b)); });
  const w = document.createTreeWalker(r, NodeFilter.SHOW_TEXT); let n;
  while ((n = w.nextNode())) { if (!n.textContent.trim()) continue; const rg = document.createRange(); rg.selectNodeContents(n);
    for (const b of rg.getClientRects()) if (bad(b)) { out.push(fmt('text "' + n.textContent.trim().slice(0, 24) + '"', b)); break; } }
  return out; }"""


def main():
    out, pages = sys.argv[1], sys.argv[2:]
    if not pages:
        sys.exit(__doc__)
    WORK.mkdir(exist_ok=True)
    writer = PdfWriter()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 816, "height": 1056})
        for i, f in enumerate(pages):
            name = pathlib.Path(f).name
            tmp = WORK / f"page{i}.html"
            tmp.write_text(to_html(pathlib.Path(f).read_text()))
            pg.goto(tmp.as_uri())
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            need = pg.evaluate(NEEDS_JS)
            print(f"{name}: needs {need}px of 1056" + ("  OVERFULL" if need > 1056 else ""))
            for e in pg.evaluate(EDGE_JS, SAFE_PX)[:5]:
                print(f"  EDGE {name}: {e} is within {SAFE_PX}px of the paper edge")
            pdf = WORK / f"page{i}.pdf"
            pg.pdf(path=str(pdf), width="8.5in", height="11in", print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            for page in PdfReader(str(pdf)).pages:
                writer.add_page(page)
        browser.close()
    with open(out, "wb") as fh:
        writer.write(fh)
    print("wrote", out, len(writer.pages), "pages")


if __name__ == "__main__":
    main()
