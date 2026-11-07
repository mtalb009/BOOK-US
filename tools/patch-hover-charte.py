"""One-shot patch of html/saywho-book-us.html: header font, no preselection,
media partners on the brand charter, hover states for every interactive element.

Usage: python3 tools/patch-hover-charte.py
"""
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "html" / "saywho-book-us.html"
html = path.read_text(encoding="utf-8")


def sub(old, new, count=1):
    global html
    if old not in html:
        raise SystemExit(f"not found: {old[:80]}")
    html = html.replace(old, new, count)


# 1. Header font = Helvetica Neue Condensed Bold (Figma), no Arial Narrow first.
FONT_FACE = (
    '@font-face{font-family:"SW Condensed";font-weight:700;'
    'src:local("HelveticaNeue-CondensedBold"),local("Helvetica Neue Condensed Bold")}\n'
    '@font-face{font-family:"SW Condensed";font-weight:900;'
    'src:local("HelveticaNeue-CondensedBlack"),local("Helvetica Neue Condensed Black")}\n'
)
sub("<style>", "<style>\n" + FONT_FACE)
sub('--font-cond:"Arial Narrow","Helvetica Neue Condensed Bold","Helvetica Neue"',
    '--font-cond:"SW Condensed","Helvetica Neue"')
sub("font-weight:700;font-size:20px;letter-spacing:-.005em;white-space:nowrap",
    "font-weight:700;font-stretch:condensed;font-size:20px;letter-spacing:.005em;white-space:nowrap")

# 2. Nothing preselected.
sub('value="Photo coverage" checked>', 'value="Photo coverage">')

# 3. Media partners: same tile vocabulary as the choice lists (no grey box).
sub('<div class="tiny">SELECT YOUR MEDIA PARTNERS — MULTIPLE CHOICES POSSIBLE</div>',
    '<p class="mp-title"><span data-translate="Select your media partners">Select your media partners</span>'
    ' <span class="muted" data-translate="Multiple choices possible">Multiple choices possible</span></p>')
sub(".media-partner-choices{margin-top:16px;padding:16px;border-radius:6px;background:var(--soft)}",
    ".media-partner-choices{margin-top:16px;padding:0;width:100%}"
    ".mp-title{margin:0;font-size:15px;line-height:1.2;font-weight:500;color:#000}"
    ".mp-title .muted{display:block;margin-top:3px;font-weight:400}")
sub(".media-partner-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 16px;margin-top:14px}",
    ".media-partner-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}"
    ".media-partner-grid .check-line{min-height:48px;padding:0 16px;border:1px solid var(--line);border-radius:6px;background:#fff}"
    ".media-partner-grid .check-line:has(input:checked){border-color:#000;box-shadow:inset 0 0 0 1px #000;background:var(--sel)}")

# 4. Hover states (appended last so they win).
HOVER = """
/* ---------- Hover states ---------- */
a,button,.btn,.option,.choice-row,.check-line .cb,.field input,.field select,.field textarea,.control,.upsell,.media-partner-grid .check-line,.sw-detail-close,.sw-brand,.sw-footer-brand{transition:background-color .15s,border-color .15s,color .15s,opacity .15s,box-shadow .15s}
.choice-row:hover{background:var(--soft)}
.choice-row:has(input:checked):hover{background:#DCEEFF}
.choice-row:hover .cb,.check-line:hover .cb{border-color:#000;box-shadow:0 0 0 1px #000}
.check-line:hover>span:last-child{text-decoration:underline;text-underline-offset:3px}
.upsell:hover{border-color:#000}
.media-partner-grid .check-line:hover{border-color:#000;background:var(--soft)}
.media-partner-grid .check-line:has(input:checked):hover{background:#DCEEFF}
.media-partner-grid .check-line:hover>span:last-child{text-decoration:none}
.option.selected:hover{background:#DCEEFF}
.field input:hover,.field select:hover,.field textarea:hover,.control:hover{border-color:#000}
a.btn:hover{background:#333;border-color:#333;color:#fff}
.info-btn:hover{color:#000;transform:scale(1.08)}
.sw-detail-close:hover{background:var(--soft);border-radius:50%}
.sw-brand:hover,.sw-footer-brand:hover{opacity:.7}
.sw-header .nav-search:hover{opacity:.6}
.sw-footer-links a:hover,.sw-social a:hover{text-decoration:none;opacity:.7}
.sw-newsletter button:hover{background:#E8E8E8}
.sw-newsletter input[type=email]:hover{border-color:#fff}
"""
sub("</style>", HOVER + "</style>")

path.write_text(html, encoding="utf-8")
print("patched", path)
