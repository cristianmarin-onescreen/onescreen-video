// Tarjetas de intro de producto — Lessn, Scrybe, QuizWiz, SuprNotes.
//
//   HF_INK="#000000"  →  tinta negra, con el azul de marca en el antetítulo
//   HF_INK="#ffffff"  →  TODO BLANCO, sin azul
//   HF_ONLY="c02"     →  emite SOLO esa tarjeta, rebasada a 0, como clip suelto
//
// No hay locución: el ritmo sale de un modelo de lectura explícito, no de una
// estimación. Ver READING más abajo.
//
// REGLA DE MARCA: "OneScreen" en NEVIS a -0.050em; el nombre del producto y todo lo
// demás en Rubik, caja mixta y peso regular.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
mkdirSync(join(ROOT, "compositions", "frames"), { recursive: true });

const W = 3840;
const H = 2160;
const FPS = 25;
const FRAME = 1 / FPS;
const INK = process.env.HF_INK || "#000000";
const LIGHT = INK.toLowerCase() === "#ffffff";
// El acento vive SOLO en el antetítulo "Conoce". No se tiñe el logotipo: el wordmark
// de OneScreen es negro o blanco, nunca azul. En la variante blanca no hay acento.
const ACCENT = LIGHT ? INK : "#3976ff";
const ID = "intros";

// ————————————————————————— El modelo de lectura —————————————————————————
// Ritmo estándar de lectura en pantalla. Los números no son de gusto: 2.7 palabras por
// segundo es el rango cómodo que usan los estándares de subtitulado (≈160 ppm) bajado
// un punto, porque aquí hay que leer además un nombre de marca desconocido. Lo demás
// es lo que la lectura necesita ALREDEDOR del texto:
//   ACQUIRE  el ojo encuentra la tarjeta y el icono aterriza antes de que haya que leer
//   LINEBRK  cada salto de línea cuesta una sacada extra
//   HOLD     reposo tras la última palabra: una tarjeta que corta en la última sílaba
//            se siente arrebatada aunque el tiempo de lectura fuera suficiente
//   FADE     el fundido de salida, que ya no es tiempo de lectura
const READING = { ACQUIRE: 0.62, WPS: 2.7, LINEBRK: 0.3, HOLD: 1.0, FADE: 0.5 };
const T_EYEBROW = 0.3;              // "Conoce" entra pisándole los talones al icono
const T_NAME = READING.ACQUIRE;     // el nombre, que es el héroe, empieza tras la entrada
const GAP_TAG = 0.25;    // respiro entre el nombre y el descriptor
const STAGGER = 0.055;   // cascada palabra a palabra dentro de una línea

const r6 = (x) => Math.round(x * 1e6) / 1e6;
const snap = (t) => Math.round(Math.round(t / FRAME) * FRAME * 1e6) / 1e6;
const words = (s) => s.trim().split(/\s+/).length;

// HF_LANG="pt" compone la tarjeta en portugues de Brasil. El modelo de lectura NO
// cambia: las duraciones se recalculan solas con el conteo de palabras portugues, que
// es lo que significa "el mismo ritmo" cuando no hay voz que seguir.
const LANG = (process.env.HF_LANG || "es").toLowerCase();
const COPY = {
  es: { eyebrow: "Conoce", tags: {
        Lessn:     ["Crea presentaciones en segundos"],
        Scrybe:    ["Graba, traduce y transcribe", "tus reuniones"],
        QuizWiz:   ["Crea evaluaciones en segundos"],
        SuprNotes: ["Un entorno de estudio", "hecho solo con tus fuentes"] } },
  pt: { eyebrow: "Conheça", tags: {
        Lessn:     ["Crie apresentações em segundos"],
        Scrybe:    ["Grave, traduza e transcreva", "suas reuniões"],
        QuizWiz:   ["Crie avaliações em segundos"],
        SuprNotes: ["Um ambiente de estudo", "feito só com as suas fontes"] } },
};
if (!COPY[LANG]) throw new Error(`HF_LANG="${LANG}" no existe. Idiomas: ${Object.keys(COPY).join(", ")}`);
const EYEBROW = COPY[LANG].eyebrow;

const CARDS = [
  { id: "c01", icon: "lessn",     product: "Lessn",     tag: COPY[LANG].tags.Lessn },
  { id: "c02", icon: "scrybe",    product: "Scrybe",    tag: COPY[LANG].tags.Scrybe },
  { id: "c03", icon: "quizwiz",   product: "QuizWiz",   tag: COPY[LANG].tags.QuizWiz },
  { id: "c04", icon: "suprnotes", product: "SuprNotes", tag: COPY[LANG].tags.SuprNotes },
];

