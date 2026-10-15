"""Arkerion Sans v2 — dessin des 14 glyphes de « Arkerion » en contours uniques.

Chaque glyphe est construit comme un vrai contour de caractère : une seule
silhouette extérieure (et ses contre-formes), sans pièces superposées. Les
courbes sont des quarts de super-ellipse découpés exactement aux points de
jonction (intersections calculées), ce qui garantit :
  - des tangentes continues aux raccords courbe/courbe ;
  - des points d'extremum sur les courbes (découpe par quadrants) ;
  - des fûts et des barres alignés exactement sur 0, x, H et l'ascendante.
"""
import math
import sys
sys.path.insert(0, '/home/claude/arkerion')
from geom import Ell, intersect, H, V, solid, hole, poly, bez

# --------------------------------------------------------------- métriques
M = dict(
    upm=1000, cap=700, xh=520, asc=735, desc=-200,
    os_cap=12, os_lc=10,
    SV=86, SH=74,          # capitales : fût, délié horizontal
    sv=80, sh=68,          # bas-de-casse
    round_v=1.08,          # épaississement des flancs des rondes
    k_out=0.56, k_in=0.575,
)


# ------------------------------------------------------------------ outils
class Path:
    """Contour construit segment par segment, en coordonnées absolues."""

    def __init__(self, p):
        self.p0 = p; self.cur = p; self.segs = []

    def L(self, p):
        if math.dist(p, self.cur) > 0.01:
            self.segs.append(('L', p)); self.cur = p
        return self

    def C(self, curves):
        for s in curves:
            if math.dist(s[0], self.cur) > 0.5:
                self.L(s[0])
            if math.dist(s[0], s[3]) < 0.01 and math.dist(s[1], s[2]) < 0.01:
                continue
            self.segs.append(('C', s[1], s[2], s[3])); self.cur = s[3]
        return self

    def close(self):
        if self.segs and self.segs[-1][0] == 'L' and math.dist(self.segs[-1][1], self.p0) < 0.01:
            self.segs.pop()
        return (self.p0, self.segs)


def ccw(e, u0, u1):
    """Arc d'ellipse dans le sens antihoraire de u0 à u1."""
    return e.arc(u0, u1)


def cw(e, u0, u1):
    """Arc d'ellipse dans le sens horaire de u0 à u1."""
    segs = e.arc(u1, u0)
    return [(s[3], s[2], s[1], s[0]) for s in reversed(segs)]


def hit(e, line, hint):
    u = e.cross(line, hint)
    return u, e.at(u)


def solve(f, lo, hi, target, it=60):
    """Bissection : f croissante ou décroissante, renvoie x tel que f(x)=target."""
    flo = f(lo) - target
    for _ in range(it):
        m = (lo + hi) / 2
        fm = f(m) - target
        if (fm < 0) == (flo < 0):
            lo, flo = m, fm
        else:
            hi = m
    return (lo + hi) / 2


def offset(p, q, d):
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy)
    return (-dy / L * d, dx / L * d)


def edges(p, q, t0, t1=None):
    """Bords gauche et droit d'un trait d'axe p→q, épaisseur t0 en p et t1 en q."""
    t1 = t0 if t1 is None else t1
    a0 = offset(p, q, t0 / 2); a1 = offset(p, q, t1 / 2)
    left = ((p[0] + a0[0], p[1] + a0[1]), (q[0] + a1[0], q[1] + a1[1]))
    right = ((p[0] - a0[0], p[1] - a0[1]), (q[0] - a1[0], q[1] - a1[1]))
    return left, right


def soft_terminal(path, t_from, t_to, out_dir, bulge=0.16):
    """Terminaison légèrement bombée de t_from à t_to (adoucit les angles)."""
    L = math.dist(t_from, t_to) * bulge
    d = math.hypot(*out_dir) or 1
    ox, oy = out_dir[0] / d * L, out_dir[1] / d * L
    c1 = (t_from[0] + (t_to[0] - t_from[0]) / 3 + ox, t_from[1] + (t_to[1] - t_from[1]) / 3 + oy)
    c2 = (t_from[0] + 2 * (t_to[0] - t_from[0]) / 3 + ox, t_from[1] + 2 * (t_to[1] - t_from[1]) / 3 + oy)
    path.segs.append(('C', c1, c2, t_to)); path.cur = t_to


def radial_cut(eo, ei, phi, cx, cy):
    ux, uy = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    ray = ((cx, cy), (cx + ux, cy + uy)); far = (cx + ux * 3000, cy + uy * 3000)
    uo, po = hit(eo, ray, far); ui, pi = hit(ei, ray, far)
    return uo, po, ui, pi, (ux, uy)


