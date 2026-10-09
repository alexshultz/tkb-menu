// Builds the editable TKB Diner menu (regular) as a Word file.
// usage: node build.js <kit dir> <fonts dir> <out.docx>
const fs = require('fs');
const path = require('path');
const d = require('docx');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, Header, Footer,
  AlignmentType, BorderStyle, ShadingType, WidthType, TabStopType, VerticalAlign,
  HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, TextWrappingType, CharacterSet, PageBreak,
} = d;

const [KIT, FONTS, OUT] = process.argv.slice(2);
const img = (f) => fs.readFileSync(path.join(KIT, f));

// ---- tokens (from the style guide) ----
const C = {
  paper: 'FBF6EC', tint: 'F1E4D0', ink: '2A1E18', inkSoft: '4E3D31', inkMuted: '5A4636',
  maroon: '8A2A2B', teal: '2E6A68', leader: 'B9A68F', rule: 'D9CCB8',
  onDark: 'FBF6EC', onDarkSoft: 'E9DFCF', onDarkPrice: 'F2C9A0', onMaroonLabel: 'F2D9C0', onDarkLabel: '9FD3CF',
};
const F = {
  slab: 'Zilla Slab Bold', slabSemi: 'Zilla Slab SemiBold',
  body: 'Libre Franklin', italic: 'Libre Franklin Italic', medium: 'Libre Franklin Medium', semi: 'Libre Franklin SemiBold',
};
const px = (n) => Math.round(n * 15);        // CSS px -> twips (DXA)
const emu = (n) => Math.round(n * 9525);     // CSS px -> EMU
const PAGE_W = 12240, PAGE_H = 15840;
const MARGIN_X = px(56);                     // 840
const TEXT_W = PAGE_W - 2 * MARGIN_X;        // 10560
const GAP = px(44);                          // 660
const COL_W = Math.floor((TEXT_W - GAP) / 2); // 4950
const ITEM_GAP = 250;                        // ~13px after an item

// ---- text helpers ----
const run = (text, o = {}) => new TextRun({ text, font: o.font || F.body, size: o.size || 20, color: o.color || C.ink, allCaps: o.caps, characterSpacing: o.spacing, bold: false });
const leaderTab = (color = C.leader) => new TextRun({ text: '\t', color, font: F.body, size: 20 });

function P(children, o = {}) {
  return new Paragraph({
    children, alignment: o.align, keepNext: o.keepNext, keepLines: true,
    spacing: { before: o.before || 0, after: o.after || 0, line: o.line || 240, lineRule: o.lineRule || 'auto' },
    tabStops: o.tab ? [{ type: TabStopType.RIGHT, position: o.tab, leader: o.leader || 'dot' }] : undefined,
    border: o.border, indent: o.indent, pageBreakBefore: o.pageBreakBefore,
  });
}
const kicker = (newPage = true) => P([run('TKB Diner', { font: F.semi, size: 18, color: C.teal, caps: true, spacing: 43 })], { after: 120, pageBreakBefore: newPage });
const title = (t) => P([run(t, { font: F.slab, size: 81, color: C.maroon })], { after: 360 });
const heading = (t, o = {}) => P([run(t, { font: F.slab, size: 34, color: C.ink })], {
  before: o.first ? 0 : 260, after: 130, keepNext: true,
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: C.ink, space: 3 } },
});
const note = (t, o = {}) => P([run(t, { font: F.italic, size: 20, color: C.inkMuted })], { after: o.after ?? 150, keepNext: true });
const label = (t, color = C.teal) => P([run(t, { font: F.semi, size: 18, color, caps: true, spacing: 36 })], { after: 90, keepNext: true });
const desc = (t, o = {}) => P([run(t, { size: 20, color: o.color || C.inkSoft })], { after: o.after ?? ITEM_GAP });

// One priced line: name ........ price  (+ optional description)
function item(name, price, description, o = {}) {
  const tab = o.tab || COL_W - 20;
  const size = o.size || 27;
  const children = [run(name, { font: o.list ? F.medium : F.slabSemi, size: o.list ? 22 : size, color: o.nameColor || C.ink })];
  if (price !== undefined && price !== null) {
    children.push(leaderTab(o.leaderColor));
    children.push(run(price, { font: F.slab, size: o.list ? 22 : size, color: o.priceColor || C.maroon }));
  }
  const gap = o.list ? 90 : ITEM_GAP;
  const out = [P(children, { tab, after: description ? 20 : gap, keepNext: !!description })];
  if (description) out.push(desc(description, { color: o.descColor, after: gap }));
  return out;
}
const spacer = (twips = 120) => P([run('', { size: 2 })], { after: 0, line: Math.max(twips, 20), lineRule: 'exact' });

