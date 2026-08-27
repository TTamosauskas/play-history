# Contexto Audit — 1940s

Status: inventory complete; curation in progress.

## Inventory

- Total catalog tracks: 65
- Generic current primary: 49
- Specific-but-reviewable current primary: 16
- Coverage by year: 1940=6, 1941=7, 1942=8, 1943=6, 1944=6, 1945=6, 1946=9, 1947=5, 1948=5, 1949=7

## Editorial bar

Every 1940–1949 track must receive an exact year+artist+title Contexto entry. The primary link must explain why the recording matters historically rather than collapse it into broad taxonomy such as Música popular, Jazz, Samba, Rock, Blues or Música country.

Priority contexts for this decade include swing and big-band culture; crooners and traditional pop; wartime and postwar popular song; vocal groups; jump blues and early rhythm and blues; New Orleans R&B and the prehistory of rock and roll; honky-tonk and western swing; film and radio song; the Brazilian Era do Rádio; samba-canção, choro, marchinha, baião and the national circulation of northeastern repertoire; and historically specific cultural or technological contexts where they better explain a recording than genre alone.

## Acceptance criteria

1. Ten per-year patch files cover all 65 identities exactly once.
2. No primary target remains in the strict generic-primary set.
3. Each row has a concise historical basis.
4. `tools/audit_context_decade.py 1940 --validate-patches` passes.
5. 1940s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete.
6. Existing 1950s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green.
