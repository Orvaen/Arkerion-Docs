"""Compile les trois propositions de l'étude n°2 en OTF (CFF) avec crénage."""
import os, json, base64
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from build import draw
from directions2 import PROPOSALS, build

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out2')
os.makedirs(OUT, exist_ok=True)
CH = 'ARKEIONarkeion'

def compile_font(P, i):
    G, K = build(P)
    fam = 'Arkerion Study %s' % P['name'].replace('é', 'e')
    order = ['.notdef', 'space'] + list(CH)
    fb = FontBuilder(1000, isTTF=False)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({0x20: 'space', **{ord(c): c for c in CH}})
    cs, met = {}, {}
    pen = T2CharStringPen(500, None)
    for p in [(60, 0), (440, 0), (440, 700), (60, 700)]:
        (pen.moveTo if p == (60, 0) else pen.lineTo)(p)
    pen.closePath(); cs['.notdef'] = pen.getCharString(); met['.notdef'] = (500, 60)
    sp = round(G['n']['adv'] * 0.5)
    cs['space'] = T2CharStringPen(sp, None).getCharString(); met['space'] = (sp, 0)
    for c in CH:
        pen = T2CharStringPen(G[c]['adv'], None); draw(pen, G[c]['c'])
        cs[c] = pen.getCharString(); met[c] = (G[c]['adv'], G[c]['sb'][0])
    ps = fam.replace(' ', '') + '-Regular'
    fb.setupCFF(ps, {'FullName': fam + ' Regular'}, cs, {})
    fb.setupHorizontalMetrics(met)
    fb.setupHorizontalHeader(ascent=940, descent=-260)
    fb.setupNameTable({'familyName': fam, 'styleName': 'Regular', 'uniqueFontIdentifier': ps,
                       'psName': ps, 'version': 'Version 0.200; étude'})
    fb.setupOS2(sTypoAscender=P['asc'] + 60, sTypoDescender=P['desc'] - 40, sTypoLineGap=200,
                usWinAscent=940, usWinDescent=260, sxHeight=P['xh'], sCapHeight=P['cap'],
                achVendID='ARKR', fsSelection=0x40 | 0x80, version=4)
    fb.setupPost()
    if K:
        fea = 'feature kern {\n' + ''.join('  pos %s %s %d;\n' % (p[0], p[1], v) for p, v in K.items()) + '} kern;\n'
        addOpenTypeFeaturesFromString(fb.font, fea)
    path = os.path.join(OUT, 'ArkerionStudy2-%d-%s.otf' % (i + 1, P['name'].replace('é', 'e')))
    fb.save(path)
    return path, G, K

if __name__ == '__main__':
    meta = []
    for i, P in enumerate(PROPOSALS):
        path, G, K = compile_font(P, i)
        meta.append({'name': P['name'], 'file': os.path.basename(path), 'kern': K,
                     'b64': base64.b64encode(open(path, 'rb').read()).decode(),
                     'xh': P['xh'], 'SV': P['SV'], 'sv': P['sv'], 'SH': P['SH'], 'sh': P['sh'],
                     'adv': {c: G[c]['adv'] for c in CH}})
        print(path, os.path.getsize(path), K)
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'))
