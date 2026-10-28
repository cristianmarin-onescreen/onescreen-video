// Genera los 10 bocetos (pase de wireframe) en compositions/frames/.
// Un boceto = el layout del cuadro en su momento clave, con las palabras reales,
// el fondo y la tinta de frame.md y un solo acento. Sin movimiento, sin decoración.
// La línea de tiempo se registra vacía: el Studio solo necesita el póster.
import { mkdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const OUT = join(ROOT, "compositions", "frames");
mkdirSync(OUT, { recursive: true });

const W = 3840;
const H = 2160;

// Escalones de frame.md. `colossal` es un rango: se ajusta a la medida de la palabra
// buscando ~78cqw de ancho, que es la regla "fit-to-measure" del spec.
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
  background: #ffffff;
  color: #000000;
  font-family: "Rubik", sans-serif;
  -webkit-font-smoothing: antialiased;
}
.stage {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 0 8cqw;
}
.stage.left { justify-items: start; text-align: left; }
.block {
  display: block;
  max-width: 80cqw;
  text-align: center;
  margin-top: -1.2cqh;   /* levante óptico — el centro geométrico se lee bajo */
}
.stage.left .block { text-align: left; }
.t-micro    { font-size: 0.95cqw; font-weight: 500; letter-spacing: 0.22em; text-transform: uppercase; }
.t-body     { font-size: 1.9cqw;  font-weight: 400; line-height: 1.5; }
.t-sub      { font-size: 3.0cqw;  font-weight: 500; line-height: 1.25; letter-spacing: -0.010em; }
.t-phrase   { font-size: 5.0cqw;  font-weight: 500; line-height: 1.10; letter-spacing: -0.022em; }
.t-display  { font-size: 7.6cqw;  font-weight: 600; line-height: 1.02; letter-spacing: -0.030em; }
.t-mega     { font-size: 11.5cqw; font-weight: 700; line-height: 0.96; letter-spacing: -0.038em; }
.t-colossal { font-size: 15cqw;   font-weight: 800; line-height: 0.92; letter-spacing: -0.045em; }
.muted  { color: #8a8a8e; }
.accent { color: #3976ff; }
.rule {
  display: block;
  width: 12cqw;          /* marca de acento, NO subrayado — por eso es corta */
  height: 0.45cqh;
  background: #3976ff;
  border-radius: 0;
  margin: 3.2cqh auto 0; /* el aire es lo que impide que se lea como subrayado */
}
.stage.left .rule { margin-left: 0; }
.lead { display: block; margin-bottom: 1.4cqh; }
.tail { display: block; margin-top: 1.4cqh; }
`.trim();

// Cada cuadro: el layout de su momento clave. `ground: "night"` invierte el suelo.
const FRAMES = [
  {
    id: "01-espacios",
    title: "Espacios",
    duration: 5.0,
    note: "Momento clave 3.7s — el primer verso ya salió; el segundo está completo.",
    css: "",
    body: `
      <div class="stage">
        <div class="block t-phrase">
          Y hay espacios que <span class="accent">cambian</span> lo que pasa dentro de ellos.
        </div>
      </div>`,
  },
  {
    id: "02-noche",
    title: "Noche",
    duration: 2.5,
    ground: "night",
    note: "Momento clave 7.0s — único bloque oscuro. El campo estelar llega en el build.",
    css: `
#root { background: #050507; color: #ffffff; }`,
    body: `
      <div class="stage">
        <div class="block t-display">
          Hay espacios que no se llenan con <span class="accent">cualquier</span> cosa.
        </div>
      </div>`,
  },
  {
    id: "03-falta-una-cosa",
    title: "Falta una cosa",
    duration: 3.583333,
    note: "Momento clave 10.4s — el verso ya se apagó; 'una cosa.' se queda sola y quieta.",
    css: "",
    body: `
      <div class="stage">
        <div class="block">
          <span class="lead t-sub muted">Y hay espacios a los que solo les <span class="accent">falta</span></span>
          <span class="t-display">una cosa.</span>
        </div>
      </div>`,
  },
  {
    id: "04-onescreen",
    title: "OneScreen",
    duration: 2.666667,
    note: "Momento clave 13.2s — 'Esa cosa.' entra en la posición exacta que dejó el cuadro 3.",
    css: "",
    body: `
      <div class="stage">
        <div class="block">
          <span class="lead t-sub muted">Esa cosa. Es una</span>
          <span class="t-colossal">OneScreen.</span>
          <span class="rule"></span>
        </div>
      </div>`,
  },
  {
    id: "05-mas-que-tecnologia",
    title: "Más que tecnología",
    duration: 4.416667,
    note: "Momento clave 17.3s — 'tecnología.' aparece ya apagada, se dice y se descarta.",
    css: "",
    body: `
      <div class="stage">
        <div class="block">
          <span class="lead t-sub muted">Porque para nosotros,</span>
          <span class="t-phrase">transformar un espacio es mucho <span class="accent">más</span> que solo <span class="muted">tecnología.</span></span>
        </div>
      </div>`,
  },
  {
    id: "06-tres-pruebas",
    title: "Las tres pruebas",
    duration: 6.375,
    note: "Momento clave 24.3s — las tres líneas acumuladas; solo la tercera sigue en negro.",
    css: `
.proof { display: block; margin-bottom: 1.3cqh; }
/* "grande." rompe el eje a propósito: propia línea, escalón display, acento. */
.grande {
  display: block;
  margin-top: 0.4cqh;
  font-size: 7.6cqw;
  font-weight: 600;
  line-height: 1.02;
  letter-spacing: -0.030em;
}`,
    body: `
      <div class="stage left">
        <div class="block t-sub">
          <span class="proof muted">Es una clase que por fin se entiende.</span>
          <span class="proof muted">Es un equipo que toma mejores decisiones.</span>
          <span class="proof">Es una idea, que ahora se ve en<span class="grande accent">grande.</span></span>
        </div>
      </div>`,
  },
  {
    id: "07-creemos",
    title: "Creemos / transformar",
    duration: 7.25,
    note: "Momento clave 31.4s — el ancla 'En transformar' lleva 6s sin moverse; rota el objeto.",
    css: `
/* El ancla vive en su propia línea y no se mueve en 6 s; debajo rota el objeto.
   Ponerlos lado a lado desbordaba los 80cqw y partía "En / transformar" en dos. */
.anchor { display: block; white-space: nowrap; }
.object { display: block; white-space: nowrap; margin-top: 0.6cqh; }`,
    body: `
      <div class="stage left">
        <div class="block t-phrase">
          <span class="anchor">En transformar</span>
          <span class="object">empresas del <span class="accent">futuro.</span></span>
        </div>
      </div>`,
  },
  {
    id: "08-el-futuro-tambien",
    title: "El futuro también",
    duration: 3.0,
    note: "Momento clave 34.3s — el clímax. Única palabra colossal teñida del film.",
    css: `
.hero { display: block; font-size: 22cqw; font-weight: 800; line-height: 0.9; letter-spacing: -0.05em; }
/* "El" y "también." se pegan a la palabra: su trabajo es dar escala por contraste,
   no flotar sueltas. Márgenes cortos, no los 1.4cqh por defecto. */
.hero-lead { display: block; margin-bottom: -0.6cqh; }
.hero-tail { display: block; margin-top: -0.4cqh; }`,
    body: `
      <div class="stage">
        <div class="block">
          <span class="hero-lead t-sub muted">El</span>
          <span class="hero accent">futuro</span>
          <span class="hero-tail t-sub muted">también.</span>
        </div>
      </div>`,
  },
  {
    id: "09-lockup",
    title: "Lockup",
    duration: 3.416667,
    note: "Momento clave 37.6s — única aparición del logotipo, en vector.",
    css: `
.mark { display: block; width: 46cqw; margin: 0 auto; color: #000000; }
.mark img { display: block; width: 100%; height: auto; }
.sign { display: block; margin-top: 4.4cqh; }
.sign-line { display: block; }   /* sin <br>: lo prohíben las reglas de determinismo */`,
    body: `
      <div class="stage">
        <div class="block">
          <span class="mark"><img id="f09-wordmark" src="assets/onescreen-wordmark.svg" alt="OneScreen" /></span>
          <span class="rule"></span>
          <span class="sign t-phrase">
            <span class="sign-line">Transforma el espacio.</span>
            <span class="sign-line">Transforma el <span class="accent">futuro.</span></span>
          </span>
        </div>
      </div>`,
  },
  {
    id: "10-toca-la-pantalla",
    title: "Toca la pantalla",
    duration: 4.875,
    note: "Momento clave 41.5s — el anillo de toque dispara sobre la palabra 'tocar'.",
    css: `
/* El anillo baja al tercio inferior, lejos del texto: pegado bajo "pantalla."
   se leía como una viñeta. Y es grande, porque representa un dedo, no un punto. */
.ring {
  position: absolute;
  left: 50%;
  top: 74cqh;
  width: 9cqw;
  height: 9cqw;
  margin-left: -4.5cqw;
  border: 0.42cqh solid #3976ff;
  border-radius: 50%;
}
.mark-small { position: absolute; left: 50%; top: 14cqh; width: 26cqw; margin-left: -13cqw; }
.mark-small img { display: block; width: 100%; height: auto; }
.cta-lead { display: block; margin-bottom: 1.2cqh; }`,
    body: `
      <div class="stage">
        <span class="mark-small"><img id="f10-wordmark" src="assets/onescreen-wordmark.svg" alt="OneScreen" /></span>
        <div class="block">
          <span class="cta-lead t-sub muted">Tu transformación puede comenzar ya,</span>
          <span class="t-display">solo tienes que tocar la <span class="accent">pantalla.</span></span>
        </div>
        <span class="ring"></span>
      </div>`,
  },
];

