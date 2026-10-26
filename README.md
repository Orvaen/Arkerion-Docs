# Arkerion Docs

Documentation d'**Arkerion**, entreprise de développement web et logiciel. Site [Docusaurus](https://docusaurus.io) écrit en **MDX** et composé avec nos propres polices, **Arkerion Sans** et **Arkerion Mono**.

**En ligne :** https://orvaen.github.io/Arkerion-Docs/

## Démarrer

```bash
npm install
npm start          # http://localhost:3000/Arkerion-Docs/
```

```bash
npm run build      # site statique dans build/
npm run serve      # sert la version construite
```

Node.js 18 ou plus récent.

## Publication

Chaque push sur `main` construit et publie le site sur GitHub Pages (`.github/workflows/deploy.yml`).
À la première mise en place : **Settings › Pages › Source : GitHub Actions**.

## Contenu

```
docs/                 pages MDX
  intro.mdx
  identite/           logo, couleurs, typographie, polices
  produits/           Nebula
  contribuer/         rédiger une page, faire tourner le site
src/
  components/Brand.js composants MDX : Lockup, Mark, LogoGrid, ColorGrid, Specimen, TypeScale, Ligatures
  css/custom.css      thème Arkerion (polices, couleurs, clair et sombre)
  fonts/              polices chargées par le site
  pages/index.js      page d'accueil
static/
  fonts/              Arkerion Sans et Arkerion Mono à télécharger (TTF, OTF)
    v2/               Arkerion Sans v2 (lettres du nom Arkerion)
  v2/comparaison.html page de comparaison v1 / v2
  img/logo/           logos SVG noir et blanc
sources/              générateur Python des polices (fontTools)
  arkerion-sans-v2/   sources UFO v1 et v2, scripts et rapport de la v2
```

## Polices

Versions d'étude : Arkerion Sans 0.15 (p, q, b, d et r redessinés à partir de l'arche du n ; o, O, c, ç, a, e, p, q, b et d élargis ; A et N à empattements ; a, f, g, s, S, y et G redessinés), Arkerion Mono 0.3. Les polices couvrent l'alphabet latin de base, les chiffres, la ponctuation de code et les accents français courants ; Arkerion Mono a dix ligatures de code (`=> -> <- == === != !== <= >= <=>`). La suite du travail est décrite sur la page *Polices* de la documentation.

---

© Arkerion. Tous droits réservés. Les polices et le logo sont la propriété d'Arkerion.
