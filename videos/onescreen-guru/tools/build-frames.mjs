// Capa de lettering de SC08 — «OneScreen Gurú».
//
//   HF_INK="#000000"  →  tinta negra, con el azul de marca como acento
//   HF_INK="#ffffff"  →  TODO BLANCO, sin azul. El montaje va sobre fondos azules y
//                        un acento #3976ff sobre azul desaparece.
//
// REGLA DE MARCA: "OneScreen" se compone en NEVIS; el modelo ("Core") y todo lo demás
// en Rubik. El tracking de Nevis es -0.050em, medido contra el logotipo vectorial
// oficial: a igual altura de caja, Nevis a ese tracking reproduce el ancho del
// wordmark con un 0.19% de desviación. No es una estimación.
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
const LIGHT = INK.toLowerCase() === "#ffffff";
// En la variante blanca el acento ES la tinta: todo blanco, nada de azul.
// ACENTO VERDE, no azul, y en LAS DOS variantes.
// Gurú es un producto de identidad verde — el botón que lo invoca es verde —, así que
// el acento de esta pieza es el verde exacto de marca. Se mantiene también en la
// variante de tinta blanca: el motivo por el que esa variante iba toda blanca era que
// el azul #3976ff desaparece sobre los fondos azules del montaje, y el verde no tiene
// ese problema. Es la única de las diez piezas que no usa el azul.
const ACCENT = "#2ad268";
const ID = "guru";

