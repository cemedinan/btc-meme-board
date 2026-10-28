#!/usr/bin/env python3
"""Daily update for BTC Meme Board.
Usage: python3 update.py [incoming.json] [--no-push]
Optional: --day=YYYY-MM-DD to override the Santiago date label.
incoming.json: list of 5 original entries (see UPDATE.md). Each needs id (e.g. 2026-10-28-j1),
type (JOKE|MEME), format, timeliness (EVERGREEN|CURRENT), hook (one line, CURRENT only),
suggested_post, suggested_alt, image_src (path to the rendered image on the box), image_alt.
Merges (skipping ids already present), compresses images to images/YYYY-MM-DD-N.jpg,
prunes posts older than 7 days (and their images), stamps meta, commits and pushes."""
import json, sys, os, subprocess, datetime as dt
from PIL import Image
R = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(R, 'data', 'memes.json')
now = dt.datetime.now(dt.timezone.utc)
today = now.astimezone(dt.timezone(dt.timedelta(hours=-3))).strftime('%Y-%m-%d')  # Santiago date label
def P(s): return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
db = json.load(open(DATA)) if os.path.exists(DATA) else {"meta": {}, "entries": []}
args = [a for a in sys.argv[1:] if not a.startswith('--')]
added = 0
for a in sys.argv:
    if a.startswith('--day='): today = a[6:]
os.makedirs(os.path.join(R, 'images'), exist_ok=True)
if args:
    have = {e['id'] for e in db['entries']}
    n = 0
    for e in json.load(open(args[0])):
        if e['id'] in have: print('skip existing', e['id']); continue
        n += 1
        while os.path.exists(os.path.join(R, 'images', f'{today}-{n}.jpg')): n += 1
        rel = f'images/{today}-{n}.jpg'
        im = Image.open(e.pop('image_src')).convert('RGB'); im.thumbnail((1200, 1200))
        im.save(os.path.join(R, rel), 'JPEG', quality=82, optimize=True, progressive=True)
        e['image'] = rel; e['added'] = today; e.setdefault('created_at', now.strftime('%Y-%m-%dT%H:%M:%SZ')); db['entries'].append(e); have.add(e['id']); added += 1
cut = now - dt.timedelta(days=7); keep = []
for e in db['entries']:
    if P(e.get('created_at') or e['added'] + 'T12:00:00Z') < cut:
        p = os.path.join(R, e.get('image', ''))
        if e.get('image') and os.path.exists(p): os.remove(p)
        print('pruned', e['id'])
    else: keep.append(e)
keep.sort(key=lambda e: e['id']); keep.sort(key=lambda e: e['added'], reverse=True)  # newest day first; j1,j2,m1..m3
db['entries'] = keep
db['meta'] = {"generated_at": now.strftime('%Y-%m-%dT%H:%M:%SZ'), "latest_day": max([e['added'] for e in keep], default=today), "window_days": 7}
json.dump(db, open(DATA, 'w'), ensure_ascii=False, indent=1)
print(f'added {added}, total {len(keep)}')
if '--no-push' not in sys.argv:
    g = lambda *a: subprocess.run(['git', '-C', R, *a], check=True)
    g('add', '-A')
    if subprocess.run(['git', '-C', R, 'diff', '--cached', '--quiet']).returncode:
        g('commit', '-m', f'daily update {today}'); g('push', 'origin', 'HEAD:main')
