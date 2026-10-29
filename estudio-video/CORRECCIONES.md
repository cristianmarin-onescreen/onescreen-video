# Correcciones de Cris (registro vivo)

Lo más nuevo arriba. Cada entrada: fecha · video · lo que dijo · regla que salió (y dónde quedó). Claude agrega una entrada cada vez que Cris corrige o aprueba algo (ver [SKILL.md](SKILL.md), §4). La regla vigente siempre está en [CLAUDE.md](CLAUDE.md); si dos entradas chocan, manda la más nueva.

## 2026-10-29 · Reglas que gastaban tiempo y API
- **Estabilidad de cámara** — «puso a Claude a evaluar la estabilidad de cámara de todos los planos, llevo 50 minutos y no he recibido el primer storyboard». → `estable.py` (decodifica cada clip 4K) apagado por defecto en `seleccion.py` (`ESTABLE=1` solo sobre planos ya elegidos); el movimiento lo filtra la columna «Movimiento» del Directorio y el tramo arranca en «Mejor momento». (CLAUDE.md paso 9, §9)
- **Gemini** — «hace llamados a lo maldita sea a Gemini y eso consume mucho por API innecesariamente». → Gemini prohibido en el flujo de video salvo pedido de Cris (`veo_i2v.py`, cadena de Mercado Libre); se usa la ficha del Directorio, ya pagada. (CLAUDE.md §4.1, §9)
- **Revisión visual** — en vez de una tira de 3-5 fotogramas por candidato con un pool 3×: una hoja de contacto por video, un fotograma por candidato, 5-6 candidatos por toma; los motion designs, en una rejilla por video. Meta: storyboard ≤15 min tras la voz. (CLAUDE.md §4.1, §4.5, §9)

