// Engancha el audio GUÍA del corte y hornea los 25 fps en la raíz de index.html.
//
// El audio es el del propio PrevSC02.mp4 y va solo para que el editor pueda alinear
// la capa por forma de onda. En Premiere se desvincula y se borra; no es parte del
// entregable. Se engancha entero, sin cortes.
//
// Los 25 fps son obligatorios: sin `data-fps` el render cae a 30 por defecto y los
// tiempos dejan de coincidir con el corte.
//
// Idempotente. Se ejecuta DESPUÉS de assemble-index.mjs, que reescribe index.html.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const INDEX = join(ROOT, "index.html");
const AUDIO = "assets/guide-audio.m4a";
const FONT = "assets/fonts/Rubik-Variable.ttf";
const FPS = "25";

for (const f of [AUDIO, FONT]) if (!existsSync(join(ROOT, f))) throw new Error(`falta ${f}`);

let html = readFileSync(INDEX, "utf8");
const changes = [];

// La raíz se localiza por data-composition-id, no por formato: el Studio reescribe
// index.html en una sola línea en cuanto se abre el preview.
const rootMatch = html.match(/<div\b[^>]*data-composition-id="main"[^>]*>/);
if (!rootMatch) throw new Error("no encontré el elemento raíz en index.html");
const rootTag = rootMatch[0];
const total = rootTag.match(/data-duration="([\d.]+)"/)?.[1];
if (!total) throw new Error("la raíz no declara data-duration");

if (!rootTag.includes("data-fps=")) {
  html = html.replace(rootTag, rootTag.replace(/>$/, ` data-fps="${FPS}">`));
  changes.push(`data-fps="${FPS}" en la raíz`);
}

if (!html.includes(`src="${AUDIO}"`)) {
  const audio = [
    ``,
    `      <!-- Audio guía del corte, para alinear la capa. Ver tools/wire-audio.mjs. -->`,
    `      <audio`,
    `        id="el-guide"`,
    `        src="${AUDIO}"`,
    `        data-start="0"`,
    `        data-duration="${total}"`,
    `        data-track-index="10"`,
    `        data-volume="1"`,
    `      ></audio>`,
  ].join("\n");
  const close = html.lastIndexOf("    </div>");
  if (close === -1) throw new Error("no encontré el cierre del root");
  html = html.slice(0, close) + audio + "\n" + html.slice(close);
  changes.push(`<audio> guía 0 → ${total}s en la pista 10`);
}

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

if (changes.length === 0) console.log("index.html ya estaba enganchado — sin cambios");
else {
  writeFileSync(INDEX, html, "utf8");
  for (const c of changes) console.log(`  + ${c}`);
}
