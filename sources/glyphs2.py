"""Arkerion Sans — étude n°2. Dessin paramétrique des glyphes de « Arkerion ».

Les glyphes sont dessinés à partir de x = 0 sans approches : l'espacement est
calculé ensuite par spacing.py (méthode des aires de blanc, profondeur limitée).
Toutes les épaisseurs sont exprimées en épaisseur réelle (perpendiculaire au
trait), y compris pour les diagonales.
"""
import math
from geom import (Ell, ring, band, rect, stroke, poly, solid, hole, H, V,
                  intersect, from_curves)


def term(eo, ei, phi, ang=None):
    """Coupe de terminaison passant par le milieu du trait à l'angle polaire
    phi (°) de la courbe ; inclinaison ang° (None = radiale, ⟂ au trait)."""
    cx, cy = eo.segs[1][0][0], eo.segs[0][0][1]
    ux, uy = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    ray = ((cx, cy), (cx + ux, cy + uy))
    far = (cx + ux * 3000, cy + uy * 3000)
    po = eo.at(eo.cross(ray, far)); pi = ei.at(ei.cross(ray, far))
    m = ((po[0] + pi[0]) / 2, (po[1] + pi[1]) / 2)
    a = math.radians(phi if ang is None else ang)
    dx, dy = math.cos(a), math.sin(a)
    return ((m[0] - dx * 600, m[1] - dy * 600), (m[0] + dx * 600, m[1] + dy * 600))


def mid(l):
    return ((l[0][0] + l[1][0]) / 2, (l[0][1] + l[1][1]) / 2)


def hw(t, p, q):
    """Largeur horizontale d'un trait d'épaisseur réelle t, d'axe p→q."""
    ang = math.atan2(abs(q[1] - p[1]), abs(q[0] - p[0]))
    return t / math.sin(ang)


# ================================================================ CAPITALES
def cap_A(P):
    W, cap, SV, SH = P['wA'], P['cap'], P['SV'], P['SH']
    af = P['A_apex']
    xa, xb = W / 2 - af / 2, W / 2 + af / 2
    hL = hw(SV * P['A_tl'], (0, 0), (xa, cap))
    hR = hw(SV * P['A_tr'], (W, 0), (xb, cap))
    Lin = ((hL, 0), (xa + hL, cap)); Rin = ((W - hR, 0), (xb - hR, cap))
    y0 = P['A_bar']; y1 = y0 + SH * 0.92
    outer = poly([(0, 0), (xa, cap), (xb, cap), (W, 0), (W - hR, 0),
                  intersect(Rin, H(y0)), intersect(Lin, H(y0)), (hL, 0)])
    counter = poly([intersect(Lin, H(y1)), intersect(Rin, H(y1)), intersect(Lin, Rin)])
    return [solid(outer), hole(counter)]


def cap_E(P):
    cap, SV, SH = P['cap'], P['SV'], P['SH']
    top, mid_, bot = P['E_arms']
    ym = P['E_mid']
    return [rect(0, 0, SV, cap),
            rect(SV - 2, cap - SH, top, cap),
            rect(SV - 2, ym, mid_, ym + SH * 0.92),
            rect(SV - 2, 0, bot, SH)]


def cap_I(P):
    return [rect(0, 0, P['SV'], P['cap'])]


def cap_N(P):
    W, cap = P['wN'], P['cap']
    sv = P['SV'] * P['N_stem']
    hd = hw(P['SV'] * P['N_diag'], (0, cap), (W, 0))
    return [rect(0, 0, sv, cap), rect(W - sv, 0, W, cap),
            solid(poly([(0, cap), (hd, cap), (W, 0), (W - hd, 0)]))]


def cap_O(P):
    W, cap, os_ = P['wO'], P['cap'], P['os']
    rx, ry = W / 2, cap / 2 + os_
    eo = Ell(rx, cap / 2, rx, ry, k=P['kO'])
    ei = Ell(rx, cap / 2, rx - P['SV'] * P['rs'], ry - P['SH'] * P['rt'],
             k=P['kO'] + P['k_in'])
    return ring(eo, ei)


