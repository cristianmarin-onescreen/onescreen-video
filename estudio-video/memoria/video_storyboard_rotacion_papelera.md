---
name: video-storyboard-rotacion-papelera
description: "29-oct-2026: Cris se cansó de ver los mismos 20 planos y tomas falsas; un plano 1 vez cada 15 storyboards, papelera de veto en el storyboard, filtro FALSA y reglas medibles en código; wiggle = Camera Wiggle de Cris."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 24925707-6a06-4c89-b163-36e8b0c9a474
  modified: 2026-10-29T13:57:35.234Z
---

Un plano propuesto en un storyboard no vuelve a salir hasta 15 storyboards después (cada video = uno). La papelera 🗑 de cada plano lo veta para siempre. `seleccion.py` filtra tomas falsas por la ficha (risas, poses, selfies, brindis, aplausos, mirar a cámara, errores de grabación). Todo lo medible se comprueba en código y detiene el script (tabla «Reglas que se miden en código» de estudio-video/CLAUDE.md).

**Why:** 29-oct: «siempre me trae los mismos 20 planos» (el ranking es determinista y solo penalizaban los usos aprobados); el día anterior salieron tomas falsas, gente riéndose y alguien dibujando un pene en una pantalla. «Lo que sea medible que sea medible y no solo instrucción.»
**How to apply:** usar `estudio-video/herramientas/planos_rotacion.py` (historial `registro/planos_propuestos.json`, vetados `registro/planos_vetados.json`); siempre levantar `storyboard.py servir` para que la papelera funcione; nunca usar `--sin-rotacion` sin que Cris lo pida. El wiggle vigente es `cam_wiggle()` + `motion/camera_wiggle.json` (Camera Wiggle de sus capas de ajuste), no `wig()`. Ver [[proceso-video-16-pasos]].