## 2026-10-28 — Auditoría de CLAUDE.md y archivos (a pedido de Cris)
- **Voz:** la nota de memoria `voz_y_planos_prohibidos_videos` seguía con eleven_v3 + tempo 1,12 (la receta rechazada); se reescribió, se copió `voz_una_sola_receta` al repo y `sync_memoria.py` ahora también copia `feedback_pasar_link*`. Paso 3 y tabla de herramientas apuntan a `voz_post.py` (>0,22 s → 0,14 s, sin tempo); `voz_exp_d.py` busca la pieza en `D:\OneScreen\Contenido`, escribe en `vNNNN` libre y se niega si hay `Voz\aprobada\`.
- **Estilo:** §2 ya no dice «sin brillo» ni limita la paleta (verde Gurú, degradados, halos); §1 deja claro que no van palabras sueltas sobre plano; se retiraron `hub` y `palabras` de la tabla (37 plantillas) y las píldoras residuales del código y la documentación.
- **Estado:** Corporativo marcado como desactualizado (voz vieja y cortes de 1,2 s); la fila de INTA remite a la hoja; excepción permanente de escritura en el Directorio limitada a las columnas Y y AQ.

## 2026-10-27 · La voz aprobada no se regenera
- **Voz congelada** — "No entiendo por qué siempre regeneras la voz si ya te había dicho que estaba bien". → cuando Cris dice que la voz está bien, la toma se congela en `Voz\aprobada\`; CTA, gráficos, planos y música se corrigen sobre ese audio; voz nueva solo si él lo pide o, tras preguntarle en una línea, lo autoriza. (CLAUDE.md §6, memoria `voz_aprobada_no_se_regenera`)

## 2026-10-27 · INTA: revisión de los 12 previews .0002 (Cris)
- **Planos** — "hay planos que no tienen nada que ver (montando una pantalla), pedazos de videos ya editados, personas hablando como apoyo, planos de IA, planos viejos". → solo clips crudos de cámara ≥ 2024, sin IA, sin exportaciones/pauta/música, sin gente hablando de apoyo, sin instalación salvo que la voz lo diga; casos: solo planos del caso (CLAUDE.md §4, `seleccion.py`).
- **Voz** — "castellano, horrible" (INTA17/18). Hale suena a España en otros modelos. *(Ruta que se anotó aquí —fuente colombiana → voz a voz— quedó reemplazada: la vigente es Hale directo, v4, neutro latino, validado con Gemini; ver 26-oct INTA y CLAUDE.md §6.)* "SuprNotes" se dice "Súper Nouts".
- **Música** — "no uses la misma canción, y la pusiste mal": una canción distinta por pieza, con su punto de giro (marca de Cris) justo al terminar el hook; sin SFX (`mix_inta.py`).
- **Texto vs motion** — "mucho texto y muy poco motion graphic": cada idea se dibuja (íconos de línea, flujos, conteo, tachado) con 2-3 palabras; piloto INTA16 (`gfx_inta.py`); pendiente su OK para las otras 11.
- **Ritmo/CTA** — escenas de texto quietas ≤ 2,2 s; el CTA "descarga la ficha" no sirve → "Escríbenos por WhatsApp". INTA25: sin narrador, hablan los entrevistados (`armar_caso25.py`).

## 2026-10-27 · INTA: planos anteriores a 2024
- **Nada grabado antes de 2024** — "hay un error, no uses planos anteriores a 2024, muchos tienen a excolaboradores que ahora trabajan en la competencia". Los .0002 usaban 32 planos de 2023 (de 159). → filtro duro por "Fecha de grabación" ≥ 2024 en `seleccion.py` (CLAUDE.md §4); los 12 previews se re-hacen como .0003 y el .0002 queda Reemplazado.

## 2026-10-26 · INTA (12 previews)
- **Voz** — "la voz está un asco, no estás usando Hale en español neutro" / "todas deben ser con la voz de Hale con voice director". → Hale directo, eleven_v4, español neutro latino, guion dirigido; sin voz a voz (CLAUDE.md §6). Los previews .0001 (voz colombiana a Hale) quedan Reemplazados por .0002.

## 2026-10-26 · Hoja de producción v2 (cambio de arquitectura)
- **Cuatro pestañas, cuatro dueños** — Cris con el chat de estrategia: Guiones (skill de estrategia; yo solo Estado y Versiones generadas), Producción (mía), Planner (script local, publica y mide a 24/48/72 h), Histórico (yo, al cerrar). Variaciones, Publicaciones, Resultados, Convenciones y README quedaron archivadas y ocultas. → CLAUDE.md §8, CLAUDE.md (Hoja de producción), registro/HOJA.md, `registro.py` v2, espejo `guiones/produccion/planner/historico.csv` (los viejos en `registro/legacy/`).
- **Solo se produce desde un guion aprobado** (Estado y Decisión = Aprobado); ya no creo filas "Pendiente" de publicación ni uso las columnas Usado. Hasta la confirmación de la prueba en seco no se escribe nada en la hoja.

## 2026-10-28 · Proceso obligatorio de 16 pasos
- **Flujo definido por Cris** — voz Hale con notas de dirección → listar planos → cortar silencios → ubicar guion/hook → punto de giro de la música (masterizados) → transcripción con tiempos → motion graphics en HyperFrames + revisión/descarga/validación de planos → ensamble sin planos <1,5 s → márgenes → preview 720p → aprobado: .prproj (color solo si el plano ya lo tenía; Cris colorea el resto y exporta, final 4K 16:9) → 1:1, 4:5, 9:16 → mexicano (ElevenLabs + Enhance Speech) → Brasil. → proceso en CLAUDE.md (detalle en CLAUDE.md); **reemplaza** "color una sola vez antes de montar" (26-oct) y el corte promedio de 1,2 s (CLAUDE.md §4-5, §7).

## 2026-10-26 · Color antes de montar (reemplazado el 28-oct), links y hoja (Rental)
- **Color una sola vez** — "tú haces realmente un prproj con los clips, en la duración final, sin música ni nada; yo los coloreo y exporto; tú a base de ese export lo montas… ese será nuestro master". → prproj de planos sueltos (`PLANOS=1`), Cris colorea y exporta, los cortes coloreados alimentan todos los formatos e idiomas; nada de conversión neutra ni Lumetri clonado en gráficos. (CLAUDE.md §4, PROCESO-VIDEO)
- **Guardar el color** — "guarda ese color para futuros, apúntalo en el directorio". → cada corte coloreado queda en `cortes\` y su ruta en la col. AB del Directorio. (PROCESO-VIDEO)
- **Fotos de tarjetas** — "el plano no se ve trackeado como en tu preview" y "se acaba el plano y se pone gris"; en 9:16 "no se ve nada" en esos cuadros. → fotos horneadas en la capa de gráficos con el último cuadro congelado; en vertical, foto desde el plano completo en horizontal y ventana más alta. (CLAUDE.md §4)
- **Links** — "acostúmbrate a pasarme el link, no a decirme dónde está porque me haces perder tiempo". → siempre link clicable. (CLAUDE.md §7, memoria `feedback_pasar_link_no_ruta`)
- **Hoja** — "no veo en el excel esto actualizado". → al aprobar se escribe la fila en la hoja de producción (no solo el espejo) y se relee. (CLAUDE.md §7-8)
- **Voz mexicana** — "el audio mexicano suena muy natural, pero la calidad suena terrible… pásalo por el enhance speech de Adobe antes de montarlo, no lo pases con la música, solo la voz". → Enhance Speech sobre la voz sola antes de montar; versión nueva RENT.0010 reemplaza a RENT.0008 y se borra la anterior de Drive. (PROCESO-VIDEO paso 15)
- **Técnico (Premiere):** el prproj dio "dañado" por (1) saltos de línea/tildes mal serializados y (2) datos de Lumetri solo en la primera aparición de cada `BinaryHash`. (PROCESO-VIDEO, "Si hay que generar un .prproj")

## 2026-10-26 · Voz dirigida, ruta en D: y carpeta solo de video
- **Texto de dirección para ElevenLabs** — "no veo que en voz tengas en cuenta que debes generar las narraciones con textos de dirección optimizados para ElevenLabs". → la narración siempre sale de un guion dirigido (etiquetas, puntuación de ritmo, arco emocional) más un guion limpio para subtítulos y Scribe. (CLAUDE.md §6, skill §2, checklist)
- **Todo en D:** — "por qué tienes indicaciones de guardar en C:? Todo debes guardarlo en D: en la carpeta de OneScreen, Contenido, el año y el mes en una nueva carpeta". → `D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\`, carpeta nueva por pieza; nada en C:. (CLAUDE.md §7b, skill §5, herramientas)
- **Esta carpeta es de video** — "¿por qué acá tienes información de carruseles? ¿Odoo, Todoist, reporte semanal qué tienen que ver?". → se quita la nota de carruseles de `memoria/` y de `sync_memoria.py`, y la mención a Odoo de la skill; CLAUDE.md aclara que aquí solo va video.

## 2026-10-26 · Carpeta de Drive
- **Exports en Drive, previews no** — "crea la carpeta de producción de video en drive, pero ahí no me pongas los previews, ahí pongamos los exports listos para subir". → carpeta "Producción de video" (`1cda9LOGC2Yb_wli88bNpmJ0BRFqOnmDm`) solo con exports aprobados (sin `_preview`), subcarpeta por pieza; previews por el chat. (CLAUDE.md (Hoja de producción), HOJA.md)

## 2026-10-26 · Aprobación en las dos vías
- **Hoja ⇄ sesión** — "quiero que funcione de las dos vías: o yo actualizo el Excel con el aprobado, o cuando lo apruebe en las sesiones se actualice allá". → `registro.py importar` (hoja → espejo + acciones) y `registro.py celdas` (sesión → hoja, celda por celda); permiso explícito para que Claude escriba la decisión de Cris en la hoja cuando la da en la sesión. (CLAUDE.md (Hoja de producción), HOJA.md, CLAUDE.md §8)

## 2026-10-26 · Reestructura de la hoja de producción
- **Dónde se aprueba y se publica** — "no veo dónde quedan las piezas producidas para que yo las apruebe y con esa aprobación se publiquen". → columna Link del preview (Drive) + Decisión de Cris (amarilla) en Producción; Aprobada habilita usos, .prproj y publicación.
- **Piezas vs versiones** — "no entiendo la diferencia, me parece redundante". → una sola tabla (Producción, una fila por ID); sin pestaña de piezas.
- **Variaciones y resultados** — "¿dónde se ve lo de las variaciones? ¿dónde registro notas de resultados para tomar decisiones?". → columnas Hook / Contenido / CTA + pestaña Variaciones (catálogo y aprendizaje) + pestaña Resultados (mediciones, qué vimos, decisión, próxima variación).
- **Conexión con el Directorio de planos** — "para que marque en el # de usos y agregue un uso". → al aprobar, +1 en col. Y y línea en col. AQ por cada plano usado; fecha en Producción para no duplicar.

## 2026-10-26 · Hoja maestra de producción
- **Hoja de directorio de producción** — "esta será la hoja de directorio de producción de video: dale formato y guárdala en la memoria de la skill y el entorno para apuntar a eso". → Sheet `1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks` formateado (Piezas, Versiones, Publicaciones, Convenciones, README para Claude), es la fuente de verdad del registro; CSV = espejo. (`registro/HOJA.md`, CLAUDE.md (Hoja de producción), CLAUDE.md §8)

## 2026-10-26 · Entorno de video
- **Registro tipo hoja de fichas** — "que tenga un registro de lo que se ha usado, las versiones con un ID único guardado en el nombre del archivo (no impreso), convenciones de versiones y variaciones (hook, contenido, CTA), y un registro de si el video exportado se usó y si está publicado; otro agente y entorno jala la información y la sube". → carpeta `registro/` (piezas, versiones, publicaciones, manifest.json), `registro.py`, ID `<PIEZA>.<NNNN>`, nombre `<ID>_<H#C#A#>_<voz>_<formato>[_preview].<ext>`, protocolo de relevo. (`registro/LEEME.md`, CLAUDE.md (Hoja de producción), CLAUDE.md §8)

