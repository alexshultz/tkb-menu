# TKB Diner menu style guide

The live, browsable version (with color swatches and component previews) is the Claude design system "TKB Diner Menu Style Guide". This folder is a copy of its text, tokens and component stylesheet. Band SVGs are in `../assets/bands/`.

TKB Diner is a small-town diner at 814 Broadway in Marysville, Kansas, serving breakfast, lunch and dinner. This system describes its printed menu: six letter-size pages that slide into the diner's existing black menu folder. Everything here is built from that menu. Use it to edit the menu, to add a page, or to make anything that should look like it belongs with it: a specials sheet, a table tent, a flyer, a social post.

The regular menu is the brand. Holiday and special-event versions are allowed to play, but they change only two things (the cover art and the band across the top of the page). See the Holidays & special events section.

## The look in one paragraph

Warm cream paper, dark brown ink, a confident slab-serif for names and prices, a plain sans for descriptions, and a single red-and-white checkerboard strip across the top of each page, like a diner tablecloth. Maroon and teal come from the original TKB cover. Nothing is glossy or trendy: it should feel like a well-run local diner that takes its food seriously.

## Voice and copy

- Plain and friendly. Say what is on the plate: "Ham, cheddar, potatoes, onions, peppers and two eggs". No adjectives the kitchen can't back up.
- The one exception is a real point of pride, said once and specifically: "Breaded by hand in our kitchen and fried crisp and golden the moment you order."
- **Item names** in Title Case, in `item-name`: "Western Burrito", "Bird's Nest", "The Black Squirrel". Keep the diner's own names exactly, including "Hobo" and "One Eyed Jack".
- **Descriptions** in sentence case, in `description`, ingredients separated by commas with "and" before the last one. No serial comma, no full stop.
- **Serving notes** go once under the section heading in italic `note` ("Served with fries · substitute any side +2"), not repeated on every item.
- **Prices** are numbers only, no dollar sign. Whole dollars have no decimals ("11"). Use decimals only where the price has cents ("4.25", "3.50"); in a column of drink prices keep two decimals throughout.
- **Two prices** for one item are written "9 / 12" until the diner confirms what the second price means; then label them ("cup 4 · bowl 6", "half 5 · full 10").
- **Separators**: a middle dot with a space each side ( · ) between short facts on one line. Add-ons are written "+2".
- Spell it the diner's way: Reuben, Rachel, Colby jack, jalapeño, Dorothy Lynch, Pepsi, Dr Pepper (no period).
- No emoji, no exclamation marks, no ALL CAPS sentences. Uppercase is only for the small spaced-out labels (`kicker`, `label`, `tagline`).
- The address is "814 Broadway · Marysville, KS 66508"; the phone is "(785) 562-3354"; social is "Join us on Facebook". Hours are not on the menu yet; don't invent them.

## Color

- Ground every page in `paper`. Set text in `ink` (names, headings), `ink-soft` (descriptions) and `ink-muted` (notes, footer).
- `maroon` is for page titles, prices and the TKB Diner name. Never set a paragraph in it.
- `teal` is for the small uppercase labels and for outlining a box. It is the second color; use it in small doses.
- Highlight a group of items by putting them on `paper-tint` with a `maroon` label. Highlight one item by giving it a solid callout: `ink` (Black Squirrel) or `maroon` (Prime Rib) with `on-dark` text. Use at most two solid callouts on a page.
- `leader` and `table-rule` are for dotted leaders and table lines only. They are too light for text (2.2:1).
- `check-red` appears only in the checkerboard band.
- The regular cover is the one dark surface: `cover-ground` with `copper` frame lines, the title in `copper-light`, text in `cover-text`. Don't carry the charcoal onto inside pages.
- Every text pairing in this system meets WCAG AA at its size; each token's note gives the ratio. Check any new pairing before using it.

## Type

