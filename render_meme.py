#!/usr/bin/env python3
"""Caption a meme template (output square 1080 JPG, navy frame + brand watermark from assets/logo-watermark.png).
band mode : python3 render_meme.py band template.jpg out.jpg "TOP CAPTION" ["BOTTOM CAPTION"]
  -> white caption band(s) with black bold text above/below the template.
drake mode: python3 render_meme.py drake template.jpg out.jpg "REJECTED TEXT" "APPROVED TEXT"
  -> text in the right half of each panel (for 2x2 Drake-style templates).
Templates: download public templates, e.g. curl -sL -A Mozilla/5.0 -o t.jpg https://i.imgflip.com/<id>.jpg
 (Drake 30b1gx, This is fine wxica, Waiting skeleton 2fm6x, Two buttons 1g8my4, Expanding brain 1jwhww,
  Distracted boyfriend 1ur9b0, Change my mind 24y43o, Always has been 46e43q, Gigachad: search imgflip)."""
import sys, os, textwrap
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import watermark
from PIL import Image, ImageDraw, ImageFont
NAVY=(11,11,43); WHITE=(242,242,245); LIME=(197,229,35); BLACK=(15,15,20)
FP='/usr/share/fonts/truetype/sand-box/google/Oswald/Oswald-VariableFont_wght.ttf'
def font(s):
    f=ImageFont.truetype(FP,s)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f
def wrap_fit(d,text,w,h,start=80):
    s=start
    while s>18:
        f=font(s); cpl=max(6,int(w/(s*0.5)))
        lines=textwrap.wrap(text,cpl)
        while lines and max(d.textlength(l,font=f) for l in lines)>w and cpl>6:
            cpl-=1; lines=textwrap.wrap(text,cpl)
        th=len(lines)*s*1.15
        if th<=h and max(d.textlength(l,font=f) for l in lines)<=w: return f,lines,s
        s-=3
    return f,lines,s
def draw_block(d,box,text,fill=BLACK,start=80):
    x0,y0,x1,y1=box; f,lines,s=wrap_fit(d,text,x1-x0,y1-y0,start)
    y=(y0+y1)/2-len(lines)*s*1.15/2
    for l in lines: d.text(((x0+x1)/2,y),l,font=f,fill=fill,anchor='ma'); y+=s*1.15
def finish(img,out):
    S=1080; c=Image.new('RGB',(S,S),NAVY); img.thumbnail((S-48,S-48),Image.LANCZOS)
    c.paste(img,((S-img.width)//2,(S-img.height)//2)); c=watermark.apply(c)
    c.save(out,'JPEG',quality=86,optimize=True)
def band(tpl,out,top,bottom=None):
    t=Image.open(tpl).convert('RGB'); W=1000; t=t.resize((W,int(t.height*W/t.width)),Image.LANCZOS)
    bh_t=(300 if t.height>t.width else 260) if len(top)>40 else 190; bh_b=(190 if bottom else 0)
    im=Image.new('RGB',(W,t.height+bh_t+bh_b),WHITE); im.paste(t,(0,bh_t)); d=ImageDraw.Draw(im)
    draw_block(d,(30,15,W-30,bh_t-15),top)
    if bottom: draw_block(d,(30,bh_t+t.height+15,W-30,im.height-15),bottom)
    finish(im,out)
def drake(tpl,out,a,b):
    t=Image.open(tpl).convert('RGB').resize((1000,1000),Image.LANCZOS); d=ImageDraw.Draw(t)
    for i,txt in enumerate((a,b)):
        d.rectangle([500,i*500,1000,i*500+500],fill=WHITE); draw_block(d,(530,i*500+30,970,i*500+(470 if i==0 else 350)),txt,start=72)  # keep watermark corner clear
    finish(t,out)
if __name__=='__main__':
    m=sys.argv[1]; {'band':band,'drake':drake}[m](*sys.argv[2:])
