---
name: voz-una-sola-receta
description: Voz en off de OneScreen = UNA receta fija (INTA37 exp_d); prohibido usar otros modelos/ajustes o acelerar en el post; Cris se molesta por la pérdida de tiempo
metadata:
  type: feedback
---

Siempre se genera la voz con `videos/onescreen-inta/voz_exp_d.py`: fuente Cristian Sánchez con eleven_v4, es, speed 1,12, style 0,6, stability 0,45 → voz a voz a Hale (stability 0,2, similarity 0,7, style 0,7), guion dirigido enérgico (MAYÚSCULA en el énfasis), sin TEMPO en el post.

**Why:** 28-oct, INTA20-22: usé la voz vieja (eleven_v3 + tempo 1,12) sin comprobarla contra CLAUDE.md; Cris: «suena una mierda», «siempre voz nueva, prohíbete los otros ajustes, qué pérdida de tiempo».
**How to apply:** no probar variantes, no perfilar ni comparar, no usar scripts viejos (voz_inta.py, voz_hale_directa.py, voz_v4_dirigida.py ya están bloqueados). Antes de montar con una voz existente, confirmar que salió de esta receta; si no, regenerar y dársela a escuchar. Ver [[voz-hale-receta-inta37]] y [[voz-aprobada-no-se-regenera]].
