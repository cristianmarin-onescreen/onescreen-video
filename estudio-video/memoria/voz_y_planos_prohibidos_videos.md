---
name: voz-y-planos-prohibidos-videos
description: "Vigente (28-oct 2026): voz = receta única voz_exp_d.py (eleven_v4 + voz a voz a Hale, sin tempo, sin juez Gemini); planos solo desde 2024 y vetados 103182/103512."
metadata:
  node_type: memory
  type: feedback
  modified: 2026-10-28T21:50:02.700Z
  originSessionId: 501eb933-b1a3-4620-a103-09fbe237186b
---

## Voz (regla vigente, 28-oct)
UNA sola receta: `videos/onescreen-inta/voz_exp_d.py` (detalle en [[voz-una-sola-receta]] y `estudio-video/CLAUDE.md` §6): fuente Cristian Sánchez `o2vbTbO3g4GrKUg7rehy`, `eleven_v4`, es, speed 1,12, style 0,6, stability 0,45 → voz a voz a Hale `wWWn96OtTHu1sn8SRGEr` (`eleven_multilingual_sts_v2`, 0,2 / 0,7 / 0,7). Luego `voz_post.py` (silencios >0,22 s a pausas de 0,14 s, **sin tempo**, mono 48 kHz) y Scribe. **Sin juez Gemini.** Una voz aprobada no se regenera: [[voz-aprobada-no-se-regenera]].

**Why:** la ruta con eleven_v3 + tempo 1,12 sonó plana y lenta; el 28-oct Cris la rechazó. `voz_inta.py`, `voz_hale_directa.py` y `voz_v4_dirigida.py` están bloqueados (OBSOLETO).

## Planos
- **Solo grabados desde 2024 (27-oct):** "no uses planos anteriores a 2024, muchos tienen a excolaboradores que ahora trabajan en la competencia". Filtrar por "Fecha de grabación" del Directorio (≥ 2024; sin fecha tampoco). Hecho en `videos/onescreen-inta/seleccion.py` (`base_ok`).
- **Vetados:** **103182** (C0138, hombre de barba con camisa OneScreen y audífonos: "ese hombre no debe salir") y **103512** (C0379, grupo de cuatro personas sentadas riendo).
Ver [[directorio-video-onescreen]].
