# Contexto Audit — 1940s

Status: complete for v6.17.0.

## Inventory

- Total catalog tracks: 65
- Initial generic primary: 49
- Initial specific-but-reviewable primary: 16
- Coverage by year: 1940=6, 1941=7, 1942=8, 1943=6, 1944=6, 1945=6, 1946=9, 1947=5, 1948=5, 1949=7
- Final coverage: 65/65 exact identities curated
- Distinct final primary contexts: 23

## Editorial result

Every 1940–1949 track now has an exact year+artist+title Contexto entry with a concise historical basis. No primary target remains in the strict generic-primary set. Broad labels such as Samba or Rhythm and blues are retained only as secondary context where useful.

The decade is represented through historically specific contexts including swing, big band, traditional pop, crooner culture, jump blues, wartime popular song, bolero crossover, samba-exaltação, the Brazilian Era do Rádio, samba-canção, carnival, film music, honky-tonk, calypso, twelve-bar blues, choro, baião, Dixieland, western swing, Christmas music and the emergence of rock and roll.

Notable corrections include `Brasil Pandeiro` as samba-exaltação; `Green Eyes` as a Cuban bolero translated into the big-band market; `Copacabana` as a landmark of the new samba-canção and a precursor to bossa nova; the 1946 `Baião` recording as the first recorded baião; `The Fat Man` as an early rock-and-roll/R&B landmark; and `Saturday Night Fish Fry` as jump blues at the threshold of rock and roll.

## Structural enforcement

1. Ten per-year patch files cover all 65 identities exactly once.
2. `tools/audit_context_decade.py 1940 --validate-patches` passes with no generic primary.
3. 1940s is wired into `tools/build.py` `AUDIT_SPECS` and the public runtime.
4. The public version/cache key is v6.17.0.
5. CI permanently validates 1940s, 1950s, 1960s and 1970s before the modular build.
6. Generated JavaScript, smoke runtime and curated-build verification pass on the final clean branch.
