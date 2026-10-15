import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './Nebula.module.css';

/** Symbole Nebula (« Amas »), en currentColor. Même grille de 64 que le symbole Structure. */
export function NebulaMark({ size = 48, label }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="18 18 64 64"
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      className={styles.mark}>
      <g fill="currentColor">
        <path d="M26 18 H40 A18 18 0 0 1 58 36 V50 A8 8 0 0 1 50 58 H26 A8 8 0 0 1 18 50 V26 A8 8 0 0 1 26 18 Z" />
        <rect x="64" y="40" width="18" height="18" rx="6" />
        <rect x="40" y="64" width="18" height="18" rx="6" />
        <rect x="68" y="68" width="14" height="14" rx="5" />
      </g>
    </svg>
  );
}

/** Logo complet, en image (le nom est vectorisé en Arkerion Sans). */
export function NebulaLockup({ height = 56 }) {
  const base = useBaseUrl('/img/nebula/');
  return (
    <div className={styles.hero}>
      <div className={styles.heroLight}>
        <img src={`${base}nebula-logo-noir.svg`} alt="Nebula" style={{ height }} />
      </div>
      <div className={styles.heroDark}>
        <img src={`${base}nebula-logo-blanc.svg`} alt="Nebula, version blanche" style={{ height }} />
      </div>
    </div>
  );
}

function Preview({ title, note, children, wide }) {
  return (
    <figure className={`${styles.preview} ${wide ? styles.wide : ''}`}>
      <div className={styles.stage}>{children}</div>
      <figcaption className={styles.cap}>
        <span>{title}</span>
        <span className={styles.muted}>{note}</span>
      </figcaption>
    </figure>
  );
}

/** Aperçus du logo Nebula en situation. */
export function NebulaPreviews() {
  const base = useBaseUrl('/img/nebula/');
  return (
    <div className={styles.grid}>
      <Preview title="Icône d'application" note="fond noir ou blanc">
        <div className={styles.icons}>
          <div className={`${styles.appIcon} ${styles.iconInk}`}>
            <NebulaMark size={54} />
          </div>
          <div className={`${styles.appIcon} ${styles.iconPaper}`}>
            <NebulaMark size={54} />
          </div>
        </div>
      </Preview>

      <Preview title="Petites tailles" note="64, 32, 24 et 16 px">
        <div className={styles.sizes}>
          {[64, 32, 24, 16].map((s) => (
            <div key={s} className={styles.size}>
              <NebulaMark size={s} />
              <code>{s}</code>
            </div>
          ))}
        </div>
      </Preview>

      <Preview title="Onglet de navigateur" note="favicon à 16 px">
        <div className={styles.browser}>
          <div className={styles.tabs}>
            <div className={`${styles.tab} ${styles.tabActive}`}>
              <NebulaMark size={14} />
              <span>Nebula</span>
              <span className={styles.close}>×</span>
            </div>
            <div className={styles.tab}>
              <span className={styles.dot} />
              <span>Nouvel onglet</span>
            </div>
          </div>
          <div className={styles.urlbar}>orvaen.github.io/Arkerion-Docs/docs/produits/nebula</div>
        </div>
      </Preview>

      <Preview title="Fenêtre du logiciel" note="barre de titre">
        <div className={styles.window}>
          <div className={styles.titlebar}>
            <span className={styles.lights}>
              <i />
              <i />
              <i />
            </span>
            <span className={styles.wtitle}>
              <NebulaMark size={14} />
              Nebula
            </span>
          </div>
          <div className={styles.wbody}>
            <div>
              <span className={styles.prompt}>~</span> nebula
            </div>
            <div className={styles.cursorLine}>
              <span className={styles.prompt}>~</span> <span className={styles.cursor} />
            </div>
          </div>
        </div>
      </Preview>

      <Preview title="Carte de partage" note="1280 × 640, réseaux sociaux et GitHub" wide>
        <div className={styles.social}>
          <img src={`${base}nebula-logo-blanc.svg`} alt="Nebula" className={styles.socialLogo} />
          <div className={styles.socialFoot}>
            <span>Un logiciel Arkerion</span>
          </div>
        </div>
      </Preview>
    </div>
  );
}
