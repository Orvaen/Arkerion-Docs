"""Arkerion Sans — dessin paramétrique des glyphes de l'étude ARKERION.

Chaque fonction reçoit les paramètres P d'une direction et renvoie
(contours, chasse). Les glyphes sont construits avec l'approche sidebearing
gauche intégrée : x = 0 correspond à l'origine de la chasse.
"""
import math
from geom import (Ell, ring, band, rect, stroke, poly, solid, hole, H, V,
                  translate, intersect)


def _mid(l):
    return ((l[0][0] + l[1][0]) / 2, (l[0][1] + l[1][1]) / 2)


def xmax(contours):
    from geom import flatten
    return max(x for c in contours for x, _ in flatten(c))


def glyph(contours, lsb, body, rsb):
    return translate(contours, lsb), lsb + body + rsb


# ================================================================ CAPITALES
def cap_A(P):
    W = P['wA']; cap = P['cap']; af = P['A_apex']
    hL, hR = P['A_thin'], P['A_thick']          # épaisseurs horizontales des jambages
    xa, xb = W / 2 - af / 2, W / 2 + af / 2
    ya, yb = cap + P['A_apex_dy'][0], cap + P['A_apex_dy'][1]
    Lout = ((0, 0), (xa, ya)); Rout = ((W, 0), (xb, yb))
    Lin = ((hL, 0), (xa + hL, ya)); Rin = ((W - hR, 0), (xb - hR, yb))
    y0, y1 = P['A_bar'], P['A_bar'] + P['SH'] * 0.96
    apex_in = intersect(Lin, Rin)
    outer = poly([(0, 0), (xa, ya), (xb, yb), (W, 0), (W - hR, 0),
                  intersect(Rin, H(y0)), intersect(Lin, H(y0)), (hL, 0)])
    counter = poly([intersect(Lin, H(y1)), intersect(Rin, H(y1)), apex_in])
    return glyph([solid(outer), hole(counter)], P['sb_diag'], W, P['sb_diag'])


def cap_E(P):
    cap, SV, SH = P['cap'], P['SV'], P['SH']
    top, mid, bot = P['E_arms']
    ym = P['E_mid']
    c = [rect(0, 0, SV, cap),
         rect(SV - 4, cap - SH, top, cap),
         rect(SV - 4, ym, mid, ym + SH * 0.94),
         rect(SV - 4, 0, bot, SH)]
    W = max(top, mid, bot)
    return glyph(c, P['sb_stem'], W, P['sb_open'])


def cap_I(P):
    return glyph([rect(0, 0, P['SV'], P['cap'])], P['sb_stem'], P['SV'], P['sb_stem'])


def cap_N(P):
    W, cap = P['wN'], P['cap']
    sv = P['SV'] * P['N_stem']; hd = P['N_diag']
    c = [rect(0, 0, sv, cap - P['N_notch']), rect(W - sv, P['N_notch'], W, cap),
         solid(poly([(0, cap), (hd, cap), (W, 0), (W - hd, 0)]))]
    return glyph(c, P['sb_stem'], W, P['sb_stem'])


def cap_O(P):
    W, cap, os_ = P['wO'], P['cap'], P['os']
    rx, ry = W / 2, cap / 2 + os_
    k = P['kO']
    eo = Ell(W / 2, cap / 2, rx, ry, k=k)
    ei = Ell(W / 2, cap / 2, rx - P['SV'] * 1.07, ry - P['SH'] * 0.98, k=k + P['k_in'])
    return glyph(ring(eo, ei), P['sb_round'], W, P['sb_round'])


def cap_R(P):
    W, cap, SV, SH = P['wR'], P['cap'], P['SV'], P['SH']
    bw = P['R_bowl']                     # largeur hors-tout de la panse
    ym = P['R_join']                     # bas de la barre de jonction
    bx = P['R_bx']                       # début de la courbe de la panse
    cy = (cap + ym) / 2
    ry = (cap - ym) / 2
    eo = Ell(bx, cy, bw - bx, ry, k=P['kR'])
    iy0, iy1 = ym + P['R_hbar'], cap - SH
    ei = Ell(bx, (iy0 + iy1) / 2, bw - bx - SV * 1.04, (iy1 - iy0) / 2,
             k=P['kR'] + P['k_in'])
    c = [rect(0, 0, SV, cap),
         rect(SV - 4, cap - SH, bx + 1, cap),
         rect(SV - 4, ym, bx + 1, ym + P['R_hbar']),
         band(eo, ei, V(bx), (bx, ym), V(bx), (bx, cap))]
    # jambe
    p, q = P['R_leg'](P)
    wl = P['R_legw']
    c.append(stroke(p, q, wl, P['R_legcut'](P), H(0), wq=wl * P.get('R_flare', 1.0)))
    return glyph(c, P['sb_stem'], W, P['sb_diag'])


