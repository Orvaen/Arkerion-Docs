import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import CodeBlock from '@theme/CodeBlock';
import { Mark } from '@site/src/components/Brand';
import styles from './index.module.css';

const SECTIONS = [
  {
    to: '/docs/identite/logo',
    title: 'Identité',
    text: "Le symbole Structure, les couleurs et les règles d'usage du logo.",
  },
  {
    to: '/docs/identite/polices',
    title: 'Polices Arkerion',
    text: "Arkerion Sans pour l'interface, Arkerion Mono pour le code, avec ligatures.",
  },
  {
    to: '/docs/produits/nebula',
    title: 'Nebula',
    text: 'Le logiciel développé par Arkerion.',
  },
  {
    to: '/docs/contribuer/rediger',
    title: 'Rédiger la doc',
    text: 'Écrire une page en MDX : titres, code, encadrés et composants.',
  },
];

const SAMPLE = `import { defineConfig } from "@arkerion/sdk";

export default defineConfig({
  name: "nebula",
  healthCheck: (res) => res.status >= 200 && res.status !== 503,
});`;

export default function Home() {
  return (
    <Layout title="Accueil" description="Documentation d'Arkerion, entreprise de développement web et logiciel.">
      <header className={styles.hero}>
        <div className={styles.inner}>
          <div className={styles.lockup}>
            <Mark size={64} />
            <h1 className={styles.word}>Arkerion</h1>
          </div>
          <p className={styles.lead}>
            Documentation d'Arkerion, entreprise de développement web et logiciel. Identité, polices, produits et guides.
          </p>
          <div className={styles.ctas}>
            <Link className={styles.primary} to="/docs/intro">
              Lire la documentation
            </Link>
            <Link className={styles.ghost} to="/docs/identite/polices">
              Découvrir les polices
            </Link>
          </div>
        </div>
      </header>
      <main className={styles.inner}>
        <div className={styles.cards}>
          {SECTIONS.map((s) => (
            <Link key={s.to} to={s.to} className={styles.card}>
              <span className={styles.cardTitle}>{s.title}</span>
              <span className={styles.cardText}>{s.text}</span>
            </Link>
          ))}
        </div>
        <div className={styles.split}>
          <div>
            <h2 className={styles.h2}>Composée avec nos propres polices</h2>
            <p className={styles.p}>
              Tout ce site est composé en Arkerion Sans. Les extraits de code utilisent Arkerion Mono et ses ligatures :
              les flèches, les égalités et les comparaisons s'affichent en un seul signe.
            </p>
          </div>
          <CodeBlock language="ts" title="nebula.config.ts">
            {SAMPLE}
          </CodeBlock>
        </div>
      </main>
    </Layout>
  );
}
