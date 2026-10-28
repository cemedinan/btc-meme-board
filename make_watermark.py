#!/usr/bin/env python3
"""One-time: build assets/logo-watermark.png from assets/logo-original.jpg (NO redraw).
Alpha = projection of (pixel - navy bg) onto (ref color - bg), ref = lime or white (best fit);
colour un-premultiplied: F = (C - (1-a)*B)/a. Cropped to the chevrons' bbox + small margin."""
import numpy as np
from PIL import Image
im=np.asarray(Image.open('assets/logo-original.jpg').convert('RGB')).astype(float)
H,W,_=im.shape
B=np.median(np.concatenate([im[:40].reshape(-1,3),im[-40:].reshape(-1,3)]),0)
d=np.linalg.norm(im-B,axis=2)
lime=np.median(im[(d>150)&(im[...,2]<120)],0); white=np.median(im[(d>150)&(im[...,2]>200)],0)
best=None
for R in (lime,white):
    v=R-B; a=np.clip(((im-B)@v)/(v@v),0,1)
    res=np.linalg.norm(im-(B+a[...,None]*v),axis=2)
    best=(a,res) if best is None else (np.where(res<best[1],a,best[0]),np.minimum(res,best[1]))
a=best[0]; a[a<0.04]=0
F=np.clip((im-(1-a[...,None])*B)/np.maximum(a[...,None],1e-3),0,255)
ys,xs=np.where(a>0.5); m=int(0.02*W)
y0,y1,x0,x1=max(ys.min()-m,0),min(ys.max()+m,H),max(xs.min()-m,0),min(xs.max()+m,W)
out=np.dstack([F,a*255])[y0:y1,x0:x1].round().astype(np.uint8)
Image.fromarray(out,'RGBA').save('assets/logo-watermark.png')
print('bg',B.round(),'lime',lime.round(),'white',white.round(),'crop',(x0,y0,x1,y1))
# verification: recomposite on bg and diff vs original crop
comp=Image.new('RGB',(x1-x0,y1-y0),tuple(int(c) for c in B)); comp.paste(Image.fromarray(out,'RGBA'),(0,0),Image.fromarray(out,'RGBA'))
diff=np.abs(np.asarray(comp).astype(float)-im[y0:y1,x0:x1])
print('mean abs diff',diff.mean().round(2),'p99',np.percentile(diff,99).round(1),'max',diff.max())
