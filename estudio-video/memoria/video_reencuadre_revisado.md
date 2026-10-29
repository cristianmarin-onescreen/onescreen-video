---
name: video-reencuadre-revisado
description: "29-oct-2026: Cris notó que reencuadro a 9:16/4:5/1:1 sin mirar; ahora revisar_encuadre.py hace hojas, yo marco el foco por toma y se mide; el builder no arma verticales sin revisión. Sin Gemini."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 24925707-6a06-4c89-b163-36e8b0c9a474
  modified: 2026-10-29T14:41:21.776Z
---

Antes de armar cualquier vertical: `estudio-video/herramientas/revisar_encuadre.py PIEZA 9 45 1`, ABRIR cada hoja `encuadre_<fmt>.jpg`, escribir `encuadre/notas.json` (foco [x0, x1] leído en la regla + qué se ve), corregir `enc` y `--aprobar`. `build_inta_sb.py` se niega sin `revisado.json` vigente.

**Why:** 29-oct: «cuando reencuadra no está mirando qué reencuadra, debe revisar». Al revisar salieron cortes reales: manos que escriben fuera del cuadro, la presentadora fuera, solo una nuca o una espalda, palabras partidas. Cris también dijo «no uses Gemini» (además, el 29-oct no había créditos: 402).
**How to apply:** el foco es lo que la frase necesita (rostro, mano que toca, pantalla en uso, QR); si no cabe todo, decidir y decirlo en «ve». Los verticales de INTA23.0006 se renderizaron antes con los cortes viejos. Ver [[video-storyboard-rotacion-papelera]].
