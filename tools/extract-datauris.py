"""Extract base64 data URIs from an HTML file into asset files and report their context.

Usage: python3 tools/extract-datauris.py <in.html> <assets dir>
"""
import base64
import re
import sys
from pathlib import Path

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
ext = {"image/jpeg": "jpg", "image/png": "png", "image/svg+xml": "svg"}
for i, m in enumerate(re.finditer(r"data:([a-z/+]+);base64,([A-Za-z0-9+/=]+)", html)):
    name = out_dir / f"v20-asset-{i}.{ext.get(m.group(1), 'bin')}"
    name.write_bytes(base64.b64decode(m.group(2)))
    before = html[max(0, m.start() - 120):m.start()].replace("\n", " ")
    print(f"{name.name}  {name.stat().st_size // 1024} KB  context: ...{before[-120:]}")
