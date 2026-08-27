# Contexto Audit — 1950s

Status: inventory complete; curation in progress.

## Inventory

- Total catalog tracks: 84
- Generic current primary: 49
- Specific-but-reviewable current primary: 35
- Coverage by year: 1950=10, 1951=7, 1952=4, 1953=4, 1954=7, 1955=10, 1956=10, 1957=11, 1958=9, 1959=12

## Editorial bar

Every 1950–1959 track must receive an exact year+artist+title Contexto entry. The primary link must explain why the recording matters historically rather than collapse it into broad taxonomy such as Música popular, Música pop, Rock, Blues or Samba.

Priority contexts for this decade include the emergence and crossover of rock and roll; rhythm and blues; doo-wop; rockabilly; Chicago/electric blues; gospel-to-soul transitions; country/honky-tonk; traditional pop and crooner culture; recording technology; baião, forró, choro and samba-canção; radio-era popular song; and the formation of bossa nova.

## Acceptance criteria

1. Ten per-year patch files cover all 84 identities exactly once.
2. No primary target remains in the strict generic-primary set.
3. Each row has a concise historical basis.
4. `tools/audit_context_decade.py 1950 --validate-patches` passes.
5. 1950s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete.
6. Existing 1960s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green.
