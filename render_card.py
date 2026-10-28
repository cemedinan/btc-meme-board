#!/usr/bin/env python3
"""Render a brand meme card (navy/white/lime, 1080x1080).
python3 render_card.py out.jpg "WHITE LINE" "LIME LINE" [motif]
motif: binoculars | plane | tombstone | loop | ticket | none"""
import sys
from PIL import Image, ImageDraw, ImageFont
NAVY=(11,11,43); NAVY2=(28,28,72); NAVY3=(48,48,100); WHITE=(242,242,245); LIME=(197,229,35)
F='/usr/share/fonts/truetype/sand-box/google/IBM Plex Mono/IBMPlexMono-Bold.ttf'
def fit(d,t,maxw,start):
    s=start
    while s>30:
        f=ImageFont.truetype(F,s)
        if d.textlength(t,font=f)<=maxw: return f
        s-=4
    return ImageFont.truetype(F,s)
def motif(d,m):
    cx,cy=540,400
    if m=='binoculars':
        for dx in (-130,130): d.ellipse([cx+dx-120,cy-120,cx+dx+120,cy+120],outline=WHITE,width=14); d.ellipse([cx+dx-60,cy-60,cx+dx+60,cy+60],fill=NAVY3)
        d.rectangle([cx-30,cy-30,cx+30,cy+30],fill=WHITE); d.ellipse([cx+100,cy-40,cx+140,cy],fill=LIME)
    elif m=='plane':
        d.line([(160,cy+90),(920,cy+90)],fill=NAVY3,width=6)
        d.polygon([(380,cy+40),(700,cy-80),(740,cy-60),(430,cy+70)],fill=WHITE)
        d.polygon([(540,cy-10),(470,cy-150),(510,cy-155),(620,cy-40)],fill=WHITE)
        d.polygon([(560,cy+10),(520,cy+120),(560,cy+120),(640,cy-10)],fill=NAVY3)
        d.ellipse([720,cy-180,800,cy-100],fill=LIME)
    elif m=='tombstone':
        d.rounded_rectangle([390,cy-170,690,cy+150],radius=150,fill=NAVY3); d.rectangle([390,cy,690,cy+150],fill=NAVY3)
        d.text((540,cy-40),'RIP',font=ImageFont.truetype(F,80),fill=WHITE,anchor='mm')
        d.text((540,cy+50),'x13',font=ImageFont.truetype(F,56),fill=LIME,anchor='mm'); d.line([(300,cy+150),(780,cy+150)],fill=WHITE,width=8)
    elif m=='loop':
        d.arc([360,cy-180,720,cy+180],20,340,fill=WHITE,width=18); d.polygon([(700,cy-100),(760,cy-40),(680,cy-30)],fill=LIME)
        d.text((540,cy),'$',font=ImageFont.truetype(F,150),fill=LIME,anchor='mm')
    elif m=='ticket':
        d.rounded_rectangle([300,cy-130,780,cy+130],radius=24,outline=WHITE,width=12)
        for y in range(cy-110,cy+120,30): d.line([(620,y),(620,y+14)],fill=WHITE,width=6)
        d.text((460,cy),'BTC\nCONF',font=ImageFont.truetype(F,56),fill=WHITE,anchor='mm',align='center'); d.text((700,cy),'×',font=ImageFont.truetype(F,120),fill=LIME,anchor='mm')
def main(out,l1,l2,m='none'):
    im=Image.new('RGB',(1080,1080),NAVY); d=ImageDraw.Draw(im)
    d.rectangle([0,0,1080,1080],outline=NAVY2,width=36)
    motif(d,m)
    f1=fit(d,l1,900,72); f2=fit(d,l2,900,96)
    d.text((540,760),l1,font=f1,fill=WHITE,anchor='mm')
    bb=d.textbbox((540,870),l2,font=f2,anchor='mm'); d.rectangle([bb[0]-18,bb[1]-14,bb[2]+18,bb[3]+14],fill=LIME)
    d.text((540,870),l2,font=f2,fill=NAVY,anchor='mm')
    import sys as _s,os as _o; _s.path.insert(0,_o.path.dirname(_o.path.abspath(__file__))); import watermark; im=watermark.apply(im)
    im.save(out,'JPEG',quality=88)
if __name__=='__main__': main(*sys.argv[1:])
