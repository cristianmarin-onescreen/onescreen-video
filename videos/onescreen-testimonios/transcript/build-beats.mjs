// Mapa de tiempos de PrevSC02: texto corregido + timings reales, cuantizados a 25 fps.
//
// El corte tiene tres bloques, medidos sobre el archivo, no supuestos:
//   A  0.00 – 19.16 s   NEGRO   locución de marca → lettering a cuadro completo
//   B 19.16 – 62.92 s   ENTREVISTAS → subtítulos verbatim en columna izquierda
//   C 62.92 – 73.40 s   NEGRO   locución de cierre → lettering a cuadro completo
//
// Los límites vienen de `blackdetect` y los 18 cortes de plano de `select=gt(scene,0.25)`.
// Las cajas de cara se midieron con YuNet cada 0.4 s: ninguna cara entra a la izquierda
// del 38% del ancho en ningún plano, y de ahí sale la columna segura del 34%.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 73.4;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);
const r6 = (n) => Math.round(n * 1e6) / 1e6;

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

// --- correcciones al texto ---------------------------------------------------
// Whisper acierta el tiempo; la ortografía se corrige a mano. "One Screen" es la
// marca partida en dos tokens: se fusiona en uno solo conservando el arranque del
// primero y el final del segundo, para no inventar tiempos.
const MERGE = [[53, 54, "OneScreen,"], [86, 87, "OneScreen,"], [173, 174, "OneScreen."], [184, 185, "OneScreen"]];
const FIX = { 8: "¿Y", 20: "ella?", 21: "Hasta", 154: "Ya" };

const merged = new Set(MERGE.flatMap(([a, b]) => [b]));
const mergeStart = new Map(MERGE.map(([a, b, text]) => [a, { b, text }]));

const words = [];
for (let i = 0; i < raw.length; i++) {
  if (merged.has(i)) continue;
  const m = mergeStart.get(i);
  const start = snap(raw[i].start, -1);
  const end = snap(m ? raw[m.b].end : raw[i].end, 1);
  words.push({
    i: words.length,
    src: i,
    text: m ? m.text : FIX[i] ?? raw[i].text,
    start,
    end: end > start ? end : snap(start + FRAME, 0),
  });
}

// --- bloques ------------------------------------------------------------------
const idxOf = (src) => words.findIndex((w) => w.src === src);
const A_END = idxOf(51);   // primera palabra del bloque de entrevistas
const C_START = idxOf(183);

// Cuadros de los bloques negros: una frase por cuadro. `accent` es el índice SRC
// de la única palabra azul del cuadro (null = ninguna).
const BLACK_FRAMES = [
  { block: "A", from: 0, to: 7, accent: 6, scale: "phrase" },
  { block: "A", from: 8, to: 20, accent: 13, scale: "phrase" },
  { block: "A", from: 21, to: 24, accent: null, scale: "display" },
  { block: "A", from: 25, to: 37, accent: 37, scale: "phrase" },
  { block: "A", from: 38, to: 44, accent: 38, scale: "display" },
  { block: "A", from: 45, to: 50, accent: null, scale: "display" },
  { block: "C", from: 183, to: 196, accent: 188, scale: "phrase" },
  { block: "C", from: 197, to: 201, accent: 200, scale: "display" },
  { block: "C", from: 202, to: 202, accent: null, scale: "colossal", rule: true },
  { block: "C", from: 203, to: 208, accent: 208, scale: "display" },
];

const bySrc = new Map(words.map((w) => [w.src, w]));
const spanWords = (fromSrc, toSrc) => words.filter((w) => w.src >= fromSrc && w.src <= toSrc);

const blackFrames = BLACK_FRAMES.map((f, n) => {
  const ws = spanWords(f.from, f.to);
  return {
    id: `${f.block}${n + 1}`,
    block: f.block,
    scale: f.scale,
    rule: !!f.rule,
    text: ws.map((w) => w.text).join(" "),
    start: ws[0].start,
    end: ws.at(-1).end,
    words: ws.map((w) => ({
      id: `w${w.i}`,
      i: w.i,
      text: w.text,
      start: w.start,
      accent: w.src === f.accent,
    })),
  };
});

