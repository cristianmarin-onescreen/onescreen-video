// Genera la capa de lettering de SC03 en compositions/frames/.
//
// Capa de superposición: suelo transparente, ProRes 4444, dos tintas.
//   HF_INK="#000000"  → sobre metraje claro
//   HF_INK="#ffffff"  → sobre metraje oscuro
//
// ESTILO. Este no usa mi sistema del manifiesto sino el del cliente, leído de sus
// montajes SC01/SC02:
//   · tres escalas dentro del mismo cuadro, no una por línea;
//   · VERSALITAS en la palabra héroe — mi spec anterior las prohibía y estaba mal;
//   · pesos mezclados: el conector ligero, la carga pesada;
//   · el azul marca los ordinales, que son el hilo conductor de la pieza.
// Sin gris, como en los entregables anteriores.
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
const ID = "metas";

const CSS = `
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
/* Todos los cuadros comparten centro óptico: un cuadro de una línea y otro de cuatro
   se leen sobre el mismo eje. Se centra con grid, NO con un margen negativo del 50%:
   los porcentajes de margin se resuelven contra el ANCHO del contenedor, así que
   -50% en un bloque de 86cqw empujaba el texto 1651 px fuera del cuadro. */
.beat {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 0 7cqw;
  opacity: 0;
}
.beat > .inner {
  display: block;
  max-width: 86cqw;
  text-align: center;
  margin-top: -1.4cqh;   /* levante óptico */
}
.ln { display: block; }
.w { display: inline-block; opacity: 0; will-change: transform; }
.accent { color: ${ACCENT}; }

/* Escalones. La rampa es más contrastada que la del manifiesto: el salto de sub a
   mega es de 3.3x, no de 2.3x. Es lo que hace que un cuadro con tres escalas se lea
   como jerarquía y no como desorden. */
.s-sub      { font-size: 3.0cqw;  font-weight: 500; line-height: 1.24; letter-spacing: -0.008em; }
.s-phrase   { font-size: 5.0cqw;  font-weight: 500; line-height: 1.12; letter-spacing: -0.020em; }
.s-display  { font-size: 7.0cqw;  font-weight: 600; line-height: 1.04; letter-spacing: -0.028em; }
.s-mega     { font-size: 10.0cqw; font-weight: 800; line-height: 0.98; letter-spacing: -0.035em; }
.s-colossal { font-size: 11.5cqw; font-weight: 800; line-height: 0.96; letter-spacing: -0.040em; }

/* Las versalitas piden tracking ABIERTO, no negativo: en caja alta el tracking
   cerrado junta los astas verticales y la palabra se emplasta. */
.caps { text-transform: uppercase; }
.caps.s-sub      { letter-spacing: 0.16em; font-weight: 600; }
.caps.s-phrase   { letter-spacing: 0.02em; }
.caps.s-display  { letter-spacing: 0.000em; }
.caps.s-mega     { letter-spacing: -0.012em; }
.caps.s-colossal { letter-spacing: -0.018em; }

/* Separación entre líneas de distinto escalón dentro de un cuadro. */
.ln + .ln { margin-top: 0.5cqh; }
.ln.s-sub + .ln.s-mega,
.ln.s-sub + .ln.s-colossal,
.ln.s-sub + .ln.s-display { margin-top: 1.1cqh; }
`.trim();

const HELPERS = `
function word(tl, sel, t) {
  tl.set(sel, { opacity: 1 }, t);
  tl.fromTo(sel, { y: 62 }, { y: 0, duration: 0.17, ease: "power4.out", immediateRender: false }, t);
}
`.trim();

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const body = beats.frames
  .map((f) => {
    const lines = f.lines
      .map((l) => {
        const cls = ["ln", `s-${l.scale}`, l.caps ? "caps" : "", l.accent ? "accent" : ""].filter(Boolean).join(" ");
        const ws = l.words.map((w) => `<span class="w" id="${f.id}-${w.id}">${esc(w.text)}</span>`).join(" ");
        return `            <span class="${cls}">${ws}</span>`;
      })
      .join("\n");
    return `        <div class="beat" id="${f.id}">\n          <span class="inner">\n${lines}\n          </span>\n        </div>`;
  })
  .join("\n");

const js = beats.frames
  .map((f, n) => {
    const next = beats.frames[n + 1];
    const out = [];
    out.push(`        // ${f.id} — ${f.text}`);
    out.push(`        tl.set("#${f.id}", { opacity: 1 }, ${Math.round((f.start - 0.02) * 1e6) / 1e6});`);
    for (const l of f.lines) for (const w of l.words) out.push(`        word(tl, "#${f.id}-${w.id}", ${w.start});`);
    if (next) {
      // El cuadro cede el sitio 0.06 s antes de que entre el siguiente: nunca hay
      // pantalla vacía entre verso y verso, y nunca se pisan dos cuadros.
      const t = Math.round((next.start - 0.06) * 1e6) / 1e6;
      out.push(`        tl.to("#${f.id}", { y: -170, duration: 0.24, ease: "power4.in" }, ${Math.round((t - 0.24) * 1e6) / 1e6});`);
      out.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.12, ease: "none" }, ${Math.round((t - 0.12) * 1e6) / 1e6});`);
    } else {
      // Último cuadro: se sostiene sobre la cola y se retira sin prisa.
      out.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.6, ease: "power2.in" }, ${beats.speechEnd + 0.8});`);
    }
    return out.join("\n");
  })
  .join("\n\n");

const indent = (s, n) => s.split("\n").map((l) => (l ? " ".repeat(n) + l : l)).join("\n");

const html = `<!doctype html>
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
        data-duration="${beats.totalDuration}"
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
`;

writeFileSync(join(OUT, `${ID}.html`), html, "utf8");
console.log(`${ID}.html · ${beats.frames.length} cuadros · ${beats.totalDuration}s · tinta ${INK}`);