def cap_K(P):
    W, cap, SV = P['wK'], P['cap'], P['SV']
    c = [rect(0, 0, SV, cap)]
    c += _k_branches(P, W, cap, SV, P['K_join'], P['K_arm_w'], P['K_leg_w'],
                     P['K_mode'], P['K_legfrom'])
    return glyph(c, P['sb_stem'], W, P['sb_diag'])


def _k_branches(P, W, top, sv, yj, wa, wl, mode, legfrom):
    """Bras et jambe de K / k.
    mode 'stem' : bras et jambe partent du fût (même point) ;
    mode 'arm'  : la jambe naît du bras (à la fraction legfrom de sa longueur)."""
    # axe du bras : du fût au coin haut-droit
    p = (sv * 0.55, yj)
    q = (W - wa * 0.62, top)
    arm = stroke(p, q, wa, V(sv * 0.5), H(top))
    if mode == 'stem':
        lp = (sv * 0.55, yj + 40)
    else:
        lp = (p[0] + (q[0] - p[0]) * legfrom, p[1] + (q[1] - p[1]) * legfrom)
    lq = (W - wl * 0.62, 0)
    if mode == 'stem':
        leg = stroke(lp, lq, wl, V(sv * 0.5), H(0))
    else:
        # coupe de départ : axe du bras (la jambe s'enracine dans le bras)
        leg = stroke(lp, lq, wl, (p, q), H(0))
    return [arm, leg]


# ================================================================ BAS-DE-CASSE
def lc_i(P):
    sv, xh = P['sv'], P['xh']
    d = P['dot']
    cx, cy = sv / 2, P['dot_y']
    if P['dot_shape'] == 'round':
        e = Ell(cx, cy, d / 2, d / 2)
    else:
        e = Ell(cx, cy, d / 2, d / 2, k=P['dot_k'])
    from geom import from_curves
    c = [rect(0, 0, sv, xh), solid(from_curves(e.arc(0, 4)))]
    return glyph(c, P['lsb_stem'], sv, P['lsb_stem'])


def lc_o(P):
    W, xh, os_ = P['wo'], P['xh'], P['osx']
    rx, ry = W / 2, xh / 2 + os_
    eo = Ell(W / 2, xh / 2, rx, ry, k=P['ko'])
    ei = Ell(W / 2, xh / 2, rx - P['sv'] * 1.08, ry - P['sh'], k=P['ko'] + P['k_in'])
    return glyph(ring(eo, ei), P['lsb_round'], W, P['lsb_round'])


def _arch(P, W, xh, sv, sh, cyA):
    """Ellipses de l'épaule (n, r). Renvoie (eo, ei)."""
    os_ = P['osx']
    cxo = W * P['arch_cx']
    eo = Ell(cxo, cyA, W - cxo, xh + os_ - cyA, rxL=cxo, ryB=cyA, k=P['k_arch'])
    cxi = cxo - P['arch_shift']
    rxRi = (W - sv) - cxi
    ei = Ell(cxi, cyA, rxRi, xh + os_ - sh * P['arch_thin'] - cyA,
             rxL=cxi - sv * P['arch_crotch'], ryB=cyA, k=P['k_arch'] + P['k_in'])
    return eo, ei


def lc_n(P):
    W, xh, sv, sh = P['wn'], P['xh'], P['sv'], P['sh']
    cy = xh * P['arch_cy']
    eo, ei = _arch(P, W, xh, sv, sh, cy)
    c = [rect(0, 0, sv, xh), rect(W - sv, 0, W, cy + 2),
         band(eo, ei, H(cy), (W, cy), V(sv * 0.8), (sv, xh))]
    return glyph(c, P['lsb_stem'], W, P['lsb_stem'] * 0.94)


