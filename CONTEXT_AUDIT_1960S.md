# Context audit — 1960s

Status: complete for v6.15.0.

The 1960s Contexto audit covers every catalog track from 1960 through 1969 with an explicit year+artist+title patch and a concise historical basis.

## Coverage

Total: 132 tracks.

- 1960: 12
- 1961: 7
- 1962: 5
- 1963: 5
- 1964: 18
- 1965: 15
- 1966: 12
- 1967: 18
- 1968: 21
- 1969: 19

The initial inventory classified 72 primaries as generic and 60 as requiring historical review. All 132 entries were reviewed. The finished audit rejects broad primaries such as `Música popular`, `Música pop`, `Música popular brasileira`, `MPB`, `Rock`, `Jazz`, `Blues`, `Samba`, `Funk` and `Soul music`.

## Editorial bar

The primary Contexto target answers why the recording matters historically rather than merely identifying a broad genre. The decade therefore uses movements, scenes, production languages, specific subgenres and cultural contexts including Bossa nova, samba-jazz, Jovem Guarda, British Invasion, Motown, baroque pop, psychedelic rock, Summer of Love, Tropicália, protest song, southern soul, jongo, Afro-Brazilian music, Brazilian soul, samba-rock and Brazilian instrumental music.

Broad genres remain useful as secondary targets when they add orientation without replacing the historical explanation.

## Structural enforcement

The decade is represented by ten files:

`tools/patches/context_1960s_1960.json` through `tools/patches/context_1960s_1969.json`.

`tools/audit_context_decade.py 1960 --validate-patches` enforces exact catalog coverage, unique identities, non-empty targets and the stricter generic-primary rule. `tools/build.py` additionally treats the decade as an audited catalog block, and `assets/catalog-runtime.js` loads all ten files in the public player.

The CI workflow runs the 1960s validator before the modular build, JavaScript checks, smoke test and curated-build verification.
