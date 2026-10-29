"""Regenerate base/base_resume.docx.

The look follows rules.md section 7, which is the structure of
example/Nigamananda Behera Resume.docx with one right-hand column and
10 pt bullets. The base holds layout only: page size, margins, fonts,
spacing, and the section headings in their fixed order. tools/render.py
fills a copy of it, so every resume shares exactly the same layout.

Change a constant below and rerun `python tools/make_base.py` to change
the look of every future resume. Earlier outputs are not affected.
"""

from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "base" / "base_resume.docx"

# Section headings in print order. render.py rejects any other heading and
# any other order. Sections with no content are simply left out.
SECTIONS = [
    "Education",
    "Experience",
    "Projects",
    "Skills",
    "Certificates",
]

# Measurements are in twips (1 pt = 20 twips, 1 inch = 1440 twips) and are
# measured from the left margin. Font sizes are in half-points (20 = 10 pt).
PAGE_W, PAGE_H = 11900, 16840          # A4
MARGIN_TOP, MARGIN_BOTTOM = 840, 280
MARGIN_LEFT, MARGIN_RIGHT = 780, 800

FONT = "Times New Roman"
LINK_COLOR = "0000FF"
BODY_SIZE = 20                         # 10 pt
BODY_LINE = 230                        # exact 11.5 pt, same as single spacing
NAME_SIZE = 40                         # 20 pt
CONTACT_SIZE = 18                      # 9 pt
CONTACT_LINE = 292                     # 1.22 lines
HEADING_SIZE = 24                      # 12 pt
HEADING_AFTER = 40