def lc_r(P):
    W, xh, sv, sh = P['wr_arch'], P['xh'], P['sv'], P['sh']
    cy = xh * P['arch_cy']
    Q = dict(P); Q['arch_cx'] = P.get('r_arch_cx', P['arch_cx'])
    eo, ei = _arch(Q, W, xh, sv * P.get('r_ear', 0.92), sh, cy)
    cut = P['r_term'](eo, ei)
    c = [rect(0, 0, sv, xh), band(eo, ei, cut, _mid(cut), V(sv * 0.8), (sv, xh))]
    return glyph(c, P['lsb_stem'], xmax(c), P['rsb_r'])


def lc_e(P):
    W, xh, os_, sv, sh = P['we'], P['xh'], P['osx'], P['sv'], P['sh']
    rx, ry = W / 2, xh / 2 + os_
    eo = Ell(W / 2, xh / 2, rx, ry, k=P['ko'])
    ei = Ell(W / 2, xh / 2, rx - sv * 1.06, ry - sh, k=P['ko'] + P['k_in'])
    yb = P['e_bar']; hb = sh * 0.9
    cut = P['e_term'](eo, ei)
    c = [band(eo, ei, H(yb), (W, yb), cut, _mid(cut)),
         rect(W / 2 - rx + sv * 0.5, yb, W - 1, yb + hb)]
    return glyph(c, P['lsb_round'], W, P['rsb_e'])


def lc_a(P):
    W, xh, os_, sv, sh = P['wa'], P['xh'], P['osx'], P['sv'], P['sh']
    # capuchon
    cyh = xh * P['a_hood_cy']
    xl = P['a_term_x']
    eo = Ell(W - P['a_hood_rx'], cyh, P['a_hood_rx'], xh + os_ - cyh,
             rxL=W - P['a_hood_rx'] - xl, ryB=cyh, k=P['ko'])
    ei = Ell(W - P['a_hood_rx'], cyh, P['a_hood_rx'] - sv,
             xh + os_ - sh * 0.96 - cyh, rxL=W - P['a_hood_rx'] - xl - sv * 0.9,
             ryB=cyh - 10, k=P['ko'] + P['k_in'])
    cut = P['a_term'](eo, ei)
    hood = band(eo, ei, H(cyh), (W, cyh), cut, _mid(cut))
    # panse
    bt = P['a_bowl_top']
    cyb = bt * 0.47
    bo = Ell(W - P['a_bowl_rx'], cyb, P['a_bowl_rx'], bt - cyb,
             rxL=W - P['a_bowl_rx'], ryB=cyb + os_, k=P['ka_bowl'])
    bi = Ell(W - P['a_bowl_rx'] + 6, cyb + (sh * 0.98 - sh * 0.9) / 2,
             P['a_bowl_rx'] - sv * 0.6, bt - cyb - sh * 0.9,
             rxL=W - P['a_bowl_rx'] - sv * 1.02, ryB=cyb + os_ - sh * 0.98,
             k=P['ka_bowl'] + P['k_in'])
    bowl = band(bo, bi, V(W - sv * 0.78), (W, bt), V(W - sv * 0.78), (W, 0))
    c = [rect(W - sv, 0, W, cyh + 2), hood, bowl]
    if P.get('a_spur'):
        c.append(rect(W - 2, 0, W + P['a_spur'], sh * 0.7))
    return glyph(c, P['lsb_round'], W + P.get('a_spur', 0), P['lsb_stem'] * 0.9)


def lc_k(P):
    W, asc, xh, sv = P['wk'], P['asc'], P['xh'], P['sv']
    c = [rect(0, 0, sv, asc)]
    c += _k_branches(P, W, xh, sv, P['k_join'], P['k_arm_w'], P['k_leg_w'],
                     P['k_mode'], P['k_legfrom'])
    return glyph(c, P['lsb_stem'], W, P['lsb_diag'])


GLYPHS = {
    'A': cap_A, 'R': cap_R, 'K': cap_K, 'E': cap_E, 'I': cap_I, 'O': cap_O, 'N': cap_N,
    'a': lc_a, 'r': lc_r, 'k': lc_k, 'e': lc_e, 'i': lc_i, 'o': lc_o, 'n': lc_n,
}
