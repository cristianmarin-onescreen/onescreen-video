// Mapa de tiempos de SC11 — «OneScreen Write».
//
// Regla de marca: "OneScreen" en NEVIS, todo lo demás en Rubik.
//
// OJO: esta locución NUNCA nombra el producto. Ni "Write" ni el lockup aparecen en el
// audio ni en el guion escrito — el nombre solo existe en la ruta del archivo. No se
// inventa texto: la capa dice exactamente lo que dice la voz. Si hace falta un lockup
// de cierre, hay que grabarlo o ponerlo en el montaje.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 22.4;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// Ortografía. La voz dice "Herramientas como DIFERENTES trazos"; el guion escrito pone
// "Herramientas cómo, TODOS LOS trazos". Manda la voz — y de paso el "cómo" del guion
// llevaba tilde por error: ahí es comparativo, no interrogativo.
const FIX = { 4: "pero,", 5: "¿y", 23: "periódica", 32: "Corrección", 43: "este," };
const MERGE = [];
const BRAND = new Set([11]);   // única mención de la marca → Nevis

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

// Cuadros que van sobre el tablero en pantalla: ahi el texto se comporta como
// subtitulo en el tercio inferior en vez de lettering centrado, que taparia justo la
// herramienta que se esta ensenando. Arranca en la lista de herramientas y termina en
// el remate del recorrido; el gancho de apertura y la llamada final siguen a pantalla
// completa.
const LOWER = new Set(["f03","f04","f05","f06","f07","f08"]);

const F = (id, lines) => ({ id, lines });
const L = (a, b, scale, o = {}) => ({ from: a, to: b, scale, ...o });

const FRAMES = [
  F("f01", [L(0, 3, "sub"), L(4, 7, "mega", { caps: true, accent: true })]),
  F("f02", [L(8, 13, "sub"), L(14, 16, "mega", { caps: true })]),
  F("f03", [L(17, 18, "sub"), L(19, 20, "mega", { caps: true })]),
  F("f04", [L(21, 21, "sub"), L(22, 23, "mega", { caps: true }), L(24, 24, "sub")]),
  F("f05", [L(25, 27, "mega", { caps: true })]),
  // PhET NO va en versalitas: es un nombre propio con caja fija, forzarlo lo desfigura.
  F("f06", [L(28, 30, "sub"), L(31, 31, "mega")]),
  F("f07", [L(32, 34, "mega", { caps: true, accent: true })]),
  F("f08", [L(35, 39, "sub"), L(40, 41, "mega", { caps: true })]),
  F("f09", [L(42, 47, "sub"), L(48, 48, "mega", { caps: true, accent: true })]),
  F("f10", [L(49, 52, "sub"), L(53, 54, "mega", { caps: true, accent: true })]),
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
  return { id: f.id, lower: LOWER.has(f.id), start: lines[0].words[0].start, lines, text: lines.map((l) => l.text).join(" / ") };
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
  source: "OneScreen Write - Narrador.wav",
  speechEnd: 22.2,
  brandTracking: "-0.050em",
  frames: built,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`menciones de marca en Nevis: ${words.filter((w) => w.brand).length}\n`);
console.log(`subtitulo en tercio inferior: ${built.filter((f) => f.lower).length} cuadros
`);
for (const f of built) console.log(`  ${f.id} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