const CSS = `
@font-face {
  font-family: "Rubik";
  src: url("assets/fonts/Rubik-Variable.ttf") format("truetype");
  font-weight: 300 900;
  font-style: normal;
  font-display: block;
}
/* Nevis es una sola tipografía Bold. Se declara cubriendo 100—900 a propósito: así
   el navegador NUNCA sintetiza negrita encima de una que ya lo es, que engordaría
   los trazos y rompería la coincidencia con el logotipo. */
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
.beat {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 0 7cqw;
  opacity: 0;
}
.beat > .inner { display: block; max-width: 86cqw; text-align: center; margin-top: -1.4cqh; }
.ln { display: block; }
.w { display: inline-block; opacity: 0; will-change: transform; }
.accent { color: ${ACCENT}; }

/* La marca. Nevis, tracking medido contra el logotipo. Nunca en versalitas: el
   wordmark es caja mixta y forzarlo a caja alta deja de ser la marca. */
.brand {
  font-family: "Nevis", "Rubik", sans-serif;
  font-weight: 400;
  letter-spacing: -0.050em;
  text-transform: none !important;
}

.s-sub      { font-size: 3.0cqw;  font-weight: 500; line-height: 1.24; letter-spacing: -0.008em; }
.s-phrase   { font-size: 5.0cqw;  font-weight: 500; line-height: 1.12; letter-spacing: -0.020em; }
.s-display  { font-size: 7.0cqw;  font-weight: 600; line-height: 1.06; letter-spacing: -0.028em; }
.s-mega     { font-size: 10.0cqw; font-weight: 800; line-height: 1.00; letter-spacing: -0.035em; }
.s-colossal { font-size: 12.5cqw; font-weight: 800; line-height: 0.98; letter-spacing: -0.040em; }

/* Peso regular dentro de un escalón grande. Solo toca font-weight y tracking, nunca
   font-size: el escalón sigue mandando el tamaño. El tracking se afloja porque el
   negativo de los escalones grandes está calculado para peso 800, y en regular
   ese mismo valor junta demasiado las letras. */
.ln.w-reg { font-weight: 400; letter-spacing: -0.018em; }

.caps { text-transform: uppercase; }
.caps.s-sub      { letter-spacing: 0.16em; font-weight: 600; }
.caps.s-display  { letter-spacing: 0.000em; }
.caps.s-mega     { letter-spacing: -0.012em; }
.caps.s-colossal { letter-spacing: -0.018em; }

/* Nevis tiene la caja alta más corta que Rubik al mismo cuerpo: se compensa un 12%
   para que "OneScreen" pese lo mismo que una línea Rubik del mismo escalón.
   El valor va ABSOLUTO en cqw, no en em. Una regla .ln.s-mega.brand con font-size en
   em tiene tres clases de especificidad y gana a .s-mega, así que en vez de multiplicar
   el escalón lo sustituía por 1.12em del tamaño heredado — 18 px en un cuadro 4K. */
.ln.s-sub.brand      { font-size: 3.36cqw; }
.ln.s-phrase.brand   { font-size: 5.60cqw; }
.ln.s-display.brand  { font-size: 7.84cqw; }
.ln.s-mega.brand     { font-size: 11.20cqw; }
.ln.s-colossal.brand { font-size: 14.00cqw; }
/* Marca EN LÍNEA dentro de una línea de otra tipografía: aquí el padre sí lleva el
   escalón en cqw, así que el em multiplica y es correcto. */
.w.brand { font-size: 1.12em; }

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
        // Una línea entera de marca lleva .brand en la línea; si la marca convive con
        // otras palabras, la clase va en el span de la palabra.
        const allBrand = l.words.every((w) => w.brand);
        const cls = ["ln", `s-${l.scale}`, l.caps && !allBrand ? "caps" : "", l.regular ? "w-reg" : "", l.accent ? "accent" : "", allBrand ? "brand" : ""]
          .filter(Boolean)
          .join(" ");
        const ws = l.words
          .map((w) => `<span class="w${w.brand && !allBrand ? " brand" : ""}" id="${f.id}-${w.id}">${esc(w.text)}</span>`)
          .join(" ");
        return `            <span class="${cls}">${ws}</span>`;
      })
      .join("\n");
    return `        <div class="beat" id="${f.id}">\n          <span class="inner">\n${lines}\n          </span>\n        </div>`;
  })
  .join("\n");

const js = beats.frames
  .map((f, n) => {
    const next = beats.frames[n + 1];
    const out = [`        // ${f.id} — ${f.text}`];
    out.push(`        tl.set("#${f.id}", { opacity: 1 }, ${Math.round((f.start - 0.02) * 1e6) / 1e6});`);
    for (const l of f.lines) for (const w of l.words) out.push(`        word(tl, "#${f.id}-${w.id}", ${w.start});`);
    if (next) {
      const t = Math.round((next.start - 0.06) * 1e6) / 1e6;
      out.push(`        tl.to("#${f.id}", { y: -170, duration: 0.24, ease: "power4.in" }, ${Math.round((t - 0.24) * 1e6) / 1e6});`);
      out.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.12, ease: "none" }, ${Math.round((t - 0.12) * 1e6) / 1e6});`);
    } else {
      // La salida del último cuadro tiene que CABER en la composición. Aquí la cola es
      // de solo 0.74 s, así que anclarla a speechEnd+1.2 (28.3 s) la dejaba fuera de
      // los 27.84 s de la pieza y el tween no se ejecutaba nunca.
      // La salida del último cuadro solo se programa si CABE. Aquí la cola es de
      // 0.3 s: un fundido de 0.6 s arrancaría antes de que termine de entrar la
      // última palabra y el texto daría un parpadeo. Con cola corta se sostiene
      // hasta el final y el corte lo da el editor.
      const lastWord = Math.max(...f.lines.flatMap((l) => l.words.map((w) => w.start)));
      const fadeAt = Math.min(beats.speechEnd + 1.2, beats.totalDuration - 0.62);
      if (fadeAt > lastWord + 0.45) {
        out.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.6, ease: "power2.in" }, ${Math.round(fadeAt * 1e6) / 1e6});`);
      } else {
        out.push(`        // sin fundido de salida: la cola (${Math.round((beats.totalDuration - lastWord) * 100) / 100}s) no da para uno.`);
      }
    }
    return out.join("\n");
  })
  .join("\n\n");

const indent = (s, n) => s.split("\n").map((l) => (l ? " ".repeat(n) + l : l)).join("\n");

writeFileSync(
  join(OUT, `${ID}.html`),
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
`,
  "utf8"
);
console.log(`${ID}.html · ${beats.frames.length} cuadros · ${beats.totalDuration}s · tinta ${INK} · acento ${ACCENT}`);
