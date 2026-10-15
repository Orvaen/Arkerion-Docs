"""Mesure des métriques (pas des contours) d'une police : proportions, graisses,
largeurs, approches. Sert à comparer Arkerion Mono à une référence."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen


class Flat(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.polys = []; self.cur = []
    def _moveTo(self, p): self.cur = [p]
    def _lineTo(self, p): self.cur.append(p)
    def _curveToOne(self, a, b, c):
        p0 = self.cur[-1]
        for i in range(1, 17):
            t = i / 16; u = 1 - t
            self.cur.append((u**3*p0[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*c[0], u**3*p0[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*c[1]))
    def _qCurveToOne(self, a, b):
        p0 = self.cur[-1]
        for i in range(1, 13):
            t = i / 12; u = 1 - t
            self.cur.append((u*u*p0[0]+2*u*t*a[0]+t*t*b[0], u*u*p0[1]+2*u*t*a[1]+t*t*b[1]))
    def _closePath(self):
        if self.cur: self.polys.append(self.cur)
        self.cur = []
    _endPath = _closePath


def runs(polys, y=None, x=None):
    """Segments d'encre (règle non nulle) le long d'une ligne horizontale (y) ou verticale (x)."""
    ev = []
    for pts in polys:
        n = len(pts)
        for i in range(n):
            (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
            if y is not None:
                if (ya <= y < yb) or (yb <= y < ya):
                    ev.append((xa + (y - ya) * (xb - xa) / (yb - ya), 1 if yb > ya else -1))
            else:
                if (xa <= x < xb) or (xb <= x < xa):
                    ev.append((ya + (x - xa) * (yb - ya) / (xb - xa), 1 if xb > xa else -1))
    ev.sort(); w = 0; out = []; start = None
    for pos, d in ev:
        nw = w + d
        if w == 0 and nw != 0: start = pos
        if w != 0 and nw == 0: out.append((start, pos))
        w = nw
    return out


def measure(path):
    f = TTFont(path); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    upm = f['head'].unitsPerEm; k = 1000 / upm
    os2 = f['OS/2']
    def poly(ch):
        g = cmap[ord(ch)]; p = Flat(gs); gs[g].draw(p)
        return [[(x * k, y * k) for x, y in pts] for pts in p.polys], f['hmtx'][g][0] * k
    def bbox(ps):
        xs = [x for p in ps for x, _ in p]; ys = [y for p in ps for _, y in p]
        return min(xs), min(ys), max(xs), max(ys)
    R = {}
    R['upm'] = upm; R['advance'] = poly('n')[1]
    R['capH'] = bbox(poly('H')[0])[3]; R['xH'] = bbox(poly('x')[0])[3]
    R['asc(l)'] = bbox(poly('l')[0])[3]; R['desc(p)'] = bbox(poly('p')[0])[1]
    ps, adv = poly('n'); r = runs(ps, y=R['xH'] * 0.35); R['stem n'] = round(r[0][1] - r[0][0], 1)
    ps, adv = poly('H'); r = runs(ps, y=R['capH'] * 0.25); R['stem H'] = round(r[0][1] - r[0][0], 1)
    r = runs(ps, x=bbox(ps)[0] + (bbox(ps)[2] - bbox(ps)[0]) / 2); R['bar H'] = round(r[0][1] - r[0][0], 1)
    ps, adv = poly('o'); b = bbox(ps)
    R['o width'] = round(b[2] - b[0], 1); R['o lsb'] = round(b[0], 1); R['o rsb'] = round(adv - b[2], 1)
    r = runs(ps, y=(b[1] + b[3]) / 2); R['o side'] = round(r[0][1] - r[0][0], 1)
    r = runs(ps, x=(b[0] + b[2]) / 2); R['o top'] = round(r[-1][1] - r[-1][0], 1)
    ps, adv = poly('n'); b = bbox(ps); R['n width'] = round(b[2] - b[0], 1)
    ps, adv = poly('H'); b = bbox(ps); R['H width'] = round(b[2] - b[0], 1)
    ps, adv = poly('.'); b = bbox(ps); R['period'] = round(b[2] - b[0], 1)
    R['hinting'] = 'oui' if ('fpgm' in f or 'prep' in f) else 'non'
    return R


if __name__ == '__main__':
    rs = [measure(p) for p in sys.argv[1:]]
    keys = list(rs[0])
    for kk in keys:
        print('%-10s' % kk + ''.join('%14s' % (r[kk] if not isinstance(r[kk], float) else round(r[kk], 1)) for r in rs))
