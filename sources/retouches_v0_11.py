"""Arkerion Sans 0.11 — N à empattements (validé : variante « N2 »).

Le N rejoint le A dans le style à empattements, d'après un modèle choisi par
Arkerion (contours originaux) :
- fûts fins (58), diagonale épaisse (108 en chasse horizontale) qui finit en
  pointe en bas à droite, légèrement sous la ligne de base ;
- pied en bas à gauche, bec en haut à gauche, empattement en haut à droite,
  raccordés aux fûts par des congés courbes, mêmes mesures que le A.

Dans le fichier de police, la version est notée 0.920.

Usage : python3 retouches_v0_11.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen

SEAM=8
def area(p): return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2
def ccw(p): return p if area(p)>0 else p[::-1]

def N_shapes(L0, R1, ts, td, cap=700, tip=-12, ext=43, sh=32, fh=54):
    out=[]
    out.append(('poly',ccw([(L0,0),(L0+ts,0),(L0+ts,cap),(L0,cap)])))                 # fût gauche (fin)
    # diagonale épaisse : du haut gauche jusqu'à une pointe en bas à droite
    slope=(R1-L0)/(cap-tip)
    yh=cap-(R1-(L0+td))/slope                                                          # où le bord droit touche le fût droit
    out.append(('poly',ccw([(L0,cap),(L0+td,cap),(R1,yh),(R1,tip)])))
    out.append(('poly',ccw([(R1-ts,yh-40),(R1,yh-40),(R1,cap),(R1-ts,cap)])))          # fût droit (fin)
    # empattements
    out.append(('poly',ccw([(L0-ext*1.1,0),(L0+ts+ext*0.9,0),(L0+ts+ext*0.9,sh),(L0-ext*1.1,sh)])))     # pied gauche
    out.append(('poly',ccw([(L0-ext*1.1,cap-sh),(L0+4,cap-sh),(L0+4,cap),(L0-ext*1.1,cap)])))           # bec haut gauche
    out.append(('poly',ccw([(R1-ts-ext*0.9,cap-sh),(R1+ext*1.1,cap-sh),(R1+ext*1.1,cap),(R1-ts-ext*0.9,cap)])))  # haut droit
    def fillet(xe, ys, side, v, w):
        e=xe-side*SEAM
        E0=(e,ys); E1=(e,ys+v*fh); Sp=(xe+side*w,ys)
        c1=(e, ys+v*fh*0.4); c2=(xe+side*w*0.4, ys)
        return ('fil',(E0,E1,c1,c2,Sp))
    w=ext*0.75
    out+= [fillet(L0,sh,-1,1,w), fillet(L0+ts,sh,1,1,w),                 # pied gauche
           fillet(L0,cap-sh,-1,-1,w),                                     # bec haut gauche
           fillet(R1-ts,cap-sh,-1,-1,w), fillet(R1,cap-sh,1,-1,w)]       # haut droit
    return out

def draw(pen, items):
    R=lambda p:(round(p[0]),round(p[1]))
    for kind,d in items:
        if kind=='poly':
            pen.moveTo(R(d[0])); [pen.lineTo(R(p)) for p in d[1:]]; pen.closePath()
        else:
            E0,E1,c1,c2,Sp=d
            if area([E0,E1,Sp])>0:
                pen.moveTo(R(E0)); pen.lineTo(R(E1)); pen.curveTo(R(c1),R(c2),R(Sp))
            else:
                pen.moveTo(R(E0)); pen.lineTo(R(Sp)); pen.curveTo(R(c2),R(c1),R(E1))
            pen.closePath()


P = dict(L0=84, R1=656, ts=58, td=108)
ADV = 740


def main(src, dst):
    f = TTFont(src)
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    pen = T2CharStringPen(ADV, None)
    draw(pen, N_shapes(**P))
    cs['N'] = pen.getCharString(private=cs['N'].private, globalSubrs=cs['N'].globalSubrs)
    f['hmtx']['N'] = (ADV, round(P['L0'] - 43 * 1.1))
    f['head'].fontRevision = 0.92
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.920; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.910', '0.920')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
