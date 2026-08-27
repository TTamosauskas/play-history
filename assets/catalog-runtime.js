/* Play History v6.23.0 — branch-safe catalog/bootstrap runtime. */
(() => {
  const VERSION = '6.23.0';
  const ADDITIONS_FILE = 'additions_2020s.json';
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
  function validateAdditions(baseTracks, additions){
    if (!Array.isArray(additions) || additions.length !== 21){
      throw new Error(`Pacote 2020s inválido: ${Array.isArray(additions) ? additions.length : 0} faixas`);
    }
    const youtubeIds = new Set(baseTracks.map(track => track.youtubeId).filter(Boolean));
    const identities = new Set(baseTracks.map(track => exactKey(Number(track.year), track.artist, track.title)));
    for (const track of additions){
      const identity = exactKey(Number(track.year), track.artist, track.title);
      if (!Number.isInteger(Number(track.year)) || Number(track.year) < 2020 || Number(track.year) > 2029){
        throw new Error(`Ano inválido em adição: ${track.artist} — ${track.title}`);
      }
      if (!track.artist || !track.title || !track.albumTitle){
        throw new Error(`Metadados obrigatórios ausentes em adição: ${track.artist || '?'} — ${track.title || '?'}`);
      }
      if (identities.has(identity)) throw new Error(`Faixa duplicada no catálogo: ${track.year} — ${track.artist} — ${track.title}`);
      identities.add(identity);
      if (!/^[A-Za-z0-9_-]{11}$/.test(String(track.youtubeId || ''))){
        throw new Error(`YouTube ID inválido: ${track.artist} — ${track.title}`);
      }
      if (youtubeIds.has(track.youtubeId)) throw new Error(`YouTube ID duplicado: ${track.youtubeId}`);
      youtubeIds.add(track.youtubeId);
      if (!/^https:\/\/i\.ytimg\.com\/vi\/[A-Za-z0-9_-]{11}\/(?:hqdefault|maxresdefault)\.jpg$/.test(String(track.artworkUrl || ''))){
        throw new Error(`Artwork inválido: ${track.artist} — ${track.title}`);
      }
      if (track.lyricsPolicy !== 'show_if_verified'){
        throw new Error(`Política de letra inválida: ${track.artist} — ${track.title}`);
      }
      if (!Array.isArray(track.contextWikiTargets) || !track.contextWikiTargets.length){
        throw new Error(`Contexto ausente: ${track.artist} — ${track.title}`);
      }
      for (const target of track.contextWikiTargets){
        if (!target?.kind || !target?.en) throw new Error(`Alvo de contexto inválido: ${track.artist} — ${track.title}`);
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
    const [legacy, additions, ...patchLists] = await Promise.all([
      text('./source/legacy.html'),
      json(`./tools/patches/${ADDITIONS_FILE}`),
      ...AUDIT_FILES.map(name => json(`./tools/patches/${name}`))
    ]);
    const project = projectFromLegacy(legacy);
    const baseTracks = (project.tracks || []).map(normalizeTrack);
    if (baseTracks.length !== 1726) throw new Error(`Catálogo histórico incompleto: ${baseTracks.length}`);
    const addedTracks = additions.map(normalizeTrack);
    validateAdditions(baseTracks, addedTracks);
    const tracks = baseTracks.concat(addedTracks);
    applyContexts(tracks, patchLists);
    window.PLAY_HISTORY = {meta:{version:VERSION,totalTracks:tracks.length},catalog:tracks};
    for (const [group, count] of Object.entries(MODULE_PARTS)) await loadModule(group, count);
  }

  boot().catch(fail);
})();
