// Genera las 3 composiciones de PrevSC02 en compositions/frames/.
//
// Es una CAPA de superposición: el suelo va siempre transparente y se entrega en
// ProRes 4444 para montar sobre el corte en Premiere. Dos variantes de tinta:
//   HF_INK="#000000"  → sobre metraje claro
//   HF_INK="#ffffff"  → sobre metraje oscuro y sobre los bloques negros
//
// Sin gris: por instrucción del usuario no hay nivel intermedio. La jerarquía la
// hacen la escala y el orden de llegada, no el color.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const OUT = join(ROOT, "compositions", "frames");
mkdirSync(OUT, { recursive: true });

const beats = JSON.parse(readFileSync(join(ROOT, "transcript", process.env.HF_BEATS || "beats.json"), "utf8"));
const W = 3840;
const H = 2160;
const INK = process.env.HF_INK || "#000000";
const ACCENT = "#3976ff";

// Recorrido parcial de costura: 12% del cuadro.
const TRAVEL = 460;
const EXIT_DUR = 0.34;
const EXIT_LEAD = 0.285;
const EXIT_FADE_DELAY = 0.165;
const EXIT_FADE = 0.10;
const ENTRY_DUR = 0.42;

const BASE_CSS = `
@font-face {
  font-family: "Rubik";
  src: url("assets/fonts/Rubik-Variable.ttf") format("truetype");
  font-weight: 300 900;
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
  -webkit-font-smoothing: antialiased;
}
.stage { position: absolute; inset: 0; }
.w { display: inline-block; opacity: 0; will-change: transform; }
.accent { color: ${ACCENT}; }
/* Escalones. colossal aquí es 11cqw y no 15: "¿Comenzamos?" son 12 caracteres y a
   15cqw se saldría del ancho útil. */
.s-phrase   { font-size: 5.0cqw;  font-weight: 500; line-height: 1.10; letter-spacing: -0.022em; }
.s-display  { font-size: 7.6cqw;  font-weight: 600; line-height: 1.02; letter-spacing: -0.030em; }
.s-colossal { font-size: 11cqw;   font-weight: 800; line-height: 0.94; letter-spacing: -0.040em; }
/* Cuadros de los bloques negros: a cuadro completo, centrados. */
.beat { position: absolute; left: 8cqw; right: 8cqw; top: 34cqh; text-align: center; opacity: 0; }
.rule {
  display: block; width: 10cqw; height: 0.45cqh;
  background: ${ACCENT}; margin: 3.4cqh auto 0; transform-origin: 50% 50%; opacity: 0;
}
/* COLUMNA SEGURA. Medida, no estimada: ninguna cara entra a la izquierda del 38%
   del ancho en los 18 planos del tramo de entrevistas. La columna llega al 34% y
   deja 4 puntos de margen. Anclada por abajo para que los bloques de 2, 3 y 4
   líneas compartan línea base y el subtítulo no salte de altura. */
.caption {
  position: absolute;
  left: 6cqw;
  width: 28cqw;
  bottom: 22cqh;
  text-align: left;
  font-size: 2.3cqw;
  font-weight: 500;
  line-height: 1.28;
  letter-spacing: -0.008em;
  opacity: 0;
}
`.trim();

const TL_HELPERS = `
function word(tl, sel, t) {
  tl.set(sel, { opacity: 1 }, t);
  tl.fromTo(sel, { y: 52 }, { y: 0, duration: 0.15, ease: "power4.out", immediateRender: false }, t);
}
function seamExit(tl, sel, cut, axis, dir) {
  var t0 = cut - ${EXIT_LEAD};
  var to = { duration: ${EXIT_DUR}, ease: "power4.in" };
  to[axis] = ${TRAVEL} * dir;
  tl.to(sel, to, t0);
  tl.to(sel, { opacity: 0, duration: ${EXIT_FADE}, ease: "none" }, t0 + ${EXIT_FADE_DELAY});
}
function seamEntry(tl, sel, axis, dir) {
  var from = { opacity: 0.35 };
  from[axis] = -${TRAVEL} * dir;
  var to = { opacity: 1, duration: ${ENTRY_DUR}, ease: "power4.out" };
  to[axis] = 0;
  tl.fromTo(sel, from, to, 0);
}
`.trim();

const spans = (prefix, ws) =>
  ws.map((w) => `<span class="w${w.accent ? " accent" : ""}" id="${prefix}-${w.id}">${w.text}</span>`).join(" ");

const indent = (s, n) => s.split("\n").map((l) => (l ? " ".repeat(n) + l : l)).join("\n");

