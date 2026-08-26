# Auditoria de Contexto — anos 2020

Escopo: todas as 63 faixas do catálogo datadas de 2020 a 2026.

## Princípio

O link **Contexto** é material didático de história da música. Seu primeiro alvo deve situar a faixa numa linhagem musical reconhecível — gênero, subgênero, cena, movimento ou tradição — e não apenas no mercado amplo em que ela circulou.

A classificação é feita **por faixa, não por artista**. Em obras híbridas, o primeiro alvo é a chave histórica mais informativa; o segundo alvo preserva uma linhagem complementar ou funciona como fallback enciclopédico.

Neste ciclo, `Música pop`, `MPB` e `Rock` são considerados rótulos primários genéricos demais quando existe uma categoria mais explicativa. O build recusa esses três termos como contexto primário nas faixas auditadas de 2020–2026.

## Resultado

- 63/63 faixas têm curadoria explícita em `tools/patches/context_2020s.json`.
- 61/63 contextos primários mudam em relação à v6.8.1.
- Apenas Sepultura — **Isolation** (`Thrash metal`) e SZA — **Kill Bill** (`R&B contemporâneo`) já tinham um primeiro contexto adequado.
- Nenhuma faixa de 2020–2026 pode voltar silenciosamente a `Música pop`, `MPB` ou `Rock` como contexto primário.
- O arquivo de auditoria precisa cobrir exatamente todas as faixas da janela 2020–2026; faixa faltante, extra, duplicada, ano divergente ou alvo incompleto faz o build falhar.

## Exemplos do critério

- BTS — **Dynamite** → `K-pop` → `Música disco`: preserva tanto o fenômeno histórico do K-pop global quanto a linguagem disco-pop da gravação.
- Dua Lipa — **Levitating** → `Nu-disco` → `Música disco`: situa a faixa no revival disco dos anos 2020.
- Mateus Aleluia — **Olorum** → `Música afro-brasileira` → `Afoxé`: substitui o guarda-chuva MPB pela matriz cultural que explica a obra.
- Bad Bunny — **Tití Me Preguntó** → `Dembow` → `Latin trap`: destaca a matriz dominicana e sua relação com a música urbana latina.
- Burna Boy — **Last Last** e Rema — **Calm Down** → `Afrobeats`: registra a internacionalização do gênero africano na década.
- DENNIS & MC Kevin o Chris — **Tá OK** → `Funk carioca`: recoloca a faixa na história do baile funk, não em MPB.
- Banda AL9 — **Chama De Amor** → `Jovem Guarda` → `Power pop`: prioriza a referência histórica deliberada do projeto.
- Tyla — **Water** → `Amapiano` → `Afrobeats`: destaca a circulação global da linguagem sul-africana e o log drum característico.
- Kendrick Lamar — **Not Like Us** → `Hip hop da Costa Oeste` → `Hyphy`: preserva a geografia e a linhagem regional essenciais ao sentido da faixa.
- Sabrina Carpenter — **Espresso** → `Nu-disco` → `Música disco`: a crítica da Pitchfork descreve explicitamente a gravação como nu-disco.
- Shaboozey — **A Bar Song (Tipsy)** → `Country rap` → `Country pop`: registra a convergência histórica de country e hip hop.
- Jota.pê — **Até Outro Dia** → `Reggae` → `Música do Brasil`: segue a descrição do próprio artista do reggae como ponto de partida, sem apagar as referências brasileiras e africanas.

## Evidência e fontes

A auditoria foi confrontada com fontes primárias e editoriais, incluindo materiais de artistas/selos, Grammy, Pitchfork, Billboard, Apple Music, Bandcamp e imprensa musical especializada. O campo `basis` de cada entrada registra a justificativa curatorial resumida.

Referências de controle usadas durante o ciclo incluem:

- Pitchfork, Sabrina Carpenter — “Espresso”: https://pitchfork.com/reviews/tracks/sabrina-carpenter-espresso/
- Pitchfork, Miley Cyrus — “Flowers”: https://pitchfork.com/reviews/tracks/miley-cyrus-flowers/
- Pitchfork, Doja Cat — *Scarlet*: https://pitchfork.com/reviews/albums/doja-cat-scarlet/
- Liniker — *CAJU* (Bandcamp): https://liniker.bandcamp.com/album/caju
- Apple Music — Os Garotin: https://music.apple.com/br/artist/os-garotin/1694153633

O arquivo JSON é o registro canônico da auditoria; este documento explica o método. Os ciclos seguintes devem usar arquivos separados por década para manter as decisões rastreáveis e revisáveis.
