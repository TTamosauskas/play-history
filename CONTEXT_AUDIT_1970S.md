# Context audit — 1970s

Status: complete in v6.14.0.

The 1970s now use the same explicit editorial regime as the later audited decades: every catalog track from 1970 through 1979 has an exact year+artist+title Contexto row, every target has `pt` and `en`, the decade is wired into `tools/build.py` `AUDIT_SPECS`, the public runtime loads all ten year files, and CI validates the decade before every build.

## Scope and result

The inventory contains 261 tracks: 1970=19, 1971=22, 1972=25, 1973=36, 1974=27, 1975=29, 1976=34, 1977=27, 1978=20, 1979=22.

Before curation, 210 of the 261 rows had a generic primary context and the remaining 51 still required historical review. The completed pass uses 69 distinct primary contexts across the decade.

## Editorial bar

The Contexto link should explain why a track matters historically rather than merely name a broad genre. Broad labels such as “Rock”, “Música pop”, “Música popular brasileira”, “MPB”, “Samba”, “Funk”, “Soul music”, “Jazz” and “Blues” are treated as research starting points rather than acceptable audited primaries.

The curated targets therefore work at the level of scene, movement, production language, technology, club culture, political context, or specific subgenre. Across the decade this includes, among others, Tropicália, Clube da Esquina, soul brasileiro, Black Rio, samba-rock, samba-jazz, música de protesto, jazz fusion, rock psicodélico, rock progressivo, glam rock, punk rock, disco, reggae, hard rock and heavy metal.

Each row also carries a concise `basis` field explaining the historical reason for the chosen target.

## Files

The complete audit is stored in `tools/patches/context_1970s_1970.json` through `tools/patches/context_1970s_1979.json`.

`tools/audit_context_decade.py` can reproduce the inventory and validates exact coverage, duplicate identities, empty targets, generic primaries and overly broad period targets.

Run the decade-specific validation with:

```bash
python tools/audit_context_decade.py 1970 --validate-patches
```

The normal build then validates the decade again through `AUDIT_SPECS`:

```bash
python tools/build.py
```

## Acceptance criteria

The completed pass has ten per-year patch files, one row for every one of the 261 catalog tracks, no missing or extra identities, no duplicate year-artist-title identity, no generic primary target under the stricter 1970s audit, complete bilingual targets, and a historical `basis` for every row.

This puts the 1970s under durable build and CI protection rather than leaving the improvement as a one-time link cleanup.
