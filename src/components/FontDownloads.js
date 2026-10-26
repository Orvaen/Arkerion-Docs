import React from 'react';
import clsx from 'clsx';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './FontDownloads.module.css';

/* Boutons de téléchargement des polices. Les fichiers viennent de
   static/fonts ; l'archive .zip est créée par le workflow de publication
   (.github/workflows/deploy.yml), elle n'existe donc pas avec `npm start`. */

const FONTS = [
  {
    name: 'Arkerion Sans',
    version: '0.15',
    role: "Interface, titres et texte courant.",
    file: 'ArkerionSans-Regular',
    sample: 'Aa',
    mono: false,
  },
  {
    name: 'Arkerion Mono',
    version: '0.3',
    role: 'Code, terminal et éditeur.',
    file: 'ArkerionMono-Regular',
    sample: '=>',
    mono: true,
  },
];

function Download({ href, label, hint, primary }) {
  return (
    <a className={clsx(styles.btn, primary && styles.primary)} href={href} download>
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
        <path d="M7 1.5v8M3.5 6 7 9.5 10.5 6M2 12.5h10" />
      </svg>
      {label}
      {hint && <span className={styles.hint}>{hint}</span>}
    </a>
  );
}

export default function FontDownloads() {
  const base = useBaseUrl('/fonts/');
  return (
    <div className={styles.wrap}>
      <div className={styles.grid}>
        {FONTS.map((f) => (
          <div key={f.name} className={styles.card}>
            <span className={clsx(styles.sample, f.mono && styles.sampleMono)} aria-hidden="true">
              {f.sample}
            </span>
            <div className={styles.meta}>
              <p className={styles.name}>
                {f.name} <span className={styles.version}>v{f.version}</span>
              </p>
              <p className={styles.role}>{f.role}</p>
              <div className={styles.actions}>
                <Download href={`${base}${f.file}.ttf`} label="TTF" hint="recommandé" primary />
                <Download href={`${base}${f.file}.otf`} label="OTF" />
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className={styles.all}>
        <Download href={`${base}arkerion-polices.zip`} label="Tout télécharger" hint=".zip, TTF et OTF" />
        <span className={styles.note}>Graisse Regular uniquement, versions d'étude.</span>
      </div>
    </div>
  );
}
