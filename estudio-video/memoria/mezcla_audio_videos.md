---
name: mezcla-audio-videos
description: "Gusto de Cristian para música/SFX en videos editados (19-oct-2026, pitch Lessn): percusión rápida ≥160 BPM, música presente, efectos discretos; carve de HyperFrames baja demasiado."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 95afbb51-9292-4963-b2f6-59622fdcb009
  modified: 2026-10-19T19:45:32.832Z
---

Música de fondo: **percusión tipo drumming, al menos 160 BPM**, energía constante. La "corporativa suave" a 100 BPM la rechazó por tranquila.
Niveles aprobados (v3 de `videos/onescreen-lessn-pitch`): voz ≈ -18 LUFS, música+SFX ≈ -24 LUFS (unos 6 LU por debajo de la voz); efectos de sonido discretos (volumen 0.13–0.23). En la v2 dijo "efectos muy altos, música muy baja".

**Why:** lo dijo al revisar la v2 y aprobó la v3 con esos niveles.
**How to apply:** en videos editados de OneScreen, generar la música con ElevenLabs (`/v1/music`, force_instrumental) y los SFX con `/v1/sound-generation`, porque `media-use resolve --type bgm` necesita el CLI de heygen y no está instalado. No usar `carve.mjs` con la música: aun con strength 0.5 la dejó unos 10 LU bajo la voz. Mejor un volumen fijo de ~0.26 sobre una pista de -12 LUFS. Medir la mezcla restando el audio del render sin música (amix con volume=-1). Ver [[hyperframes-render-trampas]] y [[marca-tipografia-onescreen]].
