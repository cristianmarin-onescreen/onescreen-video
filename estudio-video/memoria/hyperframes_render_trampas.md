---
name: hyperframes-render-trampas
description: "Tres fallos de HyperFrames que solo aparecen en el MP4 (no en preview/snapshot) — GSAP lazy/immediateRender:false, puntas redondas en trazos ocultos, disco C: lleno."
metadata:
  node_type: memory
  type: feedback
  originSessionId: d0aa621e-3e8e-4f07-bae5-e68e2cccafc8
  modified: 2026-10-02T21:11:07.296Z
---

Aprendido en el video Flota de IA (2-oct-2026, `videos/onescreen-flota-ia`). Cristian vio en el MP4 "problemas de opacidad" que la vista previa no mostraba.

1. **Nunca `immediateRender: false` con un estado inicial visible**, y siempre `gsap.defaults({ lazy: false })` en un script compartido. El render captura cada cuadro apenas busca la posición; los valores diferidos de GSAP no se aplican a tiempo → partículas que no salen, líneas de escaneo invisibles. Patrón seguro: `fromTo` de posición (immediateRender por defecto) + `fromTo({opacity:0},{opacity:1,duration:0.01})` aparte (`FX.show` en `assets/fx.js` de ese proyecto). Los `<circle>` animados por `attr` necesitan `cx`/`cy` iniciales o la consola tira errores.
2. **Trazos "por dibujar" con `pathLength=1`: usar `stroke-dasharray: 1 2`, no `1`.** Con `1` y `stroke-linecap: round` queda un punto visible en el inicio del trazo antes de dibujarse.
3. **C: está casi lleno (~0.5 GB)**: renderizar con salida en D: y `TMP/TEMP` + `--frames-cache-dir` en D:. Si el MP4 destino está abierto en un reproductor, el render termina pero falla al renombrar y BORRA el archivo nuevo → usar un nombre nuevo (v2, v3…).

**Why:** `hyperframes snapshot` recarga por cuadro y no reproduce estos fallos; solo el MP4 los muestra.
**How to apply:** antes de entregar un render, extraer tiras de fotogramas con ffmpeg en los momentos de partículas/escaneos/paquetes y mirarlas. Relacionado: [[builds-java-loopback-windows]] (otro problema de entorno de este equipo), [[marca-tipografia-onescreen]].
