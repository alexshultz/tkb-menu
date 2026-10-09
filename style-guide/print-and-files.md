# Print production & files

## Printing

- Paper: US Letter (8.5 × 11 in), portrait, plain white stock. The cream is printed, not the paper.
- Print the PDFs at 100% / Actual size. Turn off "Fit to page", which shrinks everything and breaks the margins.
- No bleed and no crop marks. Each PDF page is exactly one sheet.
- The diner's printer cannot print the outer 1/4in (`safe-zone`). Everything printed sits at least that far in; only the page ground reaches the edge, so on that printer every page has a thin white rim. It is most visible on the charcoal regular cover.
- Colors are designed on screen. Print one sheet of each new design on the diner's printer before running the set; the cream and maroon vary between printers.
- Slip-in order is cover, then pages 2–6. Pages 3–4 and 5–6 face each other.

## Where the files are

- **Design master**: the Claude canvas "TKB Diner Menu". The regular menu is its first canvas page; each seasonal set has a canvas page of its own. Each artboard is one sheet. Export a set with Export › All artboards (.pdf) from its canvas page.
- **Repository** `alexshultz/tkb-menu`:
  - `design/`: every canvas page as a `.dc.html` file plus `canvas.json`. The regular pages are `Main` (cover), `Breakfast`, `Starters`, `Burgers`, `Dinner`, `Kids`. Seasonal copies carry a one-letter prefix and have the same page names.
  - `print/TKB-Diner-Menu.pdf`: the regular menu, ready to print. Seasonal PDFs are in `print/seasonal/`.
  - `word/`: the editable Word menu for the diner, the staff how-to and the drop-in pictures.
  - `assets/logos/`: the regular logo (print version and untouched original). `assets/bands/`: the checkerboard band. `assets/seasonal/`: seasonal cover art and bands.
  - `style-guide/`: a copy of this guide's text, tokens and component stylesheet.
  - `tools/`: the PDF renderer and the Word build.
  - `reference/current-menu-photos/`: photos of the menu this one replaced.
- **In this system**: the Logos, Bands, Seasonal and Print files asset groups hold the same logos, standalone SVG bands and the current PDFs.

## The Word menu

The diner edits the menu in `word/TKB Diner Menu.docx`, a native Word file built from the regular pages: prices sit on dot-leader tab stops, both fonts are embedded, and the cover art and bands are drop-in pictures. Every drop-in shares one canvas size (cover 620 × 575 px, band 756 × 34 px, transparent PNG), so Change Picture puts a new one in exactly the same place. A seasonal look is three picture changes: cover art, the band in the page header (all inside pages), and the band in the cover footer.

The canvas and the Word file are separate copies. Decide which one is current before making changes: if the diner has edited the Word file, take their file as the source and copy its changes back to the canvas before printing new PDFs.

## Rendering and checking

`tools/render.py` turns pages into one PDF with headless Chromium, using local copies of Zilla Slab and Libre Franklin and of the logos. For every page it reports:

- how much height the content needs; anything over 1056 px means the page is overfull and must be cut, not shrunk;
- anything printed inside the 1/4in safe zone.

Run it after every content change. A change to items or prices has to be made in every copy of the inside pages: the regular canvas pages, each seasonal set, and the Word file.

## Settled

- Slip-ins are plain US Letter prints.
- Two-price items are half and full orders.
- Drinks carry two decimals: fountain soda 3.00, tea 2.50 (same price iced or hot), orange juice 3.00, milk 3.00, coffee 2.50. Water is listed without a price.
- Specialty coffee drinks are on the diner's separate drink menu; the drinks section points to it.
- Dressing and descriptions both say "1000 Island".
- The lemon-lime fountain drink is Starry.
- Breakfast is served all day: said on the cover and as a tag beside the Classic Breakfast title.
- Opening hours stay off the menu.
- Gluten-free: no item marks; guests ask their server.
- Both chicken-strip entries (basket and kids) are hand-breaded to order.
