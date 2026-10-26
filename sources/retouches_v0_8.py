"""Arkerion Sans v0.8 — p, q, b, d élargis et nouveau g (validé : variante « P2 »).

Pourquoi : depuis la v0.2, le p et ses cousins faisaient 510 unités, moins que
le o (581), le c, le a et le e élargis depuis. Le g, lui, était resté une
esquisse de la v0.1.

- p et b : +60 unités (570). Tous les points à droite de l'axe x = 279
  (sommet de l'arche, extremums haut et bas de la panse) s'écartent ;
  l'épaule et les épaisseurs ne changent pas. q et d sont leurs miroirs.
- g : la panse du q, un fût jusqu'à la hauteur d'x, puis une queue qui
  tourne en quart de cercle vers un bras plat jusqu'au bord gauche de la
  panse (même construction que le f de la v0.6, retournée).

Usage : python3 retouches_v0_8.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from retouches_v0_6 import contours, widen, charstring, replay

AXIS, WIDEN = 279, 60
STEM_W, XH, DESC, TH = 82, 532, -200, 72
TAIL_RO = 1.1        # rayon des courbes de la queue, comme le f « G2 »


def mirror(c, W):
    """Symétrie horizontale d'un contour enregistré ; le sens est rétabli."""
    segs, start, last = [], None, None
    for op, a in c:
        if op == 'moveTo':
            start = last = a[0]
        elif op == 'lineTo':
            segs.append(('L', last, a[0])); last = a[0]
        elif op == 'curveTo':
            segs.append(('C', last, a[0], a[1], a[2])); last = a[2]
        elif op == 'closePath' and last != start:
            segs.append(('L', last, start))
    segs = [(s[0],) + tuple((W - p[0], p[1]) for p in s[1:]) for s in segs]
    segs = [(s[0],) + tuple(reversed(s[1:])) for s in reversed(segs)]
    out = [('moveTo', [segs[0][1]])]
    for s in segs:
        out.append(('lineTo', [s[2]]) if s[0] == 'L' else ('curveTo', [s[2], s[3], s[4]]))
    out.append(('closePath', []))
    return out


def is_stem(c):
    xs = [p[0] for _, a in c for p in a]; ys = [p[1] for _, a in c for p in a]
    return (max(xs) - min(xs) == STEM_W and min(ys) <= -40 and max(ys) >= 500
            and all(op in ('moveTo', 'lineTo', 'closePath') for op, _ in c))


def rect(x0, y0, x1, y1):
    return [('moveTo', [(x0, y0)]), ('lineTo', [(x1, y0)]), ('lineTo', [(x1, y1)]),
            ('lineTo', [(x0, y1)]), ('closePath', [])]


def g_tail(s0, s1, L, ro=TAIL_RO, top=300):
    """Fût qui descend, quart de cercle vers la gauche, bras plat jusqu'à L (antihoraire)."""
    B, k = DESC, 0.55
    ji, xi = B + TH + round(68 * ro), s0 - round(61 * ro)     # courbe intérieure
    jo, xo = B + round(140 * ro), s1 - round(137 * ro)        # courbe extérieure
    return [('moveTo', [(s0, top)]), ('lineTo', [(s0, ji)]),
            ('curveTo', [(s0, round(ji - (ji - (B + TH)) * k)), (round(xi + (s0 - xi) * k), B + TH), (xi, B + TH)]),
            ('lineTo', [(L, B + TH)]), ('lineTo', [(L, B)]), ('lineTo', [(xo, B)]),
            ('curveTo', [(round(xo + (s1 - xo) * k), B), (s1, round(jo - (jo - B) * k)), (s1, jo)]),
            ('lineTo', [(s1, top)]), ('closePath', [])]


def put(f, name, conts, adv):
    charstring(f, name, adv, replay(conts))
    xs = [p[0] for c in conts for _, a in c for p in a]
    f['hmtx'][name] = (adv, round(min(xs)))


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    W = f['hmtx']['p'][0] + WIDEN
    P = [widen(c, AXIS, WIDEN) for c in contours(gs['p'])]
    B = [widen(c, AXIS, WIDEN) for c in contours(gs['b'])]
    Q = [mirror(c, W) for c in P]
    D = [mirror(c, W) for c in B]
    for name, conts in (('p', P), ('b', B), ('q', Q), ('d', D)):
        put(f, name, conts, W)

    s1 = W - 65; s0 = s1 - STEM_W
    bowl = [c for c in Q if not is_stem(c)]
    left = min(p[0] for c in bowl for _, a in c for p in a)
    put(f, 'g', bowl + [rect(s0, 250, s1, XH), g_tail(s0, s1, left)], W)

    f['head'].fontRevision = 0.8
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.800; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.700', '0.800')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
