"""Contrôle technique d'une police : contours, sens, chevauchements,
auto-intersections, extremums, alignement sur les lignes de métrique,
épaisseurs mesurées et approches."""
import sys, json, itertools
sys.path.insert(0, '/home/claude/arkerion/tools')
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from measure import Flat, runs


def contours_of(gs, g):
    rp = RecordingPen(); gs[g].draw(rp)
    cs, cur = [], []
    for op, args in rp.value:
        cur.append((op, args))
        if op in ('closePath', 'endPath'):
            cs.append(cur); cur = []
    return cs


def flat(gs, g):
    p = Flat(gs); gs[g].draw(p); return p.polys


def area(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) / 2


def seg_inter(a, b, c, d):
    def o(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def poly_cross(P, Q):
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        for j in range(len(Q)):
            if seg_inter(a, b, Q[j], Q[(j + 1) % len(Q)]):
                return True
    return False


def self_cross(P):
    n = len(P)
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if seg_inter(P[i], P[(i + 1) % n], P[j], P[(j + 1) % n]):
                return True
    return False


def missing_extrema(contour):
    """Courbes dont l'intérieur contient un extremum horizontal ou vertical."""
    miss = 0; cur = None
    for op, args in contour:
        if op == 'moveTo':
            cur = args[0]
        elif op == 'lineTo':
            cur = args[0]
        elif op == 'curveTo':
            p0, c1, c2, p3 = cur, *args
            for k in (0, 1):
                a, b, c, d = p0[k], c1[k], c2[k], p3[k]
                lo, hi = min(a, d), max(a, d)
                if min(b, c) < lo - 1 or max(b, c) > hi + 1:
                    miss += 1
            cur = p3
    return miss


def analyze(path, metrics):
    f = TTFont(path); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    out = {}
    for ch in 'ARKEIONarkeion':
        g = cmap[ord(ch)]
        cs = contours_of(gs, g); polys = flat(gs, g)
        dirs = ['ccw' if area(p) > 0 else 'cw' for p in polys]
        overl = sum(1 for a, b in itertools.combinations(polys, 2) if poly_cross(a, b))
        selfx = sum(1 for p in polys if self_cross(p))
        ys = [y for p in polys for _, y in p]; xs = [x for p in polys for x, _ in p]
        adv = f['hmtx'][g][0]
        npts = sum(len([a for _, a in c]) for c in cs)
        out[ch] = dict(contours=len(cs), dirs=dirs, overlaps=overl, self_intersections=selfx,
                       missing_extrema=sum(missing_extrema(c) for c in cs),
                       ymin=round(min(ys), 1), ymax=round(max(ys), 1),
                       lsb=round(min(xs)), rsb=round(adv - max(xs)), adv=adv, segments=npts)
    def w(ch, y=None, x=None, k=0):
        polys = flat(gs, cmap[ord(ch)]); r = runs(polys, y=y, x=x); return round(r[k][1] - r[k][0], 1) if len(r) > k else None
    xh, cap = metrics['xh'], metrics['cap']
    st = {'I stem': w('I', y=cap / 2), 'n stem': w('n', y=xh * 0.3), 'E bar': w('E', x=metrics['E_x']),
          'o side': w('o', y=xh / 2), 'o top': None, 'O side': w('O', y=cap / 2)}
    poly = flat(gs, cmap[ord('o')]); xs = [x for p in poly for x, _ in p]; cx = (min(xs) + max(xs)) / 2
    r = runs(poly, x=cx); st['o top'] = round(r[-1][1] - r[-1][0], 1); st['o bottom'] = round(r[0][1] - r[0][0], 1)
    poly = flat(gs, cmap[ord('O')]); xs = [x for p in poly for x, _ in p]; cx = (min(xs) + max(xs)) / 2
    r = runs(poly, x=cx); st['O top'] = round(r[-1][1] - r[-1][0], 1)
    gpos = 'GPOS' in f
    return out, st, gpos


if __name__ == '__main__':
    path, xh, cap, ex = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    out, st, gpos = analyze(path, {'xh': xh, 'cap': cap, 'E_x': ex})
    print('%-3s %3s %-22s %4s %4s %4s %7s %7s %5s %5s %5s' % ('gl', 'nc', 'sens', 'chev', 'auto', 'ext', 'ymin', 'ymax', 'lsb', 'rsb', 'chasse'))
    for ch, d in out.items():
        print('%-3s %3d %-22s %4d %4d %4d %7.1f %7.1f %5d %5d %5d' % (ch, d['contours'], ','.join(d['dirs']), d['overlaps'], d['self_intersections'], d['missing_extrema'], d['ymin'], d['ymax'], d['lsb'], d['rsb'], d['adv']))
    print(st, 'crénage GPOS:', gpos)
