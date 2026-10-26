import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import clsx from 'clsx';
import styles from './EditorDemo.module.css';

/* Éditeur de code de démonstration, fait maison, en Arkerion Mono.
   Principe : un <textarea> au texte transparent posé exactement sur un <pre>
   coloré. Les deux partagent la même police, la même taille et la même hauteur
   de ligne : la colonne des numéros, la bande de la ligne active et le texte
   tombent ainsi sur la même grille, ligne par ligne.
   Le curseur natif est masqué : un curseur maison est placé par calcul
   (ligne × hauteur de ligne, colonne × largeur d'un caractère, police à chasse
   fixe), sans animation de déplacement, donc sans latence. */

const EXEMPLE = `// Arkerion Mono : chiffres, ponctuation et ligatures de code
type Glyphe = { nom: string; chasse: number };

const glyphes: Glyphe[] = [
  { nom: "G", chasse: 750 },
  { nom: "O", chasse: 800 },
  { nom: "y", chasse: 504 },
];

export function plusLarge(liste: Glyphe[]): Glyphe | null {
  if (liste.length === 0) return null;
  return liste.reduce((a, b) => (b.chasse >= a.chasse ? b : a));
}

const total = glyphes.map((g) => g.chasse).reduce((a, b) => a + b, 0);
console.log(\`Chasse totale : \${total}\`); // 2054
`;

const KEYWORDS = new Set(
  'const let var function return if else for while of in export import from type interface new null undefined true false class extends await async'.split(' '),
);

