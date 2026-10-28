// Genera las 10 composiciones ANIMADAS en compositions/frames/.
//
// Fuente de verdad del tiempo: transcript/beats.json (timings reales de la locución,
// cuantizados a 24 fps). Fuente de verdad de la marca: frame.md. Fuente de verdad de
// los layouts: los bocetos aprobados � este script los VISTE de movimiento, no los
// redibuja.
//
// Doctrina de movimiento aplicada (motion-doctrine + cut-the-curve):
//   · Corriente del film: LEFT. UP se gasta en las dos fronteras del bloque nocturno.
//     El inverse zoom se gasta dos veces, ambas en llegadas.
//   · El portador de cada costura es el TEXTO, no el envoltorio de escena: sobre fondo
//     blanco no hay superficie que se vea viajar. Por eso los vectores se autorizan
//     aquí dentro y ledger.json apunta a héroes internos.
//   · La primera palabra de cada escena entra EN el corte, montada en el vector de
//     entrada; las demás entran en su propio timestamp. El adelanto máximo es 0.21 s
//     (cuadro 9) y el resto está entre 0.08 y 0.18 s � el texto va un pelo delante de
//     la voz, que es como se lee bien.
//   · Cero movimiento inactivo. Nada flota, nada respira, nada pulsa en bucle.
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

// Color de suelo. Por defecto blanco (el film tal cual). Con HF_GROUND se generan las
// variantes para montaje:
//   HF_GROUND="#00FF00"    → croma verde   (+ node tools/set-ground.mjs "#00FF00")
//   HF_GROUND="transparent" → canal alfa   (+ node tools/set-ground.mjs "transparent")
// Verde puro y no el verde de plató (#00B140) porque la fuente es sintética: ningún
// color del film se le acerca en tono (negro, gris #7e7e82, azul #3976ff, blanco), así
// que el keyer puede trabajar con tolerancia estrecha.
const GROUND = process.env.HF_GROUND || "#ffffff";
// Cualquier suelo que no sea el blanco original es una variante de montaje: el bloque
// nocturno pierde su fondo negro y se comporta como las demás escenas.
const IS_KEY = GROUND.toLowerCase() !== "#ffffff";

// Tinta. Por defecto negra (el film sobre blanco). Con HF_INK="#ffffff" se genera la
// variante de texto blanco, pensada para componer sobre metraje OSCURO:
//   HF_GROUND=transparent HF_INK="#ffffff" node tools/build-frames.mjs
//
// El gris de apoyo se invierte con ella. No es el complemento aritmético de #7e7e82:
// sobre metraje oscuro un gris medio se pierde, así que sube a #b9b9be — sigue
// leyéndose claramente como secundario frente al blanco puro, pero sobrevive encima
// de imagen. El azul de marca NO se toca: #3976ff es la marca, no una decisión de
// contraste.
const INK = process.env.HF_INK || "#000000";
const LIGHT_TEXT = INK.toLowerCase() !== "#000000";
const MUTED = LIGHT_TEXT ? "#b9b9be" : "#7e7e82";

// ---- constantes de movimiento, escaladas a 4K -------------------------------
// El catálogo está escrito para 1920; recorrido parcial = 12% del cuadro.
const TRAVEL = 460;      // 12% de 3840
const EXIT_DUR = 0.34;   // power4.in
// Cuánto lleva rodando la salida cuando cae el corte. Con power4.in sobre 0.34 s, a
// los 0.285 s la velocidad instantánea es ~3200 px/s — que es justo la de entrada del
// cuadro siguiente. Cortar antes (a los 0.20 s) dejaba la salida 57 veces más lenta
// que la entrada: la ley de vectores se cumplía en dirección pero no en velocidad.
const EXIT_LEAD = 0.285;
// El fundido NO arranca con el desplazamiento. Con power4.in, en los primeros 0.165 s
// de un tween de 0.34 s el texto recorre 25 px de 460 — es decir, no se mueve. Ese
// tramo se aprovecha para que la última palabra siga LEGIBLE en vez de apagarse casi
// al aparecer. El fundido entra al final, cuando la aceleración ya es visible, y
// termina 0.02 s antes del corte.
const EXIT_FADE_DELAY = 0.165;
const EXIT_FADE = 0.10;
const ENTRY_DUR = 0.42;  // power4.out � la entrada es ~127% de la salida
const ENTRY_OPACITY = 0.35; // ignición a media trayectoria; 0� 1 binario "popea"

// Entrada de palabra (§6 waterfall entry): opacidad binaria, desde abajo, power4.out.
const WORD_Y = { heavy: 140, normal: 90, light: 66 };
const WORD_DUR = { heavy: 0.20, normal: 0.16, light: 0.12 };

// Todas las escenas viven en el DOM al mismo tiempo; el runtime solo muestra la que
// toca en cada frame. La auditoría de layout, en cambio, mide getBoundingClientRect
// en cada muestra sin mirar la ventana temporal del clip. Como este film es
// tipografía CENTRADA, la caja de cada escena cae encima de la de todas las demás y
// la auditoría reporta choques entre escenas que nunca coexisten en pantalla.
//
// Se marca el ESCENARIO de cada cuadro: es el envoltorio más pequeño que cubre el
// caso. No se toca la raíz � `data-layout-allow-overflow` a nivel raíz apagaría
// además text-clipping y content-cramped-container en todo el subárbol, y esos sí
// los queremos vivos. Las comprobaciones de borde de lienzo (primary-offscreen,
// foreground-over-panel) siguen corriendo igual.
const XSCENE = `data-layout-allow-overlap data-layout-allow-occlusion`;