## 2026-10-23 · Rental DaaS v3
- **Entrada del lettering** — "prefiero que aparezca de abajo hacia arriba por palabra, con transparencia, no brusco, estilo Apple; la estirada me recuerda a PowerPoint". → palabra por palabra, fundido, ≥1 s, sin giros. (CLAUDE.md §1)
- **Diagramación repetida** — "título grande a la izquierda y motion a la derecha: se siente plantilla; más juguetón, lettering de Apple, tipo cámara 3D". → diagramación distinta por escena; perspective/z/giros suaves. (CLAUDE.md §2)
- **Cruces** — "estás pisando textos con gráficos". → revisar cruces en los tres formatos antes de renderizar. (CLAUDE.md §3)
- **Márgenes** — "más aire a los lados, lo estás dejando muy al límite". → 16:9 lados 270; 9:16 y 4:5 lados 150. (CLAUDE.md §3)
- **Píldoras** — "en contenedores no uses píldoras, ya te lo había dicho". → ningún contenedor sobre plano; "Contáctanos" = texto + ícono. (CLAUDE.md §1)
- **Tarjetas con plano** — "en las tarjeticas habías puesto planos, estaban chéveres" / "esas me encantaban". → tarjetas de ventajas con plano + mini-diagrama + título + subtítulo, en escenas con fondo. (CLAUDE.md §2)
- **Íconos animados** — "no puede ser solo un iconito animado… cosas que representan otras cosas". → diagramas que representan lo dicho. (CLAUDE.md §2)
- **Trazo y brillo** — "muy delgados, ni ese brillo; me gustaban más como en Flota de IA". → trazo ~7 % del ícono; sin brillo (reservado). (CLAUDE.md §2)
- **Fondos** — "puedes poner los motion graphics sobre fondos blancos o de colores, variado". → escenas de color/blanco alternadas. (CLAUDE.md §2)
- **Balance** — "no mataste los motion, los varíes; más balance: ni todo motion ni todo texto". → mezcla plano+texto, escenas de color y plano limpio. (CLAUDE.md §2)
- **Texto sobre plano / subtítulos** — "texto sobre el plano, el blanco para enfatizar; subtítulos blancos con trazo negro duro y muy fino; sin subtítulos si ya hay explicación visual; nunca en cuadros". → (CLAUDE.md §1; `estilo-onescreen/08_TEXTO_Y_SUBTITULOS.md`)
- **Planos** — "déjalos sin colorear y exporta el Premiere jalando el Lumetri de esos planos". → *(reemplazada el 26-oct por "color una sola vez antes de montar", arriba)* (CLAUDE.md §4)
- **Una versión** — "corrígelo solo con una versión y luego, cuando la apruebe, sacamos las nuevas". → una versión neutra hasta aprobar; preview antes del .prproj. (CLAUDE.md §7)
- **Flujo (26-oct)** — "se debe exportar el video de preview para que yo apruebe, y luego creas el prproj si se puede jalando los Lumetri que ya existan; el directorio maestro apunta al proyecto si ya tienen color o ya fueron usados". → dos puertas de aprobación; Directorio maestro columnas Z/AP/AQ. (skill `video-onescreen`, CLAUDE.md)

