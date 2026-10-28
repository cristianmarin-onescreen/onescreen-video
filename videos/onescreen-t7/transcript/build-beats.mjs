// Mapa de tiempos de SC05 — «OneScreen T7».
//
// Misma regla de marca que la pieza Core: "OneScreen" en NEVIS, el modelo ("T7") y
// todo lo demás en Rubik. El modelo va en caja mixta y peso regular.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 27.84;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Ortografía según el guion; los tiempos son los de la locución.
// Nota sobre el orden: el guion pone "(6 Billones…)" como paréntesis del NPU y "O sea,"
// al inicio de la frase de la Core. La VOZ lo dice al revés — "…de IA. O sea, 6 billones
// de operaciones por segundo." — y el lettering sigue a la voz.
const FIX = {
  1: "T7", 7: "65”", 18: "micrófonos", 23: "Cámara", 37: "billones",
  44: "táctiles.", 45: "Todo", 55: "aún", 64: "educación.",
};
const MERGE = [[9, 10, "105”"]];
const BRAND = new Set([0, 57]);   // las dos menciones de la marca → Nevis

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
  // Lockup de apertura: marca en Nevis, modelo en Rubik regular.
  F("f01", [L(0, 0, "colossal"), L(1, 1, "mega", { regular: true, accent: true })]),
  F("f02", [L(2, 4, "display")]),
  F("f03", [L(5, 6, "sub", { caps: true }), L(7, 9, "colossal", { accent: true })]),
  F("f04", [L(11, 12, "mega", { caps: true, accent: true }), L(13, 16, "sub")]),
  F("f05", [L(17, 18, "mega", { caps: true }), L(19, 22, "sub")]),
  F("f06", [L(23, 24, "mega", { caps: true }), L(25, 27, "sub")]),
  F("f07", [L(28, 29, "mega", { caps: true }), L(30, 33, "sub")]),
  F("f08", [L(34, 35, "sub"), L(36, 37, "colossal", { caps: true, accent: true }), L(38, 41, "sub")]),
  F("f09", [L(42, 44, "mega", { caps: true })]),
  F("f10", [L(45, 53, "sub"), L(54, 56, "mega", { caps: true })]),
  // Lockup de cierre.
  F("f11", [L(57, 57, "mega"), L(58, 58, "display", { regular: true }), L(59, 64, "sub")]),
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
  source: "SC05.wav",
  speechEnd: 27.1,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`menciones de marca en Nevis: ${words.filter((w) => w.brand).length}\n`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
