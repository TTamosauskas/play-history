# Contexto Audit — 1900s

Status: inventory complete; curation in progress.

## Inventory

- Total catalog tracks: 60
- Generic current primary: 56
- Specific-but-reviewable current primary: 4
- Coverage by year: 1900=6, 1901=4, 1902=7, 1903=6, 1904=6, 1905=8, 1906=7, 1907=5, 1908=5, 1909=6

## Editorial bar

Every 1900–1909 track must receive an exact year+artist+title Contexto entry. The primary link must explain why the recording matters historically rather than collapse it into broad taxonomy such as Música popular, Ragtime, Choro, Samba or Tango brasileiro when a more specific historical framing is available.

Priority contexts for this decade include the acoustic-recording era; Tin Pan Alley, vaudeville, Broadway and operetta; ragtime songs and early popular dance repertory; quartet, tenor, sentimental and novelty-song culture; march and patriotic repertory; songs about the automobile, airship and other markers of technological modernity; baseball and mass entertainment; opera on record and the Caruso recording boom; and historically accurate treatment of blackface/minstrelsy and racialized commercial repertory without presenting those traditions uncritically. Brazilian tracks require separation among Casa Edison and the first local recording industry, tango brasileiro, maxixe, choro, lundu, modinha, patriotic/civic song, carnival repertory, Santos-Dumont/aviation culture and the early careers of Bahiano, Eduardo das Neves, Patápio Silva and Ernesto Nazareth.

## Acceptance criteria

1. Ten per-year patch files cover all 60 identities exactly once.
2. No primary target remains in the strict generic-primary set.
3. Each row has a concise historical basis.
4. `python tools/audit_context_decade.py 1900 --validate-patches` passes.
5. 1900s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete.
6. Existing 1910s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green.
