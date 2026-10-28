---
name: voz-aprobada-no-se-regenera
description: "27-oct-2026: Cris se molestó porque regeneré la voz de un video cuando ya había dicho que estaba bien; la voz aprobada queda congelada y solo se vuelve a generar si él lo pide."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 96e0d40d-fdc3-4d28-91e8-56177ff33ab4
  modified: 2026-10-27T16:57:01.324Z
---

Cris dijo (27-oct, INTA16): "No entiendo por qué siempre regeneras la voz si ya te había dicho que estaba bien? esto es una perdedera de tiempo contigo". Antes: "para qué haces tomas nuevas de voz???".

**Why:** cada toma nueva cuesta tiempo y créditos, y rompe una voz que ya aprobó (el acento ya estaba bien). Una corrección de motion, planos, CTA o música NO es una corrección de voz.

**How to apply:**
- Cuando Cris diga que la voz/acento está bien, esa toma queda congelada: copia a `Voz\aprobada\` y no se llama a ElevenLabs para esa pieza.
- Corregir CTA, gráficos, planos o música se hace sobre el audio existente (recortar, mover, texto en pantalla). Si un cambio de guion exigiría voz nueva, preguntar antes en una línea, no generar "por si acaso".
- Solo se regenera si Cris pide explícitamente cambiar la voz. Ver [[voz-y-planos-prohibidos-videos]], [[mezcla-audio-videos]].
