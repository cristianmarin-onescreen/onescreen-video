// Mapa de tiempos de SC08 — «OneScreen Gurú».
//
// Regla de marca: "OneScreen" en NEVIS (cuatro menciones), el nombre del servicio
// ("Gurú") y todo lo demás en Rubik, con el nombre en caja mixta y peso regular.
//
// Esta pieza es la que más veces nombra la marca de las diez, y una de esas veces cae
// DENTRO de una línea en versalitas. El guard `text-transform: none !important` de la
// clase .brand es lo que impide que el wordmark salga como "ONESCREEN".
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 27.04;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Ortografía del guion; tiempos de la locución. La voz dice "a UN SOLO click" y el
// guion escribe "a SOLO UN click": manda la voz.
const FIX = {
  20: "institución.", 24: "Te", 27: "Gurú.", 34: "botón", 36: "Gurú,",
  38: "podrás", 43: "click,", 60: "cómo", 64: "sencillo.",
};
const MERGE = [[22, 23, "24/5."]];
const BRAND = new Set([11, 26, 31, 48]);

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
  F("f01", [L(0, 2, "sub"), L(3, 5, "mega", { caps: true })]),
  F("f02", [L(6, 14, "sub"), L(15, 16, "mega", { caps: true, accent: true }), L(17, 20, "sub")]),
  F("f03", [L(21, 21, "sub", { caps: true }), L(22, 22, "colossal", { accent: true })]),
  // Lockup del servicio.
  // El nombre del servicio va en verde, igual que el azul marcaba el modelo en Core,
  // T7 y Titan. Aqui el color ES la identidad del producto.
  F("f04", [L(24, 25, "sub"), L(26, 26, "mega"), L(27, 27, "mega", { regular: true, accent: true })]),
  // "el boton verde Guru" en verde: es literalmente el nombre del boton.
  F("f05", [L(28, 32, "sub"), L(33, 36, "mega", { caps: true, accent: true })]),
  F("f06", [L(37, 43, "sub"), L(44, 46, "mega", { caps: true }), L(47, 51, "sub")]),
  F("f07", [L(52, 53, "sub"), L(54, 54, "mega", { caps: true }), L(55, 58, "sub")]),
  F("f08", [L(59, 62, "sub"), L(63, 64, "mega", { caps: true, accent: true })]),
  F("f09", [L(65, 68, "sub"), L(69, 70, "mega", { caps: true, accent: true })]),
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
  source: "Gurú - Final.wav",
  speechEnd: 26.8,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`menciones de marca en Nevis: ${words.filter((w) => w.brand).length}\n`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
