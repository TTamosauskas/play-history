# Contexto Audit — 1930s

Status: inventory complete; curation in progress.

## Inventory

- Total catalog tracks: 66
- Generic current primary: 65
- Specific-but-reviewable current primary: 1
- Coverage by year: 1930=9, 1931=8, 1932=5, 1933=6, 1934=3, 1935=7, 1936=6, 1937=8, 1938=6, 1939=8

## Editorial bar

Every 1930–1939 track must receive an exact year+artist+title Contexto entry. The primary link must explain why the recording matters historically rather than collapse it into broad taxonomy such as Música popular, Jazz or Samba.

Priority contexts for this decade include swing and the rise of big-band culture; crooners and microphone-era traditional pop; vocal jazz and close-harmony groups; Broadway and film song; the Great Depression; Cuban rumba and Latin crossover; stride, Dixieland and Kansas City jazz; landmark improvisation; the Brazilian Era do Rádio; urban samba, samba-choro, choro, marchinha, valsa-canção and seresta; recording technology and samba percussion; carnival culture; Estado Novo nationalism and samba-exaltação; and the construction of Carmen Miranda's baiana image.

## Acceptance criteria

1. Ten per-year patch files cover all 66 identities exactly once.
2. No primary target remains in the strict generic-primary set.
3. Each row has a concise historical basis.
4. `python tools/audit_context_decade.py 1930 --validate-patches` passes.
5. 1930s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete.
6. Existing 1940s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green.
