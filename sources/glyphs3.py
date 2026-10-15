"""Arkerion Sans — étude n°3 : extension d'esquisse à l'ASCII de base (+ accents
français courants) pour tester les propositions en contexte (IDE).

Les 14 glyphes de « Arkerion » restent ceux de glyphs2 (dessin travaillé) ;
les autres sont construits avec les mêmes paramètres et la même logique,
au niveau esquisse."""
import math
from geom import (Ell, ring, band, rect, stroke, poly, solid, hole, H, V,
                  intersect, from_curves, reverse, area, translate)
from glyphs2 import GLYPHS as CORE, term, mid, hw, arch, k_branches, cap_O
from pens import pen, joint, ell_path, ell_tan, line_seg, dot


# ------------------------------------------------------------------ outils
def xform(contours, f):
    out = []
    for p0, segs in contours:
        out.append((f(p0), [(s[0],) + tuple(f(p) for p in s[1:]) for s in segs]))
    return out


def mirror(contours, W):
    """Symétrie horizontale (inverse l'orientation → on la rétablit)."""
    return [reverse(c) for c in xform(contours, lambda p: (W - p[0], p[1]))]


def rot180(contours, W, Hh):
    return xform(contours, lambda p: (W - p[0], Hh - p[1]))


def ells(cx, cy, rx, ry, tv, th, k, kin, rxR=None, rxL=None):
    eo = Ell(cx, cy, rx if rxR is None else rxR, ry, rxL=rx if rxL is None else rxL, k=k)
    ei = Ell(cx, cy, (rx if rxR is None else rxR) - tv, ry - th,
             rxL=(rx if rxL is None else rxL) - tv, k=k + kin)
    return eo, ei


def c_shape(P, W, top, sv, sh, k, phi, ang, os_):
    """c / C : anneau ouvert à droite, terminaisons symétriques."""
    rx, ry = W / 2, top / 2 + os_
    eo, ei = ells(rx, top / 2, rx, ry, sv * P['rs'], sh * P['rt'], k, P['k_in'])
    a = term(eo, ei, -phi, None if ang is None else -ang)
    b = term(eo, ei, phi, ang)
    return [band(eo, ei, a, mid(a), b, mid(b))]


def bowl_stem(P, W, sv, sh, top, os_, k, stem_y0, stem_y1):
    """Panse + fût à droite (d, q, et par symétrie b, p)."""
    ox = sv * 0.15
    rx = (W - ox) / 2; cx = rx
    eo = Ell(cx, top / 2, rx, top / 2 + os_, k=k)
    il, ir = sv * P['rs'], W - sv * 0.55
    cxi = (il + ir) / 2
    ei = Ell(cxi, top / 2, (ir - il) / 2, top / 2 + os_ - sh * P['rt'], k=k + P['k_in'])
    cut = V(W - sv * 0.72)
    return [rect(W - sv, stem_y0, W, stem_y1),
            band(eo, ei, cut, (W, top), cut, (W, 0))]


def vee(W, top, apex, t, tl, tr, base=0):
    """V renversé (pointe en bas) : V, v, w."""
    xa, xb = W / 2 - apex / 2, W / 2 + apex / 2
    hL = hw(t * tl, (0, top), (xa, base)); hR = hw(t * tr, (W, top), (xb, base))
    Lin = ((hL, top), (xa + hL, base)); Rin = ((W - hR, top), (xb - hR, base))
    vx = intersect(Lin, Rin)
    pts = [(0, top), (xa, base), (xb, base), (W, top), (W - hR, top), vx, (hL, top)]
    return solid(poly(pts))