def cap_R(P):
    cap, SV, SH = P['cap'], P['SV'], P['SH']
    bw, bx, ym = P['R_bw'], P['R_bx'], P['R_ym']
    hb = SH * 0.92
    cy, ry = (cap + ym) / 2, (cap - ym) / 2
    eo = Ell(bx, cy, bw - bx, ry, k=P['kR'])
    iy0, iy1 = ym + hb, cap - SH
    ei = Ell(bx, (iy0 + iy1) / 2, bw - bx - SV * P['rs'], (iy1 - iy0) / 2,
             k=P['kR'] + P['k_in'])
    c = [rect(0, 0, SV, cap), rect(SV - 2, cap - SH, bx + 1, cap),
         rect(SV - 2, ym, bx + 1, ym + hb),
         band(eo, ei, V(bx), (bx, ym), V(bx), (bx, cap))]
    xs = SV + (bw - SV) * P['R_leg_from']
    p, q = (xs, ym + hb / 2), (P['R_leg_to'], 0)
    t = SV * P['R_leg_t']
    c.append(stroke(p, q, t, H(ym + hb * 0.5), H(0), wq=t * P.get('R_leg_flare', 1)))
    return c


def k_branches(P, top, sv, yj, x_arm, x_leg, t_arm, t_leg, leg_from, taper):
    p, q = (sv * 0.5, yj), (x_arm, top)
    arm = stroke(p, q, t_arm * taper, V(sv * 0.5), H(top), wq=t_arm)
    if leg_from <= 0:
        lp = (sv * 0.5, yj + 30)
        leg = stroke(lp, (x_leg, 0), t_leg * taper, V(sv * 0.5), H(0), wq=t_leg)
    else:
        lp = (p[0] + (q[0] - p[0]) * leg_from, p[1] + (q[1] - p[1]) * leg_from)
        leg = stroke(lp, (x_leg, 0), t_leg, (p, q), H(0))
    return [arm, leg]


def cap_K(P):
    cap, SV = P['cap'], P['SV']
    return [rect(0, 0, SV, cap)] + k_branches(
        P, cap, SV, P['K_join'], P['K_arm_x'], P['K_leg_x'],
        SV * P['K_arm_t'], SV * P['K_leg_t'], P['K_leg_from'], P['K_taper'])


# ================================================================ BAS-DE-CASSE
def lc_i(P):
    sv, xh, d = P['sv'], P['xh'], P['dot']
    e = Ell(sv / 2, P['dot_y'], d / 2, d / 2, k=P.get('dot_k', 0.5523))
    return [rect(0, 0, sv, xh), solid(from_curves(e.arc(0, 4)))]


def lc_o(P):
    W, xh, os_ = P['wo'], P['xh'], P['osx']
    rx, ry = W / 2, xh / 2 + os_
    eo = Ell(rx, xh / 2, rx, ry, k=P['ko'])
    ei = Ell(rx, xh / 2, rx - P['sv'] * P['rs'], ry - P['sh'] * P['rt'], k=P['ko'] + P['k_in'])
    return ring(eo, ei)


def arch(P, W, sv, sh, cx_f, cy_f=None):
    xh, os_ = P['xh'], P['osx']
    cy = xh * (cy_f or P['arch_cy'])
    cxo = W * cx_f
    eo = Ell(cxo, cy, W - cxo, xh + os_ - cy, rxL=cxo, ryB=cy, k=P['k_arch'])
    cxi = cxo - P['arch_shift']
    ei = Ell(cxi, cy, (W - sv * P['rs']) - cxi, xh + os_ - sh * P['arch_thin'] - cy,
             rxL=cxi - sv * P['arch_crotch'], ryB=cy, k=P['k_arch'] + P['k_in'])
    return eo, ei, cy


