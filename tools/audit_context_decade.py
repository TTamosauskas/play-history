#!/usr/bin/env python3
"""
Audit Contexto curation for one decade.

This tool reads the canonical legacy catalog, applies the same context precedence
used by the player/build pipeline, and emits an audit inventory for a decade.
It is intentionally strict: a decade should only enter tools/build.py AUDIT_SPECS
after every track has an explicit, historically informative target.

For pre-1900 research, --include-additions folds the curated additions package for
the decade into the inventory and the specificity score distinguishes musical
form/subgenre from broad movement/period labels.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "source" / "legacy.html"
PATCH_DIR = ROOT / "tools" / "patches"

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
LOW_INFORMATION_KINDS = {"century", "decade"}
SPECIFICITY_LEVELS = {
    "form": 3,
    "subgenre": 3,
    "genre": 2,
    "tradition": 2,
    "movement": 1,
    "century": 0,
    "decade": 0,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_project() -> list[dict[str, Any]]:
    text = LEGACY.read_text(encoding="utf-8")
    match = re.search(r"const PROJECT\s*=\s*(\{.*?\});\s*\nconst CATALOG", text, re.S)
    if not match:
        raise SystemExit("PROJECT não encontrado em source/legacy.html")
    project = json.loads(match.group(1))
    tracks = project.get("tracks") or []
    if not isinstance(tracks, list) or not tracks:
        raise SystemExit("Catálogo vazio ou inválido em source/legacy.html")
    return tracks


def addition_tracks(start: int, end: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(PATCH_DIR.glob("additions_*.json")):
        data = load_json(path)
        if not isinstance(data, list):
            continue
        for track in data:
            try:
                year = int(track.get("year"))
            except (TypeError, ValueError):
                continue
            if start <= year <= end:
                copy = dict(track)
                copy["_audit_targets"] = copy.get("contextWikiTargets") or []
                rows.append(copy)
    return rows


def patch_files() -> list[Path]:
    files = [PATCH_DIR / "context_overrides.json"]
    files.extend(sorted(PATCH_DIR.glob("context_[0-9][0-9][0-9][0-9]s_*.json")))
    files.extend(sorted(PATCH_DIR.glob("context_20[0-9][0-9]s.json")))
    return [path for path in files if path.exists()]


def build_override_maps() -> tuple[dict[tuple[int, str, str], list[dict[str, Any]]], dict[tuple[str, str], list[dict[str, Any]]]]:
    exact: dict[tuple[int, str, str], list[dict[str, Any]]] = {}
    loose: dict[tuple[str, str], list[dict[str, Any]]] = {}

    for path in patch_files():
        rows = load_json(path)
        if not isinstance(rows, list):
            raise SystemExit(f"Patch inválido: {path}")
        for item in rows:
            if not isinstance(item, dict):
                raise SystemExit(f"Item inválido em {path}: {item!r}")
            artist = item.get("artist")
            title = item.get("title")
            targets = item.get("targets")
            if not artist or not title or not isinstance(targets, list) or not targets:
                raise SystemExit(f"Patch incompleto em {path}: {item!r}")
            if item.get("year") is None:
                key = (artist, title)
                if key in loose:
                    raise SystemExit(f"Override solto duplicado: {key}")
                loose[key] = targets
            else:
                key = (int(item["year"]), artist, title)
                if key in exact:
                    raise SystemExit(f"Override exato duplicado: {key}")
                exact[key] = targets

    return exact, loose


def base_pattern_targets(track_index: int) -> list[dict[str, Any]]:
    patterns = load_json(PATCH_DIR / "context_patterns.json")
    indices = load_json(PATCH_DIR / "context_index_a.json") + load_json(PATCH_DIR / "context_index_b.json")
    if track_index >= len(indices):
        raise SystemExit(f"Índice de contexto ausente para faixa #{track_index}")
    return patterns[int(indices[track_index])]


def current_targets(track: dict[str, Any], track_index: int | None, exact: dict, loose: dict) -> tuple[list[dict[str, Any]], str]:
    year = int(track.get("year"))
    artist = track.get("artist") or ""
    title = track.get("title") or ""
    exact_key = (year, artist, title)
    loose_key = (artist, title)

    if exact_key in exact:
        return exact[exact_key], "audited"
    if loose_key in loose:
        return loose[loose_key], "legacy_override"
    if track_index is None:
        return track.get("_audit_targets") or track.get("contextWikiTargets") or [], "addition"
    return base_pattern_targets(track_index), "pattern"


def specificity_level(targets: list[dict[str, Any]]) -> int:
    primary = targets[0] if targets else {}
    return SPECIFICITY_LEVELS.get(str(primary.get("kind") or "").strip(), -1)


def row_quality(targets: list[dict[str, Any]], historical_specificity: bool = False) -> tuple[str, str]:
    primary = targets[0] if targets else {}
    pt = str(primary.get("pt") or "").strip()
    kind = str(primary.get("kind") or "").strip()
    level = specificity_level(targets)
    if not pt:
        return "missing", "sem contexto primário"
    if pt in GENERIC_PRIMARY:
        return "generic", f"primário genérico: {pt}"
    if kind in LOW_INFORMATION_KINDS:
        return "low_information", f"tipo fraco: {kind}"
    if historical_specificity and level < 2:
        return "underspecified", f"especificidade histórica baixa: {kind or '?'} (nível {level})"
    return "review", "revisar historicamente"


def iter_decade_rows(start: int, end: int, include_additions: bool = False) -> list[dict[str, Any]]:
    base_tracks = load_project()
    exact, loose = build_override_maps()
    historical_specificity = end < 1900
    rows: list[dict[str, Any]] = []
    identities: set[tuple[int, str, str]] = set()

    def append_track(track: dict[str, Any], track_index: int | None) -> None:
        year = int(track.get("year"))
        artist = track.get("artist") or ""
        title = track.get("title") or ""
        identity = (year, artist, title)
        if identity in identities:
            return
        targets, source = current_targets(track, track_index, exact, loose)
        status, issue = row_quality(targets, historical_specificity)
        primary = targets[0] if targets else {}
        rows.append(
            {
                "year": year,
                "artist": artist,
                "title": title,
                "source": source,
                "status": status,
                "issue": issue,
                "specificity": specificity_level(targets),
                "primary_kind": primary.get("kind", ""),
                "primary_pt": primary.get("pt", ""),
                "primary_en": primary.get("en", ""),
                "targets": targets,
            }
        )
        identities.add(identity)

    for index, track in enumerate(base_tracks):
        year = int(track.get("year"))
        if start <= year <= end:
            append_track(track, index)

    if include_additions:
        for track in addition_tracks(start, end):
            append_track(track, None)

    rows.sort(key=lambda row: (row["year"], row["artist"], row["title"]))
    return rows


def write_csv(rows: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["year", "artist", "title", "source", "status", "issue", "specificity", "primary_kind", "primary_pt", "primary_en"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_markdown(rows: list[dict[str, Any]], output: Path, label: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    by_status = Counter(row["status"] for row in rows)
    by_year = Counter(row["year"] for row in rows)
    by_specificity = Counter(row["specificity"] for row in rows)
    lines = [
        f"# Contexto audit inventory — {label}",
        "",
        f"Total tracks: {len(rows)}",
        "",
        "Status counts: " + ", ".join(f"{name}={count}" for name, count in sorted(by_status.items())),
        "",
        "Specificity counts: " + ", ".join(f"L{level}={by_specificity[level]}" for level in sorted(by_specificity)),
        "",
        "Year counts: " + ", ".join(f"{year}={by_year[year]}" for year in sorted(by_year)),
        "",
        "| Year | Artist | Title | Current primary | Kind | Specificity | Source | Status | Issue |",
        "| --- | --- | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['year']} | {row['artist']} | {row['title']} | "
            f"{row['primary_pt']} | {row['primary_kind']} | {row['specificity']} | "
            f"{row['source']} | {row['status']} | {row['issue']} |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_skeleton(rows: list[dict[str, Any]], decade: int, patch_dir: Path) -> None:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["year"])].append(row)

    for year in range(decade, decade + 10):
        items = []
        for row in grouped.get(year, []):
            items.append(
                {
                    "year": year,
                    "artist": row["artist"],
                    "title": row["title"],
                    "targets": row["targets"],
                    "basis": "TODO: justificar forma/subgênero/tradição com fonte histórica específica.",
                }
            )
        path = patch_dir / f"context_{decade}s_{year}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_patch_coverage(rows: list[dict[str, Any]], decade: int) -> int:
    expected = {(row["year"], row["artist"], row["title"]) for row in rows}
    actual: dict[tuple[int, str, str], dict[str, Any]] = {}
    historical_specificity = decade < 1900

    for year in range(decade, decade + 10):
        path = PATCH_DIR / f"context_{decade}s_{year}.json"
        if not path.exists():
            print(f"missing patch file: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        for item in load_json(path):
            key = (int(item.get("year")), item.get("artist"), item.get("title"))
            if key in actual:
                print(f"duplicate audit row: {key}", file=sys.stderr)
                return 1
            targets = item.get("targets")
            if not isinstance(targets, list) or not targets:
                print(f"empty targets: {key}", file=sys.stderr)
                return 1
            status, issue = row_quality(targets, historical_specificity)
            if status in {"missing", "generic", "low_information", "underspecified"}:
                print(f"weak primary target: {key}: {issue}", file=sys.stderr)
                return 1
            actual[key] = item

    missing = expected - set(actual)
    extra = set(actual) - expected
    if missing or extra:
        print(f"incomplete audit: missing={sorted(missing)} extra={sorted(extra)}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory and validate Contexto targets for a decade.")
    parser.add_argument("decade", type=int, help="Decade start, e.g. 1970")
    parser.add_argument("--csv", type=Path, help="Write inventory CSV")
    parser.add_argument("--markdown", type=Path, help="Write inventory Markdown")
    parser.add_argument("--include-additions", action="store_true", help="Include additions_<decade>s*.json in the runtime inventory")
    parser.add_argument("--write-skeleton", action="store_true", help="Write context_<decade>s_<year>.json skeleton files")
    parser.add_argument("--validate-patches", action="store_true", help="Validate curated per-year files for this decade")
    args = parser.parse_args()

    if args.decade % 10 != 0:
        raise SystemExit("Use o início da década, por exemplo 1970.")
    start = args.decade
    end = args.decade + 9
    rows = iter_decade_rows(start, end, args.include_additions)
    if not rows:
        raise SystemExit(f"Nenhuma faixa encontrada entre {start} e {end}.")

    label = f"{start}s"
    if args.csv:
        write_csv(rows, args.csv)
    if args.markdown:
        write_markdown(rows, args.markdown, label)
    if args.write_skeleton:
        write_skeleton(rows, args.decade, PATCH_DIR)
    if args.validate_patches:
        return validate_patch_coverage(rows, args.decade)

    by_status = Counter(row["status"] for row in rows)
    by_year = Counter(row["year"] for row in rows)
    by_specificity = Counter(row["specificity"] for row in rows)
    print(f"{label}: {len(rows)} tracks")
    print("by_year: " + ", ".join(f"{year}={by_year[year]}" for year in sorted(by_year)))
    print("by_status: " + ", ".join(f"{name}={count}" for name, count in sorted(by_status.items())))
    print("by_specificity: " + ", ".join(f"L{level}={by_specificity[level]}" for level in sorted(by_specificity)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())