# Arkerion Sans v2 — rapport de modifications

Base : `ArkerionStudy-1-Atelier.otf` (v1, 14 glyphes : A R K E I O N a r k e i o n).
Résultat : `ArkerionSans-Regular-v2.otf`, mêmes 14 glyphes, alphabet complet non commencé.

## 1. Sauvegarde et sources

| Fichier | Contenu |
|---|---|
| `source/ArkerionStudy-1-Atelier.otf` | copie intacte de la v1 (SHA-256 identique à l'original) |
| `ufo/ArkerionSans-Regular-v1.ufo` | contours de la v1 extraits de l'OTF, éditables (FontLab, Glyphs, RoboFont) |
| `ufo/ArkerionSans-Regular-v2.ufo` | sources éditables de la v2 : contours, chasses, crénage, zones d'alignement, fûts de référence |
| `glyphs_v2.py`, `build_v2.py` | construction de chaque glyphe et génération de l'OTF et de l'UFO |

## 2. Analyse de la v1

- **Contours superposés partout** : 23 chevauchements (R 6, K 3, E 3, k 3…). Cause des liserés visibles à l'écran.
- **Débordements de chasse** : approche droite négative sur R (−3), K (−19) et k (−9).
- **A** étroit, à pointe en dépassement (708) et jambages de même épaisseur.
- **r** à l'oreille longue terminée en pointe ; **e** à la terminaison oblique aiguë.
- **K/k** : jambe et bras qui se croisent dans le fût, jonction lourde.
- **R** : jambe partant du fût, sans caractère.
- Hauteur d'x de 500 (0,71 de la capitale) ; aucun crénage.

## 3. Modifications

| Glyphe | v2 |
|---|---|
| A | plus large (684), sommet plat de 46 aligné sur H, jambage gauche délié (0,80) et droit appuyé (1,02), barre abaissée à 186 |
| R | jambe issue de la panse, raide, qui s'évase de 0,94 à 1,14 × fût vers le pied et dépasse la panse |
| K, k | bras issu du fût, affiné à la jonction ; jambe greffée sur le bras ; plus aucun débordement |
| E | barre médiane au-dessus du centre géométrique ; bras inférieur le plus long |
| O, o | construction conservée ; flancs 1,08 × fût, déliés 74 et 68, dépassements 12 et 10 |
| N | fûts à 0,92, diagonale à 1,04 × fût en épaisseur réelle |
| n | épaule qui naît du fût sous son sommet (0,875 x), aisselle à 0,64 x : arche plus fluide |
| r | oreille plus courte, coupe perpendiculaire au trait et légèrement bombée |
| e | terminaison radiale bombée, ouverture agrandie, œil plus généreux |
| a | capuchon et panse recalibrés, jonctions affinées, terminaison adoucie |
| i | point aligné sur l'ascendante, diamètre 1,2 × fût |

**Hauteur d'x : 500 → 520** (rapport x/H 0,74). Les épreuves à 12–16 px montrent des minuscules plus lisibles sans déséquilibrer les capitales.

## 4. Qualité typographique

- **Contours uniques** : chaque glyphe est redessiné comme une seule silhouette avec ses contre-formes, aux intersections calculées. Aucun chevauchement, aucune auto-intersection.
- **Courbes** : quarts de super-ellipse découpés aux points de jonction ; points d'extremum présents sur toutes les courbes ; raccords courbe/courbe tangents. Seuls les angles des terminaisons (a, e, r) sont volontairement vifs.
- **Épaisseurs** : capitales 86 / 74, minuscules 80 / 68. Rondes compensées (×1,08), diagonales calculées en épaisseur perpendiculaire.
- **Alignements** : droites exactement sur 0, 520, 700 et 735 ; rondes en dépassement de 10 (minuscules) et 12 (capitales).
- **Espacement** : approches calculées par aires de blanc à profondeur limitée (fût : 80 en capitale, 64 en minuscule), puis **13 paires de crénage** (ke, ko, ra, re, ro, Ae, Ao, AR, RK, RI, KE, ER, ka).

## 5. Vérification technique (v2)

| Contrôle | v1 | v2 |
|---|---|---|
| Contours (14 glyphes) | 37 | 21 |
| Chevauchements | 23 | 0 |
| Auto-intersections | 0 | 0 |
| Extremums manquants | 0 | 0 |
| Approches négatives | 3 | 0 |
| Paires de crénage | 0 | 13 |

## 6. Limites

- **Hinting** : la v2 n'est pas hintée (ttfautohint n'est pas disponible ici). À faire avant tout usage en petite taille sous Windows.
- **Jeu de caractères** : seulement les 14 lettres de l'étude, comme demandé.
- **Poids visuel** : le réglage de la page de comparaison épaissit le rendu par contour. C'est un outil d'évaluation, pas une vraie graisse.

## 7. Comparer

Ouvrez `comparaison.html` dans un navigateur. La page contient :

- l'épreuve vectorielle v1 / v2 avec les lignes de métrique ;
- « Arkerion » de 12 à 110 px ;
- chaque glyphe avant/après, avec superposition possible ;
- le tableau des mesures ;
- les réglages de texte, taille, poids visuel et espacement.
