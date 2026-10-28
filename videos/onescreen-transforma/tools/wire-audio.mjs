// Engancha la narración maestra a index.html — y la engancha ENTERA.
//
// Por qué no se usa `audio_meta.json`: ese contrato es por cuadro
// (`voices: [{ frame, path }]`) y assemble-index le pone a cada <audio> la
// duración de su cuadro. Eso obligaría a partir `narration.wav` en 10 pedazos.
// La locución tiene colas de reverberación que cruzan los límites de escena
// (p. ej. "una cosa." termina en 10.70 s pero su cola sigue sonando pasado el
// corte de 11.083 s), así que cortarla se oiría como un tijeretazo. El usuario
// pidió explícitamente no modificar el audio.
//
// Solución: un solo <audio> de longitud completa en la pista 10. La pista 1
// (cuadros) y la 10 (voz) son lanes distintas, así que no hay solape ilegal.
//
// Idempotente: correr dos veces no duplica nada. Se ejecuta DESPUÉS de
// assemble-index.mjs, que reescribe index.html desde cero.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const INDEX = join(ROOT, "index.html");
const NARRATION = "assets/narration.wav";
const FONT = "assets/fonts/Rubik-Variable.ttf";

if (!existsSync(join(ROOT, NARRATION))) throw new Error(`falta ${NARRATION}`);
if (!existsSync(join(ROOT, FONT))) throw new Error(`falta ${FONT}`);

let html = readFileSync(INDEX, "utf8");
const changes = [];

// El elemento raíz. Se localiza por data-composition-id="main" y no por formato: el
// Studio reescribe index.html en una sola línea y le añade atributos data-hf-id en
// cuanto se abre el preview, así que cualquier regex atada al salto de línea se rompe.
const rootRe = /<div\b[^>]*data-composition-id="main"[^>]*>/;
const rootMatch = html.match(rootRe);
if (!rootMatch) throw new Error("no encontré el elemento raíz en index.html");
const rootTag = rootMatch[0];

const dur = rootTag.match(/data-duration="([\d.]+)"/);
if (!dur) throw new Error("la raíz no declara data-duration");
const total = dur[1];

if (!html.includes(`src="${NARRATION}"`)) {
  const audio = [
    ``,
    `      <!-- Narración maestra: una sola pieza, sin cortes. Ver tools/wire-audio.mjs. -->`,
    `      <audio`,
    `        id="el-narration"`,
    `        src="${NARRATION}"`,
    `        data-start="0"`,
    `        data-duration="${total}"`,
    `        data-track-index="10"`,
    `        data-volume="1"`,
    `      ></audio>`,
  ].join("\n");
  // Antes del cierre del root (el último </div> antes de </body>).
  const close = html.lastIndexOf("    </div>");
  if (close === -1) throw new Error("no encontré el cierre del root");
  html = html.slice(0, close) + audio + "\n" + html.slice(close);
  changes.push(`<audio> narración 0 → ${total}s en la pista 10`);
}

// 24 fps horneado en la raíz. Sin esto el render cae a 30 por defecto y los cortes
// dejan de caer en frontera de frame, que es toda la premisa del montaje.
if (!rootTag.includes("data-fps=")) {
  html = html.replace(rootTag, rootTag.replace(/>$/, ' data-fps="24">'));
  changes.push('data-fps="24" en la raíz');
}

// Rubik en el <head> del anfitrión: se descarga una vez y está lista antes de
// que monte el primer cuadro. Las sub-composiciones la vuelven a declarar
// (el navegador deduplica por URL), pero ahí llega tarde para el primer frame.
if (!html.includes("@font-face")) {
  const face = `      @font-face {
        font-family: "Rubik";
        src: url("${FONT}") format("truetype");
        font-weight: 300 900;
        font-style: normal;
        font-display: block;
      }
`;
  html = html.replace("    <style>\n", `    <style>\n${face}`);
  changes.push("@font-face Rubik en el <head>");
}

if (changes.length === 0) {
  console.log("index.html ya estaba enganchado — sin cambios");
} else {
  writeFileSync(INDEX, html, "utf8");
  for (const c of changes) console.log(`  + ${c}`);
}
