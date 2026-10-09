# Print production & files

## Printing

- Paper: US Letter (8.5 × 11 in), portrait, plain white stock. The cream is printed, not the paper.
- Print the PDFs at 100% / Actual size. Turn off "Fit to page", which shrinks everything and breaks the margins.
- No bleed and no crop marks. Each PDF page is exactly one sheet.
- The diner's printer cannot print the outer 1/4in (`safe-zone`). Everything printed sits at least that far in; only the page ground reaches the edge, so on that printer every page has a thin white rim. It is most visible on the charcoal regular cover.
- Colors are designed on screen. Print one sheet of each new design on the diner's printer before running the set; the cream and maroon vary between printers.
- Slip-in order is cover, then pages 2–6. Pages 3–4 and 5–6 face each other.

## Where the files are

- **Editable design**: the Claude canvas "TKB Diner Menu", one canvas page per set (Regular, Halloween, Thanksgiving, Christmas). Each artboard is one sheet. Export a set with Export › All artboards (.pdf) from its canvas page.
- **Source and history**: the GitHub repository `alexshultz/tkb-menu`.
  - `design/` holds every page as a `.dc.html` file plus `canvas.json`. Regular pages have plain names (`Main`, `Breakfast`, `Starters`, `Burgers`, `Dinner`, `Kids`); seasonal copies are prefixed `H` (Halloween), `T` (Thanksgiving) and `X` (Christmas).
  - `print/` holds the print-ready PDFs.
  - `assets/logos/` holds the logos; `assets/logos/original/` holds the untouched source art.
  - `tools/render.py` renders a set to PDF and checks it.
  - `reference/current-menu-photos/` holds photos of the old menu.
- **In this system**: the Logos, Bands, Seasonal and Print files asset groups hold the same logos, standalone SVG bands and the current PDFs.

## Rendering and checking

`tools/render.py` turns pages into one PDF with headless Chromium, using local copies of Zilla Slab and Libre Franklin and of the logos. For every page it reports:

- how much height the content needs; anything over 1056 px means the page is overfull and must be cut, not shrunk;
- anything printed inside the 1/4in safe zone.

Run it after every content change. A change to items or prices has to be made in every set (regular and each seasonal copy), because the inside pages are separate copies.

## Open questions for the diner

- Two-price items (biscuits & gravy 4/7, sandwiches 9/11 and 10/12, salads 9/12): what the second price means.
- Prices for iced tea, hot tea, coffee, milk and orange juice.
- Which items are gluten-free; the menu currently says to ask the server.
- Whether the kids' chicken strips are hand-breaded like the basket strips.
- "Thousand Island" in the dressing list but "1000 Island" in item descriptions: pick one.
- Sierra Mist was renamed Starry in 2023.
- Opening hours, if they should appear on the cover.
