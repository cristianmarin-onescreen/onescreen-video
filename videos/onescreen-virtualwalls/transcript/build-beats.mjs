// Mapa de tiempos de LED_1 — «VirtualWalls de OneScreen».
//
// Misma regla de marca: "OneScreen" en NEVIS, el modelo ("VirtualWalls") y todo lo
// demás en Rubik, con el modelo en caja mixta y peso regular.
//
// Aquí la marca va DETRÁS del modelo — "las VirtualWalls de OneScreen" —, así que
// "OneScreen" aparece EN LÍNEA dentro de una frase Rubik, no como línea propia.
//
// La última línea del guion escrito, "Ahora, sobre esta", NO está en la locución: la
// voz termina en "Solo toca esta pantalla." a los 18.96 s. No se letra.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 19.28;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

const FIX = { 24: "108”", 38: "también.", 39: "¿Quieres", 41: "más" };
const MERGE = [[26, 27, "217”"]];
const BRAND = new Set([22]);   // la única mención de la marca → Nevis

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

// Las versalitas de "MUY GRANDE" y "GIGANTE" vienen del propio guion, que las escribe
// en caja alta: es una instrucción de énfasis del cliente, no una decisión mía.
const FRAMES = [
  F("f01", [L(0, 5, "sub"), L(6, 6, "mega", { caps: true })]),
  F("f02", [L(7, 7, "sub"), L(8, 9, "colossal", { caps: true })]),
  F("f03", [L(10, 15, "sub"), L(16, 16, "colossal", { caps: true, accent: true })]),
  // El modelo en su propia línea; la marca en línea dentro de la frase que la sigue.
  F("f04", [L(17, 19, "sub"), L(20, 20, "mega", { regular: true }), L(21, 22, "display")]),
  F("f05", [L(23, 23, "sub", { caps: true }), L(24, 26, "colossal", { accent: true })]),
  F("f06", [L(28, 29, "sub"), L(30, 30, "colossal", { caps: true })]),
  F("f07", [L(31, 35, "sub"), L(36, 38, "mega", { caps: true })]),
  F("f08", [L(39, 43, "sub"), L(44, 44, "mega", { caps: true })]),
  F("f09", [L(45, 46, "sub"), L(47, 48, "mega", { caps: true, accent: true })]),
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
  source: "LED_1.wav",
  speechEnd: 19.0,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`menciones de marca en Nevis: ${words.filter((w) => w.brand).length}\n`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