## 28-oct-2026 — INTA36 (Gurú)
- **Planos que no coinciden con la voz** — "hay muchos planos que no tienen nada que ver con lo que estás diciendo; hablaste de Gurú y pusiste planos de pantalla normal, y hablas de ingenieros y no pones los planos donde hay ingenieros". → cada plano se **mira** (tira de fotogramas) contra la frase que cubre; si la voz nombra Gurú, el plano muestra Gurú en pantalla (Directorio, Software en pantalla = Gurú); si nombra ingenieros o soporte, equipos de soporte; si no hay plano así en el Directorio, se dice. El puntaje por palabras clave del selector no basta. (CLAUDE.md §4)
- **Textos como el video de referencia** — "quiero que los textos se parezcan más a este de referencia" (`06. Beneficios en educación PUBLICADO\Beneficios en educación_V1.mp4`). → palabras sueltas en negrita blanca a media altura y margen izquierdo, que entran una a una con su palabra de la voz y se acumulan en la línea; para énfasis, tarjeta blanca con texto azul alineado a la izquierda, línea ligera + línea en negrita. Sin textos de dos líneas abajo a la izquierda. (CLAUDE.md §1; `build_inta.py` función `pal`, `specs.py` `pal(...)` y `blanca=True`)

## Antes del 23-oct (resumen)
- Sin mouse en apps táctiles; jamás foto fija como plano (Veo 3.1). (CLAUDE.md §4)
- Música de percusión ≥160 BPM, voz -18 / música -24 LUFS; cortes 2-3 cuadros antes de la palabra. (CLAUDE.md §5-6)
- Paleta sin amarillo ni navy; logo oficial siempre. (CLAUDE.md §1-2)
- **Revisión de INTA36.0002 (Cris, 28-oct)** — "cuando dices lo de botón verde gurú no estás mostrando el botón gurú; hay un plano de una mano golpeando que sale menos de 1 segundo, que no tiene nada que ver; los textos sobre video no deben quedar así sueltos". → (1) lo literal se ve literal: «botón verde» exige el botón en el plano; (2) un plano sin relación con la frase y de <1 s rompe la regla de relación y el mínimo de 1,5 s: revisar cada tira, también los cortes de transición; (3) las palabras sueltas del estilo de referencia, tal como se montaron, no sirven: **pendiente de aclarar con Cris** cómo quiere los textos sobre video. (CLAUDE.md §1, §4)

## 2026-10-28 — Idea de Cris: storyboard antes del ensamble
- **Storyboard por IDs** — "en el momento que empiezas a listar planos, crea un storyboard, plano a plano, con la voz a la izquierda y el plano a la derecha, cada plano con un id; así puedo decir 'en este id pon este plano' y nos ahorramos tokens de export de previews". → nuevo paso 9b del proceso (puerta de aprobación antes del ensamble y del preview 720p). (CLAUDE.md, paso 9b)

## 28-oct-2026 · INTA37 · código de idioma de la voz
- **Cris:** «cuando le pidas la voz a ElevenLabs el `es` debe ser `es-CO`».
- **Verificado el mismo día:** la API rechaza `es-CO` (y `es_CO`, `es-co`) con 400 `unsupported_language` en eleven_v4, v3, multilingual_v2, flash_v2_5 y turbo_v2_5; solo acepta `es`. El conector de ElevenLabs de Claude tampoco tiene parámetro de idioma.
- **Estado:** pendiente de decidir con Cris cómo conseguir acento colombiano (la ruta de voz a voz desde fuente colombiana de `voz_inta.py` es la única que lo logró). `voz_v4_dirigida.py` lee `LC` (por defecto `es-CO`, hoy falla); pasar `LC=es` mientras tanto.

## 28-oct-2026 · INTA37 · la voz Hale es otra
- **Cris:** «asegúrate de estar usando este Hale: `wWWn96OtTHu1sn8SRGEr`» (en la API: "Hale - Expressive, Deep and Emotive"; la anterior `dXtC3XhB9GtPusIpNtQx` es "Hale - Smooth, Confident and Persuasive").
- **Regla:** la voz en off es `wWWn96OtTHu1sn8SRGEr`. Actualizado en CLAUDE.md (pasos y §6) y en `voz_inta.py` / `voz_v4_dirigida.py`. Las voces ya aprobadas con la anterior no se regeneran.

## 2026-10-28 · Proceso de voz definido (INTA36)
- **Cris:** «si se hace lo de la toma con Cristian Sánchez y luego el voz a voz a Hale ya quedaría bien, no gastemos a Gemini revisando». → la voz se genera siempre así (fuente `eleven_v3` estabilidad 0,1 → voz a voz a Hale con `eleven_multilingual_sts_v2` 0,4/0,75/0,3 → `voz_post.py` tempo 1,12), sin juez Gemini. **Reemplaza** «Hale directo con v4» (26-oct) y la validación con Gemini; CLAUDE.md paso 1 y §6; `voz_inta.py` con el juez apagado por defecto.
- **A confirmar:** el texto que Cris pegó lista Hale `dXtC3XhB9GtPusIpNtQx` (la de INTA36.0001-0006); la regla vigente del 28-oct (INTA37) es `wWWn96OtTHu1sn8SRGEr`. Se dejó la nueva como destino.

## 28-oct-2026 · INTA37 · voz aprobada (receta)
- **Cris:** la voz colombiana por voz a voz sonaba «súper plana, sin dirección, lentísima»; **«exp_d está perfecta»**.
- **Receta aprobada:** fuente = voz colombiana `o2vbTbO3g4GrKUg7rehy` con `eleven_v4`, `language_code=es`, guion dirigido más enérgico (etiquetas + MAYÚSCULA en el énfasis), `speed 1,12`, `style 0,6`, `stability 0,45`, speaker boost → voz a voz a Hale `wWWn96OtTHu1sn8SRGEr` (STS stability 0,2, style 0,7, similarity 0,7). 27,9 s, rango F0 ~137 Hz (la plana: 57 Hz, 41 s). El juez de Gemini la oye «España» aunque Cris la aprueba: **manda el oído de Cris, el juez es solo orientativo**. Script: `videos/onescreen-inta/voz_prueba37b.py`. Post de silencios con `TEMPO=1.0` (no volver a acelerar la voz aprobada).

