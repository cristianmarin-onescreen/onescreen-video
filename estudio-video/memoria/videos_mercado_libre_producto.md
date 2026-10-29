---
name: videos-mercado-libre-producto
description: "Videos 9:16 de producto para 12 publicaciones de Mercado Libre (nombrados con SKU); Veo 3.1 fue retirado, se usa Gemini Omni; créditos de la API agotados el 28-oct-2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 8b1125b2-5866-4aed-bf71-648c6d13b597
  modified: 2026-10-28T23:51:22.753Z
---

Alejandro pidió (28-oct-2026) un video vertical, máx. 1 min, producto en uso y con los specs más importantes (sin guion ni voz), por cada SKU de ML: LAPIZP, A10W, CAST2, OCWL10C (Sensor Box), CAMSNAP2, CAMPTZ (ficha "PTZ 4K"), OCMIC60 (ficha "Amplifyr", el listado dice Mic-60), MC1500, MC1800, OSP-72 (Poster P1.9, ficha OSP-72.0001), CAMWEB (WebCam 101/102, Cris: "es la misma, no pasa nada"), OPSL7I7 (OPS i7 general: "tener Windows en tu PC").

**Cómo se hace:** `estudio-video/herramientas/ml_producto.py` (recortes → clips → build → render); salida en `D:\OneScreen\Contenido\2026\10. Octubre\Mercado Libre\` (`Exports\<SKU>.mp4`). Specs solo de la ficha (Drive > Fichas técnicas, el ID de la ficha es el SKU, p. ej. `A10W.0001`); los renders oficiales de la ficha son la imagen de partida de los clips. Lápiz (LAPIZP) no tiene ficha: faltan sus specs.

**Why:** Cris pidió "los planos que no tengas créalos con Gemini Veo" y "primero haz los videos que sí puedas".
**How to apply:**
- Veo 3.1 (fast, lite y normal) fue retirado por Google: el reemplazo es `gemini-omni-1.1-flash` (Interactions API, `herramientas/veo_i2v.py`). Tier 1: 4 peticiones/min y tope por gasto: ir de a uno.
- Los clips de IA alteran el producto: mirar cada tira de fotogramas contra el render de la ficha. Rechazados: A10W_b (inventó un anillo luminoso) y Sensor Box a/b (convirtió el sensor redondo en lente de cámara).
- 28-oct: créditos prepagados agotados (HTTP 402); faltan ~20 clips. Ver [[videos-sin-fotos-estaticas]], [[proceso-video-16-pasos]].

**Estado 28-oct noche:** voz estilo Apple aprobada («si esa es la idea») para los 12 guiones (`Guiones_voz.md`); montaje que sigue a la voz (sin silencios); color de los planos del lápiz lo pone Cris (`LAPIZ_COLOR.mp4`, **Claude no colorea**: se genera el .prproj con `ml_lapiz.py`); listos A10W, CAST2, OCWL10C, CAMSNAP2, CAMPTZ, MC1800, LAPIZP; Poster (OSP-72) descartado porque el clip de IA no era igual al real. Cuota de la API (20 peticiones/día, Tier 1) se reinicia 2:00 a. m. Colombia; `ml_noche.py` corre solo para MC1500, OCMIC60, CAMWEB, OPSL7I7 y OSP-72 y deja `Entrega_Alejandro\`. Planos del lápiz: C0125, C0123, C0127 de `Varios\Harrison Caballero\...\MARCADOR INFINITO\videos` (nunca el video exportado).
