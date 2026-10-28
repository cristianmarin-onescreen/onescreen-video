---
name: pipeline-color-slog3
description: "Pipeline automático de color S-Log3 → look de Cris (grade/, config/estilo.yaml, skill colorear-plano); estado de calibración, decisión pendiente (balance de blancos) y trampas"
metadata:
  node_type: memory
  type: project
  originSessionId: 17466fae-e870-4e0b-9095-7729b8c6b6bd
  modified: 2026-10-12T20:44:02.616Z
---

Pipeline construido el 12-oct-2026 en `Desktop\Claudio\grade\` (un script por etapa + `pipeline.py` de entrada), parámetros en `config/estilo.yaml`, pruebas en `tests/`. Instrucciones operativas: skill `.claude/skills/colorear-plano/SKILL.md` (cárgala cuando Cris pase un plano y pida color).

**Estado:** 5 planos de `samples/orig/` coloreados en `samples/graded/` (versión `_graded` y `_graded_ambiente`). Calibración etapa 4 con la toma 02: 4b MAE 0.0014, 4d 0.0054 (pasan), 4c 0.0070 (meta 0.006, falla). Luz (etapa 3) calibrada con una sola toma.

**Why:** Cris quiere que un agente gradúe su material sin él, y que Hyperframes use los planos ya graduados.

**Decisión abierta:** ¿balance de blancos al 100 % o dejar ambiente? En la toma 02 de referencia, sin balance se acerca más a Cris (MAE 0.0285 vs 0.050); en la 01 coincide con balance. No afirmar una regla; entregar ambas versiones hasta que Cris elija.

**How to apply:** no recalibrar ni cambiar parámetros sin que lo pida; mirar siempre el contact sheet antes de entregar; LUTs y referencias (01.MP4 = 1.6 GB) no van a git. Cris dijo explícitamente que solo le importa el color, no revisar escala/movimiento de plano. Trampas técnicas (yuvj sin etiquetas, clips girados, rutas con tilde, heredocs) están en la skill.

Relacionado: [[hyperframes_render_trampas]], [[marca_tipografia_onescreen]].

**21-oct-2026 (Cris: "sí aprende"):** recalibración con su grado real. Su Lumetri: LUT Glenderaterra (= el 2383) al 50 %, aplicado en el clip fuente (Controles de efectos > Origen), temperatura −27, contraste +88,8, saturación creativa 80,7 %, viñeta leve; exposición por clip. Medido sobre 7 tomas de 3 videos (Colaboradores/Nativos/Regreso) contra su render final: resuelve la decisión abierta: **"ambiente" (`fuerza 0`) coincide con su azul/verde** (dlnB/G +0.014, sd 0.025; con 1.0: +0.054, sd 0.043) y hay que quitar ~3,5 % de rojo (`look.rojo_extra: 0.965`). Error cromático RMS 0.080 → 0.031. Valores ahora por defecto en `config/estilo.yaml`. **Luma sin calibrar:** su resultado sale ~0.08 más claro en la mediana (±0.06), depende de la exposición manual por clip; en la toma 01 antigua era al revés (+0.05 el mío) → no tocar la etapa 3 sin más datos. Tests: mismas 2 fallas de antes (gris .5845 y HSL 4c 0.0070). Ver [[estilo-organico-cris]].
