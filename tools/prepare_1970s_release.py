#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / "tools" / "patches"
RELEASE_VERSION = "6.14.0"
DECADE = 1970
EXPECTED_TOTAL = 261
EXPECTED_BY_YEAR = {
    1970: 19,
    1971: 22,
    1972: 25,
    1973: 36,
    1974: 27,
    1975: 29,
    1976: 34,
    1977: 27,
    1978: 20,
    1979: 22,
}
GENERIC_PRIMARY = {
    "Música popular",
    "Música pop",
    "Música popular brasileira",
    "MPB",
    "Rock",
    "Jazz",
    "Blues",
    "Samba",
    "Funk",
    "Soul music",
}
ALLOWED_KINDS = {"genre", "subgenre", "movement", "century", "decade"}


def fail(message: str) -> None:
    raise SystemExit(message)


def load_rows() -> list[dict]:
    rows: list[dict] = []
    counts: Counter[int] = Counter()
    identities: set[tuple[int, str, str]] = set()
    for year in range(DECADE, DECADE + 10):
        path = PATCH_DIR / f"context_1970s_{year}.json"
        if not path.exists():
            fail(f"Arquivo ausente: {path.relative_to(ROOT)}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            fail(f"Patch inválido: {path.relative_to(ROOT)}")
        for item in data:
            key = (int(item.get("year", 0)), str(item.get("artist") or ""), str(item.get("title") or ""))
            if key[0] != year or not key[1] or not key[2]:
                fail(f"Identidade inválida em {path.relative_to(ROOT)}: {key}")
            if key in identities:
                fail(f"Faixa duplicada na década: {key}")
            identities.add(key)
            counts[year] += 1
            targets = item.get("targets")
            if not isinstance(targets, list) or not targets:
                fail(f"Contexto vazio: {key}")
            for target in targets:
                if target.get("kind") not in ALLOWED_KINDS:
                    fail(f"Tipo de contexto inválido: {key}: {target}")
                if not str(target.get("pt") or "").strip() or not str(target.get("en") or "").strip():
                    fail(f"Alvo incompleto: {key}: {target}")
            primary = targets[0]
            if primary.get("pt") in GENERIC_PRIMARY:
                fail(f"Primário genérico: {key}: {primary.get('pt')}")
            if primary.get("kind") in {"century", "decade"}:
                fail(f"Primário histórico amplo demais: {key}: {primary}")
            basis = str(item.get("basis") or "").strip()
            if not basis or "TODO" in basis.upper():
                fail(f"Justificativa editorial ausente: {key}")
            rows.append(item)
    if len(rows) != EXPECTED_TOTAL:
        fail(f"Total 1970s inesperado: {len(rows)} != {EXPECTED_TOTAL}")
    if dict(counts) != EXPECTED_BY_YEAR:
        fail(f"Distribuição anual inesperada: {dict(counts)} != {EXPECTED_BY_YEAR}")
    return rows


def prepare_build() -> None:
    path = ROOT / "tools" / "build.py"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"VERSION='[^']+'", f"VERSION='{RELEASE_VERSION}'", text, count=1)
    if "'label':'1970s'" not in text:
        anchor = "AUDIT_SPECS=[\n    {\n        'label':'1980s'"
        replacement = (
            "AUDIT_SPECS=[\n"
            "    {\n"
            "        'label':'1970s','start':1970,'end':1979,'count':261,\n"
            "        'files':[f'context_1970s_{year}.json' for year in range(1970,1980)],\n"
            "    },\n"
            "    {\n"
            "        'label':'1980s'"
        )
        if anchor not in text:
            fail("Âncora AUDIT_SPECS/1980s não encontrada em tools/build.py")
        text = text.replace(anchor, replacement, 1)
    path.write_text(text, encoding="utf-8")


def prepare_runtime() -> None:
    path = ROOT / "assets" / "catalog-runtime.js"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\* Play History v[^ ]+", f"/* Play History v{RELEASE_VERSION}", text, count=1)
    text = re.sub(r"const VERSION = '[^']+';", f"const VERSION = '{RELEASE_VERSION}';", text, count=1)
    if "context_1970s_" not in text:
        anchor = "    'context_overrides.json',\n"
        insertion = anchor + "    ...Array.from({length: 10}, (_, i) => `context_1970s_${1970 + i}.json`),\n"
        if anchor not in text:
            fail("Âncora context_overrides não encontrada em assets/catalog-runtime.js")
        text = text.replace(anchor, insertion, 1)
    path.write_text(text, encoding="utf-8")


def prepare_index() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'data-build="[^"]+"', f'data-build="{RELEASE_VERSION}"', text, count=1)
    text = re.sub(r'(<title>Player Musical 800–2026 — v)[^<]+', rf'\g<1>{RELEASE_VERSION}', text, count=1)
    text = re.sub(r'(\?v=)[^"\']+', rf'\g<1>{RELEASE_VERSION}', text)
    path.write_text(text, encoding="utf-8")


def write_manifest(rows: list[dict]) -> None:
    primary_counts = Counter(item["targets"][0]["pt"] for item in rows)
    manifest = {
        "release": RELEASE_VERSION,
        "decade": "1970s",
        "tracks": len(rows),
        "byYear": EXPECTED_BY_YEAR,
        "uniquePrimaryContexts": len(primary_counts),
        "mostCommonPrimaryContexts": primary_counts.most_common(15),
    }
    (ROOT / "release_1970s_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    rows = load_rows()
    prepare_build()
    prepare_runtime()
    prepare_index()
    write_manifest(rows)
    print(
        f"OK: 1970s preparados para v{RELEASE_VERSION}; "
        f"{len(rows)} faixas; distribuição {EXPECTED_BY_YEAR}"
    )


if __name__ == "__main__":
    main()
