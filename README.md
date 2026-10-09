# TKB Diner menu

The printed menu for TKB Diner, 814 Broadway, Marysville, Kansas · (785) 562-3354. The menu is six US Letter pages, printed on plain paper and slid into the diner's existing six-sleeve menu folder.

## How the menu system works

**The regular menu is the menu.** Six pages in this order:

1. Cover
2. Classic Breakfast
3. Appetizers & Sandwiches
4. Burgers & Baskets
5. Entrees, Soup & Salads
6. Kids, Drinks & Desserts

Pages 3–4 and 5–6 face each other in the folder.

**One look, written down.** Colors, type, layout, components, copy rules and print rules are in the style guide (`style-guide/`, and the browsable Claude design system "TKB Diner Menu Style Guide"). Anything new, whether a page, a specials sheet, a flyer or a social post, follows it.

**Seasonal and event versions are optional extras.** They reuse the regular inside pages unchanged and swap only two things: the cover art (a themed version of the two TKB squirrels) and the decorative band across the top of each page. They are made as the occasion comes up. The ones made so far are kept in the `seasonal/` folders as examples.

**The menu exists in three forms:**

| Form | Where | Used for |
| --- | --- | --- |
| Design canvas | Claude canvas "TKB Diner Menu" (snapshot in `design/`) | The design master. Layout changes, new pages, new seasonal sets. |
| Print PDF | `print/TKB-Diner-Menu.pdf` | Printing. Six pages, 100% size, no bleed. |
| Word file | `word/TKB Diner Menu.docx` | The diner's own edits: prices, items, seasonal picture swaps. |

The canvas and the Word file are separate copies of the same content. Whoever changes one has to carry the change to the other (see Changing the menu).

## What's where

| Path | Contents |
| --- | --- |
| `print/TKB-Diner-Menu.pdf` | The regular menu, print-ready. |
| `print/seasonal/` | Print-ready PDFs of seasonal sets. |
| `word/TKB Diner Menu.docx` | Editable regular menu for Microsoft Word: prices on dot-leader tab stops, fonts embedded, drop-in cover picture and bands. |
| `word/How to update the menu.docx` | Two-page guide for diner staff: editing items, swapping pictures, printing, fonts. |
| `word/Pictures/` | Drop-in pictures for the Word file. `cover-regular.png` and `band-regular.png` are the everyday look; the others are seasonal. Every cover picture is a 620 × 575 px canvas and every band a 756 × 34 px canvas (transparent PNGs; covers stored at 2×, bands at 4× for sharp printing), so Change Picture swaps one for another in place. |
| `design/` | Snapshot of the canvas: one `.dc.html` file per page plus `canvas.json` (artboard positions and canvas pages). The regular pages are `Main` (cover), `Breakfast`, `Starters`, `Burgers`, `Dinner`, `Kids`. Seasonal copies carry a one-letter prefix and the same page names. These files render inside the canvas editor or through `tools/render.py`, not as standalone web pages. |
| `style-guide/` | The style guide: `README.md` (brand book for the regular menu), `holidays-and-events.md` (how to make a seasonal or event version), `print-and-files.md` (printing, files, open questions), `tokens.json` (every color, type style, spacing and size), `components.css` and `components/` (the building blocks and their rules). |
| `assets/logos/` | The regular logo: `tkb-logo-print.png` (cleaned-up print version) and `original/`. |
| `assets/bands/` | The checkerboard band as a standalone SVG. |
| `assets/seasonal/` | Seasonal cover art (`art/`, with untouched originals in `art/original/`) and seasonal bands (`bands/`, SVG). |
| `tools/render.py` | Renders canvas pages to a PDF and checks each page fits one sheet and clears the printer's dead zone. |
| `tools/word/` | Builds the Word file and the staff guide. |
| `reference/current-menu-photos/` | Photos of the menu this one replaced. |

## Changing the menu

**A price or an item.** First decide which copy is current. If the diner has edited the Word file, get their file and treat it as the source.

1. Make the change in the canvas: on the regular pages, and on any seasonal set that will be printed again.
2. Make the same change in the Word file (by hand, or edit `tools/word/build.js` and rebuild).
3. Render the PDF with `tools/render.py` and check that every page reports 1056 px or less and no EDGE warnings. Pages 5 and 6 are close to full: an added item there usually means trimming something else. Never shrink the type.
4. Commit the updated `design/`, `print/` and `word/` files.

**A new page or a layout change.** Do it on the canvas following the style guide, then render and commit. The Word file has to be rebuilt to match.

**A seasonal or event version.** Follow `style-guide/holidays-and-events.md`: new cover art in the same formula (two squirrels over a drink, no words on the cover) and a new band. In the Word file, that is three picture changes. On the canvas, copy the regular pages to a new canvas page and swap the cover art and bands.

**Other printed or digital pieces.** Start from the "Making other media" section of the style guide.

## Printing

US Letter, plain paper, 100% / Actual size, no bleed. The diner's printer cannot print the outer 1/4 in, so everything printed sits at least that far in. Only the page color reaches the edge, which leaves a thin white rim. Print one test sheet before a full run.

## Tools

**PDF renderer** (`tools/render.py`):

```
cd tools && npm install && cd ..
pip install playwright pypdf fonttools && python3 -m playwright install chromium
python3 tools/render.py print/TKB-Diner-Menu.pdf design/Main.dc.html design/Breakfast.dc.html \
    design/Starters.dc.html design/Burgers.dc.html design/Dinner.dc.html design/Kids.dc.html
```

It loads Zilla Slab and Libre Franklin from `tools/node_modules` and maps the canvas's picture links (`/_blob/<id>`) to the repo's logo files. A newly uploaded cover picture needs a line in its `BLOBS` table.

**Word build** (`tools/word/`):

```
python3 tools/word/make-fonts.py
node tools/word/build.js word/Pictures tools/word/fonts word/build/raw.docx
python3 tools/word/fixup.py word/build/raw.docx "word/TKB Diner Menu.docx"
node tools/word/howto.js "word/How to update the menu.docx"
```

`make-fonts.py` turns each font weight into its own single-style TrueType family ("Zilla Slab SemiBold", "Libre Franklin Medium" and so on), because docx-js embeds one style per font name. `build.js` lays out the six pages. `fixup.py` makes the file open cleanly in Word: it upper-cases the embedded-font keys, gives each picture a unique id, and keeps fonts embedded when the file is re-saved.

## Settled content decisions

- Slip-ins are plain US Letter prints.
- Two-price items are half and full orders, written "half 4 · full 7".
- Drinks are priced with two decimals: fountain soda 3.00, tea (iced or hot) 2.50, orange juice 3.00, milk 3.00.
- Gluten-free: no items are marked; the allergy note asks guests to tell their server.
- Hand-breaded to order: Pork Tender, Chicken Fried Chicken and Country Fried Steak (sandwiches and entrees), and both chicken-strip entries (basket and kids).

## Open questions for the diner

- Coffee has no price yet. It is listed with water as "Also: coffee and water".
- Tea is listed as one price for iced or hot. Confirm both cost 2.50.
- The dressing list says "Thousand Island" and item descriptions say "1000 Island". Pick one.
- Sierra Mist was renamed Starry in 2023.
- Opening hours, if they should go on the cover.
