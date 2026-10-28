---
name: proceso-video-16-pasos
description: "28-oct-2026: Cris definió el proceso obligatorio de 16 pasos para todo video (voz Hale (receta única) → planos → preview 720p → .prproj con color → formatos → mexicano → Brasil); vive en estudio-video/CLAUDE.md (detalle técnico en CLAUDE.md)."
metadata:
  node_type: memory
  type: feedback
---

Cris pidió (28-oct) imprimir y que "siempre se siga" el proceso de 16 pasos; está en `estudio-video/CLAUDE.md`.

**Why:** los flujos anteriores se contradecían (color antes de montar, voz colombiana, cortes de 1,2 s).
**How to apply:** seguirlo en orden. Cambios clave: preview 720p primero y el color después, en el .prproj (solo se incluye el que el plano ya tenía; Cris colorea el resto y exporta, final 4K 16:9); ningún plano <1,5 s; música solo de Masterizadas con el punto de giro al terminar el hook; validar tramos de planos sin movimientos de cámara (Gemini si hace falta); mexicano = ElevenLabs + Enhance Speech; luego pt-BR. Ver [[voz-y-planos-prohibidos-videos]], [[musica-punto-de-giro]].

**Vigente (28-oct), detalle completo en `estudio-video/CLAUDE.md`:**
- **Storyboard (paso 9b):** `herramientas/storyboard.py`; una capa (cada toma = un plano O un motion); SIEMPRE 5 opciones por toma = 3 planos + 2 motion designs, con mi favorita ★; «Ninguna sirve» = 5 nuevas (3+2) solo de esas tomas; planos evaluados mirándolos, sin repetir entre videos del lote ni tomas falsas; los motion se construyen solo si Cris los elige.
- **Motion:** se COMPONE con `motion/elementos.py`; las plantillas son ejemplos (biblioteca por referencias, `plantillas_ref.py`; catálogo con `catalogo.py`). `motion/ideas.py` propone 2 metáforas por frase. Color por significado (verde Gurú, azul solución, blanco explicar); fondo siempre vivo; PROHIBIDO píldoras y redes de nodos; sin barrido de entrada; nada se sobrepone (`boceto.revisar`).
- **Un solo preview 16:9 a 720p por pieza;** tras aprobarlo: color → 4K 16:9 → recortes 9:16/4:5/1:1 → variantes.
