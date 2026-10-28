// Capa de lettering de SC07 — «Ecosistema de software».
//
//   HF_INK="#000000"  →  tinta negra, con el azul de marca como acento
//   HF_INK="#ffffff"  →  TODO BLANCO, sin azul. El montaje va sobre fondos azules y
//                        un acento #3976ff sobre azul desaparece.
//
// REGLA DE MARCA: "OneScreen" se compone en NEVIS; el modelo ("Core") y todo lo demás
// en Rubik. El tracking de Nevis es -0.050em, medido contra el logotipo vectorial
// oficial: a igual altura de caja, Nevis a ese tracking reproduce el ancho del
// wordmark con un 0.19% de desviación. No es una estimación.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
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
const ACCENT = LIGHT ? INK : "#3976ff";
const ID = "software";

// HF_ONLY="f18" emite SOLO ese cuadro, como clip suelto para parchear el montaje sin
// rehacer la pieza entera. El clip empieza exactamente donde empieza el cuadro en el
// maestro, asi que en la linea de tiempo se coloca en ese mismo segundo y encaja al
// fotograma. Sin la variable no cambia nada del camino normal.
const ONLY = process.env.HF_ONLY || "";
const ALL = beats.frames;
const SEL = ONLY ? ALL.filter((f) => f.id === ONLY) : ALL;
if (ONLY && !SEL.length) throw new Error(`HF_ONLY="${ONLY}" no existe. Cuadros: ${ALL.map((f) => f.id).join(", ")}`);
const SHIFT = ONLY ? SEL[0].start : 0;
const NEXT_OF_SEL = ONLY ? ALL[ALL.indexOf(SEL[0]) + 1] : null;
const DURATION = ONLY
  ? Math.round(((NEXT_OF_SEL ? NEXT_OF_SEL.start : beats.totalDuration) - SHIFT) * 1e6) / 1e6
  : beats.totalDuration;

const r6 = (x) => Math.round(x * 1e6) / 1e6;
const clamp = (x) => Math.max(0, r6(x));       // nada puede programarse antes del 0 del clip
const at = (x) => clamp(x - SHIFT);            // tiempo del maestro -> tiempo del clip

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
/* Icono de producto. Los cuatro logotipos de software traen su propio fondo morado
   con esquinas redondeadas, asi que el MISMO archivo sirve para la variante de tinta
   negra y para la blanca: no dependen del color del texto. */
.ic { display: block; width: 13cqw; margin: 0 auto 1.6cqh; opacity: 0; }
.ic img { display: block; width: 100%; height: auto; }
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

/* Escalones. El rango va de 3.4 a 9.6cqw — un factor de 2.8x entre el cuerpo mas
   pequeno y el mas grande. Antes era 3.0 a 12.5 (4.2x) y el salto resultaba brusco:
   la linea pequena quedaba en letra menuda y la grande se comia el cuadro. Se corrige
   por los dos extremos a la vez: sube el piso y baja el techo, y la jerarquia se
   mantiene con peso y color, que no dependen del tamano. */
.s-sub      { font-size: 3.4cqw; font-weight: 500; line-height: 1.26; letter-spacing: -0.010em; }
.s-phrase   { font-size: 5.2cqw; font-weight: 500; line-height: 1.14; letter-spacing: -0.018em; }
.s-display  { font-size: 6.4cqw; font-weight: 600; line-height: 1.08; letter-spacing: -0.024em; }
.s-mega     { font-size: 8.2cqw; font-weight: 800; line-height: 1.02; letter-spacing: -0.028em; }
.s-colossal { font-size: 9.6cqw; font-weight: 800; line-height: 1.00; letter-spacing: -0.030em; }

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
.ln.s-sub.brand      { font-size: 3.81cqw; }
.ln.s-phrase.brand   { font-size: 5.82cqw; }
.ln.s-display.brand  { font-size: 7.17cqw; }
.ln.s-mega.brand     { font-size: 9.18cqw; }
.ln.s-colossal.brand { font-size: 10.75cqw; }
/* Marca EN LÍNEA dentro de una línea de otra tipografía: aquí el padre sí lleva el
   escalón en cqw, así que el em multiplica y es correcto. */
.w.brand { font-size: 1.12em; }

.ln + .ln { margin-top: 0.5cqh; }
.ln.s-sub + .ln.s-mega,
.ln.s-sub + .ln.s-colossal,
.ln.s-sub + .ln.s-display { margin-top: 1.1cqh; }

