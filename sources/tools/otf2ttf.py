"""Convertit un OTF (CFF) en TTF et marque chaque glyphe OVERLAP_SIMPLE :
les contours qui se chevauchent sont alors rendus sans liserés par les
moteurs de rendu (macOS notamment), en attendant la fusion des contours."""
import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen


def convert(src, dst):
    f = TTFont(src)
    gs = f.getGlyphSet(); order = f.getGlyphOrder()
    glyf = newTable('glyf'); glyf.glyphOrder = order; glyf.glyphs = {}
    for name in order:
        pen = TTGlyphPen(gs)
        gs[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        g = pen.glyph()
        if g.numberOfContours > 0:
            g.flags[0] |= 0x40  # OVERLAP_SIMPLE
        glyf.glyphs[name] = g
    del f['CFF ']
    if 'VORG' in f: del f['VORG']
    f['glyf'] = glyf; f['loca'] = newTable('loca')
    f['maxp'] = newTable('maxp'); m = f['maxp']
    m.tableVersion = 0x00010000
    for k in ('maxZones', 'maxTwilightPoints', 'maxStorage', 'maxFunctionDefs', 'maxInstructionDefs',
              'maxStackElements', 'maxSizeOfInstructions', 'maxComponentElements', 'maxComponentDepth',
              'maxPoints', 'maxContours', 'maxCompositePoints', 'maxCompositeContours'):
        setattr(m, k, 0)
    m.maxZones = 1
    f['head'].glyphDataFormat = 0
    f['post'].formatType = 2.0; f['post'].extraNames = []; f['post'].mapping = {}
    f['post'].glyphOrder = order
    f.sfntVersion = '\x00\x01\x00\x00'
    f.save(dst)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        convert(p, p[:-4] + '.ttf'); print(p[:-4] + '.ttf')