// —————————————————— Tiempos: se derivan, no se escriben a mano ——————————————————
let cursor = 0;
const built = CARDS.map((c) => {
  const nameWords = 2;                                   // "OneScreen" + el producto
  const tagWords = c.tag.reduce((n, l) => n + words(l), 0);
  const tNameEnd = T_NAME + nameWords / READING.WPS;
  const tTag = snap(tNameEnd + GAP_TAG);
  const readEnd = tTag + tagWords / READING.WPS + READING.LINEBRK * (c.tag.length - 1);
  const hold = snap(readEnd + READING.HOLD);
  const dur = snap(hold + READING.FADE);

  const card = {
    ...c,
    start: snap(cursor),
    dur,
    tIcon: 0,
    tEyebrow: snap(T_EYEBROW),
    tName: snap(T_NAME),
    tTag,
    tFade: hold,
    readSeconds: r6(readEnd),
    tagWords,
  };
  cursor = snap(cursor + dur);
  return card;
});
const TOTAL = snap(cursor);

// ————————————————————————— Recorte a una sola tarjeta —————————————————————————
const ONLY = process.env.HF_ONLY || "";
const SEL = ONLY ? built.filter((c) => c.id === ONLY) : built;
if (ONLY && !SEL.length) throw new Error(`HF_ONLY="${ONLY}" no existe. Tarjetas: ${built.map((c) => c.id).join(", ")}`);
const SHIFT = ONLY ? SEL[0].start : 0;
const DURATION = ONLY ? SEL[0].dur : TOTAL;
const at = (x) => Math.max(0, r6(x - SHIFT));

const CSS = `
@font-face {
  font-family: "Rubik";
  src: url("assets/fonts/Rubik-Variable.ttf") format("truetype");
  font-weight: 300 900;
  font-style: normal;
  font-display: block;
}
/* Nevis es una sola tipografía Bold. Se declara cubriendo 100—900 a propósito: así el
   navegador NUNCA sintetiza negrita encima de una que ya lo es, que engordaría los
   trazos y rompería la coincidencia con el logotipo. */
@font-face {
  font-family: "Nevis";
  src: url("assets/fonts/Nevis.ttf") format("truetype");
  font-weight: 100 900;
  font-style: normal;
  font-display: block;
}
#root {
  position: absolute;
  inset: 0;
  width: ${W}px;
  height: ${H}px;
  overflow: hidden;
  container-type: size;
  background: transparent;
  color: ${INK};
  font-family: "Rubik", sans-serif;
  font-synthesis: none;
  -webkit-font-smoothing: antialiased;
}
.stage { position: absolute; inset: 0; }
.card {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 0 8cqw;
  opacity: 0;
}
.card > .inner { display: block; max-width: 80cqw; text-align: center; margin-top: -1.0cqh; }
.ln { display: block; }
.w { display: inline-block; opacity: 0; will-change: transform; }

/* El icono oficial trae su propio mosaico morado, así que el mismo archivo sirve para
   la tinta negra y para la blanca: no depende del color del texto. */
.ic { display: block; width: 9.5cqw; margin: 0 auto 2.2cqh; opacity: 0; }
.ic img { display: block; width: 100%; height: auto; }

/* El acento vive solo aquí. Teñir el nombre dejaría de ser el wordmark. */
.eyebrow { font-size: 3.0cqw; font-weight: 600; text-transform: uppercase; letter-spacing: 0.16em; color: ${ACCENT}; }

/* El nombre es el héroe: escalón grande pero en peso regular, como quedó definido en la
   pieza de la Core. El tracking se afloja porque el negativo de los escalones grandes
   está calculado para peso 800 y en regular junta demasiado las letras. */
.name { font-size: 7.2cqw; font-weight: 400; letter-spacing: -0.018em; line-height: 1.04; margin-top: 1.4cqh; }
/* Descriptor en peso regular, no en 500. A 500 pesaba casi tanto como el nombre —que
   va en regular— y los dos competian; el nombre debe ganar por tamano, no pelearse.
   Y mas aire arriba: pegado al nombre se leia como una segunda linea del lockup. */
.tag  { font-size: 4.4cqw; font-weight: 400; letter-spacing: -0.012em; line-height: 1.20; margin-top: 2.5cqh; }
.tag + .tag { margin-top: 0.2cqh; }

.brand {
  font-family: "Nevis", "Rubik", sans-serif;
  font-weight: 400;
  letter-spacing: -0.050em;
  text-transform: none !important;
}
/* Nevis tiene la caja alta más corta que Rubik al mismo cuerpo: se compensa un 12%.
   Aquí el padre ya lleva el escalón en cqw, así que el em multiplica y es correcto. */
.w.brand { font-size: 1.12em; }
`.trim();

const HELPERS = `
function word(tl, sel, t) {
  tl.set(sel, { opacity: 1 }, t);
  tl.fromTo(sel, { y: 46 }, { y: 0, duration: 0.34, ease: "power4.out", immediateRender: false }, t);
}
`.trim();

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// Cada palabra es su propio span: la cascada necesita direccionarlas una a una.
const lineHTML = (cardId, key, i, text, cls) => {
  const ws = text
    .trim()
    .split(/\s+/)
    .map((t, j) => `<span class="w${t === "OneScreen" ? " brand" : ""}" id="${cardId}-${key}${i}-${j}">${esc(t)}</span>`)
    .join(" ");
  return `            <span class="${cls}">${ws}</span>`;
};

