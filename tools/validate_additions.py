#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "source" / "legacy.html"
ADDITIONS = ROOT / "tools" / "patches" / "additions_2020s.json"
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
ARTWORK_RE = re.compile(r"^https://i\.ytimg\.com/vi/[A-Za-z0-9_-]{11}/(?:hqdefault|maxresdefault)\.jpg$")
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


def main():
    base = load_legacy_tracks()
    additions = json.loads(ADDITIONS.read_text(encoding="utf-8"))
    if len(additions) != 21:
        raise SystemExit(f"Pacote 2020s esperado: 21; encontrado: {len(additions)}")

    identities = {identity(track) for track in base}
    youtube_ids = {str(track.get("youtubeId")) for track in base if track.get("youtubeId")}
    added_ids = set()

    for track in additions:
        label = f'{track.get("year")} — {track.get("artist")} — {track.get("title")}'
        year = int(track.get("year", 0))
        if year < 2020 or year > 2029:
            raise SystemExit(f"Ano fora do pacote: {label}")
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
        if youtube_id in youtube_ids or youtube_id in added_ids:
            raise SystemExit(f"YouTube ID duplicado: {label} — {youtube_id}")
        added_ids.add(youtube_id)

        artwork = str(track["artworkUrl"])
        if not ARTWORK_RE.fullmatch(artwork):
            raise SystemExit(f"Artwork fora do padrão: {label}")
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

    print(f"OK: {len(additions)} adições 2020s; IDs, identidades, artwork, álbum, letra e contexto validados.")


if __name__ == "__main__":
    main()
