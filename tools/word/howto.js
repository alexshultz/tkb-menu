// "How to update the menu" — a two-page guide for diner staff.
// usage (from the repo root): node tools/word/howto.js "word/How to update the menu.docx"
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, LevelFormat, AlignmentType, BorderStyle } = require('docx');
const OUT = process.argv[2];
const FONT = 'Calibri';
const ink = '2A1E18', maroon = '8A2A2B', muted = '5A4636';

const t = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 23, bold: o.bold, italics: o.italic, color: o.color || ink });
const p = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [t(runs)], spacing: { before: o.before || 0, after: o.after ?? 120, line: 276 }, numbering: o.num ? { reference: o.num, level: 0 } : undefined, keepNext: o.keepNext });
const h = (text) => new Paragraph({ children: [t(text, { size: 30, bold: true, color: maroon })], spacing: { before: 280, after: 120 }, keepNext: true, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'D9CCB8', space: 4 } } });
const step = (runs, ref) => p(runs, { num: ref, after: 90 });
const b = (s) => t(s, { bold: true });

const doc = new Document({
  creator: 'TKB Diner', title: 'How to update the TKB Diner menu',
  numbering: { config: ['a', 'b', 'c', 'd', 'e'].map((r) => ({ reference: r, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 320 } } } }] })).concat([{ reference: 'dots', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 320 } } } }] }]) },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1260, right: 1260 } } },
    children: [
      new Paragraph({ children: [t('How to update the TKB Diner menu', { size: 44, bold: true, color: maroon })], spacing: { after: 120 } }),
      p([t('Open ', { color: muted }), b('TKB Diner Menu.docx'), t(' in Microsoft Word. It is the six menu pages in order: the cover, then pages 2 to 6. Everything you type in it can be changed; the pictures for the cover and the strip across the top of each page can be swapped for holidays.', { color: muted })], { after: 200 }),

      h('Change a price or an item'),
      step([t('Click on the price or the words and type over them. The row of dots between a name and its price adjusts by itself, so never type dots or spaces.')], 'a'),
      step([b('To add an item: '), t('click at the start of an item name, select that line and the description line under it, copy (Ctrl+C, or Cmd+C on a Mac), click at the start of the next item and paste (Ctrl+V / Cmd+V). Then type the new name, price and description over the copy.')], 'a'),
      step([b('To remove an item: '), t('select its name line and description line and press Delete.')], 'a'),
      step([b('Keep each page on one sheet. '), t('Word shows the page count at the bottom left of the window; it must say 6 pages. If a page spills onto a new one, remove an item or shorten a description. Do not make the text smaller.')], 'a'),
      step([t('Prices are numbers only, no dollar sign: "11", "4.25", "9 / 12".')], 'a'),

      h('Switch to a holiday look (three pictures)'),
      p('Each holiday has two picture files in the Pictures folder: a cover picture (cover-…png) and a band (band-…png). Swap three pictures:', { after: 120 }),
      step([b('Cover picture. '), t('Right-click the picture on page 1 and choose '), b('Change Picture › From a File'), t(', then pick the cover file, for example cover-christmas.png.')], 'b'),
      step([b('Top band, all pages at once. '), t('Double-click the very top of any page to open the header. Right-click the strip and choose '), b('Change Picture › From a File'), t(', then pick the band file, for example band-christmas.png. Double-click the middle of the page to close the header.')], 'b'),
      step([b('Bottom band on the cover. '), t('Double-click the very bottom of page 1, right-click the strip there and change it to the same band file.')], 'b'),
      p([t('To go back to the everyday menu, do the same with '), b('cover-regular.png'), t(' and '), b('band-regular.png'), t('. Save the holiday version under its own name (File › Save As), for example "TKB Diner Menu – Christmas.docx", so the regular file stays as it is.')], { before: 80 }),

      h('New holidays or special events'),
      p('Any new picture drops into the same spot at the same size if it is made to these sizes:', { after: 90 }),
      step([b('Cover picture: '), t('620 × 575 pixels (or 1240 × 1150 for sharper printing), PNG with a transparent background, the art centered. Keep the same idea: the two squirrels over a drink, dressed for the occasion. Do not add words like "Happy Easter"; the picture says it.')], 'dots'),
      step([b('Band: '), t('756 × 34 pixels (or 3024 × 136), PNG with a transparent background, small shapes in a row, centered top to bottom. Pale or white shapes need a darker outline or they disappear on the cream page.')], 'dots'),
      p('The full design rules are in the TKB Diner menu style guide.', { before: 80 }),

      h('Printing'),
      step([t('Print on plain US Letter paper at '), b('Actual size'), t(' (or 100%). Turn off "Fit to page".')], 'c'),
      step([t('The cream color is part of the page and prints by itself. Your printer cannot print the outer quarter inch, so a thin white edge around each page is normal.')], 'c'),
      step([t('Print one test sheet before printing a full batch.')], 'c'),

      h('Fonts'),
      step([t('The menu uses two fonts, Zilla Slab and Libre Franklin. They are saved inside the file, so the menu looks right on any computer with Word.')], 'd'),
      step([t('Keep that setting on when you save: on Windows, '), b('File › Options › Save › Embed fonts in the file'), t('; on a Mac, '), b('Word › Preferences › Save › Embed fonts'), t('.')], 'd'),
      step([t('If the menu ever shows a plain font like Times or Arial, install both fonts for free from fonts.google.com and reopen the file.')], 'd'),

      h('Please don\'t'),
      step([t('Delete or move the cream page background or the bands in the header.')], 'e'),
      step([t('Change the fonts or colors, or stretch the pictures.')], 'e'),
      step([t('Type the occasion on the cover.')], 'e'),
    ],
  }],
});
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log('wrote', OUT); });