## 2026-10-28 — Storyboard con revisión por toma
- **Cris:** «agregar una opción de comentario por plano, aprobar o rechazar, y un comentario general del storyboard, aprobar y rechazar; simple, determinista y que no te tome tiempo: tú solo cargas campos en una plantilla HTML ya hecha, puedes cargar varios videos y yo reviso cada storyboard video por video». → `herramientas/storyboard.py` + `storyboard_plantilla.html` (CLAUDE.md, paso 9b). Probado con un SPEC de dos videos: decisiones, comentarios, resumen por video y copiado funcionan.
- **Cris:** «ese copiar y pegar no sirve, que haya un botón de enviar y eso lo puedas leer». → botón Enviar + `storyboard.py servir` (servidor local que guarda `decisiones/<ID>.json`); se quitaron los botones de copiar. Probado: el JSON llega a la carpeta.
- **Cris:** «cuando haya planos rechazados, que cree uno nuevo con los planos pendientes, quizá trayendo 3 o 4 opciones nuevas y que yo elija la que es». → ronda de corrección en CLAUDE.md (paso 9b): storyboard vN+1 solo con las tomas rechazadas, 3-4 opciones por toma, elección con un clic. La plantilla y `storyboard.py` ya soportan `"opciones"`; probado (elegir B → `{"op": "B"}` en el JSON).
- **Cris:** «que no sean dos botones, uno solo que siempre sea de enviar todos los videos, que jamás deje enviar si hay cosas pendientes por decidir». → un solo botón «Enviar todos los videos», deshabilitado mientras falte una decisión (por toma o general, en cualquier video); lista lo que falta y marca las tomas pendientes. Probado: bloqueado al inicio y con un video a medias, habilitado al decidir todo, ambos JSON guardados.

## 2026-10-28 — INTA35 / INTA36: primera ronda de storyboard
- **Cris (INTA35):** S04 «usa pantallazos o recrea la interfaz y anímala» (plataforma Academy); S11 «mejor un motion graphics de un certificado llenándose»; S08 «un plano que sea de un caso de éxito»; S12 «usa un plano acá» (el CTA no va en tarjeta suelta); S02, S06 («otro valor de plano») y S09 («otra alternativa») rechazadas. Aprobadas: S01, S03, S05, S07, S10.
- **Cris (INTA36):** «no uses tarjeta final suelta»; S09 «eso no es Gurú» (el chat/AI Bot de Gurú no es el botón verde de soporte); pide un plano de un ingeniero OneScreen (S03), de alguien en una videollamada en pantalla (S04) y de alguien usando la pantalla (S01); elige C0005.MP4 para S02 y C0006.MP4 para S07 (Gurú). Aprobadas: S05, S06.
- **Reglas:** el CTA final va sobre un plano, no en tarjeta suelta; software/plataformas que no se pueden filmar se muestran con pantallazos o interfaz recreada y animada; lo que se nombra como proceso (certificar) puede ser motion graphic; Gurú = botón verde y soporte, no el chat de IA.

## 2026-10-28 — Storyboard: 4 opciones por toma, una sola capa
- **Cris:** «el botón de storyboard completo aprobar/rechazar sobra; mejor que siempre me traigas 4 planos desde el inicio y selecciones tú el que sea tu favorito, con eso es una sola ronda; si ninguno sirve, traemos 4 candidatos nuevos; siempre propón en uno de esos un motion graphic; no lo pensemos como capa 1 de planos y capa 2 de motions, sino todo en una sola capa, y yo elijo». → quitados los botones generales; cada toma lleva siempre 4 opciones (≥1 motion), mi favorita ★ preseleccionada, «Ninguna sirve → 4 nuevas»; los motion graphics solo se construyen si Cris los elige. (CLAUDE.md pasos 7 y 9b; `storyboard.py` + plantilla). Probado: elegir motion, «ninguna sirve» con comentario, bloqueo y envío con el JSON correcto.
- **Cris:** «en motion graphics no pongas la descripción del motion sino como un pantallazo del motion, para que se entienda; no tiene que ser animada ni construida, solo un pantallazo, si quieres con indicaciones de cómo será el movimiento». → la opción de motion es un fotograma dibujado (SVG 16:9, paleta de marca) con flechas e indicación escrita del movimiento; `storyboard.py` ya lo genera desde `boceto` (`boceto_svg`). Probado en la página.

## 2026-10-28 — Biblioteca de plantillas de motion
- **Cris:** «que tengas una referencia de motions, porque literalmente te tocará hacer un motion por plano; para que no sea tan pesado, que sea de plantillas». → `motion/plantillas.py` con 11 plantillas por tipo de frase (titular, cifra, flujo, comparación, lista3, tachado, hub, pantalla, checklist, CTA, barras); el storyboard las usa con `"plantilla"` + `"params"`; el build de HyperFrames se implementa al primer uso de cada una. (CLAUDE.md, sección «Plantillas de motion»)

## 2026-10-28 — Solo 3 opciones por toma
- **Cris:** «mejor solo 3 opciones». → cada toma trae 3 opciones (A-C), al menos una de motion y mi favorita ★; «Ninguna sirve» trae 3 nuevas. (CLAUDE.md pasos 7 y 9b, ronda de corrección, checklist; página y script del storyboard)

