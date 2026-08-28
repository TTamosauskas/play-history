# Auditoria de Contexto — piloto pré-1900

Status: piloto em andamento.

## Objetivo

Levar o repertório anterior a 1900 ao mesmo nível de especificidade editorial já aplicado ao século XX e XXI. O primeiro alvo de `Contexto` deve apontar para a forma, subgênero ou tradição musical que melhor explica a obra; gênero amplo e movimento histórico entram como camadas complementares.

## Unidade de trabalho

A pesquisa passa a ser feita em pacotes de pelo menos 50 faixas. Quando uma década tiver menos de 50 músicas, décadas adjacentes são incorporadas até o pacote atingir o mínimo. Como a frente pré-1900 avança para trás a partir dos anos 1890, o agrupamento desta etapa acrescenta décadas anteriores.

O limite de 50 define a unidade editorial de pesquisa e revisão. Os arquivos canônicos podem continuar segmentados por ano/década para preservar rastreabilidade, enquanto inventário, pesquisa, revisão e aceite acontecem por pacote.

O comando do piloto é:

`python tools/audit_context_package.py 1890 --min-tracks 50 --direction backward --include-additions`

## Regra de precedência

1. forma ou subgênero específico;
2. gênero ou tradição musical;
3. movimento, escola ou cena histórica;
4. século ou década como fallback final.

A classificação permanece por obra/faixa. O repertório erudito usa forma musical quando ela é mais informativa que um rótulo estilístico amplo; repertório popular usa subgênero, prática ou cena quando documentados.

## Primeiras entradas pesquisadas

### Scott Joplin — Please Say You Will (1895)

Contexto: `Parlor song` → `Waltz`. A obra é uma canção para voz e piano de 1895 e a classificação preserva a tradição de parlor song antes do contexto formal complementar.

### Scott Joplin — Combination March (1896)

Contexto: `Marcha (música)` → `Ragtime`. A marcha funciona como forma principal e o ragtime como contexto de transição estilística.

### Arthur Collins — Hello! Ma Baby (1899)

Contexto: `Coon song` → `Tin Pan Alley` → `Ragtime`. A terminologia racializada é registrada como categoria histórica e exige enquadramento crítico explícito.

### Scott Joplin — Maple Leaf Rag (1899)

Contexto: `Classic rag` → `Ragtime`. A especificidade formal passa a preceder o gênero amplo.

## Critério de especificidade

O piloto usa quatro níveis: nível 3 = `form` ou `subgenre`; nível 2 = `genre` ou `tradition`; nível 1 = `movement`; nível 0 = `century` ou `decade`.

Cada faixa anterior a 1900 deve atingir pelo menos nível 2. Obras com forma/subgênero documentalmente identificável devem atingir nível 3.

## Fontes de controle

Library of Congress, IMSLP, RISM, catálogos de bibliotecas, MusicBrainz como apoio de identidade, literatura musicológica e fontes históricas digitalizadas formam a base de pesquisa. A Wikipédia permanece como destino do painel `Contexto`, enquanto a classificação editorial nasce de fontes mais fortes e específicas para cada período.

## Próximas etapas

Resolver automaticamente o primeiro pacote de pelo menos 50 faixas a partir dos anos 1890, revisar todas as identidades desse intervalo, criar a curadoria canônica por ano/década, conectar o intervalo ao pipeline de auditoria e bloquear regressões para contextos de baixa especificidade.
