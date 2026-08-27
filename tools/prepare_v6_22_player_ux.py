#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def file(path):
    return ROOT / path


def replace_once(path, old, new):
    target = file(path)
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"marker not found in {path}: {old[:80]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def replace_between(path, start, end, replacement):
    target = file(path)
    text = target.read_text(encoding="utf-8")
    a = text.find(start)
    b = text.find(end, a + len(start))
    if a < 0 or b < 0:
        raise SystemExit(f"range markers not found in {path}")
    target.write_text(text[:a] + replacement + text[b:], encoding="utf-8")


# Version/cache keys.
replace_once("tools/build.py", "VERSION='6.21.0'", "VERSION='6.22.0'")
replace_once("assets/catalog-runtime.js", "/* Play History v6.21.0", "/* Play History v6.22.0")
replace_once("assets/catalog-runtime.js", "const VERSION = '6.21.0';", "const VERSION = '6.22.0';")
replace_once("assets/catalog-runtime.js", "services: 8,", "services: 9,")

index = file("index.html")
text = index.read_text(encoding="utf-8")
text = text.replace("6.21.0", "6.22.0")
old_links = '''      <button class="track-link" id="infoLink" type="button" hidden>Sobre</button>\n      <button class="track-link" id="contextLink" type="button" hidden>Contexto</button>\n      <a class="track-link" id="albumLink" hidden target="_blank" rel="noopener noreferrer" title="Abrir álbum no YouTube Music">Álbum</a>\n      <button class="track-link" id="lyricsLink" type="button" hidden>Letra</button>'''
new_links = '''      <button class="track-link" id="contextLink" type="button" hidden>Contexto</button>\n      <a class="track-link" id="albumLink" hidden target="_blank" rel="noopener noreferrer" title="Abrir álbum no YouTube Music">Álbum</a>\n      <button class="track-link" id="lyricsLink" type="button" hidden>Letra</button>\n      <a class="track-link" id="appreciationLink" hidden target="_blank" rel="noopener noreferrer">Apreciação</a>'''
if old_links not in text:
    raise SystemExit("track-links marker not found in index.html")
index.write_text(text.replace(old_links, new_links, 1), encoding="utf-8")

# DOM references and resolution cache generation.
replace_once(
    "assets/source/app/01.part",
    'const infoLink = document.getElementById("infoLink");\nconst contextLink = document.getElementById("contextLink");',
    'const contextLink = document.getElementById("contextLink");'
)
replace_once(
    "assets/source/app/01.part",
    'const lyricsLink = document.getElementById("lyricsLink");',
    'const lyricsLink = document.getElementById("lyricsLink");\nconst appreciationLink = document.getElementById("appreciationLink");'
)
replace_once("assets/source/app/01.part", 'const YOUTUBE_RESOLUTION_STORAGE_PREFIX = "player-musical-yt-v47:";', 'const YOUTUBE_RESOLUTION_STORAGE_PREFIX = "player-musical-yt-v48:";')
replace_once("assets/source/app/01.part", 'Player Musical 800-2026 v6.7.0', 'Player Musical 800-2026 v6.22.0')

# Reject YouTube's 120x90 unavailable-video placeholder and proactively recover the ID.
replace_once(
    "assets/source/services/01.part",
    '''    artImg.onload = () => {\n      if (token !== artworkRenderToken) return;\n      art.classList.add("has-image");\n    };''',
    '''    artImg.onload = () => {\n      if (token !== artworkRenderToken) return;\n      const source = String(artImg.currentSrc || artImg.src || "");\n      const youtubeUnavailablePlaceholder = /(?:^|\\/)i\\.ytimg\\.com\\//i.test(source)\n        && artImg.naturalWidth <= 160\n        && artImg.naturalHeight <= 120;\n      if (youtubeUnavailablePlaceholder){\n        art.classList.remove("has-image");\n        const failedId = track.youtubeId || extractYoutubeVideoId(source);\n        if (failedId && !failedYoutubeIds.has(failedId)){\n          failedYoutubeIds.add(failedId);\n          clearCachedYoutubeIdForTrack(track);\n          artworkCache.delete(trackIdentity(track));\n          if (typeof recoverTrackVideo === "function"){\n            recoverTrackVideo(track, failedId).then(replacementId => {\n              if (token !== artworkRenderToken || !replacementId) return;\n              artworkCache.delete(trackIdentity(track));\n              renderArtwork(track);\n            }).catch(() => {});\n          }\n        }\n        loadNextCandidate();\n        return;\n      }\n      art.classList.add("has-image");\n    };'''
)

