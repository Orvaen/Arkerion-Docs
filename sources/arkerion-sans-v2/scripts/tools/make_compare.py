import os, sys, json, base64
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE); sys.path.insert(0, HERE + '/tools'); sys.path.insert(0, '/home/claude/arkerion')
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from analyze import analyze

V1 = HERE + '/source/ArkerionStudy-1-Atelier.otf'
V2 = HERE + '/build/ArkerionSans-Regular-v2.otf'


def kern_pairs(f):
    out = {}
    if 'GPOS' not in f:
        return out
    order = f.getGlyphOrder()
    for lk in f['GPOS'].table.LookupList.Lookup:
        for st in lk.SubTable:
            if getattr(st, 'Format', 0) == 1 and hasattr(st, 'PairSet'):
                firsts = st.Coverage.glyphs
                for g1, ps in zip(firsts, st.PairSet):
                    for pvr in ps.PairValueRecord:
                        v = pvr.Value1.XAdvance if pvr.Value1 and hasattr(pvr.Value1, 'XAdvance') else 0
                        out[g1 + pvr.SecondGlyph] = v
    return out


def extract(path, metrics):
    f = TTFont(path); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    glyphs = {}
    for ch in 'ARKEIONarkeion':
        g = cmap[ord(ch)]
        sp = SVGPathPen(gs); gs[g].draw(TransformPen(sp, (1, 0, 0, -1, 0, 0)))
        bp = BoundsPen(gs); gs[g].draw(bp)
        adv = f['hmtx'][g][0]
        glyphs[ch] = dict(d=sp.getCommands(), adv=adv, lsb=round(bp.bounds[0]), rsb=round(adv - bp.bounds[2]))
    kern = {k: v for k, v in kern_pairs(f).items() if len(k) == 2}
    return dict(glyphs=glyphs, kern=kern, space=f['hmtx'][cmap[32]][0], metrics=metrics)


m1 = dict(asc=735, cap=700, xh=500, desc=-200)
m2 = dict(asc=735, cap=700, xh=520, desc=-200)
d1, d2 = extract(V1, m1), extract(V2, m2)
a1, s1, _ = analyze(V1, {'xh': 500, 'cap': 700, 'E_x': 300})
a2, s2, _ = analyze(V2, {'xh': 520, 'cap': 700, 'E_x': 300})
tot = lambda a, k: sum(v[k] for v in a.values())
neg = lambda a: sum(1 for v in a.values() if v['rsb'] < 0 or v['lsb'] < 0)


def word(d, w, kern=True):
    x = 0; prev = None
    for ch in w:
        if prev and kern:
            x += d['kern'].get(prev + ch, 0)
        x += d['glyphs'][ch]['adv']; prev = ch
    return x


table = [
    ['Hauteur d\'x', 500, 520, True, '+4 % : minuscules plus lisibles, rapport x/H 0,74'],
    ['Hauteur des capitales', 700, 700, False, ''],
    ['Fût capitale (I)', s1['I stem'], s2['I stem'], False, ''],
    ['Fût minuscule (n)', s1['n stem'], s2['n stem'], False, ''],
    ['Délié horizontal (barre du E)', s1['E bar'], s2['E bar'], False, ''],
    ['o : flanc / haut / bas', '%s / %s / %s' % (s1['o side'], s1['o top'], s1['o bottom']),
     '%s / %s / %s' % (s2['o side'], s2['o top'], s2['o bottom']), True, 'flancs 1,08 × fût, déliés 0,85 × fût'],
    ['Sommet du A', '%s (pointe en dépassement)' % a1['A']['ymax'], '%s (sommet plat)' % a2['A']['ymax'], True, 'aligné sur la hauteur des capitales'],
    ['Contours (14 glyphes)', tot(a1, 'contours'), tot(a2, 'contours'), True, 'un contour par silhouette'],
    ['Chevauchements de contours', tot(a1, 'overlaps'), tot(a2, 'overlaps'), True, 'plus aucun : rendu sans liseré'],
    ['Auto-intersections', tot(a1, 'self_intersections'), tot(a2, 'self_intersections'), False, ''],
    ['Extremums manquants', tot(a1, 'missing_extrema'), tot(a2, 'missing_extrema'), False, ''],
    ['Glyphes à approche négative', neg(a1), neg(a2), True, 'R, K et k débordaient de leur chasse'],
    ['Paires de crénage', len(d1['kern']), len(d2['kern']), True, ''],
    ['Largeur de « Arkerion »', word(d1, 'Arkerion'), word(d2, 'Arkerion'), False, 'en unités, crénage compris'],
]

notes = {
    'A': 'Plus large et mieux assis : sommet plat étroit aligné sur H, jambage gauche délié et droit appuyé, barre abaissée.',
    'R': 'Jambe raide issue de la panse, qui s\'évase vers le pied et dépasse la panse : plus de caractère, plus de stabilité.',
    'K': 'Jambe greffée sur le bras plutôt que croisée ; bras légèrement affiné au fût, plus de débordement de chasse.',
    'E': 'Barre médiane au-dessus du centre géométrique (centre optique), bras inférieur le plus long.',
    'I': 'Fût de 86 unités, cohérent avec les autres capitales.',
    'O': 'Flancs 1,08 × fût, déliés 74 : couleur égale à celle des droites ; dépassement de 12.',
    'N': 'Fûts affinés (0,92) et diagonale à 1,04 × fût, calculée en épaisseur réelle.',
    'a': 'Capuchon et panse recalibrés pour la hauteur d\'x ; jonctions affinées, terminaison radiale adoucie.',
    'r': 'Oreille raccourcie, coupe perpendiculaire au trait et légèrement bombée : plus de pointe.',
    'k': 'Même construction que le K, bras et jambe équilibrés autour d\'une jonction unique.',
    'e': 'Terminaison inférieure radiale et bombée, ouverture agrandie, barre au-dessus du centre.',
    'i': 'Point aligné sur l\'ascendante, diamètre 1,2 × fût.',
    'o': 'Construction conservée ; épaisseurs rééquilibrées, dépassement de 10, tension 0,56.',
    'n': 'Épaule qui naît du fût sous son sommet, aisselle profonde (0,64 x) : arche plus fluide.',
}

t = open(HERE + '/compare_template.html').read()
t = t.replace('__V1__', base64.b64encode(open(V1, 'rb').read()).decode())
t = t.replace('__V2__', base64.b64encode(open(V2, 'rb').read()).decode())
t = t.replace('__DATA__', json.dumps({'v1': d1, 'v2': d2, 'table': table}, ensure_ascii=False))
t = t.replace('__NOTES__', json.dumps(notes, ensure_ascii=False))
open(HERE + '/comparaison.html', 'w').write(t)
print('ok', len(t), d2['kern'])