## 2026-10-28 — Rediseño del motion: referencias reales, degradados y color por significado
- **Cris:** «no me gusta el diseño, se siente torpe, viejo, de presentación plantilluda de PowerPoint»; «busca videos que realmente sean Apple lettering, mira pantallazos, copia los diseños»; «usemos texturas y gradientes así como estos» (cotizaciones de Gurú y Academy); «verdes solo cuando es de Gurú, azules cuando hablamos de solución, blanco cuando exponemos o enseñamos algo»; «no uses esos titulitos en mayúscula tipo título de diapositiva». → plantillas v3 (`frase` estilo Apple con degradado en la palabra clave, `panel4` tipo cotización, tarjetas de vidrio, fondos con degradado y textura, temas gurú/solución/explicar, sin rótulos en mayúscula). Referencias descargadas y medidas en `D:\OneScreen\Contenido\2026\10. Octubre\_referencias_motion\apple\`. (CLAUDE.md «Plantillas de motion»; `estilo-onescreen/05_MOTION.md` §8)

## 2026-10-28 — Ideas de diseño de motion (siete referencias de Cris)
- **Cris:** «mira estas ideas, pilas: no me cambies los colores ni las tipografías, son ideas de diseño de motion design; que los contenedores parezca que brillaran; jamás dejes un fondo estático, siempre algún movimiento, así sea sutil». → fondos con aurora + grano + rejilla que SIEMPRE se mueven, contenedores con halo y borde de luz, marcador sobre la frase clave, número fantasma, órbita con destello, indicador de progreso; `motion/boceto.py` y `plantillas.py` actualizados y probados. (CLAUDE.md, «Plantillas de motion»)

## 2026-10-28 — Segundo lote de referencias de diseño (nueve imágenes)
- **Cris:** envió nueve referencias más (notificación con pila de capas, gráfica de área, palabras en píldoras, anillos con íconos, chips flotantes, contenedor con borde degradado, pregunta SÍ/NO con flechas, tarjetas con objeto que rompe el borde). → 8 plantillas nuevas en `motion/plantillas.py` (`notificacion`, `curva`, `palabras`, `orbitas`, `chips`, `ruta`, `pregunta`, `tarjeta_plano`), 23 en total, con el renderizador ampliado (borde de degradado, área con degradado). Imágenes en `_referencias_motion\ideas\`. Siguen valiendo: colores y tipografías de OneScreen sin cambios, fondo siempre vivo, contenedores que brillan.

## 2026-10-28 — Cada referencia es una plantilla; nunca se reemplazan
- **Cris:** «no, pero estás reemplazando las anteriores con estas; la idea es que cada idea que te he mandado sea una referencia de diseño y la guardes como plantilla, con eso siempre tendrás de dónde escoger». → biblioteca por referencias: una plantilla por referencia con su imagen (`REFERENCIAS`) y ejemplo (`EJEMPLOS`) en `motion/plantillas_ref.py`; 12 plantillas nuevas (35 en total) y catálogo visual `motion/catalogo.py` (referencia ↔ plantilla). Referencias 17-19 guardadas en `_referencias_motion\ideas\`. (CLAUDE.md, «Plantillas de motion»)

## 2026-10-28 — Plantillas mal armadas, objeto copiado, patrones y catálogo completo
- **Cris:** «hay varias plantillas mal armadas, cosas se sobreponen sobre otras, y en una pusiste el coso de médico de la referencia; los patrones de puntos o cuadrícula deberían ser más sutiles»; «no veo todas las referencias que te he pasado, ¿dónde tienes el catálogo completo?». → revisor de armado (`boceto.revisar`) y retoques en `linea`, `puntos_halo`, `cita_tarjeta`, `linea_neon`, `esfera_suave`, `palabra_halo` (se quitó el estetoscopio: marcador neutro); puntos/rejilla casi imperceptibles; catálogo reescrito: parte 1 con TODAS las referencias guardadas (22 imágenes + fotogramas de Apple) y su plantilla; referencias 20-22 con sus plantillas (`curvas_tarjetas`, `dashboard_flotante`, `infografia_paneles`). (CLAUDE.md, «Plantillas de motion»)

## 2026-10-28 — Las referencias son estilo, no plantillas: componer escenas propias
- **Cris:** «en vez de coger el estilo de diseño, lo cogiste literalmente como plantillas y no sales de ahí; esto eran referencias, pero debes tener la capacidad de crearlos tú solo basado en esos estilos». → `motion/elementos.py`: vocabulario de 23 elementos y compositor libre `escena()`; las plantillas pasan a ser ejemplos; principios del estilo y método de composición en CLAUDE.md («Sistema de diseño de motion»); el storyboard acepta `"escena"` además de `"plantilla"`. Probado con 4 escenas compuestas desde cero. Falta: construir cada escena en HyperFrames.

## 2026-10-28 — Del guion a ideas de motion + lienzo de elementos UI
- **Cris:** «intentemos algo: que lo que está escrito en el guion cree automáticamente ideas para el motion design, ideas para volver ideas abstractas en temas de animación abstracta»; «crea un lienzo donde tengas los elementos UI». → `motion/ideas.py` (guion → 3 metáforas visuales por frase, léxico de 17 ideas abstractas, variación automática de luz y composición) y `motion/lienzo.py` (lienzo con los elementos en los tres colores y su código); 6 elementos abstractos nuevos. Probado con un guion de 7 frases de INTA36. (CLAUDE.md, «Guion → ideas de motion»)

## 2026-10-28 — Prohibidas las píldoras y las redes de nodos
- **Cris:** «no uses píldoras, no uses este tipo de redes, prohibidas» (con captura de la red de nodos). → CLAUDE.md §2; se quitó `pildora` y `red` del vocabulario (`boton` rectangular de esquinas suaves en su lugar), se retiraron las plantillas `palabras` y `hub`, se redondeó menos todo lo que era cápsula (barras, filas, toggles, burbujas, pestañas, indicador de progreso) y el revisor de armado marca «píldora prohibida». Las ideas de equipo y conexión ya no usan redes. Verificado: el catálogo, las ideas del guion y las escenas de ejemplo salen sin avisos.

## 2026-10-28 — Storyboard 3 planos + 2 motion; evaluar los planos mirándolos, sin repetir ni tomas falsas
- **Cris:** «el storyboard me muestra 3 planos y 2 motion designs, y que escoja el favorito. En una prueba con 3 videos repetía al menos la mitad de los planos entre los 3; ponía tomas falsas, gente tomándose fotos y riéndose, que no servían; no es solo hacer el fetch del Directorio, es también ver los planos y evaluar si sirven». → 5 opciones por toma (3 planos A-C + 2 motion D-E) en CLAUDE.md (paso 9b, ronda de corrección, checklist), la página y el script del storyboard; nueva regla de evaluación visual en §4 (mirar cada plano, prueba de relevancia, lista de tomas falsas rechazadas, ningún plano repetido entre los videos de un lote, pool de 3×); `storyboard.py` avisa si una toma no trae 3+2 o si un plano se repite entre videos; `ideas.py` genera 2 ideas por frase.


## 2026-10-28 — INTA20-22: sin barrido de entrada en los motion
- **Cris:** «no me gustan las transiciones» (el barrido de izquierda a derecha con que entraba cada motion). → `build_inta_sb.py` quita el `clipPath`; el motion entra por corte directo. Regla en CLAUDE.md §2.

## 2026-10-28 — Un solo preview (16:9); todo lo demás, tras aprobar
- **Cris** (viendo que un lote de 3 piezas renderizaba 3 formatos cada una): «el proceso debe ser que solamente haga 1 preview, si queda bien, ahí sí coloreamos y luego sí pasamos a renderizar todo; renderizar así todo para preview es desperdicio». → CLAUDE.md paso 12: **un solo preview 16:9 a 720p por pieza** (por video si son varios, no 3×3); nada de 9:16, 4:5, .prproj, color, 4K ni variantes antes de la aprobación; los otros formatos se revisan con fotogramas fijos; orden tras aprobar: color → 4K 16:9 → recortes 9:16/4:5/1:1 → variantes. Ajustados también §3, reglas transversales, checklist, H.4 y la fila de render (`FMT=16` para el preview).


## 2026-10-28 — INTA20-22: la voz sonaba mal (receta vieja)
- **Cris:** «¿por qué no seguiste las indicaciones de claude.md de ponerle director, velocidad?»; «suena una mierda». → los previews .0003 usaron la voz del 27-oct (eleven_v3 + tempo 1,12 en el post), no la receta aprobada en INTA37 (v4, speed 1,12, guion enérgico, sin acelerar). Se regeneró en `Voz\v0003\` con `voz_exp_d.py`; CLAUDE.md §6 lleva la receta vigente arriba. Antes de montar con una voz hay que comprobar su receta y entregarla a escuchar.


## 2026-10-28 — Videos de producto para Mercado Libre (12 SKU): voz, motion y gasto de la API
- **Cris:** «hagamos el video tipo producto, con los specs más importantes» y, al ver el primero: «¿por qué no tiene voz?»; «en el segundo 9 hay un frame que quedó colado del original»; «métele más motion graphics, eso solo son planos ahí quietos sin gracia y specs sueltos»; «créale un guion estilo producto de Apple que complemente esos videos»; «no uses los modelos más caros de video, no uses muchos intentos porque esto gasta dinero real»; «completa lo que falte con motion graphics, pero no dejes sin planos». → Un video de producto **lleva voz** (receta única, `voz_exp_d.py`) con guion corto estilo Apple, una frase por escena, solo datos de la ficha; los clips de Omni se **recortan 0,4 s al inicio** (arrancan con la imagen de referencia estática: ese era el frame colado); plano y escena de color con motion se **alternan** (cifras que cuentan, anillos, barras, arcos, producto flotando); cada clip generado cuesta dinero: **un intento por clip**, nunca reintentar uno vacío ni fallido, el modelo es `gemini-omni-1.1-flash` (Veo 3.1 fue retirado; ~US$0,10/s a 720p; Tier 1: 4/min y 20/día) y se prefiere **2 clips por video** + motion graphics; **ningún video queda sin planos**. (CLAUDE.md, «Videos de producto»)

## 2026-10-28 — INTA23/INTA27: voz, pronunciación, caso de éxito y marca
- **Cris:** «DEBES REGENERAR LA VOZ, NO REUTILIZAR» (las tomas viejas); «23 pone AI y lo pronuncia en inglés, debe ser IA; QuizWiz = Cuis Wis, SuprNotes = Supr Nouts, Lessn = leson, Gurú como suena en español, Scrybe = escraib, LearningHub = lernin jab, Sage = seich»; «27 no limpiaste el audio del caso de éxito, y solo usaste un plano de Areandina»; «nunca escribas One Screen».
- → Voz nueva con `voz_exp_d.py` (guion dirigido enérgico) y las marcas escritas como suenan en `guion_dirigido_v3.txt` (glosario en memoria `pronunciacion_marcas_voz`; IA = `i-a`). El audio de un caso de éxito se limpia con Adobe Enhance Speech antes de montarlo (`voz_compuesta_27.py` usa `INTA27_extracto_enh.wav`). En un extracto de caso se usan varios planos del caso (cortes de ~2 s), no uno solo. La marca se escribe siempre «OneScreen» junta, también en los subtítulos (Scribe la parte en «One Screen»: `build_inta_sb.py` la une). Reglas en CLAUDE.md §1 y §6.

## 2026-10-28 — INTA23/INTA27: wiggle y tercio
- **Cris:** «ponle un tercio cuando hable la vieja de Areandina para que sepamos quién es y el cargo»; al aprobar 23 y 27: «en ninguno pusiste wiggle» (confirmó: planos y motion graphics).
- → Tercio inferior (nombre + cargo, sin caja, barra azul fina) cuando habla una persona de un caso, con ella A CÁMARA (no sobre planos de apoyo): `montaje_aprobado.json` lleva `tercio` y `build_inta_sb.py` lo dibuja. **Wiggle por defecto** en planos y en el contenido de los motion (vaivén leve y determinista de posición y rotación, `wig()` en `build_inta_sb.py`; `WIGGLE=0` lo apaga). Un cambio de estilo = ID nuevo.



## 2026-10-28 — Lápiz (Mercado Libre): Claude no colorea; se entrega .prproj
- **Cris:** «no le pongas color a los planos del lápiz, genera el prproj para que yo coloree, no tienes autorización a colorear nada» (antes: «no uses el video exportado»). → Claude coloreó con `grade/pipeline.py` sin que Cris lo pidiera: se borraron esas copias y el proyecto montado con ellas, y se generó `LAPIZP\Premiere\LAPIZP_planos_para_colorear.prproj` (3 originales 4K sin color, `ml_lapiz.py prproj`). **Regla:** el color de los planos S-Log3 lo pone Cris en Premiere; el pipeline automático solo se corre si Cris lo pide en esa conversación. Con material que Cris pasa, solo planos crudos (nunca el video exportado). (CLAUDE.md, «Videos de producto»)


## 2026-10-28 — Videos de producto: sin silencios, título cortado, producto fiel al real
- **Cris:** «tienen silencios entre la narración, corta eso, no importa que el video quede más corto»; «el título de SnapCam 2 se ve cortado»; «póster te quedaron mal, el producto en los planos no es igual al real». → El montaje **sigue a la voz**: cada escena dura lo que su frase (+0,2 s) y los planos se reparten sobre esa duración (el A10W pasó de 30 a ~26 s); `tam()` mide con Rubik 800 (0,74 em por carácter; con 0,60 se cortaban títulos y cifras anchas); el cierre tiene ancho máximo. **Póster (OSP-72):** los clips de IA alteraron el producto (se veía una pantalla grande en lugar del póster delgado de 62 × 173 × 3,3 cm): export descartado en `Exports\_rechazados\`; se regeneran 2 clips con prompts que fijan las proporciones, y se compara cada clip con el render de la ficha antes de usarlo. (CLAUDE.md, «Videos de producto»)

## 2026-10-29 — Storyboards: siempre los mismos planos, tomas falsas y wiggle
- **Cris:** «en todas las pruebas de estos tres días siempre me trae los mismos 20 planos, no hay variación; quiero que solo me pueda proponer un mismo plano 1 vez cada 15 storyboards»; «ponle un botón de papelera al storyboard para vetar planos: ayer me sacó muchas tomas falsas, gente riéndose, incluso alguien dibujando un pene en una pantalla»; «lo que sea medible que sea medible y no solo instrucción»; «agrega lo del wiggle como lo hicimos en la sesión de 23 y 27».
- → **Rotación:** un plano propuesto no vuelve hasta 15 storyboards después (`planos_rotacion.py`, `registro/planos_propuestos.json`; lo aplican `seleccion.py` y `storyboard.py`). **Papelera 🗑** en cada plano del storyboard: veto permanente al instante (`registro/planos_vetados.json`). **Filtro automático de tomas falsas** por la ficha del Directorio (`FALSA` en `seleccion.py`). **Reglas medibles** convertidas en errores que detienen el script (tabla en CLAUDE.md). **Wiggle:** el vigente es el Camera Wiggle de Cris (`cam_wiggle()` + `motion/camera_wiggle.json`), no el `wig()` por elemento que decía §2; el builder no arma si no quedó aplicado. (CLAUDE.md §2, §4.6-8, paso 9b, «Reglas que se miden en código»)

## 2026-10-29 — Reencuadre a ciegas en los verticales
- **Cris:** «cuando está reencuadrando no está mirando qué está reencuadrando, solo lo está haciendo y ya; debe revisar»; «no uses Gemini».
- → `revisar_encuadre.py` (local: ffmpeg + OpenCV): hoja de contacto por formato con la ventana del recorte y el peor caso (zoom + empuje + Camera Wiggle); se mira cada hoja, se marca el foco de cada toma en `notas.json` y se MIDE que quepa; `build_inta_sb.py` no arma 9:16/4:5/1:1 sin `revisado.json` vigente. Revisión hecha: INTA27 (S02 cortaba la mano que escribe, S07 dejaba fuera a la presentadora, S08c y S11 cortaban cara o lápiz; corregidos) e INTA23 (S03 cortaba las palabras, S06 era solo una espalda, S12 solo una nuca; corregidos). Los verticales de INTA23.0006 ya renderizados llevan los cortes viejos. (CLAUDE.md paso 14 y «Reglas que se miden en código»)

## 2026-10-29 — INTA41: planos de colegio y casos de éxito antes de 2024
- **Cris:** «usa los planos de colegio san mateo, lo importante es mostrar planos de colegios con OneScreen, pueden ser de casos de éxito»; «quita esa regla de 2024 para lo que sean casos de éxito»; «40 minutos para escoger un plano????».
- → La regla de 2024 no aplica a los casos de éxito (`registro/planos_casos.json`, que eximen `seleccion.py` y `storyboard.py`). En piezas de colegios, primero los planos de casos de colegios con OneScreen, aunque tengan menores o pidan aprobación. Escoger planos debe ser rápido: ir directo al material del caso en vez de recorrer todo el Directorio.
