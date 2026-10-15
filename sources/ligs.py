"""Ligatures de code d'Arkerion Mono (esquisse). Chaque ligature occupe
exactement n cellules de 600 : la grille monospace est préservée."""
from geom import rect, stroke, H, V, translate
from glyphs3 import perp, mirror

CELL = 600
M = 70  # marge latérale dans les cellules


def _axis(P):
    return P['xh'] * 0.5 + 6


def chev(tip, y, h, L, t, right=True):
    """Chevron dont la pointe est en (tip, y), ouvert vers l'arrière."""
    s = -1 if right else 1
    a, b = (tip + s * L, y + h), (tip + s * L, y - h)
    cut = V(tip + s * t * 0.3)
    return [stroke(a, (tip, y), t, perp(a, (tip, y), a), cut),
            stroke(b, (tip, y), t, perp(b, (tip, y), b), cut)]


def bars(x0, x1, ys, h):
    return [rect(x0, y - h / 2, x1, y + h / 2) for y in ys]


def slash(cx, y, t):
    p, q = (cx - 110, y - 230), (cx + 110, y + 230)
    return stroke(p, q, t, perp(p, q, p), perp(p, q, q))


def build(P):
    y, sh, t = _axis(P), P['sh'], P['sv'] * 0.92
    h, L = 190, 250
    W2, W3 = 2 * CELL, 3 * CELL
    tip2 = W2 - M
    out = {}
    # ->  et  <-
    a = bars(M, tip2 - 30, [y], sh) + chev(tip2, y, h, L, t)
    out['arrow'] = (a, 2, ['hyphen', 'greater'])
    out['larrow'] = (mirror(a, W2), 2, ['less', 'hyphen'])
    # =>
    xe = tip2 - L * 100 / h + 24
    out['darrow'] = (bars(M, xe, [y - 100, y + 100], sh) + chev(tip2, y, h, L, t), 2, ['equal', 'greater'])
    # ==  ===  !=  !==
    out['eq2'] = (bars(M, W2 - M, [y - 100, y + 100], sh), 2, ['equal', 'equal'])
    out['eq3'] = (bars(M, W3 - M, [y - 135, y, y + 135], sh), 3, ['equal', 'equal', 'equal'])
    out['neq2'] = (out['eq2'][0] + [slash(CELL, y, t)], 2, ['exclam', 'equal'])
    out['neq3'] = (out['eq3'][0] + [slash(1.5 * CELL, y, t)], 3, ['exclam', 'equal', 'equal'])
    # <=  >=  (≤ ≥)
    cy, ch, x0, x1 = y + 80, 168, 210, W2 - 210
    le = chev(x0, cy, ch, x1 - x0, t, right=False) + bars(x0, x1, [y - 190], sh)
    out['le'] = (le, 2, ['less', 'equal'])
    out['ge'] = (mirror(le, W2), 2, ['greater', 'equal'])
    # <=>
    xe3 = L * 100 / h - 24
    sp = bars(M + xe3, W3 - M - xe3, [y - 100, y + 100], sh) + chev(M, y, h, L, t, right=False) + chev(W3 - M, y, h, L, t)
    out['spaceship'] = (sp, 3, ['less', 'equal', 'greater'])
    return out


FEA_ORDER = ['spaceship', 'neq3', 'eq3', 'neq2', 'eq2', 'darrow', 'arrow', 'larrow', 'le', 'ge']


def fea(ligs):
    lines = ['feature calt {']
    for k in FEA_ORDER:
        lines.append('  sub %s by %s.code;' % (' '.join(ligs[k][2]), k))
    lines.append('} calt;')
    return '\n'.join(lines) + '\n'
