"""Arkerion Sans v0.5 — c et ç élargis (validé : variante « C2 », +55).

Pourquoi : le c (et donc le ç) paraissait resserré à côté du o élargi en v0.3.
Le c garde sa moitié gauche et ses deux terminaisons ; tous les points situés
à droite de son axe (x = 249, où se trouvent ses extremums haut et bas)
glissent de 55 unités. Les tangentes horizontales en haut et en bas sont
conservées, les épaisseurs ne changent pas. La cédille du ç est recentrée
(décalage de la moitié de l'élargissement).

Usage : python3 retouches_v0_5.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

AXIS = 249
WIDEN = 55


def contours(glyph):
    rec = RecordingPen(); glyph.draw(rec)
    out, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op == 'closePath':
            out.append(cur); cur = []
    return out


def widen(c, d):
    return [(op, [(p[0] + d if p[0] > AXIS else p[0], p[1]) for p in a]) for op, a in c]


def shift(c, d):
    return [(op, [(p[0] + d, p[1]) for p in a]) for op, a in c]


def put(f, name, conts, adv):
    cs = f['CFF '].cff.topDictIndex[0].CharStrings
    pen = T2CharStringPen(adv, None)
    for c in conts:
        for op, a in c:
            if op == 'closePath':
                pen.closePath()
            else:
                getattr(pen, op)(*[(round(x), round(y)) for x, y in a])
    cs[name] = pen.getCharString(private=cs[name].private, globalSubrs=cs[name].globalSubrs)
    f['hmtx'][name] = (adv, f['hmtx'][name][1])


def main(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet()
    c = contours(gs['c'])
    cedilla = [x for x in contours(gs['ccedilla']) if x not in c]
    adv = f['hmtx']['c'][0] + WIDEN
    new_c = [widen(x, WIDEN) for x in c]
    put(f, 'c', new_c, adv)
    put(f, 'ccedilla', new_c + [shift(x, WIDEN / 2) for x in cedilla], adv)

    f['head'].fontRevision = 0.5
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.500; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.400', '0.500')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