# On playback recovery, try alternate query formulations instead of stopping after the first wave.
player02 = file("assets/source/player/02.part")
text = player02.read_text(encoding="utf-8")
start = text.find("  const task = (async () => {\n    const queries = youtubeQueriesForTrack(track);")
end_marker = "  })().finally(() => youtubeResolutionInFlight.delete(key));"
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("resolveTrackYoutubeId task markers not found")
end += len(end_marker)
new_task = '''  const task = (async () => {\n    const queries = youtubeQueriesForTrack(track);\n    let best = null;\n\n    // MusicBrainz and the strongest search formulation start together.\n    const firstQuery = queries[0] || `${track.artist} ${track.title}`;\n    const mbPromise = resolveMusicBrainzYoutubeId(track).catch(() => null);\n    const [mbResult, firstWave] = await Promise.all([\n      Promise.race([\n        mbPromise,\n        new Promise(resolve => setTimeout(() => resolve(null), 3000))\n      ]),\n      searchYoutubeResolverWave(track, firstQuery)\n    ]);\n\n    if (mbResult && !failedYoutubeIds.has(mbResult)){\n      best = {videoId:mbResult, source:"musicbrainz", score:145};\n    }\n    const firstBest = bestYoutubeCandidate(firstWave, track);\n    if (firstBest && (!best || firstBest.score > best.score)) best = firstBest;\n\n    // A removed/private/embed-blocked upload often leaves a good replacement under\n    // a slightly different query. Try two additional formulations before giving up.\n    if (!best || best.score < 104){\n      const alternates = [...new Set(queries.slice(1, 3))];\n      for (const query of alternates){\n        const wave = await Promise.race([\n          searchYoutubeResolverWave(track, query),\n          new Promise(resolve => setTimeout(() => resolve([]), 2600))\n        ]);\n        const candidate = bestYoutubeCandidate(wave, track);\n        if (candidate && (!best || candidate.score > best.score)) best = candidate;\n        if (best && best.score >= 104) break;\n      }\n    }\n\n    const resolvedId = best && best.score >= 74 ? best.videoId : null;\n    if (resolvedId){\n      persistYoutubeIdForTrack(track, resolvedId);\n      track.youtubeId = resolvedId;\n      track.youtubeUrl = `https://www.youtube.com/watch?v=${resolvedId}`;\n      track.youtubeMusicUrl = `https://music.youtube.com/watch?v=${resolvedId}`;\n      track.videoStatus = `runtime_resolved_${best.source || "search"}`;\n      track.videoValidationClass = best.score >= 108 ? "runtime_hq_confident" : "runtime_hq_best_match";\n    }\n    return resolvedId;\n  })().finally(() => youtubeResolutionInFlight.delete(key));'''
player02.write_text(text[:start] + new_task + text[end:], encoding="utf-8")

# Contexto becomes a two-section dialog: Contexto first, Sobre second.
combined_context = r'''function appendContextSection(heading, result, fallbackMessage, actionLabel){
  const section = document.createElement("section");
  section.className = "context-section";

  const title = document.createElement("h3");
  title.className = "context-section-title";
  title.textContent = heading;
  section.appendChild(title);

  if (result?.title || result?.contextLabel){
    const meta = document.createElement("p");
    meta.className = "context-section-meta";
    meta.textContent = [result?.contextLabel, result?.title].filter(Boolean).join(" · ");
    section.appendChild(meta);
  }

  const copy = document.createElement("p");
  copy.className = result?.extract ? "context-summary" : "context-message";
  copy.textContent = result?.extract ? trimContextExcerpt(result.extract) : fallbackMessage;
  section.appendChild(copy);

  if (result?.url){
    const link = document.createElement("a");
    link.className = "context-action context-section-action";
    link.href = result.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = actionLabel;
    section.appendChild(link);
  }

  contextDialogBody.appendChild(section);
}

async function openCulturalContextForTrack(track){
  if (!track) return;
  const token = openContextDialog("Contexto", track);
  try {
    const [culturalState, aboutState] = await Promise.allSettled([
      resolveWikipediaCulturalContext(track),
      resolveWikipediaSummary(track)
    ]);
    if (token !== contextRenderToken || !contextTrackIsCurrent(track)) return;

    const cultural = culturalState.status === "fulfilled" ? culturalState.value : null;
    const about = aboutState.status === "fulfilled" ? aboutState.value : null;

    contextDialogKicker.textContent = "Contexto";
    contextDialogTitle.textContent = track.title;
    contextDialogSubtitle.textContent = `${track.artist} · ${track.year}`;
    contextDialogBody.replaceChildren();
    contextDialogActions.replaceChildren();

    appendContextSection(
      "Contexto",
      cultural,
      "Nenhum dos títulos enciclopédicos direcionados para subgênero, gênero, movimento ou período forneceu texto.",
      cultural ? wikipediaCulturalActionLabel(cultural.contextKind) : "Wikipedia ↗"
    );
    appendContextSection(
      "Sobre",
      about,
      "Nenhum dos títulos enciclopédicos direcionados para a faixa ou o artista forneceu texto.",
      about ? wikipediaActionLabel(about.contextKind) : "Wikipedia ↗"
    );
  } catch (_) {
    if (token !== contextRenderToken) return;
    setContextMessage("As fontes enciclopédicas estão temporariamente indisponíveis.");
    setContextActions([]);
  }
}

'''
replace_between(
    "assets/source/services/08.part",
    "async function openAboutForTrack(track){",
    "async function openLyricsForTrack(track){",
    combined_context
)

