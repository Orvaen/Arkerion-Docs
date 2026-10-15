"""Arkerion Mono — esquisse : déclinaison à chasse fixe (600/1000) de la
proposition « Code », avec les formes de lisibilité propres au code :
i/l/I/1 différenciés par des empattements, zéro pointé, ponctuation plus
grande, hauteur d'x généreuse."""
import os, json, base64
from geom import rect, translate, flatten
from geom import Ell, ring, solid, poly, H
from glyphs3 import GLYPHS as G3, xform, vee, hw, ells, dot, KIND, stroke, perp
from pens import pen, joint
from glyphs2 import arch, band, V
from directions2 import P2

CELL = 600

PM = dict(P2)
# v2 : rondes à flancs plus droits (remplissent la cellule), contraste réduit,
# graisse plus franche, largeurs homogènes, centrage optique.
PM.update(name='Mono', xh=548, asc=730, sv=84, sh=76, SV=86, SH=78, dot=118, dot_y=548 + 140,
          kO=0.64, ko=0.64, ka=0.63, kR=0.64, k_arch=0.64, k_in=0.02, rs=1.03, rt=0.98,
          arch_cy=0.56, arch_thin=0.96, arch_crotch=0.46,
          wA=540, A_apex=70, A_bar=200, wN=480, wO=500,
          R_bw=472, R_bx=268, R_leg_to=486, R_ym=318, R_leg_from=0.55,
          K_arm_x=470, K_leg_x=488, K_join=262,
          E_arms=(436, 408, 446), E_mid=316,
          wn=456, wo=482, we=478, wa=462, a_hood_rx=222, a_bowl_rx=238, a_bowl_top=312, a_hood_l=30,
          wr=436, r_cx=0.5, r_cy=0.6, r_term=(32, 14), e_term=(-30, -14), a_term=(152, 14),
          k_arm_x=436, k_leg_x=456, k_join=200)
# v3 : plus de fluidité — épaules qui naissent du fût en douceur, léger
# contraste, rondes moins tendues, terminaisons qui suivent le trait,
# queues courbes sur i, l, y au lieu d'empattements plats.
PM.update(sh=70, SH=74, kO=0.6, ko=0.6, ka=0.6, kR=0.6, k_arch=0.58, k_in=0.025,
          arch_cx=0.58, arch_cy=0.5, arch_crotch=0.32, arch_shift=10, arch_thin=0.94,
          r_cx=0.56, r_cy=0.56, r_term=(40, None), e_term=(-36, None), a_term=(146, None),
          K_taper=0.8)
# v4 : plus léger et moins haut (retour client : trop épais, trop haut).
PM.update(sv=72, sh=62, SV=74, SH=66, xh=526, dot=104, dot_y=526 + 140, asc=720,
          a_bowl_top=300, k_join=190)
# v5 : proportions d'une police de code éprouvée (mesurées, pas de contours
# repris) : lettres plus étroites dans la cellule et approches plus larges,
# graisse plus franche mais contraste quasi nul, capitales et hauteur d'x plus
# grandes, ponctuation nettement plus grosse.
PM.update(cap=730, xh=550, asc=730, desc=-180, os=12, osx=10,
          sv=88, sh=80, SV=88, SH=80, dot=142, dot_y=550 + 128,
          wo=432, wn=414, we=428, wa=414, a_hood_rx=198, a_bowl_rx=212, a_bowl_top=314, a_hood_l=26,
          wr=392, k_arm_x=380, k_leg_x=398, k_join=200,
          wO=444, wA=480, A_apex=64, A_bar=210, wN=420, E_arms=(386, 362, 392), E_mid=332,
          R_bw=424, R_bx=236, R_leg_to=436, R_ym=330, K_arm_x=414, K_leg_x=430, K_join=276)


# ------------------------------------------------------- formes propres au code
def tail(P, cx, y0):
    """Queue courbe vers la droite au pied d'un fût (i, l)."""
    sv, sh = P['sv'], P['sh']
    seg = [joint((cx, y0 + 30), (0, -1), (cx + 200, sh / 2 + 2), (1, 0.06), 0.66)]
    return pen(seg, sv, sh * 0.98, cut1=82)


def m_i(P):
    sv, sh, xh = P['sv'], P['sh'], P['xh']
    x = 0
    return [rect(x, 150, x + sv, xh), rect(x - 132, xh - sh, x + sv, xh),
            tail(P, x + sv / 2, 160), dot(x + sv / 2 - 10, P['dot_y'], P['dot'])]


