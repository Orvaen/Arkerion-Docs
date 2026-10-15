"""Génère les fichiers du logo Arkerion (SVG) : symbole Structure, nom
vectorisé en Arkerion Sans (contours, sans dépendance à la police) et logo
complet, en noir et en blanc."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from directions2 import P2
from build3 import build_all

OUT = sys.argv[1] if len(sys.argv) > 1 else 'logo'
os.makedirs(OUT, exist_ok=True)

SYMBOL = ('<path d="M26 18 H64 A18 18 0 0 1 82 36 A6 6 0 0 1 76 42 H50 A6 6 0 0 0 44 48 V74 A8 8 0 0 1 36 82 '
          'H26 A8 8 0 0 1 18 74 V26 A8 8 0 0 1 26 18 Z"/><rect x="53" y="51" width="29" height="31" rx="7"/>')

TRACK = -25  # interlettrage du nom : -2,5 % du corps


def word_paths():
    G, K = build_all(P2)
    x = 0; ds = []; prev = None
    for ch in 'Arkerion':
        if prev:
            x += K.get((prev, ch), 0) + TRACK
        for p0, segs in G[ch]['c']:
            f = lambda p: '%g %g' % (round(p[0] + x, 1), round(-p[1], 1))
            d = 'M' + f(p0)
            for s in segs:
                d += ('L' + f(s[1])) if s[0] == 'L' else ('C' + ' '.join(f(q) for q in s[1:]))
            ds.append(d + 'Z')
        x += G[ch]['adv']; prev = ch
    lsb = G['A']['sb'][0]
    return ''.join(ds), x - G['n']['sb'][1], lsb


def svg(w, h, vb, body, fill, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}" role="img" '
            f'aria-label="{label}"><title>{label}</title><g fill="{fill}" fill-rule="nonzero">{body}</g></svg>\n')


d, wend, lsb = word_paths()
for name, fill in (('noir', '#0D0E10'), ('blanc', '#FFFFFF')):
    open(f'{OUT}/arkerion-symbole-{name}.svg', 'w').write(
        svg(512, 512, '18 18 64 64', SYMBOL, fill, 'Arkerion, symbole'))
    # nom seul : capitale 700, x de 0 au bout du n
    ww = wend - lsb
    open(f'{OUT}/arkerion-nom-{name}.svg', 'w').write(
        svg(round(ww / 4), round(740 / 4), f'{lsb} -715 {ww} 740', f'<path d="{d}"/>', fill, 'Arkerion'))
    # logo complet : symbole de 1000 unités centré sur la capitale, espace 330
    S, gap = 1000, 330
    sym = f'<g transform="translate(0 {-350 - S / 2}) scale({S / 64}) translate(-18 -18)">{SYMBOL}</g>'
    word = f'<g transform="translate({S + gap - lsb} 0)"><path d="{d}"/></g>'
    W = S + gap + ww
    open(f'{OUT}/arkerion-logo-{name}.svg', 'w').write(
        svg(round(W / 5), round(S / 5), f'0 {-350 - S / 2} {W} {S}', sym + word, fill, 'Arkerion'))
print('logos ok', OUT)