// ---- table helpers ----
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE };
function cell(children, width, o = {}) {
  return new TableCell({
    children: children.length ? children : [P([run('')])], width: { size: width, type: WidthType.DXA },
    margins: o.margins || { top: 0, bottom: 0, left: 0, right: 0 },
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    borders: o.borders || { top: NONE, bottom: NONE, left: NONE, right: NONE },
    verticalAlign: o.valign || VerticalAlign.TOP,
  });
}
// Two menu columns side by side
function columns(left, right) {
  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: [COL_W, GAP, COL_W], borders: noBorders,
    rows: [new TableRow({ cantSplit: true, children: [cell(left, COL_W), cell([], GAP), cell(right, COL_W)] })],
  });
}
// Items running two-up across the page
function grid(items) {
  const rows = [];
  for (let i = 0; i < items.length; i += 2) {
    rows.push(new TableRow({ cantSplit: true, children: [cell(items[i], COL_W), cell([], GAP), cell(items[i + 1] || [], COL_W)] }));
  }
  return new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: [COL_W, GAP, COL_W], borders: noBorders, rows });
}
// A single boxed cell: tinted group, teal outline, or solid feature
function box(children, width, kind) {
  const pad = kind === 'feature' ? { top: px(14), bottom: px(10), left: px(20), right: px(20) } : { top: px(11), bottom: px(4), left: px(14), right: px(14) };
  const line = { style: BorderStyle.SINGLE, size: 16, color: C.teal };
  const o = { margins: pad };
  if (kind === 'tint') o.fill = C.tint;
  if (kind === 'outline') o.borders = { top: line, bottom: line, left: line, right: line };
  if (kind === 'ink') o.fill = C.ink;
  if (kind === 'maroon') o.fill = C.maroon;
  return new Table({ width: { size: width, type: WidthType.DXA }, columnWidths: [width], borders: noBorders, rows: [new TableRow({ cantSplit: true, children: [cell(children, width, o)] })] });
}
const innerTab = (width, kind) => width - (kind === 'feature' ? px(40) : px(28)) - 20;

function highlight(lbl, line, items, width = COL_W) {
  const tab = innerTab(width);
  return box([
    label(lbl, C.maroon),
    P([run(line, { font: F.italic, size: 20, color: C.inkSoft })], { after: 120, keepNext: true }),
    ...items.flatMap(([n, p]) => item(n, p, null, { tab, size: 27 })),
  ], width, 'tint');
}
function feature(kind, o, width = COL_W) {
  const tab = innerTab(width, 'feature');
  const ink = kind === 'ink';
  const kids = [];
  if (o.label) kids.push(P([run(o.label, { font: F.semi, size: 17, color: ink ? C.onDarkLabel : C.onMaroonLabel, caps: true, spacing: 37 })], { after: 80 }));
  if (o.headline) kids.push(P([run(o.headline, { font: F.slab, size: 33, color: C.onDark })], { after: 90 }));
  if (o.name) kids.push(...item(o.name, o.price, null, { tab, size: o.size || 33, nameColor: C.onDark, priceColor: ink ? C.onDarkPrice : C.onDark, leaderColor: ink ? '8C7A66' : 'C98A7E' }).map((p) => p));
  if (o.desc) kids.push(desc(o.desc, { color: ink ? C.onDarkSoft : C.onMaroonLabel, after: 100 }));
  return box(kids, width, kind === 'ink' ? 'ink' : 'maroon');
}
const fullDivider = (children) => P(children, { before: 120, border: { top: { style: BorderStyle.DOTTED, size: 12, color: C.leader, space: 8 } } });

// ---- floating pictures (the drop-in areas) ----
function floatingPicture(file, x, y, w, h, o = {}) {
  return new ImageRun({
    type: 'png', data: img(file), transformation: { width: w, height: h },
    altText: { name: o.name || file, title: o.name || file, description: o.description || '' },
    floating: {
      horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: emu(x) },
      verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: emu(y) },
      allowOverlap: true, lockAnchor: true, behindDocument: !!o.behind,
      wrap: { type: TextWrappingType.NONE }, zIndex: o.z || 1,
    },
  });
}
const BAND = { x: 30, w: 756, h: 34, top: 24 };
const paperBackground = () => floatingPicture('paper.png', 0, 0, 816, 1056, { behind: true, z: 0, name: 'Page background', description: 'Cream page colour. Leave as is.' });
const bandPicture = (y, nm) => floatingPicture('band-regular.png', BAND.x, y, BAND.w, BAND.h, { name: nm, description: 'Drop-in band. Right-click > Change Picture to swap in a holiday band (756 x 34 px).' });

