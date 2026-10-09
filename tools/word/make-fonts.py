"""Prepare the fonts the Word build embeds.

docx-js embeds one font file per font name (no bold/italic slots), so each weight the
menu uses becomes its own single-style family, named the way Windows names the
installed Google fonts ("Zilla Slab SemiBold", "Libre Franklin Medium", ...).

Reads the woff files from tools/node_modules/@fontsource (run `npm install` in tools/
first) and writes TrueType files to tools/word/fonts/.

usage: python3 tools/word/make-fonts.py
"""
import pathlib
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "node_modules/@fontsource"
OUT = HERE / "fonts"
FACES = [
    ("zilla-slab", "700", "normal", "Zilla Slab Bold"),
    ("zilla-slab", "600", "normal", "Zilla Slab SemiBold"),
    ("libre-franklin", "400", "normal", "Libre Franklin"),
    ("libre-franklin", "400", "italic", "Libre Franklin Italic"),
    ("libre-franklin", "500", "normal", "Libre Franklin Medium"),
    ("libre-franklin", "600", "normal", "Libre Franklin SemiBold"),
]

OUT.mkdir(exist_ok=True)
for pkg, weight, style, family in FACES:
    font = TTFont(SRC / pkg / "files" / f"{pkg}-latin-{weight}-{style}.woff")
    font.flavor = None
    names = font["name"]
    for rec in list(names.names):
        if rec.nameID in (16, 17, 21, 22):
            names.removeNames(nameID=rec.nameID)
    ps = family.replace(" ", "-")
    for pid, eid, lid in [(3, 1, 0x409), (1, 0, 0)]:
        names.setName(family, 1, pid, eid, lid)
        names.setName("Regular", 2, pid, eid, lid)
        names.setName(family, 4, pid, eid, lid)
        names.setName(ps, 6, pid, eid, lid)
    os2 = font["OS/2"]
    os2.fsSelection = (os2.fsSelection & ~0b1100001) | 0b1000000  # Regular style bit only
    os2.fsType = 0  # installable embedding (both fonts are SIL Open Font License)
    font["head"].macStyle = 0
    font.save(OUT / f"{ps}.ttf")
    print("wrote", OUT / f"{ps}.ttf")
