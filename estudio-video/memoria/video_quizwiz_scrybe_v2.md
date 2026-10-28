---
name: video-quizwiz-scrybe-v2
description: v2 del video QuizWiz+Scrybe (21-oct-2026) rehecho con las reglas medidas de edición y estilo Flota IA; dónde vive y qué falta
metadata:
  type: project
---

v2 entregada en `D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\` (QuizWiz-Scrybe_v2_16x9 / 9x16 / 4x5, 45 s, con subtítulos). Código en `videos/onescreen-quizwiz-scrybe/` (`build_v2.py` FMT=16|9|45, `trims_v2.py`, `mix_v2.py`, `post_v2.py`); proyectos HyperFrames en `D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2_{16,9,45}`; voz ElevenLabs v4 toma "e".

Aplicado de [[edicion-cris-ritmo-voz]] y [[estilo-motion-apple]]: cambios 100 ms antes de la palabra, SFX 75 ms antes, flotación de cámara + aberración cromática, intro de marca al final, gráficos por máscara/trazo.

**Why:** Cris pidió "ver si aprendiste" re-ejecutando el video con lo medido.
**How to apply:** Falta versión sin subtítulos (CAPS=0), color no recalibrado (planos de cámara usan los graduados de antes; UI/stock sin tratar). Trampas: subtítulos consecutivos se pisan 1 cuadro si no se acortan 50 ms; en vertical subir texto de tarjetas blancas y check para no chocar con el subtítulo al 49 %; el plano previo a una tarjeta blanca debe extenderse 0,6 s o queda negro.