def tangent_out(e, u, direction):
    a, b = e.at(u - 1e-3), e.at(u + 1e-3)
    t = (b[0] - a[0], b[1] - a[1])
    return t if direction > 0 else (-t[0], -t[1])


# ================================================================ capitales
def g_I():
    SV, cap = M['SV'], M['cap']
    return [poly([(0, 0), (SV, 0), (SV, cap), (0, cap)])]


def g_E():
    SV, SH, cap = M['SV'], M['SH'], M['cap']
    top, mid, bot = 438, 404, 456
    hm = SH * 0.94
    ym = (cap - hm) / 2 + 8           # barre centrale légèrement au-dessus du centre optique
    return [poly([(0, 0), (bot, 0), (bot, SH), (SV, SH), (SV, ym), (mid, ym), (mid, ym + hm),
                  (SV, ym + hm), (SV, cap - SH), (top, cap - SH), (top, cap), (0, cap)])]


def g_O():
    W, cap, os_ = 742, M['cap'], M['os_cap']
    rx, ry = W / 2, cap / 2 + os_
    eo = Ell(rx, cap / 2, rx, ry, k=M['k_out'])
    ei = Ell(rx, cap / 2, rx - M['SV'] * M['round_v'], ry - M['SH'], k=M['k_in'])
    return [Path(eo.at(0)).C(ccw(eo, 0, 4)).close(), hole(Path(ei.at(0)).C(ccw(ei, 0, 4)).close())]


def g_N():
    W, cap = 606, M['cap']
    sv = M['SV'] * 0.92
    t = M['SV'] * 1.04
    hd = solve(lambda h: h * math.sin(math.atan2(cap, W - h)), 50, 400, t)
    up = ((hd, cap), (W, 0)); lo = ((0, cap), (W - hd, 0))
    P1 = intersect(V(sv), lo); P3 = intersect(V(W - sv), up)
    return [poly([(0, 0), (sv, 0), P1, (W - hd, 0), (W, 0), (W, cap), (W - sv, cap), P3, (hd, cap), (0, cap)])]


def g_A():
    W, cap, SV, SH = 684, M['cap'], M['SV'], M['SH']
    af = 46                                    # sommet plat, étroit
    xa, xb = W / 2 - af / 2, W / 2 + af / 2
    tl, tr = SV * 0.80, SV * 1.02              # jambage gauche délié, droit appuyé
    hL = tl / math.sin(math.atan2(cap, xa)); hR = tr / math.sin(math.atan2(cap, W - xb))
    Lin = ((hL, 0), (xa + hL, cap)); Rin = ((W - hR, 0), (xb - hR, cap))
    y0 = 186; y1 = y0 + SH * 0.92             # barre basse : silhouette assise
    outer = poly([(0, 0), (hL, 0), intersect(Lin, H(y0)), intersect(Rin, H(y0)), (W - hR, 0),
                  (W, 0), (xb, cap), (xa, cap)])
    counter = poly([intersect(Lin, H(y1)), intersect(Rin, H(y1)), intersect(Lin, Rin)])
    return [solid(outer), hole(counter)]


def g_R():
    cap, SV, SH = M['cap'], M['SV'], M['SH']
    ym, hb = 312, SH * 0.92
    bx, bw = 296, 540
    cy, ry = (cap + ym) / 2, (cap - ym) / 2
    eo = Ell(bx, cy, bw - bx, ry, k=0.57)
    iy0, iy1 = ym + hb, cap - SH
    ei = Ell(bx, (iy0 + iy1) / 2, bw - bx - SV * M['round_v'], (iy1 - iy0) / 2, k=0.59)
    # jambe : part de la panse, raide, s'évase vers le pied
    p, q = (bx + 26, ym + hb / 2), (bw + 46, 0)
    lft, rgt = edges(p, q, SV * 0.94, SV * 1.14)
    # lft est à gauche du sens p→q (vers le haut-droite) : c'est le bord droit visuel
    edge_l, edge_r = rgt, lft
    A1 = intersect(edge_l, H(ym)); A2 = intersect(edge_l, H(0)); A3 = intersect(edge_r, H(0))
    R_ym = intersect(edge_r, H(ym))
    path = Path((0, 0)).L((SV, 0)).L((SV, ym)).L(A1).L(A2).L(A3)
    if R_ym[0] <= bx:
        path.L(R_ym).L((bx, ym)).C(ccw(eo, 3, 5))
    else:
        uq, Q = hit(eo, edge_r, (R_ym[0], ym + 20))
        path.L(Q).C(ccw(eo, uq, 5))
    path.L((0, cap))
    counter = Path((SV, cap - SH)).L((bx, cap - SH)).C(cw(ei, 1, -1)).L((SV, iy0)).close()
    return [solid(path.close()), hole(counter)]