- Two families, both free from Google Fonts: **Zilla Slab** (`display`) for anything you'd point at (titles, headings, item names, prices) and **Libre Franklin** (`body`) for everything you read (descriptions, notes, labels, fine print). Don't add a third face to the regular menu.
- Load them with `https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,500;0,600;1,400&family=Zilla+Slab:wght@500;600;700&display=swap`. Offline, install both from Google Fonts before opening a design file, or the page silently falls back to Georgia and Arial and runs longer.
- Use the named styles; don't invent in-between sizes. The menu runs on a small ladder: `page-title` 54, `section-heading` 23, `item-name` and `price` 18, `list-item` 15, `description` 13, `label` and `footer` 12.
- Nothing smaller than 12px (9pt) prints. Menu content (descriptions, notes) stays at 13px or larger.
- A section heading is always followed by a 2px `ink` rule running to the end of the column.

## Layout

- Pages are US Letter, portrait, designed at 816 × 1056 px (96 px per inch). Every page is one fixed sheet: if the content doesn't fit, cut or move items. Never shrink type to make it fit.
- From the top: the band (inset `band-inset-top` and `band-inset-x`), then the `kicker` and `page-title`, then the content, then the footer pinned to the bottom.
- Content sits in two equal columns `column-gap` apart inside `page-margin-x` margins. Short items can run two-up within the full width (appetizers, burgers).
- Inside a column, items stack with `item-gap` between them. A short list (sides) tightens to `list-gap`.
- Every priced line is name, dotted `leader`, price, with `leader-gap` either side. The price sits flush right with the column edge.
- The footer is address left, phone right, in `footer` style above a 1.5px `ink` rule, on every inside page.
- Keep everything printed at least `safe-zone` (1/4in) from every edge. The diner's printer cannot print there.
- Pages 3–4 and 5–6 face each other in the folder; balance their density.

## Page order (slip-in)

1. Cover
2. Classic Breakfast: Favorites, From the Griddle, 3-Egg Omelettes, Breakfast Plates, Sides & Extras
3. Appetizers & Sandwiches: Sampler, appetizers, Deli Classics, Hot Sandwiches (hand-breaded box)
4. Burgers & Baskets: add-on chips, The Black Squirrel callout, burgers, Baskets & Wraps, swap-your-fries line
5. Entrees, Soup & Salads: entrees (hand-breaded box), Prime Rib callout, soup, salads, dressings, sides
6. Kids, Drinks & Desserts: kids' meals, desserts, We Cater callout, drinks, beer table, allergy and consumer advisory

## Components

Each component below has a live preview and guidelines: PageHeader, SectionHeading, MenuItem, CompactList, ItemGrid, HighlightBox, OutlineBox, FeatureCallout, AddOnChips, BeerTable, FinePrint, PageFooter, Band, CoverRegular and SeasonalCovers. They are drawn in HTML/CSS in the menu files; there is no code bundle to import. To reuse one, copy its markup from the preview and keep the token names.

## Logos and imagery

- The regular logo (two squirrels around a coffee cup with "tkb" on it) is a picture with its own dark background. Use it only on `cover-ground` or another near-black, never on cream: its square edge shows. On cream or white, set "TKB Diner" in `cover-title` instead.
- Don't redraw, recolor, stretch or crop the squirrels. Leave at least the height of the cup clear around the logo.
- The file is 1280 px square: print it no wider than about 6.5in (200 dpi). For anything larger, ask the diner for the original artwork.
- No food photography on the menu. If a later piece uses photos, keep them on `paper` with a thin `ink` rule, never as a full-page background.

## Making other media

- **Specials sheet or insert (half or full letter)**: `paper` ground, checkerboard band at the top, `kicker` "TKB DINER", the title in `page-title`, items as MenuItems. Same margins and safe zone.
- **Table tent (4 × 6 in, folded)**: band across the top, one headline in `section-heading` or larger, at most four items, phone in the footer.
- **Flyer or poster**: one message only. "TKB Diner" in `cover-title`, the message in `page-title`, the address block in `address` and `phone`. Keep the band.
- **Social post (1080 × 1350 px or 1080 × 1080 px)**: `paper` ground, band at the top, headline in Zilla Slab 700 at roughly 90–120px, one supporting line in Libre Franklin. On a dark post, use the regular logo on `cover-ground`.
- **Website or online menu**: same two fonts, `paper` ground, `maroon` titles, `teal` labels. Prices and names follow the same copy rules.
