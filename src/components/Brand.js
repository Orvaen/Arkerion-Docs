import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './Brand.module.css';

/** Symbole Structure, en currentColor. */
export function Mark({ size = 48, label }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="18 18 64 64"
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      className={styles.symbol}>
      <path
        fill="currentColor"
        d="M26 18 H64 A18 18 0 0 1 82 36 A6 6 0 0 1 76 42 H50 A6 6 0 0 0 44 48 V74 A8 8 0 0 1 36 82 H26 A8 8 0 0 1 18 74 V26 A8 8 0 0 1 26 18 Z"
      />
      <rect x="53" y="51" width="29" height="31" rx="7" fill="currentColor" />
    </svg>
  );
}

/** Logo complet : symbole + nom composé en Arkerion Sans. */
export function Lockup({ size = 40 }) {
  return (
    <span className={styles.lockup} style={{ fontSize: size }}>
      <Mark size={size * 1.15} />
      <span className={styles.word}>Arkerion</span>
    </span>
  );
}

export function LogoGrid({ name = 'Arkerion', prefix = 'arkerion', dir = '/img/logo/' }) {
  const files = [
    ['Logo complet', 'usage principal', `${prefix}-logo-noir.svg`, `${prefix}-logo-blanc.svg`],
    ['Symbole seul', 'icône, avatar', `${prefix}-symbole-noir.svg`, `${prefix}-symbole-blanc.svg`],
    ['Nom seul', 'texte courant', `${prefix}-nom-noir.svg`, `${prefix}-nom-blanc.svg`],
  ];
  const base = useBaseUrl(dir);
  return (
    <div className={styles.grid3}>
      {files.map(([label, use, dark, light]) => (
        <figure key={label} className={styles.tile}>
          <div className={styles.art}>
            <img src={`${base}${dark}`} alt={`${label} ${name}`} className={styles.logoImg} />
          </div>
          <div className={`${styles.art} ${styles.dark}`}>
            <img src={`${base}${light}`} alt={`${label} ${name}, version blanche`} className={styles.logoImg} />
          </div>
          <figcaption className={styles.cap}>
            <span>{label}</span>
            <span className={styles.muted}>{use}</span>
          </figcaption>
        </figure>
      ))}
    </div>
  );
}

export function ColorGrid({ colors }) {
  return (
    <div className={styles.swatches}>
      {colors.map((c) => (
        <div key={c.hex} className={styles.swatch}>
          <div className={styles.chip} style={{ background: c.hex }} />
          <div className={styles.info}>
            <span>{c.name}</span>
            <code>{c.hex}</code>
            <span className={styles.muted}>{c.role}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export function Specimen({ mono = false, big, lines, caption }) {
  return (
    <div className={`${styles.specimen} ${mono ? styles.mono : ''}`}>
      <div className={styles.big}>{big}</div>
      <div className={styles.glyphs}>
        {lines.map((l) => (
          <div key={l}>{l}</div>
        ))}
      </div>
      <div className={styles.row}>
        <span>{caption[0]}</span>
        <span>{caption[1]}</span>
      </div>
    </div>
  );
}

export function TypeScale({ steps }) {
  return (
    <div className={styles.scale}>
      {steps.map((s) => (
        <div key={s.label} className={styles.step}>
          <code>{s.label}</code>
          <span style={{ fontSize: s.size, lineHeight: s.lh }}>{s.text}</span>
        </div>
      ))}
    </div>
  );
}

export function Ligatures() {
  const items = ['=>', '->', '<-', '==', '===', '!=', '!==', '<=', '>=', '<=>'];
  return (
    <div className={styles.ligs}>
      {items.map((t) => (
        <div key={t} className={styles.lig}>
          <span className={styles.ligOn}>{t}</span>
          <code className={styles.ligOff}>{t.split('').join(' ')}</code>
        </div>
      ))}
    </div>
  );
}