TEXT_INDENT = 113                      # headings, company lines, skill lines
SUB_INDENT = 295                       # education's italic second line only
COLUMN_TAB = 10320                     # right edge; dates and locations end here
BULLET_LEFT, BULLET_HANG = 845, 360    # round bullet, 0.25 in hang
BULLET_RIGHT = 108                     # keep bullet text off the right edge
LINE_GAP = 40                          # 2 pt under a bullet, company, or project line
ENTRY_GAP = 80                         # 4 pt under the last line of a section

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def rpr(size, bold=False, italic=False, caps=False, underline=False, extra=""):
    parts = [f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/>']
    if bold:
        parts.append("<w:b/><w:bCs/>")
    if italic:
        parts.append("<w:i/><w:iCs/>")
    if caps:
        parts.append("<w:caps/>")
    if underline:
        parts.append('<w:u w:val="single" w:color="000000"/>')
    parts.append(extra)
    parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    return "<w:rPr>" + "".join(parts) + "</w:rPr>"


def spacing(line, rule="exact", before=0, after=0):
    return f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="{rule}"/>'


def tab(kind, pos):
    return f'<w:tabs><w:tab w:val="{kind}" w:pos="{pos}"/></w:tabs>'


def ind(left, hanging=0, right=0):
    hang = f' w:hanging="{hanging}"' if hanging else ""
    rhs = f' w:right="{right}"' if right else ""
    return f'<w:ind w:left="{left}"{hang}{rhs}/>'


def style(sid, name, ppr, run, next_style=None, based="Normal"):
    parts = [f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/>']
    if based:
        parts.append(f'<w:basedOn w:val="{based}"/>')
    if next_style:
        parts.append(f'<w:next w:val="{next_style}"/>')
    parts.append(f"<w:qFormat/><w:pPr>{ppr}</w:pPr>{run}</w:style>")
    return "".join(parts)


STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
  <w:docDefaults>
    <w:rPrDefault>{rpr(BODY_SIZE, extra='<w:lang w:val="en-US"/>')}</w:rPrDefault>
    <w:pPrDefault><w:pPr>{spacing(BODY_LINE)}</w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/><w:qFormat/>
    <w:pPr><w:widowControl/>{spacing(BODY_LINE)}{ind(TEXT_INDENT)}<w:jc w:val="both"/></w:pPr>
    {rpr(BODY_SIZE)}
  </w:style>
  {style("Name", "Name", spacing(240, "auto") + ind(0) + '<w:jc w:val="center"/>',
         rpr(NAME_SIZE, bold=True), next_style="Contact")}
  {style("Contact", "Contact", spacing(CONTACT_LINE, "auto") + ind(0) + '<w:jc w:val="center"/>',
         rpr(CONTACT_SIZE))}
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Entry"/><w:uiPriority w:val="9"/><w:qFormat/>
    <w:pPr><w:keepNext/>{tab("left", COLUMN_TAB)}{spacing(240, "auto", 0, HEADING_AFTER)}{ind(TEXT_INDENT)}<w:jc w:val="left"/><w:outlineLvl w:val="0"/></w:pPr>
    {rpr(HEADING_SIZE, bold=True, caps=True, underline=True)}
  </w:style>
  {style("Entry", "Entry", "<w:keepNext/>" + tab("right", COLUMN_TAB) + spacing(BODY_LINE) + ind(TEXT_INDENT) + '<w:jc w:val="both"/>',
         rpr(BODY_SIZE), next_style="EntrySub")}
  {style("EntrySub", "Entry Sub", "<w:keepNext/>" + tab("right", COLUMN_TAB) + spacing(BODY_LINE) + ind(SUB_INDENT) + '<w:jc w:val="both"/>',
         rpr(BODY_SIZE, italic=True), next_style="Bullet")}
  {style("EntryTitle", "Entry Title", "<w:keepNext/>" + tab("right", COLUMN_TAB) + spacing(BODY_LINE) + ind(TEXT_INDENT) + '<w:jc w:val="both"/>',
         rpr(BODY_SIZE, italic=True), next_style="Bullet")}
  {style("Bullet", "Bullet", '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>' + spacing(BODY_LINE, after=LINE_GAP) + ind(BULLET_LEFT, BULLET_HANG, BULLET_RIGHT) + '<w:jc w:val="both"/>',
         rpr(BODY_SIZE))}
  <w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">
    <w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/>
  </w:style>
  <w:style w:type="character" w:styleId="Hyperlink">
    <w:name w:val="Hyperlink"/><w:basedOn w:val="DefaultParagraphFont"/>
    <w:rPr><w:color w:val="{LINK_COLOR}"/><w:u w:val="single"/></w:rPr>
  </w:style>
</w:styles>
"""

NUMBERING = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="{W_NS}">
  <w:abstractNum w:abstractNumId="0">
    <w:multiLevelType w:val="singleLevel"/>
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="bullet"/>
      <w:lvlText w:val="\u2022"/>
      <w:lvlJc w:val="left"/>
      <w:pPr>{ind(BULLET_LEFT, BULLET_HANG, BULLET_RIGHT)}</w:pPr>
      <w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/><w:b w:val="0"/><w:i w:val="0"/><w:sz w:val="{BODY_SIZE}"/><w:szCs w:val="{BODY_SIZE}"/></w:rPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>
"""


def para(style_id, text=""):
    run = f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r><w:r><w:tab/></w:r>' if text else ""
    return f'<w:p><w:pPr><w:pStyle w:val="{style_id}"/></w:pPr>{run}</w:p>'


body = [para("Name"), para("Contact")] + [para("Heading1", h) for h in SECTIONS]

DOCUMENT = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W_NS}" xmlns:r="{R_NS}">
  <w:body>
    {"".join(body)}
    <w:sectPr>
      <w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>
      <w:pgMar w:top="{MARGIN_TOP}" w:right="{MARGIN_RIGHT}" w:bottom="{MARGIN_BOTTOM}" w:left="{MARGIN_LEFT}" w:header="0" w:footer="0" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
"""

# ulTrailSpace makes Word underline the trailing tab that draws the heading rule.
SETTINGS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="{W_NS}">
  <w:defaultTabStop w:val="720"/>
  <w:characterSpacingControl w:val="doNotCompress"/>
  <w:compat>
    <w:ulTrailSpace/>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>
"""

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>
"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", DOCUMENT)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/numbering.xml", NUMBERING)
        z.writestr("word/settings.xml", SETTINGS)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
