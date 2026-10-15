"""Étude n°2 — trois propositions de marque pour Arkerion Sans (Regular)."""
from glyphs2 import GLYPHS, CAPS
from spacing import space, kern

BASE = dict(cap=700, asc=740, desc=-200, os=12, osx=10, k_in=0.025,
            arch_shift=4, arch_thin=0.94, arch_crotch=0.5, r_ear=0.95)


def mk(**kw):
    P = dict(BASE); P.update(kw)
    P.setdefault('dot_y', P['xh'] + 150)
    return P


# 1 — Clarté : rondes presque circulaires, proportions amples, terminaisons
# horizontales, contraste quasi nul, espacement généreux de marque.
P1 = mk(name='Clarté', xh=490, SV=84, SH=78, sv=80, sh=74, rs=1.05, rt=0.98,
        wA=676, A_apex=46, A_tl=0.88, A_tr=0.98, A_bar=200,
        E_arms=(452, 418, 462), E_mid=310,
        wN=612, N_stem=0.92, N_diag=1.04,
        wO=758, kO=0.553,
        R_bw=546, R_bx=328, R_ym=318, kR=0.56, R_leg_from=0.62, R_leg_to=600, R_leg_t=0.98,
        K_join=280, K_arm_x=566, K_leg_x=590, K_arm_t=0.92, K_leg_t=0.98, K_leg_from=0, K_taper=0.86,
        wo=502, ko=0.553,
        wn=414, arch_cx=0.50, arch_cy=0.50, k_arch=0.56,
        wr=320, r_cx=0.56, r_cy=0.62, r_term=(44, 4),
        we=474, e_bar=234, e_term=(-30, -4),
        wa=430, a_hood_cy=0.50, a_hood_rx=200, a_hood_l=30, a_term=(150, 176),
        a_bowl_top=272, a_bowl_rx=226, ka=0.56, a_bowl_top_t=0.9,
        k_join=170, k_arm_x=362, k_leg_x=392, k_arm_t=0.92, k_leg_t=0.98, k_leg_from=0,
        dot=98,
        sp_lc=64, sp_uc=80, depth=1.22)

# 2 — Code : grande hauteur d'x, courbes légèrement tendues, terminaisons
# inclinées, jambe du k issue du bras ; dessinée pour l'interface et le code.
P2 = mk(name='Code', xh=532, SV=86, SH=78, sv=82, sh=74, rs=1.04, rt=0.97,
        wA=652, A_apex=54, A_tl=0.88, A_tr=0.98, A_bar=196,
        E_arms=(482, 452, 488), E_mid=312,
        wN=604, N_stem=0.9, N_diag=1.05,
        wO=702, kO=0.59, k_in=0.03,
        R_bw=552, R_bx=318, R_ym=322, kR=0.6, R_leg_from=0.58, R_leg_to=590, R_leg_t=0.98,
        K_join=262, K_arm_x=562, K_leg_x=582, K_arm_t=0.92, K_leg_t=0.98, K_leg_from=0.34, K_taper=0.88,
        wo=494, ko=0.59,
        wn=420, arch_cx=0.54, arch_cy=0.54, k_arch=0.60,
        wr=312, r_cx=0.56, r_cy=0.64, r_term=(40, 20),
        we=480, e_bar=252, e_term=(-34, -20),
        wa=440, a_hood_cy=0.52, a_hood_rx=210, a_hood_l=24, a_term=(150, 20),
        a_bowl_top=302, a_bowl_rx=230, ka=0.59, a_bowl_top_t=0.9,
        k_join=192, k_arm_x=386, k_leg_x=402, k_arm_t=0.92, k_leg_t=0.98, k_leg_from=0.34,
        dot=96,
        sp_lc=58, sp_uc=70, depth=1.2)

# 3 — Nuance : humaniste contemporaine, léger contraste, proportions variées,
# coupes obliques perpendiculaires au trait, jonctions affinées.
P3 = mk(name='Nuance', xh=508, SV=86, SH=72, sv=82, sh=66, rs=1.08, rt=0.95,
        wA=642, A_apex=40, A_tl=0.84, A_tr=1.0, A_bar=190,
        E_arms=(432, 400, 452), E_mid=318,
        wN=600, N_stem=0.9, N_diag=1.04,
        wO=740, kO=0.565,
        R_bw=522, R_bx=300, R_ym=304, kR=0.57, R_leg_from=0.30, R_leg_to=582, R_leg_t=0.96,
        K_join=270, K_arm_x=542, K_leg_x=572, K_arm_t=0.9, K_leg_t=0.97, K_leg_from=0, K_taper=0.84,
        wo=488, ko=0.565,
        wn=402, arch_cx=0.50, arch_cy=0.52, k_arch=0.565, arch_thin=0.9,
        wr=310, r_cx=0.55, r_cy=0.62, r_term=(46, 26),
        we=462, e_bar=236, e_term=(-40, -58),
        wa=424, a_hood_cy=0.50, a_hood_rx=200, a_hood_l=30, a_term=(140, 150),
        a_bowl_top=282, a_bowl_rx=220, ka=0.565, a_bowl_top_t=0.88,
        k_join=176, k_arm_x=352, k_leg_x=382, k_arm_t=0.9, k_leg_t=0.97, k_leg_from=0,
        dot=100,
        sp_lc=62, sp_uc=76, depth=1.22)

PROPOSALS = [P1, P2, P3]
PAIRS = ['Ar', 'rk', 'ke', 'er', 'ri', 'io', 'on', 'AR', 'RK', 'KE', 'ER', 'RI', 'IO', 'ON']


def build(P):
    out = {}
    for ch, f in GLYPHS.items():
        uc = ch in CAPS
        tgt = P['sp_uc'] if uc else P['sp_lc']
        top = P['cap'] if uc else P['xh']
        cs, adv, sb = space(f(P), top, tgt, tgt * P['depth'], min_r=0.52 if ch == 'E' else 0.2)
        out[ch] = dict(c=cs, adv=adv, sb=sb)
    kp = {}
    for a, b in PAIRS:
        uc = a in CAPS and b in CAPS
        top = P['cap'] if uc else P['xh']
        D = (P['sp_uc'] if uc else P['sp_lc']) * P['depth']
        k = kern(out[a]['c'], out[a]['adv'], out[b]['c'], top, D)
        if k:
            kp[a + b] = k
    return out, kp


def compact(P, kr=0.9, kn=0.94, ks=0.78, kmin=0.575):
    """Retour client : rondes plus étroites et moins circulaires, approches resserrées."""
    for k in ('wO', 'wo', 'we', 'wa', 'a_hood_rx', 'a_bowl_rx'):
        P[k] = round(P[k] * kr)
    for k in ('wn', 'wr', 'wN', 'wA', 'K_arm_x', 'K_leg_x', 'k_arm_x', 'k_leg_x', 'R_leg_to'):
        P[k] = round(P[k] * kn)
    P['R_bw'] = round(P['R_bw'] * 0.95); P['R_bx'] = round(P['R_bx'] * 0.95)
    P['E_arms'] = tuple(round(a * 0.95) for a in P['E_arms'])
    for k in ('kO', 'ko', 'ka', 'kR'):
        P[k] = max(P[k], kmin)
    P['k_arch'] = max(P['k_arch'], kmin)
    P['sp_lc'] = round(P['sp_lc'] * ks); P['sp_uc'] = round(P['sp_uc'] * ks)
    return P


for _P in PROPOSALS:
    compact(_P)