def m_l(P):
    sv, sh = P['sv'], P['sh']
    return [rect(0, 150, sv, P['asc']), rect(-140, P['asc'] - sh, sv, P['asc']),
            tail(P, sv / 2, 160)]


def m_y(P):
    sv, xh, d = P['sv'], P['xh'], P['desc']
    W = 440
    tr = hw(sv, (W, xh), (W * 0.5, 0))
    right = stroke((W - tr / 2, xh), (W * 0.5, -10), sv * 0.96, H(xh), H(-60))
    left = stroke((hw(sv, (0, xh), (W * 0.47, 0)) / 2, xh), (W * 0.47, 0), sv * 0.86, H(xh), H(0))
    hook = pen([joint((W * 0.5 + 18, -40), (-0.45, -1), (W * 0.12, d + P['sh'] / 2 + 6), (-1, 0), 0.55)],
               sv * 0.96, P['sh'], cut1=95)
    return [right, left, hook]


def m_j(P):
    c = G3['j'](P)
    sv, sh, xh = P['sv'], P['sh'], P['xh']
    return c + [rect(-170, xh - sh, sv, xh)]


def m_I(P):
    SV, SH, cap = P['SV'], P['SH'], P['cap']
    return [rect(0, 0, SV, cap), rect(-170, cap - SH, SV + 170, cap), rect(-170, 0, SV + 170, SH)]


def m_1(P):
    SV, SH, cap = P['SV'], P['SH'], P['cap']
    p, q = (SV * 0.3, cap - SH * 0.3), (-170, cap - 150)
    return [rect(0, 0, SV, cap), stroke(p, q, SH, perp(p, q, p), perp(p, q, q)),
            rect(-170, 0, SV + 170, SH)]


def m_0(P):
    c = G3['0'](P)
    xs = [x for cc in c for x, _ in flatten(cc)]
    cx = (min(xs) + max(xs)) / 2
    e = Ell(cx, P['cap'] / 2, 44, 74)
    from geom import from_curves
    return c + [solid(from_curves(e.arc(0, 4)))]


def m_m(P):
    Q = dict(P); Q['sv'] = P['sv'] * 0.8; Q['wn'] = (478 + Q['sv'] * P['rs']) / 2 / 0.80
    return G3['m'](Q)


def m_w(P):
    t = P['sv'] * 0.86
    W1 = 272
    a = vee(W1, P['xh'], t * 0.5, t, 0.9, 0.96)
    Ww = 2 * W1 - hw(t * 0.96, (0, P['xh']), (W1 / 2, 0))
    return [a] + translate([a], Ww - W1)


def m_W(P):
    t = P['SV'] * 0.84
    W1 = 282
    a = vee(W1, P['cap'], t * 0.4, t, 0.9, 0.96)
    Ww = 2 * W1 - hw(t * 0.96, (0, P['cap']), (W1 / 2, 0))
    return [a] + translate([a], Ww - W1)


def m_M(P):
    cap, SV = P['cap'], P['SV']
    W = 472; sv = SV * 0.86; yv = cap * 0.30
    hd = hw(SV * 0.8, (0, cap), (W / 2, yv))
    return [rect(0, 0, sv, cap), rect(W - sv, 0, W, cap),
            solid(poly([(0, cap), (hd, cap), (W / 2 + hd / 2, yv), (W / 2 - hd / 2, yv)])),
            solid(poly([(W - hd, cap), (W, cap), (W / 2 + hd / 2, yv), (W / 2 - hd / 2, yv)]))]


def big_punct(fn, k=1.18):
    def f(P):
        Q = dict(P); Q['dot'] = P['dot'] * k
        return fn(Q)
    return f


GLYPHS = dict(G3)
GLYPHS.update({'y': m_y, 'i': m_i, 'l': m_l, 'j': m_j, 'I': m_I, '1': m_1, '0': m_0,
               'm': m_m, 'w': m_w, 'W': m_W, 'M': m_M,
               '.': big_punct(G3['.']), ',': big_punct(G3[',']), ':': big_punct(G3[':']),
               ';': big_punct(G3[';'])})


