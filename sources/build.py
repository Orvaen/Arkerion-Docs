"""Compile chaque direction en police de test OTF (CFF) + données SVG."""
import json, base64, os
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from glyphs import GLYPHS
from directions import DIRECTIONS

OUT = os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(OUT, exist_ok=True)
NAMES = {'A': 'A', 'R': 'R', 'K': 'K', 'E': 'E', 'I': 'I', 'O': 'O', 'N': 'N',
         'a': 'a', 'r': 'r', 'k': 'k', 'e': 'e', 'i': 'i', 'o': 'o', 'n': 'n'}


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


def svg_d(contours):
    out = []
    f = lambda p: '%g %g' % (round(p[0], 1), round(-p[1], 1))
    for p0, segs in contours:
        out.append('M' + f(p0))
        for s in segs:
            out.append(('L' + f(s[1])) if s[0] == 'L' else ('C' + ' '.join(f(p) for p in s[1:])))
        out.append('Z')
    return ''.join(out)


def build(P, idx):
    fam = 'Arkerion Study %s' % P['name']
    order = ['.notdef', 'space'] + list(NAMES.values())
    fb = FontBuilder(1000, isTTF=False)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({0x20: 'space', **{ord(c): n for c, n in NAMES.items()}})
    cs, metrics, data = {}, {}, {}
    pen = T2CharStringPen(500, None)
    pen.moveTo((50, 0)); pen.lineTo((450, 0)); pen.lineTo((450, 700)); pen.lineTo((50, 700)); pen.closePath()
    cs['.notdef'] = pen.getCharString(); metrics['.notdef'] = (500, 50)
    pen = T2CharStringPen(250, None); cs['space'] = pen.getCharString(); metrics['space'] = (250, 0)
    for ch, name in NAMES.items():
        contours, adv = GLYPHS[ch](P)
        adv = round(adv)
        pen = T2CharStringPen(adv, None)
        draw(pen, contours)
        cs[name] = pen.getCharString()
        xs = [p[0] for c in contours for p in [c[0]] + [s[-1] for s in c[1]]]
        metrics[name] = (adv, round(min(xs)))
        data[ch] = {'d': svg_d(contours), 'adv': adv}
    fb.setupCFF(fam.replace(' ', '') + '-Regular', {'FullName': fam + ' Regular'}, cs, {})
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=930, descent=-250)
    fb.setupNameTable({'familyName': fam, 'styleName': 'Regular'})
    fb.setupOS2(sTypoAscender=P['asc'], sTypoDescender=P['desc'], sTypoLineGap=200,
                usWinAscent=930, usWinDescent=250, sxHeight=P['xh'], sCapHeight=P['cap'],
                achVendID='ARKR')
    fb.setupPost()
    path = os.path.join(OUT, 'ArkerionStudy-%d-%s.otf' % (idx + 1, P['name']))
    fb.save(path)
    return path, data


if __name__ == '__main__':
    bundle = []
    for i, P in enumerate(DIRECTIONS):
        path, data = build(P, i)
        b64 = base64.b64encode(open(path, 'rb').read()).decode()
        bundle.append({'name': P['name'], 'font': b64, 'glyphs': data,
                       'metrics': {k: P[k] for k in ('cap', 'xh', 'asc', 'SV', 'sv', 'SH', 'sh')}})
        print(path, os.path.getsize(path))
    json.dump(bundle, open(os.path.join(OUT, 'study.json'), 'w'))
