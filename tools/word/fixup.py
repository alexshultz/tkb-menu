"""Post-process the docx-js output so Word opens it cleanly.

- font keys in fontTable.xml upper-cased (the schema requires [0-9A-F])
- every drawing gets a unique wp:docPr id
- settings.xml asks Word to keep fonts embedded when the file is re-saved

usage: python3 fixup.py in.docx out.docx
"""
import re, sys, zipfile

src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
counter = [0]

def renumber(xml):
    def sub(m):
        counter[0] += 1
        return f'<wp:docPr id="{counter[0]}"'
    return re.sub(r'<wp:docPr id="\d+"', sub, xml)

with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        name = info.filename
        if name == 'word/fontTable.xml':
            data = re.sub(rb'w:fontKey="(\{[0-9a-fA-F-]+\})"', lambda m: b'w:fontKey="' + m.group(1).upper() + b'"', data)
        elif name == 'word/settings.xml':
            xml = data.decode('utf-8')
            if '<w:embedTrueTypeFonts' not in xml:
                if '<w:displayBackgroundShape/>' in xml:
                    xml = xml.replace('<w:displayBackgroundShape/>', '<w:displayBackgroundShape/><w:embedTrueTypeFonts/>', 1)
                else:
                    xml = re.sub(r'(<w:settings[^>]*>)', r'\1<w:embedTrueTypeFonts/>', xml, count=1)
            data = xml.encode('utf-8')
        elif re.match(r'word/(document|header\d+|footer\d+)\.xml$', name):
            data = renumber(data.decode('utf-8')).encode('utf-8')
        zout.writestr(info, data)
print('drawings renumbered:', counter[0])