// --- bloque B: subtítulos verbatim en columna --------------------------------
// La columna útil da ~24 caracteres por línea; se corta a 3 líneas por bloque.
// Se rompe además en fin de frase y en cualquier pausa mayor a 0.55 s, porque un
// subtítulo que cruza un silencio largo se queda huérfano en pantalla.
const MAX_CHARS = 72;
const PAUSE = 0.55;
const ACCENT_TEXT = /^OneScreen/;

const captionWords = words.slice(A_END, C_START);
const captions = [];
let cur = [];
for (let k = 0; k < captionWords.length; k++) {
  const w = captionWords[k];
  const prev = cur.at(-1);
  const wouldBe = cur.map((x) => x.text).join(" ").length + w.text.length + 1;
  if (cur.length && (wouldBe > MAX_CHARS || w.start - prev.end > PAUSE)) {
    captions.push(cur);
    cur = [];
  }
  cur.push(w);
  if (/[.?!]$/.test(w.text) && cur.map((x) => x.text).join(" ").length > 28) {
    captions.push(cur);
    cur = [];
  }
}
if (cur.length) captions.push(cur);

const captionBlocks = captions.map((ws, n) => {
  const next = captions[n + 1];
  // Un subtítulo se queda hasta que entra el siguiente; el último aguanta 0.7 s.
  const out = next ? snap(next[0].start - FRAME, -1) : snap(ws.at(-1).end + 0.7, 0);
  return {
    id: `c${n + 1}`,
    text: ws.map((w) => w.text).join(" "),
    start: ws[0].start,
    end: out,
    words: ws.map((w) => ({
      id: `w${w.i}`,
      i: w.i,
      text: w.text,
      start: w.start,
      accent: ACCENT_TEXT.test(w.text),
    })),
  };
});

// --- escenas ------------------------------------------------------------------
const CUT_A = snap(19.16, 0);
const CUT_B = snap(62.92, 0);
const scenes = [
  { id: "01-apertura", ground: "negro", start: 0, end: CUT_A },
  { id: "02-testimonios", ground: "metraje", start: CUT_A, end: CUT_B },
  { id: "03-cierre", ground: "negro", start: CUT_B, end: snap(TOTAL, 0) },
].map((s) => ({
  ...s,
  duration: r6(s.end - s.start),
  durationFrames: frames(s.end) - frames(s.start),
}));

const out = {
  fps: FPS,
  format: "3840x2160",
  totalDuration: snap(TOTAL, 0),
  totalFrames: frames(snap(TOTAL, 0)),
  source: "PrevSC02.mp4",
  safeColumn: { widthPct: 34, note: "ninguna cara entra a la izquierda del 38% en los 18 planos" },
  scenes,
  blackFrames,
  captions: captionBlocks,
  words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps`);
for (const s of scenes) console.log(`  ${s.id.padEnd(16)} ${String(s.start).padStart(8)} → ${String(s.end).padStart(8)}  ${s.durationFrames}f`);
console.log(`\nbloques negros: ${blackFrames.length} cuadros`);
for (const f of blackFrames) console.log(`  ${f.id.padEnd(4)} ${String(f.start).padStart(7)}–${String(f.end).padStart(7)}  ${f.scale.padEnd(9)} ${f.text}`);
console.log(`\nsubtítulos: ${captionBlocks.length} bloques`);
const lens = captionBlocks.map((c) => c.text.length);
console.log(`  longitud: min ${Math.min(...lens)} · media ${Math.round(lens.reduce((a, b) => a + b, 0) / lens.length)} · max ${Math.max(...lens)} caracteres`);
const durs = captionBlocks.map((c) => r6(c.end - c.start));
console.log(`  permanencia: min ${Math.min(...durs)}s · media ${(durs.reduce((a, b) => a + b, 0) / durs.length).toFixed(2)}s · max ${Math.max(...durs)}s`);
