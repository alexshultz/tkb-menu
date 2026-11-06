"""Fonts for the fixed-layout Word build (exact.py).

Each face the menu uses becomes its own one-style family (Word embeds one file per
font name). Vertical metrics are made identical in hhea, OS/2 typo and OS/2 win, so
Word (Windows or Mac) and LibreOffice all put the baseline at the same height.

usage: python3 tools/word/exact_fonts.py      (after `npm install` in tools/)
writes tools/word/fonts-exact/*.ttf and installs copies in ~/.local/share/fonts
"""
import pathlib, shutil, subprocess
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "node_modules/@fontsource"
OUT = HERE / "fonts-exact"
FACES = [  # (package, weight, style, Word family)
    ("zilla-slab", "500", "normal", "Zilla Slab Medium"),
    ("zilla-slab", "600", "normal", "Zilla Slab SemiBold"),
    ("zilla-slab", "700", "normal", "Zilla Slab Bold"),
    ("libre-franklin", "400", "normal", "Libre Franklin"),
    ("libre-franklin", "400", "italic", "Libre Franklin Italic"),
    ("libre-franklin", "500", "normal", "Libre Franklin Medium"),
    ("libre-franklin", "600", "normal", "Libre Franklin SemiBold"),
]


def main():
    OUT.mkdir(exist_ok=True)
    local = pathlib.Path.home() / ".local/share/fonts"
    local.mkdir(parents=True, exist_ok=True)
    for pkg, weight, style, family in FACES:
        f = TTFont(SRC / pkg / "files" / f"{pkg}-latin-{weight}-{style}.woff")
        f.flavor = None
        names = f["name"]
        for rec in list(names.names):
            if rec.nameID in (16, 17, 21, 22):
                names.removeNames(nameID=rec.nameID)
        ps = family.replace(" ", "-")
        for pid, eid, lid in [(3, 1, 0x409), (1, 0, 0)]:
            names.setName(family, 1, pid, eid, lid)
            names.setName("Regular", 2, pid, eid, lid)
            names.setName(family, 4, pid, eid, lid)
            names.setName(ps, 6, pid, eid, lid)
        os2, hhea = f["OS/2"], f["hhea"]
        asc, desc = os2.usWinAscent, os2.usWinDescent
        hhea.ascent, hhea.descent, hhea.lineGap = asc, -desc, 0
        os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = asc, -desc, 0
        os2.fsSelection = (os2.fsSelection | (1 << 7) | (1 << 6)) & ~0b100001  # USE_TYPO_METRICS, REGULAR; not italic/bold
        os2.usWeightClass = 400
        f["head"].macStyle = 0
        os2.fsType = 0  # installable embedding
        path = OUT / f"{ps}.ttf"
        f.save(path)
        shutil.copy(path, local / path.name)
        print(f"{family}: ascent {asc}, descent {desc} per {f['head'].unitsPerEm}")
    subprocess.run(["fc-cache", "-f"], check=False)


if __name__ == "__main__":
    main()
