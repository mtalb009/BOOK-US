"""List wording differences (HTML text nodes + JS string literals) between two pages.

Usage: python3 tools/diff-wording.py <reference.html> <current.html>
"""
import re
import sys
from html.parser import HTMLParser


class Texts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script", "svg"):
            self.skip += 1
        for k, v in attrs:
            if k in ("placeholder", "aria-label", "title") and v and v.strip():
                self.out.append(v.strip())

    def handle_endtag(self, tag):
        if tag in ("style", "script", "svg"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.out.append(" ".join(data.split()))


def strings(path):
    html = open(path, encoding="utf-8").read()
    html = re.sub(r"data:[a-z/+]+;base64,[A-Za-z0-9+/=]+", "", html)
    parser = Texts()
    parser.feed(html)
    found = set(parser.out)
    for script in re.findall(r"<script[^>]*>(.*?)</script>", html, re.S):
        for m in re.finditer(r"'((?:[^'\\\n]|\\.){12,})'|\"((?:[^\"\\\n]|\\.){12,})\"", script):
            s = m.group(1) or m.group(2)
            if " " in s and not s.startswith(("http", "#", ".")):
                found.add(s)
    return found


ref, cur = strings(sys.argv[1]), strings(sys.argv[2])
print("=== only in reference ===")
for s in sorted(ref - cur):
    print("-", s[:200])
print("=== only in current ===")
for s in sorted(cur - ref):
    print("+", s[:200])
