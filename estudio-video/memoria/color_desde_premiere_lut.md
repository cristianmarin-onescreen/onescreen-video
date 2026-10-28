---
name: color-desde-premiere-lut
description: "El .cube que exporta Lumetri NO sirve fuera de Premiere; lo que sí funciona es ajustar un LUT comparando el original S-Log3 con un export de Premiere (prueba C1186, 22-oct-2026)"
metadata:
  node_type: memory
  type: project
  originSessionId: 17cb4ff0-915f-46d2-a579-b07ff30ecf7b
  modified: 2026-10-22T15:01:11.685Z
---

22-oct-2026, prueba en `D:\OneScreen\Contenido\2026\10. Octubre\Pruebas prproj color\` (clip C1186). Cris quiere que cada plano lleve su color de Premiere guardado y que en el ensamble de Hyperframes se use ese color sin exportar desde Premiere.

- El `.prproj` es XML gzip: se leen todos los valores de Lumetri (temperatura, contraste, LUT 2383 al 50 %, viñeta…), pero es solo la receta; no se puede renderizar fuera de Premiere.
- El "Exportar .cube" de Lumetri (menú ≡ del panel) NO sirve: no incluye la gestión de color de Premiere (Anular espacio color = Sony S-Log3/S-Gamut3, asignación de tono "Conservación del tono", compresión de gama "Conservación de la luminancia"), su salida pasa de 1 (llega a 3,15) y no declara espacios. Probé 6 lecturas (con/sin LUT S-Log3, lineal, OETF): todas oscuras y casi sin color; Cris: "se ve una mierda". Desactivar el S-Log interno da un .cube idéntico byte a byte.
- Lo que SÍ funcionó: Cris exporta `C1186 - color.mp4`; ajusto un LUT 33³ (S-Log3 crudo rango completo → Rec.709) + viñeta radial por separado, con pasadas alternadas. Validado en fotogramas reservados: sesgo 0, mediana 2,6/255. Salidas: `C1186_ajustado.cube`, `C1186_vineta.json`, `C1186_desde_lut.mp4`. Scripts en el scratchpad de la sesión (no en git todavía).

- Basta UN fotograma: "Exportar fotograma" (icono cámara del monitor de programa, PNG 16 bits) coincide con el export de video (mediana 0,8/255) y el LUT ajustado solo con ese PNG da en todo el clip lo mismo que con el video (mediana 2,6/255, sesgo <0,5). El PANTALLAZO de la ventana NO sirve: sombras +11 y medios −7 niveles (transformación de pantalla, gamma 2,4).

**Why:** evitar adivinar la matemática de Lumetri; el export de Premiere es la única verdad.
**How to apply:** no volver a intentar el .cube de Lumetri. Sin validar aún: si el LUT de un plano sirve para otros planos de la misma escena/luz (la exposición de Cris es por clip). Relacionado: [[pipeline-color-slog3]].
