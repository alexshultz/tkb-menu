"""Fixed-layout Word build: a .docx that matches the canvas page line for line.

Each page becomes one Word page holding
  - a picture of the page with all text removed (rules, dotted leaders, tint boxes,
    bands, art), pinned behind the text at the page's top-left corner, and
  - one text box per line of text, pinned where that line sits on the canvas, in the
    same fonts (embedded in the file), with the same size, colour and letter spacing.
Nothing flows, so nothing drifts: editing a price or a description changes that line
only. Prices and other right-hand text sit in right-aligned boxes, so a longer price
grows to the left, toward its leader.

Word sizes text in half points, so the canvas pages use only sizes that are whole half
points (13.333px = 10pt, not 13px = 9.75pt). A size that isn't is set to the half
point below it, with a note. Kerning and standard ligatures are on, as in the browser.

Setup: npm install (in tools/), then python3 tools/word/exact_fonts.py
usage: python3 tools/word/exact.py out.docx page.dc.html [page.dc.html ...]
All pages in one file must share a size (Letter pages, or one card size).
"""
import io, re, sys, uuid, zipfile, pathlib, html
from playwright.sync_api import sync_playwright
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from render import to_html, WORK  # noqa: E402

FONTS = HERE / "fonts-exact"
DPI = 400
EMU_PX = 9525  # EMU per CSS px
CHROME_METRICS = {"zilla": (0.944, 0.256), "franklin": (0.966, 0.246)}  # what Chromium lays out with
WORD_METRICS = {"zilla": (0.944, 0.256), "franklin": (1.177, 0.246)}    # fonts-exact (hhea = typo = win)

EXTRACT_JS = r"""() => {
const root = document.body.firstElementChild, R = root.getBoundingClientRect();
const blockOf = n => { let e = n.parentElement; while (e && getComputedStyle(e).display === 'inline') e = e.parentElement; return e; };
const align = b => {
  const s = getComputedStyle(b);
  if (s.textAlign === 'right' || s.textAlign === 'end') return 'right';
  if (s.textAlign === 'center') return 'center';
  const prev = b.previousElementSibling;
  if (prev && prev.classList.contains('ld')) return 'right';
  const p = b.parentElement, ps = p && getComputedStyle(p);
  if (ps && ps.display.includes('flex') && ps.flexDirection.startsWith('row') && ps.justifyContent === 'space-between'
      && b === p.lastElementChild && p.children.length > 1) return 'right';
  return 'left';
};
const blocks = new Map(); let order = 0;
const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let n;
while ((n = w.nextNode())) {
  const t = n.textContent; if (!t.length) continue;
  const el = n.parentElement, s = getComputedStyle(el);
  if (!t.trim() && !blockOf(n)) continue;
  if (s.visibility === 'hidden' || s.display === 'none') continue;
  const b = blockOf(n);
  if (!t.trim() && !blocks.has(b)) continue;
  if (!blocks.has(b)) blocks.set(b, { align: align(b), order: order++, chars: [] });
  const style = { family: s.fontFamily, weight: s.fontWeight, italic: s.fontStyle === 'italic', size: parseFloat(s.fontSize),
    color: s.color, ls: s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing), upper: s.textTransform === 'uppercase' };
  const rg = document.createRange();
  for (let i = 0; i < t.length; i++) {
    rg.setStart(n, i); rg.setEnd(n, i + 1);
    const rs = [...rg.getClientRects()].filter(r => r.width > 0.01);
    if (!rs.length) { blocks.get(b).chars.push({ ch: t[i], collapsed: true, style }); continue; }
    const r = rs[0];
    blocks.get(b).chars.push({ ch: t[i], x0: r.left - R.left, x1: r.right - R.left, top: r.top - R.top, h: r.height, style });
  }
}
const out = [];
for (const [b, info] of blocks) {
  const lines = []; let cur = null, lastTop = null;
  for (const c of info.chars) {
    if (c.collapsed) { if (cur) cur.pending = true; continue; }
    if (lastTop === null || Math.abs(c.top + c.h - lastTop) > 2) { cur = { chars: [], pending: false }; lines.push(cur); }
    else if (cur.pending && !/\s/.test(c.ch)) { cur.chars.push({ ...c, ch: ' ', x0: c.x0, x1: c.x0 }); }
    cur.pending = false;
    cur.chars.push(c); lastTop = c.top + c.h;
  }
  for (const l of lines) {
    const cs = l.chars;
    while (cs.length && /\s/.test(cs[cs.length - 1].ch)) cs.pop();
    while (cs.length && /\s/.test(cs[0].ch)) cs.shift();
    if (!cs.length) continue;
    out.push({ align: info.align, order: info.order,
      x0: Math.min(...cs.map(c => c.x0)), x1: Math.max(...cs.map(c => c.x1)),
      chars: cs.map(c => ({ ch: c.ch, top: c.top, h: c.h, s: c.style })) });
  }
}
return { w: R.width, h: R.height, lines: out };
}"""


