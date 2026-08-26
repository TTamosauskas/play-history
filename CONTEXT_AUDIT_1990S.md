# Auditoria de Contexto — anos 1990

Escopo: todas as 159 faixas do catálogo datadas de 1990 a 1999.

## Princípio

O link **Contexto** é material didático de história da música. O primeiro alvo deve levar o estudante à linhagem que melhor explica a faixa — gênero, subgênero, cena, movimento ou tradição — em vez de reproduzir o guarda-chuva comercial em que a gravação circulou.

A classificação é feita **por faixa, não por artista**. Em obras híbridas, o primeiro alvo é a chave histórica mais informativa; o segundo preserva uma linhagem complementar ou funciona como fallback enciclopédico.

Como nos ciclos posteriores já auditados, `Música pop`, `MPB` e `Rock` ficam bloqueados como contexto primário. Categorias amplas só são preservadas quando são historicamente defensáveis para a própria faixa; por exemplo, `Música popular brasileira` em Djavan — **Oceano** aparece por extenso e com um segundo alvo mais específico (`Jazz brasileiro`).

## Resultado

- 159/159 faixas têm curadoria explícita nos shards `tools/patches/context_1990s_1990.json` … `context_1990s_1999.json`.
- 143/159 contextos primários mudam em relação à v6.11.0.
- A v6.11.0 tinha 63 faixas dos anos 1990 em `MPB` e 58 em `Música pop` como primeiro contexto.
- Apenas 16 primários anteriores foram considerados defensáveis e mantidos em essência: Depeche Mode — **Enjoy the Silence** (`Synth-pop`), Sepultura — **Arise** (`Thrash metal`), Legião Urbana — **Teatro dos Vampiros** (`Rock brasileiro`), Daniela Mercury — **O Canto da Cidade** (`Axé`), Sepultura — **Refuse/Resist** (`Thrash metal`), Itamar Assumpção — **Quem É Cover de Quem** (`Vanguarda paulista`), The Cranberries — **Zombie** (`Rock alternativo`), Mundo Livre S/A — **Livre Iniciativa** (`Manguebeat`), Cidade Negra — **Onde Você Mora?** (`Reggae`), Júpiter Maçã — **Lugar do Caralho** (`Rock psicodélico`), Paulinho da Viola — **Bebadosamba** (`Samba`), Daniela Mercury — **À Primeira Vista** (`Axé`), Titãs — **Pra Dizer Adeus** (`Rock brasileiro`), Mundo Livre S/A — **Meu Esquema** (`Manguebeat`), Otto — **Bob** (`Manguebeat`) e Cidade Negra — **A Estrada** (`Reggae`).
- Faixa faltante, extra, duplicada, ano divergente, alvo incompleto ou contexto primário genérico proibido faz o build falhar.

## Exemplos do critério

- Nirvana — **Smells Like Teen Spirit** → `Grunge` → `Rock alternativo`: situa a faixa no movimento de Seattle que redefiniu o rock mainstream no início da década.
- Oasis — **Wonderwall** → `Britpop` → `Rock alternativo`: prioriza a cena britânica específica, em vez de “rock” ou “pop”.
- Warren G feat. Nate Dogg — **Regulate** e 2Pac feat. Dr. Dre — **California Love** → `G-funk` → `West Coast hip hop`: preserva a geografia e a linguagem sonora essenciais ao rap da Costa Oeste.
- Coolio feat. L.V. — **Gangsta's Paradise** → `Gangsta rap` → `West Coast hip hop`: tira a faixa do pop genérico e a recoloca em sua linhagem de hip hop.
- Lauryn Hill — **Doo Wop (That Thing)** → `Neo soul` → `Hip hop soul`: registra a convergência R&B/hip hop que marcou o fim da década.
- Haddaway — **What Is Love** → `Eurodance` → `House music`: situa a canção na cultura de pista europeia dos anos 1990.
- Britney Spears — **...Baby One More Time** → `Teen pop` → `Dance-pop`: registra a retomada do teen pop no final da década.
- Angra — **Carry On** → `Power metal` → `Metal progressivo`: corrige a antiga classificação como MPB.
- Raça Negra — **Cheia de Manias** → `Pagode romântico` → `Samba`: reconhece o pagode romântico paulista como fenômeno histórico próprio.
- **Rap da Felicidade** → `Funk carioca` → `Hip hop brasileiro`: recoloca o clássico de Cidinho & Doca na história do funk do Rio de Janeiro.
- Fernanda Abreu — **Rio 40 Graus** → `Samba-funk` → `Funk carioca`: registra a ponte deliberada entre samba, funk e rap urbano carioca.
- Chico Science e Nação Zumbi — **A Praieira** / **Maracatu Atômico** → `Manguebeat` → `Maracatu`: prioriza o movimento recifense e sua matriz rítmica.
- Vitor Ramil — **Ramilonga** → `Estética do frio` → `Milonga`: trata o conceito estético regional como chave histórica, não como MPB genérica.
- Claudinho & Buchecha — **Só Love** → `Funk melody` → `Funk carioca`: diferencia a vertente romântica/melódica dentro do funk carioca.
- É O Tchan — **Pau Que Nasce Torto / Melô do Tchan** e As Meninas — **Xibom Bombom** → `Pagode baiano`: torna visível a cena baiana que o rótulo MPB escondia.

## Leitura histórica da década

A curadoria torna visíveis alguns dos principais eixos dos anos 1990: grunge e alternative rock; Britpop; G-funk, gangsta rap e hip hop regional; contemporary R&B, new jack swing, hip hop soul e neo soul; house, Eurodance e alternative dance; teen pop e Latin pop; power metal e a transformação do metal extremo. No Brasil, distingue sertanejo romântico e de raiz, pagode romântico, pagode baiano, axé e samba-reggae, manguebeat, funk carioca e funk melody, hip hop brasileiro, samba-funk, reggae-rock, rock gaúcho, skate punk e a Estética do Frio.

## Evidência e fontes de controle

A auditoria foi confrontada com fontes editoriais, acadêmicas, enciclopédicas e primárias quando disponíveis. O campo `basis` de cada entrada registra a justificativa curatorial resumida.

Referências de controle usadas durante o ciclo incluem materiais de AllMusic, Folha de S.Paulo, páginas oficiais de artistas, Dicionário Cravo Albin e estudos acadêmicos. Casos especialmente verificados incluem Fernanda Abreu — **Rio 40 Graus** (mistura declarada de funk, rap e samba), Vitor Ramil — **Ramilonga** e a **Estética do Frio**, Raça Negra e a história do pagode romântico, É o Tchan/Raça Pura e o pagode baiano, **Rap da Felicidade** como marco do funk carioca, e Chico Science/Mundo Livre S/A no Manguebeat.

Os dez shards JSON anuais formam o registro canônico da auditoria da década; este documento explica o método.