// El logotipo va EN LÍNEA, no como <img>. Un <img> renderiza el SVG en su propio
// contexto de documento, así que el `fill="currentColor"` de los trazos nunca hereda
// el `color` del cuadro: el logotipo salía siempre negro, y en la variante de texto
// blanco quedaba invisible sobre metraje oscuro. En línea sí hereda y se tiñe con INK.
// Se le quitan los id de capa de Illustrator ("b", "c") porque el logotipo aparece en
// dos cuadros y los id tienen que ser únicos en la página ensamblada; no hay ninguna
// referencia url(#...) que dependa de ellos (verificado).
const WORDMARK_SVG = readFileSync(join(ROOT, "assets", "onescreen-wordmark.svg"), "utf8")
  .replace(/^﻿/, "")
  .replace(/<\?xml[^>]*\?>\s*/, "")
  .replace(/\s(?:id|data-name)="[^"]*"/g, "")
  .replace("<svg", '<svg role="img" aria-label="OneScreen"')
  .trim();

const wordsById = new Map(beats.words.map((w) => [w.i, w]));
const sceneById = new Map(beats.scenes.map((s) => [s.id, s]));

// `at` de una palabra, relativo al inicio de SU escena. El primer argumento se ignora
// (queda por legibilidad en las plantillas): el índice de palabra es global y único,
// así que la escena se deduce.
const at = (_ignored, i) => {
  for (const s of beats.scenes) {
    const w = s.words.find((w) => w.i === i);
    if (w) return w.at;
  }
  throw new Error(`palabra ${i} no está en ninguna escena`);
};
// Fin de una palabra, relativo a su escena. Todo lo que reacciona a que una palabra
// TERMINE de decirse tiene que usar esto: `at` devuelve el inicio, y usarlo para
// programar una salida hace que el texto empiece a irse con la voz todavía encima.
const atEnd = (_ignored, i) => {
  for (const s of beats.scenes) {
    const w = s.words.find((w) => w.i === i);
    if (w) return Math.round((w.at + w.dur) * 1e6) / 1e6;
  }
  throw new Error(`palabra ${i} no está en ninguna escena`);
};
const isAccent = (sceneId, i) => !!sceneById.get(sceneId).words.find((w) => w.i === i)?.accent;

// Palabras que ya tienen que estar COMPUESTAS en el primer frame de su escena: la
// primera de cada escena (viaja montada en el vector de entrada de la costura) y las
// dos del portador del match-cut. Su estado visible se declara en CSS, no con un
// tl.set en la posición 0: un set de duración cero en 0 no se renderiza cuando el
// cabezal está exactamente en 0, así que el primer frame saldría en blanco.
const FIRST_WORDS = new Set([0, 18, 27, 38, 39, 43, 55, 79, 98]);

// Emite los spans de un rango de palabras [from..to] (índices globales del guion).
function spans(fid, sceneId, from, to) {
  const out = [];
  for (let i = from; i <= to; i++) {
    const w = wordsById.get(i);
    const cls = ["w", FIRST_WORDS.has(i) ? "first" : "", isAccent(sceneId, i) ? "accent" : ""]
      .filter(Boolean)
      .join(" ");
    out.push(`<span class="${cls}" id="${fid}-w${i}">${w.text}</span>`);
  }
  return out.join(" ");
}
const ids = (fid, from, to) => {
  const a = [];
  for (let i = from; i <= to; i++) a.push(`"#${fid}-w${i}"`);
  return `[${a.join(", ")}]`;
};

// ---- CSS base ---------------------------------------------------------------
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
  background: ${GROUND};
  color: ${INK};
  font-family: "Rubik", sans-serif;
  -webkit-font-smoothing: antialiased;
}
.stage { position: absolute; inset: 0; display: grid; place-items: center; padding: 0 8cqw; }
.stage.left { justify-items: start; text-align: left; }
/* Escenarios que posicionan a sus hijos en ABSOLUTO (3, 4, 9, 10). Tienen que ser
   bloque, no grid: place-items:center le da justify-self:center a un hijo absoluto,
   y eso lo dimensiona a su contenido en vez de respetar left:0/right:0 � con lo cual
   text-align:center deja de centrar y la línea se pega al borde izquierdo. */
.stage.abs { display: block; place-items: normal; padding: 0; }
.block { display: block; max-width: 80cqw; text-align: center; margin-top: -1.2cqh; }
.stage.left .block { text-align: left; }
/* Estado inicial en CSS, nunca en un tl.set en la posición 0.
   Se oculta con OPACITY, jamás con la propiedad visibility: esa se HEREDA, y un hijo
   puesto en visible anula el hidden que el framework le aplica al clip padre. El
   resultado es que todas las escenas se dibujan encima de todas a la vez. */
