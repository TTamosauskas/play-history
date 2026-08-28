# Auditoria de Contexto — pacote 1810–1899

Status: pacote concluído e pronto para aceite.

## Objetivo

Levar o repertório anterior a 1900 ao mesmo nível de especificidade editorial já aplicado ao século XX e XXI. O primeiro alvo de `Contexto` aponta para a forma, subgênero ou tradição musical que melhor explica a obra; gênero amplo e movimento histórico entram como camadas complementares.

## Unidade de trabalho

A pesquisa passa a ser feita em pacotes de pelo menos 50 faixas. Quando uma década tiver menos de 50 músicas, décadas adjacentes são incorporadas até o pacote atingir o mínimo. Como a frente pré-1900 avança para trás a partir dos anos 1890, o agrupamento acrescenta décadas anteriores.

O primeiro agrupamento automático resolveu o intervalo **1810–1899**, com **56 faixas**. A distribuição é: 1810s=7, 1820s=3, 1830s=6, 1840s=8, 1850s=4, 1860s=3, 1870s=7, 1880s=4 e 1890s=14.

O diagnóstico inicial registrava 51 faixas em especificidade nível 1, duas em nível 2 e três em nível 3. Após a curadoria completa, o pacote passou para **46 faixas em nível 2 e 10 em nível 3**. Todas as 56 identidades agora atingem a especificidade mínima editorial L2.

O limite de 50 define a unidade editorial de pesquisa e revisão. Os arquivos canônicos permanecem segmentados por origem para preservar rastreabilidade, enquanto inventário, pesquisa, revisão e aceite acontecem por pacote.

O comando de aceite do pacote é:

`python tools/audit_context_package.py 1890 --min-tracks 50 --direction backward --include-additions --require-specificity 2`

## Regra de precedência

1. forma ou subgênero específico;
2. gênero ou tradição musical;
3. movimento, escola ou cena histórica;
4. século ou década como fallback final.

A classificação permanece por obra/faixa. O repertório erudito usa forma musical quando ela é mais informativa que um rótulo estilístico amplo; repertório popular usa subgênero, prática ou cena quando documentados.

## Resultado da curadoria

A maior transformação ocorreu nas 51 faixas que antes apresentavam movimentos amplos como `Música do romantismo` ou `Classicismo` como primeiro alvo. O pacote agora prioriza categorias como `Concerto para clarinete`, `Concerto para piano`, `Cavatina`, `Tema e variações`, `Parlor song`, `Música programática`, `Mazurca`, `Noturno`, `Balada`, `Marcha fúnebre`, `Abertura`, `Ária`, `Musikdrama`, `Poema sinfônico`, `Suíte`, `Música incidental`, `Abertura de concerto`, `Canção revolucionária`, `Arabesque`, `Dança de caráter`, `Valsa` e `Scherzo`.

Os casos racializados do fim do século XIX usam terminologia histórica com enquadramento crítico explícito. `The Laughing Song` e `Hello! Ma Baby`, por exemplo, recebem o subgênero histórico correspondente como primeiro alvo e mantêm vaudeville, Tin Pan Alley ou ragtime como camadas de contexto.

A adição de 1839 de Chopin também passou a priorizar `Marcha fúnebre`, seguida por `Sonata para piano` e `Romantismo na música`, alinhando a faixa ao mesmo princípio forma-primeiro aplicado ao restante do lote.

## Critério de especificidade

O auditor usa quatro níveis: nível 3 = `form` ou `subgenre`; nível 2 = `genre` ou `tradition`; nível 1 = `movement`; nível 0 = `century` ou `decade`.

Cada faixa anterior a 1900 deve atingir pelo menos nível 2. Obras com forma ou subgênero documentalmente identificável avançam para nível 3 quando o destino enciclopédico é estável e adequado.

## Fontes de controle

Library of Congress, IMSLP, RISM, catálogos de bibliotecas, MusicBrainz como apoio de identidade, literatura musicológica, instituições orquestrais e operísticas e fontes históricas digitalizadas formam a base de pesquisa. A Wikipédia permanece como destino do painel `Contexto`, enquanto a classificação editorial nasce de fontes mais fortes e específicas para cada período.

## Aceite e continuidade

O workflow do pacote executa a regra de agrupamento mínimo de 50 faixas e agora também exige especificidade mínima L2. O pacote 1810–1899 atende aos dois critérios. Após a incorporação deste lote, a próxima frente parte dos anos 1800 e agrega décadas anteriores até formar o próximo pacote de pelo menos 50 músicas.
