"""Étude n°3 : compile les 3 propositions avec le jeu ASCII d'esquisse."""
import os, json, base64
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.agl import UV2AGL
from build import draw
from geom import translate, flatten
from spacing import space, kern
from glyphs3 import GLYPHS, KIND
from directions2 import PROPOSALS, PAIRS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out3')
os.makedirs(OUT, exist_ok=True)


def gname(ch):
    return UV2AGL.get(ord(ch), 'uni%04X' % ord(ch))


TEXT_K = 1.45  # approches de texte : le logo resserre via l'interlettrage


def build_all(P):
    P = dict(P); P['sp_lc'] = P['sp_lc'] * TEXT_K; P['sp_uc'] = P['sp_uc'] * TEXT_K
    G = {}
    for ch, f in GLYPHS.items():
        kind = KIND[ch]
        c = f(P)
        if kind in ('lc', 'uc'):
            uc = kind == 'uc'
            tgt = P['sp_uc'] if uc else P['sp_lc']
            top = P['cap'] if uc else P['xh']
            minr = 0.52 if ch in 'EFL' else 0.2
            cs, adv, sb = space(c, top, tgt, tgt * P['depth'], min_r=minr)
        elif kind == 'fig':
            tgt = P['sp_uc'] * 0.9
            cs, adv, sb = space(c, P['cap'], tgt, tgt * P['depth'], min_r=0.3)
        else:
            xs = [x for cc in c for x, _ in flatten(cc)]
            s = P['sp_lc'] * (0.95 if ch in '.,:;!' else 0.75)
            cs = translate(c, s - min(xs)); adv = round(max(xs) - min(xs) + 2 * s); sb = (round(s), round(s))
        G[ch] = dict(c=cs, adv=adv, sb=sb)
    # chiffres tabulaires
    fw = max(G[d]['adv'] for d in '0123456789')
    for d in '0123456789':
        g = G[d]; dx = (fw - g['adv']) / 2
        g['c'] = translate(g['c'], dx); g['adv'] = fw
    K = {}
    for a, b in PAIRS:
        uc = KIND[a] == 'uc' and KIND[b] == 'uc'
        top = P['cap'] if uc else P['xh']
        Dd = (P['sp_uc'] if uc else P['sp_lc']) * P['depth']
        k = kern(G[a]['c'], G[a]['adv'], G[b]['c'], top, Dd)
        if k:
            K[(a, b)] = k
    return G, K


def compile_font(P, i):
    G, K = build_all(P)
    nm = P['name'].replace('é', 'e')
    fam = 'Arkerion Study %s' % nm
    chars = list(G)
    names = {c: gname(c) for c in chars}
    order = ['.notdef', 'space'] + [names[c] for c in chars]
    fb = FontBuilder(1000, isTTF=False)
    fb.setupGlyphOrder(order)
    cmap = {0x20: 'space', 0xA0: 'space'}
    cmap.update({ord(c): names[c] for c in chars})
    fb.setupCharacterMap(cmap)
    cs, met = {}, {}
    pen = T2CharStringPen(500, None)
    pen.moveTo((60, 0)); pen.lineTo((440, 0)); pen.lineTo((440, 700)); pen.lineTo((60, 700)); pen.closePath()
    cs['.notdef'] = pen.getCharString(); met['.notdef'] = (500, 60)
    sp = round(G['n']['adv'] * 0.48)
    cs['space'] = T2CharStringPen(sp, None).getCharString(); met['space'] = (sp, 0)
    for c in chars:
        pen = T2CharStringPen(G[c]['adv'], None); draw(pen, G[c]['c'])
        cs[names[c]] = pen.getCharString()
        xs = [x for cc in G[c]['c'] for x, _ in flatten(cc)]
        met[names[c]] = (G[c]['adv'], round(min(xs)))
    ps = fam.replace(' ', '') + '-Regular'
    fb.setupCFF(ps, {'FullName': fam + ' Regular'}, cs, {})
    fb.setupHorizontalMetrics(met)
    fb.setupHorizontalHeader(ascent=940, descent=-260)
    fb.setupNameTable({'familyName': fam, 'styleName': 'Regular', 'uniqueFontIdentifier': ps + '-0.3',
                       'psName': ps, 'version': 'Version 0.300'})
    fb.setupOS2(sTypoAscender=P['asc'] + 60, sTypoDescender=P['desc'] - 40, sTypoLineGap=200,
                usWinAscent=940, usWinDescent=260, sxHeight=P['xh'], sCapHeight=P['cap'],
                achVendID='ARKR', fsSelection=0x40 | 0x80, version=4)
    fb.setupPost()
    if K:
        fea = 'feature kern {\n' + ''.join('  pos %s %s %d;\n' % (names[a], names[b], v) for (a, b), v in K.items()) + '} kern;\n'
        addOpenTypeFeaturesFromString(fb.font, fea)
    path = os.path.join(OUT, 'ArkerionStudy3-%d-%s.otf' % (i + 1, nm))
    fb.save(path)
    return path, G, K


if __name__ == '__main__':
    meta = []
    for i, P in enumerate(PROPOSALS):
        path, G, K = compile_font(P, i)
        meta.append({'name': P['name'], 'b64': base64.b64encode(open(path, 'rb').read()).decode()})
        print(path, os.path.getsize(path), len(G))
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'), ensure_ascii=False)