def fit(contours, maxw=552, kind='punct'):
    xs = [x for c in contours for x, _ in flatten(c)]
    x0, x1 = min(xs), max(xs)
    w = x1 - x0
    s = min(1.0, maxw / w)
    if kind == 'punct' or s < 1:
        cx = (x0 + x1) / 2
        return xform(contours, lambda p: ((p[0] - cx) * s + CELL / 2, p[1])), round(w), s
    # centrage optique : on répartit le blanc selon les approches calculées
    from spacing import profile, solve
    top = PM['xh'] if kind == 'lc' else PM['cap']
    rows = profile(contours, 0, top); ink = [r for r in rows if r]
    zx0 = min(r[0] for r in ink); zx1 = max(r[1] for r in ink)
    D = 80
    l = max(solve([(r[0] - zx0) if r else D for r in rows], 60, D), 6)
    r_ = max(solve([(zx1 - r[1]) if r else D for r in rows], 60, D), 6)
    free = CELL - (zx1 - zx0)
    lsb = free * l / (l + r_)
    return translate(contours, lsb - zx0), round(w), 1.0


if __name__ == '__main__':
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.t2CharStringPen import T2CharStringPen
    from build import draw
    from build3 import gname
    out = {}
    squeezed = []
    for ch, f in GLYPHS.items():
        if ch == 'j':
            c0 = f(PM); c = translate(c0, CELL * 0.57 - PM['sv'] / 2); w, s = 0, 1.0
        else:
            c, w, s = fit(f(PM), kind=KIND.get(ch, 'punct'))
        if s < 0.999:
            squeezed.append((ch, w, round(s, 2)))
        out[ch] = c
    print('ajustés à la cellule :', squeezed)
    names = {c: gname(c) for c in out}
    import ligs as LG
    LIGS = LG.build(PM)
    fb = FontBuilder(1000, isTTF=False)
    fb.setupGlyphOrder(['.notdef', 'space'] + [names[c] for c in out] + [k + '.code' for k in LIGS])
    cmap = {0x20: 'space', 0xA0: 'space'}; cmap.update({ord(c): names[c] for c in out})
    fb.setupCharacterMap(cmap)
    cs, met = {}, {}
    pen = T2CharStringPen(CELL, None)
    pen.moveTo((80, 0)); pen.lineTo((520, 0)); pen.lineTo((520, 700)); pen.lineTo((80, 700)); pen.closePath()
    cs['.notdef'] = pen.getCharString(); met['.notdef'] = (CELL, 80)
    cs['space'] = T2CharStringPen(CELL, None).getCharString(); met['space'] = (CELL, 0)
    for ch, c in out.items():
        pen = T2CharStringPen(CELL, None); draw(pen, c)
        cs[names[ch]] = pen.getCharString()
        met[names[ch]] = (CELL, round(min(x for cc in c for x, _ in flatten(cc))))
    for k, (c, n, _) in LIGS.items():
        pen = T2CharStringPen(CELL * n, None); draw(pen, c)
        cs[k + '.code'] = pen.getCharString()
        met[k + '.code'] = (CELL * n, round(min(x for cc in c for x, _ in flatten(cc))))
    fam = 'Arkerion Study Mono'
    fb.setupCFF('ArkerionStudyMono-Regular', {'FullName': fam + ' Regular', 'isFixedPitch': True}, cs, {})
    fb.setupHorizontalMetrics(met)
    fb.setupHorizontalHeader(ascent=940, descent=-260)
    fb.setupNameTable({'familyName': fam, 'styleName': 'Regular', 'psName': 'ArkerionStudyMono-Regular',
                       'uniqueFontIdentifier': 'ArkerionStudyMono-0.1', 'version': 'Version 0.100'})
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-240, sTypoLineGap=200, usWinAscent=940, usWinDescent=260,
                sxHeight=PM['xh'], sCapHeight=PM['cap'], achVendID='ARKR', fsSelection=0x40 | 0x80, version=4)
    fb.font['OS/2'].panose.bFamilyType = 2; fb.font['OS/2'].panose.bProportion = 9
    fb.setupPost(isFixedPitch=1)
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    addOpenTypeFeaturesFromString(fb.font, LG.fea(LIGS))
    os.makedirs('out3', exist_ok=True)
    fb.save('out3/ArkerionStudyMono-Regular.otf')
    json.dump({'b64': base64.b64encode(open('out3/ArkerionStudyMono-Regular.otf', 'rb').read()).decode()},
              open('out3/mono.json', 'w'))
    print('ok', len(out))
