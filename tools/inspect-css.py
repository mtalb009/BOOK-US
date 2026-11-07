"""Print CSS rules whose selector contains any of the given substrings.

Usage: python3 tools/inspect-css.py <file.html> <substr> [<substr> ...]
"""
import sys

path, needles = sys.argv[1], sys.argv[2:]
html = open(path, encoding="utf-8").read()
css = []
pos = 0
while True:
    a = html.find("<style", pos)
    if a < 0:
        break
    a = html.find(">", a) + 1
    b = html.find("</style>", a)
    css.append(html[a:b])
    pos = b
css = "\n".join(css)
for chunk in css.split("}"):
    if "{" not in chunk:
        continue
    sel, body = chunk.rsplit("{", 1)
    sel = sel.split("{")[-1].strip()
    if any(n in sel for n in needles):
        print(f"{sel[:90]} {{ {body.strip()[:220]} }}")
