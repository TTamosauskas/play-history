/* Play History v6.24.0 — branch-safe catalog/bootstrap runtime. */
(() => {
  const VERSION = '6.24.0';
  const ADDITION_FILES = [
    'additions_2010s.json',
    'additions_2020s.json'
  ];
  const AUDIT_FILES = [
    'context_overrides.json',
    ...Array.from({length: 10}, (_, i) => `context_1900s_${1900 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1910s_${1910 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1920s_${1920 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1930s_${1930 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1940s_${1940 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1950s_${1950 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1960s_${1960 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1970s_${1970 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1980s_${1980 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_1990s_${1990 + i}.json`),
    ...Array.from({length: 10}, (_, i) => `context_2000s_${2000 + i}.json`),
    'context_2010s.json',
    'context_2020s.json'
  ];
  const MODULE_PARTS = {
    app: 4,
    services: 9,
    player: 8,
    bootstrap: 1
  };

  const url = path => `${path}?v=${VERSION}`;
  async function text(path){
    const response = await fetch(url(path), {cache:'no-cache'});
    if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    return response.text();
  }
  async function json(path){ return JSON.parse(await text(path)); }

  function projectFromLegacy(source){
    const match = source.match(/const PROJECT\s*=\s*(\{[\s\S]*?\});\s*\nconst CATALOG/);
    if (!match) throw new Error('PROJECT não encontrado em source/legacy.html');
    return JSON.parse(match[1]);
  }
  function looseKey(artist, title){ return `${artist}\u0000${title}`; }
  function exactKey(year, artist, title){ return `${year}\u0000${artist}\u0000${title}`; }
  function normalizeTrack(track){
    const copy = {...track};
    if (copy.artist === 'Júpiter Maçã' && copy.title === 'A Marchinha Psicótica de Dr. Soup'){
      copy.youtubeId = '3dEeAXY7nTs';
      copy.youtubeUrl = 'https://www.youtube.com/watch?v=3dEeAXY7nTs';
      copy.youtubeMusicUrl = 'https://music.youtube.com/watch?v=3dEeAXY7nTs';
    }
    copy.youtubeQuery = `${copy.artist || ''} ${copy.title || ''}`.trim();
    return copy;
  }
  function additionDecade(filename){
    const match = String(filename || '').match(/^additions_(\d{4})s\.json$/);
    return match ? Number(match[1]) : null;
  }
  function validateAdditionPackages(baseTracks, packages){
    const youtubeIds = new Set(baseTracks.map(track => track.youtubeId).filter(Boolean));
    const identities = new Set(baseTracks.map(track => exactKey(Number(track.year), track.artist, track.title)));
    const artworkRe = /^https:\/\/i\.ytimg\.com\/vi\/([A-Za-z0-9_-]{11})\/(?:hqdefault|maxresdefault)\.jpg$/;

    for (const pkg of packages){
      const decade = additionDecade(pkg?.name);
      const additions = pkg?.tracks;
      if (decade === null || !Array.isArray(additions) || !additions.length){
        throw new Error(`Pacote de adições inválido: ${pkg?.name || '?'}`);
      }

      for (const track of additions){
        const year = Number(track.year);
        const label = `${track.artist || '?'} — ${track.title || '?'}`;
        const identity = exactKey(year, track.artist, track.title);
        if (!Number.isInteger(year) || year < decade || year > decade + 9){
          throw new Error(`Ano inválido em ${pkg.name}: ${label}`);
        }
        if (!track.artist || !track.title || !track.albumTitle || !track.wikipediaTrackTerm){
          throw new Error(`Metadados obrigatórios ausentes em ${pkg.name}: ${label}`);
        }
        if (identities.has(identity)) throw new Error(`Faixa duplicada no catálogo: ${year} — ${label}`);
        identities.add(identity);

        if (!/^[A-Za-z0-9_-]{11}$/.test(String(track.youtubeId || ''))){
          throw new Error(`YouTube ID inválido: ${label}`);
        }
        if (youtubeIds.has(track.youtubeId)) throw new Error(`YouTube ID duplicado: ${track.youtubeId}`);
        youtubeIds.add(track.youtubeId);

        const artworkMatch = String(track.artworkUrl || '').match(artworkRe);
        if (!artworkMatch || artworkMatch[1] !== track.youtubeId){
          throw new Error(`Artwork inválido ou desacoplado do vídeo: ${label}`);
        }
        if (track.lyricsPolicy !== 'show_if_verified'){
          throw new Error(`Política de letra inválida: ${label}`);
        }
        if (!Array.isArray(track.contextWikiTargets) || !track.contextWikiTargets.length){
          throw new Error(`Contexto ausente: ${label}`);
        }
        for (const target of track.contextWikiTargets){
          if (!target?.kind || !target?.en) throw new Error(`Alvo de contexto inválido: ${label}`);
        }
      }
    }
  }
  function applyContexts(tracks, patchLists){
    const looseOverrides = new Map();
    const exactOverrides = new Map();
    for (const list of patchLists){
      for (const item of list){
        if (!item?.artist || !item?.title || !Array.isArray(item.targets) || !item.targets.length) continue;
        if (item.year !== undefined && item.year !== null){
          exactOverrides.set(exactKey(Number(item.year), item.artist, item.title), item.targets);
        } else {
          looseOverrides.set(looseKey(item.artist, item.title), item.targets);
        }
      }
    }
    for (const track of tracks){
      const targets = exactOverrides.get(exactKey(Number(track.year), track.artist, track.title))
        || looseOverrides.get(looseKey(track.artist, track.title));
      if (!targets) continue;
      track.contextWikiTargets = targets.map(target => ({kind:target.kind, pt:target.pt, en:target.en}));
      track.contextTermPt = track.contextWikiTargets[0]?.pt || '';
      track.contextTermEn = track.contextWikiTargets[0]?.en || '';
    }
  }
  async function loadModule(group, count){
    const parts = await Promise.all(Array.from({length: count}, (_, i) => {
      const name = String(i + 1).padStart(2, '0');
      return text(`./assets/source/${group}/${name}.part`);
    }));
    const blobUrl = URL.createObjectURL(new Blob([parts.join('')], {type:'text/javascript'}));
    try {
      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = blobUrl;
        script.onload = resolve;
        script.onerror = () => reject(new Error(`Falha ao executar módulo ${group}`));
        document.head.appendChild(script);
      });
    } finally {
      URL.revokeObjectURL(blobUrl);
    }
  }
  function fail(error){
    console.error('Falha ao inicializar Play History', error);
    const status = document.getElementById('status');
    if (status) status.textContent = 'Falha ao carregar o catálogo. Recarregue a página.';
  }

  async function boot(){
    const [legacy, additionPackages, patchLists] = await Promise.all([
      text('./source/legacy.html'),
      Promise.all(ADDITION_FILES.map(async name => ({
        name,
        tracks: (await json(`./tools/patches/${name}`)).map(normalizeTrack)
      }))),
      Promise.all(AUDIT_FILES.map(name => json(`./tools/patches/${name}`)))
    ]);
    const project = projectFromLegacy(legacy);
    const baseTracks = (project.tracks || []).map(normalizeTrack);
    if (baseTracks.length !== 1726) throw new Error(`Catálogo histórico incompleto: ${baseTracks.length}`);
    validateAdditionPackages(baseTracks, additionPackages);
    const addedTracks = additionPackages.flatMap(pkg => pkg.tracks);
    const tracks = baseTracks.concat(addedTracks);
    applyContexts(tracks, patchLists);
    window.PLAY_HISTORY = {meta:{version:VERSION,totalTracks:tracks.length},catalog:tracks};
    for (const [group, count] of Object.entries(MODULE_PARTS)) await loadModule(group, count);
  }

  boot().catch(fail);
})();
