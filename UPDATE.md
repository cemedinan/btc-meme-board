# Daily update procedure

Live: https://cemedinan.github.io/btc-meme-board/ · Repo: https://github.com/cemedinan/btc-meme-board (Pages: legacy, branch `main`, path `/`).
The page (`index.html`) is static and renders `data/memes.json` client-side, same layout as `x-virality-board`, restyled navy/white/lime. Do not edit HTML for daily updates.

## 1. Find candidates and check 😂 replies (agent step)
- Search candidates with `x` → `search_posts_all` (`start_time` = now − 7 days, `post.fields=public_metrics,created_at`, `expansions=author_id`, `user.fields=username`, `sort_order=relevancy`). Good sources: Bitcoin comedy accounts (`from:MandelDuck OR from:pete_rizzo_ OR from:CryptoWendyO OR from:sunxliao ...`), humor keywords (`(bitcoin OR btc) (meme OR lol OR 😂) lang:en -is:retweet -is:reply`).
- Keep only real humor/memes about Bitcoin in English (no news, shilling, giveaways, token promos).
- **Qualifying rule:** the post must have at least one reply containing 😂. Check with one batched search:
  `(conversation_id:ID1 OR conversation_id:ID2 ...) 😂 is:reply`, `post.fields=referenced_tweets`, follow `next_token`.
  Count replies whose text has 😂 and whose `referenced_tweets[replied_to].id` is the candidate (`conversation_id` is not returned, so this counts direct replies only).
- Rank by 😂 replies seen, then impressions. Take the top 5; if fewer than 5 qualify, publish only those and say so in the report.
- Store `laugh_replies` (int) and `laugh_note: "seen"` (it is a sample count from search).

## 2. Suggested posts: comedian voice, 2 versions
Write as the best stand-up comedian in the world, for a Bitcoin audience, in English:
premise → twist → kicker. Sharp, sarcastic, original, few words. Same joke territory as the source, but clearly better wording; never copy verbatim.
No invented facts, no claims about video/image contents you cannot see (for video posts write an independent joke on the theme), no hashtag spam, no motivational fluff, no price predictions or financial advice, no real people's likenesses.
Provide `suggested_post` (primary) and `suggested_alt` (alternative); each gets its own copy button.

## 3. Images: navy / white / lime art direction
Square 1080×1080 JPG. Deep navy background #0B0B2B, accents only white #F2F2F5 and lime #C5E523 plus navy tints (#1C1C48, #303064). Flat, minimal, bold geometric/editorial, lots of negative space, high contrast. Short punchline: white line + lime highlight line. Small chevron-up mark (lime over white) top right. No multicolor, no gradients, no photoreal people.
Preferred (exact control): `python3 render_card.py out.jpg "WHITE LINE" "LIME LINE" <motif>` (motifs: binoculars, plane, ticket, tombstone, loop, none; add new motifs in the script as needed). If using GenerateImage instead, spell out this palette strictly and Read every image; regenerate any that stray.

## 3b. Incoming JSON
Create e.g. `/workspace/btc-incoming/YYYY-MM-DD.json` — a list of objects:
```json
{"id":"…","username":"handle","author":"handle","created_at":"2026-10-25T09:36:00Z",
 "url":"https://x.com/handle/status/…","text":"joke text","metrics":{"impression_count":0,"like_count":0,"repost_count":0,"reply_count":0},
 "laugh_replies":3,"laugh_note":"seen",
 "suggested_post":"primary","suggested_alt":"alternative",
 "image_src":"/path/to/card.jpg","image_alt":"short description"}
```

## 4. Run the script
```
cd /workspace/btc-meme-board && git pull && python3 update.py /workspace/btc-incoming/YYYY-MM-DD.json
```
It: compresses images to `images/YYYY-MM-DD-N.jpg` (Santiago date), adds entries with `added`=today, removes entries whose post `created_at` is older than 7 days and deletes their images, sorts, updates `meta`, then `git commit` + `git push`. Add `--no-push` to test locally. Running with no file just prunes and pushes.

## 5. Verify
`curl -s -o /dev/null -w '%{http_code}' https://cemedinan.github.io/btc-meme-board/data/memes.json` → 200 (Pages rebuild takes ~1 min).

## Rule: suggested posts
- Never rely on video (or image) contents you cannot see. Use only what is in the post's text/title.
- For video posts, write an independent, original, text-only Bitcoin joke on the same theme that stands on its own and makes no claim about what the video shows.
- Never add details, numbers or facts that are not in the source.
