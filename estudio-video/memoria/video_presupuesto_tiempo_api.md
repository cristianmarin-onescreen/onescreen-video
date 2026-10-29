---
name: video-presupuesto-tiempo-api
description: "29-oct-2026: storyboard ≤15 min tras la voz; sin Gemini en el flujo de video; sin estable.py sobre candidatos; una hoja de contacto por video."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0880bf99-0449-417c-ac31-e049b62336a2
  modified: 2026-10-29T15:02:54.866Z
---

Un storyboard tardó 50 min sin salir porque `seleccion.ficha_plano()` corría `estable.py` (decodifica hasta 45 s de cada clip 4K + FFT por cuadro) sobre cada candidato, y las reglas mandaban «si hay duda, Gemini lee el clip». Ahora:
- `estable.py` apagado por defecto (`ESTABLE=1` solo sobre planos que Cris ya eligió). El movimiento de cámara lo filtra la columna «Movimiento» del Directorio; el tramo arranca en «Mejor momento».
- Gemini prohibido en selección, validación, storyboard, voz y encuadre; excepciones solo si Cris lo pide (`veo_i2v.py`, cadena nocturna de Mercado Libre). La ficha de Gemini del Directorio ya está pagada.
- Revisión visual: una hoja de contacto por video (un fotograma por candidato, 5-6 candidatos por toma) y una rejilla de bocetos de motion por video. Nada de un Read por plano.

**Why:** Cris, 29-oct: «llevo 50 minutos y no he recibido el primer storyboard» y «llamados a lo maldita sea a Gemini».
**How to apply:** si una etapa pasa de 5 min, parar y buscar qué está procesando de más. Antes de volver obligatoria una regla nueva que añada trabajo por plano o por toma, decir su costo y pedir el OK de Cris. Ver `estudio-video/CLAUDE.md` §9 y [[video-storyboard-rotacion-papelera]].