// ---- the cover ----
const coverChildren = [
  P([new ImageRun({ type: 'png', data: img('cover-regular.png'), transformation: { width: 620, height: 575 }, altText: { name: 'Cover picture', title: 'Cover picture', description: 'Drop-in cover picture. Right-click > Change Picture to swap in holiday art (620 x 575 px).' } })], { align: AlignmentType.CENTER, after: 0, line: 240 }),
  P([run('TKB Diner', { font: F.slab, size: 132, color: C.maroon })], { align: AlignmentType.CENTER, before: 300, after: 120, line: 240 }),
  P([run('Breakfast · Lunch · Dinner', { font: F.semi, size: 21, color: C.teal, caps: true, spacing: 55 })], { align: AlignmentType.CENTER, after: 0 }),
  P([run('814 Broadway · Marysville, KS 66508', { size: 25, color: C.inkMuted })], { align: AlignmentType.CENTER, before: 760, after: 40 }),
  P([run('(785) 562-3354', { font: F.slab, size: 36, color: C.ink })], { align: AlignmentType.CENTER, after: 40 }),
  P([run('Join us on Facebook', { size: 25, color: C.inkMuted })], { align: AlignmentType.CENTER }),
];

// ---- inside pages ----
const brk = () => new Paragraph({ children: [new PageBreak()] });
const FULL_TAB = TEXT_W - 20;
const listItem = (n, p) => item(n, p, null, { list: true });

const page2 = [
  kicker(false), title('Classic Breakfast'),
  columns([
    heading('Favorites', { first: true }),
    ...item('Biscuits & Gravy', '4 / 7', 'Biscuits and homemade sausage gravy'),
    ...item('Breakfast Sandwich', '8', 'Choice of ham, bacon or sausage, cheese and one egg'),
    ...item('Breakfast Burrito', '9', 'Choice of meat, cheddar and two eggs'),
    ...item('Western Burrito', '11', 'Ham, cheddar, potatoes, onions, peppers and two eggs'),
    ...item('Breakfast Bowl', '10', 'Hashbrowns, ham, bacon, sausage, cheese, veggies and two eggs'),
    ...item('Stacked Hashbrowns', '11', 'Ham, bacon, sausage, cheese, veggies and two eggs'),
    heading('From the Griddle'),
    ...item('French Toast', 'half 5 · full 10', 'Dusted with powdered sugar, side of syrup · add blueberries +1'),
    ...item('Pancakes', '1 for 2 · 3 for 5 · 6 for 8', 'Single, short stack or full stack'),
    ...item('Oatmeal', '6', 'Served with brown sugar, craisins and pecans'),
  ], [
    heading('3-Egg Omelettes', { first: true }), note('Served with your choice of toast'),
    ...item('Denver', '12', 'Ham, cheddar, onions and peppers'),
    ...item('Garden', '11', 'All the veggies and cheese'),
    ...item('Meat & Cheese', '12', 'Ham, bacon and sausage'),
    heading('Breakfast Plates'),
    ...item('One Eyed Jack', '5', 'One egg and toast'),
    ...item('Hobo', '6', 'Two eggs and toast'),
    ...item("Bird's Nest", '9', 'One egg, choice of meat and toast'),
    ...item('Bullseye', '10', 'Two eggs, choice of meat and toast'),
    heading('Sides & Extras'),
    ...[['Hashbrowns', '3'], ['Toast', '3'], ['Sausage gravy', '3'], ['Biscuit', '2'], ['Ham, bacon or sausage', '4'], ['Egg', '2'], ['Cheese', '2'], ['Onion, pepper, jalapeño', '1']].flatMap(([n, p]) => listItem(n, p)),
  ]),
];

