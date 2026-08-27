# Contexto Audit — 1950s

Status: complete in v6.16.0.

## Inventory

- Total catalog tracks: 84
- Generic primary before curation: 49
- Specific-but-reviewable primary before curation: 35
- Coverage by year: 1950=10, 1951=7, 1952=4, 1953=4, 1954=7, 1955=10, 1956=10, 1957=11, 1958=9, 1959=12
- Distinct curated primary contexts: 32

## Editorial result

All 84 tracks from 1950–1959 now have exact year+artist+title Contexto entries, explicit targets and a concise historical basis. The primary link is chosen to explain why the recording matters historically rather than collapse it into a broad taxonomy.

The completed pass includes contexts such as traditional pop, country pop, the American folk revival, multitrack recording, samba-canção, choro, baião, xote, coco, doo-wop, jump blues, New Orleans R&B, honky-tonk, rockabilly, bossa nova, Chicano rock, Brazilian rock and samba-rock.

Primary labels considered too generic for this audit are Música popular, Música pop, Música popular brasileira, MPB, Rock, Jazz, Blues, Samba, Funk and Soul music. A broad genre can remain as a secondary target when historically useful, but not as the primary explanation.

## Validation

```bash
python tools/audit_context_decade.py 1950 --validate-patches
```

CI permanently validates the 1950s audit before the modular build, alongside the 1960s and 1970s regression audits. The v6.16.0 build also verifies that `context_1950s_` is loaded by the public runtime.
