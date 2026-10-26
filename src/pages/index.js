import React, { useState } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import CodeBlock from '@theme/CodeBlock';
import { Mark } from '@site/src/components/Brand';
import styles from './index.module.css';

/* Page d'accueil : en-tête en deux colonnes (texte, code), mosaïque de trois
   entrées, parcours en un panneau, puis une barre de liens pour continuer.
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

function LinkList({ links }) {
  return (
    <ul className={styles.linkList}>
      {links.map(([label, to]) => (
        <li key={label}>
          <SmartLink to={to} className={styles.arrowLink}>
            {label}
          </SmartLink>
        </li>
      ))}
    </ul>
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
  const [identity, fonts, nebula] = ENTRIES;
  return (
    <Layout title="Accueil" description="Documentation d'Arkerion, entreprise de développement web et logiciel.">
      <main className={styles.page}>
        <header className={styles.hero}>
          <div className={styles.heroText}>
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
          </div>
          <Snippets />
        </header>

        <section className={styles.section}>
          <h2 className={styles.h2}>Explorer</h2>
          <div className={styles.bento}>
            <div className={clsx(styles.tile, styles.tileIdentity)}>
              <span className={styles.tileArt} aria-hidden="true">
                <Mark size={96} />
              </span>
              <div>
                <h3 className={styles.h3}>{identity.title}</h3>
                <p className={styles.entryText}>{identity.text}</p>
                <LinkList links={identity.links} />
              </div>
            </div>

            <div className={clsx(styles.tile, styles.tileFonts)}>
              <div className={styles.specimens} aria-hidden="true">
                <span className={clsx(styles.sample, styles.sans)}>Aa</span>
                <span className={clsx(styles.sample, styles.mono)}>{'=>'}</span>
              </div>
              <div>
                <h3 className={styles.h3}>
                  {fonts.title}
                  <span className={styles.badge}>Sans v0.14</span>
                </h3>
                <p className={styles.entryText}>{fonts.text}</p>
                <LinkList links={fonts.links} />
              </div>
            </div>

            <div className={clsx(styles.tile, styles.tileNebula)}>
              <h3 className={styles.h3}>{nebula.title}</h3>
              <p className={styles.entryText}>{nebula.text}</p>
              <LinkList links={nebula.links} />
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <div className={styles.panel}>
            <div className={styles.panelHead}>
              <h2 className={styles.h2}>De l'idée à la page publiée</h2>
              <p className={styles.sub}>Le parcours d'une page de cette documentation.</p>
            </div>
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
          </div>
        </section>

        <nav className={styles.more} aria-label="Continuer">
          <span className={styles.moreLabel}>Continuer</span>
          {MORE.map(([title, , to]) => (
            <SmartLink key={title} to={to} className={styles.moreLink}>
              {title}
            </SmartLink>
          ))}
        </nav>
      </main>
    </Layout>
  );
}
