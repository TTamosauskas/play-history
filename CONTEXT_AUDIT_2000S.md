# Auditoria de Contexto — anos 2000

Escopo: todas as 107 faixas do catálogo datadas de 2000 a 2009.

## Princípio

O link **Contexto** é material didático de história da música. O primeiro alvo deve levar o estudante à linhagem que melhor explica a faixa — gênero, subgênero, cena, movimento ou tradição — e não ao guarda-chuva comercial em que ela apareceu.

A classificação é feita **por faixa, não por artista**. Em obras híbridas, o primeiro alvo é a chave histórica mais informativa; o segundo preserva uma linhagem complementar ou funciona como fallback enciclopédico.

Neste ciclo, `Música pop`, `MPB` e `Rock` são bloqueados como contexto primário, como nas décadas seguintes já auditadas. `Rock brasileiro` só é mantido como primário quando funciona como movimento/cena histórica e não existe uma chave de faixa mais específica e defensável.

## Resultado

- 107/107 faixas têm curadoria explícita nos shards `tools/patches/context_2000s_2000.json` … `context_2000s_2009.json`.
- 98/107 contextos primários mudam em relação à v6.10.0.
- A v6.10.0 tinha 45 faixas dos anos 2000 em `Música pop` e 31 em `MPB` como primeiro contexto.
- Nove primários já eram defensáveis: Capital Inicial — **Primeiros Erros (Chove)** (`Rock brasileiro`), João Gilberto — **Desde Que o Samba É Samba** (`Bossa nova`), Elza Soares — **A Carne** (`Samba`), Linkin Park — **Numb** (`Nu metal`), João Gilberto — **Wave** (`Bossa nova`), Beyoncé — **Irreplaceable** (`R&B contemporâneo`), Beyoncé — **Single Ladies** (`R&B contemporâneo`), Júpiter Maçã — **A Marchinha Psicótica de Dr. Soup** (`Rock psicodélico`) e Otto — **Crua** (`Manguebeat`).
- Faixa faltante, extra, duplicada, ano divergente, alvo incompleto ou contexto primário genérico proibido faz o build falhar.

## Exemplos do critério

- 50 Cent — **In da Club** → `Gangsta rap` → `East Coast hip hop`: AllMusic lista East Coast Rap, Hardcore Rap e Gangsta Rap para o single.
- The White Stripes — **Seven Nation Army** → `Garage rock revival` → `Indie rock`: AllMusic a trata como faixa-símbolo do garage rock revival e também alternative/indie rock.
- OutKast — **Hey Ya!** → `Hip hop alternativo` → `Electro-funk`: o contexto preserva o papel do OutKast no alternative rap e o hibridismo funk/electro da faixa.
- Usher — **Yeah!** → `Crunk` → `R&B contemporâneo`: exemplo canônico do encontro crunk/R&B que dominou o meio da década.
- Kanye West — **Stronger** → `Electro hip hop` → `Pop rap`: a amostra de Daft Punk e a produção eletrônica registram a aproximação rap/electro.
- The Black Eyed Peas — **I Gotta Feeling** → `Dance-pop` → `Electro house`: marca a passagem do pop de rádio para a era EDM no fim da década.
- Tribalistas — **Já Sei Namorar** → `Pop brasileiro` → `Música popular brasileira`: AllMusic classifica diretamente a faixa como Brazilian Pop/Brazilian Traditions/MPB.
- O Surto — **A Cera** → `Hardcore punk` → `Surf music`: a Folha descreveu a mistura do grupo como rock'n'roll, hardcore e surf music.
- Dallas Company — **Clima de Rodeio** → `Country` → `Sertanejo`: o Dicionário Cravo Albin registra a banda como country/sertanejo e a faixa como marco do country em português.
- Caetano Veloso — **Não Me Arrependo** → `Rock alternativo` → `Art rock`: a crítica contemporânea de *Cê* descreveu a canção como rock de matriz sessentista; o álbum usa formação de banda elétrica.
- Cansei de Ser Sexy — **Let's Make Love and Listen to Death from Above** → `Indie electronic` → `Electroclash`: AllMusic a classifica em indie electronic/indie rock, dentro da cena electro-indie da época.
- Restart — **Recomeçar** → `Happy rock` → `Emo pop`: a própria história do grupo registra Restart como nome central do fenômeno happy rock/bandas coloridas.

## Leitura histórica da década

A curadoria procura tornar visíveis alguns eixos centrais dos anos 2000: a consolidação regional do hip hop norte-americano (Gangsta rap, East Coast, Southern/Dirty South, Midwest), o garage rock revival e o indie, o post-grunge, nu metal e pop-punk, a ascensão do crunk, do electro e do dance-pop que desembocaria no EDM, o crossover global de Latin pop e de música de cinema indiana, além de cenas brasileiras como funk carioca/funk melody, forró universitário, country em português, Manguebeat pós-anos 1990, hip hop brasileiro, indie eletrônico e happy rock.

## Evidência e fontes de controle

A auditoria foi confrontada com fontes editoriais, enciclopédicas e primárias quando disponíveis. O campo `basis` de cada entrada registra a justificativa curatorial resumida.

Referências de controle usadas durante o ciclo incluem:

- AllMusic — 50 Cent, *In da Club*: East Coast Rap / Hardcore Rap / Gangsta Rap.
- AllMusic — The White Stripes, “Seven Nation Army”: Garage Rock Revival / Alternative-Indie Rock / Indie Rock / Blues-Rock.
- AllMusic — Eminem, “Stan”: Hardcore Rap.
- AllMusic — OutKast, “Hey Ya!”: Alternative Rap; a resenha de *Speakerboxxx/The Love Below* destaca soul e electro-funk.
- AllMusic — Tribalistas, “Já Sei Namorar”: Brazilian Pop / Brazilian Traditions / MPB.
- Folha de S.Paulo — O Surto no Rock in Rio 3: mistura de rock’n’roll, hardcore e surf music.
- Dicionário Cravo Albin — Dallas Country: banda country e sertaneja; “Clima de rodeio” descrita como marco do country em português.
- Folha de S.Paulo e AllMusic — Caetano Veloso, *Cê*: formação elétrica de rock e “Não Me Arrependo” descrita como rock de matriz sessentista.
- AllMusic — CSS, “Let’s Make Love and Listen to Death from Above”: Indie Electronic / Alternative-Indie Rock / Indie Rock.
- Folha de S.Paulo e Wikipédia — Restart/Cine e o fenômeno brasileiro “happy rock”/bandas coloridas.

Os dez shards JSON anuais formam o registro canônico da auditoria da década; este documento explica o método.