const apps = [['Corn Nuggets', '8'], ['Onion Rings', '9'], ['Pickle Chips', '8'], ['Mozzarella Sticks', '9'], ['Cheeseballs', '9'], ['Jalapeño Bites', '9'], ['Spinach Artichoke Dip', '9'], ['Broccoli & Cheese Bites', '9'], ['Mac & Cheese Wedges', '9'], ['French Fries', '7'], ['Sweet Potato Fries', '8']];
const page3 = [
  kicker(), title('Appetizers & Sandwiches'),
  heading('Appetizers', { first: true }),
  box(item('Sampler — pick any 3', '13', null, { tab: TEXT_W - px(32) - 20 }), TEXT_W, 'outline'),
  spacer(160),
  grid(apps.map(([n, p]) => item(n, p, null, { size: 27 }).map((x) => x))),
  heading('Sandwiches'), note('Served with fries · substitute any side +2'),
  columns([
    label('Deli Classics'),
    ...item('BLT', '9 / 11', 'Wheat, bacon, lettuce, tomato, mayo'),
    ...item('Reuben', '10 / 12', 'Rye, corned beef, 1000 Island, sauerkraut, Swiss'),
    ...item('Rachel', '10 / 12', 'Rye, turkey, 1000 Island, sauerkraut, Swiss'),
    ...item('Club', '10 / 12', 'Sourdough, turkey, bacon, tomato, ranch, Colby jack'),
  ], [
    label('Hot Sandwiches · 13'),
    desc('On a bun with mayo; lettuce, tomato and onion on the side', { after: 120 }),
    highlight('Hand-Breaded to Order', 'Breaded by hand in our kitchen and fried crisp and golden the moment you order.', [['Pork Tender', '13'], ['Chicken Fried Chicken', '13'], ['Country Fried Steak', '13']]),
    spacer(140),
    ...item('Grilled Chicken', '13'),
    ...item('Philly', '13', 'Hoagie bun, peppers, onions, Swiss'),
  ]),
];

const burgers = [
  ['Plain Jane', '12', 'Just the burger patty'], ['Patty Melt', '13', 'Rye, 1000 Island, Swiss'],
  ['The Whiskey', '14', 'Swiss, cheddar, bacon, onion tanglers, whiskey sauce'], ['The Sunrise', '14', 'Cheddar, bacon, fried egg'],
  ['The Firehouse', '14', 'Pepper jack, bacon, jalapeño, sriracha mayo'], ['The Midwest', '14', 'Colby jack, onion ring, BBQ sauce'],
  ['TKB Melt', '14', 'Swiss, grilled peppers, onions and mushrooms, garlic aioli'], ['The Club', '14', 'Colby jack, turkey, bacon, tomato, ranch'],
  ['The Carter', '14', 'Cheddar & Swiss, onion tanglers, bacon, fried egg, ranch'], ['The Reuben Burger', '14', 'Swiss, corned beef, sauerkraut, 1000 Island'],
];
const chip = (t, p) => [run(t + ' ', { font: F.medium, size: 20, color: C.ink }), run(p, { font: F.semi, size: 20, color: C.maroon }), run('     ', { size: 20 })];
const page4 = [
  kicker(), title('Burgers & Baskets'),
  heading('Burgers', { first: true }), note('Served with fries · substitute any side +2', { after: 100 }),
  P([run('Add   ', { font: F.semi, size: 18, color: C.teal, caps: true, spacing: 36 }), ...chip('Cheese', '+1'), ...chip('Peppers or jalapeños', '+1'), ...chip('Bacon', '+2'), ...chip('Extra patty', '+3')], { after: 160 }),
  feature('ink', { name: 'The Black Squirrel', price: '14', desc: 'Bacon jam, muenster & gouda, Nutella', size: 33 }, TEXT_W),
  spacer(160),
  grid(burgers.map(([n, p, ds]) => item(n, p, ds))),
  heading('Baskets & Wraps'),
  grid([
    item('Fish & Chips', '14', '8 oz walleye strips and fries'),
    [P([run('Chicken Strips', { font: F.slabSemi, size: 27 }), leaderTab(), run('14', { font: F.slab, size: 27, color: C.maroon })], { tab: COL_W - 20, after: 20, keepNext: true }),
      P([run('Hand-breaded to order', { font: F.semi, size: 20, color: C.maroon }), run(' · 4 chicken strips and fries', { size: 20, color: C.inkSoft })], { after: ITEM_GAP })],
    item('Shrimp', '15', '8 butterfly shrimp and fries'),
    item('CBR Wrap', '12', 'Crispy or grilled chicken, bacon, ranch, cheese, lettuce, tomato'),
  ]),
  fullDivider([run('Swap your fries (+2): ', { font: F.semi, size: 20, color: C.ink }), run('veggie of the day, baked potato, loaded baked potato, sweet potato fries, mashed potatoes & gravy, side salad, seasonal salad, cup of soup or an appetizer', { size: 20, color: C.inkSoft })]),
];

