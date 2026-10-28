---
name: videos-sin-fotos-estaticas
description: Regla de Cris para videos — jamás fotos estáticas como plano; si solo hay foto, animarla con Veo (Google AI Studio)
metadata:
  type: feedback
---

En los videos NUNCA va una foto/imagen estática como plano. Si solo existe el asset en foto, se manda a animar con Veo 3.1 (Google AI Studio; clave `GOOGLE_AI_STUDIO` o `GEMINI_API_KEY`, modelo `veo-3.1-fast-generate-preview`, endpoint `predictLongRunning`, sin `personGeneration`, 6 s, 720p) y se usa el clip. Si Cris rechaza la imagen, generar un plano nuevo por texto→video en vez de reusar la foto.

**Why:** en la v2 de QuizWiz+Scrybe puse `examen.png` como plano y Cris lo reprochó dos veces ("jamás", "no me gusta, usa otra"); ya lo había dicho al inicio ("si no tienes assets generalos con google ai studio").
**How to apply:** antes de montar, revisar que ningún `seg` sea `img`; reemplazar por clip Veo (docente armando el examen, `D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\veo\docente_a.mp4`). Veo a veces falla con error 13 interno: reintentar. Ver [[video-quizwiz-scrybe-v2]].
