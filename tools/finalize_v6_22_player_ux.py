#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "assets/source/services/01.part"
text = path.read_text(encoding="utf-8")
old = '''      if (youtubeUnavailablePlaceholder){\n        art.classList.remove("has-image");\n        const failedId = track.youtubeId || extractYoutubeVideoId(source);\n        if (failedId && !failedYoutubeIds.has(failedId)){\n          failedYoutubeIds.add(failedId);\n          clearCachedYoutubeIdForTrack(track);\n          artworkCache.delete(trackIdentity(track));\n          if (typeof recoverTrackVideo === "function"){\n            recoverTrackVideo(track, failedId).then(replacementId => {\n              if (token !== artworkRenderToken || !replacementId) return;\n              artworkCache.delete(trackIdentity(track));\n              renderArtwork(track);\n            }).catch(() => {});\n          }\n        }\n        loadNextCandidate();\n        return;\n      }'''
new = '''      if (youtubeUnavailablePlaceholder){\n        art.classList.remove("has-image");\n        // maxresdefault may be absent even for a healthy upload. Treat the ID as\n        // failed only when hqdefault also returns YouTube's 120x90 placeholder.\n        const definitiveYoutubeFailure = /\\/hqdefault\\.jpg(?:$|[?#])/i.test(source);\n        const failedId = definitiveYoutubeFailure ? track.youtubeId : null;\n        if (failedId && !failedYoutubeIds.has(failedId)){\n          failedYoutubeIds.add(failedId);\n          clearCachedYoutubeIdForTrack(track);\n          artworkCache.delete(trackIdentity(track));\n          if (typeof recoverTrackVideo === "function"){\n            recoverTrackVideo(track, failedId).then(replacementId => {\n              if (token !== artworkRenderToken || !replacementId) return;\n              artworkCache.delete(trackIdentity(track));\n              renderArtwork(track);\n            }).catch(() => {});\n          }\n        }\n        loadNextCandidate();\n        return;\n      }'''
if old not in text:
    raise SystemExit("generated placeholder block not found")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Finalized v6.22.0 YouTube placeholder guard")