# Exact ChatGPT appreciation URL requested by the user. Only title and artist placeholders change.
appreciation_template = r'''const APPRECIATION_URL_TEMPLATE = "https://chatgpt.com/?q=%22Quero%20ouvir%20[NOME DA MUSICA],%20de%20[NOME DO ARTISTA],%20como%20um%20apreciador%20musical%20atento,%20buscando%20extrair%20o%20m%C3%A1ximo%20poss%C3%ADvel%20da%20experi%C3%AAncia%20emocional,%20musical,%20est%C3%A9tica%20e%20art%C3%ADstica.%20Crie%20para%20mim%20um%20guia%20de%20escuta%20profunda%20da%20faixa,%20como%20faria%20um%20cr%C3%ADtico%20musical%20experiente,%20m%C3%BAsico%20ou%20produtor%20conversando%20com%20algu%C3%A9m%20que%20deseja%20aprender%20a%20ouvir%20m%C3%BAsica%20com%20mais%20sensibilidade,%20repert%C3%B3rio%20e%20discernimento.%20Analise%20a%20m%C3%BAsica%20levando%20em%20conta%20seu%20g%C3%AAnero,%20%C3%A9poca,%20proposta%20art%C3%ADstica%20e%20linguagem%20musical%20pr%C3%B3pria.%20Adapte%20os%20crit%C3%A9rios%20de%20an%C3%A1lise%20%C3%A0%20obra%20em%20quest%C3%A3o,%20dando%20maior%20aten%C3%A7%C3%A3o%20aos%20elementos%20que%20realmente%20importam%20naquela%20grava%C3%A7%C3%A3o.%20Explique%20o%20que%20vale%20a%20pena%20perceber%20enquanto%20a%20m%C3%BAsica%20acontece,%20incluindo,%20quando%20forem%20relevantes:%20melodia,%20harmonia,%20ritmo,%20groove,%20din%C3%A2mica,%20timbres,%20instrumenta%C3%A7%C3%A3o,%20arranjo,%20interpreta%C3%A7%C3%A3o%20vocal%20ou%20instrumental,%20produ%C3%A7%C3%A3o,%20espacialidade,%20textura,%20letra,%20estrutura%20e%20constru%C3%A7%C3%A3o%20emocional.%20Sempre%20que%20poss%C3%ADvel,%20indique%20momentos%20espec%C3%ADficos%20da%20grava%C3%A7%C3%A3o%20e%20explique:%20O%20que%20est%C3%A1%20acontecendo%20musicalmente%20naquele%20momento;%20Em%20que%20elemento%20devo%20concentrar%20minha%20aten%C3%A7%C3%A3o;%20O%20que%20devo%20tentar%20perceber%20auditivamente;%20Que%20efeito%20emocional,%20f%C3%ADsico%20ou%20psicol%C3%B3gico%20aquele%20recurso%20produz;%20Como%20esse%20detalhe%20contribui%20para%20a%20identidade%20e%20para%20a%20evolu%C3%A7%C3%A3o%20da%20m%C3%BAsica.%20Observe%20atentamente%20como%20a%20faixa%20se%20transforma%20ao%20longo%20do%20tempo.%20Mostre%20entradas%20e%20sa%C3%ADdas%20de%20instrumentos,%20mudan%C3%A7as%20de%20intensidade,%20altera%C3%A7%C3%B5es%20harm%C3%B4nicas%20ou%20r%C3%ADtmicas,%20repeti%C3%A7%C3%B5es,%20contrastes,%20sil%C3%AAncios,%20transi%C3%A7%C3%B5es,%20crescendos,%20rupturas,%20cl%C3%ADmax%20e%20resolu%C3%A7%C3%A3o.%20Analise%20tamb%C3%A9m%20a%20performance%20dos%20int%C3%A9rpretes.%20Quando%20houver%20voz,%20observe%20aspectos%20como%20timbre,%20respira%C3%A7%C3%A3o,%20articula%C3%A7%C3%A3o,%20fraseado,%20din%C3%A2mica,%20extens%C3%A3o,%20textura,%20ataques,%20sustenta%C3%A7%C3%A3o%20das%20notas,%20improvisa%C3%A7%C3%B5es%20e%20mudan%C3%A7as%20de%20intensidade.%20Em%20m%C3%BAsicas%20instrumentais,%20aplique%20esse%20mesmo%20n%C3%ADvel%20de%20aten%C3%A7%C3%A3o%20%C3%A0%20expressividade%20dos%20instrumentos%20protagonistas.%20Explore%20a%20rela%C3%A7%C3%A3o%20entre%20composi%C3%A7%C3%A3o,%20interpreta%C3%A7%C3%A3o,%20arranjo%20e%20produ%C3%A7%C3%A3o.%20Mostre%20como%20esses%20elementos%20trabalham%20juntos%20para%20produzir%20determinada%20atmosfera,%20emo%C3%A7%C3%A3o%20ou%20narrativa.%20Caso%20exista%20letra,%20analise%20a%20rela%C3%A7%C3%A3o%20entre%20palavras%20e%20m%C3%BAsica:%20como%20melodia,%20harmonia,%20ritmo,%20interpreta%C3%A7%C3%A3o%20e%20produ%C3%A7%C3%A3o%20refor%C3%A7am,%20contradizem%20ou%20ampliam%20o%20significado%20do%20texto.%20Quero%20aprender%20tamb%C3%A9m%20a%20distinguir%20tr%C3%AAs%20n%C3%ADveis%20de%20percep%C3%A7%C3%A3o:%20Ouvinte%20casual:%20elementos%20mais%20imediatamente%20percept%C3%ADveis.%20Apreciador%20experiente:%20detalhes%20estruturais,%20expressivos%20e%20est%C3%A9ticos%20que%20exigem%20aten%C3%A7%C3%A3o%20consciente.%20M%C3%BAsico%20ou%20produtor:%20decis%C3%B5es%20t%C3%A9cnicas,%20composicionais,%20perform%C3%A1ticas%20e%20de%20produ%C3%A7%C3%A3o%20que%20ajudam%20a%20explicar%20por%20que%20a%20grava%C3%A7%C3%A3o%20funciona%20da%20maneira%20que%20funciona.%20Organize%20minha%20experi%C3%AAncia%20em%20quatro%20audi%C3%A7%C3%B5es%20progressivas.%20Primeira%20audi%C3%A7%C3%A3o%20%E2%80%94%20experi%C3%AAncia%20pura:%20diga%20onde%20colocar%20a%20aten%C3%A7%C3%A3o%20para%20absorver%20atmosfera,%20emo%C3%A7%C3%A3o,%20energia%20e%20impress%C3%A3o%20geral,%20evitando%20an%C3%A1lise%20excessiva.%20Segunda%20audi%C3%A7%C3%A3o%20%E2%80%94%20arquitetura%20da%20m%C3%BAsica:%20conduza%20minha%20aten%C3%A7%C3%A3o%20pela%20estrutura,%20pelos%20principais%20instrumentos,%20pela%20voz,%20pelo%20ritmo,%20pela%20harmonia%20e%20pela%20evolu%C3%A7%C3%A3o%20din%C3%A2mica.%20Terceira%20audi%C3%A7%C3%A3o%20%E2%80%94%20detalhes%20finos:%20revele%20pequenas%20escolhas%20de%20interpreta%C3%A7%C3%A3o,%20produ%C3%A7%C3%A3o,%20timbre,%20textura,%20espacialidade,%20ornamenta%C3%A7%C3%A3o%20ou%20arranjo%20que%20facilmente%20passam%20despercebidas.%20Quarta%20audi%C3%A7%C3%A3o%20%E2%80%94%20integra%C3%A7%C3%A3o:%20ajude-me%20a%20ouvir%20novamente%20a%20faixa%20como%20um%20todo,%20agora%20percebendo%20simultaneamente%20sua%20emo%C3%A7%C3%A3o%20e%20sua%20constru%C3%A7%C3%A3o%20art%C3%ADstica.%20Evite%20transformar%20a%20an%C3%A1lise%20em%20mera%20enumera%C3%A7%C3%A3o%20de%20conceitos%20t%C3%A9cnicos.%20Cada%20observa%C3%A7%C3%A3o%20deve%20responder%20principalmente%20%C3%A0%20pergunta:%20%E2%80%9CComo%20perceber%20isso%20com%20os%20meus%20pr%C3%B3prios%20ouvidos%20e%20por%20que%20isso%20torna%20a%20m%C3%BAsica%20mais%20interessante?%E2%80%9D%20Quando%20utilizar%20termos%20t%C3%A9cnicos,%20explique-os%20de%20maneira%20simples%20e%20associe-os%20imediatamente%20a%20algo%20que%20eu%20possa%20identificar%20auditivamente.%20Tamb%C3%A9m%20destaque%20tr%C3%AAs%20a%20cinco%20momentos%20da%20m%C3%BAsica%20que%20merecem%20aten%C3%A7%C3%A3o%20especial,%20explicando%20por%20que%20eles%20s%C3%A3o%20particularmente%20importantes.%20Ao%20final,%20responda:%20O%20que%20torna%20esta%20m%C3%BAsica%20artisticamente%20interessante?%20Qual%20%C3%A9%20sua%20principal%20for%C3%A7a%20musical%20ou%20expressiva?%20Que%20escolhas%20fazem%20esta%20grava%C3%A7%C3%A3o%20ter%20uma%20identidade%20pr%C3%B3pria?%20O%20que%20provavelmente%20passaria%20despercebido%20em%20uma%20escuta%20comum?%20O%20que%20devo%20tentar%20perceber%20na%20pr%C3%B3xima%20vez%20que%20ouvir%20outras%20m%C3%BAsicas%20depois%20de%20aprender%20com%20esta%20faixa?%20Meu%20objetivo%20%C3%A9%20terminar%20a%20experi%C3%AAncia%20tendo%20desenvolvido%20minha%20pr%C3%B3pria%20capacidade%20de%20escuta,%20e%20n%C3%A3o%20apenas%20aprendido%20curiosidades%20sobre%20uma%20m%C3%BAsica%20espec%C3%ADfica.%22";

function appreciationUrl(track){
  return APPRECIATION_URL_TEMPLATE
    .replace("[NOME DA MUSICA]", encodeURIComponent(String(track?.title || "")))
    .replace("[NOME DO ARTISTA]", encodeURIComponent(String(track?.artist || "")));
}
'''
file("assets/source/services/09.part").write_text(appreciation_template, encoding="utf-8")

