---
name: zonas-seguras-videos
description: "21-oct-2026: cada relación de aspecto tiene zonas seguras propias; en verticales no interferir con la UI de redes y usarlas también para encuadrar. Valores usados y cómo se aplicaron."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 287f99fa-4d5c-4169-aa67-98b013349425
  modified: 2026-10-21T19:38:56.925Z
---

Cris pidió (21-oct-2026, video QuizWiz+Scrybe) que en todo video OneScreen se respeten **zonas seguras distintas por relación de aspecto**, y que **también guíen el encuadre** del material (rostro, QR, celular, pantalla dentro de la caja segura), no solo la posición de textos. Las verticales no deben chocar con la UI de las redes.

Valores que adopté (margen izq/der/arriba/abajo, px): **9:16 1080×1920** = 65 / 192 / 288 / 672 (caja ~823×960; guía de Meta para anuncios en Reels: 14 % arriba, 35 % abajo, 6 % lados, + columna de botones a la derecha); **4:5 1080×1350** = 80 / 80 / 80 / 100 (contenido dentro del recorte central 3:4 de la cuadrícula); **16:9 1920×1080** = 96 / 96 / 108 / 120. Son cifras aproximadas de guías públicas que difieren entre sí (no hay spec oficial); Cris no las ha validado.

**Why:** los subtítulos a 300 px del borde en vertical quedaban bajo la UI de Reels/TikTok, y el QR de los planos quedaba fuera de la caja.
**How to apply:** texto, logos y botones SIEMPRE dentro de la caja; el video puede sangrar. Antes de entregar, dibujar la caja sobre fotogramas (snapshot + PIL) y mirar que el sujeto/QR caiga dentro. Para subir un sujeto en vertical, recortar con más zoom desde el 4K (crop de menor altura, y0 anclado abajo) en vez de dejar el recorte de altura completa; cuesta ~1,5× de ampliación. En el proyecto: `SAFE` en `videos/onescreen-quizwiz-scrybe/build.py` (FMT=16|9|45). Ver [[marca-tipografia-onescreen]], [[paleta-motion-graphics]], [[pipeline-color-slog3]] (recortar a vertical ANTES de colorear).
