"""Arkerion Mono 0.3 — point du i et du j remonté.

Pourquoi : le point commençait à 607 unités, 57 au-dessus de la hauteur d'x
(550). En 13 px, un pixel vaut 77 unités : une fois le hinting appliqué, le
point se collait au fût et « utilisateur » se lisait « utllisateur ».

Le point est maintenant un rond de 128 unités (au lieu de 142), de 650 à 778 :
99 unités d'écart avec la hauteur d'x, plus d'un pixel jusqu'en 10 px.
Même placement que JetBrains Mono (649 à 777), mêmes métriques.

Dans le fichier de police, la version est notée 0.300.

Usage : python3 mono_retouches_v0_3.py ArkerionMono-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

DOT_BOTTOM, DOT_D = 650, 128
K = 0.5523                       # tangentes d'un cercle en quatre cubiques


def contours(rec):
    out, cur = [], []
    for op, args in rec:
        cur.append((op, args))
        if op in ('closePath', 'endPath'):
            out.append(cur)
            cur = []
    return out


def is_dot(c):
    ys = [p[1] for op, a in c for p in a]
    return ys and min(ys) > 560          # le seul contour au-dessus de la hauteur d'x


def circle(pen, cx, cy, r):
    k = r * K
    pen.moveTo((cx + r, cy))
    pen.curveTo((cx + r, cy + k), (cx + k, cy + r), (cx, cy + r))
    pen.curveTo((cx - k, cy + r), (cx - r, cy + k), (cx - r, cy))
    pen.curveTo((cx - r, cy - k), (cx - k, cy - r), (cx, cy - r))
    pen.curveTo((cx + k, cy - r), (cx + r, cy - k), (cx + r, cy))
    pen.closePath()


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    for name in ('i', 'j'):
        rec = RecordingPen()
        gs[name].draw(rec)
        pen = T2CharStringPen(f['hmtx'][name][0], None)
        for c in contours(rec.value):
            if is_dot(c):
                xs = [p[0] for op, a in c for p in a]
                cx = (min(xs) + max(xs)) / 2
                circle(pen, round(cx), DOT_BOTTOM + DOT_D / 2, DOT_D / 2)
            else:
                for op, args in c:
                    getattr(pen, op)(*args)
        cs[name] = pen.getCharString(private=cs[name].private, globalSubrs=cs[name].globalSubrs)
    f['head'].fontRevision = 0.3
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.300; étude'
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
