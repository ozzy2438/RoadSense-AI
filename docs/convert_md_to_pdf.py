"""Convert azure-ingestion-guide.md to a well-formatted PDF using weasyprint."""

import pathlib
import markdown
import weasyprint

DOCS_DIR = pathlib.Path("/Users/osmanorka/RoadSense-AI/docs")
MD_PATH = DOCS_DIR / "azure-ingestion-guide.md"
PDF_PATH = DOCS_DIR / "azure-ingestion-guide.pdf"

CSS = """
@page {
    margin: 2cm;
    size: A4;
}

* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #1a1a1a;
    background: #ffffff;
    margin: 0;
    padding: 0;
}

/* ── Headings ── */
h1 {
    font-size: 22pt;
    font-weight: 700;
    color: #0d1117;
    border-bottom: 3px solid #0078d4;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 18px;
}

h2 {
    font-size: 16pt;
    font-weight: 700;
    color: #0d1117;
    border-bottom: 1.5px solid #d0d7de;
    padding-bottom: 5px;
    margin-top: 28px;
    margin-bottom: 12px;
}

h3 {
    font-size: 13pt;
    font-weight: 600;
    color: #24292f;
    margin-top: 20px;
    margin-bottom: 8px;
}

h4, h5, h6 {
    font-size: 11pt;
    font-weight: 600;
    color: #24292f;
    margin-top: 14px;
    margin-bottom: 6px;
}

/* ── Paragraphs & lists ── */
p {
    margin: 0 0 10px 0;
}

ul, ol {
    margin: 0 0 10px 0;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
}

/* ── Code — inline ── */
code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 9.5pt;
    background-color: #f0f0f0;
    color: #c7254e;
    padding: 1px 4px;
    border-radius: 3px;
}

/* ── Code — fenced blocks ── */
pre {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-left: 4px solid #0078d4;
    border-radius: 4px;
    padding: 12px 14px;
    margin: 12px 0;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 9pt;
    background-color: transparent;
    color: #1a1a1a;
    padding: 0;
    border-radius: 0;
}

/* ── Tables ── */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

th {
    background-color: #0078d4;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 7px 10px;
    border: 1px solid #0066b8;
}

td {
    padding: 6px 10px;
    border: 1px solid #d0d7de;
    color: #24292f;
}

tr:nth-child(even) td {
    background-color: #f6f8fa;
}

/* ── Blockquotes ── */
blockquote {
    margin: 12px 0;
    padding: 8px 14px;
    border-left: 4px solid #0078d4;
    background-color: #f0f7ff;
    color: #24292f;
    border-radius: 0 4px 4px 0;
}

blockquote p {
    margin: 0;
}

/* ── Horizontal rules ── */
hr {
    border: none;
    border-top: 1px solid #d0d7de;
    margin: 18px 0;
}

/* ── Strong / emphasis ── */
strong {
    font-weight: 700;
    color: #0d1117;
}

em {
    font-style: italic;
}

/* ── Links ── */
a {
    color: #0078d4;
    text-decoration: none;
}
"""

def build_html(md_text: str) -> str:
    """Convert markdown text to a complete HTML document string."""
    md_extensions = [
        "tables",
        "fenced_code",
        "codehilite",
        "nl2br",
        "sane_lists",
    ]
    body_html = markdown.markdown(
        md_text,
        extensions=md_extensions,
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "noclasses": True,
                "pygments_style": "friendly",
            }
        },
    )

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RoadSense AI — Azure Ingestion Rehberi</title>
  <style>
{CSS}
  </style>
</head>
<body>
{body_html}
</body>
</html>
"""


def main() -> None:
    md_text = MD_PATH.read_text(encoding="utf-8")
    html = build_html(md_text)

    pdf_bytes = weasyprint.HTML(string=html, base_url=str(DOCS_DIR)).write_pdf()
    PDF_PATH.write_bytes(pdf_bytes)

    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"PDF created: {PDF_PATH}")
    print(f"File size:   {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
