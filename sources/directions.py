"""Les trois directions de l'étude Arkerion Sans (graisse Regular)."""
from geom import H, V

BASE = dict(
    cap=700, asc=735, desc=-205, os=12, osx=10,
    SV=88, SH=76, sv=82, sh=70, k_in=0.02,
    sb_stem=82, sb_round=46, sb_diag=12, sb_open=36,
    lsb_stem=66, lsb_round=42, lsb_diag=10, rsb_e=40, rsb_r=10,
    # A
    A_bar=200, A_apex_dy=(0, 0),
    # E
    E_mid=314,
    # N
    N_stem=0.9, N_notch=0,
    # R
    R_join=312, R_hbar=72, kR=0.58,
    # K
    K_join=250, K_arm_w=86, K_leg_w=96,
    # n / r
    arch_cx=0.53, arch_cy=0.53, arch_shift=4, arch_thin=0.92, arch_crotch=0.52, k_arch=0.58,
    # k
    k_join=180, k_arm_w=80, k_leg_w=90,
    # a
    a_hood_cy_f=0.52, a_bowl_top_f=0.58,
)


def mk(**kw):
    P = dict(BASE); P.update(kw)
    xh = P['xh']
    P.setdefault('a_hood_cy', P['a_hood_cy_f'])
    P.setdefault('a_bowl_top', xh * P['a_bowl_top_f'])
    P.setdefault('dot_y', xh + 136)
    P.setdefault('e_bar', xh * 0.46)
    return P


# ------------------------------------------------------------------ fonctions
def leg_from_stem(P):
    ym = P['R_join'] + P['R_hbar'] / 2
    return (P['SV'] + 34, ym), (P['wR'] - P['R_legw'] * 0.58, 0)


def leg_from_bowl(f):
    def _f(P):
        ym = P['R_join'] + P['R_hbar'] / 2
        x = P['R_bx'] + (P['R_bowl'] - P['R_bx']) * f
        return (x, ym), (P['wR'] - P['R_legw'] * 0.6, 0)
    return _f


def legcut_bar(P):
    return H(P['R_join'] + P['R_hbar'] * 0.55)


def term_angle(phi, ang=None):
    """Coupe de terminaison : droite passant par le milieu du trait à l'angle
    polaire phi (°) de la courbe, inclinée de ang° (None = perpendiculaire)."""
    import math
    def _f(eo, ei):
        c = eo.segs[0][0][0] - (eo.segs[0][0][0] - eo.segs[1][0][0]), eo.segs[0][0][1]
        cx, cy = eo.segs[1][0][0], eo.segs[0][0][1]
        ux, uy = math.cos(math.radians(phi)), math.sin(math.radians(phi))
        ray = ((cx, cy), (cx + ux, cy + uy))
        far = (cx + ux * 2000, cy + uy * 2000)
        po = eo.at(eo.cross(ray, far)); pi = ei.at(ei.cross(ray, far))
        m = ((po[0] + pi[0]) / 2, (po[1] + pi[1]) / 2)
        a = math.radians(phi if ang is None else ang)
        dx, dy = math.cos(a), math.sin(a)
        return ((m[0] - dx * 600, m[1] - dy * 600), (m[0] + dx * 600, m[1] + dy * 600))
    return _f


# ------------------------------------------------------------- Direction 1 --
# « Atelier » — humaniste : proportions classiques, ouvertures larges,
# terminaisons obliques, courbes plus souples.
D1 = mk(
    name='Atelier', xh=500, sv=80, sh=66,
    wA=650, A_apex=34, A_apex_dy=(8, 8), A_thin=80, A_thick=104, A_bar=196,
    E_arms=(448, 410, 470),
    wN=590, N_diag=118,
    wO=736, kO=0.555,
    wR=560, R_bowl=520, R_bx=290, R_legw=92, R_leg=leg_from_stem, R_legcut=legcut_bar,
    wK=570, K_mode='stem', K_legfrom=0.0,
    wo=476, ko=0.56,
    wn=392, arch_cx=0.50, k_arch=0.56, arch_crotch=0.50,
    wr_arch=330, r_arch_cx=0.56, r_term=term_angle(50, 58),
    we=448, e_term=term_angle(-36, -52), e_bar=232,
    wa=410, a_hood_rx=196, a_term_x=34, a_term=term_angle(150, 115),
    a_bowl_rx=214, ka_bowl=0.56,
    wk=392, k_mode='stem', k_legfrom=0.0,
    dot=96, dot_shape='round',
)

# ------------------------------------------------------------- Direction 2 --
# « Grotesk » — néo-grotesque rigoureux : largeurs régulières, ouvertures
# plus fermées, terminaisons horizontales, courbes super-elliptiques.
D2 = mk(
    name='Grotesk', xh=536, sh=72,
    wA=672, A_apex=84, A_thin=96, A_thick=104, A_bar=192,
    E_arms=(500, 470, 500),
    wN=612, N_diag=124,
    wO=720, kO=0.60,
    wR=590, R_bowl=550, R_bx=310, R_legw=96, R_leg=leg_from_bowl(0.42), R_legcut=legcut_bar,
    wK=598, K_mode='arm', K_legfrom=0.30,
    wo=488, ko=0.605,
    wn=420, arch_cx=0.55, k_arch=0.60,
    wr_arch=330, r_arch_cx=0.56, r_term=term_angle(34, 14),
    we=476, e_term=term_angle(-30, -18), e_bar=250,
    wa=432, a_hood_rx=210, a_term_x=26, a_term=term_angle(148, 18),
    a_bowl_rx=224, ka_bowl=0.60,
    wk=408, k_mode='arm', k_legfrom=0.30,
    dot=92, dot_shape='square', dot_k=0.80,
)

# ------------------------------------------------------------- Direction 3 --
# « Signature » — squelette néo-grotesque, détails humanistes et quelques
# traits propriétaires : A à sommet biseauté, R à jambe évasée issue de la
# panse, k à jambe greffée sur le bras, r/e/a à coupes verticales.
D3 = mk(
    name='Signature', xh=520,
    wA=664, A_apex=66, A_apex_dy=(-4, 12), A_thin=74, A_thick=110, A_bar=186,
    E_arms=(468, 430, 484),
    wN=600, N_diag=122,
    wO=728, kO=0.58,
    wR=574, R_bowl=530, R_bx=300, R_legw=86, R_flare=1.16,
    R_leg=leg_from_bowl(0.10), R_legcut=legcut_bar,
    wK=586, K_mode='arm', K_legfrom=0.46,
    wo=482, ko=0.585,
    wn=404, arch_cx=0.54, k_arch=0.59,
    wr_arch=336, r_arch_cx=0.56, r_term=term_angle(52),
    we=462, e_term=term_angle(-58, 90), e_bar=246,
    wa=420, a_hood_rx=204, a_term_x=30, a_term=term_angle(118, 90),
    a_bowl_rx=218, ka_bowl=0.585,
    wk=400, k_mode='arm', k_legfrom=0.50,
    dot=104, dot_shape='round',
)

DIRECTIONS = [D1, D2, D3]
