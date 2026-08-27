#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / "tools" / "patches"
VERSION_OLD = "6.17.0"
VERSION_NEW = "6.18.0"
DECADE = 1930
EXPECTED_TOTAL = 66
EXPECTED_BY_YEAR = {1930:9,1931:8,1932:5,1933:6,1934:3,1935:7,1936:6,1937:8,1938:6,1939:8}
GENERIC_PRIMARY = {"Música popular","Música pop","Música popular brasileira","MPB","Rock","Jazz","Blues","Samba","Funk","Soul music"}


def validate_patches() -> None:
    total = 0
    seen = set()
    for year, expected in EXPECTED_BY_YEAR.items():
        path = PATCH_DIR / f"context_{DECADE}s_{year}.json"
        rows = json.loads(path.read_text(encoding="utf-8"))
        if len(rows) != expected:
            raise SystemExit(f"{path.name}: {len(rows)} != {expected}")
        for row in rows:
            key = (int(row.get("year")), row.get("artist"), row.get("title"))
            if key in seen:
                raise SystemExit(f"duplicate: {key}")
            seen.add(key)
            targets = row.get("targets") or []
            if not targets:
                raise SystemExit(f"empty targets: {key}")
            primary = targets[0].get("pt")
            if primary in GENERIC_PRIMARY:
                raise SystemExit(f"generic primary: {key}: {primary}")
            if not str(row.get("basis") or "").strip() or "TODO" in str(row.get("basis")):
                raise SystemExit(f"invalid basis: {key}")
        total += len(rows)
    if total != EXPECTED_TOTAL:
        raise SystemExit(f"total {total} != {EXPECTED_TOTAL}")


def patch_build() -> None:
    path = ROOT / "tools" / "build.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(f"VERSION='{VERSION_OLD}'", f"VERSION='{VERSION_NEW}'", 1)
    marker = "AUDIT_SPECS=[\n"
    spec = (
        "    {\n"
        "        'label':'1930s','start':1930,'end':1939,'count':66,\n"
        "        'files':[f'context_1930s_{year}.json' for year in range(1930,1940)],\n"
        "    },\n"
    )
    if "'label':'1930s'" not in text:
        text = text.replace(marker, marker + spec, 1)
    if f"VERSION='{VERSION_NEW}'" not in text or "'label':'1930s'" not in text:
        raise SystemExit("build patch failed")
    path.write_text(text, encoding="utf-8")


def patch_runtime() -> None:
    path = ROOT / "assets" / "catalog-runtime.js"
    text = path.read_text(encoding="utf-8")
    text = text.replace(f"v{VERSION_OLD}", f"v{VERSION_NEW}", 1)
    text = text.replace(f"const VERSION = '{VERSION_OLD}';", f"const VERSION = '{VERSION_NEW}';", 1)
    marker = "    'context_overrides.json',\n"
    line = "    ...Array.from({length: 10}, (_, i) => `context_1930s_${1930 + i}.json`),\n"
    if "context_1930s_" not in text:
        text = text.replace(marker, marker + line, 1)
    if f"const VERSION = '{VERSION_NEW}';" not in text or "context_1930s_" not in text:
        raise SystemExit("runtime patch failed")
    path.write_text(text, encoding="utf-8")


def patch_index() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8").replace(VERSION_OLD, VERSION_NEW)
    if VERSION_NEW not in text or VERSION_OLD in text:
        raise SystemExit("index patch failed")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    validate_patches()
    patch_build()
    patch_runtime()
    patch_index()
    print(f"OK: prepared 1930s release candidate v{VERSION_NEW}; {EXPECTED_TOTAL} tracks")


if __name__ == "__main__":
    main()
