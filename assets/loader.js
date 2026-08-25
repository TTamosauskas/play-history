/* Play History v6.7.3 — modular static loader and year-search entry point */
const BUILD_VERSION = '6.7.3';
const MODULES = [
  './assets/js/app.js',
  './assets/js/services.js',
  './assets/js/player.js',
  './assets/js/bootstrap.js'
];

const earlyYearForm = document.getElementById('yearForm');
const earlyYearInput = document.getElementById('yearInput');
let bootReady = false;
let pendingYear = String(earlyYearInput?.value || '').trim();
let entryYearTimer = null;

function validRequestedYear(raw) {
  const value = String(raw || '').trim();
  if (!/^\d{3,4}$/.test(value)) return false;
  const year = Number(value);
  return year >= 800 && year <= 2026;
}

function requestedYearValue() {
  return String(earlyYearInput?.value || '').trim();
}

function applyRequestedYear(raw, autoplay = true) {
  const value = String(raw || '').trim();
  if (!validRequestedYear(value)) return false;
  pendingYear = value;
  if (!bootReady || typeof window.selectYear !== 'function') return false;
  return window.selectYear(Number(value), Boolean(autoplay)) !== false;
}

function handleYearEntryInput(event) {
  pendingYear = requestedYearValue();
  if (!bootReady) return;

  // This listener owns year search. Prevent the legacy player listener from
  // scheduling a second selection for the same keystroke.
  event?.stopImmediatePropagation?.();
  clearTimeout(entryYearTimer);
  if (!validRequestedYear(pendingYear)) return;
  const requested = pendingYear;
  entryYearTimer = setTimeout(() => {
    if (requested === requestedYearValue()) applyRequestedYear(requested, true);
  }, 160);
}

function handleYearEntrySubmit(event) {
  event?.preventDefault?.();
  event?.stopImmediatePropagation?.();
  clearTimeout(entryYearTimer);
  pendingYear = requestedYearValue();
  applyRequestedYear(pendingYear, true);
}

earlyYearInput?.addEventListener('input', handleYearEntryInput);
earlyYearInput?.addEventListener('change', handleYearEntryInput);
earlyYearForm?.addEventListener('submit', handleYearEntrySubmit);

function versionedUrl(url) {
  return `${url}${url.includes('?') ? '&' : '?'}v=${encodeURIComponent(BUILD_VERSION)}`;
}

async function fetchText(url) {
  const response = await fetch(versionedUrl(url), { cache: 'no-cache' });
  if (!response.ok) throw new Error(`Falha ao carregar ${url}: HTTP ${response.status}`);
  return response.text();
}

function expandTrack(row) {
  const [artist,title,year,youtubeId,brazil,packedContext,decadeRank,yearPriority,albumTitle,albumUrl,artworkMode,artworkPageTitle,artworkUrl,lyricsPolicy,wikiTrack,wikiArtistPt,wikiArtistEn] = row;
  const packedTargets = typeof packedContext?.[0] === 'string' ? [packedContext] : packedContext;
  const contextWikiTargets = (packedTargets || []).map(([kind,pt,en]) => ({kind,pt,en}));
  const track = {
    artist,title,year,youtubeId,
    catalogSource:brazil ? 'brazil' : 'international',
    contextWikiTargets,
    contextTermPt:contextWikiTargets[0]?.pt || '',
    decadeRank,yearPriority,
    wikipediaTrackTerm:wikiTrack || title,
    wikipediaArtistTermPt:wikiArtistPt || artist,
    wikipediaArtistTermEn:wikiArtistEn || artist
  };
  if (youtubeId){
    track.youtubeUrl=`https://www.youtube.com/watch?v=${youtubeId}`;
    track.youtubeMusicUrl=`https://music.youtube.com/watch?v=${youtubeId}`;
  }
  track.youtubeQuery=`${artist || ''} ${title || ''}`.trim();
  if (albumTitle) track.albumTitle=albumTitle;
  if (albumUrl) track.albumUrl=albumUrl;
  if (artworkMode) track.artworkMode=artworkMode;
  if (artworkPageTitle) track.artworkPageTitle=artworkPageTitle;
  if (artworkUrl) track.artworkUrl=artworkUrl;
  if (lyricsPolicy) track.lyricsPolicy=lyricsPolicy;
  return track;
}

function loadScript(url) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = versionedUrl(url);
    script.async = false;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error(`Falha ao executar ${url}`));
    document.head.appendChild(script);
  });
}

function replayPendingYear() {
  const raw = String(pendingYear || requestedYearValue()).trim();
  if (!validRequestedYear(raw)) return;
  if (earlyYearInput) earlyYearInput.value = raw;
  queueMicrotask(() => applyRequestedYear(raw, true));
}

(async () => {
  try {
    const rows = JSON.parse(await fetchText('./assets/catalog.json'));
    window.PLAY_HISTORY = {
      meta: { version:BUILD_VERSION, totalTracks:rows.length },
      catalog: rows.map(expandTrack)
    };

    for (const url of MODULES) await loadScript(url);

    bootReady = true;
    replayPendingYear();
  } catch (error) {
    console.error(error);
    bootReady = true;
    const status = document.getElementById('status');
    if (status) status.textContent = 'Falha ao carregar o player.';
  }
})();
