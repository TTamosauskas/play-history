# Auditoria de Contexto — anos 1890

Status: piloto em andamento.

## Objetivo

Levar o repertório anterior a 1900 ao mesmo nível de especificidade editorial já aplicado ao século XX e XXI. O primeiro alvo de `Contexto` deve apontar para a forma, subgênero ou tradição musical que melhor explica a obra; gênero amplo e movimento histórico entram como camadas complementares.

## Regra de precedência do piloto

1. forma ou subgênero específico;
2. gênero ou tradição musical;
3. movimento, escola ou cena histórica;
4. século ou década como fallback final.

A classificação permanece por obra/faixa. O repertório erudito usa forma musical quando ela é mais informativa que um rótulo estilístico amplo; repertório popular usa subgênero, prática ou cena quando documentados.

## Primeiras entradas pesquisadas

### Scott Joplin — Please Say You Will (1895)

Contexto atual: `Parlor song`.

Direção: manter `Parlor song` como alvo primário e acrescentar `Waltz` como alvo complementar quando houver artigo enciclopédico adequado. A obra é uma canção para voz e piano de 1895; fontes especializadas a descrevem como uma das canções sentimentais/valsa de Joplin anteriores ao ragtime maduro.

### Scott Joplin — Combination March (1896)

Contexto atual: `Marcha (música)` → `Ragtime`.

Direção: tratar `Marcha` como forma principal; `Ragtime` permanece como contexto de transição estilística, e não como substituto da forma da obra. O catálogo deve distinguir forma musical de movimento/período.

### Arthur Collins — Hello! Ma Baby (1899)

Contexto atual: `Tin Pan Alley` → `Ragtime`.

Direção: pesquisar e testar `Coon song` como subgênero histórico primário, com `Tin Pan Alley` e `Ragtime` como contexto complementar. A terminologia é historicamente ofensiva e deve ser apresentada de maneira explicitamente histórica e crítica, seguindo o padrão já usado na auditoria dos anos 1900 para repertório racializado.

### Scott Joplin — Maple Leaf Rag (1899)

Contexto atual: `Ragtime`.

Direção: elevar para `Classic rag`/`classic piano rag` quando existir destino enciclopédico estável; `Ragtime` permanece como fallback. A Library of Congress usa `Maple Leaf Rag` como exemplo central da forma classic rag.

## Critério de especificidade

O piloto usará quatro níveis: nível 3 = `form` ou `subgenre`; nível 2 = `genre` ou `tradition`; nível 1 = `movement`; nível 0 = `century` ou `decade`.

Cada faixa anterior a 1900 deve atingir pelo menos nível 2. Obras com forma/subgênero documentalmente identificável devem atingir nível 3.

## Fontes de controle do piloto

- Library of Congress — coleção Ragtime / Classic Rag e registros históricos de áudio;
- IMSLP — forma, instrumentação, publicação e catálogo de obras;
- RISM e catálogos de bibliotecas para repertório erudito quando aplicável;
- MusicBrainz como apoio de identidade de obra/gravação;
- literatura musicológica e fontes históricas digitalizadas para terminologia de gênero/subgênero;
- Wikipédia como destino do painel `Contexto`, e não como única autoridade de classificação.

## Próximas etapas

Gerar inventário completo 1890–1899 da base legada, revisar cada identidade, criar shards anuais `context_1890s_<ano>.json`, adicionar a década aos `AUDIT_SPECS`, validar cobertura exata e bloquear regressões para contextos de baixa especificidade.
