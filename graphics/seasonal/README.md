# Seasonal graphics

Ready-to-swap banners and cover art, made at the template sizes in `graphics/templates/`. Each season's Word files and PDFs are in `word/proposed/<season>/` and `print/proposed/<season>/`.

To make a season's files without Word:

    python3 tools/word/swap-graphics.py "word/proposed/TKB Diner Menu - proposed.docx" out.docx --banner <banner.png> --cover <cover.png>

then convert `out.docx` to PDF (LibreOffice: `soffice --headless --convert-to pdf out.docx`). In Word, Change Picture does the same thing.

| Season | Source |
| --- | --- |
| Thanksgiving | Cover art only: `cover-art-thanksgiving-black-1479x1191.png`, from Alex's edited `tkb_squirrels_thanksgiving.psd` (Nov 2026), centered on a transparent frame of the cover's shape. Seasonal editions keep the regular checkerboard banner; only the cover art changes. |
