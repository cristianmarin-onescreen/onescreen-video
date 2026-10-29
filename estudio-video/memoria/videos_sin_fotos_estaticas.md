---
name: videos-sin-fotos-estaticas
description: Regla de Cris para videos — jamás fotos estáticas como plano; si solo hay foto, animarla con Gemini Omni (herramientas/veo_i2v.py; Veo 3.1 fue retirado)
metadata:
  type: feedback
---

En los videos NUNCA va una foto/imagen estática como plano. Si solo existe el asset en foto, se anima con imagen→video y se usa el clip: hoy `estudio-video/herramientas/veo_i2v.py` (Gemini Omni `gemini-omni-1.1-flash`, Interactions API; clave `GEMINI_API_KEY` o `GOOGLE_AI_STUDIO`). Veo 3.1 (`veo-3.1-fast-generate-preview`, `predictLongRunning`) fue retirado por Google el 28-oct-2026. Si Cris rechaza la imagen, generar un plano nuevo por texto→video en vez de reusar la foto.

**Why:** en la v2 de QuizWiz+Scrybe puse `examen.png` como plano y Cris lo reprochó dos veces ("jamás", "no me gusta, usa otra"); ya lo había dicho al inicio ("si no tienes assets generalos con google ai studio").
**How to apply:** antes de montar, revisar que ningún `seg` sea `img`; reemplazar por un clip generado (ejemplo de la época de Veo: `D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\veo\docente_a.mp4`). Cada clip cuesta dinero real: un intento por clip, sin reintentar errores que se cobran (solo esperar y repetir ante 429). Ver [[video-quizwiz-scrybe-v2]] y [[videos-mercado-libre-producto]].
