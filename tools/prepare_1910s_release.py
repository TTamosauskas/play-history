#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "6.20.0"

build = ROOT / "tools" / "build.py"
text = build.read_text(encoding="utf-8")
text = text.replace("VERSION='6.19.0'", "VERSION='6.20.0'", 1)
marker = "AUDIT_SPECS=[\n    {\n        'label':'1920s'"
if "'label':'1910s'" not in text:
    replacement = "AUDIT_SPECS=[\n    {\n        'label':'1910s','start':1910,'end':1919,'count':61,\n        'files':[f'context_1910s_{year}.json' for year in range(1910,1920)],\n    },\n    {\n        'label':'1920s'"
    if marker not in text:
        raise SystemExit('AUDIT_SPECS 1920s marker not found')
    text = text.replace(marker, replacement, 1)
build.write_text(text, encoding="utf-8")

runtime = ROOT / "assets" / "catalog-runtime.js"
text = runtime.read_text(encoding="utf-8")
text = text.replace("v6.19.0", "v6.20.0", 1)
text = text.replace("const VERSION = '6.19.0';", "const VERSION = '6.20.0';", 1)
line = "    ...Array.from({length: 10}, (_, i) => `context_1910s_${1910 + i}.json`),\n"
marker = "    ...Array.from({length: 10}, (_, i) => `context_1920s_${1920 + i}.json`),\n"
if line not in text:
    if marker not in text:
        raise SystemExit('runtime 1920s marker not found')
    text = text.replace(marker, line + marker, 1)
runtime.write_text(text, encoding="utf-8")

index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
text = text.replace('data-build="6.19.0"', 'data-build="6.20.0"', 1)
text = text.replace('— v6.19.0</title>', '— v6.20.0</title>', 1)
text = text.replace('?v=6.19.0', '?v=6.20.0')
index.write_text(text, encoding="utf-8")