// ---------------------------------------------------------------------------
// Escenas de bloque negro (1 y 3): una frase por cuadro, a cuadro completo.
function blackScene({ id, block, sceneStart, duration, entrySeam, exitSeam }) {
  const list = beats.blackFrames.filter((f) => f.block === block);
  const rel = (t) => Math.round((t - sceneStart) * 1e6) / 1e6;

  const body = list
    .map(
      (f) =>
        `        <div class="beat s-${f.scale}" id="${f.id}">${spans(f.id, f.words)}` +
        (f.rule ? `<span class="rule" id="${f.id}-rule"></span>` : "") +
        `</div>`
    )
    .join("\n");

  const js = list
    .map((f, n) => {
      const next = list[n + 1];
      const lines = [`        // ${f.id} — ${f.text}`];
      if (n === 0 && entrySeam) {
        lines.push(`        seamEntry(tl, "#${f.id}", "x", -1);`);
        lines.push(`        tl.set("#${f.id}-${f.words[0].id}", { opacity: 1 }, 0);`);
        lines.push(...f.words.slice(1).map((w) => `        word(tl, "#${f.id}-${w.id}", ${rel(w.start)});`));
      } else {
        lines.push(`        tl.set("#${f.id}", { opacity: 1 }, ${rel(f.words[0].start) - 0.02});`);
        lines.push(...f.words.map((w) => `        word(tl, "#${f.id}-${w.id}", ${rel(w.start)});`));
      }
      if (f.rule) {
        lines.push(`        tl.set("#${f.id}-rule", { opacity: 1 }, ${rel(f.end) - 0.10});`);
        lines.push(
          `        tl.fromTo("#${f.id}-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.32, ease: "power3.out", immediateRender: false }, ${rel(f.end) - 0.10});`
        );
      }
      if (next) {
        // Sale cuando el siguiente cuadro va a entrar, no cuando termina de decirse:
        // así el relevo es continuo y no queda el cuadro vacío entre frase y frase.
        const out = rel(next.words[0].start) - 0.06;
        lines.push(`        tl.to("#${f.id}", { y: -${Math.round(TRAVEL * 0.45)}, duration: 0.26, ease: "power4.in" }, ${Math.round((out - 0.26) * 1e6) / 1e6});`);
        lines.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.12, ease: "none" }, ${Math.round((out - 0.14) * 1e6) / 1e6});`);
      } else if (exitSeam) {
        lines.push(`        seamExit(tl, "#${f.id}", ${duration}, "x", -1);`);
      } else {
        // Último cuadro del film: se retira suave sobre la cola.
        lines.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.5, ease: "power2.in" }, ${duration - 0.9});`);
      }
      return lines.join("\n");
    })
    .join("\n\n");

  return { id, body, js };
}

// ---------------------------------------------------------------------------
// Escena 2: subtítulos verbatim en la columna segura.
function captionScene({ id, sceneStart, duration }) {
  const rel = (t) => Math.round((t - sceneStart) * 1e6) / 1e6;
  const list = beats.captions;

  const body = list
    .map((c) => `        <div class="caption" id="${c.id}">${spans(c.id, c.words)}</div>`)
    .join("\n");

  const js = list
    .map((c, n) => {
      const lines = [`        // ${c.id} — ${c.text}`];
      if (n === 0) {
        lines.push(`        seamEntry(tl, "#${c.id}", "x", -1);`);
        lines.push(`        tl.set("#${c.id}-${c.words[0].id}", { opacity: 1 }, 0);`);
        lines.push(...c.words.slice(1).map((w) => `        word(tl, "#${c.id}-${w.id}", ${rel(w.start)});`));
      } else {
        lines.push(`        tl.set("#${c.id}", { opacity: 1 }, ${rel(c.words[0].start) - 0.02});`);
        lines.push(...c.words.map((w) => `        word(tl, "#${c.id}-${w.id}", ${rel(w.start)});`));
      }
      if (n === list.length - 1) {
        lines.push(`        seamExit(tl, "#${c.id}", ${duration}, "x", -1);`);
      } else {
        // Relevo seco entre subtítulos: 0.14 s, TERMINANDO en c.end, no empezando
        // ahí. Arrancar el fundido en c.end dejaba al bloque saliente encima del
        // entrante durante 0.14 s y se leían los dos a la vez.
        lines.push(`        tl.to("#${c.id}", { opacity: 0, duration: 0.14, ease: "none" }, ${Math.round((rel(c.end) - 0.14) * 1e6) / 1e6});`);
      }
      return lines.join("\n");
    })
    .join("\n\n");

  return { id, body, js };
}

const [s1, s2, s3] = beats.scenes;
const SCENES = [
  blackScene({ id: s1.id, block: "A", sceneStart: s1.start, duration: s1.duration, entrySeam: false, exitSeam: true }),
  captionScene({ id: s2.id, sceneStart: s2.start, duration: s2.duration }),
  blackScene({ id: s3.id, block: "C", sceneStart: s3.start, duration: s3.duration, entrySeam: true, exitSeam: false }),
];

SCENES.forEach((sc, n) => {
  const meta = beats.scenes[n];
  const html = `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>${sc.id}</title>
  </head>
  <body>
    <template>
      <style>
${indent(BASE_CSS, 8)}
      </style>

      <div
        id="root"
        data-composition-id="${sc.id}"
        data-width="${W}"
        data-height="${H}"
        data-duration="${meta.duration}"
      >
        <div class="stage" data-layout-allow-overlap data-layout-allow-occlusion>
${sc.body}
        </div>
      </div>

      <script>
        window.__timelines = window.__timelines || {};
        var tl = gsap.timeline({ paused: true });

${indent(TL_HELPERS, 8)}

${sc.js}

        window.__timelines["${sc.id}"] = tl;
      </script>
    </template>
  </body>
</html>
`;
  writeFileSync(join(OUT, `${sc.id}.html`), html, "utf8");
  console.log(`  ${sc.id}.html  ${String(meta.duration).padStart(8)}s  ${meta.durationFrames}f`);
});
console.log(`\ntinta ${INK} · 3 escenas · suelo transparente`);