// Coloration minimale : commentaires, chaînes, nombres, mots-clés, types, appels.
const TOKEN = /(\/\/.*)|(`(?:\\.|[^`\\])*`?|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/g;

function highlight(line) {
  const out = [];
  let last = 0;
  let m;
  TOKEN.lastIndex = 0;
  while ((m = TOKEN.exec(line))) {
    if (m.index > last) out.push([null, line.slice(last, m.index)]);
    const [text, comment, string, number, word] = m;
    let kind = null;
    if (comment) kind = 'comment';
    else if (string) kind = 'string';
    else if (number) kind = 'number';
    else if (word) {
      if (KEYWORDS.has(word)) kind = 'keyword';
      else if (/^[A-Z]/.test(word)) kind = 'type';
      else if (line[m.index + word.length] === '(') kind = 'fn';
    }
    out.push([kind, text]);
    last = m.index + text.length;
  }
  if (last < line.length) out.push([null, line.slice(last)]);
  return out;
}

const TAB = 2;

// Ligne et colonne visuelle (tabulations développées) d'un index du texte.
function caretPosition(text, index) {
  const before = text.slice(0, index);
  const start = before.lastIndexOf('\n') + 1;
  const line = before.split('\n').length - 1;
  let col = 0;
  for (const ch of before.slice(start)) col = ch === '\t' ? (Math.floor(col / TAB) + 1) * TAB : col + 1;
  return { line, col };
}

export default function EditorDemo({ initial = EXEMPLE, filename = 'glyphes.ts' }) {
  const [code, setCode] = useState(initial.replace(/\n$/, ''));
  const [pos, setPos] = useState({ line: 0, col: 0 });
  const [tick, setTick] = useState(0);          // relance le clignotement à chaque déplacement
  const [focused, setFocused] = useState(false);
  const [ligatures, setLigatures] = useState(true);
  const [full, setFull] = useState(false);
  const [cw, setCw] = useState(0);              // largeur d'un caractère, en px
  const root = useRef(null);
  const area = useRef(null);
  const probe = useRef(null);
  const caret = useRef(null);

  const lines = useMemo(() => code.split('\n'), [code]);

  const sync = useCallback(() => {
    const el = area.current;
    if (!el) return;
    const i = el.selectionDirection === 'backward' ? el.selectionStart : el.selectionEnd;
    const next = caretPosition(el.value, i);
    setPos((p) => (p.line === next.line && p.col === next.col ? p : next));
    setTick((t) => t + 1);
  }, []);

  // Largeur d'un caractère : mesurée sur 100 caractères, puis remesurée une
  // fois la police chargée et à chaque changement de taille.
  useLayoutEffect(() => {
    const measure = () => probe.current && setCw(probe.current.getBoundingClientRect().width / 100);
    measure();
    document.fonts?.ready.then(measure);
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, [full]);

  // Sélection : l'événement natif suit les flèches maintenues et la souris.
  useEffect(() => {
    const onSel = () => document.activeElement === area.current && sync();
    document.addEventListener('selectionchange', onSel);
    return () => document.removeEventListener('selectionchange', onSel);
  }, [sync]);

  // Garde le curseur visible quand il sort de la zone (défilement).
  useEffect(() => {
    if (focused && caret.current) caret.current.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }, [pos, focused]);

  // Plein écran : API native si elle existe, sinon un calque fixe.
  useEffect(() => {
    const onChange = () => setFull(document.fullscreenElement === root.current);
    document.addEventListener('fullscreenchange', onChange);
    return () => document.removeEventListener('fullscreenchange', onChange);
  }, []);

  useEffect(() => {
    if (!full || document.fullscreenElement) return undefined;
    const onKey = (e) => e.key === 'Escape' && setFull(false);
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [full]);

  const toggleFull = () => {
    const el = root.current;
    if (document.fullscreenElement) document.exitFullscreen();
    else if (el.requestFullscreen) el.requestFullscreen().catch(() => setFull((v) => !v));
    else setFull((v) => !v);
    requestAnimationFrame(() => area.current?.focus());
  };

  const onKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const el = e.currentTarget;
      const { selectionStart: s, selectionEnd: t, value } = el;
      setCode(value.slice(0, s) + ' '.repeat(TAB) + value.slice(t));
      requestAnimationFrame(() => {
        el.selectionStart = el.selectionEnd = s + TAB;
        sync();
      });
      return;
    }
    requestAnimationFrame(sync);                 // flèches, Début, Fin : dès la frame suivante
  };

  return (
    <figure ref={root} className={clsx(styles.editor, !ligatures && styles.noLig, full && styles.full)}>
      <div className={styles.bar}>
        <span className={styles.tab}>
          <span className={styles.dot} aria-hidden="true" />
          {filename}
        </span>
        <span className={styles.actions}>
          <button
            type="button"
            className={styles.toggle}
            aria-pressed={ligatures}
            onClick={() => setLigatures((v) => !v)}>
            Ligatures {ligatures ? 'activées' : 'désactivées'}
          </button>
          <button
            type="button"
            className={styles.toggle}
            aria-pressed={full}
            title={full ? 'Quitter le plein écran (Échap)' : 'Plein écran'}
            onClick={toggleFull}>
            <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.4">
              {full ? <path d="M4.5 1v3.5H1M7.5 1v3.5H11M4.5 11V7.5H1M7.5 11V7.5H11" /> : <path d="M1 4.5V1h3.5M11 4.5V1H7.5M1 7.5V11h3.5M11 7.5V11H7.5" />}
            </svg>
            {full ? 'Quitter' : 'Plein écran'}
          </button>
        </span>
      </div>

      <div className={styles.body} onMouseDown={(e) => {
        // Clic sous la dernière ligne : curseur en fin de texte.
        if (e.target === e.currentTarget) {
          e.preventDefault();
          const el = area.current;
          el.focus();
          el.selectionStart = el.selectionEnd = el.value.length;
          sync();
        }
      }}>
        <div
          className={clsx(styles.band, focused && styles.bandFocus)}
          style={{ transform: `translateY(calc(${pos.line} * var(--ed-lh)))` }}
          aria-hidden="true"
        />
        <ol className={styles.gutter} aria-hidden="true">
          {lines.map((_, i) => (
            <li key={i} className={clsx(i === pos.line && styles.numActive)}>
              {i + 1}
            </li>
          ))}
        </ol>
        <div className={styles.scroller}>
          <div className={styles.stack}>
            <span ref={probe} className={styles.probe} aria-hidden="true">
              {'0'.repeat(100)}
            </span>
            <pre className={styles.code} aria-hidden="true">
              {lines.map((l, i) => (
                <span key={i} className={styles.line}>
                  {highlight(l).map(([kind, text], j) =>
                    kind ? (
                      <span key={j} className={styles[kind]}>
                        {text}
                      </span>
                    ) : (
                      text
                    ),
                  )}
                  {'\n'}
                </span>
              ))}
            </pre>
            <textarea
              ref={area}
              className={styles.input}
              value={code}
              rows={lines.length}
              wrap="off"
              spellCheck={false}
              autoCapitalize="off"
              autoComplete="off"
              autoCorrect="off"
              aria-label={`Éditeur de démonstration, fichier ${filename}`}
              onChange={(e) => {
                setCode(e.target.value);
                setPos(caretPosition(e.target.value, e.target.selectionEnd));
                setTick((t) => t + 1);
              }}
              onKeyDown={onKeyDown}
              onSelect={sync}
              onFocus={() => {
                setFocused(true);
                sync();
              }}
              onBlur={() => setFocused(false)}
            />
            {focused && cw > 0 && (
              <span
                key={tick}
                ref={caret}
                className={styles.caret}
                style={{ transform: `translate(${pos.col * cw}px, calc(${pos.line} * var(--ed-lh)))` }}
                aria-hidden="true"
              />
            )}
          </div>
        </div>
      </div>

      <figcaption className={styles.status}>
        <span>
          Ln {pos.line + 1}, Col {pos.col + 1}
        </span>
        <span className={styles.statusRight}>
          <span>{lines.length} lignes</span>
          <span>TypeScript</span>
          <span>Arkerion Mono</span>
        </span>
      </figcaption>
    </figure>
  );
}
