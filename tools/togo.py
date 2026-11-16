"""Generates the two-sided to-go / online menu (design/proposed/ToGoFront.dc.html and
ToGoBack.dc.html) from the content below. Same look as the full menu, tighter set.

usage: python3 tools/togo.py
"""
import pathlib, html

OUT = pathlib.Path(__file__).resolve().parent.parent / "design" / "proposed"
E = html.escape

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>TKB Diner to-go menu, {side}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,500;0,600;1,400&amp;family=Zilla+Slab:wght@500;600;700&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
.band{{height:16px;margin:28px 30px 0;flex-shrink:0;background:conic-gradient(#A3302F 25%,#FFFFFF 0 50%,#A3302F 0 75%,#FFFFFF 0) 0 0/16px 16px}}
.kicker{{font:600 12px/1 'Libre Franklin',sans-serif;letter-spacing:.24em;text-transform:uppercase;color:#2E6A68}}
.sec{{margin:0;font:700 18px/1.1 'Zilla Slab',serif;color:#2A1E18;display:flex;align-items:center;gap:10px}}
.sec::after{{content:"";flex:1;height:2px;background:#2A1E18}}
.big{{margin:0;font:700 24px/1.05 'Zilla Slab',serif;color:#8A2A2B}}
.note{{font:italic 400 12px/1.35 'Libre Franklin',sans-serif;color:#5A4636}}
.it{{display:flex;flex-direction:column;gap:0}}
.row{{display:flex;align-items:baseline;gap:6px}}
.nm{{font:600 14.667px/1.2 'Zilla Slab',serif;color:#2A1E18}}
.ld{{flex:1;min-width:8px;border-bottom:2px dotted #B9A68F;transform:translateY(-3px)}}
.pr{{font:700 14.667px/1.2 'Zilla Slab',serif;color:#8A2A2B;white-space:nowrap}}
.ds{{font:400 12px/1.3 'Libre Franklin',sans-serif;color:#4E3D31}}
.lbl{{font:600 12px/1 'Libre Franklin',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#2E6A68}}
.lblm{{font:600 12px/1 'Libre Franklin',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#8A2A2B}}
.col{{display:flex;flex-direction:column;gap:5px;min-width:0}}
.blk{{display:flex;flex-direction:column;gap:7px}}
.mini .nm{{font:500 13.333px/1.25 'Libre Franklin',sans-serif}}
.mini .pr{{font:700 13.333px/1.25 'Zilla Slab',serif}}
.tint{{background:#F1E4D0;border-radius:8px;padding:8px 10px;display:flex;flex-direction:column;gap:6px}}
.box{{border:2px solid #2E6A68;border-radius:8px;padding:8px 10px;display:flex;flex-direction:column;gap:5px}}
.dark{{background:#2A1E18;border-radius:8px;padding:8px 10px;display:flex;flex-direction:column;gap:2px}}
.hb{{font-weight:600;color:#8A2A2B}}
.foot{{display:flex;justify-content:space-between;font:500 12px/1 'Libre Franklin',sans-serif;color:#5A4636;border-top:1.5px solid #2A1E18;padding-top:8px}}
</style>
</helmet>
<div style="width: 816px; height: 1056px; box-sizing: border-box; background: #FFFFFF; color: #2A1E18; font-family: 'Libre Franklin', sans-serif; display: flex; flex-direction: column; overflow: hidden">
<div class="band"></div>
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 10px; padding: 14px 36px 28px">
{body}
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":816,"height":1056}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""


def item(name, price, desc=None, tag=None):
    d = ""
    if desc or tag:
        t = f'<span class="hb">{E(tag)}</span>' + (" · " if desc else "") if tag else ""
        d = f'<div class="ds">{t}{E(desc or "")}</div>'
    return f'<div class="it"><div class="row"><span class="nm">{E(name)}</span><span class="ld"></span><span class="pr">{E(price)}</span></div>{d}</div>'


def mini(rows, cols=1):
    cells = "".join(f'<div class="row"><span class="nm">{E(n)}</span><span class="ld"></span><span class="pr">{E(p)}</span></div>' for n, p in rows)
    grid = f"display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));column-gap:14px;row-gap:3px"
    return f'<div class="mini" style="{grid}">{cells}</div>'


def sec(t):
    return f'<h2 class="sec">{E(t)}</h2>'


def note(t):
    return f'<div class="note">{t}</div>'


def header(subtitle, compact=False):
    if compact:
        return f"""<div style="display:flex;align-items:baseline;justify-content:space-between;gap:16px"><div style="font:700 24px/1 'Zilla Slab',serif;color:#8A2A2B">TKB Diner <span style="font:600 16px/1 'Zilla Slab',serif;color:#2A1E18">{subtitle}</span></div><div style="font:700 20px/1 'Zilla Slab',serif;color:#2A1E18">(785) 562-3354</div></div>"""
    return f"""<div style="display:flex;align-items:flex-end;justify-content:space-between;gap:16px">
<div style="display:flex;flex-direction:column;gap:6px"><div class="kicker">Breakfast · Lunch · Dinner</div><h1 style="margin:0;font:700 40px/1 'Zilla Slab',serif;color:#8A2A2B">TKB Diner <span style="font:600 22.667px/1 'Zilla Slab',serif;color:#2A1E18">{subtitle}</span></h1></div>
<div style="text-align:right;display:flex;flex-direction:column;gap:4px"><div style="font:700 26px/1 'Zilla Slab',serif;color:#2A1E18">(785) 562-3354</div><div class="ds" style="font-size:13.333px">Call ahead for pickup · 814 Broadway, Marysville, KS</div></div>
</div>"""


SWAP = ('<b style="font-weight:600;color:#2A1E18;font-style:normal">Sandwiches and burgers come with fries.</b> '
        '<span style="font-style:normal">Swap your fries <b class="hb">+2</b>: veggie of the day, baked potato, mashed potatoes &amp; gravy, '
        'side salad, seasonal salad, or cup of soup · <b class="hb">+4</b>: sweet potato fries or an appetizer · '
        '<b class="hb">+5</b>: loaded baked potato</span>')


def H(t, top=True):
    return f'<h2 class="big"{" style=\"margin-top:6px\"" if top else ""}>{t}</h2>'


def blocks():
    b = {}
    b["breakfast1"] = [
        '<div class="row" style="align-items:center;justify-content:space-between"><h2 class="big">Classic Breakfast</h2>'
        '<div style="border:1.5px solid #2E6A68;border-radius:6px;padding:4px 7px;white-space:nowrap" class="lbl">All day</div></div>',
        sec("Favorites"),
        item("Biscuits & Gravy", "half 4 · full 7", "Biscuits and homemade sausage gravy"),
        item("Breakfast Sandwich", "8", "Choice of ham, bacon, or sausage, plus cheese and one egg"),
        item("Breakfast Burrito", "9", "Choice of meat, cheddar, and two eggs"),
        item("Western Burrito", "11", "Ham, cheddar, potatoes, onions, peppers, and two eggs"),
        item("Breakfast Bowl", "10", "Hashbrowns, ham, bacon, sausage, cheese, veggies, and two eggs"),
        item("Stacked Hashbrowns", "11", "Ham, bacon, sausage, cheese, veggies, and two eggs"),
        sec("From the Griddle"),
        item("French Toast", "half 5 · full 10", "Powdered sugar, side of syrup · add blueberries +1"),
        item("Pancakes", "1 for 2 · 3 for 5 · 6 for 8", "Single, short stack, or full stack"),
        item("Oatmeal", "6", "Brown sugar, craisins, and pecans"),
        sec("3-Egg Omelettes"),
        note("Served with your choice of toast"),
        item("Denver", "12", "Ham, cheddar, onions, and peppers"),
        item("Garden", "11", "All the veggies and cheese"),
        item("Meat & Cheese", "12", "Ham, bacon, or sausage"),
    ]
    b["breakfast2"] = [
        sec("Breakfast Plates"),
        item("One Eyed Jack", "5", "One egg and toast"),
        item("Hobo", "6", "Two eggs and toast"),
        item("Bird's Nest", "9", "One egg, choice of meat, and toast"),
        item("Bullseye", "10", "Two eggs, choice of meat, and toast"),
        sec("Sides & Extras"),
        mini([("Hashbrowns", "3"), ("Toast", "3"), ("Sausage gravy", "3"), ("Biscuit", "2"),
              ("Ham, bacon, or sausage", "4"), ("Egg", "2"), ("Cheese", "2"), ("Onion, pepper, jalapeño", "1")]),
    ]
    b["apps"] = [
        H("Appetizers"),
        '<div class="box">' + item("Sampler, pick any 3", "13") + "</div>",
        mini([("Corn Nuggets", "8"), ("Onion Rings", "9"), ("Pickle Chips", "8"), ("Mozzarella Sticks", "9"),
              ("Cheeseballs", "9"), ("Jalapeño Bites", "9"), ("Spinach Artichoke Dip", "9"), ("Broccoli & Cheese Bites", "9"),
              ("Mac & Cheese Wedges", "9"), ("French Fries", "7"), ("Sweet Potato Fries", "8")]),
    ]
    b["sandwiches"] = [
        H("Sandwiches", False),
        sec("Deli Classics"),
        item("BLT", "half 9 · full 11", "Wheat, bacon, lettuce, tomato, mayo"),
        item("Reuben", "half 10 · full 12", "Rye, corned beef, 1000 Island, sauerkraut, Swiss"),
        item("Rachel", "half 10 · full 12", "Rye, turkey, 1000 Island, sauerkraut, Swiss"),
        item("Club", "half 10 · full 12", "Sourdough, turkey, bacon, tomato, ranch, Colby jack"),
        sec("Hot Sandwiches · 13"),
        note("On a bun with mayo; lettuce, tomato, and onion on the side"),
        '<div class="tint"><div class="lblm">Hand-breaded to order</div>'
        + item("Pork Tender", "13") + item("Chicken Fried Chicken", "13") + item("Country Fried Steak", "13") + "</div>",
        item("Grilled Chicken", "13"),
        item("Philly", "13", "Hoagie bun, peppers, onions, Swiss"),
    ]
    b["baskets"] = [
        H("Baskets &amp; Wraps"),
        item("Fish & Chips", "14", "8 oz walleye strips and fries"),
        item("Shrimp", "15", "8 butterfly shrimp and fries"),
        item("Chicken Strips", "14", "4 chicken strips and fries", tag="Hand-breaded to order"),
        item("Chicken Nuggets", "12", "3 chicken strips cut bite-size, with fries", tag="Hand-breaded to order"),
        item("CBR Wrap", "12", "Crispy or grilled chicken, bacon, ranch, cheese, lettuce, tomato"),
    ]
    b["kids"] = [
        '<div class="tint" style="margin-top:6px"><div class="lblm">Kids\' Meals</div><div class="ds" style="font-style:italic;margin-top:-3px">Choose fries, mac &amp; cheese, or mashed potatoes</div>'
        + mini([("Chicken Strips (2)", "8"), ("Hamburger", "9"), ("Grilled Cheese", "7"), ("PB&J", "7")]) + "</div>",
    ]
    b["burgers"] = [
        H("Burgers", False),
        note("Served with fries; see the swaps on the front"),
        note('<span style="font-style:normal"><b class="lbl" style="letter-spacing:.12em">Add</b> cheese <b class="hb">+1</b> · peppers or jalapeños <b class="hb">+1</b> · bacon <b class="hb">+2</b> · extra patty <b class="hb">+3</b></span>'),
        '<div class="dark"><div class="row"><span class="nm" style="color:#fff">The Black Squirrel</span><span class="ld" style="border-color:#8C7A66"></span><span class="pr" style="color:#F2C9A0">14</span></div><div class="ds" style="color:#E9DFCF">Bacon jam, muenster &amp; gouda, Nutella</div></div>',
        item("Plain Jane", "12", "Just the burger patty"),
        item("Patty Melt", "13", "Rye, 1000 Island, Swiss"),
        item("The Whiskey", "14", "Swiss, cheddar, bacon, onion tanglers, whiskey sauce"),
        item("The Firehouse", "14", "Pepper jack, bacon, jalapeño, sriracha mayo"),
        item("TKB Melt", "14", "Swiss, grilled peppers, onions and mushrooms, garlic aioli"),
        item("The Carter", "14", "Cheddar & Swiss, onion tanglers, bacon, fried egg, ranch"),
        item("The Sunrise", "14", "Cheddar, bacon, fried egg"),
        item("The Midwest", "14", "Colby jack, onion ring, BBQ sauce"),
        item("The Club", "14", "Colby jack, turkey, bacon, tomato, ranch"),
        item("The Reuben Burger", "14", "Swiss, corned beef, sauerkraut, 1000 Island"),
    ]
    b["entrees"] = [
        H("Entrees", False),
        note("With your choice of two sides and a dinner roll"),
        item("Steak Bites", "½ lb 18 · 1 lb 23"),
        '<div class="tint"><div class="lblm">Hand-breaded to order</div>'
        + item("Chicken Fried Chicken", "18") + item("Country Fried Steak", "19") + item("Pork Tender", "17") + "</div>",
        item("Hamburger Steak", "17", "Sautéed mushrooms and onions optional"),
        item("Grilled Chicken", "17"),
        item("12 oz KC Strip", "26"),
        '<div style="background:#8A2A2B;border-radius:8px;padding:8px 10px;display:flex;flex-direction:column;gap:2px">'
        '<div class="lbl" style="color:#F2D9C0;line-height:1.3">Last Friday &amp; Saturday of the month</div>'
        '<div class="row"><span class="nm" style="color:#fff">Prime Rib</span><span class="ld" style="border-color:#C98A7E"></span><span class="pr" style="color:#fff">26</span></div>'
        '<div class="ds" style="color:#F4E6DA">With two sides and a dinner roll</div></div>',
        '<div class="box"><div class="row" style="align-items:baseline;gap:8px"><span class="lbl">Sides</span><span class="ds" style="font-style:italic">Choose two with any entree</span></div>'
        '<div class="ds" style="color:#2A1E18">Fries · Veggie of the day · Baked potato · Mac &amp; cheese · Side salad · Cup of soup · Mashed potatoes &amp; gravy</div>'
        '<div class="lbl" style="margin-top:3px">Premium sides</div>'
        + mini([("Sweet potato fries", "+2"), ("An appetizer", "+2"), ("Loaded baked potato", "+3")]) + "</div>",
    ]
    b["soup"] = [
        H("Homemade Soup", False),
        '<div class="row"><span class="nm">Cup 4 · Bowl 6</span></div>'.replace('<span class="nm">Cup 4 · Bowl 6</span>', '<span class="nm">Cup</span><span class="ld"></span><span class="pr">4</span><span style="width:16px"></span><span class="nm">Bowl</span><span class="ld"></span><span class="pr">6</span>'),
        note("Call to ask about today's soups"),
    ]
    b["soupsalad"] = [
        H("Salads"),
        item("Chef", "half 9 · full 12", "Ham, turkey, tomatoes, cheddar, hard-boiled egg"),
        item("Greek", "half 9 · full 12", "Spinach, chicken, olives"),
        item("Grilled Chicken", "half 9 · full 12", "Grilled chicken breast"),
        '<div class="ds"><b style="font-weight:600;color:#2A1E18">Dressings:</b> homemade ranch, blue cheese, raspberry vinaigrette, Dorothy Lynch, Italian, 1000 Island, honey mustard</div>',
    ]
    b["desserts"] = [
        H("Desserts"),
        note("Ask about today's homemade desserts"),
        mini([("Pie", "4.25"), ("Cheesecake", "4.75")], cols=2),
    ]
    b["cater"] = [
        '<div class="dark" style="margin-top:6px"><div class="lbl" style="color:#9FD3CF">We cater</div>'
        '<div class="nm" style="color:#fff">Weddings, parties, and meetings</div>'
        '<div class="ds" style="color:#E9DFCF">Call for our catering menu and pricing.</div></div>',
    ]
    grid = ('<div style="display:grid;grid-template-columns:minmax(0,1.6fr) repeat(4,minmax(0,.5fr));column-gap:4px;row-gap:3px;align-items:baseline">'
            + "".join(f'<div class="lbl" style="font-size:12px;letter-spacing:.04em;{"text-align:right" if i else ""}">{h}</div>' for i, h in enumerate(["oz", "12", "16", "20", "32"]))
            + "".join(f'<div class="nm" style="font-size:13.333px">{n}</div>' + "".join(f'<div class="pr" style="font-size:13.333px;text-align:right;{"color:#B9A68F" if p == "—" else ""}">{p}</div>' for p in ps)
                      for n, ps in [("Latte, macchiato", ["4.75", "5.25", "5.75", "7.00"]), ("Frappe", ["—", "5.00", "5.75", "6.75"]),
                                    ("Shaken espresso", ["—", "4.00", "4.50", "5.00"]), ("Cold brew", ["—", "3.00", "3.25", "4.00"])])
            + "</div>")
    spec = [("Apple Pie", "apple, brown sugar cinnamon, and vanilla"), ("Black Squirrel", "chocolate, hazelnut, and almond"),
            ("Blonde", "white chocolate, caramel, and toasted marshmallow"), ("Blueberry Pie", "blueberry, brown sugar cinnamon, and vanilla"),
            ("Caramel Kiss", "caramel and French vanilla"), ("Fluffernutter", "peanut butter and toasted marshmallow"),
            ("Honeybee", "honey, rose or lavender, and vanilla"), ("London Fog", "Earl Grey tea, vanilla, lavender, and steamed milk"),
            ("Nutty Monkey", "caramel, banana, and peanut butter"), ("Peppermint Patty", "chocolate and peppermint"),
            ("Turtle", "chocolate, caramel, and toffee")]
    b["coffee"] = [
        H("Coffee Bar"),
        note("Latte and macchiato hot or iced; 12 oz is hot, 32 oz is iced · 3 add-ins included, extras +1.25 each"),
        grid,
        '<div class="row" style="gap:8px;margin-top:3px"><span class="lblm">Specialty drinks</span><span class="ds" style="font-style:italic">any size, same price</span></div>',
        "".join(f'<div class="ds" style="padding-left:10px;text-indent:-10px"><b style="font:600 13.333px/1.25 \'Zilla Slab\',serif;color:#2A1E18">{E(n)}</b> {E(d)}</div>' for n, d in spec),
    ]
    b["drinks"] = [
        H("Drinks"),
        item("Fountain soda", "3.00", "24 oz · Pepsi, Diet Pepsi, Mountain Dew, Dr Pepper, Starry"),
        mini([("Tea, iced or hot", "2.50"), ("Coffee", "2.50"), ("Orange juice", "3.00"), ("Milk", "3.00")]),
    ]
    return b


FRONT = [["breakfast1", "desserts"], ["breakfast2", "apps", "kids"], ["sandwiches", "baskets"]]
BACK = [["burgers", "drinks"], ["entrees", "soupsalad"], ["soup", "coffee", "cater"]]
FINE = ('<div style="font:400 12px/1.4 \'Libre Franklin\',sans-serif;color:#4E3D31;display:flex;flex-direction:column;gap:4px;border-top:1.5px dotted #B9A68F;padding-top:8px">'
        '<div><b style="font-weight:600;color:#2A1E18">Allergies &amp; gluten-free:</b> Many items are or can be made gluten-free. Tell us about any allergies when you order and we will accommodate as best we can. Ours is an open-air kitchen, so cross-contact is always a risk.</div>'
        '<div><b style="font-weight:600;color:#2A1E18">Consumer advisory:</b> Eggs on our menu can be ordered raw or undercooked. Consuming raw or undercooked meats, poultry, seafood, shellfish, or eggs may increase your risk of foodborne illness. For more information, see the Kansas Department of Agriculture website.</div></div>')


def page(side, layout, b):
    cols = "".join('<div class="col">' + "".join("".join(b[k]) for k in ks) + "</div>" for ks in layout)
    grid = f'<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:24px;flex-grow:1;align-content:start">{cols}</div>'
    if side == "front":
        body = (header("Takeout menu")
                + f'<div class="note" style="border-top:1.5px solid #2A1E18;border-bottom:1.5px solid #2A1E18;padding:6px 0">{SWAP}</div>'
                + grid + '<div class="foot"><span>Breakfast served all day · Prices subject to change</span><span>More on the back</span></div>')
    else:
        body = (f'<div style="flex-grow:1;display:flex;padding-top:4px">{grid}</div>' + FINE
                + '<div class="foot"><span>814 Broadway · Marysville, KS 66508 · Join us on Facebook</span><span>Call ahead: (785) 562-3354</span></div>')
    return HEAD.format(side=side, body=body)


def front():
    return page("front", FRONT, blocks())


def back():
    return page("back", BACK, blocks())


if __name__ == "__main__":
    (OUT / "ToGoFront.dc.html").write_text(front())
    (OUT / "ToGoBack.dc.html").write_text(back())
    print("wrote", OUT / "ToGoFront.dc.html", OUT / "ToGoBack.dc.html")
