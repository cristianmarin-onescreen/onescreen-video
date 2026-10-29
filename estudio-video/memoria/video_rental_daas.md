---
name: video-rental-daas
description: Video OneScreen Rental/DaaS (21-23 oct 2026): v3 con estilo corregido por Cris (texto sobre plano, diagramas que representan, tarjetas con plano), proyecto Premiere con Lumetri; dónde vive todo
metadata:
  type: project
---

Pedido de Cris (21-oct): video del guion "primera aula digital / dos caminos / DaaS / ventajas / pregúntanos" (onescreenlatam.com/rental). Versiones previas: neutra, acento ecuatoriano, mexicano y pt-BR en `D:\OneScreen\Contenido\2026\10. Octubre\Rental DaaS\`.

**v3 (23-oct): estilo corregido, UNA sola versión (neutra, voz `v_rv_1`) hasta que Cris apruebe; después acentos/PT.** Código `videos/onescreen-quizwiz-scrybe/build_rental3.py` (FMT=16|9|45, ALPHA=0|1) + parches `patch_r3a..d.py`; mezcla `mix_rental.py`, post `post_rental.py`, render `D:\hf-render\rental\run_r3.sh` → `out_r3/`. Premiere: `build_prproj.py`, `build_xmeml.py`, `validate_prproj.py` y carpeta `Rental DaaS\Premiere v3\` (prproj + respaldo FCP XML + MOV alfa + mapa de color). Sin abrir en Premiere (no verificable desde aquí).

Reglas de estilo que Cris corrigió (ver [[estilo-onescreen-texto-subtitulos]]): texto directo sobre el plano, nunca en contenedores ni píldoras; subtítulos blancos con trazo negro duro y fino, solo donde nada más lo dice; márgenes seguros reales; balance entre plano+texto, escenas de color/blancas y plano limpio; los motion graphics deben ser diagramas que REPRESENTAN lo que dice la voz (nodos, flujos, paquetes de luz, barras, colas), no íconos animados; trazo grueso (~7 % del tamaño del ícono, como Flota de IA); sin brillo/sombra difusa en gráficos (el brillo se reserva para cosas especiales); las tarjetas de ventajas con plano arriba + título + subtítulo le encantan (en escenas con fondo sí van tarjetas; sobre plano no).
Planos sin colorear: el color real vive en el Lumetri de sus proyectos (Sheet Directorio, col AP); C1198 y C0627 no tienen color en ningún proyecto.

**Trampas:** D: casi lleno (borrar cachés `D:\hf-render\tmp\fc*`/`rfc*` antes de renderizar); Manrope no está cargada en el proyecto (solo Rubik).

**Why:** Cris pide reutilizar el método de [[video-quizwiz-scrybe-v2]].
**How to apply:** no rehacer las versiones de acento/PT hasta la aprobación de v3; reusar el builder.

**26-oct: v3 aprobada como RENT.0005.** Premiere en `Rental DaaS\Premiere RENT.0005\`. C1010 y C1379: sus clips en sus proyectos NO tienen Lumetri (cuidado: `closure()` desde un TrackItem se escapa a otros clips y da falsos positivos; mirar solo la cadena `ComponentOwner/Components`). Sin color real: C1198, C0627, C1010, C1379. Siempre regenerar la capa alfa tras aprobar (`PROJ=...\v_16a FMT=16 ALPHA=1 build_rental3.py`, luego `hyperframes render --format mov --resolution 4k -f 24000/1001`). El prproj generado dio "el proyecto parece dañado" en Premiere (26-oct): causa en investigación.

**Causa del 'proyecto dañado' (26-oct):** (1) serialización: Premiere guarda los saltos de línea de texto XML incrustado como &#10; y tildes en UTF-8; `prser.py` reproduce byte a byte; (2) BinaryHash: Premiere escribe el base64 de los parámetros Arb (Lumetri/Look) SOLO en la primera aparición de cada hash, las demás van vacías; al clonar un Lumetri había que rellenar los datos (`collect_hashes`/`fix_hashes` en build_prproj.py). Antes de arreglarlo, todo prproj con Lumetri clonado daba 'dañado' (no era la versión del proyecto fuente). Diagnóstico con variables STOP/NOMASTERS/NOCLIPS/NOTRACKS/NOCOLOR/NOMOTION/COLORONLY.

**Flujo nuevo propuesto por Cris (26-oct):** NO hornear planos en neutro dentro de gráficos ni armar prproj finales con Lumetri. (1) `PLANOS=1 build_prproj.py` genera un prproj con los planos sueltos a su duración final (V1, +0,5 s de margen, Lumetri previo clonado como punto de partida, sin música ni gráficos) en `Rental DaaS\Colorear planos\`; (2) Cris colorea y exporta UN solo video 4K; (3) yo lo corto con `.planos.json` (origen_in/out y secuencia_inicio) y lo uso como fuente en HyperFrames para todos los formatos (16:9, 9:16, 4:5/1:1) e idiomas = master de color. Este export sustituye la conversión neutra S-Log3→709.

**Master de color (26-oct):** Cris coloreó los 8 planos en `Rental DaaS\Colorear planos\RENT.0005_planos_coloreados.mp4` (4K H.264, 31 s); cortado por plano en `...\Colorear planos\cortes\<src>_<clip>_color.mp4` (ventana usada + 0,5 s de margen). Registrado en el Directorio (col. AB Archivo graduado = ese corte; AP/AQ = el prproj de colorear; Z = Sí para C1198 y C0627). Reusar estos cortes antes de volver a colorear esos planos; la ventana exacta está en `RENT.0005_planos_para_colorear.planos.json`.

**Flujo reordenado (26-oct):** el proceso completo y optimizado quedó en `CLAUDE.md` (color una sola vez antes de montar, variantes en lote, trampas de prproj, links y hoja). Versiones aprobadas: RENT.0006 (neutro), 0007 (Ecuador), 0008 (México), 0009 (pt-BR), 3 formatos cada una; hoja de producción actualizada.

**Voz mexicana (26-oct):** sonaba con eco; pasada solo la voz por Adobe Enhance Speech (stem `enhanced_speech`, v_mx_d1_enh.wav) y montada como RENT.0010, que reemplaza a RENT.0008 (borrada de Drive). Exports aprobados en Drive: carpeta `Producción de video/RENT - Rental DaaS` (RENT.0006, 0007, 0009, 0010). Subida con rclone remoto `gdrivew` (scope drive). Las demás voces no mostraron el problema.
