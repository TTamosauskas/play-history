#!/usr/bin/env python3
"""Build editorial Contexto work packages with a minimum number of tracks.

A sparse decade is grouped with adjacent decades until the package reaches the
requested minimum. Pre-1900 research defaults to moving backward in time, which
matches the editorial rollout after the 1890s pilot. The terminal catalog slice
can optionally be emitted as a partial package when fewer than the requested
minimum tracks remain.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from audit_context_decade import iter_decade_rows, row_quality, specificity_level

PATCH_DIR = Path(__file__).resolve().parent / "patches"


def resolve_package(
    anchor: int,
    minimum: int,
    include_additions: bool,
    direction: str,
    allow_partial: bool = False,
):
    start = anchor
    end = anchor + 9

    for _ in range(220):
        rows = iter_decade_rows(start, end, include_additions)
        if len(rows) >= minimum:
            return start, end, rows

        at_boundary = (direction == "backward" and start <= 0) or (
            direction == "forward" and end >= 2999
        )
        if at_boundary:
            if allow_partial and rows:
                return start, end, rows
            break

        if direction == "backward":
            start = max(0, start - 10)
        else:
            end = min(2999, end + 10)

    raise SystemExit(
        f"Catálogo insuficiente para formar pacote de {minimum} faixas a partir de {anchor}s."
    )


def package_label(start: int, end: int) -> str:
    if start == end - 9 and start % 10 == 0:
        return f"{start}s"
    return f"{start}–{end}"


def curated_package_overrides(start: int, end: int):
    overrides = {}
    for path in sorted(PATCH_DIR.glob("context_pre1900_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise SystemExit(f"Pacote de Contexto inválido: {path.name}")
        for item in data:
            try:
                year = int(item.get("year"))
            except (TypeError, ValueError):
                raise SystemExit(f"Ano inválido em {path.name}: {item!r}")
            if year < start or year > end:
                continue
            key = (year, item.get("artist"), item.get("title"))
            targets = item.get("targets")
            if not key[1] or not key[2] or not isinstance(targets, list) or not targets:
                raise SystemExit(f"Entrada incompleta em {path.name}: {item!r}")
            if key in overrides:
                raise SystemExit(f"Contexto de pacote duplicado: {key}")
            overrides[key] = (targets, path.name)
    return overrides


def apply_curated_package(rows, start: int, end: int):
    overrides = curated_package_overrides(start, end)
    if not overrides:
        return rows

    row_keys = {(int(row["year"]), row["artist"], row["title"]) for row in rows}
    missing = set(overrides) - row_keys
    if missing:
        raise SystemExit(f"Overrides de pacote sem faixa correspondente: {sorted(missing)}")

    curated = []
    for row in rows:
        copy = dict(row)
        key = (int(copy["year"]), copy["artist"], copy["title"])
        override = overrides.get(key)
        if override:
            targets, source_file = override
            primary = targets[0]
            status, issue = row_quality(targets, historical_specificity=True)
            copy.update(
                targets=targets,
                source=f"package:{source_file}",
                status=status,
                issue=issue,
                specificity=specificity_level(targets),
                primary_kind=primary.get("kind", ""),
                primary_pt=primary.get("pt", ""),
                primary_en=primary.get("en", ""),
            )
        curated.append(copy)
    return curated


def validate_specificity(rows, required_level: int) -> None:
    weak = [
        row for row in rows
        if int(row.get("specificity", -1)) < required_level
    ]
    if weak:
        preview = "; ".join(
            f"{row['year']} · {row['artist']} — {row['title']} "
            f"(L{row.get('specificity', -1)}: {row.get('primary_pt', '')})"
            for row in weak[:12]
        )
        suffix = "" if len(weak) <= 12 else f"; +{len(weak) - 12} outras"
        raise SystemExit(
            f"Pacote abaixo da especificidade mínima L{required_level}: "
            f"{len(weak)} faixas. {preview}{suffix}"
        )


def write_csv(rows, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "year", "artist", "title", "source", "status", "issue", "specificity",
        "primary_kind", "primary_pt", "primary_en",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_markdown(rows, output: Path, start: int, end: int, minimum: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    by_status = Counter(row["status"] for row in rows)
    by_year = Counter(row["year"] for row in rows)
    by_specificity = Counter(row["specificity"] for row in rows)
    decades = list(range((start // 10) * 10, (end // 10) * 10 + 1, 10))
    decade_counts = {
        decade: sum(1 for row in rows if decade <= int(row["year"]) <= decade + 9)
        for decade in decades
    }

    lines = [
        f"# Contexto research package — {package_label(start, end)}",
        "",
        f"Minimum target: {minimum} tracks",
        f"Actual tracks: {len(rows)}",
        f"Range: {start}–{end}",
        "",
        "Decade counts: " + ", ".join(
            f"{decade}s={count}" for decade, count in decade_counts.items()
        ),
        "",
        "Status counts: " + ", ".join(
            f"{name}={count}" for name, count in sorted(by_status.items())
        ),
        "",
        "Specificity counts: " + ", ".join(
            f"L{level}={by_specificity[level]}" for level in sorted(by_specificity)
        ),
        "",
        "Year counts: " + ", ".join(
            f"{year}={by_year[year]}" for year in sorted(by_year)
        ),
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Group sparse Contexto decades into editorial packages."
    )
    parser.add_argument("anchor", type=int, help="Anchor decade, e.g. 1890")
    parser.add_argument("--min-tracks", type=int, default=50, help="Minimum package size")
    parser.add_argument(
        "--direction", choices=("backward", "forward"), default="backward",
        help="Direction used to add adjacent decades",
    )
    parser.add_argument("--include-additions", action="store_true")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Emit the terminal catalog slice when fewer than --min-tracks remain",
    )
    parser.add_argument(
        "--require-specificity",
        type=int,
        choices=(0, 1, 2, 3),
        help="Fail when any track has specificity below this level",
    )
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()

    if args.anchor % 10 != 0:
        raise SystemExit("Use o início da década, por exemplo 1890.")
    if args.min_tracks < 1:
        raise SystemExit("--min-tracks deve ser maior que zero.")

    start, end, rows = resolve_package(
        args.anchor,
        args.min_tracks,
        args.include_additions,
        args.direction,
        args.allow_partial,
    )
    rows = apply_curated_package(rows, start, end)
    label = package_label(start, end)

    if args.require_specificity is not None:
        validate_specificity(rows, args.require_specificity)

    if args.csv:
        write_csv(rows, args.csv)
    if args.markdown:
        write_markdown(rows, args.markdown, start, end, args.min_tracks)

    by_decade = Counter((int(row["year"]) // 10) * 10 for row in rows)
    by_specificity = Counter(int(row.get("specificity", -1)) for row in rows)
    print(f"package={label} tracks={len(rows)} minimum={args.min_tracks}")
    print("by_decade: " + ", ".join(
        f"{decade}s={by_decade[decade]}" for decade in sorted(by_decade)
    ))
    print("by_specificity: " + ", ".join(
        f"L{level}={by_specificity[level]}" for level in sorted(by_specificity)
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
