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
# printer's unprintable border: 1/4 inch at 96 px/in
SAFE_PX = 24
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
            # flex children shrink instead of overflowing, so compare each child's
            # natural height (min-content) against the space the page actually gives it
            over = pg.evaluate("""() => { const r = document.body.firstElementChild;
              const kids = [...r.children]; const prev = kids.map(k => k.style.flexShrink);
              kids.forEach(k => k.style.flexShrink = '0'); const need = r.scrollHeight;
              kids.forEach((k, i) => k.style.flexShrink = prev[i]); return need; }""")
            print(f"{pathlib.Path(f).name}: needs {over}px of 1056")
            # anything other than the page background inside the printer's no-print zone
            zone = SAFE_PX
            # only things that put ink on paper: text, images, svgs, boxes with a fill or border
            edge = pg.evaluate("""(z) => { const r = document.body.firstElementChild; const out = [];
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
              return out; }""", zone)
            for e in edge[:5]: print(f"  EDGE {pathlib.Path(f).name}: {e} is within {zone}px of the paper edge")
            if over > 1056: print(f"WARNING {f}: content needs {over}px (> 1056) and will be squeezed")
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
