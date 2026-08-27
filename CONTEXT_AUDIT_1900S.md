# Contexto Audit — 1900s

Status: curation complete; release integration in progress.

## Inventory

- Total catalog tracks: 60
- Generic current primary before curation: 56
- Specific-but-reviewable current primary before curation: 4
- Coverage by year: 1900=6, 1901=4, 1902=7, 1903=6, 1904=6, 1905=8, 1906=7, 1907=5, 1908=5, 1909=6
- Distinct curated primary contexts: 27
- Generic primaries after curation: 0

## Editorial result

The decade is covered by ten exact year+artist+title patch files. Primary targets separate Tin Pan Alley, parlor song, vaudeville, musical theatre, Broadway, operetta, barbershop, ragtime, old-time music, march/patriotic repertory, opera/aria, automobile and aviation modernity, the St. Louis World's Fair, baseball and the Ziegfeld Follies. Historically racialized commercial repertory is identified explicitly through coon song/minstrelsy and African-American musical-theatre contexts rather than hidden under generic labels.

Brazilian tracks are separated into tango brasileiro, choro, lundu, modinha, maxixe, valsa and the early recording industry. Notable anchors include Digo as an Ernesto Nazareth tango; Isto É Bom as lundu and landmark of Brazilian disc recording; Santos Dumont (A Conquista do Ar) as a marcha/dobrado about aviation; Primeiro Amor as a valsa in Patápio Silva's choro-era repertory; Casinha Pequenina as modinha; Gaúcho (Corta-Jaca) as maxixe/tango brasileiro; and Eduardo das Neves' repertory as part of the lundu, popular stage and early phonographic culture.

## Acceptance criteria

1. Ten per-year patch files cover all 60 identities exactly once. — complete
2. No primary target remains in the strict generic-primary set. — complete
3. Each row has a concise historical basis. — complete
4. `python tools/audit_context_decade.py 1900 --validate-patches` passes. — pending CI gate
5. 1900s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete. — release gate pending
6. Existing 1910s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green. — regression gate pending
