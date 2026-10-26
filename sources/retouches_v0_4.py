"""Arkerion Sans v0.4 — nouveau A à empattements (validé : variante « S3 »).

Pourquoi : le A de la v0.3 était parfaitement symétrique (jambes égales,
sommet plat), donc figé. Le nouveau A s'inspire de celui de Lora, avec des
contours dessinés pour Arkerion (aucun contour de Lora n'est repris) :

- sommet en pointe, en léger dépassement de la ligne des capitales ;
- jambe gauche fine, jambe droite appuyée ;
- barre basse et fine, qui monte légèrement vers la droite ;
- pieds à empattements, raccordés aux jambes par des congés courbes.

C'est le seul glyphe à empattements de la police : un trait de signature.
À suit (l'accent est recentré sur le nouveau sommet).

Usage : python3 retouches_v0_4.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen

# Paramètres du A « S3 » (moyenne des variantes S1 et S2)
P = dict(
    x0=56, x1=676,      # pieds des jambes, hors empattements
    xa=364, wa=11,      # centre et largeur du sommet
    ya=715,             # hauteur du sommet (dépassement de 15)
    tl=51, tr=111,      # chasse horizontale des jambes : gauche fine, droite appuyée
    yb=207, tb=56,      # barre : bas et épaisseur
    tilt=5.5,           # la barre monte de 5,5 unités vers la droite
    ext=43,             # débord des empattements
    sh=32,              # épaisseur des empattements
    fh=54,              # hauteur des congés
)
ADV = 736
SEAM = 8                # les congés mordent de 8 unités dans la jambe : pas de liseré


def area(p):
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(p, p[1:] + p[:1])) / 2


def shapes(x0, x1, xa, wa, ya, tl, tr, yb, tb, tilt, ext, sh, fh):
    aL, aR = xa - wa / 2, xa + wa / 2
    xLo = lambda y: x0 + (aL - x0) * y / ya
    xLi = lambda y: x0 + tl + (aL - x0) * y / ya
    xRo = lambda y: x1 + (aR - x1) * y / ya
    xRi = lambda y: x1 - tr + (aR - x1) * y / ya
    ybr = yb + tilt
    outer = [(x0, 0), (x0 + tl, 0), (xLi(yb), yb), (xRi(ybr), ybr),
             (x1 - tr, 0), (x1, 0), (aR, ya), (aL, ya)]
    # sommet de la contre-forme : intersection des deux bords intérieurs
    a1, b1 = x0 + tl, (aL - x0) / ya
    a2, b2 = x1 - tr, (aR - x1) / ya
    yi = (a2 - a1) / (b1 - b2); xi = a1 + b1 * yi
    yt = yb + tb
    counter = [(xLi(yt), yt), (xRi(yt + tilt), yt + tilt), (xi, yi)]
    out = [('poly', outer if area(outer) > 0 else outer[::-1]),          # plein : antihoraire
           ('poly', counter if area(counter) < 0 else counter[::-1])]    # creux : horaire
    for xa_, xb_ in [(x0 - ext * 1.1, x0 + tl + ext * 0.9), (x1 - tr - ext * 0.9, x1 + ext * 1.1)]:
        out.append(('poly', [(xa_, 0), (xb_, 0), (xb_, sh), (xa_, sh)]))

    def fillet(edge, side, xs):
        e = lambda y: edge(y) - side * SEAM
        E0, E1, Sp = (e(sh), sh), (e(sh + fh), sh + fh), (xs, sh)
        c1 = (E1[0] + (E0[0] - E1[0]) * 0.6, E1[1] + (E0[1] - E1[1]) * 0.6)
        c2 = (Sp[0] + (E0[0] - Sp[0]) * 0.6, sh)
        return ('fillet', (E0, E1, c1, c2, Sp))

    out += [fillet(xLo, -1, x0 - ext * 1.1 + ext * 0.25),
            fillet(xLi, 1, x0 + tl + ext * 0.9 - ext * 0.2),
            fillet(xRi, -1, x1 - tr - ext * 0.9 + ext * 0.2),
            fillet(xRo, 1, x1 + ext * 1.1 - ext * 0.25)]
    return out


def draw(pen, items):
    R = lambda p: (round(p[0]), round(p[1]))
    for kind, data in items:
        if kind == 'poly':
            pen.moveTo(R(data[0]))
            for p in data[1:]:
                pen.lineTo(R(p))
            pen.closePath()
        else:
            E0, E1, c1, c2, Sp = data
            if area([E0, E1, Sp]) > 0:
                pen.moveTo(R(E0)); pen.lineTo(R(E1)); pen.curveTo(R(c1), R(c2), R(Sp))
            else:
                pen.moveTo(R(E0)); pen.lineTo(R(Sp)); pen.curveTo(R(c2), R(c1), R(E1))
            pen.closePath()


def contours(glyph):
    rec = RecordingPen(); glyph.draw(rec)
    out, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op == 'closePath':
            out.append(cur); cur = []
    return out


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    old_A = contours(gs['A'])
    bp = BoundsPen(gs); gs['A'].draw(bp)
    old_center = (bp.bounds[0] + bp.bounds[2]) / 2
    accent = [c for c in contours(gs['Agrave']) if c not in old_A]
    dx = round(P['xa'] - old_center)
    items = shapes(**P)
    lsb = round(P['x0'] - P['ext'] * 1.1)
    for name, extra in (('A', []), ('Agrave', accent)):
        pen = T2CharStringPen(ADV, None)
        draw(pen, items)
        for c in extra:
            for op, args in c:
                if op == 'closePath':
                    pen.closePath()
                else:
                    getattr(pen, op)(*[(round(p[0] + dx), round(p[1])) for p in args])
        cs[name] = pen.getCharString(private=cs[name].private, globalSubrs=cs[name].globalSubrs)
        f['hmtx'][name] = (ADV, lsb)

    f['head'].fontRevision = 0.4
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.400; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.300', '0.400')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
