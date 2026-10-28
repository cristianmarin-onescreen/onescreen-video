# Asset inventory

Ruta **no-capture**. El capture de `https://onescreenlatam.com` fue rechazado por la
protección de acceso del sitio (HTTP 403, `Just a moment...` — challenge de Cloudflare
contra tráfico automatizado). No se consumió ningún resultado parcial. El brief ya
traía el material fuente, así que la ruta no-capture es válida y además es la
correcta para este film: es lettering puro, sin capturas de producto.

## assets/

- `onescreen-wordmark.svg` — **logotipo oficial OneScreen**, vector limpio,
  `viewBox="0 0 827.95 126.01"` (ratio 6.57:1), incluye el símbolo ®. Origen: archivo
  de marca de la propia empresa (`D:\OneScreen\Contenido\2026\4. Abril\Mesa México\SVG\Logotipo_Vector.svg`).
  El archivo original venía en variante blanca (`fill="#fff"`); se cambió a
  `fill="currentColor"` para poder teñirlo por CSS (negro sobre blanco, blanco sobre
  negro, o #3976ff) sin duplicar archivos. Vector ⇒ nítido a 3840x2160 sin límite.
  **Uso: exclusivamente el lockup de cierre.** No aparece antes.

- `narration-main-v1.wav` — locución maestra ya producida (ElevenLabs, voz "Hale –
  Expressive, Deep and Emotive"). PCM 16-bit, 48 kHz, estéreo, 43.080 s.
  Habla de 0.000 s a 41.840 s; cola de silencio de 1.24 s.
  **Es la banda maestra del film.** No se regenera ni se recorta.

## Timings

`transcript/words.json` — 124 palabras con timestamps de inicio/fin, extraídos de la
locución real con whisper `large-v3-turbo` (español, sin traducción). El texto
transcrito coincide palabra por palabra con el guion entregado por el usuario; el
guion escrito manda para la ortografía (acentos), los timings mandan para la
sincronía.

## No disponible

- Capturas del sitio: bloqueadas por Cloudflare, y no requeridas por el brief.
- Tokens de marca extraídos del DOM: no disponibles. La paleta la fija el brief
  del usuario (blanco / #3976ff / negro) y la tipografía es Rubik por instrucción
  directa.
