"""Arkerion Sans v0.6 — nouveau f, a et e élargis (validé : f « G2 », jeu sobre).

Pourquoi : le f (290 unités, petit crochet, barre courte) et le a et le e
(restés étroits à côté du o et du c élargis) manquaient de présence.

- f : redessiné en f géométrique. Fût presque centré, quart de cercle qui
  tourne vers un bras horizontal plat, barre aussi large que le bras.
  Contours originaux (principe inspiré de JetBrains Mono, aucun point repris).
- a et e : +55 unités, comme le c en v0.5. La moitié droite s'écarte
  (axe du e : x = 262 ; axe du a : x = 235) ; terminaisons et épaisseurs
  inchangées. Les accents (à â é è ê ë) sont recentrés.

Usage : python3 retouches_v0_6.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

WIDEN = 55
WIDE = {  # glyphe de base : (axe, glyphes accentués qui le reprennent)
    'e': (262, ['eacute', 'egrave', 'ecircumflex', 'edieresis']),
    'a': (235, ['agrave', 'acircumflex']),
}
# f « G2 »
F = dict(L=18, R=404, s0=140, sw=82, top=740, th=72, xh=532, bar=68, ro=1.1)


def contours(glyph):
    rec = RecordingPen(); glyph.draw(rec)
    out, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op == 'closePath':
            out.append(cur); cur = []
    return out


def widen(c, axis, d):
    return [(op, [(p[0] + d if p[0] > axis else p[0], p[1]) for p in a]) for op, a in c]


def shift(c, d):
    return [(op, [(p[0] + d, p[1]) for p in a]) for op, a in c]


def charstring(f, name, adv, draw):
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    pen = T2CharStringPen(adv, None)
    draw(pen)
    cs[name] = pen.getCharString(private=cs[name].private, globalSubrs=cs[name].globalSubrs)


def replay(conts):
    def draw(pen):
        for c in conts:
            for op, a in c:
                if op == 'closePath':
                    pen.closePath()
                else:
                    getattr(pen, op)(*[(round(x), round(y)) for x, y in a])
    return draw


def f_geometric(L, R, s0, sw, top, th, xh, bar, ro):
    def draw(pen):
        s1 = s0 + sw
        yb0, yb1 = xh - bar, xh
        yt0 = top - th
        jo = top - round(140 * ro)          # départ de la courbe extérieure sur le fût
        ji = yt0 - round(68 * ro)           # départ de la courbe intérieure
        xo = s0 + round(137 * ro)           # arrivée de la courbe extérieure sur le bras
        xi = s1 + round(61 * ro)
        k = 0.55
        pen.moveTo((s0, 0)); pen.lineTo((s1, 0)); pen.lineTo((s1, yb0)); pen.lineTo((R, yb0))
        pen.lineTo((R, yb1)); pen.lineTo((s1, yb1)); pen.lineTo((s1, ji))
        pen.curveTo((s1, round(ji + (yt0 - ji) * k)), (round(xi - (xi - s1) * k), yt0), (xi, yt0))
        pen.lineTo((R, yt0)); pen.lineTo((R, top)); pen.lineTo((xo, top))
        pen.curveTo((round(xo - (xo - s0) * k), top), (s0, round(jo + (top - jo) * k)), (s0, jo))
        pen.lineTo((s0, yb1)); pen.lineTo((L, yb1)); pen.lineTo((L, yb0)); pen.lineTo((s0, yb0))
        pen.closePath()
    return draw


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    for base, (axis, derived) in WIDE.items():
        base_c = contours(gs[base])
        adv = f['hmtx'][base][0] + WIDEN
        new = [widen(c, axis, WIDEN) for c in base_c]
        charstring(f, base, adv, replay(new))
        f['hmtx'][base] = (adv, f['hmtx'][base][1])
        for g in derived:
            accent = [c for c in contours(gs[g]) if c not in base_c]
            charstring(f, g, adv, replay(new + [shift(c, WIDEN / 2) for c in accent]))
            f['hmtx'][g] = (adv, f['hmtx'][g][1])
    adv_f = F['R'] + 12
    charstring(f, 'f', adv_f, f_geometric(**F))
    f['hmtx']['f'] = (adv_f, F['L'])

    f['head'].fontRevision = 0.6
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.600; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.500', '0.600')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
