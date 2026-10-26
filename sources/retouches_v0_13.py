"""Arkerion Sans 0.13 — nouveau y (validé : variante « Y2 »).

Pourquoi : le y de l'esquisse était fait de deux barres qui se croisaient ;
la branche gauche dépassait sous la jonction (petit pied parasite), et la
lettre restait étroite (421 unités) à côté des lettres élargies.

- Branche gauche arrêtée dans la branche droite : plus de pied parasite.
- Branche droite qui tourne en courbe vers un bras plat, comme la queue du g.
- 504 unités de chasse.

Dans le fichier de police, la version est notée 0.940.

Usage : python3 retouches_v0_13.py ArkerionSans-Regular.otf sortie.otf
"""
import sys, math
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.reverseContourPen import ReverseContourPen

XH, DESC = 532, -200
def area(p): return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2

def contour(pen, start, cmds):
    pts=[start]+[c[-1] for c in cmds]
    t = pen if area(pts)>0 else ReverseContourPen(pen)
    R=lambda p:(round(p[0]),round(p[1]))
    t.moveTo(R(start))
    for c in cmds:
        if c[0]=='L': t.lineTo(R(c[1]))
        else: t.curveTo(R(c[1]),R(c[2]),R(c[3]))
    t.closePath()

def y_glyph(pen, L, R, w, vx, vy, tail=None):
    """L, R : bords extérieurs en haut ; w : chasse horizontale des branches ;
    (vx, vy) : pointe du V (axe des branches)."""
    cl, cr = L + w/2, R - w/2                 # axes des branches en haut
    sl = (vx-cl)/(XH-vy)                      # dérive en x par unité de descente (gauche)
    sr = (cr-vx)/(XH-vy)                      # (droite)
    xr = lambda y, off: cr - w/2 + off - sr*(XH-y)       # bords de la branche droite
    xl = lambda y, off: cl - w/2 + off + sl*(XH-y)       # bords de la branche gauche
    # branche gauche : s'arrête dans la branche droite (pas de pied qui dépasse)
    d1=(xr(XH,0)-xl(XH,0))/(sl+sr); d2=(xr(XH,0)-xl(XH,w))/(sl+sr)
    contour(pen,(L,XH),[('L',(L+w,XH)),('L',(xl(XH-d2,w)+8,XH-d2)),('L',(xl(XH-d1,0)+8,XH-d1))])
    if tail is None:
        contour(pen,(R-w,XH),[('L',(R,XH)),('L',(xr(DESC,w),DESC)),('L',(xr(DESC,0),DESC))])
    else:
        yo, yi, end, th = tail            # où la courbe commence (bord ext./int.), bout du bras, épaisseur
        Po=(xr(yo,w),yo); Pi=(xr(yi,0),yi)
        n=math.hypot(sr,1); dx,dy=-sr/n,-1/n
        Bo=(Po[0]-175, DESC); Bi=(Pi[0]-130, DESC+th)
        contour(pen,(R-w,XH),[('L',(R,XH)),('L',Po),
            ('C',(Po[0]+dx*95,Po[1]+dy*95),(Bo[0]+85,DESC),Bo),
            ('L',(end,DESC)),('L',(end,DESC+th)),('L',Bi),
            ('C',(Bi[0]+70,DESC+th),(Pi[0]+dx*60,Pi[1]+dy*60),Pi)])


P = dict(L=14, R=490, w=86, vx=252, vy=20, tail=(-30, 10, 40, 72))
ADV = 504


def main(src, dst):
    f = TTFont(src)
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    pen = T2CharStringPen(ADV, None)
    y_glyph(pen, **P)
    cs['y'] = pen.getCharString(private=cs['y'].private, globalSubrs=cs['y'].globalSubrs)
    f['hmtx']['y'] = (ADV, P['L'])
    f['head'].fontRevision = 0.94
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.940; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.930', '0.940')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
