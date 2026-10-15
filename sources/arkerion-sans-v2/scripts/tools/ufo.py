"""Lecture / écriture UFO 3 avec fontTools.ufoLib (sans dépendance externe)."""
import os, shutil
from fontTools.ufoLib import UFOWriter
from fontTools.pens.pointPen import SegmentToPointPen


class G:
    def __init__(self, width, unicodes):
        self.width = width; self.unicodes = unicodes


def write_ufo(path, info, glyphs, kerning=None, features=None, lib=None):
    """glyphs : liste de (nom, chasse, [unicodes], draw(segmentPen))."""
    if os.path.exists(path):
        shutil.rmtree(path)
    w = UFOWriter(path, formatVersion=3)
    class Info: pass
    i = Info()
    for k, v in info.items():
        setattr(i, k, v)
    w.writeInfo(i)
    gs = w.getGlyphSet()
    for name, width, unis, draw in glyphs:
        gs.writeGlyph(name, G(width, unis), lambda pp, d=draw: d(SegmentToPointPen(pp)))
    gs.writeContents()
    w.writeLayerContents()
    if kerning:
        w.writeKerning(kerning)
    if features:
        w.writeFeatures(features)
    w.writeLib(lib or {'public.glyphOrder': [g[0] for g in glyphs]})
    w.close()


def otf_to_ufo(otf, path):
    from fontTools.ttLib import TTFont
    f = TTFont(otf); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    rev = {}
    for u, n in cmap.items():
        rev.setdefault(n, []).append(u)
    os2, head, hhea = f['OS/2'], f['head'], f['hhea']
    name = f['name']
    info = dict(familyName=str(name.getDebugName(1)), styleName=str(name.getDebugName(2)),
                unitsPerEm=head.unitsPerEm, ascender=os2.sTypoAscender, descender=os2.sTypoDescender,
                xHeight=getattr(os2, 'sxHeight', 0), capHeight=getattr(os2, 'sCapHeight', 0),
                versionMajor=1, versionMinor=0)
    glyphs = [(g, f['hmtx'][g][0], rev.get(g, []), (lambda pen, g=g: gs[g].draw(pen))) for g in f.getGlyphOrder()]
    kern = {}
    write_ufo(path, info, glyphs, kern)
    return len(glyphs)
