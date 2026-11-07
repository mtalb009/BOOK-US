"""List visible strings of the page that have no FR or IT entry in SW_TRANSLATIONS.

Usage: python3 tools/missing-translations.py html/saywho-book-us.html
Needs node (evaluates the translation maps from the page script).
"""
import json
import re
import subprocess
import sys
from html.parser import HTMLParser

SKIP_TAGS = ("style", "script", "svg")


class Texts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.out = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        skip = tag in SKIP_TAGS or "sw-copyright" in (a.get("class") or "") \
            or (tag == "option" and a.get("value"))
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source", "use", "path", "circle", "rect"):
            self.stack.append(skip)
        if not any(self.stack) and a.get("placeholder"):
            self.out.append(a["placeholder"].strip())

    def handle_endtag(self, tag):
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source", "use", "path", "circle", "rect") and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if not any(self.stack) and data.strip():
            self.out.append(data.strip())


html = open(sys.argv[1], encoding="utf-8").read()
html_noimg = re.sub(r"data:[a-z/+]+;base64,[A-Za-z0-9+/=]+", "", html)
p = Texts()
p.feed(html_noimg.split("<script", 1)[0] if False else html_noimg)
visible = list(dict.fromkeys(s for s in p.out if re.search(r"[A-Za-z]", s)))

scripts = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S))
start = scripts.index("const SW_TRANSLATIONS=")
end = scripts.index("\n", start)
js = scripts[start:end] + "\n"
js += "\n".join(re.findall(r"^Object\.assign\(SW_TRANSLATIONS\.(?:fr|it),\s*\{.*?\}\);", scripts, re.S | re.M))
js += "\nprocess.stdout.write(JSON.stringify(SW_TRANSLATIONS));"
maps = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)

for lang in ("fr", "it"):
    missing = [s for s in visible if s not in maps[lang]]
    print(f"=== missing {lang}: {len(missing)}")
    for s in missing:
        print("-", s[:160])
