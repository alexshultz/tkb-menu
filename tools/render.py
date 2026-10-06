"""Render canvas .dc.html artboards to a single print PDF (8.5x11, no margins).

usage: python3 render.py OUT.pdf PAGE1.dc.html PAGE2.dc.html ...
Assets referenced as /_blob/<id> are mapped via BLOBS below.
"""
import re, sys, os, pathlib
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

HERE = pathlib.Path(__file__).resolve().parent
IMG = HERE.parent / "img"
BLOBS = {
    "940e0c31f89f681f04797625015c052e": IMG / "tkb_logo.png",
    "2819d2ad73cbbc96e316763654be92bd": IMG / "halloween_logo.png",
}
BLOBS.update({k: pathlib.Path(v) for k, v in (l.split("=", 1) for l in os.environ.get("EXTRA_BLOBS", "").split(";") if "=" in l)})
FONTS = [
    "zilla-slab/500.css", "zilla-slab/600.css", "zilla-slab/700.css",
    "libre-franklin/400.css", "libre-franklin/500.css", "libre-franklin/600.css", "libre-franklin/400-italic.css",
    "creepster/400.css",
]

def to_html(src: str) -> str:
    styles = "\n".join(re.findall(r"<style>(.*?)</style>", src, re.S))
    body = re.search(r"</helmet>(.*)</x-dc>", src, re.S).group(1)
    for bid, path in BLOBS.items():
        body = body.replace(f"/_blob/{bid}", path.as_uri())
    links = "\n".join(f'<link rel="stylesheet" href="{(HERE / "node_modules/@fontsource" / f).as_uri()}">' for f in FONTS)
    return f"""<!doctype html><html><head><meta charset="utf-8">{links}
<style>@page{{size:8.5in 11in;margin:0}} html,body{{margin:0;padding:0}} {styles}</style></head>
<body>{body}</body></html>"""

def main():
    out, pages = sys.argv[1], sys.argv[2:]
    writer = PdfWriter()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 816, "height": 1056})
        for i, f in enumerate(pages):
            tmp = HERE / f"_page{i}.html"
            tmp.write_text(to_html(pathlib.Path(f).read_text()))
            pg.goto(tmp.as_uri())
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            # report any page whose content overflows its fixed 1056px frame
            over = pg.evaluate("""() => { const r = document.body.firstElementChild; let m = 0;
              r.querySelectorAll('*').forEach(e => { const b = e.getBoundingClientRect(); if (b.height) m = Math.max(m, b.bottom); });
              return Math.round(m); }""")
            if over > 1056: print(f"WARNING {f}: content reaches {over}px (> 1056)")
            pdf = HERE / f"_page{i}.pdf"
            pg.pdf(path=str(pdf), width="8.5in", height="11in", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            pg.screenshot(path=str(HERE / f"_page{i}.png"))
            for page in PdfReader(str(pdf)).pages:
                writer.add_page(page)
        b.close()
    with open(out, "wb") as fh:
        writer.write(fh)
    print("wrote", out, len(writer.pages), "pages")

if __name__ == "__main__":
    main()
