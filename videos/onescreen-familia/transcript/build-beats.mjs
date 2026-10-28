// Mapa de tiempos de SC04 — «La familia OneScreen».
//
// Texto del guion del usuario, tiempos reales de la locución, cuantizados a 25 fps.
//
// REGLA DE MARCA de esta pieza: cada vez que aparece "OneScreen" se compone en
// NEVIS; el nombre del modelo ("Core") va en Rubik. Las palabras marcadas con
// `brand: true` son las que el generador tipografía en Nevis.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 46.88;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Ortografía según el guion. Las comillas de pulgada son las del guion (”), no ".
const FIX = {
  // "Core," arrastraba la coma de la transcripción; en un lockup de producto sobra.
  30: "Core",
  37: "65”", 53: "más", 64: "¿Cómo", 67: "Fácil.", 74: "1.", 75: "Encenderla.",
  77: "2.", 78: "Usarla.", 89: "Hardware.",
};
// 39 "110" + 40 "pulgadas." → 110” ; 103 "One" + 104 "Screen" → OneScreen
const MERGE = [[39, 40, "110”"], [103, 104, "OneScreen"]];
// Palabras que van en Nevis: las cuatro menciones de la marca.
const BRAND = new Set([11, 15, 29, 103]);

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

// ---------------------------------------------------------------------------
// COMPOSICIÓN. scale: sub | phrase | display | mega | colossal
// caps: versalitas · accent: azul (en la variante blanca se ignora y va todo blanco)
const F = (id, lines) => ({ id, lines });
const L = (a, b, scale, o = {}) => ({ from: a, to: b, scale, ...o });

const FRAMES = [
  F("f01", [L(0, 7, "phrase")]),
  F("f02", [L(8, 10, "sub"), L(11, 11, "mega")]),
  F("f03", [L(12, 14, "sub"), L(15, 15, "mega")]),
  F("f04", [L(16, 17, "mega", { caps: true }), L(18, 20, "sub")]),
  F("f05", [L(21, 21, "mega", { caps: true })]),
  F("f06", [L(22, 24, "mega", { caps: true })]),
  F("f07", [L(25, 28, "display")]),
  // Cuadro producto: marca en Nevis, modelo en Rubik. El corazón de la pieza.
  // El modelo va en caja mixta y peso regular: es un nombre propio, no un titular.
  F("f08", [L(29, 29, "colossal"), L(30, 30, "mega", { regular: true, accent: true })]),
  F("f09", [L(31, 34, "display")]),
  F("f10", [L(35, 36, "sub", { caps: true }), L(37, 39, "colossal", { accent: true })]),
  F("f11", [L(41, 45, "display")]),
  F("f12", [L(46, 47, "mega", { caps: true, accent: true }), L(48, 50, "sub")]),
  F("f13", [L(51, 54, "sub"), L(55, 56, "colossal", { caps: true }), L(57, 58, "sub")]),
  F("f14", [L(59, 63, "display")]),
  F("f15", [L(64, 66, "sub"), L(67, 67, "mega", { caps: true })]),
  F("f16", [L(68, 72, "display")]),
  F("f17", [L(73, 74, "mega", { caps: true, accent: true }), L(75, 75, "display")]),
  F("f18", [L(76, 77, "mega", { caps: true, accent: true }), L(78, 78, "display")]),
  F("f19", [L(79, 84, "display")]),
  F("f20", [L(85, 88, "sub"), L(89, 89, "mega", { caps: true })]),
  F("f21", [L(90, 92, "sub"), L(93, 93, "mega", { caps: true })]),
  F("f22", [L(94, 95, "sub"), L(96, 97, "mega", { caps: true })]),
  F("f23", [L(98, 100, "sub"), L(101, 102, "mega", { caps: true })]),
  F("f24", [L(103, 103, "mega"), L(105, 105, "display", { regular: true }), L(106, 113, "sub")]),
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
  source: "SC04.wav",
  speechEnd: 44.0,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
const brandCount = words.filter((w) => w.brand).length;
console.log(`menciones de marca en Nevis: ${brandCount}\n`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
