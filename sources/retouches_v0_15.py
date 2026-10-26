"""Arkerion Sans 0.15 — nouveau G (variante « G1a »).

Pourquoi : l'ancien G (703 unités) était étroit et anguleux à côté du O élargi.

- Même construction que le O : quarts d'ovale en cubiques, mêmes épaisseurs
  (extérieur ry 362, intérieur ry 286), sur un ovale 50 unités plus étroit.
  Le G est ainsi un peu plus serré que le O, la proportion classique.
- Terminal du haut coupé à l'horizontale (y 520).
- Côté droit arrondi jusqu'en haut de la barre ; barre horizontale
  (y 300 à 376) qui s'arrête dans le trait, sans fût.
- 750 unités de chasse.

Dans le fichier de police, la version est notée 0.960.

Usage : python3 retouches_v0_15.py ArkerionSans-Regular.otf sortie.otf
"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.reverseContourPen import ReverseContourPen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retouches_v0_2 as R2   # split, t_for_y

NARROW = 50                       # unités retirées à la largeur du O
YT, BAR_X0, BAR_Y0, BAR_TH = 520, 420, 300, 76


def area(p): return sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(p, p[1:]+p[:1]))/2


def draw(pen, segs):
    pts = [segs[0][1]] + [s[-1] for s in segs]
    t = pen if area(pts) > 0 else ReverseContourPen(pen)
    R = lambda p: (round(p[0]), round(p[1]))
    t.moveTo(R(segs[0][1]))
    for s in segs:
        if s[0] == 'L': t.lineTo(R(s[2]))
        else: t.curveTo(R(s[2]), R(s[3]), R(s[4]))
    t.closePath()


def rect(pen, x0, y0, x1, y1):
    draw(pen, [('L', (x0, y0), (x1, y0)), ('L', (x1, y0), (x1, y1)),
               ('L', (x1, y1), (x0, y1)), ('L', (x0, y1), (x0, y0))])


def ellipse_segments(cx, cy, rxo, ryo, rxi, ryi, k=0.592, ki=0.612):
    """Quarts d'ovale comme le O : extérieur E→N→W→S→E, intérieur E→S→W→N→E."""
    q = lambda a, b, ca, cb: ('C', a, ca, cb, b)
    E, N, W, S = (cx+rxo, cy), (cx, cy+ryo), (cx-rxo, cy), (cx, cy-ryo)
    outer = [q(E, N, (cx+rxo, cy+ryo*k), (cx+rxo*k, cy+ryo)), q(N, W, (cx-rxo*k, cy+ryo), (cx-rxo, cy+ryo*k)),
             q(W, S, (cx-rxo, cy-ryo*k), (cx-rxo*k, cy-ryo)), q(S, E, (cx+rxo*k, cy-ryo), (cx+rxo, cy-ryo*k))]
    e, n, w, s = (cx+rxi, cy), (cx, cy+ryi), (cx-rxi, cy), (cx, cy-ryi)
    inner = [q(e, s, (cx+rxi, cy-ryi*ki), (cx+rxi*ki, cy-ryi)), q(s, w, (cx-rxi*ki, cy-ryi), (cx-rxi, cy-ryi*ki)),
             q(w, n, (cx-rxi, cy+ryi*ki), (cx-rxi*ki, cy+ryi)), q(n, e, (cx+rxi*ki, cy+ryi), (cx+rxi, cy+ryi*ki))]
    return outer, inner


def g_glyph(pen):
    # O : extérieur 53..746 (rx 346,5 ; ry 362), intérieur rx 257, ry 286, centre y 350
    rxo, rxi = 346.5 - NARROW/2, 257 - NARROW/2
    outer, inner = ellipse_segments(53 + rxo, 350, rxo, 362, rxi, 286)
    o1, o2, o3, o4 = outer
    i1, i2, i3, i4 = inner
    _, o1b = R2.split(o1, R2.t_for_y(o1, YT))        # de la coupe jusqu'en haut
    i4a, _ = R2.split(i4, R2.t_for_y(i4, YT))
    bt = BAR_Y0 + BAR_TH                                # le côté droit monte jusqu'au haut de la barre
    o1a, _ = R2.split(o1, R2.t_for_y(o1, bt))
    _, i4b = R2.split(i4, R2.t_for_y(i4, bt))
    draw(pen, [o1b, o2, o3, o4, o1a, ('L', o1a[-1], i4b[1]), i4b, i1, i2, i3, i4a, ('L', i4a[-1], o1b[1])])
    rect(pen, BAR_X0 - NARROW/2, BAR_Y0, i1[1][0] + 45, BAR_Y0 + BAR_TH)   # barre, arrêtée dans le trait


def main(src, dst):
    f = TTFont(src)
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    adv = f['hmtx']['O'][0] - NARROW
    pen = T2CharStringPen(adv, None)
    g_glyph(pen)
    cs['G'] = pen.getCharString(private=cs['G'].private, globalSubrs=cs['G'].globalSubrs)
    f['hmtx']['G'] = (adv, f['hmtx']['O'][1])
    f['head'].fontRevision = 0.96
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.960; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.950', '0.960')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
