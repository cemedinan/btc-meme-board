#!/usr/bin/env python3
"""Daily update for BTC Meme Board.
Usage: python3 update.py [incoming.json] [--no-push]
incoming.json: list of new entries (see UPDATE.md). Each needs id, username, author, text,
created_at (ISO UTC), url, metrics{impression_count,like_count,repost_count,reply_count},
suggested_post, image_src (path to a generated image on the box), image_alt.
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
        e['image'] = rel; e['added'] = today; db['entries'].append(e); have.add(e['id']); added += 1
cut = now - dt.timedelta(days=7); keep = []
for e in db['entries']:
    if P(e['created_at']) < cut:
        p = os.path.join(R, e.get('image', ''))
        if e.get('image') and os.path.exists(p): os.remove(p)
        print('pruned', e['id'])
    else: keep.append(e)
db['entries'] = sorted(keep, key=lambda e: (e['added'], e['metrics'].get('impression_count', 0)), reverse=True)
db['meta'] = {"generated_at": now.strftime('%Y-%m-%dT%H:%M:%SZ'), "latest_day": max([e['added'] for e in keep], default=today), "window_days": 7}
json.dump(db, open(DATA, 'w'), ensure_ascii=False, indent=1)
print(f'added {added}, total {len(keep)}')
if '--no-push' not in sys.argv:
    g = lambda *a: subprocess.run(['git', '-C', R, *a], check=True)
    g('add', '-A')
    if subprocess.run(['git', '-C', R, 'diff', '--cached', '--quiet']).returncode:
        g('commit', '-m', f'daily update {today}'); g('push', 'origin', 'HEAD:main')
