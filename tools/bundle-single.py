"""Inline local assets of an HTML page as data URIs -> single self-contained file.

Usage: python3 tools/bundle-single.py <in.html> <out.html>
"""
import base64
import mimetypes
import re
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
html = src.read_text(encoding="utf-8")


def inline(match):
    ref = match.group(2)
    path = src.parent / ref
    if ref.startswith(("http", "data:", "mailto", "#")) or not path.is_file():
        return match.group(0)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode()
    return f"{match.group(1)}data:{mime};base64,{data}{match.group(3)}"


html = re.sub(r"""((?:src|href)=["'])([^"']+)(["'])""", inline, html)
html = re.sub(r"""(url\(["']?)([^)"']+)(["']?\))""", inline, html)
out.write_text(html, encoding="utf-8")
print(out, out.stat().st_size // 1024, "KB")
