# Contexto Audit — 1910s

Status: inventory complete; curation in progress.

## Inventory

- Total catalog tracks: 61
- Generic current primary: 54
- Specific-but-reviewable current primary: 7
- Coverage by year: 1910=5, 1911=7, 1912=6, 1913=8, 1914=7, 1915=7, 1916=4, 1917=6, 1918=6, 1919=5

## Editorial bar

Every 1910–1919 track must receive an exact year+artist+title Contexto entry. The primary link must explain why the recording matters historically rather than collapse it into broad taxonomy such as Música popular, Jazz, Blues or Samba.

Priority contexts for this decade include ragtime and Tin Pan Alley; vaudeville and early musical theatre; quartet, tenor and sentimental-song culture in the acoustic-recording era; Irish-American popular song; World War I patriotic, military and anti-war repertoire; the transition from ragtime-era dance music to the first commercially recorded jazz; and the emergence of early jazz standards. Brazilian tracks require separation among the Casa Edison recording scene, choro, carnival song, sertanejo/sertão imagery, early urban popular song, the first commercially recorded samba and the pre-radio foundations of the recording industry.

## Acceptance criteria

1. Ten per-year patch files cover all 61 identities exactly once.
2. No primary target remains in the strict generic-primary set.
3. Each row has a concise historical basis.
4. `python tools/audit_context_decade.py 1910 --validate-patches` passes.
5. 1910s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete.
6. Existing 1920s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green.