.w { display: inline-block; opacity: 0; will-change: transform; }
.w.first { opacity: 1; }
.t-micro    { font-size: 0.95cqw; font-weight: 500; letter-spacing: 0.22em; text-transform: uppercase; }
.t-body     { font-size: 1.9cqw;  font-weight: 400; line-height: 1.5; }
.t-sub      { font-size: 3.0cqw;  font-weight: 500; line-height: 1.25; letter-spacing: -0.010em; }
.t-phrase   { font-size: 5.0cqw;  font-weight: 500; line-height: 1.10; letter-spacing: -0.022em; }
.t-display  { font-size: 7.6cqw;  font-weight: 600; line-height: 1.02; letter-spacing: -0.030em; }
.t-colossal { font-size: 15cqw;   font-weight: 800; line-height: 0.92; letter-spacing: -0.045em; }
.muted  { color: ${MUTED}; }
.accent { color: #3976ff; }
.line { display: block; }
.rule {
  display: block; width: 12cqw; height: 0.45cqh;
  background: #3976ff; margin: 3.2cqh auto 0;
}
`.trim();

// ---- helpers de línea de tiempo (se inyectan en cada composición) -----------
const TL_HELPERS = `
// Entrada de palabra: opacidad binaria + desplazamiento desde abajo. Nunca un fade.
function word(tl, sel, t, weight) {
  var Y = { heavy: ${WORD_Y.heavy}, normal: ${WORD_Y.normal}, light: ${WORD_Y.light} }[weight || "normal"];
  var D = { heavy: ${WORD_DUR.heavy}, normal: ${WORD_DUR.normal}, light: ${WORD_DUR.light} }[weight || "normal"];
  tl.set(sel, { opacity: 1 }, t);
  // immediateRender:false o GSAP escribe el estado inicial al CONSTRUIR la línea de
  // tiempo, no al llegar el cabezal � y el elemento se ve desplazado desde el frame 0.
  tl.fromTo(sel, { y: Y }, { y: 0, duration: D, ease: "power4.out", immediateRender: false }, t);
}
// Reparte una lista de palabras sobre sus tiempos.
function words(tl, list, weight) {
  for (var k = 0; k < list.length; k++) word(tl, list[k][0], list[k][1], weight);
}
// SALIDA de costura (cut-the-curve): power4.in escalonado en orden de lectura, con el
// fundido de la �aLTIMA palabra muriendo 0.02 s antes del corte � así nada queda
// congelado en el corte y tampoco hay hueco muerto.
function seamExit(tl, sels, cut, axis, dir) {
  var n = sels.length;
  var span = n > 1 ? 0.14 : 0;              // ventana del escalonado
  var step = n > 1 ? span / (n - 1) : 0;
  // Se ancla por el FINAL: el último elemento en salir termina de apagarse 0.02 s
  // antes del corte. Así no queda aire muerto justo antes del cambio de escena, y
  // el desplazamiento (0.34 s) sigue corriendo al 59% cuando cae el corte — que es
  // lo que exige la ley: cortar a media trayectoria, nunca con el gesto ya resuelto.
  var t0 = cut - ${EXIT_LEAD} - span;
  for (var k = 0; k < n; k++) {
    var t = t0 + step * k;
    var to = { duration: ${EXIT_DUR}, ease: "power4.in" };
    to[axis] = ${TRAVEL} * dir;
    tl.to(sels[k], to, t);
    // Fundido lineal, retrasado respecto al desplazamiento: ver EXIT_FADE_DELAY.
    tl.to(sels[k], { opacity: 0, duration: ${EXIT_FADE}, ease: "none" }, t + ${EXIT_FADE_DELAY});
  }
}
// ENTRADA de costura: arranca a media trayectoria (opacidad ${ENTRY_OPACITY}), power4.out.
function seamEntry(tl, sel, axis, dir) {
  var from = { opacity: ${ENTRY_OPACITY} };
  from[axis] = -${TRAVEL} * dir;
  var to = { opacity: 1, duration: ${ENTRY_DUR}, ease: "power4.out" };
  to[axis] = 0;
  tl.fromTo(sel, from, to, 0);
}
// Inverse zoom � SALIDA: todo se encoge (retrocede). Sign de d(escala)/dt negativo.
function zoomOutExit(tl, sel, cut) {
  tl.to(sel, { scale: 0.8, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }, cut - 0.2);
  tl.to(sel, { opacity: 0.15, duration: 0.2, ease: "none" }, cut - 0.2);
}
// Inverse zoom � ENTRADA: llega sobredimensionado y se repliega. Mismo signo.
function zoomOutEntry(tl, sel) {
  tl.fromTo(
    sel,
    { scale: 1.25, filter: "blur(10px)", opacity: 0.15 },
    { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.5, ease: "expo.out" },
    0
  );
}
`.trim();

// ---- definición de los 10 cuadros ------------------------------------------
const FRAMES = [];

// ============================ 01 � Espacios =================================
FRAMES.push({
  id: "01-espacios",
  fid: "f01",
  sceneId: "01",
  css: `
#f01-lineA { margin-bottom: 1.2cqh; }
#f01-lineB { opacity: 0; }`,
  body: (fid) => `
      <div class="stage">
        <div class="block t-phrase">
          <span class="line" id="f01-lineA">${spans(fid, "01", 0, 6)}</span>
          <span class="line" id="f01-lineB">${spans(fid, "01", 7, 17)}</span>
        </div>
      </div>`,
  js: (fid, s) => `
        // Verso 1 � plano a propósito: su trabajo es hacer que el segundo pese.
        // La palabra 0 abre el film ya compuesta (clase .first en CSS); no tiene
        // entrada porque no hay nada antes de ella de lo que entrar.
        words(tl, [${range(fid, "01", 1, 6)}]);
        // Sale entero hacia arriba en 2.02 s y deja 0.26 s de cuadro vacío. Ese vacío
        // ES el gesto: el film enseña un espacio que solo ocupa un lugar.
        // Arranca cuando "lugar." TERMINA de decirse (2.02 s), no cuando empieza.
        tl.to("#f01-lineA", { y: -${TRAVEL * 0.55}, duration: 0.30, ease: "power4.in" }, ${atEnd(fid, 6)});
        tl.to("#f01-lineA", { opacity: 0, duration: 0.12, ease: "none" }, ${atEnd(fid, 6) + 0.10});

        // Verso 2 � entra palabra por palabra. "cambian" es el primer azul del film.
        tl.set("#f01-lineB", { opacity: 1 }, ${at(fid, 7) - 0.02});
        words(tl, [${range(fid, "01", 7, 17)}]);

        // Costura hacia la noche: UP. La lleva el CONTENEDOR, no las palabras sueltas:
        // el ledger nombra a #f01-lineB como portador y el verificador mide ese
        // elemento. Si el desplazamiento vive solo en los hijos, el portador está
        // quieto en el corte y la continuidad de vector no existe.
        seamExit(tl, ["#f01-lineB"], ${s.duration}, "y", -1);`,
});

