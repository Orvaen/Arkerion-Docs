"""Arkerion Sans v0.2 — retouche du p, q, b, d et du r (validée : variante « F »).

Pourquoi : dans la v0.1, le p (et q, b, d) était un o rond posé sur un fût,
et le r finissait en bec court qui tombait. Les nouvelles formes sont tirées
de l'arche du n, comme dans JetBrains Mono : la police gagne en cohérence.

- p, q, b, d : panse = arche du n + son symétrique vertical (axe à mi-hauteur
  entre le haut et le bas de l'arche), plus un court segment droit à droite.
  q et d sont les miroirs horizontaux de p et b.
- r : fût + arche du n, coupée à l'horizontale à y = 307. Le bras va jusqu'à
  la largeur de l'épaule du n ; la terminaison est une coupe plate.

Les courbes sont copiées telles quelles (transformations affines et découpe
exacte des Bézier), pas de polygonisation. Comme le reste de la v0.1, les
formes se chevauchent (fût + arche) ; otf2ttf.py marque OVERLAP_SIMPLE.

Usage : python3 retouches_v0_2.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

XH, DESC, ASC = 532, -200, 740
STEM = (65, 147)
R_CUT = 307          # hauteur de la coupe du bras du r
P_ADV, R_RSB = 510, 16


# ------------------------------------------------------------ contours
# contour = liste de segments : ('L', p0, p1) ou ('C', p0, c1, c2, p1)
def from_recording(value):
    out, cur, start = [], [], None
    for op, a in value:
        if op == 'moveTo':
            start = last = a[0]; cur = []
        elif op == 'lineTo':
            cur.append(('L', last, a[0])); last = a[0]
        elif op == 'curveTo':
            cur.append(('C', last) + tuple(a)); last = a[-1]
        elif op == 'closePath':
            if last != start:
                cur.append(('L', last, start))
            out.append(cur)
    return out


def rect(x0, y0, x1, y1):
    """Rectangle dans le sens des contours pleins de la police (CFF : antihoraire)."""
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return [('L', pts[i], pts[(i + 1) % 4]) for i in range(4)]


def xform(contour, f):
    return [(s[0],) + tuple(f(p) for p in s[1:]) for s in contour]


def reverse(contour):
    return [(s[0],) + tuple(reversed(s[1:])) for s in reversed(contour)]


def flip_y(contour, axis):   # symétrie verticale : le sens s'inverse, on le rétablit
    return reverse(xform(contour, lambda p: (p[0], 2 * axis - p[1])))


def mirror_x(contour, W):
    return reverse(xform(contour, lambda p: (W - p[0], p[1])))


# ---------------------------------------------------- découpe exacte
def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def split(seg, t):
    if seg[0] == 'L':
        m = lerp(seg[1], seg[2], t)
        return ('L', seg[1], m), ('L', m, seg[2])
    _, p0, c1, c2, p3 = seg
    a, b, c = lerp(p0, c1, t), lerp(c1, c2, t), lerp(c2, p3, t)
    d, e = lerp(a, b, t), lerp(b, c, t)
    f = lerp(d, e, t)
    return ('C', p0, a, d, f), ('C', f, e, c, p3)


def y_at(seg, t):
    if seg[0] == 'L':
        return seg[1][1] + (seg[2][1] - seg[1][1]) * t
    _, p0, c1, c2, p3 = seg
    u = 1 - t
    return u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p3[1]


def t_for_y(seg, y):
    lo, hi = 0.0, 1.0
    up = y_at(seg, 1) > y_at(seg, 0)
    for _ in range(60):
        m = (lo + hi) / 2
        if (y_at(seg, m) < y) == up:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def clip_above(contour, y):
    """Garde la partie du contour au-dessus de y et referme par une coupe plate.
    Suppose que chaque segment traversant la ligne est monotone en y (vrai pour
    l'arche du n : les deux pieds de l'arche)."""
    out, pend = [], None
    for s in contour:
        a, b = s[1][1] >= y, s[-1][1] >= y
        if a and b:
            out.append(s)
        elif a != b:
            first, second = split(s, t_for_y(s, y))
            if a:                        # on sort par le bas
                out.append(first); pend = first[-1]
            else:                        # on rentre par le bas
                if pend is not None:
                    out.append(('L', pend, second[1]))
                out.append(second)
    if pend is not None and out and out[0][1] != pend:   # coupe qui referme
        out.append(('L', pend, out[0][1]))
    # remet le contour dans l'ordre d'origine si la sortie précède l'entrée
    return out


def snap(contour):
    r = lambda p: (round(p[0]), round(p[1]))
    return [(s[0],) + tuple(r(p) for p in s[1:]) for s in contour]


# ---------------------------------------------------------- formes
def shapes(n_contours):
    arch = max(n_contours, key=lambda c: max(p[0] for s in c for p in s[1:])
               - min(p[0] for s in c for p in s[1:]))
    ys = [p[1] for s in arch for p in s[1:]]
    top, foot = max(ys), min(ys)            # 542, 287
    xs = [p[0] for s in arch for p in s[1:]]
    right = max(xs)                          # 460
    leg = 85                                 # épaisseur du côté droit de l'arche
    axis = (top + (XH - top)) / 2            # bas de panse en dépassement symétrique : -10
    low = 2 * axis - foot                    # 245
    bowl = [arch, flip_y(arch, axis), rect(right - leg, low - 1, right, foot + 1)]

    p = [rect(STEM[0], DESC, STEM[1], XH)] + bowl
    b = [rect(STEM[0], 0, STEM[1], ASC)] + bowl
    q = [mirror_x(c, P_ADV) for c in p]
    d = [mirror_x(c, P_ADV) for c in b]
    arm = clip_above(arch, R_CUT)
    r = [rect(STEM[0], 0, STEM[1], XH), arm]
    r_adv = round(max(pt[0] for s in arm for pt in s[1:])) + R_RSB
    return {'p': (p, P_ADV), 'q': (q, P_ADV), 'b': (b, P_ADV), 'd': (d, P_ADV), 'r': (r, r_adv)}


def draw(pen, contours):
    for c in contours:
        c = snap(c)
        pen.moveTo(c[0][1])
        for s in c:
            if s[0] == 'L':
                if s[2] != c[0][1] or s is not c[-1]:
                    pen.lineTo(s[2])
            else:
                pen.curveTo(s[2], s[3], s[4])
        pen.closePath()


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    rec = RecordingPen(); gs['n'].draw(rec)
    cff = f['CFF '].cff
    top = cff.topDictIndex[0]
    cs = top.CharStrings
    for name, (contours, adv) in shapes(from_recording(rec.value)).items():
        pen = T2CharStringPen(adv, None)
        draw(pen, contours)
        charstring = pen.getCharString(private=cs[name].private, globalSubrs=cs[name].globalSubrs)
        cs[name] = charstring
        xmin = min(p[0] for c in contours for s in c for p in s[1:])
        f['hmtx'][name] = (adv, round(xmin))
    # version
    f['head'].fontRevision = 0.2
    for rec_ in f['name'].names:
        if rec_.nameID == 5:
            rec_.string = 'Version 0.200; étude'
        elif rec_.nameID == 3:
            rec_.string = str(rec_).replace('0.100', '0.200')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
