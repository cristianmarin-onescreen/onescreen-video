---
name: edicion-cris-ritmo-voz
description: "21-oct-2026: reglas de edición medidas en 28 videos de Cris (voz manda, no la música): cortes/zooms/apoyos/gráficos 2-3 cuadros antes de la palabra; zigzag 100%/zoom cerrado; apoyo literal; guía 07_EDICION.md."
metadata:
  type: feedback
---

Cris pidió (21-oct-2026) que aprenda de sus `.prproj` (carpeta por carpeta, solo el principal de cada una, nunca autoguardados) cómo edita: ritmos con música y voz, criterio del plano de apoyo vs lo que dice la persona, zooms, y la narración como lo más importante. Resultado en `estilo-onescreen/07_EDICION.md` (guiones de edición en `estilo-onescreen/edicion_guiones/`, herramientas en `estilo-onescreen/tools/`).

Reglas medidas (28 videos): **cortes, entradas de apoyo, inicios de zoom y gráficos caen 0-120 ms (2-3 cuadros) ANTES de una palabra** (64 % vs 36 % azar); salidas de apoyo en el final de palabra; **no corta al compás de la música** (pulso = azar) ni según la velocidad del habla (corr −0,04); **zigzag ancho 100 % / cerrado** en cada corte (mediana 92 % de alternancia; cerrado 137-144 % en entrevistas, 150-188 % en presentadores); ritmo 33-41 cortes/min en explicativos, 22-27 en entrevistas, 37-47 en cortos; apoyo cubre 25-50 %, dura 1,7 s, **ilustra literalmente lo que se nombra** (listas de pasos en ráfagas de 2-4 tomas + PNG numerado, cifras como gráfico); IA/stock ampliados 200-300 %; SFX 60-85 ms antes del evento; música una pista continua.

**Confirmado por Cris (21-oct):** el zigzag es SIEMPRE un salto fijo de escala, para ocultar cortes al borrar muletillas y para dar ritmo; los valores dependen del plano (presentadores: planos parecidos, valores parecidos; casos de éxito: la composición varía por el lugar, así que varían mucho).
**Why:** quiere que el agente replique su edición, no la de plantilla.
**How to apply:** para editar un video suyo, transcribir por palabras (Scribe), fijar ritmo por formato, alternar 100 %/zoom, mover cortes a 2-3 cuadros antes de la palabra, apoyos literales, SFX antes del evento. No afirmar "edición por beats": los datos dicen que no. Ver [[estilo-organico-cris]], [[mezcla-audio-videos]].

**Casos de éxito 2026 (5 carpetas, sección 8 del 07):** 12-24 cortes/min, apoyo 63-67 % del video y 2,6-4 s por toma; cortes 0-120 ms antes de palabra en 67-78 % (azar 34-41 %); el zoom cerrado es un valor único por entrevistado (136-148 %) y varios valores donde cambia el lugar.

**Corrección 21-oct:** afirmé sin verificar que Video Demo no tenía montaje final; sí lo tiene: `Demo_OneScreen.prproj` (SC01-SC05) + proyectos `Apoyo/SCxx/SCxx.prproj` (SC06-SC12) + `Exports/`. Los proyectos de Cris pueden estar en SUBCARPETAS: antes de decir que algo no existe, buscar recursivo (`find -iname *.prproj`) y confirmar. Medidas de Demo (12 escenas, voz Hale generada): eventos visuales 0-120 ms antes de palabra 44 % vs 34 % azar (SC01 65 %, SC03 63 %; las demos de software ~40 %). Auditoría de selección: 30/33 carpetas con secuencia = render ±1 s; revisar Scrybe, vs otros, Itecsur. Ver sección 10 de 07_EDICION.md.

**Regla de Cris (25-oct-2026, video corporativo):** en piezas de voz en off sobre planos, el corte promedio iba de **1,2 a 2 s** (reemplazado el 28-oct: ningún plano dura menos de 1,5 s) (≈30-50 cortes/min): usar muchos más planos del Directorio en vez de sostener pocos.
