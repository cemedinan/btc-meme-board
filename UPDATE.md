# Daily update — BTC Meme Board (original content)

Every day: **2 JOKES + 3 MEMES**, all original, for @ForecastQuant (English). Nothing is posted to X.
No source posts, handles, links or metrics are stored or shown.

## 1. Find the news hook (5 min)
- X: `search_news` (query "bitcoin", max_age_hours 36) and `search_posts_all` for what people are joking about.
- Web: WebSearch "bitcoin news <today>".
- Use ONLY facts you verified this run (e.g. "Fed decision today", "searches at 5-year low").
  No invented numbers, no price predictions, no financial advice, nothing defamatory about real people
  (prefer not naming people at all).
- Mix: at least 1-2 items CURRENT (with hook), rest EVERGREEN (HODL, bear market, checking the price,
  self-custody, leverage pain, orange-pilling family, number go up, halving, 21 million).

## 2. Pick meme formats
- Famous, overused formats: Drake, This Is Fine, Waiting Skeleton, Two Buttons, Expanding Brain,
  Distracted Boyfriend, Change My Mind, Always Has Been, Gigachad, Wojak/NPC, Bernie...
- At least ONE trending now (WebSearch "trending meme format <month year>", X search "meme format").
  Many trends are video-only; then pick the closest still format and say so in `format`.
- Never Pepe or anything tied to hate/extremist symbols. Don't repeat a format used in the last 7 days.

## 3. Download templates
`curl -sL -A Mozilla/5.0 -o t.jpg https://i.imgflip.com/<id>.jpg` (ids listed in render_meme.py docstring;
or Know Your Meme / Wikimedia). If no download works, recreate the format with GenerateImage
(no real people's likenesses).

## 4. Voice brief
World's best stand-up: sharp, dry, sarcastic, tight setup → punchline, few words, English.
Never copy anyone's joke verbatim. Each item: `suggested_post` + a different `suggested_alt`.

## 5. Logo / watermark (RULE)
- NEVER recreate, redraw, recolor, stretch or crop the logo. The only source is
  `assets/logo-original.jpg`; `assets/logo-watermark.png` is its transparent cut-out (made once by
  `make_watermark.py`: alpha from distance to the navy bg, un-premultiplied colours, diff-checked).
- Every image gets it via `watermark.apply()` (already called by render_joke.py, render_meme.py,
  render_card.py; for any other image run `python3 watermark.py in.jpg out.jpg`):
  bottom-right, margin 4% of width, width 9.5% of width, opacity 70%, plus a subtle navy rounded plate
  automatically when the area behind is busy/bright. Keep captions out of the bottom-right corner.

## 5b. Art direction
- Jokes: `python3 render_joke.py out.jpg "SETUP" "PUNCHLINE"` — navy #0B0B2B, white #F2F2F5 setup,
  big lime #C5E523 punchline, logo watermark. Flat, minimal, nothing else.
- Memes: NOT minimal. `python3 render_meme.py band tpl.jpg out.jpg "TOP" ["BOTTOM"]` (caption band)
  or `python3 render_meme.py drake tpl.jpg out.jpg "NO" "YES"`. Output is framed in navy with the logo watermark.

## 6. Entry format (incoming.json, list of 5)
```json
{"id":"YYYY-MM-DD-j1","type":"JOKE|MEME","format":"Drake Hotline Bling","timeliness":"EVERGREEN|CURRENT",
 "hook":"one line, verified fact + source (CURRENT only, else \"\")",
 "suggested_post":"...","suggested_alt":"...","image_src":"/abs/path.jpg","image_alt":"..."}
```
ids: j1, j2, m1, m2, m3.

## 7. Run
`python3 update.py incoming.json` (add `--no-push` to test, `--day=YYYY-MM-DD` to override).
It compresses images to images/DATE-N.jpg, stamps added/created_at, prunes entries >7 days old with
their images, writes data/memes.json, commits and pushes.

## 8. Verify
- Read every image (contact sheet) before running; fix unreadable captions, typos, cropped text.
- After push (~1 min): HTTP 200 for https://cemedinan.github.io/btc-meme-board/, data/memes.json, every image.
- `google-chrome --headless --no-sandbox --window-size=900,2400 --virtual-time-budget=8000 --screenshot=shot.png URL`
  and look at it.