const page5 = [
  kicker(), title('Entrees, Soup & Salads'),
  columns([
    heading('Entrees', { first: true }), note('Served with your choice of two sides and a dinner roll'),
    ...item('Steak Bites', '½ lb 18 · 1 lb 23'),
    highlight('Hand-Breaded to Order', 'Never pre-breaded: each one is breaded by hand and fried golden when you order.', [['Chicken Fried Chicken', '18'], ['Country Fried Steak', '19'], ['Pork Tender', '17']]),
    spacer(160),
    ...item('Hamburger Steak', '17', 'Sautéed mushrooms and onions optional'),
    ...item('Grilled Chicken', '17'),
    ...item('12 oz KC Strip', '26'),
    feature('maroon', { label: 'Last Friday & Saturday of the month', name: 'Prime Rib', price: '26', desc: 'With two sides and a dinner roll', size: 39 }),
  ], [
    heading('Homemade Soup', { first: true }), note("Seasonal — today's soups are posted on the specials board"),
    ...item('Cup', '4'), ...item('Bowl', '6'),
    heading('Salads'),
    ...item('Chef', '9 / 12', 'Ham, turkey, tomatoes, cheddar, hard-boiled egg'),
    ...item('Greek', '9 / 12', 'Spinach, chicken, olives'),
    ...item('Grilled Chicken', '9 / 12', 'Grilled chicken breast'),
    box([label('Dressings'), desc('Homemade ranch · Blue cheese · Raspberry vinaigrette · Dorothy Lynch · Italian · Thousand Island · Honey mustard', { after: 100 })], COL_W, 'outline'),
    heading('Sides'), note('Choose two with any entree', { after: 100 }),
    ...['Fries', 'Veggie of the day', 'Baked potato', 'Mashed potatoes & gravy', 'Mac & cheese', 'Side salad', 'Cup of soup'].flatMap((n) => listItem(n, null)),
    ...[['Sweet potato fries', '+2'], ['An appetizer', '+2'], ['Loaded baked potato', '+3']].flatMap(([n, p]) => listItem(n, p)),
  ]),
];

