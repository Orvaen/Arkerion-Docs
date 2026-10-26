import React, { useState } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import CodeBlock from '@theme/CodeBlock';
import styles from './index.module.css';

/* Page d'accueil : en-tête et boutons, exemples de code à onglets, points
   d'entrée, parcours en quatre étapes, polices, puis liens pour continuer.
   Tout le contenu renvoie à des pages qui existent dans la documentation. */

const SNIPPETS = [
  {
    id: 'css',
    label: 'Site web',
    title: 'fonts.css',
    language: 'css',
    code: `@font-face {
  font-family: "Arkerion Sans";
  src: url("./fonts/ArkerionSans-Regular.ttf") format("truetype");
  font-display: swap;
}

body {
  font-family: "Arkerion Sans", system-ui, sans-serif;
}`,
  },
  {
    id: 'vscode',
    label: 'VS Code',
    title: 'settings.json',
    language: 'json',
    code: `{
  "editor.fontFamily": "'Arkerion Mono', monospace",
  "editor.fontLigatures": true,
  "editor.fontSize": 14,
  "editor.lineHeight": 1.6
}`,
  },
  {
    id: 'local',
    label: 'Cette doc en local',
    title: 'Terminal',
    language: 'bash',
    code: `git clone https://github.com/Orvaen/Arkerion-Docs.git
cd Arkerion-Docs
npm install
npm start`,
  },
];

const ENTRIES = [
  {
    title: 'Identité',
    text: 'Le symbole Structure, la palette et la typographie de la marque.',
    links: [
      ['Logo', '/docs/identite/logo'],
      ['Couleurs', '/docs/identite/couleurs'],
      ['Typographie', '/docs/identite/typographie'],
    ],
  },
  {
    title: 'Polices',
    text: "Arkerion Sans pour l'interface, Arkerion Mono pour le code.",
    links: [
      ['Installer les polices', '/docs/identite/polices'],
      ['Arkerion Sans v2', '/docs/identite/arkerion-sans-v2'],
    ],
  },
  {
    title: 'Nebula',
    text: 'Le logiciel développé par Arkerion.',
    links: [
      ['Présentation', '/docs/produits/nebula'],
      ['Code source', 'https://github.com/Orvaen/nebula'],
    ],
  },
];

const STEPS = [
  {
    title: 'Découvrir',
    links: [
      ['Introduction', '/docs/intro'],
      ['Le logo', '/docs/identite/logo'],
      ['La palette', '/docs/identite/couleurs'],
    ],
  },
  {
    title: 'Composer',
    links: [
      ['Typographie et hiérarchie', '/docs/identite/typographie'],
      ['Installer les polices', '/docs/identite/polices'],
      ["L'étude Arkerion Sans v2", '/docs/identite/arkerion-sans-v2'],
    ],
  },
  {
    title: 'Rédiger',
    links: [
      ['Rédiger une page', '/docs/contribuer/rediger'],
      ['Documenter Nebula', '/docs/produits/nebula'],
    ],
  },
  {
    title: 'Publier',
    links: [
      ['Faire tourner le site', '/docs/contribuer/projet'],
      ['Dépôt GitHub', 'https://github.com/Orvaen/Arkerion-Docs'],
    ],
  },
];

const FONTS = [
  {
    name: 'Arkerion Sans',
    to: '/docs/identite/typographie',
    sample: 'Aa',
    sampleClass: 'sans',
    badge: 'v0.13',
    tags: ['Interface', 'Titres'],
    text: 'La police de la marque : A et N à empattements, f et g géométriques.',
  },
  {
    name: 'Arkerion Mono',
    to: '/docs/identite/polices',
    sample: '=> !=',
    sampleClass: 'mono',
    tags: ['Code', 'Ligatures'],
    text: 'Pour les éditeurs et les terminaux, avec dix ligatures de code.',
  },
  {
    name: 'Arkerion Sans v2',
    to: '/docs/identite/arkerion-sans-v2',
    sample: 'Ark',
    sampleClass: 'wordmark',
    tags: ['Étude', 'Nom Arkerion'],
    text: "Les quatorze lettres du nom, redessinées pour le logo.",
  },
];

const MORE = [
  ['Logo', 'Versions, zones de protection et usages.', '/docs/identite/logo'],
  ['Couleurs', "La palette claire et l'Améthyste Arkerion.", '/docs/identite/couleurs'],
  ['Typographie', 'Rôles des polices et échelle des tailles.', '/docs/identite/typographie'],
  ['Contribuer', 'Écrire une page en MDX et la publier.', '/docs/contribuer/rediger'],
  ['GitHub', 'Le code source de cette documentation.', 'https://github.com/Orvaen/Arkerion-Docs'],
];

