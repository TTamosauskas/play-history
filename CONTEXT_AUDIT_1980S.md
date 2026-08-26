# Auditoria de Contexto — anos 1980

Escopo: todas as 185 entradas do catálogo datadas de 1980 a 1989.

## Princípio

O link **Contexto** é material didático de história da música. O primeiro alvo deve levar o estudante à linhagem que melhor explica a faixa — gênero, subgênero, cena, movimento ou tradição — em vez de reproduzir o guarda-chuva comercial em que a gravação circulou.

A classificação é feita **por faixa e por ano, não por artista**. Em obras híbridas, o primeiro alvo é a chave histórica mais informativa; o segundo preserva uma linhagem complementar ou funciona como fallback enciclopédico. A identidade de auditoria passa a ser `ano + artista + título`, o que preserva corretamente ocorrências repetidas no catálogo, como **Inocentes — Pânico em S.P.**, presente em 1982 e 1986.

Como nos ciclos posteriores, `Música pop`, `MPB` e `Rock` ficam bloqueados como contexto primário. `Música popular brasileira`, por extenso, é mantida em poucos casos em que a tradição da canção brasileira é realmente a chave mais defensável, sempre acompanhada de um segundo alvo mais específico quando isso acrescenta valor histórico.

## Resultado

- 185/185 entradas têm curadoria explícita nos shards `tools/patches/context_1980s_1980.json` … `context_1980s_1989.json`.
- 173/185 contextos primários mudam em relação ao catálogo anterior; apenas 12 já estavam defensáveis em essência.
- Antes da auditoria, a década concentrava 69 entradas em `MPB`, 56 em `Música pop`, 30 em `Rock brasileiro` e 4 em `Rock` como primeiro contexto.
- Faixa faltante, extra, duplicada, ano divergente, alvo incompleto ou contexto primário genérico proibido faz o build falhar.
- Com este ciclo, o contrato cumulativo cobre 604 entradas de 1980 a 2026.

## Exemplos do critério

