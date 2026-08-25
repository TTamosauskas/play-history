/* Play History v6.7.1 — modular static loader */
const BUILD_VERSION = '6.7.1';
const MODULES = [
  './assets/js/app.js',
  './assets/js/services.js',
  './assets/js/player.js',
  './assets/js/bootstrap.js'
];

const earlyYearForm = document.getElementById('yearForm');
const earlyYearInput = document.getElementById('yearInput');
let bootReady = false;
let pendingYear = '';

function validRequestedYear(raw) {
  const value = String(raw || '').trim();
  if (!/^\d{3,4}$/.test(value)) return false;
  const year = Number(value);
  return year >= 800 && year <= 2026;
}

function captureEarlyYear(event) {
  if (bootReady) return;
  if (event?.type === 'submit') event.preventDefault();
  const raw = String(earlyYearInput?.value || '').trim();
  if (raw) pendingYear = raw;
}

earlyYearInput?.addEventListener('input', captureEarlyYear);
earlyYearInput?.addEventListener('change', captureEarlyYear);
earlyYearForm?.addEventListener('submit', captureEarlyYear);

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

function runScript(code, name) {
  const script = document.createElement('script');
  script.text = `${code}\n//# sourceURL=play-history/${name}`;
  document.head.appendChild(script);
}

function releaseEarlyYearCapture() {
  bootReady = true;
  earlyYearInput?.removeEventListener('input', captureEarlyYear);
  earlyYearInput?.removeEventListener('change', captureEarlyYear);
  earlyYearForm?.removeEventListener('submit', captureEarlyYear);
}

function replayPendingYear() {
  const raw = String(pendingYear || earlyYearInput?.value || '').trim();
  if (!validRequestedYear(raw) || !earlyYearForm || !earlyYearInput) return;
  earlyYearInput.value = raw;
  queueMicrotask(() => {
    earlyYearForm.dispatchEvent(new Event('submit', { bubbles:true, cancelable:true }));
  });
}

(async () => {
  try {
    const [catalogText, ...moduleTexts] = await Promise.all([
      fetchText('./assets/catalog.json'),
      ...MODULES.map(fetchText)
    ]);
    const rows = JSON.parse(catalogText);
    window.PLAY_HISTORY = {
      meta: { version:BUILD_VERSION, totalTracks:rows.length },
      catalog: rows.map(expandTrack)
    };
    moduleTexts.forEach((code, index) => runScript(code, MODULES[index].split('/').pop()));
    releaseEarlyYearCapture();
    replayPendingYear();
  } catch (error) {
    console.error(error);
    releaseEarlyYearCapture();
    const status = document.getElementById('status');
    if (status) status.textContent = 'Falha ao carregar o player.';
  }
})();
