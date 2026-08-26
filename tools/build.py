#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
LEGACY=ROOT/'source'/'legacy.html'
EXPECTED=(ROOT/'tools'/'base_signature.txt').read_text().strip()
VERSION='6.9.0'
AUDIT_START=2020
AUDIT_END=2026
GENERIC_AUDITED_PRIMARY={'Música pop','MPB','Rock'}
ALLOWED_CONTEXT_KINDS={'genre','subgenre','movement','century','decade'}


def load_project():
    text=LEGACY.read_text(encoding='utf-8')
    m=re.search(r'const PROJECT\s*=\s*(\{.*?\});\s*\nconst CATALOG',text,re.S)
    if not m:
        raise SystemExit('PROJECT não encontrado em source/legacy.html')
    project=json.loads(m.group(1))
    tracks=project.get('tracks') or []
    sig='\n'.join(f"{t.get('artist','')}\t{t.get('title','')}\t{t.get('year','')}" for t in tracks)
    sha=hashlib.sha256(sig.encode()).hexdigest()
    if len(tracks)!=1726 or sha!=EXPECTED:
        raise SystemExit(f'Base incompatível: tracks={len(tracks)} signature={sha}')
    return tracks


def load_patch(name):
    return json.loads((ROOT/'tools'/'patches'/name).read_text(encoding='utf-8'))


def assemble(group):
    parts=sorted((ROOT/'assets'/'source'/group).glob('*.part'))
    return ''.join(p.read_text(encoding='utf-8') for p in parts)


def materialize_index():
    text=(ROOT/'index.html').read_text(encoding='utf-8')
    text=re.sub(r'data-build="[^"]+"',f'data-build="{VERSION}"',text,count=1)
    text=re.sub(r'(<title>Player Musical 800–2026 — v)[^<]+',rf'\g<1>{VERSION}',text,count=1)
    text=re.sub(r'(\?v=)[^"\']+',rf'\g<1>{VERSION}',text)
    return text


def catalog_javascript(rows):
    packed=json.dumps(rows,ensure_ascii=False,separators=(',',':'))
    return f'''/* Play History {VERSION} — generated compact catalog. */
(() => {{
  const rows={packed};
  function expandTrack(row) {{
    const [artist,title,year,youtubeId,brazil,packedContext,decadeRank,yearPriority,albumTitle,albumUrl,artworkMode,artworkPageTitle,artworkUrl,lyricsPolicy,wikiTrack,wikiArtistPt,wikiArtistEn] = row;
    const packedTargets = typeof packedContext?.[0] === 'string' ? [packedContext] : packedContext;
    const contextWikiTargets = (packedTargets || []).map(([kind,pt,en]) => ({{kind,pt,en}}));
    const track = {{
      artist,title,year,youtubeId,
      catalogSource:brazil ? 'brazil' : 'international',
      contextWikiTargets,
      contextTermPt:contextWikiTargets[0]?.pt || '',
      decadeRank,yearPriority,
      wikipediaTrackTerm:wikiTrack || title,
      wikipediaArtistTermPt:wikiArtistPt || artist,
      wikipediaArtistTermEn:wikiArtistEn || artist
    }};
    if (youtubeId){{
      track.youtubeUrl=`https://www.youtube.com/watch?v=${{youtubeId}}`;
      track.youtubeMusicUrl=`https://music.youtube.com/watch?v=${{youtubeId}}`;
    }}
    track.youtubeQuery=`${{artist || ''}} ${{title || ''}}`.trim();
    if (albumTitle) track.albumTitle=albumTitle;
    if (albumUrl) track.albumUrl=albumUrl;
    if (artworkMode) track.artworkMode=artworkMode;
    if (artworkPageTitle) track.artworkPageTitle=artworkPageTitle;
    if (artworkUrl) track.artworkUrl=artworkUrl;
    if (lyricsPolicy) track.lyricsPolicy=lyricsPolicy;
    return track;
  }}
  window.PLAY_HISTORY = {{
    meta: {{version:'{VERSION}', totalTracks:rows.length}},
    catalog: rows.map(expandTrack)
  }};
}})();
'''


