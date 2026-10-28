# Sistema de diseño de video

No se mueve nada: estos son los archivos vivos y dónde están (rutas desde la raíz del repo `Claudio`).

| Qué | Dónde |
|---|---|
| Voz y tono | `estilo-onescreen/01_VOZ.md` |
| Léxico, reglas y proceso | `estilo-onescreen/02_LEXICO_REGLAS_Y_PROCESO.md` |
| Ejemplos y antimuestras | `estilo-onescreen/03_EJEMPLOS_Y_ANTIMUESTRAS.md` |
| Contrato, brief y guion | `estilo-onescreen/04_CONTRATO_BRIEF_Y_GUION.md` |
| Motion "Apple" (Flota de IA) + ayudantes `fx.js`/`shared.css` | `estilo-onescreen/05_MOTION.md`, `estilo-onescreen/motion/` |
| Estilo "Orgánico" | `estilo-onescreen/06_ESTILO_ORGANICO.md` |
| Edición de Cris (ritmo, zoom, apoyo, voz) | `estilo-onescreen/07_EDICION.md`, `estilo-onescreen/edicion_guiones/` |
| Texto y subtítulos | `estilo-onescreen/08_TEXTO_Y_SUBTITULOS.md` |
| Traducción y EE. UU. / pt-BR | `estilo-onescreen/ANEXO_TRADUCCION_Y_EEUU.md`, `videos/LOCALIZACION-PT-BR.md` |
| Carruseles y posts 4:5 | skill `carrusel-onescreen` (`.claude/skills/carrusel-onescreen/`) |
| Color S-Log3 → look de Cris | skill `colorear-plano`, `grade/`, `config/estilo.yaml`, `luts/` |
| Logo, tipografía, paleta | `memoria/marca_tipografia_onescreen.md`, `memoria/paleta_motion_graphics.md`; vector `videos/onescreen-transforma/assets/onescreen-wordmark.svg` |
| Zonas seguras | `memoria/zonas_seguras_videos.md` y valores en [../CLAUDE.md](../CLAUDE.md) |
| Lettering 3D (Rental v3) | funciones `lets`, `flip`, `camera`, `big`, `w3` en `videos/onescreen-quizwiz-scrybe/build_rental3.py` |

Cuando una regla nueva de diseño aparezca, va primero a [../CLAUDE.md](../CLAUDE.md) y luego se baja al `estilo-onescreen/` que corresponda.
