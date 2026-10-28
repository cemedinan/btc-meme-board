# Daily update procedure

Live: https://cemedinan.github.io/btc-meme-board/ · Repo: https://github.com/cemedinan/btc-meme-board (Pages: legacy, branch `main`, path `/`).
The page (`index.html`) is static and renders `data/memes.json` client-side, same theme as `x-virality-board`. Do not edit HTML for daily updates.

## 1. Find 5 new memes (manual / agent step)
- Use the X search tool (`x` → `search_posts_all`) with `start_time` = now − 7 days, `post.fields=public_metrics,created_at,author_id`, `expansions=author_id`, `user.fields=username`, `sort_order=relevancy`.
- Useful queries: Bitcoin comedy accounts (`from:MandelDuck OR from:sunxliao ...`), humor keywords (`(bitcoin OR btc) (meme OR lol OR 😂) lang:en -is:retweet -is:reply`), timely jokes (Halloween, Thanksgiving, "Bitcoin is dead", leverage, HODL).
- Keep only real humor/memes about Bitcoin (no news, shilling, giveaways, token promos). Prefer English. Rank by impressions, else likes+reposts+replies.
- Skip ids already in `data/memes.json` (the script also skips them).

## 2. Create 5 images
- GenerateImage, 16:9, flat cartoon, white background with green #1B7F1B / blue #3366CC accents, one short monospace caption. Original concept recreation; never re-host the author's media; no real people. Check each image visually.

## 3. Write incoming JSON
Create e.g. `/workspace/btc-incoming/YYYY-MM-DD.json` — a list of objects:
```json
{"id":"…","username":"handle","author":"handle","created_at":"2026-10-25T09:36:00Z",
 "url":"https://x.com/handle/status/…","text":"joke text","metrics":{"impression_count":0,"like_count":0,"repost_count":0,"reply_count":0},
 "suggested_post":"close paraphrase in @ForecastQuant's voice: direct, simple, one idea, English, no hashtag spam, no new facts",
 "image_src":"/path/to/generated.jpg","image_alt":"short description"}
```

## 4. Run the script
```
cd /workspace/btc-meme-board && git pull && python3 update.py /workspace/btc-incoming/YYYY-MM-DD.json
```
It: compresses images to `images/YYYY-MM-DD-N.jpg` (Santiago date), adds entries with `added`=today, removes entries whose post `created_at` is older than 7 days and deletes their images, sorts, updates `meta`, then `git commit` + `git push`. Add `--no-push` to test locally. Running with no file just prunes and pushes.

## 5. Verify
`curl -s -o /dev/null -w '%{http_code}' https://cemedinan.github.io/btc-meme-board/data/memes.json` → 200 (Pages rebuild takes ~1 min).
