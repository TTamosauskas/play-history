/* Play History v6.7.0 — modular static loader */
const MODULES = [
  './assets/js/app.js',
  './assets/js/services.js',
  './assets/js/player.js',
  './assets/js/bootstrap.js'
];

async function fetchText(url) {
  const response = await fetch(url, { cache: 'default' });
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

(async () => {
  try {
    const rows = JSON.parse(await fetchText('./assets/catalog.json'));
    window.PLAY_HISTORY = {
      meta: { version:'6.7.0', totalTracks:rows.length },
      catalog: rows.map(expandTrack)
    };
    for (const url of MODULES) runScript(await fetchText(url), url.split('/').pop());
  } catch (error) {
    console.error(error);
    const status = document.getElementById('status');
    if (status) status.textContent = 'Falha ao carregar o player.';
  }
})();
