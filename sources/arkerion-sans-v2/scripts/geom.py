"""Arkerion Sans — petite boîte à outils géométrique pour dessiner des glyphes
en Bézier cubiques (unités : 1000/em, y vers le haut).

Un contour = (p0, [segments]) ; segment = ('L', p) ou ('C', c1, c2, p).
Les formes pleines sont orientées dans le sens antihoraire (convention CFF),
les contre-formes dans le sens horaire. Les primitives peuvent se chevaucher :
le remplissage non-nul les fusionne (suppression des chevauchements à l'étape
de production).
"""
import math

KAPPA = 0.5523


# ---------------------------------------------------------------- Bézier ----
def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def bez(p0, c1, c2, p3, t):
    a = lerp(p0, c1, t); b = lerp(c1, c2, t); c = lerp(c2, p3, t)
    d = lerp(a, b, t); e = lerp(b, c, t)
    return lerp(d, e, t)


def split(seg, t):
    p0, c1, c2, p3 = seg
    a = lerp(p0, c1, t); b = lerp(c1, c2, t); c = lerp(c2, p3, t)
    d = lerp(a, b, t); e = lerp(b, c, t); f = lerp(d, e, t)
    return (p0, a, d, f), (f, e, c, p3)


def subseg(seg, t0, t1):
    if t1 <= t0 + 1e-9:
        p = bez(*seg, t0)
        return (p, p, p, p)
    _, right = split(seg, t0)
    left, _ = split(right, (t1 - t0) / (1 - t0) if t0 < 1 else 0)
    return left


# --------------------------------------------------------------- Ellipse ----
class Ell:
    """Super-ellipse asymétrique : rayons et tension par quadrant.
    Paramètre global u ∈ [0,4) : 0 = point droit, 1 = haut, 2 = gauche, 3 = bas."""

    def __init__(self, cx, cy, rxR, ryT, rxL=None, ryB=None, k=KAPPA):
        rxL = rxR if rxL is None else rxL
        ryB = ryT if ryB is None else ryB
        k = k if isinstance(k, (list, tuple)) else [k] * 4
        R = (cx + rxR, cy); T = (cx, cy + ryT); L = (cx - rxL, cy); B = (cx, cy - ryB)
        self.segs = [
            (R, (cx + rxR, cy + k[0] * ryT), (cx + k[0] * rxR, cy + ryT), T),
            (T, (cx - k[1] * rxL, cy + ryT), (cx - rxL, cy + k[1] * ryT), L),
            (L, (cx - rxL, cy - k[2] * ryB), (cx - k[2] * rxL, cy - ryB), B),
            (B, (cx + k[3] * rxR, cy - ryB), (cx + rxR, cy - k[3] * ryB), R),
        ]

    def at(self, u):
        i = int(u) % 4
        return bez(*self.segs[i], u - int(u))

    def cross(self, line, hint):
        """u où l'ellipse coupe la droite `line` ((x,y),(x,y)), au plus près de hint."""
        (ax, ay), (bx, by) = line
        nx, ny = ay - by, bx - ax
        f = lambda p: (p[0] - ax) * nx + (p[1] - ay) * ny
        hits = []
        N = 400
        for i in range(4):
            prev = f(self.segs[i][0]); tp = 0.0
            for j in range(1, N + 1):
                t = j / N
                cur = f(bez(*self.segs[i], t))
                if prev == 0 or prev * cur < 0:
                    lo, hi = tp, t
                    for _ in range(50):
                        m = (lo + hi) / 2
                        if f(bez(*self.segs[i], lo)) * f(bez(*self.segs[i], m)) <= 0:
                            hi = m
                        else:
                            lo = m
                    hits.append(i + (lo + hi) / 2)
                prev, tp = cur, t
        if not hits:
            raise ValueError("pas d'intersection avec %r" % (line,))
        return min(hits, key=lambda u: math.dist(self.at(u), hint))

    def arc(self, u0, u1):
        """Segments cubiques de u0 à u1 dans le sens croissant (avec bouclage)."""
        if u1 <= u0:
            u1 += 4
        out = []
        u = u0
        while u < u1 - 1e-9:
            i = int(math.floor(u + 1e-12))
            end = min(u1, i + 1)
            seg = self.segs[i % 4]
            out.append(subseg(seg, u - i, end - i))
            u = end
        return out


