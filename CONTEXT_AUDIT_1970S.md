# Context audit — 1970s

Status: inventory gate first.

The 1970s should enter the same editorial regime already used for 1980s onward: every track must receive an explicit Contexto target, every audited target must have `pt` and `en`, and the build must fail when a track is missing or when the primary target is generic.

The current build enforces full audits only from 1980 onward. The 1970s are therefore being moved through a stricter pipeline before any broad replacement lands.

## Bar for the decade

The Contexto link should explain why the track matters historically, not merely name the broad genre. “Rock”, “Música pop”, “MPB”, “Samba”, “Funk”, “Soul music” and similarly broad primaries are starting points for research, not acceptable final primary targets for an audited decade.

For the 1970s, stronger targets usually sit at the level of scene, movement, production language, technology, club culture, political context, label ecosystem, or subgenre: examples include Tropicália afterlife, Clube da Esquina, Black Rio, Philly soul, roots reggae, dub, krautrock, glam rock, punk rock, disco, hard rock, heavy metal, progressive rock, funk rock, samba-rock, música nordestina, fusion, and Brazilian instrumental music. The correct target depends on the track.

## Workflow

Run the inventory from the repository root:

```bash
python tools/audit_context_decade.py 1970 --csv /tmp/context_1970s_inventory.csv --markdown /tmp/context_1970s_inventory.md
```

Generate editable per-year skeletons only after inspecting the inventory:

```bash
python tools/audit_context_decade.py 1970 --write-skeleton
```

Curate `tools/patches/context_1970s_1970.json` through `tools/patches/context_1970s_1979.json` by replacing weak current targets and every `TODO` basis with a specific historical justification.

Validate the decade before adding it to `AUDIT_SPECS`:

```bash
python tools/audit_context_decade.py 1970 --validate-patches
```

Only after validation passes should `tools/build.py` receive the 1970s audit spec and `assets/catalog-runtime.js` receive the 1970s patch list.

## Acceptance criteria

A complete 1970s pass has ten per-year patch files, one row for every catalog track from 1970 to 1979, no missing or extra rows, no duplicate year-artist-title identity, no generic primary target, and a concise `basis` field that explains the historical reason for the chosen Contexto target.

This avoids the false progress of swapping a few visible links while leaving the decade structurally weaker than the audited 1980s–2020s.
