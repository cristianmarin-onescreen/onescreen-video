---
name: short-casa-lopez
description: "Short vertical de 22 s del caso de éxito Casa López (19-oct-2026): proyecto en D:\\OneScreen\\Contenido\\2026\\5. Mayo\\CASO DE ÉXITO. Casa López\\Proyecto short (no en C:), cómo se armó y qué falta decidir."
metadata:
  node_type: memory
  type: project
  originSessionId: 215b2efb-8513-4c0e-9479-e782f2201f11
  modified: 2026-10-19T21:21:40.706Z
---

Short 1080×1920 de 22,6 s del caso de éxito Casa López, hecho el 19-oct-2026. Proyecto HyperFrames en `D:\OneScreen\Contenido\2026\5. Mayo\CASO DE ÉXITO. Casa López\Proyecto short` (está en D: porque a C: le quedaban 338 MB libres). Lo entregado: `D:\OneScreen\Contenido\2026\5. Mayo\CASO DE ÉXITO. Casa López\Short_Casa_Lopez_pantallas_v2.mp4`.

- Fuente: entrevista C1361 (Giovanni García, coordinador técnico y comercial), tramo 221–262 s, con el audio limpio `C1361-esv2-…wav`; 11 cortes ajustados a la rejilla de 23,976 cuadros (`work/cut.py`). Apoyos: C1274, C1287, C1276 (llanta 360° en la pantalla), C1279.
- Todo se coloreó con [[pipeline-color-slog3]] después de recortar a vertical; se usó la versión estándar. La "ambiente" también está en `work/graded/` por si Cris la prefiere.
- `build.py` genera index.html; paleta según [[paleta-motion-graphics]]; música y SFX de ElevenLabs según [[mezcla-audio-videos]].

- 19-oct: Cris pidió el proyecto para pulirlo en Premiere y así enseñarme su estilo de edición. Le dejé `Short_Premiere\` en la carpeta del caso: XML FCP7 (`premiere.py`) con los crudos 4K, más gráficos y subtítulos con alfa, SRT, LUTs y LEEME. La convención de "center" del XML no está probada en Premiere; el LEEME trae las posiciones en píxeles por si acaso. **Pendiente:** cuando devuelva su XML exportado, compararlo corte por corte con el mío y guardar las reglas que confirme como guía de estilo de edición.

**How to apply:** si pide cambios, edita `build.py` (no index.html) y renderiza con TMP y `--frames-cache-dir` en D:, con un nombre de archivo nuevo ([[hyperframes-render-trampas]]).