# Link rendering: Contexto, Álbum, Letra, Apreciação. Sobre is no longer a separate action.
replace_once(
    "assets/source/player/03.part",
    '''  showTrackAction(infoLink);\n  showTrackAction(contextLink);\n  hideTrackLink(albumLink);\n  if (shouldHideLyrics(track)) hideTrackAction(lyricsLink);\n  else showTrackAction(lyricsLink);''',
    '''  showTrackAction(contextLink);\n  hideTrackLink(albumLink);\n  if (shouldHideLyrics(track)) hideTrackAction(lyricsLink);\n  else showTrackAction(lyricsLink);\n  appreciationLink.title = `Abrir guia de escuta profunda de ${track.title} no ChatGPT`;\n  showTrackLink(appreciationLink, appreciationUrl(track));'''
)

# Remove duplicate event bindings from player/08; bootstrap remains the single binding point.
player08 = file("assets/source/player/08.part")
text = player08.read_text(encoding="utf-8")
marker = 'infoLink.addEventListener("click", () => openAboutForTrack(currentTrack()));'
pos = text.find(marker)
if pos < 0:
    raise SystemExit("duplicate player event marker not found")
player08.write_text(text[:pos].rstrip() + "\n", encoding="utf-8")

# Styling for the two Contexto sections.
replace_once(
    "assets/styles.css",
    '.context-summary{margin:0;white-space:pre-wrap;font-size:14px;line-height:1.62}',
    '''.context-summary{margin:0;white-space:pre-wrap;font-size:14px;line-height:1.62}\n.context-section{display:block}\n.context-section + .context-section{margin-top:22px;padding-top:20px;border-top:1px solid var(--line)}\n.context-section-title{margin:0 0 7px;font-size:15px;line-height:1.2;letter-spacing:-.01em}\n.context-section-meta{margin:0 0 10px;color:var(--muted);font-size:11px;line-height:1.35}\n.context-section-action{display:inline-flex;margin-top:12px}'''
)

print("Prepared Play History v6.22.0 player UX candidate")
