#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "source" / "legacy.html"
PATCHES = ROOT / "tools" / "patches"
RUNTIME = ROOT / "assets" / "catalog-runtime.js"
PACKAGE_RE = re.compile(r"^additions_(\d{4})s\.json$")
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
ARTWORK_RE = re.compile(r"^https://i\.ytimg\.com/vi/([A-Za-z0-9_-]{11})/(?:hqdefault|maxresdefault)\.jpg$")
ALLOWED_CONTEXT_KINDS = {"subgenre", "genre", "movement", "decade", "century"}


def load_legacy_tracks():
    source = LEGACY.read_text(encoding="utf-8")
    match = re.search(r"const PROJECT\s*=\s*(\{[\s\S]*?\});\s*\nconst CATALOG", source)
    if not match:
        raise SystemExit("PROJECT não encontrado em source/legacy.html")
    project = json.loads(match.group(1))
    tracks = project.get("tracks", [])
    if len(tracks) != 1726:
        raise SystemExit(f"Catálogo histórico esperado: 1726; encontrado: {len(tracks)}")
    return tracks


def identity(track):
    return int(track["year"]), str(track["artist"]), str(track["title"])


def addition_packages():
    packages = []
    for path in sorted(PATCHES.glob("additions_*s.json")):
        match = PACKAGE_RE.fullmatch(path.name)
        if not match:
            continue
        tracks = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(tracks, list) or not tracks:
            raise SystemExit(f"Pacote vazio ou inválido: {path.name}")
        packages.append((path, int(match.group(1)), tracks))
    if not packages:
        raise SystemExit("Nenhum pacote additions_*s.json encontrado")
    return packages


def validate_runtime_registration(packages):
    source = RUNTIME.read_text(encoding="utf-8")
    registered = set(re.findall(r"['\"](additions_\d{4}s\.json)['\"]", source))
    available = {path.name for path, _, _ in packages}
    missing = available - registered
    stale = registered - available
    if missing:
        raise SystemExit(f"Pacotes fora do runtime: {', '.join(sorted(missing))}")
    if stale:
        raise SystemExit(f"Pacotes registrados e ausentes: {', '.join(sorted(stale))}")


def main():
    base = load_legacy_tracks()
    packages = addition_packages()
    validate_runtime_registration(packages)

    identities = {identity(track) for track in base}
    youtube_ids = {str(track.get("youtubeId")) for track in base if track.get("youtubeId")}
    total = 0

    for path, decade, additions in packages:
        for track in additions:
            label = f'{track.get("year")} — {track.get("artist")} — {track.get("title")}'
            year = int(track.get("year", 0))
            if year < decade or year > decade + 9:
                raise SystemExit(f"Ano fora do pacote {path.name}: {label}")
            for field in ("artist", "title", "youtubeId", "albumTitle", "artworkUrl", "wikipediaTrackTerm"):
                if not str(track.get(field, "")).strip():
                    raise SystemExit(f"Campo {field} ausente: {label}")

            ident = identity(track)
            if ident in identities:
                raise SystemExit(f"Identidade duplicada: {label}")
            identities.add(ident)

            youtube_id = str(track["youtubeId"])
            if not YOUTUBE_ID_RE.fullmatch(youtube_id):
                raise SystemExit(f"YouTube ID malformado: {label} — {youtube_id}")
            if youtube_id in youtube_ids:
                raise SystemExit(f"YouTube ID duplicado: {label} — {youtube_id}")
            youtube_ids.add(youtube_id)

            artwork = str(track["artworkUrl"])
            artwork_match = ARTWORK_RE.fullmatch(artwork)
            if not artwork_match or artwork_match.group(1) != youtube_id:
                raise SystemExit(f"Artwork fora do padrão ou desacoplado do vídeo: {label}")
            if track.get("lyricsPolicy") != "show_if_verified":
                raise SystemExit(f"lyricsPolicy inesperada: {label}")

            targets = track.get("contextWikiTargets")
            if not isinstance(targets, list) or not targets:
                raise SystemExit(f"Contexto ausente: {label}")
            for target in targets:
                if target.get("kind") not in ALLOWED_CONTEXT_KINDS:
                    raise SystemExit(f"kind de contexto inválido: {label}")
                if not str(target.get("en", "")).strip():
                    raise SystemExit(f"Alvo EN ausente: {label}")
            total += 1

    names = ", ".join(path.name for path, _, _ in packages)
    print(f"OK: {total} adições em {len(packages)} pacotes ({names}); IDs, identidades, artwork, álbum, letra, contexto e registro no runtime validados.")


if __name__ == "__main__":
    main()
