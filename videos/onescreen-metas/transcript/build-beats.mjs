// Mapa de tiempos de SC03 — «Nuestras metas».
//
// Texto: el guion escrito del usuario. Tiempos: los reales de la locución (whisper
// large-v3-turbo), cuantizados a 25 fps para entrar directo en su timeline.
//
// La composición tipográfica está escrita a mano cuadro por cuadro, no derivada de
// la puntuación, porque el estilo del cliente (visto en SC01/SC02) pide tres escalas
// dentro de un mismo cuadro, versalitas en la palabra héroe y pesos mezclados en la
// misma línea. Eso no sale de un algoritmo de corte; sale de decidir qué carga cada
// verso.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 58.28;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);
const r6 = (n) => Math.round(n * 1e6) / 1e6;

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Correcciones de ortografía sobre lo que oyó whisper. El guion manda para cómo se
// escribe; la locución manda para cuándo aparece.
//   47 "en"   — el guion lo omite pero la voz lo dice; se conserva.
//   58 "se"   — la voz es ambigua; "le tomaba" es lo correcto y lo que dice el guion.
//   66 "solo" — el guion lo omite pero la voz lo dice; se conserva.
//   119 "Y"   — idem, antes de "quinto".
//   106 "LED" — SE AÑADE. El guion dice "Pantallas LED de gran formato" y es un claim
//               de producto. Una pasada sin prompt NO lo detecta en el audio, así que
//               puede que la voz no lo diga: queda señalado al usuario. Hereda el
//               tiempo de "Pantallas" para no inventar un timestamp.
const FIX = { 10: "¿Estás", 43: "más", 58: "le", 59: "tomaba", 77: "Tus", 90: "graaaaaande.", 114: "Desde", 124: "Que" };
const MERGE = [[117, 118, '217".']];   // "217" + "pulgadas." → 217" (comilla de pulgada)
const INSERT_AFTER = { 106: "LED" };

const merged = new Set(MERGE.map(([, b]) => b));
const mergeStart = new Map(MERGE.map(([a, b, text]) => [a, { b, text }]));

const words = [];
for (let i = 0; i < raw.length; i++) {
  if (merged.has(i)) continue;
  const m = mergeStart.get(i);
  const start = snap(raw[i].start, -1);
  let end = snap(m ? raw[m.b].end : raw[i].end, 1);
  if (end <= start) end = snap(start + FRAME, 0);
  let text = m ? m.text : FIX[i] ?? raw[i].text;
  if (i === 115) text = '108"';
  words.push({ i: words.length, src: i, text, start, end });
  const extra = INSERT_AFTER[i];
  if (extra) {
    // Palabra añadida del guion: comparte ventana con la anterior, medio frame después.
    words.push({ i: words.length, src: -1, text: extra, start: snap(start + FRAME, 0), end });
  }
}

const bySrc = new Map();
for (const w of words) if (w.src >= 0) bySrc.set(w.src, w);
const idx = (src) => bySrc.get(src).i;
const span = (a, b) => words.filter((w) => w.i >= idx(a) && w.i <= idx(b));

// ---------------------------------------------------------------------------
// COMPOSICIÓN. Cada cuadro es una lista de líneas; cada línea declara su escalón,
// si va en versalitas, su peso y si lleva el acento azul.
//   scale:  micro | sub | phrase | display | mega | colossal
//   caps:   true → text-transform uppercase + tracking abierto
//   accent: true → toda la línea en #3976ff (se usa en los ordinales)
const F = (id, lines, opts = {}) => ({ id, lines, ...opts });
const L = (a, b, scale, o = {}) => ({ from: a, to: b, scale, ...o });

const FRAMES = [
  // ---- intro -------------------------------------------------------------
  F("i1", [L(0, 4, "phrase")]),
  F("i2", [L(5, 9, "display")]),
  F("i3", [L(10, 11, "mega", { caps: true })]),

  // ---- 1 · aulas interactivas -------------------------------------------
  F("h1", [L(12, 12, "sub", { caps: true, accent: true }), L(13, 14, "mega", { caps: true })], { chapter: true }),
  F("c1a", [L(15, 18, "sub"), L(19, 20, "display", { caps: true })]),
  F("c1b", [L(21, 22, "display"), L(23, 24, "display")]),

  // ---- 2 · salas de reuniones -------------------------------------------
  F("h2", [L(25, 25, "sub", { caps: true, accent: true }), L(26, 28, "mega", { caps: true })], { chapter: true }),
  F("c2a", [L(29, 31, "sub"), L(32, 36, "display", { caps: true })]),
  F("c2b", [L(37, 38, "display"), L(39, 40, "display")]),
  F("c2c", [L(41, 44, "display"), L(45, 51, "sub")]),

  // ---- 3 · inteligencia artificial --------------------------------------
  F("h3", [L(52, 52, "sub", { caps: true, accent: true }), L(53, 54, "mega", { caps: true })], { chapter: true }),
  F("c3a", [L(55, 62, "sub"), L(63, 64, "display", { caps: true })]),
  F("c3b", [L(65, 68, "sub"), L(69, 70, "display", { caps: true, accent: true })]),
  F("c3c", [L(71, 76, "display")]),
  F("c3d", [L(77, 81, "display")]),
  F("c3e", [L(82, 86, "display")]),

  // ---- 4 · formato grande ------------------------------------------------
  F("h4", [L(87, 87, "sub", { caps: true, accent: true }), L(88, 89, "sub"), L(90, 90, "colossal", { caps: true })], { chapter: true }),
  F("c4a", [L(91, 93, "sub"), L(94, 96, "display", { caps: true })]),
  F("c4b", [L(97, 101, "sub"), L(102, 105, "display", { caps: true })]),
  F("c4c", [L(106, 109, "display"), L(110, 113, "sub")]),
  F("c4d", [L(114, 114, "sub", { caps: true }), L(115, 117, "colossal")]),

  // ---- 5 · la más importante --------------------------------------------
  F("h5", [L(119, 120, "sub", { caps: true, accent: true }), L(121, 123, "mega", { caps: true })], { chapter: true }),
  F("c5a", [L(124, 131, "display")]),
  F("c5b", [L(132, 135, "sub"), L(136, 137, "mega", { caps: true, accent: true })]),
];

// Resuelve índices SRC → palabras reales, y calcula ventanas.
const built = FRAMES.map((f, n) => {
  const lines = f.lines.map((l) => {
    const ws = span(l.from, l.to);
    return {
      scale: l.scale,
      caps: !!l.caps,
      accent: !!l.accent,
      text: ws.map((w) => w.text).join(" "),
      words: ws.map((w) => ({ id: `w${w.i}`, i: w.i, text: w.text, start: w.start })),
    };
  });
  const all = lines.flatMap((l) => l.words);
  return {
    id: f.id,
    chapter: !!f.chapter,
    start: all[0].start,
    lines,
    text: lines.map((l) => l.text).join(" / "),
  };
});

// La salida de un cuadro es la entrada del siguiente; el último aguanta hasta la cola.
built.forEach((f, n) => {
  const next = built[n + 1];
  f.end = next ? snap(next.start - FRAME, -1) : snap(TOTAL, 0);
});

const out = {
  fps: FPS,
  format: "3840x2160",
  totalDuration: snap(TOTAL, 0),
  totalFrames: frames(snap(TOTAL, 0)),
  source: "SC03.wav",
  speechEnd: 53.6,
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
for (const f of built) {
  const mark = f.chapter ? "▌" : " ";
  console.log(`${mark} ${f.id.padEnd(5)} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
}