// ============================ 02 � Noche ====================================
FRAMES.push({
  id: "02-noche",
  fid: "f02",
  sceneId: "02",
  css: `
/* En la variante de croma el bloque nocturno también va en verde: al keyear quedan
   el verso y las estrellas en blanco flotando sobre el metraje del editor, sin
   fondo. Decisión del usuario — el negro deja de ser contenido y pasa a ser algo
   que él pone en Premiere si lo quiere. */
#root { background: ${IS_KEY ? GROUND : "#050507"}; color: #ffffff; }
/* Campo estelar: radial-gradients ESTÁTICOS, posiciones escritas a mano.
   Nada de Math.random() � el render tiene que ser determinista. No parpadean. */
/* Radios dimensionados para 3840 px, no para 1920: un punto de 2 px sobre este
   lienzo es el 0.05 % del ancho y desaparece — además h264 se lo come. Estos van
   entre 6 y 11 px, que siguen siendo el 0.16-0.29 % del ancho: sutiles, pero ahí. */
#f02-stars {
  position: absolute; inset: -3cqh 0;
  background-image:
    radial-gradient(9px 9px at 12% 18%, rgba(255,255,255,0.78), transparent 62%),
    radial-gradient(6px 6px at 27% 71%, rgba(255,255,255,0.52), transparent 62%),
    radial-gradient(11px 11px at 41% 12%, rgba(255,255,255,0.62), transparent 62%),
    radial-gradient(6px 6px at 55% 84%, rgba(255,255,255,0.42), transparent 62%),
    radial-gradient(9px 9px at 63% 33%, rgba(255,255,255,0.68), transparent 62%),
    radial-gradient(6px 6px at 74% 62%, rgba(255,255,255,0.36), transparent 62%),
    radial-gradient(8px 8px at 86% 24%, rgba(255,255,255,0.58), transparent 62%),
    radial-gradient(6px 6px at 92% 78%, rgba(255,255,255,0.46), transparent 62%),
    radial-gradient(6px 6px at 8% 52%, rgba(255,255,255,0.34), transparent 62%),
    radial-gradient(8px 8px at 34% 44%, rgba(255,255,255,0.28), transparent 62%),
    radial-gradient(6px 6px at 48% 60%, rgba(255,255,255,0.32), transparent 62%),
    radial-gradient(7px 7px at 68% 8%, rgba(255,255,255,0.40), transparent 62%),
    radial-gradient(8px 8px at 19% 88%, rgba(255,255,255,0.30), transparent 62%),
    radial-gradient(6px 6px at 79% 91%, rgba(255,255,255,0.26), transparent 62%),
    radial-gradient(7px 7px at 57% 22%, rgba(255,255,255,0.44), transparent 62%),
    radial-gradient(6px 6px at 23% 36%, rgba(255,255,255,0.30), transparent 62%),
    radial-gradient(9px 9px at 88% 55%, rgba(255,255,255,0.50), transparent 62%),
    radial-gradient(6px 6px at 44% 93%, rgba(255,255,255,0.28), transparent 62%);
  background-repeat: no-repeat;
}
#f02-line { opacity: 0; }`,
  body: (fid) => `
      <div class="stage">
        <span id="f02-stars"></span>
        <div class="block t-display">
          <span class="line" id="f02-line">${spans(fid, "02", 18, 26)}</span>
        </div>
      </div>`,
  js: (fid, s) => `
        // Entra montada en el vector UP que traía el cuadro 1: sin arrancar del reposo.
        seamEntry(tl, "#f02-line", "y", -1);
        // Solo la PRIMERA palabra viaja con la costura (ya compuesta vía .first);
        // las demás entran en su propio timestamp.
        words(tl, [${range(fid, "02", 19, 26)}]);

        // Deriva del campo estelar: lenta, constante y en el MISMO sentido que el texto.
        // No es un vaivén � avanza y termina. 26 px en 2.5 s se lee como profundidad.
        tl.fromTo("#f02-stars", { y: 13 }, { y: -13, duration: ${s.duration}, ease: "none" }, 0);

        // Salida de la noche: UP otra vez. Dos costuras seguidas en el mismo sentido,
        // sin ping-pong.
        seamExit(tl, ["#f02-line"], ${s.duration}, "y", -1);`,
});

// ============================ 03 � Falta una cosa ===========================
FRAMES.push({
  id: "03-falta-una-cosa",
  fid: "f03",
  sceneId: "03",
  css: `
/* Posicionamiento ABSOLUTO, no flujo centrado: #f03-carrier tiene que caer en la
   misma caja exacta que #f04-carrier para que el match-cut funcione. Si el bloque
   se centrara por flujo, la altura distinta de cada cuadro movería la línea. */
#f03-lead { position: absolute; left: 0; right: 0; top: 40cqh; text-align: center; padding: 0 8cqw; opacity: 0; }
#f03-carrier { position: absolute; left: 0; right: 0; top: 50cqh; text-align: center; padding: 0 8cqw; opacity: 0; }`,
  body: (fid) => `
      <div class="stage abs">
        <span class="t-sub muted" id="f03-lead">${spans(fid, "03", 27, 35)}</span>
        <span class="t-display" id="f03-carrier">${spans(fid, "03", 36, 37)}</span>
      </div>`,
  js: (fid, s) => `
        // Vuelve el blanco montado en el mismo vector UP. Respirar.
        seamEntry(tl, "#f03-lead", "y", -1);
        words(tl, [${range(fid, "03", 28, 35)}], "light");

        // "una cosa." aterriza sola y se queda QUIETA 1.2 s. Esa quietud prepara el
        // corte: el cuadro no se apaga, se enfoca. Es la pausa antes del clímax.
        tl.set("#f03-carrier", { opacity: 1 }, ${at(fid, 36) - 0.02});
        words(tl, [${range(fid, "03", 36, 37)}], "heavy");
        tl.to("#f03-lead", { opacity: 0.35, duration: 0.45, ease: "power2.out" }, ${at(fid, 36)});

        // NO hay salida de costura: #f03-carrier es el PORTADOR del match-cut y
        // cruza el corte quieto, en la misma caja que "Esa cosa." del cuadro 4.`,
});

