"""Arkerion Sans 0.12 — apostrophe : crénage avec le A, ajout du ’.

Pourquoi : depuis le nouveau A (v0.4), le côté gauche du A descend en biais
depuis un sommet placé au milieu de la lettre. À la hauteur de l'apostrophe,
il restait ~350 unités de vide entre ' et A, contre ~114 entre d et '.
« d'Arkerion » paraissait donc collé au d et décollé du A.

- Crénage ajouté (nouvelle sous-table de la fonction kern) entre ' ’ " et
  A / À : −140 pour les apostrophes, −125 pour le guillemet droit.
- Nouveau glyphe ’ (U+2019, apostrophe typographique) : la virgule de la
  police remontée à la hauteur des capitales. Avant, le navigateur le prenait
  dans une autre police.

Dans le fichier de police, la version est notée 0.930.

Usage : python3 retouches_v0_12.py ArkerionSans-Regular.otf sortie.otf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.otlLib.builder import buildPairPosGlyphsSubtable
from fontTools.ttLib.tables.otBase import ValueRecord

KERN = {('quotesingle', 'A'): -140, ('quotesingle', 'Agrave'): -140,
        ('quoteright', 'A'): -140, ('quoteright', 'Agrave'): -140,
        ('quotedbl', 'A'): -125, ('quotedbl', 'Agrave'): -125}


def add_quoteright(f):
    """’ = la virgule remontée : son haut aligné sur celui de l'apostrophe droite."""
    gs = f.getGlyphSet()
    td = f['CFF '].cff.topDictIndex[0]
    cs = td.CharStrings
    bc = BoundsPen(gs); gs['comma'].draw(bc)
    bq = BoundsPen(gs); gs['quotesingle'].draw(bq)
    dy = bq.bounds[3] - bc.bounds[3]
    adv = f['hmtx']['comma'][0]
    pen = T2CharStringPen(adv, None)
    gs['comma'].draw(TransformPen(pen, (1, 0, 0, 1, 0, dy)))
    proto = cs['comma']
    charstring = pen.getCharString(private=proto.private, globalSubrs=proto.globalSubrs)
    name = 'quoteright'
    if name not in cs:
        order = list(f.getGlyphOrder())
        cs.charStringsIndex.append(charstring)
        cs.charStrings[name] = len(cs.charStringsIndex) - 1
        if name not in td.charset:      # le charset CFF peut être la même liste que l'ordre des glyphes
            td.charset.append(name)
        f.setGlyphOrder(order + [name])
    else:
        cs[name] = charstring
    f['hmtx'][name] = (adv, f['hmtx']['comma'][1])
    for table in f['cmap'].tables:
        if table.isUnicode():
            table.cmap[0x2019] = name


def add_kerning(f):
    pairs = {}
    for (a, b), v in KERN.items():
        vr = ValueRecord(); vr.XAdvance = v
        pairs[(a, b)] = (vr, None)
    glyph_map = {g: i for i, g in enumerate(f.getGlyphOrder())}
    sub = buildPairPosGlyphsSubtable(pairs, glyph_map)
    lookup = f['GPOS'].table.LookupList.Lookup[0]
    lookup.SubTable.append(sub)
    lookup.SubTableCount = len(lookup.SubTable)


def main(src, dst):
    f = TTFont(src)
    add_quoteright(f)
    add_kerning(f)
    f['head'].fontRevision = 0.93
    for rec in f['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 0.930; étude'
        elif rec.nameID == 3:
            rec.string = str(rec).replace('0.920', '0.930')
    f.save(dst)


if __name__ == '__main__':
    main(*sys.argv[1:3])
