# Seasonal graphics

Ready-to-swap banners and cover art, made at the template sizes in `graphics/templates/`. Each season's Word files and PDFs are in `word/proposed/<season>/` and `print/proposed/<season>/`.

To make a season's files without Word:

    python3 tools/word/swap-graphics.py "word/proposed/TKB Diner Menu - proposed.docx" out.docx --banner <banner.png> --cover <cover.png>

then convert `out.docx` to PDF (LibreOffice: `soffice --headless --convert-to pdf out.docx`). In Word, Change Picture does the same thing.

| Season | Source |
| --- | --- |
| Thanksgiving | Banner pattern from `assets/seasonal/bands/band-thanksgiving.svg`, redrawn 16 px tall on white; cover art from `assets/seasonal/art/tkb-thanksgiving-logo-print.png`, centered on a transparent frame of the cover's shape |