// ============================ 04 � OneScreen ================================
FRAMES.push({
  id: "04-onescreen",
  fid: "f04",
  sceneId: "04",
  css: `
/* MISMA caja que #f03-carrier: top 50cqh, t-display, centrado. Es el otro lado del
   match-cut; si se mueve uno hay que mover el otro. transform-origin arriba-centro
   para que al encoger el borde superior no se desplace. */
#f04-carrier { position: absolute; left: 0; right: 0; top: 50cqh; text-align: center; padding: 0 8cqw; transform-origin: 50% 0%; }
#f04-lead { position: absolute; left: 50%; top: 33cqh; margin-left: 2.2cqw; white-space: nowrap; opacity: 0; }
#f04-hero { position: absolute; left: 0; right: 0; top: 44cqh; text-align: center; opacity: 0; }
#f04-rule { position: absolute; left: 50%; top: 72cqh; margin-left: -6cqw; margin-top: 0; opacity: 0; transform-origin: 50% 50%; }`,
  body: (fid) => `
      <div class="stage abs">
        <span class="t-display" id="f04-carrier">${spans(fid, "04", 38, 39)}</span>
        <span class="t-sub muted" id="f04-lead">${spans(fid, "04", 40, 41)}</span>
        <span class="t-colossal" id="f04-hero">${spans(fid, "04", 42, 42)}</span>
        <span class="rule" id="f04-rule"></span>
      </div>`,
  js: (fid, s) => `
        // MATCH-CUT: "Esa cosa." ya está compuesta en el frame del corte, en la misma
        // caja que dejó "una cosa.". Durante un frame el espectador no sabe que hubo
        // corte: solo ve que la palabra "cosa" sobrevivió.
        // Después el portador se encoge a t-sub y sube a su sitio definitivo, dejando
        // hueco a la derecha para "Es una". 7.6cqw �  3.0cqw es un factor de 0.395;
        // 50cqh �  33cqh son -367 px con el origen en el borde superior.
        tl.to("#f04-carrier", { scale: 0.395, y: -367, x: -200, duration: 0.34, ease: "power3.inOut" }, 0.30);
        tl.to("#f04-carrier", { color: "${MUTED}", duration: 0.34, ease: "none" }, 0.30);

        tl.set("#f04-lead", { opacity: 1 }, ${at(fid, 40) - 0.02});
        words(tl, [${range(fid, "04", 40, 41)}], "light");

        // "OneScreen." � primera de las DOS únicas apariciones de colossal.
        // Negro sobre blanco: el nombre no necesita ayuda.
        tl.set("#f04-hero", { opacity: 1 }, ${at(fid, 42) - 0.02});
        word(tl, "#${fid}-w42", ${at(fid, 42)}, "heavy");

        // El filete es el único acento del cuadro. Se DIBUJA, no aparece.
        tl.set("#f04-rule", { opacity: 1 }, ${at(fid, 42) + 0.14});
        tl.fromTo("#f04-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, ${at(fid, 42) + 0.14});

        // Costura: inverse zoom. La cámara se repliega del nombre al argumento.
        zoomOutExit(tl, "#f04-hero", ${s.duration});
        zoomOutExit(tl, "#f04-carrier", ${s.duration});
        zoomOutExit(tl, "#f04-lead", ${s.duration});
        zoomOutExit(tl, "#f04-rule", ${s.duration});`,
});

// ============================ 05 � Más que tecnología =======================
FRAMES.push({
  id: "05-mas-que-tecnologia",
  fid: "f05",
  sceneId: "05",
  css: `
#f05-block { opacity: 0; }
#f05-lead { display: block; margin-bottom: 1.4cqh; }
#f05-body { display: block; }`,
  body: (fid) => `
      <div class="stage">
        <div class="block" id="f05-block">
          <span class="line t-sub muted" id="f05-lead">${spans(fid, "05", 43, 45)}</span>
          <span class="line t-phrase" id="f05-body">${spans(fid, "05", 46, 54)}</span>
        </div>
      </div>`,
  js: (fid, s) => `
        // Llega sobredimensionado y se repliega: mismo signo de escala que la salida
        // del cuadro 4 (todo encoge). Nada de crecer-desde-pequeño aquí.
        zoomOutEntry(tl, "#f05-block");
        words(tl, [${range(fid, "05", 44, 45)}], "light");
        words(tl, [${range(fid, "05", 46, 54)}]);

        // "tecnología." aparece YA apagada: la palabra se dice y se descarta en el
        // mismo gesto, que es exactamente lo que hace la frase.
        tl.set("#${fid}-w54", { color: "${MUTED}" }, ${at(fid, 54)});

        // Costura: LEFT, la corriente del film.
        seamExit(tl, ["#f05-block"], ${s.duration}, "x", -1);`,
});