def _k(top_stem, top_arm, sv, W, yj, f_leg, t_arm, t_leg, x_arm, x_leg, taper=0.84):
    """K / k en un seul contour : bras issu du fût, jambe greffée sur le bras."""
    J, T = (sv * 0.5, yj), (x_arm, top_arm)
    aU, aL = edges(J, T, t_arm * taper, t_arm)        # aU : bord haut-gauche, aL : bord bas-droit
    aU, aL = aU, aL
    if aU[0][1] < aL[0][1]:
        aU, aL = aL, aU
    S = (J[0] + (T[0] - J[0]) * f_leg, J[1] + (T[1] - J[1]) * f_leg)
    F = (x_leg, 0)
    l1, l2 = edges(S, F, t_leg)
    legL, legR = (l1, l2) if l1[1][0] < l2[1][0] else (l2, l1)
    P2 = intersect(V(sv), aL); P3 = intersect(aL, legL); P4 = intersect(legL, H(0))
    P5 = intersect(legR, H(0)); P6 = intersect(legR, aL)
    P7 = intersect(aL, H(top_arm)); P8 = intersect(aU, H(top_arm)); P9 = intersect(aU, V(sv))
    pts = [(0, 0), (sv, 0), P2, P3, P4, P5, P6, P7, P8, P9, (sv, top_stem), (0, top_stem)]
    if top_stem == top_arm:
        pts = [(0, 0), (sv, 0), P2, P3, P4, P5, P6, P7, P8, P9, (sv, top_stem), (0, top_stem)]
    return [solid(poly(pts))]


def g_K():
    SV, cap = M['SV'], M['cap']
    return _k(cap, cap, SV, 600, cap * 0.30, 0.42, SV * 0.92, SV * 1.0, 560, 586)


# ================================================================ bas-de-casse
def g_o():
    W, xh, os_ = 486, M['xh'], M['os_lc']
    rx, ry = W / 2, xh / 2 + os_
    eo = Ell(rx, xh / 2, rx, ry, k=M['k_out'])
    ei = Ell(rx, xh / 2, rx - M['sv'] * M['round_v'], ry - M['sh'], k=M['k_in'])
    return [Path(eo.at(0)).C(ccw(eo, 0, 4)).close(), hole(Path(ei.at(0)).C(ccw(ei, 0, 4)).close())]


def g_i():
    sv, xh = M['sv'], M['xh']
    d = sv * 1.2
    dot = Ell(sv / 2, M['asc'] - d / 2, d / 2, d / 2)
    return [poly([(0, 0), (sv, 0), (sv, xh), (0, xh)]), Path(dot.at(0)).C(ccw(dot, 0, 4)).close()]


def _arch(W, cx_f, cy_f, crotch_f, thin=0.94, join_f=0.875):
    """Ellipses d'épaule calibrées : l'extérieur rejoint le fût à join_f·x,
    sous le coin du fût (épaule qui naît du fût), et l'intérieur coupe le fût
    à la hauteur crotch_f·x."""
    sv, sh, xh, os_ = M['sv'], M['sh'], M['xh'], M['os_lc']
    cy = xh * cy_f; cxo = W * cx_f
    ryT = xh + os_ - cy

    def eo_of(rxL):
        return Ell(cxo, cy, W - cxo, ryT, rxL=rxL, ryB=cy, k=0.565)
    rxL = solve(lambda r: eo_of(r).at(eo_of(r).cross(V(sv), (sv, xh)))[1], cxo - sv + 2, cxo * 3, xh * join_f)
    eo = eo_of(rxL)
    cxi = cxo - 6
    ryTi = xh + os_ - sh * thin - cy

    def ei_of(r):
        return Ell(cxi, cy, (W - sv) - cxi, ryTi, rxL=r, ryB=cy, k=0.58)
    rxLi = solve(lambda r: ei_of(r).at(ei_of(r).cross(V(sv), (sv, xh)))[1], cxi - sv + 2, cxi * 3, xh * crotch_f)
    ei = ei_of(rxLi)
    return eo, ei, cy, cxo


def g_n():
    W, sv, xh = 412, M['sv'], M['xh']
    eo, ei, cy, _ = _arch(W, 0.56, 0.52, 0.64)
    ui, Pi = hit(ei, V(sv), (sv, xh)); uo, Po = hit(eo, V(sv), (sv, xh))
    p = Path((0, 0)).L((sv, 0)).L(Pi).C(cw(ei, ui, 0)).L((W - sv, 0)).L((W, 0)).L((W, cy)).C(ccw(eo, 0, uo)).L((sv, xh)).L((0, xh))
    return [solid(p.close())]


