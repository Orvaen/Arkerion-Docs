"""Arkerion Sans v0.7 — e encore élargi (validé : variante « E1 », +25).

Le e (et é è ê ë) prend 25 unités de plus après la v0.6 : 591 unités de
chasse, exactement la largeur du o. Même méthode : la moitié droite s'écarte
(axe x = 317, le centre du e après la v0.6), terminaisons et épaisseurs
inchangées, accents recentrés.

Usage : python3 retouches_v0_7.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from retouches_v0_6 import contours, widen, shift, charstring, replay
from fontTools.ttLib import TTFont

AXIS, WIDEN = 317, 25
DERIVED = ['eacute', 'egrave', 'ecircumflex', 'edieresis']


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    base_c = contours(gs['e'])
    adv = f['hmtx']['e'][0] + WIDEN
    new = [widen(c, AXIS, WIDEN) for c in base_c]
    charstring(f, 'e', adv, replay(new))
    f['hmtx']['e'] = (adv, f['hmtx']['e'][1])
    for g in DERIVED:
        accent = [c for c in contours(gs[g]) if c not in base_c]
        charstring(f, g, adv, replay(new + [shift(c, WIDEN / 2) for c in accent]))
        f['hmtx'][g] = (adv, f['hmtx'][g][1])

    f['head'].fontRevision = 0.7
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.700; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.600', '0.700')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
