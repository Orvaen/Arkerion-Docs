"""Arkerion Sans 0.10 — s et S redressés (validé : variante « S4 »).

Pourquoi : le s et le S de la v0.1 penchaient. Leur boucle du haut était
décalée à gauche, celle du bas à droite, leurs deux bouts coupés en biais
dans le même sens, et leur contour était une suite de ~300 petits segments.

Nouveau dessin, en vraies courbes :
- symétrie de rotation parfaite : la moitié du bas est celle du haut tournée
  de 180° autour du centre, donc la lettre est droite ;
- bouts coupés à l'horizontale, comme le a et le r ;
- épine assez à plat ; s : 427 unités de chasse, S : 562.

Dans le fichier de police, la version est notée 0.910 (« 0.10 » se lirait 0.1).

Usage : python3 retouches_v0_10.py ArkerionSans-Regular.otf sortie.otf
"""
import sys, math
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.reverseContourPen import ReverseContourPen

def area(p): return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2

def s_contour(x0, x1, top, bot, yT, yL, th, side, ts, ang, k=0.6):
    """s à symétrie de rotation : côté A (du bout haut extérieur au bout bas intérieur),
    puis le même côté tourné de 180°. Bouts coupés à l'horizontale."""
    cx, cy = (x0+x1)/2, (top+bot)/2
    rot = lambda p: (2*cx-p[0], 2*cy-p[1])
    a = math.radians(ang)
    u = (math.cos(a), -math.sin(a))             # direction de l'épine (descend vers la droite)
    n = (math.sin(a), math.cos(a))              # normale vers le haut
    Ml = (cx - n[0]*ts/2, cy - n[1]*ts/2)       # bord bas-gauche de l'épine au centre
    yR = 2*cy - yL                              # extremum droit de la boucle basse
    yB = 2*cy - yT                              # hauteur de la coupe du bout bas
    segs = []
    P = (x1, yT)                                 # bout haut, côté extérieur
    def C(c1, c2, p):
        nonlocal P; segs.append((c1, c2, p)); P = p
    C((x1, yT+(top-yT)*k), (cx+(x1-cx)*k, top), (cx, top))                 # A1
    C((cx-(cx-x0)*k, top), (x0, yL+(top-yL)*k), (x0, yL))                  # A2
    d1 = math.dist((x0, yL), Ml)
    C((x0, yL-(yL-Ml[1])*0.55), (Ml[0]-u[0]*d1*0.42, Ml[1]-u[1]*d1*0.42), Ml)   # A3
    E = (x1-side, yR); d2 = math.dist(Ml, E)
    C((Ml[0]+u[0]*d2*0.42, Ml[1]+u[1]*d2*0.42), (E[0], yR+(Ml[1]-yR)*0.55), E)   # A4
    ib = bot + th
    C((E[0], yR-(yR-ib)*k), (cx+(E[0]-cx)*k, ib), (cx, ib))                 # A5
    C((cx-(cx-(x0+side))*k, ib), (x0+side, ib+(yB-ib)*k), (x0+side, yB))   # A6
    # contour complet : A, coupe du bout bas, A tourné, coupe du bout haut
    start = (x1, yT)
    pts = [start]; cmds = []
    for c1, c2, p in segs: cmds.append(('C', c1, c2, p))
    rstart = rot(start)
    cmds.append(('L', rstart))
    for c1, c2, p in segs: cmds.append(('C', rot(c1), rot(c2), rot(p)))
    return start, cmds

def draw(pen, start, cmds):
    poly = [start] + [c[-1] for c in cmds]
    target = pen if area(poly) > 0 else ReverseContourPen(pen)
    R = lambda p: (round(p[0]), round(p[1]))
    target.moveTo(R(start))
    for c in cmds:
        if c[0] == 'L': target.lineTo(R(c[1]))
        else: target.curveTo(R(c[1]), R(c[2]), R(c[3]))
    target.closePath()


# Paramètres validés (« S4 »)
LOWER = dict(x0=40, x1=385, top=542, bot=-10, yT=404, yL=408, th=70, side=82, ts=72, ang=13)
UPPER = dict(x0=40, x1=520, top=712, bot=-12, yT=534, yL=538, th=76, side=88, ts=78, ang=12)
ADV = {'s': 427, 'S': 562}


def main(src, dst):
    f = TTFont(src)
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    for g, p in (('s', LOWER), ('S', UPPER)):
        pen = T2CharStringPen(ADV[g], None)
        draw(pen, *s_contour(**p))
        cs[g] = pen.getCharString(private=cs[g].private, globalSubrs=cs[g].globalSubrs)
        f['hmtx'][g] = (ADV[g], p['x0'])
    f['head'].fontRevision = 0.91
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.910; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.900', '0.910')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
