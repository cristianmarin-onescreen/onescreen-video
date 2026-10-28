// Mapa de tiempos de SC06 — «OneScreen Titan».
//
// Misma regla de marca que Core y T7: "OneScreen" en NEVIS, el modelo ("Titan") y
// todo lo demás en Rubik, con el modelo en caja mixta y peso regular.
//
// La locución ABRE con "OneScreen Titan." — el guion escrito no lo traía arriba —,
// así que la pieza gana un lockup de apertura además del de cierre.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 34.52;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Ortografía del guion; tiempos de la locución.
const FIX = {
  1: "Titan", 5: "más", 12: "tecnología", 17: "1.200", 25: "jamás", 26: "tendrás", 30: "salón",
  34: "Más", 49: "más", 50: "potente", 51: "(hasta", 52: "ahora)", 55: "65”",
  62: "Titan", 67: "¿Quieres", 72: "fácil.", 73: "Solo",
};
// "Mini" + "-LED." → una sola palabra; "1" + ".07" → una cifra; "86" + "pulgadas." → 86”
const MERGE = [[13, 14, "Mini-LED."], [36, 37, "1.07"], [57, 58, "86”"]];
const BRAND = new Set([0, 59]);   // las dos menciones de la marca → Nevis

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
  // Lockup de apertura.
  F("f01", [L(0, 0, "colossal"), L(1, 1, "mega", { regular: true, accent: true })]),
  F("f02", [L(2, 4, "sub"), L(5, 6, "mega", { caps: true })]),
  F("f03", [L(7, 12, "sub"), L(13, 13, "mega", { caps: true, accent: true })]),
  F("f04", [L(15, 16, "sub"), L(17, 18, "colossal", { caps: true, accent: true }), L(19, 20, "sub")]),
  F("f05", [L(21, 33, "display")]),
  F("f06", [L(34, 35, "sub"), L(36, 38, "colossal", { caps: true }), L(39, 43, "sub")]),
  // El guiño va PEQUEÑO: entre paréntesis y en el escalón menor es donde funciona.
  F("f07", [L(44, 50, "display"), L(51, 52, "sub", { accent: true })]),
  F("f08", [L(53, 54, "sub", { caps: true }), L(55, 57, "colossal", { accent: true })]),
  // Lockup de cierre.
  F("f09", [L(59, 59, "mega"), L(60, 60, "display", { regular: true })]),
  F("f10", [L(61, 66, "display")]),
  F("f11", [L(67, 70, "sub"), L(71, 72, "mega", { caps: true })]),
  F("f12", [L(73, 76, "sub"), L(77, 78, "mega", { caps: true, accent: true })]),
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
  source: "SC06.wav",
  speechEnd: 31.0,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`menciones de marca en Nevis: ${words.filter((w) => w.brand).length}\n`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
