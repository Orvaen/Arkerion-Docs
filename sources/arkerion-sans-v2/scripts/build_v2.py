"""Construit Arkerion Sans v2 : espacement optique, crénage, OTF et UFO."""
import os, sys
sys.path.insert(0, '/home/claude/arkerion'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/tools')
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from spacing import space, kern
from geom import flatten
from glyphs_v2 import GLYPHS, M
from ufo import write_ufo

HERE = os.path.dirname(os.path.abspath(__file__))
CAPS = set('ARKEION')
SP_UC, SP_LC, DEPTH = 80, 64, 1.25
PAIRS = ['Ar', 'rk', 'ke', 'er', 'ri', 'io', 'on', 'AR', 'RK', 'KE', 'ER', 'RI', 'IO', 'ON',
         'Ak', 'An', 'Ae', 'Ao', 'ra', 're', 'ro', 'ka', 'ko', 'ek', 'no', 'oe', 'eo']


def draw(pen, contours):
    r = lambda p: (round(p[0]), round(p[1]))
    for p0, segs in contours:
        pen.moveTo(r(p0))
        for s in segs:
            if s[0] == 'L':
                pen.lineTo(r(s[1]))
            else:
                pen.curveTo(r(s[1]), r(s[2]), r(s[3]))
        pen.closePath()


def build():
    G = {}
    for ch, f in GLYPHS.items():
        uc = ch in CAPS
        tgt = SP_UC if uc else SP_LC
        top = M['cap'] if uc else M['xh']
        min_r = 0.5 if ch == 'E' else 0.25
        cs, adv, sb = space(f(), top, tgt, tgt * DEPTH, min_r=min_r)
        G[ch] = dict(c=cs, adv=adv, sb=sb)
    K = {}
    for a, b in PAIRS:
        if a not in G or b not in G:
            continue
        uc = a in CAPS and b in CAPS
        top = M['cap'] if uc else M['xh']
        D = (SP_UC if uc else SP_LC) * DEPTH
        k = kern(G[a]['c'], G[a]['adv'], G[b]['c'], top, D, kf=0.5)
        if k:
            K[(a, b)] = k
    return G, K


def compile_otf(G, K, path):
    order = ['.notdef', 'space'] + list(G)
    fb = FontBuilder(1000, isTTF=False)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({0x20: 'space', **{ord(c): c for c in G}})
    cs, met = {}, {}
    pen = T2CharStringPen(500, None)
    for i, p in enumerate([(60, 0), (440, 0), (440, 700), (60, 700)]):
        (pen.moveTo if i == 0 else pen.lineTo)(p)
    pen.closePath(); cs['.notdef'] = pen.getCharString(); met['.notdef'] = (500, 60)
    sp = round(G['n']['adv'] * 0.5)
    cs['space'] = T2CharStringPen(sp, None).getCharString(); met['space'] = (sp, 0)
    for c, g in G.items():
        pen = T2CharStringPen(g['adv'], None); draw(pen, g['c'])
        cs[c] = pen.getCharString()
        met[c] = (g['adv'], round(min(x for cc in g['c'] for x, _ in flatten(cc))))
    fam = 'Arkerion Sans v2'
    fb.setupCFF('ArkerionSansv2-Regular', {'FullName': fam + ' Regular', 'Weight': 'Regular'}, cs, {})
    fb.setupHorizontalMetrics(met)
    fb.setupHorizontalHeader(ascent=940, descent=-260)
    fb.setupNameTable({'familyName': fam, 'styleName': 'Regular', 'psName': 'ArkerionSansv2-Regular',
                       'uniqueFontIdentifier': 'ArkerionSansv2-Regular-2.0', 'version': 'Version 2.000; étude',
                       'copyright': '© Arkerion. Tous droits réservés.'})
    fb.setupOS2(sTypoAscender=M['asc'] + 65, sTypoDescender=M['desc'] - 40, sTypoLineGap=200,
                usWinAscent=940, usWinDescent=260, sxHeight=M['xh'], sCapHeight=M['cap'],
                achVendID='ARKR', fsSelection=0x40 | 0x80, version=4)
    fb.setupPost()
    fb.font['head'].fontRevision = 2.0
    fea = 'languagesystem DFLT dflt;\nlanguagesystem latn dflt;\nfeature kern {\n' + \
          ''.join('  pos %s %s %d;\n' % (a, b, v) for (a, b), v in sorted(K.items())) + '} kern;\n'
    addOpenTypeFeaturesFromString(fb.font, fea)
    fb.save(path)
    return fea


def write_sources(G, K, fea, path):
    info = dict(familyName='Arkerion Sans', styleName='Regular', unitsPerEm=1000,
                ascender=M['asc'], descender=M['desc'], xHeight=M['xh'], capHeight=M['cap'],
                versionMajor=2, versionMinor=0, copyright='© Arkerion. Tous droits réservés.',
                openTypeOS2VendorID='ARKR', postscriptStemSnapV=[M['sv'], M['SV']],
                postscriptStemSnapH=[M['sh'], M['SH']],
                postscriptBlueValues=[-M['os_cap'], 0, M['xh'], M['xh'] + M['os_lc'], M['cap'], M['cap'] + M['os_cap']])
    glyphs = [('space', round(G['n']['adv'] * 0.5), [0x20], lambda pen: None)]
    for c, g in G.items():
        glyphs.append((c, g['adv'], [ord(c)], (lambda pen, cs=g['c']: draw(pen, cs))))
    write_ufo(path, info, glyphs, dict(K), fea.replace('feature kern {', '# crénage : voir kerning.plist\n#feature kern {'))


if __name__ == '__main__':
    G, K = build()
    os.makedirs(HERE + '/build', exist_ok=True)
    fea = compile_otf(G, K, HERE + '/build/ArkerionSans-Regular-v2.otf')
    write_sources(G, K, fea, HERE + '/ufo/ArkerionSans-Regular-v2.ufo')
    print({c: (g['adv'], g['sb']) for c, g in G.items()})
    print('crénage', K)
