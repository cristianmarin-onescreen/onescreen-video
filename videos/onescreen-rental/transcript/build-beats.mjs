// Mapa de tiempos de SC12 — «Rental / DaaS».
//
// Regla de marca: "OneScreen" en NEVIS (una mención, f02), todo lo demás en Rubik.
//
// Dos particularidades:
//   · "DaaS" NO va en versalitas — es un acrónimo de caja fija (Device as a Service) y
//     forzarlo a caja alta lo convierte en otra cosa. Mismo caso que "PhET" en la pieza
//     de Write.
//   · La pieza tiene DOS ordinales "Primero," que no significan lo mismo: el primero
//     abre los dos caminos de compra, el segundo abre la lista de ventajas. Los dos
//     llevan el tratamiento de ordinal (versalitas pequeñas + acento) para que se lean
//     como marcadores de lista y no como parte de la frase.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 40.36;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// La voz dice "SI quieres adquirir tu pantalla, preguntanos ACA"; el guion escrito
// omite el "Si" y el "acá". Manda la voz.
const FIX = { 3: "cómo", 53: "institución", 81: "Y" };
const MERGE = [];
const BRAND = new Set([12]);

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
  F("f01", [L(0, 2, "sub"), L(3, 7, "mega", { caps: true })]),
  F("f02", [L(8, 15, "sub"), L(16, 18, "mega", { caps: true, accent: true })]),
  F("f03", [L(19, 19, "sub", { caps: true, accent: true }), L(20, 21, "mega", { caps: true }), L(22, 29, "sub")]),
  // DaaS conserva su caja: no lleva `caps`.
  F("f04", [L(30, 31, "sub", { caps: true, accent: true }), L(32, 36, "sub"), L(37, 37, "colossal")]),
  F("f05", [L(38, 42, "sub"), L(43, 43, "mega", { caps: true, accent: true })]),
  F("f06", [L(44, 54, "sub"), L(55, 56, "mega", { caps: true })]),
  F("f07", [L(57, 59, "sub"), L(60, 62, "mega", { caps: true })]),
  F("f08", [L(63, 63, "sub", { caps: true, accent: true }), L(64, 69, "mega", { caps: true })]),
  F("f09", [L(70, 75, "sub"), L(76, 77, "mega", { caps: true })]),
  F("f10", [L(78, 80, "mega", { caps: true, accent: true })]),
  F("f11", [L(81, 87, "sub"), L(88, 90, "mega", { caps: true })]),
  F("f12", [L(91, 95, "sub"), L(96, 97, "mega", { caps: true, accent: true }), L(98, 101, "sub")]),
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
  source: "Rental - Narrador.wav",
  speechEnd: 40.1,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
