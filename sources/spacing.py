"""Espacement optique : aires de blanc à profondeur limitée (dans l'esprit
de HT Letterspacer), puis crénage des paires par interaction des profils."""
from geom import flatten, translate

N_ROWS = 80


def profile(contours, y0, y1):
    polys = [flatten(c, 24) for c in contours]
    rows = []
    for j in range(N_ROWS):
        y = y0 + (y1 - y0) * (j + 0.5) / N_ROWS
        xs = []
        for pts in polys:
            n = len(pts)
            for i in range(n):
                (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
                if (ya <= y < yb) or (yb <= y < ya):
                    xs.append(xa + (y - ya) * (xb - xa) / (yb - ya))
        rows.append((min(xs), max(xs)) if xs else None)
    return rows


def solve(d, target, D):
    lo, hi = -200.0, 400.0
    for _ in range(60):
        s = (lo + hi) / 2
        m = sum(min(s + x, D) for x in d) / len(d)
        if m < target:
            lo = s
        else:
            hi = s
    return (lo + hi) / 2


def space(contours, top, target, D, min_r=0.2):
    rows = profile(contours, 0, top)
    ink = [r for r in rows if r]
    xmin = min(r[0] for r in ink); xmax = max(r[1] for r in ink)
    dl = [(r[0] - xmin) if r else D for r in rows]
    dr = [(xmax - r[1]) if r else D for r in rows]
    lsb = max(solve(dl, target, D), target * 0.2); rsb = max(solve(dr, target, D), target * min_r)
    adv = round(xmax - xmin + lsb + rsb)
    return translate(contours, lsb - xmin), adv, (round(lsb), round(rsb))


def kern(ga, adva, gb, top, D, kf=0.55):
    """Crénage entre deux glyphes déjà espacés (contours en coordonnées
    propres). Compare l'aire combinée à la somme des aires séparées."""
    ra = profile(ga, 0, top); rb = profile(gb, 0, top)
    sep, comb = [], []
    for a, b in zip(ra, rb):
        ga_ = (adva - a[1]) if a else D * 1.0
        gb_ = b[0] if b else D * 1.0
        sep.append(min(ga_, D) + min(gb_, D))
        comb.append(min(ga_ + gb_, 2 * D))
    k = (sum(sep) - sum(comb)) / len(sep) * kf
    return round(k) if abs(k) >= 6 else 0
