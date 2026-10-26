"""Arkerion Sans v0.9 — nouveau a (validé : variante « J4 »).

Pourquoi : même élargi en v0.6, le a gardait une petite panse ovale et basse
et un crochet coupé à la verticale ; à côté du p et du g, il paraissait coincé.

Le a est redessiné sur les principes de celui de JetBrains Mono, avec des
courbes propres à Arkerion (aucun point repris) :
- grande panse au dessus plat (jusqu'à y = 338), côté gauche et bas pleins ;
- crochet en demi-ovale, coupé à l'horizontale à y = 380 ;
- raccord en biseau entre la panse et le fût, au-dessus de la ligne de base ;
- 572 unités de chasse, comme le p et le g.
À et â suivent (accent recentré sur la nouvelle lettre).

Usage : python3 retouches_v0_9.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from retouches_v0_6 import contours

# Paramètres du a « J4 »
P = dict(L_bowl=44, Lh=78, s1=520, bowl_top=338, cy=380)
ADV = 572
SW, XH = 82, 532            # fût et hauteur d'x
TOP_TH, SIDE = 72, 85       # épaisseurs du crochet : dessus, côtés
BOWL_TH, BOWL_SIDE, BOWL_BOT = 70, 86, 72
K, KI = 0.58, 0.60          # tension du crochet (extérieur, intérieur)
BK = 0.66                   # tension de la panse : plus pleine qu'une ellipse


def area(pts):
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1])) / 2


class Contour:
    """Contour en segments, dessiné dans le bon sens (plein : antihoraire, creux : horaire)."""

    def __init__(self, start):
        self.start, self.segs = start, []

    def L(self, p):
        self.segs.append(('L', p)); return self

    def C(self, c1, c2, p):
        self.segs.append(('C', c1, c2, p)); return self

    def draw(self, pen, hole=False):
        ccw = area([self.start] + [s[-1] for s in self.segs]) > 0
        target = pen if ccw != hole else ReverseContourPen(pen)
        R = lambda p: (round(p[0]), round(p[1]))
        target.moveTo(R(self.start))
        for s in self.segs:
            if s[0] == 'L':
                target.lineTo(R(s[1]))
            else:
                target.curveTo(R(s[1]), R(s[2]), R(s[3]))
        target.closePath()


def shapes(L_bowl, Lh, s1, bowl_top, cy):
    s0 = s1 - SW
    # crochet : demi-ovale du bout gauche (coupe horizontale à cy) jusqu'au fût
    rxo = (s1 - Lh) / 2; cx = Lh + rxo; ryo = XH + 10 - cy
    rxi = rxo - SIDE; ryi = ryo - TOP_TH
    hook = (Contour((Lh, cy)).L((Lh + SIDE, cy))
            .C((Lh + SIDE, cy + ryi * KI), (cx - rxi * KI, cy + ryi), (cx, cy + ryi))
            .C((cx + rxi * KI, cy + ryi), (s0, cy + ryi * KI), (s0, cy))
            .L((s0, cy - 40)).L((s1, cy - 40)).L((s1, cy))
            .C((s1, cy + ryo * K), (cx + rxo * K, cy + ryo), (cx, cy + ryo))
            .C((cx - rxo * K, cy + ryo), (Lh, cy + ryo * K), (Lh, cy)))
    stem = Contour((s0, 0)).L((s1, 0)).L((s1, cy)).L((s0, cy))
    # panse : dessus plat, gauche et bas arrondis, raccord en biseau dans le fût
    ft = round(L_bowl + (s0 - L_bowl) * 0.48)      # fin du plat du dessus
    bc = round(L_bowl + (s0 - L_bowl) * 0.5)       # point bas
    ym = round(bowl_top * 0.47)                    # point le plus à gauche
    outer = (Contour((s0 + 20, bowl_top)).L((ft, bowl_top))
             .C((ft - (ft - L_bowl) * BK, bowl_top), (L_bowl, ym + (bowl_top - ym) * BK), (L_bowl, ym))
             .C((L_bowl, ym - (ym + 10) * BK), (bc - (bc - L_bowl) * BK, -10), (bc, -10))
             .C((bc + (s0 - bc) * 0.6, -10), (s0 + 5, 30), (s0 + 20, 95)))
    it, Li, ib = bowl_top - BOWL_TH, L_bowl + BOWL_SIDE, -10 + BOWL_BOT
    inner = (Contour((s0 + 10, it)).L((ft + 10, it))
             .C((ft + 10 - (ft + 10 - Li) * BK, it), (Li, ym + (it - ym) * BK), (Li, ym))
             .C((Li, ym - (ym - ib) * BK), (bc + 10 - (bc + 10 - Li) * BK, ib), (bc + 10, ib))
             .C((bc + 10 + (s0 - bc) * 0.6, ib), (s0 + 10, ib + 55), (s0 + 10, 175)))
    return [(stem, False), (hook, False), (outer, False), (inner, True)]


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    old = contours(gs['a'])
    bp = BoundsPen(gs); gs['a'].draw(bp)
    dx = (P['L_bowl'] + P['s1']) / 2 - (bp.bounds[0] + bp.bounds[2]) / 2
    items = shapes(**P)
    for g in ('a', 'agrave', 'acircumflex'):
        pen = T2CharStringPen(ADV, None)
        for c, hole in items:
            c.draw(pen, hole)
        if g != 'a':
            for c in contours(gs[g]):
                if c in old:
                    continue
                for op, a in c:
                    if op == 'closePath':
                        pen.closePath()
                    else:
                        getattr(pen, op)(*[(round(x + dx), round(y)) for x, y in a])
        cs[g] = pen.getCharString(private=cs[g].private, globalSubrs=cs[g].globalSubrs)
        f['hmtx'][g] = (ADV, P['L_bowl'])

    f['head'].fontRevision = 0.9
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.900; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.800', '0.900')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
