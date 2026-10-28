// Mapa de tiempos de SC07 — «Ecosistema de software».
//
// La pieza mas larga del proyecto: 81.36 s, cuatro productos con logotipo propio.
//
// REGLA DE MARCA + ICONO: cada vez que se nombra un software aparece su icono oficial
// encima del lockup, y el lockup sigue el patron de siempre — "OneScreen" en NEVIS,
// el nombre del producto en Rubik caja mixta y peso regular.
//
// Whisper parte los nombres de marca ("One" + "Screen") y los transcribe fonetico
// ("Lesson", "Scribe", "Super Notes"). Se corrigen a la grafia oficial: Lessn, Scrybe,
// QuizWiz, SuprNotes.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const FRAME = 1 / FPS;
const TOTAL = 81.36;

const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

const raw = JSON.parse(readFileSync(join(HERE, "words-raw.json"), "utf8"));

const FIX = {
  14: "eso,", 24: "Diseñado", 77: "Lessn.", 98: "Lessn", 113: "Scrybe.",
  // La voz se transcribio como "clases basadas"; el texto correcto es "quizzes
  // basados" — es la herramienta de cuestionarios, no de clases.
  152: "quizzes", 153: "basados",
  149: "QuizWiz.", 176: "Ahora,",
};
// Nombres de marca partidos por whisper + grafia fonetica corregida.
const MERGE = [
  [96, 97, "OneScreen"], [111, 112, "OneScreen"], [147, 148, "OneScreen"],
  [188, 189, "OneScreen"], [190, 191, "SuprNotes."], [204, 205, "SuprNotes"],
];
const BRAND = new Set([46, 76, 96, 111, 147, 188]);

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
    i: words.length, src: i,
    text: m ? m.text : FIX[i] ?? raw[i].text,
    start, end, brand: BRAND.has(i),
  });
}

const bySrc = new Map(words.map((w) => [w.src, w]));
const idx = (src) => bySrc.get(src).i;
const span = (a, b) => words.filter((w) => w.i >= idx(a) && w.i <= idx(b));

// Cuadros que van sobre pantallazos del software: el texto deja de ser lettering a
// pantalla completa y se comporta como subtitulo en el tercio inferior. Arranca en la
// frase que entrega el paso a la demo ("Comencemos antes de que empiece tu clase") y
// termina con el ultimo producto; el cierre vuelve a pantalla completa.
const LOWER = new Set(["f08","f09","f10","f10b","f11","f12","f13","f14","f14b","f15",
                       "f16","f17","f18","f18b","f19","f20","f21","f22","f23","f23b",
                       "f24","f24b"]);

const F = (id, lines, icon) => ({ id, lines, icon });
const L = (a, b, scale, o = {}) => ({ from: a, to: b, scale, ...o });

const FRAMES = [
  // --- intro ---
  F("f01", [L(0, 4, "sub"), L(5, 11, "mega", { caps: true })]),
  F("f02", [L(12, 18, "sub"), L(19, 23, "mega", { caps: true, accent: true })]),
  F("f03", [L(24, 25, "sub"), L(26, 26, "mega", { caps: true })]),
  // --- la meta ---
  F("f04", [L(27, 30, "mega", { caps: true })]),
  F("f05", [L(31, 37, "sub"), L(38, 40, "sub"), L(41, 42, "colossal", { caps: true, accent: true })]),
  // --- tres momentos ---
  F("f06", [L(43, 49, "sub"), L(50, 52, "mega", { caps: true })]),
  F("f07", [L(53, 53, "sub", { caps: true }), L(54, 55, "colossal", { caps: true, accent: true }), L(56, 67, "sub")]),
  // --- Lessn ---
  F("f08", [L(68, 74, "display")]),
  F("f09", [L(75, 75, "sub"), L(76, 77, "mega", { regular: true })], "lessn"),
  F("f10", [L(78, 86, "sub")]),
  F("f10b", [L(87, 94, "mega", { caps: true })]),
  F("f11", [L(95, 102, "sub"), L(103, 105, "mega", { caps: true, accent: true })]),
  // --- Scrybe ---
  F("f12", [L(106, 110, "display")]),
  F("f13", [L(111, 113, "mega", { regular: true })], "scrybe"),
  F("f14", [L(114, 122, "sub")]),
  F("f14b", [L(123, 125, "sub"), L(126, 127, "colossal", { caps: true, accent: true }), L(128, 132, "sub")]),
  F("f15", [L(133, 138, "sub"), L(139, 142, "mega", { caps: true })]),
  // --- QuizWiz ---
  F("f16", [L(143, 146, "display")]),
  F("f17", [L(147, 149, "mega", { regular: true })], "quizwiz"),
  F("f18", [L(150, 153, "sub"), L(154, 158, "sub")]),
  F("f18b", [L(159, 163, "mega", { caps: true }), L(164, 167, "sub")]),
  F("f19", [L(168, 172, "sub"), L(173, 175, "mega", { caps: true, accent: true })]),
  // --- SuprNotes ---
  F("f20", [L(176, 179, "display")]),
  F("f21", [L(180, 182, "sub"), L(183, 187, "mega", { caps: true })]),
  F("f22", [L(188, 190, "mega", { regular: true })], "suprnotes"),
  F("f23", [L(192, 199, "sub")]),
  F("f23b", [L(200, 203, "mega", { caps: true })]),
  F("f24", [L(204, 207, "sub"), L(208, 208, "colossal", { caps: true, accent: true })]),
  F("f24b", [L(209, 216, "sub")]),
  // --- cierre ---
  F("f25", [L(217, 223, "display")]),
  F("f26", [L(224, 225, "mega", { caps: true })]),
  F("f27", [L(226, 228, "sub"), L(229, 231, "mega", { caps: true, accent: true })]),
];

const built = FRAMES.map((f) => {
  const lines = f.lines.map((l) => {
    const ws = span(l.from, l.to);
    return {
      scale: l.scale, caps: !!l.caps, accent: !!l.accent, regular: !!l.regular,
      text: ws.map((w) => w.text).join(" "),
      words: ws.map((w) => ({ id: `w${w.i}`, i: w.i, text: w.text, start: w.start, brand: w.brand })),
    };
  });
  return { id: f.id, icon: f.icon || null, lower: LOWER.has(f.id), start: lines[0].words[0].start, lines,
           text: (f.icon ? `[${f.icon}] ` : "") + lines.map((l) => l.text).join(" / ") };
});

built.forEach((f, n) => {
  const next = built[n + 1];
  f.end = next ? snap(next.start - FRAME, -1) : snap(TOTAL, 0);
});

const out = {
  fps: FPS, format: "3840x2160",
  totalDuration: snap(TOTAL, 0), totalFrames: frames(snap(TOTAL, 0)),
  source: "Software - Narrador.wav", speechEnd: 81.1, brandTracking: "-0.050em",
  frames: built, words,
};
writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

console.log(`${words.length} palabras · ${out.totalFrames} frames a ${FPS} fps · ${built.length} cuadros`);
console.log(`marca en Nevis: ${words.filter((w) => w.brand).length} · iconos: ${built.filter((f) => f.icon).length}\n`);
console.log(`subtitulo en tercio inferior: ${built.filter((f) => f.lower).length} cuadros
`);
for (const f of built) console.log(`  ${f.id.padEnd(4)} ${String(f.start).padStart(6)}–${String(f.end).padStart(6)}  ${f.text}`);