/* ————————————— Modo subtitulo (tercio inferior) —————————————
   La seccion de productos se monta sobre pantallazos del software. Ahi el texto no
   puede seguir siendo lettering a pantalla completa: taparia justo lo que hay que
   mirar. Pasa a comportarse como subtitulo — bloque anclado abajo, medida mas corta
   y un rango de cuerpos casi plano (2.9 a 3.9cqw, apenas 1.3x). El enfasis lo llevan
   el peso y el color; el tamano deja de moverse. */
.beat.lower { place-items: end center; padding: 0 12cqw 13cqh; }
.beat.lower > .inner { max-width: 80cqw; margin-top: 0; }

.lower .s-sub      { font-size: 2.9cqw; font-weight: 500; line-height: 1.22; letter-spacing: -0.004em; }
.lower .s-phrase   { font-size: 3.3cqw; font-weight: 600; line-height: 1.20; letter-spacing: -0.006em; }
.lower .s-display  { font-size: 3.3cqw; font-weight: 600; line-height: 1.20; letter-spacing: -0.006em; }
.lower .s-mega     { font-size: 3.9cqw; font-weight: 700; line-height: 1.18; letter-spacing: -0.010em; }
.lower .s-colossal { font-size: 3.9cqw; font-weight: 800; line-height: 1.18; letter-spacing: -0.010em; }

/* Una linea larga de subtitulo en versalitas se vuelve un grito y cuesta leerla.
   Aqui las versalitas solo sobreviven en el remate corto ("28 IDIOMAS", "CHATBOT"). */
.lower .caps            { text-transform: none; letter-spacing: -0.008em; font-weight: 700; }
.lower .caps.s-colossal { text-transform: uppercase; letter-spacing: 0.010em; font-weight: 800; }

.lower .ln.w-reg { font-weight: 400; letter-spacing: -0.004em; }
.lower .ln + .ln,
.lower .ln.s-sub + .ln.s-mega,
.lower .ln.s-sub + .ln.s-colossal,
.lower .ln.s-sub + .ln.s-display { margin-top: 0.7cqh; }

.lower .ln.s-sub.brand      { font-size: 3.25cqw; }
.lower .ln.s-phrase.brand   { font-size: 3.70cqw; }
.lower .ln.s-display.brand  { font-size: 3.70cqw; }
.lower .ln.s-mega.brand     { font-size: 4.37cqw; }
.lower .ln.s-colossal.brand { font-size: 4.37cqw; }

/* Lockup de producto sobre pantallazo: icono y nombre en UNA fila, como una chapa
   identificadora. Apilarlos como en pantalla completa haria el bloque demasiado alto
   para caber en el tercio inferior sin subirse encima de la interfaz. */
