# Arkerion — identité de marque

Document de référence de l'identité visuelle d'**Arkerion**, entreprise de développement web et logiciel : logo, couleurs, polices **Arkerion Sans** et **Arkerion Mono**, règles d'usage.

> Version 0.1 — étude. Les polices sont des versions de travail (voir « Statut »).

## Pages

| Page | Contenu |
|---|---|
| [`index.html`](index.html) | Charte d'identité : logo, règles d'usage, couleurs, typographie, code, applications |
| [`docs/`](docs/) | Exemple de page de documentation composée avec les polices Arkerion |
| [`ide/`](ide/) | Maquette d'IDE éditable pour tester les polices sur du code |

Pour les visualiser en ligne, activez GitHub Pages (Settings › Pages › branche `main`, dossier `/`) : le site est alors servi à l'adresse `https://rayan-studio.github.io/Arkerion-Docs/`.

En local : `npx serve .` (ou n'importe quel serveur statique) puis ouvrez `http://localhost:3000`.

## Contenu

```
assets/
  fonts/           Arkerion Sans et Arkerion Mono (TTF, OTF)
    etudes/        variantes d'étude Clarté et Nuance
  logo/            symbole, nom et logo complet en SVG, noir et blanc
docs/              page de documentation d'exemple
ide/               maquette d'IDE
sources/           générateur Python des polices (fontTools)
```

### Logo

| Fichier | Usage |
|---|---|
| `arkerion-logo-noir.svg` / `-blanc.svg` | Logo complet, usage principal |
| `arkerion-symbole-noir.svg` / `-blanc.svg` | Symbole seul : icône, avatar, favicon |
| `arkerion-nom-noir.svg` / `-blanc.svg` | Nom seul, vectorisé |

### Couleurs

| Nom | Hex | Rôle |
|---|---|---|
| Encre | `#0D0E10` | texte, logo |
| Papier | `#FFFFFF` | fonds |
| Texte secondaire | `#43474F` | paragraphes |
| Légendes | `#767B85` | métadonnées |
| Filets | `#E7E8EB` | bordures, séparateurs |
| Bleu Arkerion | `#1F4FD1` | liens, états actifs, focus |

## Statut des polices

Les deux polices sont générées par paramètres (`sources/`) et couvrent l'alphabet latin de base, les chiffres, la ponctuation de code, les accents français courants et, pour Arkerion Mono, dix ligatures de code (`=> -> <- == === != !== <= >= <=>`).

Avant un usage en production :

1. Reprendre les dessins dans un éditeur de polices (FontLab, Glyphs) et fusionner les contours qui se chevauchent.
2. Ajouter le hinting (ttfautohint) pour la netteté à petite taille sous Windows.
3. Compléter le jeu de caractères : guillemets français, tiret long, points de suspension, ligatures o-e et a-e.
4. Dessiner les graisses Medium, Semibold et Bold, puis exporter en WOFF2.

## Régénérer les polices

```sh
cd sources
pip install fonttools
python build3.py          # Arkerion Sans (3 variantes d'étude)
python mono.py            # Arkerion Mono
python tools/otf2ttf.py out3/*.otf
```

---

© Arkerion. Tous droits réservés. Les polices et le logo sont la propriété d'Arkerion.
