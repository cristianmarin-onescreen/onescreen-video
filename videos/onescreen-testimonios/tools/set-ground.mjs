// Pinta el suelo del ANFITRIÓN (index.html) del color que se le pase.
//
// Va aparte de build-frames.mjs porque son dos capas distintas: ese script pinta el
// #root de cada sub-composición, y este pinta el #root del index y el body. Las dos
// tienen que coincidir o el compositor deja un borde del color viejo — la guía del
// framework avisa de que el background del propio elemento raíz puede caerse en el
// compositado, así que se pintan ambas capas a propósito.
//
//   node tools/set-ground.mjs "#00FF00"   → variante de croma
//   node tools/set-ground.mjs "#ffffff"   → film original
//
// Idempotente y sin regex atadas al formato: el Studio reescribe index.html en una
// sola línea en cuanto se abre el preview.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const INDEX = join(HERE, "..", "index.html");

const ground = (process.argv[2] || "").trim();
if (!/^#[0-9a-fA-F]{6}$/.test(ground) && ground !== "transparent") {
  throw new Error(`suelo inválido: "${ground}" — se espera #rrggbb o "transparent"`);
}

let html = readFileSync(INDEX, "utf8");
const before = html;

// #root { … background: <algo>; } — se reemplaza solo el valor, dentro de esa regla.
html = html.replace(/(#root\s*\{[^}]*background:\s*)(#[0-9a-fA-F]{3,8}|[a-zA-Z]+)/, `$1${ground}`);
// html, body { … background: <algo>; } — el negro del scaffold asomaría por los bordes.
html = html.replace(/(html,\s*\n?\s*body\s*\{[^}]*background:\s*)(#[0-9a-fA-F]{3,8}|[a-zA-Z]+)/, `$1${ground}`);

if (html === before) {
  console.log(`sin cambios — index.html ya estaba en ${ground} (o no se encontró la regla)`);
} else {
  writeFileSync(INDEX, html, "utf8");
  console.log(`suelo del anfitrión → ${ground}`);
}