const file = (f) => `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>${f.title} — boceto</title>
  </head>
  <body>
    <template>
      <style>
${BASE_CSS.split("\n").map((l) => (l ? "        " + l : l)).join("\n")}${
  f.css ? "\n" + f.css.trim().split("\n").map((l) => (l ? "        " + l : l)).join("\n") : ""
}
      </style>

      <div
        id="root"
        data-composition-id="${f.id}"
        data-width="${W}"
        data-height="${H}"
        data-duration="${f.duration}"
      >
        <!-- BOCETO: ${f.note} -->
${f.body.replace(/^\n/, "").replace(/^ {6}/gm, "        ")}
      </div>

      <script>
        // Pase de boceto: sin movimiento. La línea de tiempo se registra vacía
        // para que el Studio pueda montar el cuadro y sacar su póster.
        window.__timelines = window.__timelines || {};
        window.__timelines["${f.id}"] = gsap.timeline({ paused: true });
      </script>
    </template>
  </body>
</html>
`;

for (const f of FRAMES) {
  writeFileSync(join(OUT, `${f.id}.html`), file(f), "utf8");
  console.log(`  ${f.id}.html  ${String(f.duration).padStart(9)}s  ${f.title}`);
}
console.log(`\n${FRAMES.length} bocetos en compositions/frames/`);
