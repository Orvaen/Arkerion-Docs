"""Arkerion Sans v0.3 — o et O élargis (validé : variante « A2 »).

Pourquoi : le o et le O de la v0.2 paraissaient serrés à côté des nouveaux
p, b, d et q. On garde leur ovale, leurs épaisseurs et leurs approches
(espacement), et on élargit seulement la lettre :

- o : +45 unités de large (approches 45 / 46 inchangées) ;
- O : +61 unités (même proportion × 1,35, approches 53 / 54 inchangées).

Les glyphes qui reprennent ces contours suivent : ô (l'accent est recentré)
et Q (la queue suit le flanc droit).

Usage : python3 retouches_v0_3.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen

K = 0.592          # tension de l'ovale d'origine (contour extérieur)
K_IN = K + 0.02    # contre-forme légèrement plus tendue, comme dans la v0.1
# glyphe : (approche gauche, centre y, rx ext, ry ext, rx int, ry int, approche droite, élargissement)
GEO = {
    'o': (45, 266, 222.5, 276, 137.0, 204, 46, 45),
    'O': (53, 350, 316.0, 362, 226.5, 286, 54, 61),
}
# glyphes composés : (base, déplacement des autres contours en fraction de l'élargissement)
DERIVED = {
    'ocircumflex': ('o', 0.5),   # accent recentré sur la nouvelle panse
    'Q': ('O', 0.85),            # queue : recentrage (0,5) + avancée du flanc à 45° (≈0,35)
}


def ring(pen, cx, cy, rx, ry, k, hole=False):
    """Ovale en quatre cubiques. Plein : antihoraire (CFF) ; contre-forme : horaire."""
    r = lambda p: (round(p[0]), round(p[1]))
    E, N, W, S = (cx + rx, cy), (cx, cy + ry), (cx - rx, cy), (cx, cy - ry)
    if not hole:
        seq = [((cx + rx, cy + ry * k), (cx + rx * k, cy + ry), N),
               ((cx - rx * k, cy + ry), (cx - rx, cy + ry * k), W),
               ((cx - rx, cy - ry * k), (cx - rx * k, cy - ry), S),
               ((cx + rx * k, cy - ry), (cx + rx, cy - ry * k), E)]
    else:
        seq = [((cx + rx, cy - ry * k), (cx + rx * k, cy - ry), S),
               ((cx - rx * k, cy - ry), (cx - rx, cy - ry * k), W),
               ((cx - rx, cy + ry * k), (cx - rx * k, cy + ry), N),
               ((cx + rx * k, cy + ry), (cx + rx, cy + ry * k), E)]
    pen.moveTo(r(E))
    for a, b, c in seq:
        pen.curveTo(r(a), r(b), r(c))
    pen.closePath()


def contours(glyph):
    rec = RecordingPen(); glyph.draw(rec)
    out, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op == 'closePath':
            out.append(cur); cur = []
    return out


def replay(pen, contour):
    for op, args in contour:
        getattr(pen, op)(*args)


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    old = {g: contours(gs[g]) for g in list(GEO) + list(DERIVED)}

    def build(name, base, extra=(), shift=0.0):
        lsb, cy, rxo, ryo, rxi, ryi, rsb, d = GEO[base]
        rxo2, rxi2 = rxo + d / 2, rxi + d / 2
        cx = lsb + rxo2
        adv = round(lsb + 2 * rxo2 + rsb) if name == base else f['hmtx'][name][0] + d
        pen = T2CharStringPen(adv, None)
        ring(pen, cx, cy, rxo2, ryo, K)
        ring(pen, cx, cy, rxi2, ryi, K_IN, hole=True)
        tp = TransformPen(pen, (1, 0, 0, 1, round(shift * d), 0))
        for c in extra:
            replay(tp, c)
        cs[name] = pen.getCharString(private=cs[name].private, globalSubrs=cs[name].globalSubrs)
        f['hmtx'][name] = (adv, f['hmtx'][name][1])

    for g in GEO:
        build(g, g)
    for g, (base, frac) in DERIVED.items():
        extra = [c for c in old[g] if c not in old[base]]
        build(g, base, extra, frac)

    f['head'].fontRevision = 0.3
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.300; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.200', '0.300')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
