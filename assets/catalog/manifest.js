const PROJECT = {version:"catalog-selection-v6.7.0-modular", generated:"2026-08-25", totalTracks:1726, tracks:[]};
const CATALOG_FIELDS = ["year","yearPriority","decadeRank","artist","title","youtubeId","catalogSource","albumTitle","albumUrl","artworkUrl","artworkMode","artworkPageTitle","lyricsPolicy","contextTermPt","contextWikiTargets","wikipediaTrackTerm","wikipediaArtistTermPt","wikipediaArtistTermEn"];
function addCatalogRows(rows){
  for (const row of rows){
    const track = {};
    for (let i = 0; i < row.length; i++){
      const value = row[i];
      if (value !== null && value !== undefined) track[CATALOG_FIELDS[i]] = value;
    }
    if (track.youtubeId){
      track.youtubeUrl = `https://www.youtube.com/watch?v=${track.youtubeId}`;
      track.youtubeMusicUrl = `https://music.youtube.com/watch?v=${track.youtubeId}`;
    }
    track.youtubeQuery = `${track.artist || ""} ${track.title || ""}`.trim();
    PROJECT.tracks.push(track);
  }
}