def face(fam, weight, italic):
    fam = fam.lower()
    w = int(weight)
    if "zilla" in fam:
        return {500: "Zilla Slab Medium", 600: "Zilla Slab SemiBold"}.get(w, "Zilla Slab Bold" if w >= 650 else "Zilla Slab Medium"), "zilla"
    if italic:
        return "Libre Franklin Italic", "franklin"
    return {500: "Libre Franklin Medium", 600: "Libre Franklin SemiBold"}.get(w, "Libre Franklin SemiBold" if w >= 600 else "Libre Franklin"), "franklin"


def hexcolor(c):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", c)
    return "%02X%02X%02X" % tuple(int(x) for x in m.groups()) if m else "000000"


def half_points(px):
    hp = px * 1.5
    if abs(hp - round(hp)) > 0.02:
        print(f"  note: {px}px is not a whole half point; Word gets {int(hp) / 2}pt")
        return int(hp)
    return round(hp)


def esc(t):
    return html.escape(t, quote=False)


class Doc:
    def __init__(self):
        self.ids = 0
        self.media = []   # (name, bytes)
        self.fonts = set()

    def nid(self):
        self.ids += 1
        return self.ids

    def picture(self, png, w, h):
        idx = len(self.media) + 1
        name = f"image{idx}.png"
        self.media.append((name, png))
        rid = f"rIdImg{idx}"
        i = self.nid()
        cx, cy = round(w * EMU_PX), round(h * EMU_PX)
        return f"""<w:r><w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="{i}" behindDoc="1" locked="1" layoutInCell="1" allowOverlap="1"><wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH><wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/><wp:docPr id="{i}" name="Page art {i}" descr="Page background: rules, leaders, boxes and art"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="{i}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:anchor></w:drawing></w:r>"""

    def textbox(self, line, page_w):
        runs, maxasc, maxdesc, baseline = [], 0, 0, None
        groups = []
        for c in line["chars"]:
            s = c["s"]
            key = (s["family"], s["weight"], s["italic"], s["size"], s["color"], s["ls"], s["upper"])
            if groups and groups[-1][0] == key:
                groups[-1][1].append(c)
            else:
                groups.append((key, [c]))
        for (fam, weight, italic, size, color, ls, upper), cs in groups:
            fname, kind = face(fam, weight, italic)
            self.fonts.add(fname)
            hp = half_points(size)
            pt = hp / 2
            a, d = WORD_METRICS[kind]
            maxasc, maxdesc = max(maxasc, a * pt), max(maxdesc, d * pt)
            if baseline is None:
                ca, cd = CHROME_METRICS[kind]
                c0 = cs[0]
                # Chromium's glyph box spans ascent + descent; the baseline divides it in that ratio
                baseline = c0["top"] + c0["h"] * ca / (ca + cd)
            text = "".join(c["ch"] for c in cs).replace(" ", " ")
            if upper:
                text = text.upper()
            rpr = f'<w:rFonts w:ascii="{fname}" w:hAnsi="{fname}" w:cs="{fname}"/><w:color w:val="{hexcolor(color)}"/><w:sz w:val="{hp}"/><w:szCs w:val="{hp}"/>'
            if ls:
                rpr += f'<w:spacing w:val="{round(ls * 15)}"/>'
            runs.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>')
        line_pt = maxasc + maxdesc
        top_px = baseline - maxasc / 0.75
        h_px = line_pt / 0.75
        x0, x1 = line["x0"], line["x1"]
        width = x1 - x0
        slack = max(24, width * 0.5)
        if line["align"] == "right":
            left, wbox, jc = max(0, x0 - slack), x1 - max(0, x0 - slack), "right"
        elif line["align"] == "center":
            mid = (x0 + x1) / 2
            half = min(width / 2 + slack, mid, page_w - mid)
            left, wbox, jc = mid - half, 2 * half, "center"
        else:
            left, wbox, jc = x0, min(width + slack, page_w - x0), "left"
        i = self.nid()
        cx, cy = round(wbox * EMU_PX), round(h_px * EMU_PX)
        para = (f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="{round(line_pt * 20)}" w:lineRule="exact"/>'
                f'<w:ind w:left="0" w:right="0"/><w:jc w:val="{jc}"/></w:pPr>{"".join(runs)}</w:p>')
        label = esc("".join(c["ch"] for c in line["chars"])[:40])
        return f"""<w:r><mc:AlternateContent><mc:Choice Requires="wps"><w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="{1000 + i}" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1"><wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="page"><wp:posOffset>{round(left * EMU_PX)}</wp:posOffset></wp:positionH><wp:positionV relativeFrom="page"><wp:posOffset>{round(top_px * EMU_PX)}</wp:posOffset></wp:positionV><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/><wp:docPr id="{i}" name="Text {i}" descr="{label}"/><wp:cNvGraphicFramePr/><a:graphic><a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"><wps:wsp><wps:cNvSpPr txBox="1"/><wps:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></wps:spPr><wps:txbx><w:txbxContent>{para}</w:txbxContent></wps:txbx><wps:bodyPr rot="0" vert="horz" wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t" anchorCtr="0" upright="1"><a:noAutofit/></wps:bodyPr></wps:wsp></a:graphicData></a:graphic></wp:anchor></w:drawing></mc:Choice></mc:AlternateContent></w:r>"""


NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
      'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
      'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" mc:Ignorable="w14 wp14"')


def obfuscate(data, guid):
    key = bytes.fromhex(guid.strip("{}").replace("-", ""))[::-1]
    b = bytearray(data)
    for i in range(32):
        b[i] ^= key[i % 16]
    return bytes(b)


def build(out, pages):
    doc = Doc()
    bodies, size = [], None
    WORK.mkdir(exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        for i, f in enumerate(pages):
            tmp = WORK / f"exact{i}.html"
            tmp.write_text(to_html(pathlib.Path(f).read_text()))
            pg = br.new_page(viewport={"width": 816, "height": 1056})
            pg.goto(tmp.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
            data = pg.evaluate(EXTRACT_JS)
            w, h = data["w"], data["h"]
            if size and size != (w, h):
                sys.exit("all pages in one file must be the same size")
            size = (w, h)
            pg.close()
            # the page with its text hidden, at print resolution
            pg = br.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=DPI / 96)
            pg.goto(tmp.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
            pg.add_style_tag(content="*{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}")
            png = pg.screenshot(clip={"x": 0, "y": 0, "width": w, "height": h})
            pg.close()
            lines = sorted(data["lines"], key=lambda l: (l["align"] == "right", l["order"]))
            parts = [doc.picture(png, w, h)] + [doc.textbox(l, w) for l in lines]
            brk = '<w:r><w:br w:type="page"/></w:r>' if i < len(pages) - 1 else ""
            bodies.append(f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" w:lineRule="exact"/><w:rPr><w:sz w:val="2"/></w:rPr></w:pPr>{"".join(parts)}{brk}</w:p>')
            print(f"{pathlib.Path(f).name}: {len(lines)} text lines")
        br.close()
    W, H = round(size[0] * 15), round(size[1] * 15)
    sect = f'<w:sectPr><w:pgSz w:w="{W}" w:h="{H}"{" w:orient=\"landscape\"" if W > H else ""}/><w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="0" w:gutter="0"/><w:cols w:space="0"/></w:sectPr>'
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document {NS}><w:body>{"".join(bodies)}{sect}</w:body></w:document>'

    font_xml, font_rels, font_files = [], [], []
    for j, name in enumerate(sorted(doc.fonts), 1):
        guid = "{" + str(uuid.uuid4()).upper() + "}"
        raw = (FONTS / f"{name.replace(' ', '-')}.ttf").read_bytes()
        font_files.append((f"word/fonts/font{j}.odttf", obfuscate(raw, guid)))
        font_rels.append(f'<Relationship Id="rIdF{j}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/font{j}.odttf"/>')
        font_xml.append(f'<w:font w:name="{name}"><w:charset w:val="00"/><w:family w:val="auto"/><w:pitch w:val="variable"/><w:embedRegular r:id="rIdF{j}" w:fontKey="{guid}"/></w:font>')

    files = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>',
        "docProps/core.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>TKB Diner</dc:title><dc:creator>TKB Diner</dc:creator></cp:coreProperties>',
        "word/_rels/document.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdSet" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rIdFT" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>'
            + "".join(f'<Relationship Id="rIdImg{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{n}"/>' for k, (n, _) in enumerate(doc.media, 1)) + "</Relationships>",
        "word/styles.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:styles {NS}><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Libre Franklin" w:hAnsi="Libre Franklin" w:cs="Libre Franklin"/><w:kern w:val="2"/><w14:ligatures w14:val="standard"/><w:sz w:val="20"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style></w:styles>',
        "word/settings.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:settings {NS}><w:embedTrueTypeFonts/><w:defaultTabStop w:val="720"/><w:characterSpacingControl w:val="doNotCompress"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>',
        "word/fontTable.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:fonts {NS}>{"".join(font_xml)}</w:fonts>',
        "word/_rels/fontTable.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(font_rels) + "</Relationships>",
        "word/document.xml": document,
    }
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, t in files.items():
            z.writestr(n, t)
        for n, b in doc.media:
            z.writestr(f"word/media/{n}", b)
        for n, b in font_files:
            z.writestr(n, b)
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2:])