def validate_context_targets(label,targets):
    if not isinstance(targets,list) or not targets:
        raise SystemExit(f'Contexto vazio: {label}')
    for target in targets:
        if not isinstance(target,dict):
            raise SystemExit(f'Contexto inválido: {label}')
        kind=target.get('kind')
        if kind not in ALLOWED_CONTEXT_KINDS:
            raise SystemExit(f'Tipo de contexto inválido: {label}: {kind!r}')
        if not str(target.get('pt') or '').strip() or not str(target.get('en') or '').strip():
            raise SystemExit(f'Alvo de contexto incompleto: {label}: {target!r}')


def build():
    tracks=load_project()
    patterns=load_patch('context_patterns.json')
    indices=load_patch('context_index_a.json')+load_patch('context_index_b.json')
    if len(indices)!=len(tracks):
        raise SystemExit('Índice de contexto incompatível')

    legacy_override_rows=load_patch('context_overrides.json')
    audit_rows=load_patch('context_2020s.json')

    expected_audit={
        (t.get('artist'),t.get('title')):int(t.get('year'))
        for t in tracks
        if AUDIT_START<=int(t.get('year'))<=AUDIT_END
    }
    audit_map={}
    for item in audit_rows:
        key=(item.get('artist'),item.get('title'))
        if key in audit_map:
            raise SystemExit(f'Faixa duplicada na auditoria 2020s: {key}')
        validate_context_targets(f'{key[0]} — {key[1]}',item.get('targets'))
        audit_map[key]=item

    audit_keys=set(audit_map)
    expected_keys=set(expected_audit)
    missing=expected_keys-audit_keys
    extra=audit_keys-expected_keys
    if missing or extra:
        raise SystemExit(f'Auditoria 2020s incompleta: faltam={sorted(missing)} extras={sorted(extra)}')
    for key,expected_year in expected_audit.items():
        declared_year=int(audit_map[key].get('year'))
        if declared_year!=expected_year:
            raise SystemExit(f'Ano incorreto na auditoria 2020s: {key}: {declared_year} != {expected_year}')
        primary=audit_map[key]['targets'][0].get('pt')
        if primary in GENERIC_AUDITED_PRIMARY:
            raise SystemExit(f'Contexto primário genérico proibido na auditoria 2020s: {key}: {primary}')

    override_rows=legacy_override_rows+audit_rows
    context_overrides={}
    for item in override_rows:
        key=(item.get('artist'),item.get('title'))
        if key in context_overrides:
            raise SystemExit(f'Override de contexto duplicado: {key}')
        validate_context_targets(f'{key[0]} — {key[1]}',item.get('targets'))
        context_overrides[key]=item['targets']
    applied_overrides=set()

    wiki_track=dict(load_patch('wiki_track.json'))
    wiki_pt=dict(load_patch('wiki_artist_pt.json'))
    wiki_en=dict(load_patch('wiki_artist_en.json'))
    rows=[]
    for i,t in enumerate(tracks):
        youtube_id=t.get('youtubeId')
        if t.get('artist')=='Júpiter Maçã' and t.get('title')=='A Marchinha Psicótica de Dr. Soup':
            youtube_id='3dEeAXY7nTs'

        context_key=(t.get('artist'),t.get('title'))
        if context_key in context_overrides:
            targets=context_overrides[context_key]
            applied_overrides.add(context_key)
        else:
            targets=patterns[indices[i]]

        packed=[[x.get('kind'),x.get('pt'),x.get('en')] for x in targets]
        if len(packed)==1:
            packed=packed[0]
        row=[
            t.get('artist'),t.get('title'),t.get('year'),youtube_id,
            1 if t.get('catalogSource')=='brazil' else 0,
            packed,t.get('decadeRank'),t.get('yearPriority'),
            t.get('albumTitle'),t.get('albumUrl'),t.get('artworkMode'),
            t.get('artworkPageTitle'),t.get('artworkUrl'),t.get('lyricsPolicy'),
            wiki_track.get(i),wiki_pt.get(i),wiki_en.get(i)
        ]
        while row and row[-1] is None:
            row.pop()
        rows.append(row)

    missing_overrides=set(context_overrides)-applied_overrides
    if missing_overrides:
        raise SystemExit(f'Overrides de contexto sem faixa correspondente: {sorted(missing_overrides)}')

    ids=[r[3] for r in rows if len(r)>3 and r[3]]
    if len(ids)!=len(set(ids)):
        raise SystemExit('youtubeId duplicado')

    def find(a,title):
        return next((r for r in rows if r[0]==a and r[1]==title),None)

    def context_targets(row):
        if not row or len(row)<=5 or not row[5]:
            return []
        return [row[5]] if isinstance(row[5][0],str) else row[5]

    def first_context(a,title):
        targets=context_targets(find(a,title))
        return targets[0][1] if targets else None

    black=find('Black Sabbath','Paranoid')
    bee=find('Bee Gees',"Stayin' Alive")
    if not black or not any(x[1]=='Heavy metal' for x in context_targets(black)):
        raise SystemExit('Contexto Black Sabbath inválido')
    if not bee or not any(x[1]=='Música disco' for x in context_targets(bee)):
        raise SystemExit('Contexto Bee Gees inválido')

    expected_contexts={
        ('The Beatles','I Want to Hold Your Hand'):'Invasão britânica',
        ('The Beatles','Yesterday'):'Invasão britânica',
        ('The Beatles','Help!'):'Invasão britânica',
        ('The Beatles','In My Life'):'Invasão britânica',
        ('The Beatles','Eleanor Rigby'):'Rock psicodélico',
        ('The Beatles','A Day in the Life'):'Rock psicodélico',
        ('The Beatles','All You Need Is Love'):'Rock psicodélico',
        ('The Beatles','Hey Jude'):'Pop rock',
        ('The Beatles','Come Together'):'Blues rock',
        ('The Beatles','Let It Be'):'Música gospel',
        ('The Temptations','My Girl'):'Motown',
        ('Linkin Park','Numb'):'Nu metal',
    }
    for (artist,title),expected_context in expected_contexts.items():
        actual=first_context(artist,title)
        if actual!=expected_context:
            raise SystemExit(f'Contexto inválido: {artist} — {title}: {actual!r} != {expected_context!r}')
    if any(x[1]=='Música pop' for x in context_targets(find('Linkin Park','Numb'))):
        raise SystemExit('Linkin Park não pode cair em Música pop')

    # A auditoria da década é um contrato completo: cada faixa deve sair do
    # catálogo com exatamente o contexto primário declarado no arquivo 2020s.
    for (artist,title),item in audit_map.items():
        expected_primary=item['targets'][0]['pt']
        actual=first_context(artist,title)
        if actual!=expected_primary:
            raise SystemExit(f'Auditoria 2020s divergente: {artist} — {title}: {actual!r} != {expected_primary!r}')
        if actual in GENERIC_AUDITED_PRIMARY:
            raise SystemExit(f'Contexto primário genérico reapareceu: {artist} — {title}: {actual}')

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT/'assets'/'js').mkdir(parents=True)
    (OUT/'index.html').write_text(materialize_index(),encoding='utf-8')
    shutil.copy2(ROOT/'assets'/'styles.css',OUT/'assets'/'styles.css')
    shutil.copy2(ROOT/'assets'/'entry.js',OUT/'assets'/'entry.js')
    (OUT/'assets'/'catalog.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (OUT/'assets'/'catalog.js').write_text(catalog_javascript(rows),encoding='utf-8')
    for group,outname in [('app','app.js'),('services','services.js'),('player','player.js'),('bootstrap','bootstrap.js')]:
        code=assemble(group)
        if not code.strip():
            raise SystemExit(f'Módulo vazio: {group}')
        (OUT/'assets'/'js'/outname).write_text(code,encoding='utf-8')
    return rows


if __name__=='__main__':
    rows=build()
    print(f'OK: {len(rows)} faixas; auditoria {AUDIT_START}–{AUDIT_END}=63/63; site {VERSION} gerado em {OUT}')