function SmartLink({ to, className, children }) {
  return (
    <Link to={to} className={className}>
      {children}
      {to.startsWith('http') && <span className={styles.ext} aria-hidden="true">↗</span>}
    </Link>
  );
}

function Snippets() {
  const [active, setActive] = useState(SNIPPETS[0].id);
  const current = SNIPPETS.find((s) => s.id === active);
  return (
    <div className={styles.snippets}>
      <div className={styles.tabs} role="tablist" aria-label="Exemples">
        {SNIPPETS.map((s) => (
          <button
            key={s.id}
            type="button"
            role="tab"
            aria-selected={s.id === active}
            className={clsx(styles.tab, s.id === active && styles.tabActive)}
            onClick={() => setActive(s.id)}>
            {s.label}
          </button>
        ))}
      </div>
      <CodeBlock language={current.language} title={current.title}>
        {current.code}
      </CodeBlock>
    </div>
  );
}

export default function Home() {
  return (
    <Layout title="Accueil" description="Documentation d'Arkerion, entreprise de développement web et logiciel.">
      <main className={styles.page}>
        <header className={styles.hero}>
          <p className={styles.eyebrow}>Documentation Arkerion</p>
          <h1 className={styles.title}>Construire avec Arkerion</h1>
          <p className={styles.lead}>
            L'identité, les polices et les produits d'Arkerion, entreprise de développement web et logiciel.
          </p>
          <div className={styles.ctas}>
            <Link className={clsx(styles.btn, styles.btnPrimary)} to="/docs/intro">
              Commencer
            </Link>
            <Link className={clsx(styles.btn, styles.btnSecondary)} to="/docs/identite/polices">
              Utiliser les polices
            </Link>
            <SmartLink className={clsx(styles.btn, styles.btnGhost)} to="https://github.com/Orvaen/Arkerion-Docs">
              Code source
            </SmartLink>
          </div>
          <Snippets />
        </header>

        <section className={styles.section}>
          <h2 className={styles.h2}>Par où commencer</h2>
          <p className={styles.sub}>Trois portes d'entrée, selon ce que vous venez chercher.</p>
          <div className={styles.entries}>
            {ENTRIES.map((e) => (
              <div key={e.title} className={styles.entry}>
                <h3 className={styles.h3}>{e.title}</h3>
                <p className={styles.entryText}>{e.text}</p>
                <ul className={styles.linkList}>
                  {e.links.map(([label, to]) => (
                    <li key={label}>
                      <SmartLink to={to} className={styles.arrowLink}>
                        {label}
                      </SmartLink>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        <section className={styles.section}>
          <h2 className={styles.h2}>De l'idée à la page publiée</h2>
          <p className={styles.sub}>Le parcours d'une page de cette documentation, en quatre étapes.</p>
          <ol className={styles.steps}>
            {STEPS.map((s, i) => (
              <li key={s.title} className={styles.step}>
                <span className={styles.stepNum}>{i + 1}</span>
                <h3 className={styles.h3}>{s.title}</h3>
                <ul className={styles.stepLinks}>
                  {s.links.map(([label, to]) => (
                    <li key={label}>
                      <SmartLink to={to}>{label}</SmartLink>
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ol>
        </section>

        <section className={styles.section}>
          <h2 className={styles.h2}>Les polices Arkerion</h2>
          <p className={styles.sub}>Dessinées pour la marque, et utilisées sur tout ce site.</p>
          <div className={styles.fonts}>
            {FONTS.map((f) => (
              <Link key={f.name} to={f.to} className={styles.fontCard}>
                <span className={clsx(styles.sample, styles[f.sampleClass])} aria-hidden="true">
                  {f.sample}
                </span>
                <span className={styles.fontName}>
                  {f.name}
                  {f.badge && <span className={styles.badge}>{f.badge}</span>}
                </span>
                <span className={styles.tags}>
                  {f.tags.map((t) => (
                    <span key={t} className={styles.tag}>
                      {t}
                    </span>
                  ))}
                </span>
                <span className={styles.fontText}>{f.text}</span>
              </Link>
            ))}
          </div>
        </section>

        <section className={clsx(styles.section, styles.last)}>
          <h2 className={styles.h2}>Continuer</h2>
          <div className={styles.more}>
            {MORE.map(([title, text, to]) => (
              <SmartLink key={title} to={to} className={styles.moreCard}>
                <span className={styles.moreTitle}>{title}</span>
                <span className={styles.moreText}>{text}</span>
              </SmartLink>
            ))}
          </div>
        </section>
      </main>
    </Layout>
  );
}