const body = SEL
  .map((c) => {
    const rows = [
      `            <span class="ic" id="${c.id}-ic"><img src="assets/icons/${c.icon}.png" alt="" /></span>`,
      lineHTML(c.id, "e", 0, EYEBROW, "ln eyebrow"),
      lineHTML(c.id, "n", 0, `OneScreen ${c.product}`, "ln name"),
      ...c.tag.map((t, i) => lineHTML(c.id, "t", i, t, "ln tag")),
    ];
    return `        <div class="card" id="${c.id}">\n          <span class="inner">\n${rows.join("\n")}\n          </span>\n        </div>`;
  })
  .join("\n");

const js = SEL
  .map((c) => {
    const out = [`        // ${c.id} — ${EYEBROW} / OneScreen ${c.product} / ${c.tag.join(" ")}`];
    const t0 = c.start;
    out.push(`        tl.set("#${c.id}", { opacity: 1 }, ${at(t0 - 0.02)});`);
    // El icono aterriza ANTES de que haya nada que leer: primero se reconoce la marca.
    out.push(`        tl.set("#${c.id}-ic", { opacity: 1 }, ${at(t0 + c.tIcon)});`);
    out.push(`        tl.fromTo("#${c.id}-ic", { scale: 0.86, y: 40 }, { scale: 1, y: 0, duration: 0.44, ease: "back.out(1.25)", immediateRender: false }, ${at(t0 + c.tIcon)});`);

    const run = (key, i, text, base) =>
      text
        .trim()
        .split(/\s+/)
        .forEach((_, j) => out.push(`        word(tl, "#${c.id}-${key}${i}-${j}", ${at(t0 + base + j * STAGGER)});`));

    run("e", 0, EYEBROW, c.tEyebrow);
    run("n", 0, `OneScreen ${c.product}`, c.tName);
    let tagBase = c.tTag;
    c.tag.forEach((t, i) => {
      run("t", i, t, tagBase);
      tagBase = r6(tagBase + words(t) / READING.WPS * 0.55);   // la 2ª línea no espera a leerse entera
    });

    // Salida: fundido limpio, sin barrido. Cada tarjeta es un clip suelto y el corte lo
    // da el editor; un desplazamiento de salida solo estorbaría al empalmar.
    out.push(`        tl.to("#${c.id}", { opacity: 0, duration: ${READING.FADE}, ease: "power2.in" }, ${at(t0 + c.tFade)});`);
    return out.join("\n");
  })
  .join("\n\n");

const indent = (s, n) => s.split("\n").map((l) => (l ? " ".repeat(n) + l : l)).join("\n");

writeFileSync(
  join(ROOT, "compositions", "frames", `${ID}.html`),
  `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>${ID}</title>
  </head>
  <body>
    <template>
      <style>
${indent(CSS, 8)}
      </style>

      <div
        id="root"
        data-composition-id="${ID}"
        data-width="${W}"
        data-height="${H}"
        data-duration="${DURATION}"
      >
        <div class="stage" data-layout-allow-overlap data-layout-allow-occlusion>
${body}
        </div>
      </div>

      <script>
        window.__timelines = window.__timelines || {};
        var tl = gsap.timeline({ paused: true });

${indent(HELPERS, 8)}

${js}

        window.__timelines["${ID}"] = tl;
      </script>
    </template>
  </body>
</html>
`,
  "utf8"
);

// El index se reescribe con la duración del recorte, así no hay que parchearlo a mano
// cada vez que se saca una tarjeta suelta.
writeFileSync(
  join(ROOT, "index.html"),
  `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${W}, height=${H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" integrity="sha384-sG0Hv1tP1lZCk9KQmrIbY/XNwi+OY84GQqhMscbnsoBFqAz8KNCil1kvfL3Hbbk2" crossorigin="anonymous"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: ${W}px; height: ${H}px; overflow: hidden; background: transparent; }
      #root { position: relative; width: ${W}px; height: ${H}px; overflow: hidden; }
      .scene { position: absolute; inset: 0; width: 100%; height: 100%; }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="${DURATION}"
      data-width="${W}"
      data-height="${H}"
      data-fps="${FPS}">
      <div
        id="el-${ID}"
        class="scene"
        data-composition-id="${ID}"
        data-composition-src="compositions/frames/${ID}.html"
        data-start="0"
        data-duration="${DURATION}"
        data-track-index="1"
      ></div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
`,
  "utf8"
);

console.log(`${ID}.html · ${LANG} · ${SEL.length} tarjeta(s)${ONLY ? ` [solo ${ONLY}]` : ""} · ${DURATION}s · tinta ${INK} · acento ${ACCENT}`);
if (!ONLY) {
  console.log(`\nritmo: ${READING.WPS} palabras/s · entrada ${READING.ACQUIRE}s · salto de linea ${READING.LINEBRK}s · reposo ${READING.HOLD}s\n`);
  for (const c of built) {
    console.log(
      `  ${c.id}  ${String(c.start).padStart(6)}  dur ${String(c.dur).padStart(5)}s  ${String(Math.round(c.dur * FPS)).padStart(4)} frames  ` +
        `OneScreen ${c.product.padEnd(10)} · lectura hasta ${c.readSeconds}s, reposo hasta ${c.tFade}s`
    );
  }
}