def g_r():
    W, sv, xh = 336, M['sv'], M['xh']
    eo, ei, cy, cxo = _arch(W, 0.54, 0.60, 0.74, thin=0.98)
    ui, Pi = hit(ei, V(sv), (sv, xh)); uo, Po = hit(eo, V(sv), (sv, xh))
    to, To, ti, Ti, ray = radial_cut(eo, ei, 34, cxo, cy)
    p = Path((0, 0)).L((sv, 0)).L(Pi).C(cw(ei, ui, ti))
    soft_terminal(p, Ti, To, tangent_out(eo, to, -1), 0.14)
    p.C(ccw(eo, to, uo)).L((sv, xh)).L((0, xh))
    return [solid(p.close())]


def g_e():
    W, xh, os_, sv, sh = 470, M['xh'], M['os_lc'], M['sv'], M['sh']
    rx, ry = W / 2, xh / 2 + os_
    eo = Ell(rx, xh / 2, rx, ry, k=M['k_out'])
    ei = Ell(rx, xh / 2, rx - sv * 1.06, ry - sh, k=M['k_in'])
    hb = sh * 0.9
    yb = xh * 0.5 - hb / 2 + 6                # barre au-dessus du centre : œil généreux
    yt = yb + hb
    uq, Qr = hit(eo, H(yb), (W, yb))
    to, To, ti, Ti, ray = radial_cut(eo, ei, -42, rx, xh / 2)
    ul, Pl = hit(ei, H(yb), (0, yb))
    p = Path(Qr).C(ccw(eo, uq, to))
    soft_terminal(p, To, Ti, tangent_out(eo, to, 1), 0.14)
    p.C(cw(ei, ti, ul)).L(Qr)
    u1, P1 = hit(ei, H(yt), (0, yt)); u2, P2 = hit(ei, H(yt), (W, yt))
    eye = Path(P2).C(ccw(ei, u2, u1)).L(P2)
    return [solid(p.close()), hole(eye.close())]


def g_a():
    W, xh, os_, sv, sh = 436, M['xh'], M['os_lc'], M['sv'], M['sh']
    # capuchon
    cyh = xh * 0.60; hx = W - 204; xl = 34
    eho = Ell(hx, cyh, W - hx, xh + os_ - cyh, rxL=hx - xl, ryB=cyh, k=0.565)
    ehi = Ell(hx - 4, cyh, (W - sv) - (hx - 4), xh + os_ - sh * 0.96 - cyh,
              rxL=hx - 4 - xl - sv * 1.02, ryB=cyh, k=0.58)
    to, To, ti, Ti, ray = radial_cut(eho, ehi, 152, hx, cyh)
    # panse
    bt = xh * 0.56; bcy = bt * 0.47; bcx = W - 232
    ebo = Ell(bcx, bcy, W - bcx, bt - bcy, rxL=bcx, ryB=bcy + os_, k=0.57)
    ebi = Ell(bcx + 8, bcy + 3, (W - sv * 0.45) - (bcx + 8), bt - bcy - sh * 0.86 - 3,
              rxL=bcx + 8 - sv * 1.06, ryB=bcy + os_ - sh * 0.98 + 3, k=0.585)
    ut, Pt = hit(ebo, V(W - sv), (W, bt)); ub, Pb = hit(ebo, V(W - sv), (W, 0))
    p = Path((W, 0)).L((W, cyh)).C(ccw(eho, 0, to))
    soft_terminal(p, To, Ti, tangent_out(eho, to, 1), 0.14)
    p.C(cw(ehi, ti, 0)).L(Pt).C(ccw(ebo, ut, ub))
    if Pb[1] > 0.5:
        p.L((W - sv, 0))
    uti, Pti = hit(ebi, V(W - sv), (W, bt)); ubi, Pbi = hit(ebi, V(W - sv), (W, 0))
    counter = Path(Pti).C(ccw(ebi, uti, ubi)).L(Pti)
    return [solid(p.close()), hole(counter.close())]


def g_k():
    sv, xh, asc = M['sv'], M['xh'], M['asc']
    return _k(asc, xh, sv, 420, xh * 0.30, 0.42, sv * 0.92, sv * 1.0, 392, 414)


GLYPHS = {'A': g_A, 'R': g_R, 'K': g_K, 'E': g_E, 'I': g_I, 'O': g_O, 'N': g_N,
          'a': g_a, 'r': g_r, 'k': g_k, 'e': g_e, 'i': g_i, 'o': g_o, 'n': g_n}
