# Contexto Audit — 1920s

Status: inventory complete; curation in progress.

## Inventory

- Total catalog tracks: 62
- Generic current primary: 61
- Specific-but-reviewable current primary: 1
- Coverage by year: 1920=6, 1921=6, 1922=3, 1923=5, 1924=6, 1925=6, 1926=5, 1927=11, 1928=7, 1929=7

## Editorial bar

Every 1920–1929 track must receive an exact year+artist+title Contexto entry. The primary link must explain why the recording matters historically rather than collapse it into broad taxonomy such as Música popular, Jazz, Blues or Samba.

Priority contexts for this decade include the Jazz Age; race records and classic female blues; New Orleans and Chicago jazz; stride piano and landmark improvisation; dance crazes such as Charleston and black bottom; Tin Pan Alley, Broadway and early film song; the rise of electrical recording and microphone-era singing; the commercial formation of country music; Harlem-era Black popular culture; and, in Brazil, the recording industry around samba and choro, teatro de revista, carnival song, the transition toward the Estácio samba style, and the consolidation of urban popular song on record and radio.

## Acceptance criteria

1. Ten per-year patch files cover all 62 identities exactly once.
2. No primary target remains in the strict generic-primary set.
3. Each row has a concise historical basis.
4. `python tools/audit_context_decade.py 1920 --validate-patches` passes.
5. 1920s is wired into `tools/build.py` and `assets/catalog-runtime.js` only after curation is complete.
6. Existing 1930s+ audits, modular build, JavaScript checks, smoke test and curated-build verification remain green.