// ============================ 06 � Las tres pruebas =========================
FRAMES.push({
  id: "06-tres-pruebas",
  fid: "f06",
  sceneId: "06",
  css: `
#f06-block { opacity: 0; }
.proof { display: block; margin-bottom: 1.3cqh; }
#f06-p2, #f06-p3 { opacity: 0; }
#f06-grande {
  display: block; margin-top: 0.4cqh;
  font-size: 7.6cqw; font-weight: 600; line-height: 1.02; letter-spacing: -0.030em;
  opacity: 0; transform-origin: 0% 50%;
}`,
  body: (fid) => `
      <div class="stage left">
        <div class="block t-sub" id="f06-block">
          <span class="proof" id="f06-p1">${spans(fid, "06", 55, 62)}</span>
          <span class="proof" id="f06-p2">${spans(fid, "06", 63, 69)}</span>
          <span class="proof" id="f06-p3">${spans(fid, "06", 70, 77)}<span class="accent" id="f06-grande">${spans(fid, "06", 78, 78)}</span></span>
        </div>
      </div>`,
  js: (fid, s) => `
        seamEntry(tl, "#f06-block", "x", -1);
        words(tl, [${range(fid, "06", 56, 62)}], "light");

        // Cada línea que entra APAGA a las anteriores � no las borra, las baja de tono.
        tl.set("#f06-p2", { opacity: 1 }, ${at(fid, 63) - 0.02});
        words(tl, [${range(fid, "06", 63, 69)}], "light");
        tl.to("#f06-p1", { color: "${MUTED}", duration: 0.35, ease: "none" }, ${at(fid, 63)});

        tl.set("#f06-p3", { opacity: 1 }, ${at(fid, 70) - 0.02});
        words(tl, [${range(fid, "06", 70, 77)}], "light");
        tl.to("#f06-p2", { color: "${MUTED}", duration: 0.35, ease: "none" }, ${at(fid, 70)});

        // "grande." rompe el eje: escala de sub a display en 0.30 s. La frase dice que
        // ahora se ve en grande; la tipografía lo HACE en vez de decirlo.
        // El span de la palabra arranca en opacidad 0 como todos los .w. Animar solo
        // el contenedor no la enciende: hay que encender también la palabra, o
        // "grande." — que es el remate de la escena — no llega a verse nunca.
        tl.set("#${fid}-w78", { opacity: 1 }, ${at(fid, 78)});
        tl.fromTo(
          "#f06-grande",
          { scale: 0.395, opacity: 0, y: 40 },
          { scale: 1, opacity: 1, y: 0, duration: 0.22, ease: "back.out(1.5)", immediateRender: false },
          ${at(fid, 78)}
        );

        seamExit(tl, ["#f06-block"], ${s.duration}, "x", -1);`,
});

// ============================ 07 � Creemos / transformar ====================
FRAMES.push({
  id: "07-creemos",
  fid: "f07",
  sceneId: "07",
  css: `
/* Escenario en bloque, no grid: con dos .block hijos el grid crea DOS FILAS y la
   firma queda arriba y el paralelismo abajo, en vez de compartir el mismo centro. */
#f07-sig { position: absolute; left: 8cqw; right: 8cqw; top: 43cqh; text-align: left; opacity: 0; }
#f07-block { position: absolute; left: 8cqw; right: 8cqw; top: 34cqh; text-align: left; opacity: 0; }
.anchor { display: block; white-space: nowrap; }
/* El objeto son DOS líneas, no una: "la educación normal, en educación del futuro."
   en un solo renglón a 5cqw mide 4493 px y se sale de un cuadro de 3840. */
#f07-objs { display: block; position: relative; margin-top: 0.6cqh; height: 22cqh; }
.object { display: block; position: absolute; left: 0; top: 0; width: 100%; }
.obj-line { display: block; white-space: nowrap; }
#f07-objB { opacity: 0; }`,
  body: (fid) => `
      <div class="stage abs">
        <div class="t-display" id="f07-sig">
          <span class="line">${spans(fid, "07", 79, 81)}</span>
        </div>
        <div class="t-phrase" id="f07-block">
          <span class="anchor" id="f07-anchor">${spans(fid, "07", 82, 83)}</span>
          <span id="f07-objs">
            <span class="object" id="f07-objA">
              <span class="obj-line">${spans(fid, "07", 84, 86)}</span>
              <span class="obj-line">${spans(fid, "07", 87, 90)}</span>
            </span>
            <span class="object" id="f07-objB">
              <span class="obj-line">${spans(fid, "07", 93, 93)}</span>
              <span class="obj-line">${spans(fid, "07", 94, 97)}</span>
            </span>
          </span>
        </div>
      </div>`,
  js: (fid, s) => `
        // "Creemos en eso." es la firma de la marca y merece su propio silencio: entra,
        // se sostiene 1.1 s sola, y se va antes de que aparezca el paralelismo.
        seamEntry(tl, "#f07-sig", "x", -1);
        words(tl, [${range(fid, "07", 80, 81)}], "light");
        // Sale cuando "eso." termina de decirse, no antes: la firma se lee entera.
        tl.to("#f07-sig", { y: -${TRAVEL * 0.5}, duration: 0.26, ease: "power4.in" }, ${atEnd(fid, 81) + 0.02});
        tl.to("#f07-sig", { opacity: 0, duration: 0.12, ease: "none" }, ${atEnd(fid, 81) + 0.10});

        // EL ANCLA. Entra una vez y no se mueve durante 6 s. Su quietud ES el argumento:
        // lo que cambia es el objeto, nunca el verbo.
        tl.set("#f07-block", { opacity: 1 }, ${at(fid, 82) - 0.02});
        words(tl, [${range(fid, "07", 82, 83)}], "heavy");

        // Objeto A: "la educación normal, en educación del futuro."
        words(tl, [${range(fid, "07", 84, 90)}], "light");

        // Waterfall cut a 29.22 s: el objeto A se va palabra por palabra hacia la
        // izquierda (la corriente) mientras el B entra a media trayectoria. Una ola
        // que cruza la costura, dentro de la misma escena.
        seamExit(tl, ${ids(fid, 84, 90)}, ${at(fid, 93)}, "x", -1);
        tl.set("#f07-objA", { opacity: 0 }, ${at(fid, 93)});
        tl.set("#f07-objB", { opacity: 1 }, ${at(fid, 93) - 0.02});
        words(tl, [${range(fid, "07", 93, 97)}], "light");

        // Costura: LEFT. El ancla se desvanece en su sitio y el objeto sale.
        tl.to("#f07-anchor", { opacity: 0, duration: 0.12, ease: "none" }, ${s.duration - 0.30});
        seamExit(tl, ["#f07-block"], ${s.duration}, "x", -1);`,
});

