#!/bin/sh
# Builds the fixed-layout Word files for the proposed menu and drink cards, then makes
# every PDF in print/proposed FROM those Word files (LibreOffice), so PDF = Word.
# Setup once: (cd tools && npm install) && python3 tools/word/exact_fonts.py
# usage, from the repo root: sh tools/word/build-exact.sh
set -e
P=design/proposed
W=word/proposed
O=print/proposed
mkdir -p "$W" "$O"
python3 tools/word/exact.py "$W/TKB Diner Menu - proposed.docx" \
  $P/PCover.dc.html $P/PBreakfast.dc.html $P/DStarters.dc.html $P/DBurgers.dc.html $P/DDinner.dc.html $P/DDrinks.dc.html
python3 tools/word/exact.py "$W/Drink Card - half letter.docx" $P/DSeasonalDrinks.dc.html $P/DDrinkCardBack.dc.html
python3 tools/word/exact.py "$W/Drink Card - 4x6.docx" $P/Card4x6Front.dc.html $P/Card4x6Back.dc.html
T=$(mktemp -d)
for f in "$W"/*.docx; do soffice --headless --convert-to pdf --outdir "$T" "$f" >/dev/null 2>&1; done
cp "$T/TKB Diner Menu - proposed.pdf" "$O/TKB-Diner-Menu-PROPOSED.pdf"
cp "$T/Drink Card - half letter.pdf" "$O/Drink-Card-half-letter.pdf"
cp "$T/Drink Card - 4x6.pdf" "$O/Drink-Card-4x6.pdf"
rm -rf "$T"
python3 - <<'PY'
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from pypdf.generic import RectangleObject
# LibreOffice rounds a 5.5in page to 14cm; trim it back to 396pt
f = 'print/proposed/Drink-Card-half-letter.pdf'; r = PdfReader(f); w = PdfWriter()
for pg in r.pages:
    pg.mediabox = RectangleObject([0, float(pg.mediabox.top) - 612, 396, float(pg.mediabox.top)]); pg.cropbox = pg.mediabox; w.add_page(pg)
w.write(f)
r = PdfReader('print/proposed/Drink-Card-half-letter.pdf'); w = PdfWriter()
for pg in r.pages:
    sheet = PageObject.create_blank_page(width=792, height=612)
    for x in (0, 396):
        sheet.merge_transformed_page(pg, Transformation().translate(x, 0))
    w.add_page(sheet)
w.write('print/proposed/Drink-Card-half-letter-2up-on-Letter.pdf')
PY
for f in "$O"/*.pdf; do echo "$f: $(pdfinfo "$f" | awk '/^Pages/{p=$2} /^Page size/{s=$3"x"$5} END{print p" pages, "s" pt"}')"; done
