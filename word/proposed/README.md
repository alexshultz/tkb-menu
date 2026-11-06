# Proposed menu: editable Word files

DRAFT, for the proposed new menu and the coffee-bar drink cards. The PDFs in `print/proposed/` are made from these files, so what you see in Word is what prints.

| File | Pages |
| --- | --- |
| `TKB Diner Menu - proposed.docx` | The six menu pages, US Letter |
| `Drink Card - half letter.docx` | Specialty Drinks front, Build Your Drink back, 5.5 × 8.5 in |
| `Drink Card - 4x6.docx` | The same card for 4 × 6 index cards |

## How these files work

Every line of text is its own small text box, pinned to an exact spot on the page. The rules, dotted leaders, tinted boxes, checkerboard bands and cover art are one picture behind the text. That's why the layout can't shift: nothing flows from one line into the next.

## Changing a price or a line

1. Open the file in **Microsoft Word** (Mac or Windows). Pages, Google Docs and Word on the web don't keep the menu's fonts, so the layout comes out wrong.
2. Click the price or line, select the text, and type the new text.
3. **File › Save As…** (or **Export**), choose **PDF**, and print that PDF at 100% / Actual size.

Prices sit in right-aligned boxes: a wider price grows to the left, toward its dotted leader. Other lines grow to the right. A line that gets much longer can run past its space, into whatever is next to it. Keep edits to about the same length, or ask for the page to be rebuilt.

The fonts are built into each file, so nothing needs installing. To be safe on a computer that has never had them, install the ones in `fonts/`.

## Adding or removing a dish

Don't do it here. Adding or removing a dish means moving everything below it. Make that change on the design canvas, then rebuild these files and the PDFs:

    sh tools/word/build-exact.sh

That needs `(cd tools && npm install)` and `python3 tools/word/exact_fonts.py` once, plus LibreOffice. The build reads `design/proposed/`, so copy the changed pages there from the canvas first. Note that rebuilding overwrites any price edits made directly in these Word files. Put those prices on the canvas first.
