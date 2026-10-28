// Mapa de tiempos de SC09 — «OneScreen Wandr».
//
// Regla de marca de siempre: "OneScreen" en NEVIS, el modelo ("Wandr") y todo lo demás
// en Rubik, con el modelo en caja mixta y peso regular.
//
// SOBRE EL NOMBRE: la locución lo pronuncia a la inglesa y whisper oye "Wonder" en una
// pasada sin prompt. Se escribe "Wandr" — confirmado contra el disco de la empresa, que
// tiene una carpeta entera de producto con ese nombre (banners, video de unboxing,
// imagen de producto, proyectos de Premiere). No existe ningún "Wonder".
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 34.16;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Ortografía y puntuación del guion del usuario; tiempos de la locución.
const FIX = {
  0: "¿Si", 6: "OneScreen,", 9: "lugar?", 10: "Te", 13: "Wandr", 14: "El",
  19: "portátil.", 50: "Inclinarla", 61: "integrada,", 71: "Wandr", 80: "stand,",
};
// "180" + "grados," → "180°," (el guion usa el símbolo; la voz dice "grados", y el
// símbolo ES esa palabra). "One" + "Screen" → una sola pieza de marca.
const MERGE = [[48, 49, "180°,"], [69, 70, "OneScreen"]];
const BRAND = new Set([6, 12, 69]);

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
  // La pregunta de apertura se parte donde la parte el guion: el gancho va abajo y grande.
  F("f01", [L(0, 6, "sub"), L(7, 9, "mega", { caps: true, accent: true })]),
  F("f02", [L(10, 11, "sub"), L(12, 12, "mega"), L(13, 13, "mega", { regular: true })]),
  F("f03", [L(14, 18, "sub"), L(19, 19, "mega", { caps: true, accent: true })]),
  F("f04", [L(20, 27, "sub"), L(28, 31, "mega", { caps: true })]),
  F("f05", [L(32, 38, "sub"), L(39, 40, "colossal", { caps: true, accent: true }), L(41, 42, "sub")]),
  F("f06", [L(43, 47, "sub"), L(48, 48, "colossal", { accent: true })]),
  F("f07", [L(50, 56, "display")]),
  F("f08", [L(57, 58, "sub"), L(59, 60, "mega", { caps: true }), L(61, 68, "sub")]),
  // Lockup: marca en Nevis, modelo en Rubik regular.
  F("f09", [L(69, 69, "mega"), L(71, 71, "display", { regular: true }), L(72, 76, "sub")]),
  F("f10", [L(77, 80, "sub"), L(81, 83, "mega", { caps: true, accent: true })]),
  F("f11", [L(84, 85, "mega", { caps: true })]),
  F("f12", [L(86, 95, "display")]),
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
  source: "Wandr - Narrador.wav",
  speechEnd: 34.0,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`menciones de marca en Nevis: ${words.filter((w) => w.brand).length}\n`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
