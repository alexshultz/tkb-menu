# TKB Diner menu

Printed menu slip-ins for TKB Diner, 814 Broadway, Marysville, KS. There are two six-page sets: the regular menu and a Halloween edition. Each page is letter size (8.5×11 in) and fits the diner's existing six-page menu folder.

The live, editable design is the Claude canvas "TKB Diner Menu" (https://claude.ai/artifact/T4UfUTeX7zyjBYndvCK3HH). It has two canvas pages, "Regular menu" and "Halloween menu". To print a set, open that canvas page and use Export › All artboards (.pdf). This repo is a snapshot of the canvas source plus the artwork and reference photos.

## Page order

| Slip-in | Regular | Halloween |
|---|---|---|
| 1 · Cover | `design/Main.dc.html` | `design/HCover.dc.html` |
| 2 · Classic Breakfast | `design/Breakfast.dc.html` | `design/HBreakfast.dc.html` |
| 3 · Appetizers & Sandwiches | `design/Starters.dc.html` | `design/HStarters.dc.html` |
| 4 · Burgers & Baskets | `design/Burgers.dc.html` | `design/HBurgers.dc.html` |
| 5 · Entrees, Soup & Salads | `design/Dinner.dc.html` | `design/HDinner.dc.html` |
| 6 · Kids, Drinks & Desserts | `design/Kids.dc.html` | `design/HKids.dc.html` |

Pages 3–4 and 5–6 face each other as spreads in the folder.

`design/canvas.json` is the canvas index (artboard positions, titles, canvas pages). The `.dc.html` files are the canvas's Design Component sources; they render inside the canvas editor, not as standalone web pages.

## Artwork

The covers load their logos from the canvas's asset store. The same files are here:

| Canvas asset URL | File | Notes |
|---|---|---|
| `/_blob/940e0c31f89f681f04797625015c052e` | `assets/logos/tkb-logo-print.png` | Regular logo. "Imagined with AI" badge painted out, edges feathered so it blends into the dark cover. |
| `/_blob/2819d2ad73cbbc96e316763654be92bd` | `assets/logos/tkb-halloween-logo-print.png` | Halloween logo. White background removed, cream sticker outline added for the dark cover. |

The untouched source images are in `assets/logos/original/`.

## Reference

`reference/current-menu-photos/` holds the photos of the diner's previous menu that the content was transcribed from.

## Open questions for the diner

- Two-price items (biscuits & gravy 4/7, sandwiches 9/11 and 10/12, salads 9/12): what the second price means, so it can be labeled.
- Tea, coffee, milk and orange juice have no prices.
- The old menu marked gluten-free items with *, but no items carried the mark. The new menu says "ask your server" instead.
- Sierra Mist was renamed Starry in 2023.
- Confirm the slip-in sleeves are letter size.
