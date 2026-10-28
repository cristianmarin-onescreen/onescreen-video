// Mapa de tiempos de SC10 — «OneScreen Academy».
//
// Regla de marca de siempre: "OneScreen" en NEVIS, el nombre del producto ("Academy")
// y todo lo demás en Rubik, con el producto en caja mixta y peso regular.
// Academy no es un modelo de pantalla sino una plataforma, pero estructuralmente es el
// mismo patrón marca + nombre y se compone igual.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 31.52;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Ortografía del guion; tiempos de la locución. La voz dice "Solo tienes que tocar
// esta pantalla" y el guion escribe "Solo toca esta pantalla": manda la voz.
const FIX = {
  2: "estás", 4: "¿esto", 12: "Sí,", 21: "tecnológica", 41: "podrá",
  47: "Encontrarás", 60: "E", 64: "podrá", 76: "¿Quieres", 78: "cómo?",
};
const MERGE = [];
const BRAND = new Set([32, 46]);   // las dos menciones de la marca → Nevis

const merged = new Set(MERGE.map(([, b]) => b));
const mergeStart = new Map(MERGE.map(([a, b, text]) => [a, { b, text }]));

const words = [];
for (let i = 0; i < raw.length; i++) {
  if (merged.has(i)) continue;
  const m = mergeStart.get(i);
  const start = snap(raw[i].start, -1);
  let end = snap(m ? raw[m.b].end : raw[i].end, 1);
  if (end <= start) end = snap(start + FRAME, 0);
  words.push({
    i: words.length,
    src: i,
    text: m ? m.text : FIX[i] ?? raw[i].text,
    start,
    end,
    brand: BRAND.has(i),
  });
}

const bySrc = new Map(words.map((w) => [w.src, w]));
const idx = (src) => bySrc.get(src).i;
const span = (a, b) => words.filter((w) => w.i >= idx(a) && w.i <= idx(b));

const F = (id, lines) => ({ id, lines });
const L = (a, b, scale, o = {}) => ({ from: a, to: b, scale, ...o });

const FRAMES = [
  F("f01", [L(0, 3, "display")]),
  F("f02", [L(4, 9, "sub"), L(10, 11, "mega", { caps: true, accent: true })]),
  // "SÍ," solo y grande: es la respuesta a la objeción y merece su propio golpe.
  F("f03", [L(12, 12, "colossal", { caps: true }), L(13, 18, "sub")]),
  F("f04", [L(19, 23, "sub"), L(24, 28, "mega", { caps: true })]),
  // Lockup del producto.
  F("f05", [L(29, 31, "sub"), L(32, 32, "mega"), L(33, 33, "mega", { regular: true })]),
  F("f06", [L(34, 41, "sub"), L(42, 42, "colossal", { caps: true, accent: true }), L(43, 46, "sub")]),
  F("f07", [L(47, 54, "sub"), L(55, 59, "display")]),
  F("f08", [L(60, 68, "sub"), L(69, 70, "mega", { caps: true, accent: true })]),
  F("f09", [L(71, 75, "mega", { caps: true })]),
  F("f10", [L(76, 78, "mega", { caps: true })]),
  F("f11", [L(79, 82, "sub"), L(83, 84, "mega", { caps: true, accent: true })]),
];

const built = FRAMES.map((f) => {
  const lines = f.lines.map((l) => {
    const ws = span(l.from, l.to);
    return {
      scale: l.scale,
      caps: !!l.caps,
      accent: !!l.accent,
      regular: !!l.regular,
      text: ws.map((w) => w.text).join(" "),
      words: ws.map((w) => ({ id: `w${w.i}`, i: w.i, text: w.text, start: w.start, brand: w.brand })),
    };
  });
  return { id: f.id, start: lines[0].words[0].start, lines, text: lines.map((l) => l.text).join(" / ") };
});

built.forEach((f, n) => {
  const next = built[n + 1];
  f.end = next ? snap(next.start - FRAME, -1) : snap(TOTAL, 0);
});

const out = {
  fps: FPS,
  format: "3840x2160",
  totalDuration: snap(TOTAL, 0),
  totalFrames: frames(snap(TOTAL, 0)),
  source: "OneScreen Academy - Narrador.wav",
  speechEnd: 31.3,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`menciones de marca en Nevis: ${words.filter((w) => w.brand).length}\n`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