def lc_n(P):
    W, xh, sv, sh = P['wn'], P['xh'], P['sv'], P['sh']
    eo, ei, cy = arch(P, W, sv, sh, P['arch_cx'])
    return [rect(0, 0, sv, xh), rect(W - sv * P['rs'], 0, W, cy + 2),
            band(eo, ei, H(cy), (W, cy), V(sv * 0.8), (sv, xh))]


def lc_r(P):
    W, xh, sv, sh = P['wr'], P['xh'], P['sv'], P['sh']
    eo, ei, cy = arch(P, W, sv * P['r_ear'], sh * P.get('r_thin', 1), P['r_cx'], P.get('r_cy'))
    cut = term(eo, ei, *P['r_term'])
    return [rect(0, 0, sv, xh), band(eo, ei, cut, mid(cut), V(sv * 0.8), (sv, xh))]


def lc_e(P):
    W, xh, os_, sv, sh = P['we'], P['xh'], P['osx'], P['sv'], P['sh']
    rx, ry = W / 2, xh / 2 + os_
    eo = Ell(rx, xh / 2, rx, ry, k=P['ko'])
    ei = Ell(rx, xh / 2, rx - sv * P['rs'], ry - sh * P['rt'], k=P['ko'] + P['k_in'])
    yb = P['e_bar']; hb = sh * 0.88
    cut = term(eo, ei, *P['e_term'])
    return [band(eo, ei, H(yb), (W, yb), cut, mid(cut)),
            rect(sv * 0.5, yb, W - sv * 0.5, yb + hb)]


def lc_a(P):
    W, xh, os_, sv, sh = P['wa'], P['xh'], P['osx'], P['sv'], P['sh']
    cyh = xh * P['a_hood_cy']
    hx = W - P['a_hood_rx']
    eo = Ell(hx, cyh, P['a_hood_rx'], xh + os_ - cyh, rxL=hx - P['a_hood_l'], ryB=cyh, k=P['ko'])
    ei = Ell(hx, cyh, P['a_hood_rx'] - sv, xh + os_ - sh * P['rt'] - cyh,
             rxL=hx - P['a_hood_l'] - sv * P['rs'] * 0.92, ryB=cyh, k=P['ko'] + P['k_in'])
    cut = term(eo, ei, *P['a_term'])
    hood = band(eo, ei, H(cyh), (W, cyh), cut, mid(cut))
    bt = P['a_bowl_top']
    cyb = (bt - os_) / 2
    brx = P['a_bowl_rx']
    bo = Ell(W - brx, cyb, brx, bt - cyb, rxL=W - brx, ryB=cyb + os_, k=P['ka'])
    bi = Ell(W - brx + 4, cyb + sh * 0.02, brx - sv * 0.62, bt - cyb - sh * P['a_bowl_top_t'],
             rxL=W - brx - sv * P['rs'] + 4, ryB=cyb + os_ - sh * P['rt'], k=P['ka'] + P['k_in'])
    bowl = band(bo, bi, V(W - sv * 0.75), (W, bt), V(W - sv * 0.75), (W, 0))
    return [rect(W - sv, 0, W, cyh + 2), hood, bowl]


def lc_k(P):
    asc, xh, sv = P['asc'], P['xh'], P['sv']
    return [rect(0, 0, sv, asc)] + k_branches(
        P, xh, sv, P['k_join'], P['k_arm_x'], P['k_leg_x'],
        sv * P['k_arm_t'], sv * P['k_leg_t'], P['k_leg_from'], P['K_taper'])


GLYPHS = {
    'A': cap_A, 'R': cap_R, 'K': cap_K, 'E': cap_E, 'I': cap_I, 'O': cap_O, 'N': cap_N,
    'a': lc_a, 'r': lc_r, 'k': lc_k, 'e': lc_e, 'i': lc_i, 'o': lc_o, 'n': lc_n,
}
CAPS = set('ARKEION')