- Bob Marley & The Wailers — **Three Little Birds** → `Reggae` → `Roots reggae`: corrige uma associação completamente alheia à história da gravação e recoloca a faixa na tradição jamaicana.
- Judas Priest — **Breaking the Law** → `Heavy metal` → `Nova onda do heavy metal britânico`; Iron Maiden — **The Trooper** recebe a mesma chave histórica ampla: a NWOBHM é indispensável para compreender a renovação do metal britânico no início da década.
- Motörhead — **Ace of Spades** → `Speed metal` → `Heavy metal`: evidencia a ponte entre heavy metal, punk e as linguagens que desembocariam no thrash.
- Joy Division — **Love Will Tear Us Apart** → `Post-punk` → `New wave`; The Smiths — **There Is a Light That Never Goes Out** → `Indie rock` → `Jangle pop`: diferencia linhagens britânicas que um rótulo genérico de rock esconderia.
- Duran Duran — **Hungry Like the Wolf** → `New romantic` → `New wave`; Soft Cell, Eurythmics, a-ha e Pet Shop Boys entram pela história do `Synth-pop`.
- Prince — **1999**, **Purple Rain** e **Kiss** priorizam `Minneapolis sound`, preservando a cena e o método de produção que articulam funk, rock, R&B e sintetizadores.
- Marvin Gaye — **Sexual Healing** → `Quiet storm` → `Contemporary R&B`; Whitney Houston — **I Wanna Dance with Somebody** → `Dance-pop` → `Contemporary R&B`: separa vertentes importantes do R&B de 1980s.
- N.W.A — **Straight Outta Compton** → `Gangsta rap` → `West Coast hip hop`; Public Enemy — **Fight the Power** → `Political hip hop` → `Golden age hip hop`: situa geografia, discurso e fase histórica do hip hop.
- Arrigo Barnabé, Itamar Assumpção, Rumo e Os Mulheres Negras priorizam `Vanguarda paulista`, em vez de serem achatados em MPB.
- Gang 90 & Absurdettes — **Perdidos na Selva** → `New wave` → `Rock brasileiro`: registra a emergência da new wave brasileira antes da consolidação do BRock.
- Legião Urbana — **Será** → `Post-punk` → `Rock brasileiro`; Capital Inicial, Plebe Rude e Mercenárias também são colocados em suas matrizes pós-punk/punk.
- Robson Jorge e Lincoln Olivetti — **Baila Comigo / Festa Brava** → `Boogie` → `Funk`: torna visível a história do boogie/funk brasileiro de estúdio.
- Olodum — **Faraó Divindade do Egito** → `Samba-reggae` → `Axé`: registra um marco da criação e gravação do samba-reggae em Salvador.
- Sarajane — **A Roda** → `Axé` → `Samba-reggae`: situa a faixa na formação da música baiana de massa que seria nomeada axé.
- Fausto Fawcett & Os Robôs Efêmeros — **Kátia Flávia, a Godiva do Irajá** → `Rap rock` → `Hip hop brasileiro`: preserva seu papel pioneiro na incorporação do rap à música brasileira gravada.
- Thaíde & DJ Hum — **Homens da Lei** → `Hip hop brasileiro` → `Old-school hip hop`: evidencia a consolidação autoral do rap paulista.
- **Melô da Mulher Feia** → `Funk carioca` → `Miami bass`: situa a nacionalização das linguagens dos bailes cariocas no fim da década.
- Elba Ramalho — **De Volta Pro Aconchego** → `Forró` → `Xote`; Luiz Gonzaga — **Asa Branca** → `Baião` → `Forró`: preserva matrizes nordestinas específicas em vez de tratá-las como MPB indiferenciada.
- Fundo de Quintal e Zeca Pagodinho priorizam `Pagode` → `Samba`, tornando visível a renovação do samba carioca ligada ao Cacique de Ramos.

## Leitura histórica da década

A curadoria torna visíveis os grandes eixos internacionais dos anos 1980: post-punk e new wave; synth-pop e New Romantic; indie/jangle e alternative rock; arena rock, glam metal, NWOBHM, speed/thrash e hardcore; pós-disco, boogie, funk e Minneapolis sound; quiet storm e contemporary R&B; a golden age do hip hop, gangsta rap e hip hop político; dance-pop, Hi-NRG, Latin pop e a cultura audiovisual da MTV.

No Brasil, a década deixa de ser tratada como uma massa de `MPB` ou `Rock brasileiro` e passa a distinguir Vanguarda Paulista; punk, hardcore e pós-punk de São Paulo e Brasília; rock gaúcho; new wave e synth-pop brasileiros; boogie, soul e funk brasileiros; pagode e partido-alto; samba-reggae e formação do axé; hip hop brasileiro e funk carioca; baião, forró, xote e frevo; Clube da Esquina, bossa nova, samba-canção e outras continuidades da canção brasileira.

## Evidência e fontes de controle

A auditoria foi confrontada com fontes editoriais, acadêmicas, enciclopédicas e primárias quando disponíveis. O campo `basis` de cada entrada registra a justificativa curatorial resumida.

Casos especialmente verificados neste ciclo incluem **Faraó Divindade do Egito** como marco inicial do samba-reggae gravado; **Kátia Flávia** no pioneirismo do rap brasileiro; **Melô da Mulher Feia** na nacionalização do Miami bass e formação do funk carioca; Robson Jorge/Lincoln Olivetti no boogie/funk brasileiro; Gang 90 na primeira onda da new wave nacional; Violeta de Outono na interseção de pós-punk e psicodelia; e **A Casa**, do repertório de *A Arca de Noé / Vinicius para Crianças*, como música infantil.

Os dez shards JSON anuais formam o registro canônico da auditoria da década; este documento explica o método.