// ============================ 08 � El futuro también ========================
FRAMES.push({
  id: "08-el-futuro-tambien",
  fid: "f08",
  sceneId: "08",
  css: `
/* Igual que el 7: dos .block en un grid se reparten en dos filas. Aquí el verso y el
   clímax nunca coexisten, así que los dos van al mismo centro, en absoluto. */
#f08-line { position: absolute; left: 8cqw; right: 8cqw; top: 44cqh; text-align: center; opacity: 0; }
#f08-payoff { position: absolute; left: 0; right: 0; top: 27cqh; text-align: center; opacity: 0; }
#f08-lead { display: block; margin-bottom: -0.6cqh; }
#f08-hero {
  display: block; font-size: 22cqw; font-weight: 800; line-height: 0.9;
  letter-spacing: -0.05em;
}
#f08-tail { display: block; margin-top: -0.4cqh; }`,
  body: (fid) => `
      <div class="stage abs">
        <div class="t-phrase" id="f08-line">${spans(fid, "08", 98, 102)}</div>
        <div id="f08-payoff">
          <span class="line t-sub muted" id="f08-lead">${spans(fid, "08", 103, 103)}</span>
          <span class="accent" id="f08-hero">${spans(fid, "08", 104, 104)}</span>
          <span class="line t-sub muted" id="f08-tail">${spans(fid, "08", 105, 105)}</span>
        </div>
      </div>`,
  js: (fid, s) => `
        seamEntry(tl, "#f08-line", "x", -1);
        words(tl, [${range(fid, "08", 99, 102)}], "light");

        // La línea se va completa en 33.40 s y quedan 0.34 s de cuadro TOTALMENTE
        // vacío � el hueco real que dejó la voz. No se rellena: es el resorte del golpe.
        // Esto es la quietud-antes-del-clímax, no un tiempo muerto.
        // Se ancla al FINAL de "cambia." (33.40 s), no a un offset del clímax: así el
        // verso se lee completo y el hueco que queda antes del golpe es el real.
        seamExit(tl, ["#f08-line"], ${Math.round((atEnd(fid, 102) + EXIT_LEAD) * 1e6) / 1e6}, "x", -1);

        // EL CLÍMAX. Segunda y última aparición de colossal, y la única vez que una
        // palabra de ese tamaño va teñida.
        tl.set("#f08-payoff", { opacity: 1 }, ${at(fid, 104) - 0.02});
        word(tl, "#${fid}-w104", ${at(fid, 104)}, "heavy");
        word(tl, "#${fid}-w103", ${at(fid, 104) + 0.06}, "light");
        word(tl, "#${fid}-w105", ${at(fid, 105)}, "light");

        // Costura: inverse zoom de LLEGADA. "futuro" se repliega para que llegue la marca.
        zoomOutExit(tl, "#f08-payoff", ${s.duration});`,
});

// ============================ 09 � Lockup ===================================
FRAMES.push({
  id: "09-lockup",
  fid: "f09",
  sceneId: "09",
  css: `
#f09-block { position: absolute; inset: 0; opacity: 0; }
/* El logotipo va posicionado en absoluto y con EXACTAMENTE la misma caja que en el
   cuadro 10: es el portador del match-cut del cierre. No tocar sin tocar el otro. */
#f09-mark { position: absolute; left: 50%; top: 30cqh; width: 46cqw; margin-left: -23cqw; color: ${INK}; }
#f09-mark svg { display: block; width: 100%; height: auto; }
#f09-rule { position: absolute; left: 50%; top: 48cqh; width: 12cqw; margin-left: -6cqw; margin-top: 0; opacity: 0; transform-origin: 50% 50%; }
#f09-sign { position: absolute; left: 0; right: 0; top: 56cqh; text-align: center; }
.sign-line { display: block; }
#f09-sign2 { opacity: 0; }`,
  body: (fid) => `
      <div class="stage abs">
        <div id="f09-block">
          <span id="f09-mark">${WORDMARK_SVG}</span>
          <span class="rule" id="f09-rule"></span>
          <span class="t-phrase" id="f09-sign">
            <span class="sign-line" id="f09-sign1">${spans(fid, "09", 107, 109)}</span>
            <span class="sign-line" id="f09-sign2">${spans(fid, "09", 110, 112)}</span>
          </span>
        </div>
      </div>`,
  js: (fid, s) => `
        // LLEGADA. El logotipo entra sobredimensionado y se asienta � mismo signo de
        // escala que la salida del cuadro 8. �anica aparición de la marca en el film.
        zoomOutEntry(tl, "#f09-block");

        // El filete repite el gesto del cuadro 4, ahora cerrando el arco.
        tl.set("#f09-rule", { opacity: 1 }, 0.34);
        tl.fromTo("#f09-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, 0.34);

        words(tl, [${range(fid, "09", 107, 109)}], "light");
        tl.set("#f09-sign2", { opacity: 1 }, ${at(fid, 110) - 0.02});
        words(tl, [${range(fid, "09", 110, 112)}], "light");

        // MATCH-CUT al cuadro 10: el logotipo NO se mueve en el corte. Salen las dos
        // líneas de texto y el filete; la marca se queda. El cierre no la borra.
        tl.to(["#f09-sign1", "#f09-sign2"], { opacity: 0, duration: 0.20, ease: "none" }, ${s.duration - 0.22});
        tl.to("#f09-rule", { opacity: 0, duration: 0.20, ease: "none" }, ${s.duration - 0.22});`,
});

