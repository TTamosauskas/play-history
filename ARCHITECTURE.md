# Arquitetura

O Play History continua 100% estático e compatível com GitHub Pages. A fonte histórica do catálogo fica em `source/legacy.html`; `tools/build.py` valida a assinatura das 1.726 identidades, aplica os deltas curatoriais da v6.6.1 e gera `_site`.

O artefato de produção contém quatro módulos: `app.js` para estado, seleção e UI; `services.js` para artwork, Wikipédia, Sobre/Contexto, metadados e letras; `player.js` para resolução de mídia, buffer e progresso; `bootstrap.js` para eventos e YouTube IFrame API. O catálogo é entregue como JSON compacto e expandido pelo `assets/loader.js`.

`Sobre` resolve termos dirigidos de faixa e artista. `Contexto` resolve subgênero, gênero e movimento antes de qualquer período cronológico; repertório histórico usa século como fallback final quando aplicável.
