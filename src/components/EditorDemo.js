import React, { useMemo, useRef, useState } from 'react';
import clsx from 'clsx';
import styles from './EditorDemo.module.css';

/* Éditeur de code de démonstration, fait maison, en Arkerion Mono.
   Principe : un <textarea> au texte transparent posé exactement sur un <pre>
   coloré. Les deux partagent la même police, la même taille et la même hauteur
   de ligne : la colonne des numéros, la bande de la ligne active et le texte
   tombent ainsi sur la même grille, ligne par ligne. */

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

function caretPosition(text, index) {
  const before = text.slice(0, index);
  const line = before.split('\n').length - 1;
  const col = index - (before.lastIndexOf('\n') + 1);
  return { line, col };
}

export default function EditorDemo({ initial = EXEMPLE, filename = 'glyphes.ts' }) {
  const [code, setCode] = useState(initial.replace(/\n$/, ''));
  const [pos, setPos] = useState({ line: 0, col: 0 });
  const [focused, setFocused] = useState(false);
  const [ligatures, setLigatures] = useState(true);
  const area = useRef(null);

  const lines = useMemo(() => code.split('\n'), [code]);

  const sync = () => {
    const el = area.current;
    if (el) setPos(caretPosition(el.value, el.selectionStart));
  };

  const onKeyDown = (e) => {
    if (e.key !== 'Tab') return;
    e.preventDefault();
    const el = e.currentTarget;
    const { selectionStart: s, selectionEnd: t, value } = el;
    const next = value.slice(0, s) + '  ' + value.slice(t);
    setCode(next);
    requestAnimationFrame(() => {
      el.selectionStart = el.selectionEnd = s + 2;
      sync();
    });
  };

  return (
    <figure className={clsx(styles.editor, !ligatures && styles.noLig)}>
      <div className={styles.bar}>
        <span className={styles.tab}>
          <span className={styles.dot} aria-hidden="true" />
          {filename}
        </span>
        <button
          type="button"
          className={styles.toggle}
          aria-pressed={ligatures}
          onClick={() => setLigatures((v) => !v)}>
          Ligatures {ligatures ? 'activées' : 'désactivées'}
        </button>
      </div>

      <div className={styles.body}>
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
                setPos(caretPosition(e.target.value, e.target.selectionStart));
              }}
              onKeyDown={onKeyDown}
              onKeyUp={sync}
              onClick={sync}
              onSelect={sync}
              onFocus={() => {
                setFocused(true);
                sync();
              }}
              onBlur={() => setFocused(false)}
            />
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
          <span>Arkerion Mono 15 px</span>
        </span>
      </figcaption>
    </figure>
  );
}