.lock { display: flex; align-items: center; justify-content: center; gap: 1.5cqw; }
.lower .ic { width: 5.6cqw; margin: 0; flex: none; }
.lower .lock .ln { font-size: 4.6cqw; margin-top: 0; }
`.trim();

const HELPERS = `
function word(tl, sel, t) {
  tl.set(sel, { opacity: 1 }, t);
  tl.fromTo(sel, { y: 62 }, { y: 0, duration: 0.17, ease: "power4.out", immediateRender: false }, t);
}
// Entrada de subtitulo: el mismo sincronismo palabra a palabra, pero con un tercio del
// recorrido y una curva menos violenta. Un subtitulo que salta 62 px sobre un
// pantallazo compite con la interfaz que hay detras en vez de acompanarla.
function wordSoft(tl, sel, t) {
  tl.set(sel, { opacity: 1 }, t);
  tl.fromTo(sel, { y: 20 }, { y: 0, duration: 0.24, ease: "power3.out", immediateRender: false }, t);
}
`.trim();

// Ajustes de cuerpo calculados por tools/fit-lines.py, que mide cada linea con las
// fuentes REALES. El escalon se elige por jerarquia, no por longitud, asi que una
// palabra larga en versalitas puede desbordar: aqui se corrige sin tocar la jerarquia.
const FIT_PATH = join(ROOT, "transcript", process.env.HF_FIT || "fit.json");
const FIT = existsSync(FIT_PATH) ? JSON.parse(readFileSync(FIT_PATH, "utf8")) : {};
const fitStyle = (frameId, lineIndex) => {
  const cqw = FIT[frameId]?.[String(lineIndex)];
  return cqw ? ` style="font-size:${cqw}cqw"` : "";
};

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const body = SEL
  .map((f) => {
    const lines = f.lines
      .map((l, li) => {
        // Una línea entera de marca lleva .brand en la línea; si la marca convive con
        // otras palabras, la clase va en el span de la palabra.
        const allBrand = l.words.every((w) => w.brand);
        const cls = ["ln", `s-${l.scale}`, l.caps && !allBrand ? "caps" : "", l.regular ? "w-reg" : "", l.accent ? "accent" : "", allBrand ? "brand" : ""]
          .filter(Boolean)
          .join(" ");
        const ws = l.words
          .map((w) => `<span class="w${w.brand && !allBrand ? " brand" : ""}" id="${f.id}-${w.id}">${esc(w.text)}</span>`)
          .join(" ");
        return `            <span class="${cls}"${fitStyle(f.id, li)}>${ws}</span>`;
      })
      .join("\n");
    const icon = f.icon
      ? `            <span class="ic" id="${f.id}-ic"><img src="assets/icons/${f.icon}.png" alt="" /></span>`
      : "";

    // En pantalla completa el icono va apilado encima del nombre. En modo subtitulo
    // comparte fila con el, para que el lockup entero quepa en el tercio inferior.
    let inner;
    if (icon && f.lower) {
      const rows = lines.split("\n");
      const nameRow = rows.pop().trim();
      inner = [...rows, `            <span class="lock">\n              ${icon.trim()}\n              ${nameRow}\n            </span>`].join("\n");
    } else {
      inner = icon ? `${icon}\n${lines}` : lines;
    }
    return `        <div class="beat${f.lower ? " lower" : ""}" id="${f.id}">
          <span class="inner">
${inner}
          </span>
        </div>`;
  })
  .join("\n");

const js = SEL
  .map((f) => {
    const next = ALL[ALL.indexOf(f) + 1];
    const out = [`        // ${f.id} — ${f.text}`];
    out.push(`        tl.set("#${f.id}", { opacity: 1 }, ${at(f.start - 0.02)});`);
    if (f.icon) {
      // El icono entra ANTES que el nombre: primero se reconoce la marca,
      // luego se lee. Escala desde 0.86 para que llegue, no para que aparezca.
      const t = at(f.start - 0.02);
      out.push(`        tl.set("#${f.id}-ic", { opacity: 1 }, ${t});`);
      const icFrom = f.lower ? "{ scale: 0.90, y: 14 }" : "{ scale: 0.86, y: 40 }";
      const icEase = f.lower ? "back.out(1.05)" : "back.out(1.3)";
      out.push(`        tl.fromTo("#${f.id}-ic", ${icFrom}, { scale: 1, y: 0, duration: 0.34, ease: "${icEase}", immediateRender: false }, ${t});`);
    }
    const enter = f.lower ? "wordSoft" : "word";
    for (const l of f.lines) for (const w of l.words) out.push(`        ${enter}(tl, "#${f.id}-${w.id}", ${at(w.start)});`);
    if (next) {
      const t = at(next.start - 0.06);
      if (f.lower) {
        // Salida de subtitulo: practicamente un encadenado. El barrido de -170 px del
        // modo a pantalla completa, repetido cada pocos segundos sobre un pantallazo,
        // marea. Aqui el bloque solo cede 26 px mientras se desvanece.
        out.push(`        tl.to("#${f.id}", { y: -26, duration: 0.20, ease: "power2.in" }, ${clamp(t - 0.20)});`);
        out.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.14, ease: "none" }, ${clamp(t - 0.14)});`);
      } else {
        out.push(`        tl.to("#${f.id}", { y: -170, duration: 0.24, ease: "power4.in" }, ${clamp(t - 0.24)});`);
        out.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.12, ease: "none" }, ${clamp(t - 0.12)});`);
      }
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
        out.push(`        tl.to("#${f.id}", { opacity: 0, duration: 0.6, ease: "power2.in" }, ${at(fadeAt)});`);
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
console.log(`${ID}.html · ${SEL.length} cuadro(s)${ONLY ? ` [solo ${ONLY}, desplazado -${SHIFT}s]` : ""} · ${DURATION}s · tinta ${INK} · acento ${ACCENT}`);
