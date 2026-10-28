#!/usr/bin/env python3
"""Joke card, brand style: python3 render_joke.py out.jpg "SETUP (white)" "PUNCHLINE (lime)"
1080x1080 navy #0B0B2B, white #F2F2F5 setup, big lime #C5E523 punchline, brand watermark (assets/logo-watermark.png) bottom-right."""
import sys
sys.path.insert(0,__file__.rsplit('/',1)[0])
from PIL import Image, ImageDraw
from render_meme import draw_block, NAVY, WHITE, LIME
def main(out,setup,punch):
    S=1080; c=Image.new('RGB',(S,S),NAVY); d=ImageDraw.Draw(c)
    d.rectangle([24,24,S-24,S-24],outline=(37,37,90),width=4)
    draw_block(d,(90,170,S-90,470),setup.upper(),fill=WHITE,start=84)
    d.rectangle([90,520,250,532],fill=LIME)
    draw_block(d,(90,570,S-90,960),punch.upper(),fill=LIME,start=150)
    import watermark; c=watermark.apply(c)
    c.save(out,'JPEG',quality=88,optimize=True)
if __name__=='__main__': main(*sys.argv[1:4])
