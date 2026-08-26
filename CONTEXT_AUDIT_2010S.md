# Auditoria de Contexto — anos 2010

Escopo: todas as 90 faixas do catálogo datadas de 2010 a 2019.

## Princípio

O link **Contexto** é material didático de história da música. O primeiro alvo deve situar a faixa numa linhagem reconhecível — gênero, subgênero, cena, movimento ou tradição — e evitar rótulos comerciais amplos quando existe uma categoria historicamente mais explicativa.

A classificação é feita **por faixa, não por artista**. Em obras híbridas, o primeiro alvo é a chave histórica mais útil; o segundo preserva uma linhagem complementar ou funciona como fallback enciclopédico.

Neste ciclo, `Música pop`, `MPB` e `Rock` são proibidos como contexto primário. O objetivo não é eliminar pop, MPB ou rock da história, e sim impedir que esses guarda-chuvas substituam categorias mais formativas.

## Resultado

- 90/90 faixas têm curadoria explícita em `tools/patches/context_2010s.json`.
- 86/90 contextos primários mudam em relação à v6.9.0.
- Apenas Elza Soares — **Mulher do Fim do Mundo** (`Samba`), BaianaSystem — **Playsom** (`Samba-reggae`), Elza Soares — **Banho** (`Samba`) e BaianaSystem — **Sulamericano** (`Samba-reggae`) já tinham um primeiro contexto considerado defensável.
- Nenhuma faixa de 2010–2019 pode voltar silenciosamente a `Música pop`, `MPB` ou `Rock` como contexto primário.
- A auditoria cobre exatamente todas as faixas da janela 2010–2019; faixa faltante, extra, duplicada, ano divergente ou alvo incompleto faz o build falhar.

## Exemplos do critério

- Adele — **Rolling in the Deep** → `Soul music` → `Pop soul`: a crítica e a discografia situam a faixa entre soul, gospel-blues e pop-soul.
- Katy Perry — **Teenage Dream** → `Power pop` → `Electropop`: a faixa é descrita explicitamente nesses dois estilos.
- Rihanna — **Only Girl (In the World)** → `Eurodance` → `Dance-pop`: registra a estética club/eurodance da virada EDM do pop.
- LMFAO — **Party Rock Anthem** → `Hip house` → `Electro house`: rap sobre house, mais informativo que “pop”.
- Michel Teló — **Ai Se Eu Te Pego** → `Sertanejo universitário` → `Sertanejo`: corrige a antiga classificação como MPB.
- Metá Metá — **Obatalá** e **São Jorge** → `Música afro-brasileira` → `Afrobeat`: preserva a matriz ritual afro-brasileira e a fusão com jazz/afrobeat.
- O Terno — **66** → `Indie rock` → `Garage rock`: situa a faixa na cena independente e no revival sessentista.
- Avicii — **Wake Me Up** → `Folktronica` → `EDM`: registra a fusão de folk/country acústico com música eletrônica de festival.
- Daft Punk — **Get Lucky** → `Música disco` → `Funk`: situa o revival disco-funk e a presença de Nile Rodgers.
- Mark Ronson feat. Bruno Mars — **Uptown Funk** → `Minneapolis sound` → `Funk`: aponta diretamente para a linhagem Prince/The Time.
- OMI — **Cheerleader (Felix Jaehn Remix)** → `Tropical house` → `Reggae fusion`: registra a função histórica do remix na consolidação do tropical house.
- Justin Bieber — **Sorry** → `Dancehall` → `Tropical house`: a produção usa dembow e linguagem caribenha.
- Major Lazer & DJ Snake feat. MØ — **Lean On** → `Moombahton` → `EDM`: coloca a faixa na história do híbrido electro house/reggaeton.
- Drake feat. Wizkid & Kyla — **One Dance** → `Afrobeats` → `Dancehall`: destaca a entrada do Afrobeats no mainstream global.
- Luis Fonsi & Daddy Yankee feat. Justin Bieber — **Despacito** → `Reggaeton` → `Latin pop`: trata o fenômeno como música urbana latina, não “pop”.
- Post Malone feat. 21 Savage — **Rockstar** → `Trap` → `Pop rap`: registra o domínio do trap nas paradas do fim da década.
- Duda Beat — **Bixinho** → `Brega pop` → `Indie pop`: preserva a linhagem brega/sofrência da nova cena pop brasileira.
- Lil Nas X feat. Billy Ray Cyrus — **Old Town Road** → `Country rap` → `Country trap`: caso central da recombinação entre hip hop e country.
- Pitty — **Te Conecta** → `Reggae rock` → `Dub`: segue a própria comunicação da gravadora sobre a virada reggae/dub da faixa.
- Marcelo Jeneci — **Pra Sonhar** e Tulipa Ruiz — **Efêmera** → `Nova MPB`: registra a geração paulistana do início da década como movimento histórico, com fallback enciclopédico mais amplo.
- Vitor Ramil — **Foi no Mês Que Vem** → `Estética do frio` → `Milonga`: prioriza o conceito estético formulado pelo próprio compositor para a música do extremo sul.
- Caetano Veloso & Gilberto Gil — **Andar com Fé** → `Reggae` → `Música afro-brasileira`: classifica a composição pela linguagem documentada da faixa, em vez de pela associação biográfica dos intérpretes à Tropicália.
- The Weeknd — **Blinding Lights** → `Synth-pop` → `New wave`: situa a estética oitentista que se tornaria uma das assinaturas do pop no início dos anos 2020.

## Evidência e fontes de controle

A auditoria foi confrontada com fontes primárias e editoriais, incluindo páginas oficiais de artistas e selos, AllMusic, Pitchfork, The Guardian, Apple Music, Bandcamp e imprensa musical brasileira.

Referências de controle usadas durante o ciclo:

- AllMusic — Adele, “Rolling in the Deep”: https://www.allmusic.com/song/rolling-in-the-deep-mt0040297367
- Pitchfork — Rihanna, “Only Girl (In the World)”: https://pitchfork.com/reviews/tracks/12055-only-girl-in-the-world/
- The Guardian — Metá Metá: https://www.theguardian.com/music/2014/dec/02/meta-meta-review-brazilian-fusion
- Monkeybuzz — O Terno, *66*: https://monkeybuzz.com.br/resenhas/albuns/o-terno-66/
- Música Instantânea — Duda Beat, *Sinto Muito*: https://musicainstantanea.com.br/critica-duda-beat-sinto-muito/
- Pitchfork — Elza Soares, “Banho”: https://pitchfork.com/reviews/tracks/elza-soares-banho
- Deckdisc — Pitty, “Te Conecta”: https://www.deckdisc.com.br/discos/pitty-te-conecta/
- Groovie Records/Bandcamp — The Blobs, “Murder”: https://groovierecords.bandcamp.com/track/the-blobs-murder
- Globoplay — geração chamada “Nova MPB” (Tulipa Ruiz, Marcelo Jeneci e outros): https://globoplay.globo.com/v/1887412/
- Wikipédia — *Um Banda Um* / “Andar com Fé” e a forte influência de reggae: https://pt.wikipedia.org/wiki/Um_Banda_Um

O arquivo JSON é o registro canônico da auditoria; este documento explica o método. Os ciclos seguintes devem permanecer separados por década para manter as decisões rastreáveis e revisáveis.
