#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "6.21.0"

build = ROOT / "tools" / "build.py"
text = build.read_text(encoding="utf-8")
text = text.replace("VERSION='6.20.0'", "VERSION='6.21.0'", 1)
marker = "AUDIT_SPECS=[\n    {\n        'label':'1910s'"
if "'label':'1900s'" not in text:
    replacement = "AUDIT_SPECS=[\n    {\n        'label':'1900s','start':1900,'end':1909,'count':60,\n        'files':[f'context_1900s_{year}.json' for year in range(1900,1910)],\n    },\n    {\n        'label':'1910s'"
    if marker not in text:
        raise SystemExit('AUDIT_SPECS 1910s marker not found')
    text = text.replace(marker, replacement, 1)
build.write_text(text, encoding="utf-8")

runtime = ROOT / "assets" / "catalog-runtime.js"
text = runtime.read_text(encoding="utf-8")
text = text.replace("v6.20.0", "v6.21.0", 1)
text = text.replace("const VERSION = '6.20.0';", "const VERSION = '6.21.0';", 1)
line = "    ...Array.from({length: 10}, (_, i) => `context_1900s_${1900 + i}.json`),\n"
marker = "    ...Array.from({length: 10}, (_, i) => `context_1910s_${1910 + i}.json`),\n"
if line not in text:
    if marker not in text:
        raise SystemExit('runtime 1910s marker not found')
    text = text.replace(marker, line + marker, 1)
runtime.write_text(text, encoding="utf-8")

index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
text = text.replace('data-build="6.20.0"', 'data-build="6.21.0"', 1)
text = text.replace('— v6.20.0</title>', '— v6.21.0</title>', 1)
text = text.replace('?v=6.20.0', '?v=6.21.0')
index.write_text(text, encoding="utf-8")