def perp(p, q, at):
    """Droite perpendiculaire à pq passant par at."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    return (at, (at[0] - dy, at[1] + dx))


def bar(x0, x1, ytop, h):
    return rect(x0, ytop - h, x1, ytop)


def hook_down(P, xr, xl, sv, sh, cyh, bottom, phi, ang, k):
    """Crochet de descendante vers la gauche (g, j, J) : du fût (bord droit xr)
    vers la terminaison à gauche."""
    cx = (xr + xl) / 2 + (xr - xl) * 0.12
    eo = Ell(cx, cyh, xr - cx, cyh - bottom, rxL=cx - xl, k=k)
    ei = Ell(cx, cyh, xr - sv - cx, cyh - bottom - sh * P['rt'],
             rxL=cx - xl - sv * P['rs'] * 0.9, k=k + P['k_in'])
    for ph, an in ((phi, ang), (phi, None), (phi - 15, None)):
        try:
            t = term(eo, ei, ph, an)
            return band(eo, ei, t, mid(t), H(cyh), (xr, cyh))
        except ValueError:
            pass
    raise ValueError('crochet')


# ============================================================ bas-de-casse
def L(P):
    return dict(sv=P['sv'], sh=P['sh'], xh=P['xh'], asc=P['asc'], desc=P['desc'],
                os=P['osx'], k=P['ko'], pe=P['e_term'])


def lc_c(P):
    g = L(P)
    phi, ang = P['e_term']
    return c_shape(P, P['we'] * 0.94, g['xh'], g['sv'], g['sh'], g['k'], phi, ang, g['os'])


def lc_d(P):
    g = L(P)
    return bowl_stem(P, P['wo'] * 1.0, g['sv'], g['sh'], g['xh'], g['os'], g['k'], 0, g['asc'])


def lc_q(P):
    g = L(P)
    return bowl_stem(P, P['wo'] * 1.0, g['sv'], g['sh'], g['xh'], g['os'], g['k'], g['desc'], g['xh'])


def lc_b(P):
    W = P['wo'] * 1.0
    return mirror(lc_d(P), W)


def lc_p(P):
    W = P['wo'] * 1.0
    return mirror(lc_q(P), W)


def lc_g(P):
    g = L(P); W = P['wo'] * 1.0
    c = bowl_stem(P, W, g['sv'], g['sh'], g['xh'], g['os'], g['k'], -40, g['xh'])
    cyh = g['desc'] + 150
    phi, ang = P['e_term']
    c.append(hook_down(P, W, 20, g['sv'], g['sh'], cyh, g['desc'] - g['os'],
                       205, None if ang is None else 180 - ang, g['k']))
    c.append(rect(W - g['sv'], cyh - 2, W, 0))
    return c


def lc_l(P):
    return [rect(0, 0, P['sv'], P['asc'])]


def lc_j(P):
    g = L(P); sv = g['sv']
    cyh = g['desc'] + 120
    phi, ang = P['e_term']
    c = [rect(0, cyh - 2, sv, g['xh']), dot(sv / 2, P['dot_y'], P['dot']),
         hook_down(P, sv, -150, sv, g['sh'], cyh, g['desc'] - g['os'],
                   212, None if ang is None else 180 - ang, g['k'])]
    return c


def lc_h(P):
    c = CORE['n'](P)
    c[0] = rect(0, 0, P['sv'], P['asc'])
    return c


def lc_m(P):
    W = P['wn'] * 0.80
    sv, sh = P['sv'], P['sh']
    eo, ei, cy = arch(P, W, sv, sh, P['arch_cx'])
    a1 = [band(eo, ei, H(cy), (W, cy), V(sv * 0.8), (sv, P['xh'])), rect(W - sv * P['rs'], 0, W, cy + 2)]
    dx = W - sv * P['rs']
    a2 = translate(a1, dx)
    return [rect(0, 0, sv, P['xh'])] + a1 + a2


def lc_u(P):
    W = P['wn']
    return rot180(CORE['n'](P), W, P['xh'])


def lc_t(P):
    g = L(P); sv, sh = g['sv'], g['sh']
    W = P['wr'] * 0.98
    x0 = W * 0.26
    cyh = g['xh'] * 0.30
    top = g['xh'] + (g['asc'] - g['xh']) * 0.55
    cx = x0 + (W - x0) * 0.46
    eo = Ell(cx, cyh, W - cx, cyh + g['os'], rxL=cx - x0, k=g['k'])
    ei = Ell(cx, cyh, W - cx - sv * 0.5, cyh + g['os'] - sh * P['rt'], rxL=cx - x0 - sv, k=g['k'] + P['k_in'])
    phi, ang = P['e_term']
    t = term(eo, ei, phi - 8, ang)
    return [rect(x0, cyh - 2, x0 + sv, top), band(eo, ei, H(cyh), (x0, cyh), t, mid(t)),
            bar(0, W * 0.94, g['xh'], sh * 0.92)]


def lc_f(P):
    g = L(P); sv, sh = g['sv'], g['sh']
    W = P['wr'] * 0.98
    x0 = W * 0.22
    top = g['asc'] + 4
    cy = top - 170
    cx = x0 + (W - x0) * 0.52
    eo = Ell(cx, cy, W - cx, top - cy, rxL=cx - x0, k=P['k_arch'])
    ei = Ell(cx - 4, cy, W - cx - sv * 0.6, top - cy - sh * P['arch_thin'],
             rxL=cx - 4 - x0 - sv * 0.52, k=P['k_arch'] + P['k_in'])
    t = term(eo, ei, *P['r_term'])
    return [rect(x0, 0, x0 + sv, top - g['os']), band(eo, ei, t, mid(t), V(x0 + sv * 0.8), (x0 + sv, top)),
            bar(0, W * 0.92, g['xh'], sh * 0.92)]


def lc_s(P):
    g = L(P); sv, sh, xh, os_ = g['sv'], g['sh'], g['xh'], g['os']
    W = P['we'] * 0.84
    wv, wh = sv * 0.98, sh * 0.96
    ry = (xh + 2 * os_) / 4
    rx = W / 2 - wv / 2
    up = Ell(W / 2, xh + os_ - ry - wh / 2 + wh / 2, rx * 0.94, ry - wh / 4)
    lo = Ell(W / 2, ry - os_ + wh / 4, rx, ry - wh / 4)
    phi, ang = P['e_term']
    # haut : de la terminaison (en haut à droite) vers la gauche, puis l'épine
    u_t = 0.38; u_l = 2.25
    s1 = ell_path(up, u_t, u_l)
    u_r = 0.25 + 4; u_b = 2.40
    s3 = ell_path(lo, u_r - 4, u_b, cw=True)
    spine = joint(up.at(u_l), ell_tan(up, u_l), lo.at(u_r - 4), ell_tan(lo, u_r - 4, cw=True), 0.45)
    return [pen(s1 + [spine] + s3, wv, wh)]


def lc_v(P):
    W = P['wn'] * 1.02
    return [vee(W, P['xh'], P['sv'] * 0.55, P['sv'], 0.9, 0.98)]


def lc_w(P):
    W1 = P['wn'] * 0.92
    t = P['sv']
    Ww = 2 * W1 - hw(t * 0.94, (0, P['xh']), (W1 / 2, 0))
    return [vee(W1, P['xh'], P['sv'] * 0.5, P['sv'], 0.88, 0.94),
            translate([vee(W1, P['xh'], P['sv'] * 0.5, P['sv'], 0.88, 0.94)], Ww - W1)[0]]


def lc_x(P):
    W, xh, t = P['wn'] * 0.98, P['xh'], P['sv'] * 0.92
    return [stroke((t * 0.55, 0), (W - t * 0.55, xh), t, H(0), H(xh)),
            stroke((t * 0.55, xh), (W - t * 0.55, 0), t * 0.9, H(xh), H(0))]


def lc_y(P):
    W, xh, t, d = P['wn'] * 1.02, P['xh'], P['sv'], P['desc']
    xr_top = W - hw(t, (W, xh), (W * 0.42, d)) / 2
    right = stroke((xr_top, xh), (W * 0.30, d), t * 0.98, H(xh), H(d))
    left = stroke((hw(t, (0, xh), (W * 0.5, 0)) / 2, xh), (W * 0.52, 0), t * 0.88, H(xh), H(0))
    return [right, left]


def lc_z(P):
    W, xh, sh, sv = P['wn'] * 0.92, P['xh'], P['sh'], P['sv']
    hd = hw(sv * 0.95, (0, sh), (W, xh - sh))
    return [bar(W * 0.04, W, xh, sh * 0.96), rect(0, 0, W, sh),
            solid(poly([(0, sh), (hd, sh), (W, xh - sh), (W - hd, xh - sh)]))]


# ================================================================ capitales
def C(P):
    return dict(SV=P['SV'], SH=P['SH'], cap=P['cap'], os=P['os'], k=P['kO'])


def cap_C(P):
    g = C(P)
    phi, ang = P['e_term']
    return c_shape(P, P['wO'] * 0.93, g['cap'], g['SV'], g['SH'], g['k'], phi - 4, ang, g['os'])


def cap_G(P):
    g = C(P); W = P['wO'] * 0.95; SV, SH, cap = g['SV'], g['SH'], g['cap']
    rx, ry = W / 2, cap / 2 + g['os']
    eo, ei = ells(rx, cap / 2, rx, ry, SV * P['rs'], SH * P['rt'], g['k'], P['k_in'])
    phi, ang = P['e_term']
    a = term(eo, ei, -(phi - 4), None if ang is None else -ang)
    ys = cap * 0.40
    return [band(eo, ei, a, mid(a), H(ys), (W, ys)),
            rect(W - SV * P['rs'], 40, W, ys), bar(W * 0.52, W, ys, SH * 0.92)]


def cap_D(P):
    g = C(P); SV, SH, cap = g['SV'], g['SH'], g['cap']
    W = P['wO'] * 0.88
    bx = W * 0.42
    eo = Ell(bx, cap / 2, W - bx, cap / 2, k=P['kO'] + 0.03)
    ei = Ell(bx, cap / 2, W - bx - SV * P['rs'], cap / 2 - SH, k=P['kO'] + 0.03 + P['k_in'])
    return [rect(0, 0, SV, cap), rect(SV - 2, cap - SH, bx + 1, cap), rect(SV - 2, 0, bx + 1, SH),
            band(eo, ei, V(bx), (bx, 0), V(bx), (bx, cap))]


def _bowl_r(P, x0, y0, y1, bw, bx, t_top, t_bot):
    """Panse droite entre y0 et y1 (barres comprises)."""
    SV = P['SV']
    cy, ry = (y0 + y1) / 2, (y1 - y0) / 2
    eo = Ell(bx, cy, bw - bx, ry, k=P['kR'])
    iy0, iy1 = y0 + t_bot, y1 - t_top
    ei = Ell(bx, (iy0 + iy1) / 2, bw - bx - SV * P['rs'], (iy1 - iy0) / 2, k=P['kR'] + P['k_in'])
    return [rect(x0, y1 - t_top, bx + 1, y1), rect(x0, y0, bx + 1, y0 + t_bot),
            band(eo, ei, V(bx), (bx, y0), V(bx), (bx, y1))]


def cap_P(P):
    g = C(P); SV, SH, cap = g['SV'], g['SH'], g['cap']
    ym = P['R_ym'] - 22
    return [rect(0, 0, SV, cap)] + _bowl_r(P, SV - 2, ym, cap, P['R_bw'] * 1.0, P['R_bx'], SH, SH * 0.92)


def cap_B(P):
    g = C(P); SV, SH, cap = g['SV'], g['SH'], g['cap']
    ym = cap * 0.47
    up = _bowl_r(P, SV - 2, ym, cap, P['R_bw'] * 0.92, P['R_bx'] * 0.92, SH, SH * 0.9)
    lo = _bowl_r(P, SV - 2, 0, ym + SH * 0.9, P['R_bw'] * 1.0, P['R_bx'] * 0.98, SH * 0.9, SH)
    return [rect(0, 0, SV, cap)] + up + lo


def cap_F(P):
    cap, SV, SH = P['cap'], P['SV'], P['SH']
    top, mid_, _ = P['E_arms']
    ym = P['E_mid'] - 14
    return [rect(0, 0, SV, cap), rect(SV - 2, cap - SH, top, cap), rect(SV - 2, ym, mid_, ym + SH * 0.92)]


def cap_L(P):
    cap, SV, SH = P['cap'], P['SV'], P['SH']
    return [rect(0, 0, SV, cap), rect(SV - 2, 0, P['E_arms'][2] * 0.96, SH)]


def cap_H(P):
    cap, SV, SH = P['cap'], P['SV'], P['SH']
    W = P['wN'] * 0.97
    ym = P['E_mid'] + 6
    return [rect(0, 0, SV, cap), rect(W - SV, 0, W, cap), rect(SV - 2, ym, W - SV + 2, ym + SH * 0.92)]


def cap_T(P):
    cap, SV, SH = P['cap'], P['SV'], P['SH']
    W = P['E_arms'][2] * 1.18
    return [rect(0, cap - SH, W, cap), rect(W / 2 - SV / 2, 0, W / 2 + SV / 2, cap)]


def cap_J(P):
    g = C(P); SV, SH, cap = g['SV'], g['SH'], g['cap']
    W = P['E_arms'][2] * 0.98
    cyh = cap * 0.30
    phi, ang = P['e_term']
    eo = Ell(W * 0.52, cyh, W * 0.48, cyh + g['os'], rxL=W * 0.52, k=g['k'])
    ei = Ell(W * 0.52, cyh, W * 0.48 - SV, cyh + g['os'] - SH * P['rt'], rxL=W * 0.52 - SV * P['rs'],
             k=g['k'] + P['k_in'])
    t = term(eo, ei, 180 - phi + 6, None if ang is None else 180 - ang)
    return [rect(W - SV, cyh - 2, W, cap), band(eo, ei, t, mid(t), H(cyh), (W, cyh))]


def cap_M(P):
    cap, SV = P['cap'], P['SV']
    W = P['wN'] * 1.16
    sv = SV * 0.9
    hd = hw(SV * 0.92, (0, cap), (W / 2, 0))
    return [rect(0, 0, sv, cap), rect(W - sv, 0, W, cap),
            solid(poly([(0, cap), (hd, cap), (W / 2 + hd / 2, 0), (W / 2 - hd / 2, 0)])),
            solid(poly([(W - hd, cap), (W, cap), (W / 2 + hd / 2, 0), (W / 2 - hd / 2, 0)]))]


def cap_Q(P):
    c = cap_O(P)
    W = P['wO']
    p, q = (W * 0.56, P['cap'] * 0.22), (W * 0.86, -70)
    t = P['SV'] * 0.92
    return c + [stroke(p, q, t, perp(p, q, p), H(-70))]


def cap_S(P):
    g = C(P); SV, SH, cap, os_ = g['SV'], g['SH'], g['cap'], g['os']
    W = P['wO'] * 0.78
    wv, wh = SV * 1.0, SH * 0.98
    ry = (cap + 2 * os_) / 4
    rx = W / 2 - wv / 2
    up = Ell(W / 2, cap + os_ - ry, rx * 0.93, ry - wh / 4)
    lo = Ell(W / 2, ry - os_ + wh / 4, rx, ry - wh / 4)
    phi, ang = P['e_term']
    s1 = ell_path(up, 0.36, 2.22)
    s3 = ell_path(lo, 0.24, 2.38, cw=True)
    spine = joint(up.at(2.22), ell_tan(up, 2.22), lo.at(0.24), ell_tan(lo, 0.24, cw=True), 0.45)
    return [pen(s1 + [spine] + s3, wv, wh)]


def cap_U(P):
    g = C(P); SV, SH, cap = g['SV'], g['SH'], g['cap']
    W = P['wN'] * 0.96
    cy = cap * 0.36
    eo = Ell(W / 2, cy, W / 2, cy + g['os'], k=P['kO'] + 0.02)
    ei = Ell(W / 2, cy, W / 2 - SV * 0.98, cy + g['os'] - SH * P['rt'], k=P['kO'] + 0.02 + P['k_in'])
    return [rect(0, cy - 2, SV, cap), rect(W - SV, cy - 2, W, cap),
            band(eo, ei, H(cy), (0, cy), H(cy), (W, cy))]


def cap_V(P):
    return [vee(P['wA'], P['cap'], P['A_apex'], P['SV'], P['A_tl'], P['A_tr'])]


def cap_W(P):
    W1 = P['wA'] * 0.86
    t = P['SV']
    Ww = 2 * W1 - hw(t * P['A_tr'] * 0.96, (0, P['cap']), (W1 / 2, 0))
    a = vee(W1, P['cap'], P['A_apex'] * 0.8, P['SV'], P['A_tl'] * 0.96, P['A_tr'] * 0.96)
    return [a, translate([a], Ww - W1)[0]]


def cap_X(P):
    W, cap, t = P['wA'] * 0.94, P['cap'], P['SV'] * 0.95
    return [stroke((t * 0.55, 0), (W - t * 0.55, cap), t, H(0), H(cap)),
            stroke((t * 0.55, cap), (W - t * 0.55, 0), t * 0.9, H(cap), H(0))]


def cap_Y(P):
    W, cap, SV = P['wA'] * 0.94, P['cap'], P['SV']
    yj = cap * 0.42
    c = [rect(W / 2 - SV / 2, 0, W / 2 + SV / 2, yj + 10)]
    c.append(stroke((hw(SV, (0, cap), (W / 2, yj)) / 2, cap), (W / 2, yj), SV * 0.9, H(cap), H(yj - 30)))
    c.append(stroke((W - hw(SV, (W, cap), (W / 2, yj)) / 2, cap), (W / 2, yj), SV * 0.96, H(cap), H(yj - 30)))
    return c


def cap_Z(P):
    W, cap, SH, SV = P['E_arms'][2] * 1.2, P['cap'], P['SH'], P['SV']
    hd = hw(SV * 0.98, (0, SH), (W, cap - SH))
    return [bar(W * 0.04, W * 0.98, cap, SH), rect(0, 0, W, SH),
            solid(poly([(0, SH), (hd, SH), (W * 0.98, cap - SH), (W * 0.98 - hd, cap - SH)]))]


# ================================================================ chiffres
def fig_w(P):
    return P['wo'] * 1.0


def d0(P):
    W = fig_w(P); cap, os_ = P['cap'], P['os']
    eo, ei = ells(W / 2, cap / 2, W / 2, cap / 2 + os_, P['SV'] * P['rs'] * 0.98, P['SH'] * P['rt'],
                  P['kO'] + 0.02, P['k_in'])
    return ring(eo, ei)


def d1(P):
    W = fig_w(P); cap, SV, SH = P['cap'], P['SV'], P['SH']
    x = W * 0.56
    p, q = (x + SV * 0.2, cap - SH * 0.4), (x - W * 0.40, cap - 150)
    return [rect(x - SV / 2, 0, x + SV / 2, cap),
            stroke(p, q, SH * 1.0, perp(p, q, p), perp(p, q, q))]


def d2(P):
    W = fig_w(P); cap, SV, SH, os_ = P['cap'], P['SV'], P['SH'], P['os']
    wv, wh = SV * 0.98, SH * 0.98
    r = W / 2 - wv / 2
    e = Ell(W / 2, cap - r * 1.02 + os_ - wh / 2 + 6, r, r * 1.02)
    # tracé : terminaison gauche (≈ 160°) → haut → droite → descente vers le bas gauche
    arc = ell_path(e, 1.78, 3.72, cw=True)
    end = arc[-1][3]
    tail = joint(end, ell_tan(e, 3.72, cw=True), (wv * 0.5, SH * 0.9), (-0.55, -1), 0.5)
    phi, ang = P['e_term']
    return [pen(arc + [tail], wv, wh),
            rect(0, 0, W, SH)]


def d3(P):
    W = fig_w(P); cap, SV, SH, os_ = P['cap'], P['SV'], P['SH'], P['os']
    wv, wh = SV * 0.96, SH * 0.94
    ymid = cap * 0.56
    ru = (cap + os_ - ymid) / 2
    up = Ell(W * 0.48, ymid + ru, W * 0.44 - wv / 2, ru - wh / 4)
    rl = (ymid + os_) / 2
    lo = Ell(W * 0.50, rl - os_ + wh / 4, W / 2 - wv / 2, rl)
    phi, ang = P['e_term']
    s_up = ell_path(up, 1.75, 3.0, cw=True)
    s_lo = ell_path(lo, 1.0, 2.28, cw=True)
    xm = W * 0.30
    c1 = pen(s_up + [line_seg(s_up[-1][3], (xm, s_up[-1][3][1]))], wv, wh)
    c2 = pen([line_seg((xm, lo.at(1.0)[1]), lo.at(1.0))] + s_lo, wv, wh)
    return [c1, c2]


def d4(P):
    W = fig_w(P) * 1.04; cap, SV, SH = P['cap'], P['SV'], P['SH']
    xs = W * 0.66
    yb = cap * 0.27
    hd = hw(SV * 0.9, (xs, cap), (0, yb + SH))
    return [rect(xs, 0, xs + SV, cap), rect(0, yb, W, yb + SH * 0.94),
            solid(poly([(xs + 10, cap), (xs + 10, cap - hd * 0.9), (hd * 0.15 + 10, yb + SH * 0.94),
                        (-0, yb + SH * 0.94), (0, yb + SH * 0.94 + 4), (xs + 10 - hd, cap)]))]


def d5(P):
    W = fig_w(P); cap, SV, SH, os_ = P['cap'], P['SV'], P['SH'], P['os']
    wv, wh = SV * 0.96, SH * 0.94
    xl = W * 0.12
    rl = cap * 0.31
    lo = Ell(W * 0.5, rl - os_ + wh / 4 + 8, W / 2 - wv / 2, rl + 12)
    yj = cap * 0.40
    s = [joint((xl + wv / 2, yj + 30), (0.5, 1), lo.at(1.0), (1, 0), 0.5)] + ell_path(lo, 1.0, 2.25, cw=True)
    phi, ang = P['e_term']
    return [rect(xl, cap - SH, W * 0.9, cap),
            stroke((xl + wv * 0.62, cap), (xl + wv * 0.38, yj + 30), wv * 0.92, H(cap), H(yj + 10)),
            pen(s, wv, wh)]


def d6(P):
    W = fig_w(P); cap, SV, SH, os_ = P['cap'], P['SV'], P['SH'], P['os']
    wv, wh = SV * 0.98, SH * 0.96
    hb = cap * 0.62
    eo, ei = ells(W / 2, hb / 2 - os_ / 2, W / 2, hb / 2 + os_ / 2, wv, wh, P['ko'] + 0.01, P['k_in'])
    left = (wv / 2, hb / 2 - os_ / 2)
    top = (W * 0.84, cap - 110)
    s = [joint(left, (0, 1), (W * 0.50, cap + os_ - wh / 2), (1, 0), 0.6),
         joint((W * 0.50, cap + os_ - wh / 2), (1, 0), top, (0.55, -0.85), 0.45)]
    return ring(eo, ei) + [pen(s, wv, wh)]


def d9(P):
    W = fig_w(P)
    return rot180(d6(P), W, P['cap'])


def d7(P):
    W = fig_w(P); cap, SV, SH = P['cap'], P['SV'], P['SH']
    p, q = (W - SV * 0.55, cap - SH), (W * 0.26, 0)
    return [rect(0, cap - SH, W, cap), stroke(p, q, SV * 0.95, H(cap - SH + 4), H(0))]


def d8(P):
    W = fig_w(P); cap, SV, SH, os_ = P['cap'], P['SV'], P['SH'], P['os']
    hl = cap * 0.55; hu = cap - hl + SH * 0.9
    lo = ells(W / 2, hl / 2 - os_ / 2, W / 2, hl / 2 + os_ / 2, SV * 0.98, SH * 0.96, P['ko'], P['k_in'])
    uw = W * 0.88
    up = ells(W / 2, cap - hu / 2 + os_ / 2, uw / 2, hu / 2 + os_ / 2, SV * 0.94, SH * 0.94, P['ko'], P['k_in'])
    return ring(*lo) + ring(*up)


# ============================================================ ponctuation
def pu(P):
    return dict(d=P['dot'] * 0.98, sv=P['sv'], sh=P['sh'], xh=P['xh'], cap=P['cap'])


def p_period(P):
    d = P['dot'] * 0.98
    return [dot(d / 2, d / 2 - 2, d)]


def p_comma(P):
    d = P['dot'] * 0.98
    p, q = (d * 0.62, d * 0.45), (d * 0.12, -150)
    return [dot(d / 2, d / 2 - 2, d), stroke(p, q, d * 0.62, perp(p, q, p), perp(p, q, q), wq=d * 0.34)]


def p_colon(P):
    d = P['dot'] * 0.98
    return [dot(d / 2, d / 2 - 2, d), dot(d / 2, P['xh'] - d / 2 + 2, d)]


def p_semicolon(P):
    d = P['dot'] * 0.98
    return p_comma(P) + [dot(d / 2, P['xh'] - d / 2 + 2, d)]


def p_excl(P):
    d = P['dot'] * 0.98; sv = P['sv']
    x = d / 2
    return [dot(x, d / 2 - 2, d),
            solid(poly([(x - sv * 0.52, P['cap']), (x + sv * 0.52, P['cap']),
                        (x + sv * 0.36, d + 110), (x - sv * 0.36, d + 110)]))]


def p_quest(P):
    d = P['dot'] * 0.98; sv, sh, cap = P['sv'], P['sh'], P['cap']
    W = P['wo'] * 0.86
    r = W / 2 - sv / 2
    e = Ell(W / 2, cap - r + P['os'] - sh / 2, r, r)
    arc = ell_path(e, 1.78, 3.55, cw=True)
    xs = W * 0.48
    tail = joint(arc[-1][3], ell_tan(e, 3.55, cw=True), (xs, d + 150), (0, -1), 0.5)
    return [pen(arc + [tail], sv, sh), rect(xs - sv * 0.47, d + 110, xs + sv * 0.47, d + 152),
            dot(xs, d / 2 - 2, d)]


def p_quote(P):
    sv, cap = P['sv'], P['cap']
    return [solid(poly([(0, cap), (sv * 0.9, cap), (sv * 0.75, cap - 230), (sv * 0.15, cap - 230)]))]


def p_dquote(P):
    sv = P['sv']
    return p_quote(P) + translate(p_quote(P), sv * 0.9 + 70)


def p_hyphen(P):
    W = P['wn'] * 0.62
    y = P['xh'] * 0.5 + P['sh'] * 0.5
    return [bar(0, W, y, P['sh'] * 0.98)]


def p_under(P):
    W = P['wn'] * 1.1
    return [rect(0, -140, W, -140 + P['sh'])]


def _paren(P):
    sv, sh = P['sv'], P['sh']
    top, bot = P['asc'] + 20, P['desc'] + 40
    h = (top - bot) / 2
    e = Ell(260, bot + h, 250, h)
    arc = ell_path(e, 1.30, 2.70)
    return [pen(arc, sv * 0.98, sh, cut0=-90 + 0, cut1=90)]


def p_lparen(P):
    return _paren(P)


def p_rparen(P):
    c = _paren(P)
    from geom import flatten
    xs = [x for cc in c for x, _ in flatten(cc)]
    W = max(xs) + min(xs)
    return mirror(c, W)


def p_lbrack(P):
    sv, sh = P['sv'], P['sh']
    top, bot = P['asc'] + 20, P['desc'] + 40
    W = sv + 110
    return [rect(0, bot, sv, top), rect(sv - 2, top - sh, W, top), rect(sv - 2, bot, W, bot + sh)]


def p_rbrack(P):
    W = P['sv'] + 110
    return mirror(p_lbrack(P), W)


def p_lbrace(P):
    sv, sh = P['sv'] * 0.92, P['sh']
    top, bot = P['asc'] + 20, P['desc'] + 40
    m = (top + bot) / 2
    W = 230
    x = W * 0.42
    segs = [joint((W, top - sh / 2), (-1, 0), (x, top - 130), (0, -1), 0.6),
            line_seg((x, top - 130), (x, m + 90)),
            joint((x, m + 90), (0, -1), (sv * 0.4, m), (-1, -0.4), 0.6)]
    s2 = [joint((sv * 0.4, m), (1, -0.4), (x, m - 90), (0, -1), 0.6),
          line_seg((x, m - 90), (x, bot + 130)),
          joint((x, bot + 130), (0, -1), (W, bot + sh / 2), (1, 0), 0.6)]
    return [pen(segs, sv, sh, cut0=90), pen(s2, sv, sh, cut1=90)]


def p_rbrace(P):
    return mirror(p_lbrace(P), 230)


def p_slash(P):
    t = P['sv'] * 0.9
    top, bot = P['cap'] + 40, P['desc'] + 60
    W = 330
    return [stroke((t / 2, bot), (W - t / 2, top), t, H(bot), H(top))]


def p_bslash(P):
    return mirror(p_slash(P), 330)


def p_bar(P):
    return [rect(0, P['desc'] + 10, P['sv'] * 0.92, P['asc'] + 30)]


def p_equal(P):
    W = P['wn'] * 1.0; sh = P['sh']; y = P['xh'] * 0.5 + 6
    return [bar(0, W, y + 100 + sh / 2, sh), bar(0, W, y - 100 + sh / 2, sh)]


def p_plus(P):
    W = P['wn'] * 1.0; sh, sv = P['sh'], P['sv']; y = P['xh'] * 0.5 + 6
    return [bar(0, W, y + sh / 2, sh), rect(W / 2 - sv / 2 + 2, y - W / 2 + 10, W / 2 + sv / 2 - 2, y + W / 2 - 10)]


def p_minus(P):
    W = P['wn'] * 1.0; sh = P['sh']; y = P['xh'] * 0.5 + 6
    return [bar(0, W, y + sh / 2, sh)]


def p_star(P):
    sv = P['sv'] * 0.86; cx, cy, r = 190, P['cap'] - 170, 165
    c = []
    for a in (90, 30, 150):
        ra = math.radians(a)
        p = (cx - math.cos(ra) * r, cy - math.sin(ra) * r)
        q = (cx + math.cos(ra) * r, cy + math.sin(ra) * r)
        c.append(stroke(p, q, sv, perp(p, q, p), perp(p, q, q)))
    return c


def _chev(P, W, flip):
    t = P['sv'] * 0.92; y = P['xh'] * 0.5 + 6; h = 190
    a, b, cpt = (W, y + h), (0, y), (W, y - h)
    c = [stroke(a, b, t, perp(a, b, a), V(t * 0.3)), stroke(cpt, b, t, perp(cpt, b, cpt), V(t * 0.3))]
    return mirror(c, W) if flip else c


def p_less(P):
    return _chev(P, P['wn'] * 0.95, False)


def p_greater(P):
    return _chev(P, P['wn'] * 0.95, True)


def p_hash(P):
    sh, sv = P['sh'], P['sv'] * 0.9
    W, top = P['wn'] * 1.12, P['cap'] - 20
    c = [bar(0, W, top * 0.68 + sh / 2, sh), bar(0, W, top * 0.34 + sh / 2, sh)]
    for x in (W * 0.33, W * 0.7):
        c.append(stroke((x - 30, 0), (x + 30, top), sv, H(0), H(top)))
    return c


def p_at(P):
    sv, sh, cap = P['sv'] * 0.88, P['sh'] * 0.9, P['cap']
    W = cap * 1.08
    cy = cap * 0.40
    eo = Ell(W / 2, cy, W / 2, cap * 0.62, k=P['ko'])
    ei = Ell(W / 2, cy, W / 2 - sv, cap * 0.62 - sh, k=P['ko'] + P['k_in'])
    a = term(eo, ei, -8, None); b = term(eo, ei, -50, None)
    outer = band(eo, ei, a, mid(a), b, mid(b))
    ix = W * 0.48; ir = W * 0.17
    ie = ells(ix, cy, ir, cap * 0.22, sv * 0.95, sh, P['ko'], P['k_in'])
    st = rect(ix + ir - sv, cy - cap * 0.2, ix + ir, cy + cap * 0.24)
    foot = joint((ix + ir - sv / 2, cy - cap * 0.18), (0, -1), (W - sv / 2, cy - 30), (0.3, 1), 0.6)
    return [outer, st, pen([foot], sv, sh)] + ring(*ie)


def p_amp(P):
    sv, sh, cap = P['SV'] * 0.95, P['SH'] * 0.95, P['cap']
    W = P['wo'] * 1.3
    pts = [
        ((W * 0.98, 0), (-0.75, 1)),
        ((W * 0.36, cap * 0.62), (-0.4, 0.9)),
        ((W * 0.40, cap - sh / 2), (1, 0)),
        ((W * 0.66, cap * 0.80), (-0.3, -1)),
        ((W * 0.22, cap * 0.40), (-0.6, -0.9)),
        ((W * 0.44, sh / 2 - 8), (1, 0)),
        ((W * 0.86, cap * 0.38), (0.25, 1)),
    ]
    segs = [joint(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 0.45) for i in range(len(pts) - 1)]
    return [pen(segs, sv, sh)]


def p_percent(P):
    sv, sh, cap = P['sv'] * 0.86, P['sh'] * 0.86, P['cap']
    r = 115; W = 640
    a = ells(r, cap - r - 10, r, r + 10, sv, sh, P['ko'], P['k_in'])
    b = ells(W - r, r, r, r + 10, sv, sh, P['ko'], P['k_in'])
    return ring(*a) + ring(*b) + [stroke((W * 0.22, 0), (W * 0.78, cap), sv * 0.95, H(0), H(cap))]


def p_dollar(P):
    c = cap_S(P)
    from geom import flatten
    xs = [x for cc in c for x, _ in flatten(cc)]
    x = (min(xs) + max(xs)) / 2
    return c + [rect(x - P['sv'] * 0.4, -90, x + P['sv'] * 0.4, P['cap'] + 90)]


def p_tilde(P):
    sv, sh = P['sv'] * 0.92, P['sh']
    y = P['xh'] * 0.5 + 10; W = P['wn'] * 1.0
    segs = [joint((sv * 0.4, y - 40), (0.6, 1), (W * 0.33, y + 55), (1, 0), 0.5),
            joint((W * 0.33, y + 55), (1, 0), (W * 0.67, y - 55), (1, 0), 0.5),
            joint((W * 0.67, y - 55), (1, 0), (W - sv * 0.4, y + 40), (0.6, 1), 0.5)]
    return [pen(segs, sv, sh)]


def p_grave(P):
    return _accent(P, 'grave')


def p_caret(P):
    t = P['sv'] * 0.86
    W, top, y0 = 420, P['cap'], P['cap'] - 260
    a, b, c = (0, y0), (W / 2, top), (W, y0)
    return [stroke((t * 0.6, y0), (W / 2, top), t, H(y0), H(top)),
            stroke((W - t * 0.6, y0), (W / 2, top), t, H(y0), H(top))]


# ================================================================ accents
def _accent(P, kind, base_top=None, cx=0):
    sv, sh = P['sv'], P['sh']
    y0 = (base_top or P['xh']) + 70
    t = sv * 0.86
    if kind == 'acute':
        p, q = (cx - 40, y0), (cx + 70, y0 + 150)
        return [stroke(p, q, t, perp(p, q, p), perp(p, q, q), wq=t * 1.1)]
    if kind == 'grave':
        p, q = (cx + 40, y0), (cx - 70, y0 + 150)
        return [stroke(p, q, t, perp(p, q, p), perp(p, q, q), wq=t * 1.1)]
    if kind == 'circ':
        return [stroke((cx - 120, y0), (cx, y0 + 150), t, H(y0), H(y0 + 150)),
                stroke((cx + 120, y0), (cx, y0 + 150), t, H(y0), H(y0 + 150))]
    if kind == 'diaer':
        d = P['dot'] * 0.95
        return [dot(cx - 95, y0 + 60, d), dot(cx + 95, y0 + 60, d)]
    raise ValueError(kind)


def cedilla(P, cx):
    sh, sv = P['sh'], P['sv'] * 0.8
    segs = [line_seg((cx, 10), (cx, -55)),
            joint((cx, -55), (1, 0), (cx + 60, -125), (0, -1), 0.6),
            joint((cx + 60, -125), (0, -1), (cx - 60, -200), (-1, 0), 0.6)]
    return [pen(segs, sv, sh * 0.85)]


def bbox_x(contours):
    from geom import flatten
    xs = [x for c in contours for x, _ in flatten(c)]
    return min(xs), max(xs)


def compose(base_fn, kind, caps=False, shift=0):
    def f(P):
        c = base_fn(P)
        x0, x1 = bbox_x(c)
        cx = (x0 + x1) / 2 + shift
        if kind == 'cedilla':
            return c + cedilla(P, cx)
        top = P['cap'] if caps else P['xh']
        acc = _accent(P, kind, top + (10 if caps else 0), cx)
        if caps:
            acc = xform(acc, lambda p: (p[0], p[1] - 30))
        return c + acc
    return f


def lc_idot(kind):
    def f(P):
        sv = P['sv']
        return [rect(0, 0, sv, P['xh'])] + _accent(P, kind, P['xh'], sv / 2)
    return f


GLYPHS = dict(CORE)
GLYPHS.update({
    'b': lc_b, 'c': lc_c, 'd': lc_d, 'f': lc_f, 'g': lc_g, 'h': lc_h, 'j': lc_j, 'l': lc_l,
    'm': lc_m, 'p': lc_p, 'q': lc_q, 's': lc_s, 't': lc_t, 'u': lc_u, 'v': lc_v, 'w': lc_w,
    'x': lc_x, 'y': lc_y, 'z': lc_z,
    'B': cap_B, 'C': cap_C, 'D': cap_D, 'F': cap_F, 'G': cap_G, 'H': cap_H, 'J': cap_J,
    'L': cap_L, 'M': cap_M, 'P': cap_P, 'Q': cap_Q, 'S': cap_S, 'T': cap_T, 'U': cap_U,
    'V': cap_V, 'W': cap_W, 'X': cap_X, 'Y': cap_Y, 'Z': cap_Z,
    '0': d0, '1': d1, '2': d2, '3': d3, '4': d4, '5': d5, '6': d6, '7': d7, '8': d8, '9': d9,
    '.': p_period, ',': p_comma, ':': p_colon, ';': p_semicolon, '!': p_excl, '?': p_quest,
    "'": p_quote, '"': p_dquote, '-': p_hyphen, '_': p_under, '(': p_lparen, ')': p_rparen,
    '[': p_lbrack, ']': p_rbrack, '{': p_lbrace, '}': p_rbrace, '/': p_slash, '\\': p_bslash,
    '|': p_bar, '=': p_equal, '+': p_plus, '*': p_star, '<': p_less, '>': p_greater,
    '#': p_hash, '@': p_at, '&': p_amp, '%': p_percent, '$': p_dollar, '~': p_tilde,
    '`': p_grave, '^': p_caret,
    'é': compose(CORE['e'], 'acute'), 'è': compose(CORE['e'], 'grave'),
    'ê': compose(CORE['e'], 'circ'), 'ë': compose(CORE['e'], 'diaer'),
    'à': compose(CORE['a'], 'grave', shift=-20), 'â': compose(CORE['a'], 'circ', shift=-20),
    'ù': compose(lc_u, 'grave', shift=-20), 'û': compose(lc_u, 'circ', shift=-20),
    'ô': compose(CORE['o'], 'circ'), 'ç': compose(lc_c, 'cedilla'),
    'î': lc_idot('circ'), 'ï': lc_idot('diaer'),
    'É': compose(CORE['E'], 'acute', caps=True, shift=-20), 'È': compose(CORE['E'], 'grave', caps=True, shift=-20),
    'Ê': compose(CORE['E'], 'circ', caps=True, shift=-20), 'À': compose(CORE['A'], 'grave', caps=True),
    'Ç': compose(cap_C, 'cedilla'),
})

KIND = {}
for ch in GLYPHS:
    if ch.isalpha() and ch.isupper():
        KIND[ch] = 'uc'
    elif ch.isalpha():
        KIND[ch] = 'lc'
    elif ch.isdigit():
        KIND[ch] = 'fig'
    else:
        KIND[ch] = 'punct'
