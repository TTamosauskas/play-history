# Contexto Audit — 1920s

Status: curation complete; release integration in progress.

## Inventory

- Total catalog tracks: 62
- Generic current primary before curation: 61
- Specific-but-reviewable current primary before curation: 1
- Coverage by year: 1920=6, 1921=6, 1922=3, 1923=5, 1924=6, 1925=6, 1926=5, 1927=11, 1928=7, 1929=7
- Distinct curated primary contexts: 35
- Generic primaries after curation: 0

## Editorial result

The decade is covered by ten exact year+artist+title patch files. Primary targets emphasize historically explanatory contexts rather than broad taxonomy: vaudeville blues and race records, Tin Pan Alley and vaudeville, dance bands and early big-band development, classic female blues, Charleston and the Harlem Renaissance, symphonic jazz and classical crossover, old-time/country commercialization, crooners, New Orleans jazz, jazz standards and improvisation, jungle style, flapper culture, early musical film and stride piano. Brazilian tracks are separated into urban samba and political satire, cançoneta, embolada, frevo-canção, carnival samba, revue, valsa-serenata/seresta, samba amaxixado/electrical recording, choro-canção, samba-canção and modinha.

## Acceptance criteria

1. Ten per-year patch files cover all 62 identities exactly once. — complete
2. No primary target remains in the strict generic-primary set. — complete
3. Each row has a concise historical basis. — complete
4. `python tools/audit_context_decade.py 1920 --validate-patches` passes. — CI gate enabled
5. 1920s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete. — release gate in progress
6. Existing 1930s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green. — regression gate enabled
