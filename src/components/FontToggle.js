import React, { useEffect, useState } from 'react';
import clsx from 'clsx';
import styles from './FontToggle.module.css';

/**
 * Sélecteur de police de la barre de navigation : affiche la doc en
 * Arkerion Sans ou dans la police sans du système, pour comparer.
 * Le choix est posé sur <html data-font="system"> et gardé dans le navigateur.
 * Un petit script dans <head> (docusaurus.config.js) le réapplique avant
 * l'affichage, pour éviter un flash de police au chargement.
 */
export const FONT_KEY = 'arkerion-font';

function apply(system) {
  const root = document.documentElement;
  if (system) root.dataset.font = 'system';
  else delete root.dataset.font;
  try {
    localStorage.setItem(FONT_KEY, system ? 'system' : 'arkerion');
  } catch (e) {
    /* stockage indisponible : le choix vaut pour cette page seulement */
  }
}

export default function FontToggle({ mobile, className }) {
  const [system, setSystem] = useState(false);

  useEffect(() => {
    setSystem(document.documentElement.dataset.font === 'system');
  }, []);

  const choose = (next) => {
    setSystem(next);
    apply(next);
  };

  return (
    <div
      role="group"
      aria-label="Police de la documentation"
      className={clsx(styles.toggle, mobile ? styles.mobile : 'navbar__item', className)}
    >
      <button
        type="button"
        className={clsx(styles.option, styles.arkerion, !system && styles.active)}
        aria-pressed={!system}
        title="Afficher la documentation en Arkerion Sans"
        onClick={() => choose(false)}
      >
        Arkerion
      </button>
      <button
        type="button"
        className={clsx(styles.option, styles.system, system && styles.active)}
        aria-pressed={system}
        title="Afficher la documentation dans la police de votre système"
        onClick={() => choose(true)}
      >
        Système
      </button>
    </div>
  );
}
