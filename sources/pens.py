"""Tracé « à la plume » : un trait d'épaisseur variable le long d'une ligne
médiane cubique. L'épaisseur suit la direction du trait (verticales = fût,
horizontales = délié), ce qui reproduit la logique de contraste des glyphes
construits à partir d'ellipses."""
import math
from geom import bez, poly, solid, intersect, Ell


def dbez(p0, c1, c2, p3, t):
    u = 1 - t
    return (3 * u * u * (c1[0] - p0[0]) + 6 * u * t * (c2[0] - c1[0]) + 3 * t * t * (p3[0] - c2[0]),
            3 * u * u * (c1[1] - p0[1]) + 6 * u * t * (c2[1] - c1[1]) + 3 * t * t * (p3[1] - c2[1]))


def line_seg(a, b):
    return (a, (a[0] + (b[0] - a[0]) / 3, a[1] + (b[1] - a[1]) / 3),
            (a[0] + 2 * (b[0] - a[0]) / 3, a[1] + 2 * (b[1] - a[1]) / 3), b)


def joint(a, ta, b, tb, k=0.4):
    """Cubique de a vers b, tangente ta au départ et tb à l'arrivée."""
    L = math.dist(a, b) * k
    na = math.hypot(*ta) or 1; nb = math.hypot(*tb) or 1
    return (a, (a[0] + ta[0] / na * L, a[1] + ta[1] / na * L),
            (b[0] - tb[0] / nb * L, b[1] - tb[1] / nb * L), b)


def ell_path(e, u0, u1, cw=False):
    """Arc d'ellipse comme liste de cubiques ; cw=True parcourt de u0 vers u1
    dans le sens horaire (u décroissant)."""
    if not cw:
        return e.arc(u0, u1)
    segs = e.arc(u1, u0)
    return [(s[3], s[2], s[1], s[0]) for s in reversed(segs)]


def ell_tan(e, u, cw=False):
    a = e.at(u - 1e-4); b = e.at(u + 1e-4)
    t = (b[0] - a[0], b[1] - a[1])
    return (-t[0], -t[1]) if cw else t


def pen(segs, wv, wh, cut0=None, cut1=None, n=28, expo=1.6):
    """segs : cubiques consécutives. wv/wh : épaisseurs verticale/horizontale.
    cut0/cut1 : angle (°) de coupe aux extrémités (None = perpendiculaire)."""
    L, R, C, T = [], [], [], []
    for si, s in enumerate(segs):
        for j in range(n + 1):
            if j == 0 and si > 0:
                continue
            t = j / n
            p = bez(*s, t); d = dbez(*s, t)
            if math.hypot(*d) < 1e-6:
                d = dbez(*s, min(max(t, 0.01), 0.99))
            ln = math.hypot(*d); tx, ty = d[0] / ln, d[1] / ln
            w = wh + (wv - wh) * abs(tx * 0 + ty) ** expo  # |sin| de l'angle de la tangente
            nx, ny = -ty, tx
            L.append((p[0] + nx * w / 2, p[1] + ny * w / 2))
            R.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
            C.append(p); T.append((tx, ty))
    for end, ang in ((0, cut0), (-1, cut1)):
        if ang is None:
            continue
        p = C[end]
        a = math.radians(ang)
        cut = (p, (p[0] + math.cos(a), p[1] + math.sin(a)))
        i2 = 1 if end == 0 else -2
        L[end] = intersect((L[i2], L[end]), cut)
        R[end] = intersect((R[i2], R[end]), cut)
    return solid(poly(L + list(reversed(R))))


def dot(cx, cy, d):
    from geom import from_curves
    return solid(from_curves(Ell(cx, cy, d / 2, d / 2).arc(0, 4)))
