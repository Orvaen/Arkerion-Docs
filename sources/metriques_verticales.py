"""Métriques verticales cohérentes pour les polices Arkerion.

Pourquoi : les polices avaient trois jeux de métriques qui ne concordaient pas.
  - hhea (lu par macOS)     : 940 au-dessus, 260 en dessous ;
  - usWin                   : 940 / 260 ;
  - OS/2 typo (lu par Windows, car le drapeau USE_TYPO_METRICS est actif) :
    800 / 240, plus un interligne de 200.
Sous Windows, le navigateur centrait donc la ligne sur une boîte plus basse que
le dessin : les capitales remontaient d'environ 70 unités, et le texte paraissait
décentré dans les boutons et les pastilles.

Correction : les trois jeux reçoivent les mêmes valeurs, interligne nul, choisies
pour que le milieu des capitales tombe au milieu de la boîte de ligne
(ascendante − descendante ≈ hauteur des capitales, avec un léger biais mesuré),
sur une hauteur totale de 1200 unités, inchangée. Les valeurs couvrent l'encombrement de tous les glyphes.

Usage : python3 metriques_verticales.py fichier.otf|ttf [...]
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

TOTAL = 1200   # hauteur de la boîte de ligne, en unités (pour 1000 unités par cadratin)
BIAS = 15      # boîte remontée de 15 unités : compense l'arrondi de la ligne de base
               # (mesuré dans Chromium, centrage alors équivalent à Inter et Arial)


def cap_height(f):
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    letter = next(c for c in 'HIE' if ord(c) in cmap)   # la police du logo n'a que les lettres du nom
    bp = BoundsPen(gs)
    gs[cmap[ord(letter)]].draw(bp)
    return bp.bounds[3]


def fix(path):
    f = TTFont(path)
    cap = cap_height(f)
    asc = round((TOTAL + cap) / 2) + BIAS
    desc = TOTAL - asc
    if -f['head'].yMin > desc:          # pas de place sous la ligne de base : pas de biais
        asc = round((TOTAL + cap) / 2)
        desc = TOTAL - asc
    head = f['head']
    if head.yMax > asc or -head.yMin > desc:
        raise SystemExit(f'{path} : glyphes hors de la boîte ({head.yMin}, {head.yMax}) pour {asc}/{desc}')
    hhea, os2 = f['hhea'], f['OS/2']
    hhea.ascent, hhea.descent, hhea.lineGap = asc, -desc, 0
    os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = asc, -desc, 0
    os2.usWinAscent, os2.usWinDescent = asc, desc
    os2.fsSelection |= 1 << 7          # USE_TYPO_METRICS : mêmes valeurs partout
    if hasattr(os2, 'sCapHeight'):
        os2.sCapHeight = round(cap)
    f.save(path)
    print(f'{path} : capitales {cap:.0f}, boîte {asc} / {desc}')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        fix(p)
