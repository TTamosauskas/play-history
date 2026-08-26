#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "source" / "legacy.html"
AUDIT_FILES = [ROOT / "tools" / "patches" / f"context_1970s_{year}.json" for year in range(1970, 1980)]
GENERIC = {"Música pop", "MPB", "Rock"}
ALLOWED = {"genre","subgenre","movement","century","decade"}


def key(year, artist, title):
    return (int(year), artist, title)


legacy = LEGACY.read_text(encoding="utf-8")
m = re.search(r"const PROJECT\s*=\s*(\{.*?\});\s*\nconst CATALOG", legacy, re.S)
if not m:
    raise SystemExit("PROJECT não encontrado")
tracks = json.loads(m.group(1)).get("tracks") or []
expected = {key(t["year"], t["artist"], t["title"]): t for t in tracks if 1970 <= int(t["year"]) <= 1979}
audit = []
for path in AUDIT_FILES:
    audit.extend(json.loads(path.read_text(encoding="utf-8")))
if len(expected) != 261:
    raise SystemExit(f"Catálogo 1970s inesperado: {len(expected)}")
if len(audit) != 261:
    raise SystemExit(f"Auditoria 1970s inesperada: {len(audit)}")

seen = {}
for item in audit:
    k = key(item.get("year"), item.get("artist"), item.get("title"))
    if k in seen:
        raise SystemExit(f"Duplicata 1970s: {k}")
    targets = item.get("targets")
    if not isinstance(targets, list) or not targets:
        raise SystemExit(f"Contexto vazio: {k}")
    for target in targets:
        if target.get("kind") not in ALLOWED:
            raise SystemExit(f"Tipo inválido: {k}: {target}")
        if not str(target.get("pt") or "").strip() or not str(target.get("en") or "").strip():
            raise SystemExit(f"Alvo incompleto: {k}: {target}")
    primary = targets[0]["pt"]
    if primary in GENERIC:
        raise SystemExit(f"Primário genérico proibido: {k}: {primary}")
    seen[k] = item

missing = set(expected) - set(seen)
extra = set(seen) - set(expected)
if missing or extra:
    raise SystemExit(f"Cobertura 1970s divergente: faltam={sorted(missing)} extras={sorted(extra)}")

regressions = {
    (1970,"Black Sabbath","Paranoid"):"Heavy metal",
    (1972,"Milton Nascimento e Lô Borges","Clube Da Esquina Nº 2"):"Clube da Esquina",
    (1972,"Novos Baianos","Acabou Chorare"):"Bossa nova",
    (1975,"Gilberto Gil","Refazenda"):"Baião",
    (1976,"Fela Kuti","Zombie"):"Afrobeat",
    (1976,"Ramones","Blitzkrieg Bop"):"Punk rock",
    (1977,"Bee Gees","Stayin' Alive"):"Música disco",
    (1977,"Banda Black Rio","Maria Fumaça"):"Samba-funk",
    (1977,"Sex Pistols","God Save the Queen"):"Punk rock",
    (1977,"Caetano Veloso","Odara (Nova Mixagem)"):"Música afro-brasileira",
    (1978,"Chic","Le Freak"):"Música disco",
    (1979,"The Sugarhill Gang","Rapper's Delight"):"Hip hop old-school",
    (1979,"The Clash","London Calling"):"Punk rock",
    (1979,"Gilberto Gil","Realce"):"Música disco",
}
for k, expected_primary in regressions.items():
    actual = seen[k]["targets"][0]["pt"]
    if actual != expected_primary:
        raise SystemExit(f"Regressão 1970s: {k}: {actual!r} != {expected_primary!r}")

changed = sum(
    1 for k, item in seen.items()
    if expected[k].get("contextTermPt") != item["targets"][0]["pt"]
)
full_mpb = sum(1 for item in audit if item["targets"][0]["pt"] == "Música popular brasileira")
if changed < 200:
    raise SystemExit(f"Auditoria pouco específica: apenas {changed} primários alterados")
if full_mpb > 7:
    raise SystemExit(f"Uso excessivo de Música popular brasileira: {full_mpb}")

print(f"OK: 1970s=261/261; primários alterados={changed}; Música popular brasileira={full_mpb}")