const beerCell = (t, w, o = {}) => cell([P([run(t, { font: o.head ? F.semi : F.slab, size: o.head ? 18 : 24, color: o.head ? C.inkMuted : (o.first ? C.ink : C.maroon), caps: o.head, spacing: o.head ? 22 : undefined })], { align: o.first ? AlignmentType.LEFT : AlignmentType.RIGHT, before: o.head ? 0 : 90, after: o.head ? 90 : 90 })], w, { borders: { top: NONE, left: NONE, right: NONE, bottom: { style: BorderStyle.SINGLE, size: o.head ? 12 : 6, color: o.head ? C.ink : C.rule } } });
const BW = [COL_W - 2400, 1200, 1200];
const beerRow = (cells, head) => new TableRow({ cantSplit: true, children: cells.map((t, i) => beerCell(t, BW[i], { head, first: i === 0 })) });
const beerTable = new Table({
  width: { size: COL_W, type: WidthType.DXA }, columnWidths: BW, borders: noBorders,
  rows: [beerRow(['Beer', 'Can', 'Bottle'], true), beerRow(['Domestic', '3.00', '3.50']), beerRow(['Import', '3.75', '4.00']), beerRow(['Domestic bucket of 6', '15.00', '17.50']),
    new TableRow({ cantSplit: true, children: [beerCell('Import bucket', BW[0], { first: true }), new TableCell({ columnSpan: 2, width: { size: 2400, type: WidthType.DXA }, margins: { top: 0, bottom: 0, left: 0, right: 0 }, borders: { top: NONE, left: NONE, right: NONE, bottom: { style: BorderStyle.SINGLE, size: 6, color: C.rule } }, children: [P([run('21.00', { font: F.slab, size: 24, color: C.maroon })], { align: AlignmentType.RIGHT, before: 90, after: 90 })] })] })],
});
const lead = (a, b) => P([run(a, { font: F.semi, size: 20, color: C.ink }), run(b, { size: 20, color: C.inkSoft })], { after: 110 });
const page6 = [
  kicker(), title('Kids, Drinks & Desserts'),
  columns([
    heading("Kids' Meals", { first: true }), note('With fries, mac & cheese or mashed potatoes'),
    ...item('Chicken Strips (2)', '8'), ...item('Hamburger', '9'), ...item('Grilled Cheese', '7'), ...item('PB&J', '7'),
    heading('Desserts'), note("Ask about today's homemade desserts"),
    ...item('Pie', '4.25'), ...item('Cheesecake', '4.75'),
    spacer(120),
    feature('ink', { label: 'We cater', headline: 'Hosting an event, a wedding or a business meeting?', desc: 'Ask for our catering menu and pricing.' }),
  ], [
    heading('Drinks', { first: true }),
    ...item('Fountain soda', '3', '24 oz with unlimited refills · Pepsi, Diet Pepsi, Mountain Dew, Dr Pepper, Sierra Mist', {}),
    desc('Also: iced tea, hot tea, coffee, milk, orange juice, water', { after: 110 }),
    note('Specialty drinks — ask for our drink menu', { after: 60 }),
    heading('Beer'),
    beerTable,
    spacer(140),
    lead('Domestic: ', 'Miller Lite, Bud, Bud Light, Busch Light, Michelob Ultra, Coors, Coors Light, Yuengling Lager'),
    lead('Import: ', 'Corona, Heineken, Modelo'),
    P([run('Make any beer a red beer ', { size: 20, color: C.inkSoft }), run('+0.25', { font: F.semi, size: 20, color: C.maroon })], { after: 140 }),
    ...item("Mike's Hard Lemonade, Smirnoff", '4.00', null, { size: 24 }),
  ]),
  P([run('', { size: 2 })], { before: 900 }),
  P([run('Allergies & gluten-free: ', { font: F.semi, size: 18, color: C.ink }), run('Many items are or can be made gluten-free. Please tell your server about any allergies and we will accommodate as best we can. Ours is an open-air kitchen, so cross-contact is always a risk.', { size: 18, color: C.inkSoft })],
    { after: 100, line: 270, border: { top: { style: BorderStyle.DOTTED, size: 12, color: C.leader, space: 8 } } }),
  P([run('Consumer advisory: ', { font: F.semi, size: 18, color: C.ink }), run('Eggs on our menu can be ordered raw or undercooked. Consuming raw or undercooked meats, poultry, seafood, shellfish or eggs may increase your risk of foodborne illness. For more information, see the Kansas Department of Agriculture website.', { size: 18, color: C.inkSoft })], { line: 270 }),
];

// ---- header & footers ----
const sharedHeader = new Header({ children: [new Paragraph({ children: [paperBackground(), bandPicture(BAND.top, 'Top band')] })] });
const coverFooter = new Footer({ children: [new Paragraph({ children: [bandPicture(1056 - BAND.top - BAND.h, 'Bottom band')] })] });
const pageFooter = new Footer({ children: [P([run('814 Broadway · Marysville, KS', { font: F.medium, size: 18, color: C.inkMuted }), new TextRun({ text: '\t', size: 18 }), run('(785) 562-3354', { font: F.medium, size: 18, color: C.inkMuted })],
  { tab: TEXT_W, leader: 'none', border: { top: { style: BorderStyle.SINGLE, size: 12, color: C.ink, space: 6 } } })] });

const fontFile = (n) => fs.readFileSync(path.join(FONTS, n.replace(/ /g, '-') + '.ttf'));
const doc = new Document({
  creator: 'TKB Diner', title: 'TKB Diner Menu', description: 'Editable regular menu. Six letter pages: cover plus five inside pages.',
  fonts: Object.values(F).map((name) => ({ name, data: fontFile(name), characterSet: CharacterSet.ANSI })),
  styles: { default: { document: { run: { font: F.body, size: 20, color: C.ink } } } },
  sections: [
    {
      properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: px(70), bottom: px(64), left: MARGIN_X, right: MARGIN_X, header: px(24), footer: px(24) } } },
      headers: { default: sharedHeader }, footers: { default: coverFooter }, children: coverChildren,
    },
    {
      properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: px(72), bottom: px(74), left: MARGIN_X, right: MARGIN_X, header: px(24), footer: px(32) } } },
      footers: { default: pageFooter },
      children: [...page2, ...page3, ...page4, ...page5, ...page6],
    },
  ],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(OUT, b); console.log('wrote', OUT, b.length); });
