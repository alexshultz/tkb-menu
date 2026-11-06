"""Swap the banner and/or cover art in a fixed-layout Word file (from exact.py).

Does what Word's Change Picture does, without Word: the new picture fills the old
picture's frame, so make it the exact template size (see graphics/templates).

usage: python3 tools/word/swap-graphics.py in.docx out.docx [--banner b.png] [--cover c.png]
"""
import re, sys, zipfile, argparse


def target(rels, rid):
    return "word/" + re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--banner"); ap.add_argument("--cover")
    a = ap.parse_args()
    z = zipfile.ZipFile(a.src)
    swap = {}
    if a.banner:
        hdr = z.read("word/header1.xml").decode()
        rid = re.search(r'r:embed="([^"]+)"', hdr).group(1)
        swap[target(z.read("word/_rels/header1.xml.rels").decode(), rid)] = open(a.banner, "rb").read()
    if a.cover:
        doc = z.read("word/document.xml").decode()
        m = re.search(r'name="Cover art".*?r:embed="([^"]+)"', doc, re.S)
        if not m:
            sys.exit("no cover art picture in this file")
        swap[target(z.read("word/_rels/document.xml.rels").decode(), m.group(1))] = open(a.cover, "rb").read()
    for name, data in swap.items():
        if not name.endswith(".png"):
            sys.exit(f"{name} is not a PNG slot")
    with zipfile.ZipFile(a.dst, "w", zipfile.ZIP_DEFLATED) as out:
        for info in z.infolist():
            out.writestr(info, swap.get(info.filename, z.read(info.filename)))
    print("wrote", a.dst, "swapped", ", ".join(swap))


if __name__ == "__main__":
    main()
