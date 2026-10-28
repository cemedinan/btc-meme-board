#!/usr/bin/env python3
"""Brand watermark. RULE: never recreate/redraw the logo. Always composite assets/logo-watermark.png
(made from assets/logo-original.jpg by make_watermark.py). Only uniform resize (aspect kept) + opacity.
Bottom-right, margin 4% of width, logo width 9.5% of width, opacity 70%.
If the area behind is busy/bright, a subtle navy rounded plate (alpha ~45%) goes behind it.
CLI: python3 watermark.py in.jpg [out.jpg]"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageStat
LOGO=os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets','logo-watermark.png')
def apply(img, width_frac=0.095, margin_frac=0.04, opacity=0.70):
    img=img.convert('RGB'); W,H=img.size
    logo=Image.open(LOGO).convert('RGBA'); lw=round(W*width_frac); lh=round(logo.height*lw/logo.width)
    logo=logo.resize((lw,lh),Image.LANCZOS)
    a=logo.getchannel('A').point(lambda v:int(v*opacity)); logo.putalpha(a)
    m=round(W*margin_frac); x,y=W-m-lw,H-m-lh
    reg=img.crop((x,y,x+lw,y+lh)).convert('L'); st=ImageStat.Stat(reg)
    busy=st.stddev[0]>28 or st.mean[0]>90
    base=img.convert('RGBA')
    if busy:
        p=round(lw*0.18); plate=Image.new('RGBA',base.size,(0,0,0,0))
        ImageDraw.Draw(plate).rounded_rectangle([x-p,y-p,x+lw+p,y+lh+p],radius=round(p*1.3),fill=(11,11,43,115))
        base=Image.alpha_composite(base,plate)
    layer=Image.new('RGBA',base.size,(0,0,0,0)); layer.paste(logo,(x,y))
    return Image.alpha_composite(base,layer).convert('RGB')
if __name__=='__main__':
    o=sys.argv[2] if len(sys.argv)>2 else sys.argv[1]; apply(Image.open(sys.argv[1])).save(o,'JPEG',quality=88,optimize=True)