// ============================ 10 � Toca la pantalla =========================
FRAMES.push({
  id: "10-toca-la-pantalla",
  fid: "f10",
  sceneId: "10",
  css: `
/* Arranca con la caja EXACTA de #f09-mark � es el otro lado del match-cut. */
#f10-mark { position: absolute; left: 50%; top: 30cqh; width: 46cqw; margin-left: -23cqw; color: ${INK}; transform-origin: 50% 0%; }
#f10-mark svg { display: block; width: 100%; height: auto; }
#f10-copy { position: absolute; left: 0; right: 0; top: 46cqh; text-align: center; padding: 0 8cqw; }
#f10-lead { display: block; margin-bottom: 1.2cqh; opacity: 0; }
#f10-main { display: block; opacity: 0; }
#f10-ring {
  position: absolute; left: 50%; top: 76cqh;
  width: 9cqw; height: 9cqw; margin-left: -4.5cqw;
  border: 0.42cqh solid #3976ff; border-radius: 50%;
  opacity: 0;
}`,
  body: (fid) => `
      <div class="stage abs">
        <span id="f10-mark">${WORDMARK_SVG}</span>
        <span id="f10-copy">
          <span class="t-sub muted" id="f10-lead">${spans(fid, "10", 113, 117)}</span>
          <span class="t-display" id="f10-main">${spans(fid, "10", 118, 123)}</span>
        </span>
        <span id="f10-ring"></span>
      </div>`,
  js: (fid, s) => `
        // El logotipo cruza el corte quieto (match-cut) y RECI�0N DESPU�0S se encoge y
        // sube, con la curva de tres fases: apenas arranca, ráfaga, cola larga.
        // 46cqw �  26cqw es escala 0.565; 30cqh �  14cqh son -346 px.
        tl.to("#f10-mark", { scale: 0.957, y: -35, duration: 0.16, ease: "power3.in" }, 0.10);
        tl.to("#f10-mark", { scale: 0.674, y: -260, duration: 0.14, ease: "none" }, 0.26);
        tl.to("#f10-mark", { scale: 0.565, y: -346, duration: 0.50, ease: "power4.out" }, 0.40);

        tl.set("#f10-lead", { opacity: 1 }, ${at(fid, 113) - 0.02});
        words(tl, [${range(fid, "10", 113, 117)}], "light");
        tl.to("#f10-lead", { y: -60, opacity: 0, duration: 0.26, ease: "power4.in" }, ${at(fid, 118) - 0.26});

        tl.set("#f10-main", { opacity: 1 }, ${at(fid, 118) - 0.02});
        words(tl, [${range(fid, "10", 118, 123)}]);

        // El anillo dispara SOBRE la palabra "tocar" � mismo frame que la causa, no
        // "poco después". Un solo pulso, no un bucle.
        tl.fromTo(
          "#f10-ring",
          { scale: 0.2, opacity: 0.9 },
          { scale: 1.35, opacity: 0, duration: 0.50, ease: "power2.out", immediateRender: false },
          ${at(fid, 121)}
        );

        // LA COLA. La voz termina en 41.84 s y quedan 1.24 s. El texto se retira y el
        // logotipo sube al centro óptico: el film no termina en una palabra, termina
        // en la marca, en silencio.
        // El logotipo baja al CENTRO ÓPTICO y crece un punto. Con origen en el borde
        // superior y base en top:30cqh (648 px), quedar centrado a 48.8 cqh con
        // escala 0.72 (alto 194 px) pide y = +309.
        tl.to("#f10-copy", { opacity: 0, duration: 0.36, ease: "power2.in" }, ${s.duration - 1.10});
        tl.to("#f10-mark", { scale: 0.72, y: 309, duration: 0.80, ease: "power4.out" }, ${s.duration - 1.05});`,
});

// ---- render -----------------------------------------------------------------
// Lista [selector, tiempo] para el helper `words`.
function range(fid, sceneId, from, to) {
  const out = [];
  for (let i = from; i <= to; i++) out.push(`["#${fid}-w${i}", ${at(sceneId, i)}]`);
  return out.join(", ");
}

const indent = (s, n) => s.split("\n").map((l) => (l ? " ".repeat(n) + l : l)).join("\n");

for (const f of FRAMES) {
  const s = sceneById.get(f.sceneId);
  // Todo escenario lleva la marca de solape entre escenas � ver XSCENE.
  const body = f.body(f.fid).replace(/<div class="stage([^"]*)">/g, `<div class="stage$1" ${XSCENE}>`);
  // `at` se llama con el sceneId dentro de las plantillas js; se enlaza aquí.
  const jsSrc = f.js(f.fid, s);
  const html = `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>${f.id}</title>
  </head>
  <body>
    <template>
      <style>
${indent(BASE_CSS, 8)}
${indent(f.css.trim(), 8)}
      </style>

      <div
        id="root"
        data-composition-id="${f.id}"
        data-width="${W}"
        data-height="${H}"
        data-duration="${s.duration}"
      >
${body.replace(/^\n/, "")}
      </div>

      <script>
        window.__timelines = window.__timelines || {};
        var tl = gsap.timeline({ paused: true });

${indent(TL_HELPERS, 8)}

${jsSrc.replace(/^\n/, "")}

        window.__timelines["${f.id}"] = tl;
      </script>
    </template>
  </body>
</html>
`;
  writeFileSync(join(OUT, `${f.id}.html`), html, "utf8");
  console.log(`  ${f.id}.html  ${String(s.duration).padStart(9)}s  ${s.words.length} palabras`);
}
console.log(`\n${FRAMES.length} cuadros animados en compositions/frames/`);

