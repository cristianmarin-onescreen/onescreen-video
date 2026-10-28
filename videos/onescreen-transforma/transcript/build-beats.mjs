// Construye beats.json: texto del guion aprobado + timings reales de la locución,
// cuantizados a la rejilla de 24 fps. Determinista: misma entrada, misma salida.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 24;
const FRAME = 1 / FPS;

// Redondeo a frontera de frame. `dir`: -1 piso, +1 techo, 0 al más cercano.
const snap = (t, dir = 0) => {
  const f = t / FRAME;
  const n = dir < 0 ? Math.floor(f) : dir > 0 ? Math.ceil(f) : Math.round(f);
  return Math.round(n * FRAME * 1e6) / 1e6;
};
const frames = (t) => Math.round(t / FRAME);

// El guion aprobado manda para la ortografía. Whisper manda para el tiempo.
// 124 tokens, alineados 1:1 con transcript/words.json (verificado).
const SCRIPT = `Hay espacios que solo ocupan un lugar.
Y hay espacios que cambian lo que pasa dentro de ellos.
Hay espacios que no se llenan con cualquier cosa.
Y hay espacios a los que solo les falta una cosa.
Esa cosa. Es una OneScreen.
Porque para nosotros, transformar un espacio es mucho más que solo tecnología.
Es una clase que por fin se entiende.
Es un equipo que toma mejores decisiones.
Es una idea, que ahora se ve en grande.
Creemos en eso.
En transformar la educación normal, en educación del futuro.
En transformar empresas, en empresas del futuro.
Porque cuando un espacio cambia.
El futuro también.
OneScreen.
Transforma el espacio. Transforma el futuro.
Tu transformación puede comenzar ya, solo tienes que tocar la pantalla.`
  .split(/\s+/)
  .filter(Boolean);

const whisper = JSON.parse(readFileSync(join(HERE, "words.json"), "utf8"));

if (whisper.length !== SCRIPT.length) {
  throw new Error(`desalineado: guion ${SCRIPT.length} vs locución ${whisper.length}`);
}

// Cortes de escena, ya elegidos para caer en los huecos reales entre frases.
// [id, título, fin en segundos]
const CUTS = [
  ["01", "espacios", 5.0],
  ["02", "noche", 7.5],
  ["03", "falta-una-cosa", 11.083333],
  ["04", "onescreen", 13.75],
  ["05", "mas-que-tecnologia", 18.166667],
  ["06", "tres-pruebas", 24.541667],
  ["07", "creemos", 31.791667],
  ["08", "el-futuro-tambien", 34.791667],
  ["09", "lockup", 38.208333],
  ["10", "toca-la-pantalla", 43.083333],
];

// La palabra de acento (#3976ff) por escena. Índice sobre SCRIPT, 0-based.
// Máximo una por escena; null = la escena no lleva acento.
const ACCENT = {
  "01": 11,  // cambian
  "02": 25,  // cualquier
  "03": 35,  // falta
  "04": null, // "OneScreen" va en negro; el acento lo pone el filete azul
  "05": 51,  // más
  "06": 78,  // grande
  "07": 97,  // futuro. (la segunda ocurrencia, la que cierra el par)
  "08": 104, // futuro  — en colossal, teñido: el clímax
  "09": 112, // futuro  (de "Transforma el futuro.")
  "10": 123, // pantalla
};

// Escalón tipográfico por palabra cuando difiere del de la escena.
const SCALE_OVERRIDE = {
  42: "colossal", // OneScreen  (la nominación)
  104: "colossal", // futuro    (el clímax)
};

const words = SCRIPT.map((text, i) => {
  const w = whisper[i];
  const start = snap(w.start, -1);
  let end = snap(w.end, 1);
  if (end <= start) end = snap(start + FRAME, 0);
  return {
    i,
    id: `w${i}`,
    text,
    start,
    end,
    startFrame: frames(start),
    endFrame: frames(end),
    raw: { start: w.start, end: w.end },
    drift: Math.round((start - w.start) * 1000) / 1000,
    confidence: w.prob,
  };
});

let cursor = 0;
let prevEnd = 0;
const scenes = CUTS.map(([id, title, endRaw]) => {
  const start = prevEnd;
  const end = snap(endRaw, 0);
  prevEnd = end;
  const mine = [];
  while (cursor < words.length && words[cursor].start < end) mine.push(words[cursor++]);
  const accentIdx = ACCENT[id];
  return {
    id,
    title,
    start,
    end,
    duration: Math.round((end - start) * 1e6) / 1e6,
    startFrame: frames(start),
    durationFrames: frames(end) - frames(start),
    text: mine.map((w) => w.text).join(" "),
    accentWord: accentIdx == null ? null : { i: accentIdx, text: SCRIPT[accentIdx] },
    // tiempos relativos al inicio de la escena — lo que consume cada composición
    words: mine.map((w) => ({
      id: w.id,
      i: w.i,
      text: w.text,
      at: Math.round((w.start - start) * 1e6) / 1e6,
      atFrame: w.startFrame - frames(start),
      dur: Math.round((w.end - w.start) * 1e6) / 1e6,
      accent: w.i === accentIdx,
      scale: SCALE_OVERRIDE[w.i] ?? null,
    })),
  };
});

if (cursor !== words.length) throw new Error(`quedaron ${words.length - cursor} palabras sin escena`);

const out = {
  fps: FPS,
  format: "3840x2160",
  totalDuration: scenes.at(-1).end,
  totalFrames: frames(scenes.at(-1).end),
  audio: { src: "assets/narration.wav", speechEnd: 41.84, tail: 1.243333 },
  scenes,
  words,
};

writeFileSync(join(HERE, "beats.json"), JSON.stringify(out, null, 1) + "\n", "utf8");

const maxDrift = Math.max(...words.map((w) => Math.abs(w.drift)));
console.log(`escenas=${scenes.length} palabras=${words.length} total=${out.totalDuration}s (${out.totalFrames}f)`);
console.log(`deriva máxima por cuantización a 24fps: ${(maxDrift * 1000).toFixed(1)} ms (1 frame = 41.7 ms)`);
for (const s of scenes) {
  console.log(
    `  ${s.id} ${s.title.padEnd(20)} ${String(s.start).padStart(9)}s → ${String(s.end).padStart(9)}s  ` +
      `${String(s.durationFrames).padStart(4)}f  ${s.words.length} palabras  acento=${s.accentWord?.text ?? "—"}`
  );
}
