#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
LEGACY=ROOT/'source'/'legacy.html'
EXPECTED=(ROOT/'tools'/'base_signature.txt').read_text().strip()

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

def build():
    tracks=load_project()
    patterns=load_patch('context_patterns.json')
    indices=load_patch('context_index_a.json')+load_patch('context_index_b.json')
    if len(indices)!=len(tracks): raise SystemExit('Índice de contexto incompatível')
    wiki_track=dict(load_patch('wiki_track.json'))
    wiki_pt=dict(load_patch('wiki_artist_pt.json'))
    wiki_en=dict(load_patch('wiki_artist_en.json'))
    rows=[]
    for i,t in enumerate(tracks):
        youtube_id=t.get('youtubeId')
        if t.get('artist')=='Júpiter Maçã' and t.get('title')=='A Marchinha Psicótica de Dr. Soup':
            youtube_id='3dEeAXY7nTs'
        targets=patterns[indices[i]]
        packed=[[x.get('kind'),x.get('pt'),x.get('en')] for x in targets]
        if len(packed)==1: packed=packed[0]
        row=[
            t.get('artist'),t.get('title'),t.get('year'),youtube_id,
            1 if t.get('catalogSource')=='brazil' else 0,
            packed,t.get('decadeRank'),t.get('yearPriority'),
            t.get('albumTitle'),t.get('albumUrl'),t.get('artworkMode'),
            t.get('artworkPageTitle'),t.get('artworkUrl'),t.get('lyricsPolicy'),
            wiki_track.get(i),wiki_pt.get(i),wiki_en.get(i)
        ]
        while row and row[-1] is None: row.pop()
        rows.append(row)
    ids=[r[3] for r in rows if len(r)>3 and r[3]]
    if len(ids)!=len(set(ids)): raise SystemExit('youtubeId duplicado')
    def find(a,title): return next((r for r in rows if r[0]==a and r[1]==title),None)
    black=find('Black Sabbath','Paranoid'); bee=find('Bee Gees',"Stayin' Alive")
    if not black or not any(x[1]=='Heavy metal' for x in ([black[5]] if isinstance(black[5][0],str) else black[5])): raise SystemExit('Contexto Black Sabbath inválido')
    if not bee or not any(x[1]=='Música disco' for x in ([bee[5]] if isinstance(bee[5][0],str) else bee[5])): raise SystemExit('Contexto Bee Gees inválido')
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT/'assets'/'js').mkdir(parents=True)
    shutil.copy2(ROOT/'index.html',OUT/'index.html')
    shutil.copy2(ROOT/'assets'/'styles.css',OUT/'assets'/'styles.css')
    shutil.copy2(ROOT/'assets'/'loader.js',OUT/'assets'/'loader.js')
    (OUT/'assets'/'catalog.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    for group,outname in [('app','app.js'),('services','services.js'),('player','player.js'),('bootstrap','bootstrap.js')]:
        code=assemble(group)
        if not code.strip(): raise SystemExit(f'Módulo vazio: {group}')
        (OUT/'assets'/'js'/outname).write_text(code,encoding='utf-8')
    return rows

if __name__=='__main__':
    rows=build()
    print(f'OK: {len(rows)} faixas; site modular gerado em {OUT}')
