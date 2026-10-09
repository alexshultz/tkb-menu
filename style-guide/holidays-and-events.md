# Holidays & special events

Holiday menus are for fun. They borrow everything from the regular menu and change only two things, so a seasonal set can be made in an afternoon and still look like TKB Diner. The same recipe works for a special event (an anniversary, a town festival, a fundraiser night).

## What changes

1. **The cover art.** A seasonal version of the two squirrels replaces the regular logo, sitting directly on `paper` with its white background removed. The cover is cream, not charcoal.
2. **The band.** The checkerboard strip is replaced by a strip of small seasonal shapes, at the top of every inside page and at the top and bottom of the cover.

## What never changes

- The inside pages: `paper` ground, `maroon` and `teal`, the same fonts, sizes, layout, content and prices as the regular menu.
- The cover text: "TKB Diner" in `cover-title` (maroon), the `tagline` "BREAKFAST · LUNCH · DINNER" between teal rules, then the address block. **Never write the occasion on the cover** ("Halloween Menu", "Merry Christmas"). The art says it.
- Seasonal colours stay inside the band and the cover art. They never color text, headings or callouts.
- The printer's `safe-zone`.

## Cover art

- Keep the formula: the same two squirrels facing each other over a steaming drink, in a seasonal costume, with "tkb" or "TKB" on the vessel and seasonal objects at the base.
- Remove the white background completely so the art sits on `paper`. No box, no drop shadow.
- On the cover, fit the art in a box 620 px wide and about 545–575 px tall, centered, 24–28 px below the top band.
- The art files are about 1300 px wide; at 620 px on the page they print at roughly 200 dpi, which is the minimum. Ask for larger artwork if the art needs to print bigger.

## Bands

A band is one SVG strip, 756 px wide (`band-width`) and 30–34 px tall, placed `band-inset-top` from the top edge and `band-inset-x` from each side. It repeats a tile of two to five small motifs.

- Draw flat shapes with no gradients and no outlines thinner than 1px. Use 3–5 saturated colors that read on cream.
- White or very pale parts (candy-cane stripes, snow) need a thin darker outline or they vanish on `paper`.
- Keep motifs about 22–28 px tall so they read as a border, not as clip art.
- Set a 1.5px `ink` rule under bands that sit on a flat baseline (checkerboard aside). A hanging garland needs no rule.
- On the cover, repeat the band at the bottom, inset 28 px from the bottom edge.
- Store each band as its own SVG (Seasonal asset group here, `assets/seasonal/bands/` in the repository) so it can be reused on table tents and social posts. For the Word menu, also export it as a 756 × 34 px PNG with a transparent background.

## Existing sets

Each holiday set so far is a copy of the six regular pages with its own cover art and band. They live beside the regular menu on the canvas (one canvas page per set) and in the repository under the seasonal folders. Treat them as examples to copy, not as part of the regular menu.

## Making a new set

1. Get the cover art (same formula) and remove its background.
2. Draw the band tile and check it at 300% zoom: every motif should be recognizable.
3. On the canvas: copy the six regular pages, replace the checkerboard band with the new band on each inside page, and build the cover from an existing seasonal cover with the art and both bands swapped. In the Word menu: change the three pictures (cover art, header band, cover footer band); the art goes on a 620 × 575 px transparent canvas.
4. Render the PDF and check that every page still fits on one sheet and nothing sits inside the safe zone.
5. Print one test sheet on the diner's printer before printing the set.

## Special-event pieces

For a one-off event flyer or table tent, use the regular look with an event band (or the checkerboard) and say the event in the headline: here, unlike the menu cover, the words do the work. Example: kicker "TKB DINER", title "Prime Rib Weekend", one line of detail, date, phone.