# -------------------------------------------------------------- Contours ----
def rev_curves(curves):
    return [(s[3], s[2], s[1], s[0]) for s in reversed(curves)]


def from_curves(curves):
    p0 = curves[0][0]
    return (p0, [('C', s[1], s[2], s[3]) for s in curves])


def poly(pts):
    return (pts[0], [('L', p) for p in pts[1:]])


def flatten(contour, n=16):
    p0, segs = contour
    pts = [p0]
    cur = p0
    for s in segs:
        if s[0] == 'L':
            pts.append(s[1]); cur = s[1]
        else:
            for j in range(1, n + 1):
                pts.append(bez(cur, s[1], s[2], s[3], j / n))
            cur = s[3]
    return pts


def area(contour):
    pts = flatten(contour)
    a = 0
    for i in range(len(pts)):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return a / 2


def reverse(contour):
    p0, segs = contour
    pts = [p0] + [s[-1] for s in segs]
    out = []
    for i in range(len(segs) - 1, -1, -1):
        s = segs[i]
        start = pts[i]
        if s[0] == 'L':
            out.append(('L', start))
        else:
            out.append(('C', s[2], s[1], start))
    return (pts[-1], out)


def solid(c):
    return c if area(c) > 0 else reverse(c)


def hole(c):
    return c if area(c) < 0 else reverse(c)


def ring(eo, ei):
    return [solid(from_curves(eo.arc(0, 4))), hole(from_curves(ei.arc(0, 4)))]


def band(eo, ei, cutA, hintA, cutB, hintB):
    """Bande comprise entre deux ellipses, de la coupe A à la coupe B dans le
    sens antihoraire. Les coupes sont des droites ; hint = point proche."""
    uao = eo.cross(cutA, hintA); ubo = eo.cross(cutB, hintB)
    uai = ei.cross(cutA, hintA); ubi = ei.cross(cutB, hintB)
    outer = eo.arc(uao, ubo)
    inner = rev_curves(ei.arc(uai, ubi))
    p0 = outer[0][0]
    segs = [('C', s[1], s[2], s[3]) for s in outer]
    segs.append(('L', inner[0][0]))
    segs += [('C', s[1], s[2], s[3]) for s in inner]
    return solid((p0, segs))


def rect(x0, y0, x1, y1):
    return solid(poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]))


def intersect(l1, l2):
    (x1, y1), (x2, y2) = l1; (x3, y3), (x4, y4) = l2
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2; b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)


def offset_line(p, q, d):
    """Droite pq décalée de d perpendiculairement (à gauche du sens p→q)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * d, dx / L * d
    return ((p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny))


def stroke(p, q, w, cutP, cutQ, wq=None):
    """Fût droit d'axe p→q, épaisseur w (wq au bout q si effilé), coupé par
    deux droites cutP et cutQ."""
    wq = w if wq is None else wq
    # côtés : on autorise un effilement en interpolant l'épaisseur
    l1 = ((p[0], p[1]), (q[0], q[1]))
    a = offset_line(p, q, w / 2); b = offset_line(p, q, -w / 2)
    a2 = offset_line(p, q, wq / 2); b2 = offset_line(p, q, -wq / 2)
    left = (a[0], a2[1]); right = (b[0], b2[1])
    pts = [intersect(left, cutP), intersect(left, cutQ),
           intersect(right, cutQ), intersect(right, cutP)]
    return solid(poly(pts))


def H(y):
    return ((-1000, y), (2000, y))


def V(x):
    return ((x, -1000), (x, 2000))


def translate(contours, dx, dy=0):
    out = []
    for p0, segs in contours:
        f = lambda p: (p[0] + dx, p[1] + dy)
        out.append((f(p0), [(s[0],) + tuple(f(p) for p in s[1:]) for s in segs]))
    return out
