# TKB Diner menu

Printed menu slip-ins for TKB Diner, 814 Broadway, Marysville, KS. There are four six-page sets: the regular menu and Halloween, Thanksgiving and Christmas editions. Each page is letter size (8.5×11 in) and fits the diner's existing six-page menu folder.

The live, editable design is the Claude canvas "TKB Diner Menu" (https://claude.ai/artifact/T4UfUTeX7zyjBYndvCK3HH), with one canvas page per set: "Regular menu", "Halloween menu", "Thanksgiving menu" and "Christmas menu". This repo is a snapshot of the canvas source, the print-ready PDFs, the artwork and the reference photos.

## Style guide

`style-guide/` describes the look (colors, type, layout, components, copy rules, print rules) for anyone editing the menu or making matching material, plus a short section on holiday and special-event variations. The browsable version with swatches and live previews is the Claude design system "TKB Diner Menu Style Guide". Standalone band SVGs are in `assets/bands/`.

## Print-ready PDFs

| Set | File |
|---|---|
| Regular | `print/TKB-Diner-Menu.pdf` |
| Halloween | `print/TKB-Diner-Menu-Halloween.pdf` |
| Thanksgiving | `print/TKB-Diner-Menu-Thanksgiving.pdf` |
| Christmas | `print/TKB-Diner-Menu-Christmas.pdf` |

Each PDF is six letter-size pages in slip-in order, with no margins added. Print at 100% / actual size.

## Page order

| Slip-in | Regular | Halloween | Thanksgiving | Christmas |
|---|---|---|---|---|
| 1 · Cover | `design/Main.dc.html` | `design/HCover.dc.html` | `design/TCover.dc.html` | `design/XCover.dc.html` |
| 2 · Classic Breakfast | `design/Breakfast.dc.html` | `design/HBreakfast.dc.html` | `design/TBreakfast.dc.html` | `design/XBreakfast.dc.html` |
| 3 · Appetizers & Sandwiches | `design/Starters.dc.html` | `design/HStarters.dc.html` | `design/TStarters.dc.html` | `design/XStarters.dc.html` |
| 4 · Burgers & Baskets | `design/Burgers.dc.html` | `design/HBurgers.dc.html` | `design/TBurgers.dc.html` | `design/XBurgers.dc.html` |
| 5 · Entrees, Soup & Salads | `design/Dinner.dc.html` | `design/HDinner.dc.html` | `design/TDinner.dc.html` | `design/XDinner.dc.html` |
| 6 · Kids, Drinks & Desserts | `design/Kids.dc.html` | `design/HKids.dc.html` | `design/TKids.dc.html` | `design/XKids.dc.html` |

Pages 3–4 and 5–6 face each other as spreads in the folder.

`design/canvas.json` is the canvas index (artboard positions, titles, canvas pages). The `.dc.html` files are the canvas's Design Component sources; they render inside the canvas editor, not as standalone web pages.

## Themes

Every set uses the same inside pages: cream background, maroon and teal, identical content. A seasonal set differs in only two ways:

- its own cover, with that season's squirrel artwork on cream and no holiday name in the wording;
- the decorative band at the top of each inside page (and top and bottom of the cover).

| Set | Cover | Band |
|---|---|---|
| Regular | Dark charcoal-and-copper squirrel logo | Red-and-white checkerboard |
| Halloween | Witch-hat squirrels with cauldron, on cream | Autumn leaves and jack-o'-lanterns |
| Thanksgiving | Pilgrim-hat squirrels with the TKB basket, on cream | Turkeys and pumpkins |
| Christmas | Santa-hat squirrels with a mug of cocoa, on cream | Garland with tree-light bulbs, candy canes and glass ball ornaments |

The menu content is identical across sets, so a price or item change has to be made on all four.

## Printer safe area

The diner's printer can't print the outer 1/4" (24px) of the page. Every band, rule and line of text sits at least that far in: bands start about 0.3" from the top and side edges. `tools/render.py` flags anything that prints inside that zone. The page background colors (cream inside, charcoal on the regular cover) are the only things that run to the edge, so a thin unprinted white margin will show around them on that printer.

## Artwork

The covers load their logos from the canvas's asset store. The same files are here:

| Canvas asset URL | File | Notes |
|---|---|---|
| `/_blob/940e0c31f89f681f04797625015c052e` | `assets/logos/tkb-logo-print.png` | Regular logo. "Imagined with AI" badge painted out, edges feathered so it blends into the dark cover. |
| `/_blob/ea027bf410aeb5870851acef4f79a9db` | `assets/logos/tkb-halloween-logo-print.png` | Halloween logo. White background fully removed so it sits on the cream cover. |
| `/_blob/2abc776de8bc8d9254c318631aca7628` | `assets/logos/tkb-thanksgiving-logo-print.png` | Thanksgiving logo (TKB woven into the basket). White background fully removed. |
| `/_blob/fe620ff1479fda4324bf3a8f10c4d003` | `assets/logos/tkb-christmas-logo-print.png` | Christmas logo (Santa hats, cocoa mug). White background fully removed. |

The untouched source images are in `assets/logos/original/`.

## Rendering the PDFs

`tools/render.py` turns a set of `.dc.html` pages into one PDF with headless Chromium (Playwright), using local copies of the fonts from the `@fontsource` npm packages (Zilla Slab, Libre Franklin, Creepster) and local copies of the logos. It also reports how much height each page needs, warns when a page's content needs more than 1056px (one letter page), because the page would otherwise be squeezed silently, and flags any text, image or colored box that falls inside the printer's 1/4" no-print zone.

## Reference

`reference/current-menu-photos/` holds the photos of the diner's previous menu that the content was transcribed from.

## Open questions for the diner

- Two-price items (biscuits & gravy 4/7, sandwiches 9/11 and 10/12, salads 9/12): what the second price means, so it can be labeled.
- Tea, coffee, milk and orange juice have no prices.
- The old menu marked gluten-free items with *, but no items carried the mark. The new menu says "ask your server" instead.
- Kids' chicken strips: are they hand-breaded like the basket strips? They are not tagged yet.
- Sierra Mist was renamed Starry in 2023.
- Confirm the slip-in sleeves are letter size.
