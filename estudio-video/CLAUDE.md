# Estudio de video OneScreen — instrucciones para Claude

Esta carpeta es el punto de partida para hacer **cualquier video de OneScreen LATAM** con Cristian (Cris). Aquí viven las reglas, la memoria de video, el mapa del sistema de diseño y el de herramientas. No empieces un video sin leer esto.

## Al empezar una sesión de video
1. **Este archivo es todo lo que hace falta:** proceso de 16 pasos, reglas, Directorio de planos, hoja de producción, checklist, herramientas y proyectos. (`SKILL.md` es solo el cargador de la skill `video-onescreen`.)
2. Si el video es de una línea ya hecha, mira su ficha en **Proyectos** y reutiliza su builder. Abre solo las notas de [memoria/INDEX.md](memoria/INDEX.md) que toquen la tarea.
3. Antes de renderizar: **Herramientas y trampas**. Antes de entregar: **Checklist**.
4. En la nube: primero lo que pide el `CLAUDE.md` de la raíz (`bash privado/desbloquear.sh` si hay que usar claves).
5. Esta skill decide **qué** y **cómo se ve**; las skills de HyperFrames (`hyperframes`, `hyperframes-core`, `media-use`…) dicen **cómo se escribe**.

## PROCESO OBLIGATORIO: los 16 pasos (se siguen siempre, en orden)

### A. Audio
1. **Voz con ElevenLabs: UNA sola receta, siempre (Cris, 28-oct), con guion dirigido enérgico.** Se genera con `videos/onescreen-inta/voz_exp_d.py` (detalle en §6). **Prohibido** usar otro modelo, otros ajustes o acelerar en el post; no se prueban variantes ni se «reajusta». Una voz ya aprobada por Cris no se regenera.
2. **Listar los planos** desde el [Directorio de video](https://docs.google.com/spreadsheets/d/1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w/edit?gid=0#gid=0) según lo que dice el guion (solo grabados desde 2024, sin los vetados, sin fotos fijas; REGLAS §4). **El fetch al Directorio solo da candidatos** (traigo al menos 3 veces los que hacen falta por toma): **cada candidato se evalúa MIRÁNDOLO** y se descartan las tomas falsas, y los videos de un mismo lote **no comparten planos** (§4, «Evaluar los planos»).
3. **Con la lista de planos y la voz hecha, cortar los silencios** de la voz desde el origen (`videos/onescreen-inta/voz_post.py`: recorta silencios >0,22 s a pausas de 0,14 s, sin tempo, y repite Scribe; `bajar_voz.py` del Rental ya no se usa).
4. **Identificar dónde empieza y dónde acaba el guion** dentro de la voz (inicio, fin y cierre del hook).
5. **Música:** el **punto de giro** de la canción cae justo cuando termina el hook de la voz. La música sale **solo de la carpeta de masterizados** (`Mezcla de música\Masterizadas`). Una canción distinta por pieza.
6. **Transcripción con marcas de tiempo por palabra** (Scribe) del audio ya listo. Con base en ella se crean los motion graphics y se ensambla.

### B. Dos procesos en paralelo
7. **Motion graphics y textos sobre fondos** según lo que dice la voz: **muy explicativos y sincronizados** con la palabra, hechos con **HyperFrames**. **Aún no se construyen:** primero van como **pantallazo estático con indicación de movimiento como los 2 motion designs de cada toma del storyboard** (paso 9b); solo se construyen en HyperFrames los que Cris elija. Estilo y diagramación: REGLAS §1-3.
8. **Revisar los planos:** si existen en el disco, se jalan de ahí (col. AM del Directorio); si solo están en Drive (col. AN), se descargan.
9. **Validar qué partes de cada plano sirven:** descartar movimientos de cámara (comunes al iniciar y al parar la grabación) y quedarse con tramos que **realmente describan lo que dice la voz**, no solo lo que parece que dice. Para validar de más, leer el video con la API de Google AI Studio (Gemini). Esto es parte de la **evaluación visual** de §4: se mira la tira de fotogramas de cada tramo; no se ofrece un plano que no se haya visto.
9b. **STORYBOARD — puerta de aprobación antes del ensamble** (idea de Cris, 28-oct). Se empieza a armar al listar los planos (paso 2) y se entrega cuando ya hay tiempos por palabra (paso 6) y tramos validados (paso 9): una **tabla plano a plano, con la voz a la izquierda y el plano a la derecha**, sincronizados. **Una sola capa:** el video es una secuencia de **tomas**; cada toma es lo que se ve en pantalla en ese tramo, **un plano o un motion graphic** (no hay «capa de planos» y «capa de motions»). Cada fila lleva un **ID de toma** (`S01`, `S02`…), el rango de tiempo, la frase exacta de la voz y **SIEMPRE 5 opciones desde el inicio: 3 planos (A-C) y 2 motion designs (D-E)**, en ese orden. Los **planos** son reales, con su fotograma, ID del Directorio y tramo (in-out), y **ya evaluados mirándolos** (§4, «Evaluar los planos»; ningún plano repetido entre los videos del lote). Cada **motion design** es **una propuesta mostrada como un pantallazo estático** (un fotograma dibujado del motion, 16:9, con la paleta de la marca; **no se anima ni se construye**), con flechas punteadas e indicación escrita de cómo se movería (de preferencia con `"plantilla"` + `"params"` de la biblioteca, sección «Plantillas de motion»; a mano, `boceto` en el SPEC con `boceto_svg`: rect, circ, txt, linea, flecha). No se pone solo la descripción en texto. **Yo marco mi favorita con ★ (puede ser un plano o un motion design) y la dejo preseleccionada**; Cris solo cambia la que no le guste. La duración de la toma se marca en rojo si es <1,5 s. Se entrega como página HTML por link clicable en `…\<Pieza>\Storyboard\` (`storyboard_<ID>_vN.html`). **Se genera con `herramientas/storyboard.py`** (determinista: yo solo relleno un `SPEC.json` con las tomas y el script rellena la plantilla `storyboard_plantilla.html`, que ya está hecha; puede cargar **varios videos** en una misma página). En la página Cris revisa video por video: **elige una de las 5 opciones por toma con un clic** (o pulsa «Ninguna sirve → traer 5 nuevas») y puede dejar un comentario por toma y uno general (opcional); **no hay botones de aprobar/rechazar del storyboard completo**: elegir las opciones es la aprobación. Hay **un solo botón, «Enviar todos los videos»**, que **no se habilita si alguna toma queda sin opción elegida** (la página muestra cuáles faltan); al enviar guarda sus decisiones en `…\Storyboard\decisiones\<ID>.json` y **yo las leo de ahí** (sin copiar y pegar). Para que funcione, **al entregar el storyboard levanto el servidor en segundo plano** (`python estudio-video/herramientas/storyboard.py servir SALIDA.html`, `run_in_background`) y le paso el link `http://localhost:8765/…`; tras su «ya envié» leo el JSON, aplico los cambios en el SPEC, regenero la página (nueva versión) y **no renderizo nada** hasta que el storyboard esté aprobado. Solo con el storyboard aprobado se ensambla: así los cambios de planos se hacen en el papel y no en previews exportados.

   **Ronda de corrección (protocolo fijo, para toda sesión futura):**
   1. Tras el «ya envié» de Cris, leo `…\Storyboard\decisiones\<ID>.json` (si no lo menciona, reviso esa carpeta: siempre hay que mirarla al retomar un video). `d: "ok"` = aprobada y queda; `d: "no"` = rechazada, con su comentario.
   2. **Una sola ronda en el caso normal:** como cada toma ya trajo 5 opciones (3 planos + 2 motion designs) y mi favorita preseleccionada, lo que Cris envía (`op` = la opción elegida, `elegido` = su descripción) **es** el montaje. Las tomas con `d: "ok"` quedan fijadas.
   3. **Solo si una toma llega con `d: "no"`** («Ninguna sirve»): genero un storyboard nuevo (vN+1) **solo con esas tomas**, con **3 planos y 2 motion designs nuevos** cada una (mismas reglas: tramo sin movimientos de cámara, ≥1,5 s, desde 2024, sin vetados, mirando el fotograma contra la frase y el comentario de Cris, sin repetir lo ya mostrado; de nuevo 3 planos + 2 motion y mi favorita ★; un plano rechazado no vuelve a aparecer). Levanto el servidor y le paso el link.
   4. Con cada envío fusiono las elecciones en el SPEC maestro. Cuando todas las tomas tengan opción elegida, el storyboard queda aprobado y recién ahí se ensambla (paso 10 en adelante) y **solo se construyen los motion graphics elegidos**.
   5. Cada ronda se guarda como `storyboard_<ID>_vN.html` y `decisiones/` conserva el último envío; no se sobrescribe un storyboard ya entregado.

### C. Ensamble y preview
10. **Ensamblar.** **Ningún plano dura menos de 1,5 s**, ni de motion ni de video.
11. **Validar márgenes** y diagramación según las reglas (REGLAS §3): nada fuera de zona segura, ningún gráfico pisa un texto.
12. **UN SOLO preview por pieza: 16:9 a 720p** (solo con el storyboard aprobado; corrección de Cris, 28-oct): render fiel pero rápido. **Antes de aprobarlo NO se renderiza nada más:** ni 9:16, 4:5 ni 1:1, ni el `.prproj`, ni el color, ni los 4K, ni las variantes; renderizarlo todo para un preview es un desperdicio. Si Cris pidió **varios videos a la vez, un preview 16:9 por video** (no 3 piezas × 3 formatos). Los cruces de texto y los márgenes de 9:16 y 4:5 se revisan con **fotogramas fijos** de las escenas críticas, sin renderizar video. Se entrega por link clicable. 🚦 **Puerta de aprobación.** Si corrige: se aplica, se registra un ID nuevo y se vuelve a renderizar **solo ese preview 16:9**.
    **Orden fijo tras la aprobación del preview:** (1) color: `.prproj` y Cris colorea (paso 13); (2) render final 16:9 en 4K; (3) recortes 9:16, 4:5 y 1:1 (paso 14); (4) variantes de voz e idioma (15-16). Solo ahí se renderiza todo.

### D. Tras aprobar el preview
13. **Generar el `.prproj`** con los clips necesarios. **Si el plano ya tenía color, ese color va en el archivo; si no, queda normal y Cris lo colorea.** Cris exporta en alta calidad y, **con base en ese export**, se hace el export final **16:9 en 4K**. El corte coloreado se registra en la col. AB del Directorio.
14. **En paralelo, los recortes 1:1, 4:5 y 9:16** (aquí se renderizan por primera vez estos formatos, nunca antes del visto bueno del preview), revisando que los puntos de atención (rostro, pantalla, QR) queden bien encuadrados.
15. **Exportar** y luego sacar las **versiones alternas en español mexicano**: la voz se genera con ElevenLabs y se limpia con **Enhance Speech de Adobe** (solo la voz, sin música) antes de montar.
16. **Versiones para Brasil** (pt-BR).

### Reglas transversales
- **Una versión hasta que Cris aprueba.** Las variantes (15-16) van después, con el estilo ya corregido.
- **Solo se produce desde un guion aprobado** (Guiones: Estado y Decisión = Aprobado; SKILL §3b.4).
- **Registro:** antes de exportar, `registro.py nueva` da el ID y el nombre canónico (`<ID>_<H#C#A#>_<voz>_<formato>[_preview]`; el ID nunca va impreso en el video). Cada versión nueva = ID nuevo. Al aprobar: fila escrita y releída en la hoja de producción, usos en el Directorio, exports sin `_preview` a Drive.
- **Entrega siempre con link clicable** (`file:///D:/…`, espacios `%20`), un link por archivo, en el mismo mensaje.
- **Todo en D:** `D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\`; nada en C: (REGLAS §7b).
- **Una corrección de Cris** va a CORRECCIONES.md y en las Reglas de este archivo en el mismo momento.
- Se dice con honestidad lo que no se pudo abrir o verificar (p. ej. un `.prproj` generado a mano: Premiere solo se prueba abriéndolo).

## Detalles técnicos por paso

### Voz con eco o mala calidad (pasos 1 y 15)
Si una voz suena con eco o calidad baja (le pasó a la mexicana), se pasa **solo la voz, sin música**, por Adobe Enhance Speech (`media_enhance_speech`) antes de montar: se sube el WAV (`asset_initialize_file_upload` → PUT con curl al enlace que devuelve → `asset_finalize_file_upload`), se corre Enhance Speech y se baja la pista `enhanced_speech` (las otras dos son fondo y reverb). La duración no cambia: los tiempos de Scribe y los SFX siguen valiendo. El resultado es una versión nueva con ID nuevo.

### Planos y color (pasos 2, 8, 9, 13)
- Un plano "tiene color" solo si su clip lleva Lumetri dentro de su prproj (cadena `ComponentOwner/Components` del `VideoClipTrackItem`); el "Sí" de la col. Z puede ser falso. Si ya existe un corte coloreado (col. AB), se usa ese.
- `PLANOS=1 python build_prproj.py SALIDA.prproj` arma un prproj de planos sueltos, a su duración final, y clona como punto de partida el Lumetri de los proyectos donde el plano ya tenía color; escribe `*.planos.json`. Tras el export de Cris se corta por plano con ese archivo y `trims_*_color.py` alinea los cortes a la línea de tiempo del builder.
- **Fotos dentro de gráficos animados** van horneadas en la capa de gráficos y congelan el último cuadro; en 9:16 y 4:5 salen del plano completo en horizontal (`media/c_<plano>.mp4`).
- El .cube de Lumetri no sirve fuera de Premiere.

### Variantes en lote (pasos 14-16)
`herramientas/render_rental_variantes.sh ID ACC SCRIBE.json VOZ.wav "16 9 45"` copia el proyecto de cada formato, reconstruye con los tiempos de esa voz, rehace la mezcla (los SFX se atan a las palabras de cada voz), renderiza, aplica el post y copia a `Exports\` con el nombre canónico. Para otro idioma: traducir los textos en pantalla y atar los eventos a las palabras de su narración (`make_pt3.py` es la plantilla) e indicar `BUILDER`, `INTRO_TPL` e `INTRO_AUD`.

### Si hay que generar un .prproj (paso 13)
- Parte de la plantilla de Cris (`C1186.prproj`) con `build_prproj.py`; V1 = master coloreado, V2 = capa de gráficos con alfa (4K, ProRes 4444), A1 = audio.
- **Trampas que hacen que Premiere diga "el proyecto parece dañado":** (1) los saltos de línea del texto XML incrustado se escriben como `&#10;` y las tildes en UTF-8 directo (`prser.py` reproduce el archivo byte a byte); (2) los datos base64 de los parámetros Arb (Lumetri/Look) van **solo en la primera aparición de cada `BinaryHash`**; al clonar hay que rellenarlos (`collect_hashes`/`fix_hashes`). Probar siempre con un control: la plantilla sin cambios debe abrir, y de ahí añadir etapas (variables `STOP`, `NOMASTERS`, `NOCLIPS`, `NOTRACKS`, `NOCOLOR`, `NOMOTION`, `COLORONLY`).

### Para un video nuevo
1. Copia el builder más parecido (hoy `videos/onescreen-quizwiz-scrybe/build_rental3.py`) a `videos/<nuevo>/` y cambia beats, textos y planos.
2. Mantén el sistema: `lets/big/w3/flip/camera` para el lettering 3D, `bgs` para escenas de color, `stg`/`pth`/`draw`/`packet` para diagramas, tarjetas con plano + mini-diagrama.
3. Usa una diagramación distinta en cada escena; no repitas título-izquierda/gráfico-derecha.

## Sistema de diseño de motion: COMPONER, no copiar (28-oct)
**Corrección de Cris:** «en vez de coger el estilo de diseño, lo cogiste literalmente como plantillas y no sales de ahí; esto eran referencias, pero debes tener la capacidad de crearlos tú solo basado en esos estilos». Las referencias son **estilo**, no moldes. Por eso hay dos niveles:
- **Vocabulario + compositor libre** (`motion/elementos.py`): una escena se **compone** desde cero para la frase concreta, con elementos sueltos y posiciones libres: `escena({"tema": ..., "fondo": {"luz": ...}, "elementos": [{"e": "titulo", ...}, {"e": "vidrio", ...}, ...]})`. En el SPEC del storyboard una opción es `{"tipo": "motion", "escena": {...}}`. Elementos: `texto`, `titulo` (líneas light/bold con degradado), `marcador`, `vidrio`, `blanca`, `chip`, `boton`, `burbuja`, `punto`, `anillos`, `orbita`, `destello`, `cursor`, `curva` (neón, área, punto final), `barras`, `icono`, `linea`, `flecha` (esquinas redondeadas), `fantasma`, `plano` (marco del plano del video que puede romper un vidrio), `progreso`, `notificacion`, `tarjeta_stat`. Se dibujan en el orden dado: lo primero queda al fondo, así una palabra o un plano puede ir detrás o delante. Ejemplos de escenas compuestas: `motion/escenas_ejemplo.py`. Si falta un elemento que la frase pide, **lo agrego al vocabulario** (y lo documento aquí) en vez de forzar una plantilla.
- **Plantillas** (`plantillas.py`, `plantillas_ref.py`): son **ejemplos de composición** (few-shot) para arrancar o inspirarme, **no el límite**. Lo normal es una escena a la medida que mezcla elementos de varias referencias; una plantilla se usa tal cual solo si de verdad es lo mejor para esa frase.

**Prohibidos: píldoras y redes de nodos (ver §2).** **Principios del estilo (extraídos de las referencias, con los colores y tipografías de OneScreen):**
1. **Fondo:** degradado profundo del color del significado + **aurora** que sube desde un borde (cambia de lado entre escenas: `luz` = abajo, arriba-der, abajo-der, centro, izquierda…) + grano fino + textura casi invisible. **Siempre se mueve.**
2. **Contenedores:** de vidrio o blancos, siempre con **halo y borde de luz**; capas apiladas dan profundidad; lo importante **rompe el borde** del contenedor (un plano que sobresale).
3. **Tipografía:** frases cortas, **light + bold mezclados**, tracking cerrado, **una palabra con degradado o marcador**, contraste de tamaños (gigante solo para impacto) y un **número o palabra «fantasma»** gigante en contorno detrás.
4. **Composición:** asimétrica, mucho aire, un foco por escena; texto a un lado y el objeto al otro, o centrado con elementos satélite; profundidad en capas (detrás/delante). **Nada se sobrepone** (revisor `boceto.revisar`).
5. **Apoyos:** chips con ícono, burbujas de valor, cursor con nombre que hace clic, anillos y órbitas con destello, curvas con punto brillante, barras con degradado, flechas que se dibujan por la pantalla, indicador de progreso.
6. **Movimiento:** fondo vivo; entradas escalonadas atadas a la voz; trazos que se dibujan; rebote solo en íconos, burbujas y botones; brillo que cruza los vidrios.
7. **Variar:** dos escenas seguidas no comparten lado de luz, composición ni elementos principales.

**Cómo compongo una escena (siempre en este orden):** (1) leo la frase y decido **qué idea visual la representa** (no un adorno); (2) elijo el **color por significado** (gurú/solución/explicar); (3) elijo la **luz** distinta a la de la escena anterior; (4) escojo 2-4 elementos del vocabulario y los **mezclo de referencias distintas**; (5) compongo con jerarquía y aire; (6) paso el revisor de solapes y miro el pantallazo; (7) escribo la indicación de movimiento. Si después de componer se parece demasiado a una plantilla existente, la cambio.

## Guion → ideas de motion (automático) y lienzo de elementos UI (28-oct)
**Idea de Cris:** que lo escrito en el guion **cree automáticamente ideas de motion design**, convirtiendo ideas abstractas en animación abstracta.
- **Generador** (`python estudio-video/motion/ideas.py GUION.txt --html ideas.html --spec spec.json`): lee el guion (una frase por línea; opcional «t0-t1 | frase»), detecta por frase qué **idea abstracta** contiene (rapidez, siempre, confianza, gratis, equipo, conexión, avance, ahorro, aprendizaje, soporte, orden/caos, sencillez, tecnología, pregunta, cifra, aula, contacto) y propone **2 metáforas visuales** distintas, ya compuestas con el vocabulario y el estilo de las referencias, con la favorita ★. Ejemplos de lo que traduce: rapidez → estela de neón que acelera; siempre/vitalicio → lazo infinito con un punto que lo recorre; confianza → anillos que se cierran sobre un núcleo; gratis → «$0» gigante tachado; equipo → personas que se encienden una a una; caos → orden → formas dispersas que se alinean. Cada idea trae su texto explicando la animación abstracta y las palabras que la dispararon. Reglas de variación: la luz (aurora) y la composición cambian entre tomas y no se repite la misma idea dos tomas seguidas; el color sale por significado (Gurú se detecta en la frase).
- **Cómo se usa en el proceso (paso 9b):** al armar el storyboard corro `ideas.py` sobre el guion limpio y uso sus 2 mejores ideas como los 2 motion designs de cada toma (`--spec` las deja en el formato del storyboard); luego les sumo los planos. Es el **punto de partida, no el límite**: la favorita se revisa y, si una frase pide algo que el léxico no conoce, **compongo la escena a mano** con `escena()` y, si la idea se repite, la agrego a `CONCEPTOS` en `ideas.py` para que la próxima vez salga sola. Guion de ejemplo: `motion/guion_ejemplo.txt`.
- **Lienzo de elementos UI** (`python estudio-video/motion/lienzo.py`): una sola página, `D:\OneScreen\Contenido\2026\10. Octubre\_referencias_motion\lienzo_elementos.html`, con todos los elementos del vocabulario (fondos, tipografía, contenedores, UI, gráficas, formas y abstractos), cada uno en los tres colores de significado y con el código para usarlo. Cada elemento nuevo se agrega a `DEMOS` de `lienzo.py` y el lienzo se regenera.
- **Elementos abstractos nuevos** en `elementos.py`: `particulas` (caos/orden), `onda`, `arco`, `infinito`, `desorden` (caos/orden) y `escalera`.

## Plantillas de motion (biblioteca única, v3 del 28-oct)
Cris: «te tocará hacer un motion por plano; para que no sea pesado, que sea de plantillas». **Las plantillas son ejemplos de composición, no el límite** (ver «Sistema de diseño de motion») (`motion/plantillas.py`): yo elijo la plantilla según el **tipo de frase** y relleno los textos; el pantallazo del storyboard y la indicación de movimiento salen solos (`{"tipo": "motion", "plantilla": "cifra", "params": {"valor": "+20", "etiqueta": "idiomas", "tema": "explicar"}}`). Cada plantilla tiene dos caras con los mismos parámetros: **boceto** (listo, 37 plantillas registradas en `PLANTILLAS`; el conteo manda el código) y **build** para HyperFrames (se implementa la primera vez que Cris elige esa plantilla, reutilizando `videos/onescreen-inta/gfx_inta.py` y `estilo-onescreen/motion/fx.js`; luego queda en la biblioteca).

**Lenguaje visual (v3).** La v1 «se sentía torpe, vieja, de PowerPoint» (Cris). Ahora mezcla dos fuentes reales:
1. **Lettering de Apple**, medido en fotogramas del video «Apple Event 2018 in 108 seconds» (referencias en `D:\OneScreen\Contenido\2026\10. Octubre\_referencias_motion\apple\sheets\`): **una frase corta por beat (1-3 palabras)**, tamaño medio con mucho aire, bold de tracking cerrado, las palabras entran una a una; fondos que alternan; **el nombre de la función lleva el texto con degradado** (Super Retina cálido, Liquid Retina azul-violeta); el texto se monta sobre la imagen del producto. Tamaño gigante solo para una palabra de impacto («big.», «That?»).
2. **El estilo propio que mostró Cris** (cotización de Gurú y Academy): **degradados profundos + textura** (puntos o rejilla fina), **tarjetas de vidrio** (relleno translúcido y borde fino), íconos de línea, título grande y texto de apoyo atenuado. Esto **reemplaza** la antigua prohibición de degradados y los fondos planos de `05_MOTION.md`.

**Color por significado (Cris, 28-oct):** `tema: "gurú"` = **verde, solo cuando se habla de Gurú**; `tema: "solucion"` = **azul, cuando hablamos de la solución**; `tema: "explicar"` = **blanco, cuando exponemos o enseñamos algo** (datos, procesos, comparaciones). (`oscuro` existe pero no se usa salvo que Cris lo pida.) **Prohibido** el rótulo pequeño en MAYÚSCULA tipo título de diapositiva («CAPA 3 · SOPORTE», «ANTES»); un título opcional es una frase normal, en negrita.

| Plantilla | Para qué frase | Parámetros (+ `tema`) |
|---|---|---|
| `frase` | **lettering Apple**: 1-3 palabras, palabra clave con degradado | `texto`, `clave` |
| `titular` | idea corta de 2 líneas, grande | `l1`, `l2` (con degradado) |
| `cifra` / `keynote` | un dato que impacta («+20 idiomas», «24/7») | `valor`, `etiqueta` |
| `flujo` | proceso A → B → C en tarjetas de vidrio con ícono | `nodos` (2-4), `iconos`, `titulo` |
| `comparacion` | antes/después, sin/con (mitades a sangre) | `izq`, `der` |
| `tarjetas` | tres ventajas en vidrio con ícono | `items` [{icono, titulo, texto}], `titulo` |
| `panel4` | **como la cotización**: texto a la izquierda + 4 tarjetas de vidrio | `titulo`, `subtitulo`, `texto`, `tarjetas` (4), `cabecera` |
| `tachado` | algo que se elimina («nadie arma el acta») | `texto`, `tachado` |
| `pantalla` | una plataforma genérica (nunca captura falsa de terceros) | `titulo`, `lineas` (≤4) |
| `checklist` | beneficios que se marcan | `items` (2-5), `titulo` |
| `cta` | cierre con llamado a la acción | `texto`, `sub` |
| `barras` | data story: un gráfico, una anotación | `valores`, `etiquetas`, `nota`, `titulo` |
| `linea` | una sola línea que recorre 3-4 ideas | `puntos`, `titulo` |
| `isometrico` | mini-mundo isométrico con etiquetas | `items` (2-3), `titulo` |
| `notificacion` | un aviso o mensaje que llega («un ingeniero ya está disponible») con pila de capas detrás | `titulo`, `texto`, `hora`, `icono` |
| `curva` | crecimiento/tendencia: gráfica de área con degradado, puntos con halo y burbuja de valor | `valores` (5-8), `titulo`, `etiqueta`, `marca` |
| `orbitas` | anillos finos con íconos en discos que giran alrededor del texto | `lineas` (2), `iconos` |
| `chips` | «todas las herramientas»: chips con ícono flotando alrededor de un título sobre anillos suaves | `centro` (2), `items` [{icono, texto}] (3-5) |
| `ruta` | un día / una secuencia: contenedor con borde de degradado que brilla y filas «etiqueta → resultado» (rectángulos de esquinas suaves) | `l1`, `l2`, `filas` (3) |
| `pregunta` | pregunta cinética con tamaños mezclados, insignia, opciones SÍ/NO en rectángulos de esquinas suaves y flechas que se dibujan | `l1`, `clave`, `l3`, `opciones`, `respuesta` |
| `tarjeta_plano` | tarjeta de color con el PLANO rompiendo el borde y el título detrás; CTA con flecha | `l1`, `l2`, `texto`, `cta` |

Íconos de línea disponibles: persona, grupo, pantalla, doc, chat, check, globo, auriculares, toque.

**Ideas de motion tomadas de las referencias de Cris (28-oct; imágenes en `D:\OneScreen\Contenido\2026\10. Octubre\_referencias_motion\ideas\`). Se toman las IDEAS de diseño; los colores y las tipografías de OneScreen NO cambian:**
- **El fondo jamás es estático.** Siempre algún movimiento, así sea sutil: la **aurora** (manchas de luz suaves que suben desde un borde) respira y deriva en ciclos de 8-12 s, el grano parpadea apenas y la rejilla o los puntos se mueven en parallax. Cada plantilla lo dice en su indicación de movimiento («FONDO VIVO»).
- **Los contenedores brillan:** las tarjetas de vidrio llevan un **halo difuso** del color de acento detrás y un **borde con luz** (blanco arriba-izquierda que se apaga en diagonal); en el motion, un barrido de luz las cruza al entrar.
- **Marcador sobre la frase clave** (`resalta`): un marcador de color de esquinas suaves (no cápsula) que se dibuja detrás de la palabra y brilla, con un **número «fantasma» gigante en contorno** detrás (`fantasma`).
- **Órbita fina con destello de 4 puntas** alrededor de una frase (`orbita`); **indicador de progreso** de beats (`paso: "2/4"`, el punto activo se alarga).
- **Degradado vertical dentro de la tipografía** (blanco que se desvanece) para titulares grandes; **grano fino** sobre el degradado; **aurora de color** que sube desde abajo.
- **Elementos que rompen el contenedor** (un sujeto o plano que sobresale del borde de la tarjeta), **cursor que hace clic** sobre un botón y **notificaciones flotantes** para escenas de producto.
- **Segundo lote de referencias (28-oct; `ideas\8-16`):** **pila de capas translúcidas** detrás de una tarjeta (`notificacion`); **gráfica de área con degradado**, puntos con halo y burbujas de valor flotantes (`curva`); (las «palabras en píldoras» de esta referencia se retiraron: píldoras prohibidas); **anillos finos concéntricos** con íconos en discos que orbitan (`orbitas`) y **chips flotantes** sobre anillos suaves (`chips`); **contenedor con borde de degradado que brilla** y filas con flecha (`ruta`); **pregunta cinética** con tamaños mezclados, insignia circular, opciones SÍ/NO y **flechas con esquinas redondeadas que se dibujan por la pantalla** (`pregunta`); **sujeto/plano que rompe el borde de la tarjeta** con el título detrás, y **palabra gigante translúcida con halo detrás del objeto** (`tarjeta_plano`, `fantasma`).
- **Barra de degradado (no cápsula)** y **contornos concéntricos** (topográficos) detrás del título: pendientes de plantilla.

**Biblioteca por referencias (regla de Cris, 28-oct): «cada idea que te he mandado es una referencia de diseño y la guardas como plantilla; con eso siempre tendrás de dónde escoger». NUNCA se reemplaza una plantilla anterior por una nueva:** cada referencia nueva = una plantilla nueva (con su nombre propio) en `motion/plantillas_ref.py`, donde `REFERENCIAS` dice de qué imagen o video sale y `EJEMPLOS` trae parámetros de muestra. El **catálogo visual** (referencia a la izquierda, nuestra plantilla a la derecha, con su indicación de movimiento) se genera con `python estudio-video/motion/catalogo.py` y queda en `D:\OneScreen\Contenido\2026\10. Octubre\_referencias_motion\catalogo.html`; sirve para escoger («la de la referencia 14» = `pregunta`). Al recibir referencias: (1) copiar la imagen a `_referencias_motion\ideas\`, (2) crear su plantilla (o, si de verdad es la misma idea, apuntarla en `REFERENCIAS` a la existente y decirlo), (3) agregarla a `EJEMPLOS`, (4) regenerar el catálogo. Las ideas que se repiten en varias referencias pueden además quedar como decoración (`resalta`, `orbita`, `fantasma`, `paso`), pero **sin quitar la plantilla de cada una**.

**Calidad de las plantillas (corrección de Cris, 28-oct):** (1) **nada se sobrepone**: antes de entregar un storyboard se pasa el revisor de armado (`boceto.revisar`, que catalogo.py ejecuta y avisa de textos que se pisan o salen del lienzo) y se mira el pantallazo; (2) **jamás se copia el contenido de la referencia** (un objeto, logo, texto o ilustración suyos, como el estetoscopio): de la referencia se toma solo la idea de diseño y el contenido es un marcador neutro («tu plano aquí») o el nuestro; (3) **patrones de puntos y de rejilla muy sutiles** (apenas perceptibles: puntos 1 px a ~9 % de opacidad, rejilla de 1 px a ~4 %).

Plantillas por referencia añadidas el 28-oct (hoy 37 en total, tras retirar `hub` y `palabras`; también `curvas_tarjetas` [ref. 20], `dashboard_flotante` [ref. 21] e `infografia_paneles` [ref. 22], el estilo «flat vector explainer»): `escritura` y `formas_flotantes` y `ui_burbujas` (ref. «Imagine»), `puntos_halo` (paletas Jade/Arctic), `escala_degradada` («Starry Night»), `frase_orbita` («Creative success»), `cita_tarjeta` (tarjeta con pestañas), `editorial_rejilla` (póster de rejilla), `tarjetas_ilustradas` («Utilidades clínicas»), `palabra_halo` («día mundial da saúde»), `linea_neon` («When a Brand Stops Evolving»), `esfera_suave` («Zen Space»).

**Reglas de uso:** (1) los 2 motion designs de cada toma están **compuestos por mí con el vocabulario** (puede apoyarse en una plantilla, pero no se limita a ella); (2) **no repetir la misma plantilla en tomas seguidas** (diagramación distinta por escena, §2); (3) si ninguna plantilla encaja con la frase, propongo una **plantilla nueva** (se agrega a `motion/plantillas.py` y a esta tabla) en vez de improvisar un motion suelto; (4) cuando Cris aprueba un motion especialmente bueno, se ajusta o se crea la plantilla; (5) para subir el nivel, antes de crear una plantilla nueva se mira una referencia real (Apple, lanzamientos de producto) y se guarda un fotograma en `_referencias_motion`.

## REGLAS de estilo y producción

Reglas dichas o confirmadas por Cris (fecha y video entre paréntesis). Se citan como «§N».

### §1. Texto y subtítulos
- **Palabras sueltas flotando sobre el plano: NO (Cris, 28-oct, INTA36.0002): «los textos sobre video no deben quedar así sueltos».** El estilo de `Beneficios en educación_V1` (Rubik extra-bold blanca a media altura, una palabra a la vez) solo vale como referencia de tipografía y entrada; no se repite ese montaje sobre plano hasta aclarar con Cris cómo quiere anclar el texto (sin cajas ni píldoras). Mientras tanto: frases cortas completas (no palabra a palabra acumulada) o escena de color. Las piezas INTA con `pal(...)` en `specs.py` están pendientes de rehacer. Para énfasis, tarjeta blanca con texto azul alineado a la izquierda (línea ligera + línea en negrita).
- **Texto directamente sobre el plano** (frase corta completa, ver arriba), mezclando Rubik bold y light en blanco. **Nunca en contenedores, cuadros ni píldoras** sobre el plano (23-oct, Rental).
- Fondo blanco solo para enfatizar una línea corta (azul, pesos mixtos).
- **Subtítulos:** Rubik 500 blanco con trazo negro duro y muy fino. 16:9 y 1:1: dos líneas abajo. 9:16: 1-3 palabras a media altura. **No se ponen** cuando un gráfico o un texto ya lo dice.
- "OneScreen" siempre con el **logo oficial** (4 colores); títulos Rubik, cuerpo Manrope (en proyectos HyperFrames de hoy solo está cargada Rubik: cargar Manrope si se usa). Slogan con "el espacio" y "el futuro" en bold.
- **Entrada del lettering:** cada palabra sube de abajo hacia arriba con transparencia, suave (≥1 s, `power3.out`). Nada de giros ni estiradas que "parecen PowerPoint" (23-oct).

### §2. Motion graphics
- **PROHIBIDO (Cris, 28-oct): las píldoras y las redes de nodos.** **Píldora** = cualquier forma de cápsula (rectángulo con las esquinas redondeadas al máximo): botones, etiquetas, burbujas, barras, filas, toggles, cápsulas de progreso o de degradado. Se usan rectángulos de **esquinas suaves de 8-16 px** (`boton`, `burbuja`). **Red** = nodos unidos por líneas (grafos, «hub» con satélites, redes de equipo o de conexión). Para equipo se usan **personas que se encienden**, para conexión **una señal que viaja entre dos íconos**. El revisor (`boceto.revisar`) marca cada píldora como «píldora prohibida» y `elementos.py` ya no trae `pildora` ni `red`; las plantillas `palabras` (píldoras) y `hub` (red) se retiraron del código y de la tabla.
- **Sin barrido de entrada (Cris, 28-oct, INTA20-22): «no me gustan las transiciones».** El motion entra por corte directo, sin el telón que se abre; solo animan los elementos dentro de la toma.
- Deben **representar lo que dice la voz** (nodos, flujos, paquetes de luz, barras, colas, órbitas), sincronizados con la palabra. **No un ícono animado.**
- **Variar el diseño y la diagramación** de una escena a otra. Prohibido el patrón "título grande a la izquierda y gráfico a la derecha" repetido. Inspiración: lettering de Apple, juego de motion design y **cámara 3D** (perspective, z, giros suaves). (23-oct)
- Trazo grueso: ~7 % del tamaño del ícono (como Flota de IA). **Brillo (28-oct, reemplaza «sin brillo»):** el halo difuso y el borde de luz van en los contenedores de vidrio y en la aurora del fondo (sección «Sistema de diseño de motion»); los trazos de gráficos e íconos siguen limpios, sin sombra difusa propia.
- Pueden ir sobre **fondos blancos o de color, variados**. Balance: ni todo motion ni todo texto encima del plano; mezclar plano con texto, escenas de color y plano limpio.
- Las **tarjetas de ventajas** (plano arriba + mini-diagrama + título + subtítulo) le encantan; en escenas con fondo sí van tarjetas, sobre plano no.
- Paleta: blanco, azul #3976ff, negro #1a1a1a; acento #7d00ba; **verde solo cuando se habla de Gurú** (color por significado, 28-oct). Los fondos son degradados profundos del color del significado (verde Gurú / azul solución / blanco explicar), con aurora y grano. **Nada de amarillo ni fondos navy.** Estilo de referencia: Flota de IA ("Apple") + las referencias de la sección de motion.

### §3. Márgenes y zonas seguras
- Aire real a los lados: no dejar nada al límite (23-oct). Valores actuales del Rental v3 (px): 16:9 lados 270, arriba 150, abajo 170; 9:16 lados 150, arriba 340, abajo 550; 4:5 lados 150, arriba 210, abajo 310.
- Texto, logos y botones dentro de la caja; el video puede sangrar. Las zonas también guían el encuadre (rostro, QR, pantalla).
- Revisar que **ningún gráfico pise un texto**: en 16:9 y, con fotogramas fijos, en 9:16 y 4:5, antes de renderizar el preview.

### §4. Planos
- **Solo planos grabados desde 2024** (columna "Fecha de grabación" del Directorio; sin fecha tampoco): los de antes muestran excolaboradores que hoy trabajan en la competencia. Filtro duro en `videos/onescreen-inta/seleccion.py` (`base_ok`); aplicarlo en cualquier selector nuevo (Cris, 27-oct-2026).
- Vetados: 103182 (hombre de barba con camisa OneScreen, no debe salir) y 103512 (grupo sentado). Ver memoria/voz_y_planos_prohibidos_videos.md (25-oct).
- **El plano debe coincidir con lo que dice la voz y se verifica mirándolo (Cris, 28-oct, INTA36):** si se nombra Gurú, plano con Gurú en pantalla; si se nombran ingenieros o soporte, plano de equipos de soporte; antes de montar se ve una tira de fotogramas de cada plano contra su frase. Si el Directorio no tiene un plano que lo ilustre, se dice en vez de rellenar con una pantalla genérica. **Lo literal se ve literal:** si la voz dice «botón verde Gurú», el plano muestra ese botón, no solo Gurú en pantalla. **Ningún plano suelto sin relación con la frase** (INTA36.0002 trajo una mano golpeando de <1 s que no tenía nada que ver: violaba también el mínimo de 1,5 s; revisar cada tira completa, incluidos los planos de transición).
- **Solo clips crudos de cámara:** sin planos de IA, sin pedazos de videos ya editados, exportaciones, pauta o música, sin personas hablando como apoyo, y sin instalación/montaje de pantalla salvo que la voz lo diga; en casos de éxito, solo planos del caso (27-oct, INTA).
- **EVALUAR LOS PLANOS MIRÁNDOLOS, SIN REPETIR Y SIN TOMAS FALSAS (Cris, 28-oct; prueba de 3 videos a la vez en la que se repetía la mitad de los planos y entraban planos de gente tomándose fotos y riéndose que no servían):** traer filas del Directorio **no es elegir planos**, es solo obtener candidatos.
  1. **Mirar antes de ofrecer.** De cada candidato saco una tira de 3-5 fotogramas del tramo y la **miro**, y la comparo con la frase. Si hay duda, Gemini lee el clip. **No se ofrece ningún plano que no se haya visto**, y en la `nota` del SPEC dejo por qué sirve.
  2. **Prueba de relevancia:** cada plano debe poder responder en una línea «¿qué parte de la frase ilustra?». Si no se puede decir, se descarta (que parezca de la categoría no basta).
  3. **Tomas falsas = rechazadas:** planos posados o de stock que no ilustran nada: **gente riéndose a cámara, tomándose fotos o selfies, grupos posando, apretones de manos, brindis, aplausos sin contexto, gente mirando a cámara sonriendo, «gente feliz» genérica**. Solo entran si la frase habla literalmente de eso. También se descartan planos mal enfocados, con movimiento de cámara en el tramo, o donde lo importante no es legible.
  4. **Nada de repetir planos:** ni dentro de un video ni **entre los videos de un mismo lote** (cuando Cris pide varios videos a la vez). Llevo una lista de planos ya usados por el lote y cada video elige de lo que queda; prefiero los de menos usos (col. Y del Directorio). Si no alcanzan planos buenos y distintos, **lo digo y cubro esa toma con motion** en vez de repetir o rellenar con planos malos. Antes de entregar verifico que la intersección de planos entre los videos del lote sea cero (`storyboard.py` lo avisa).
  5. **Pool amplio:** traigo al menos 3 veces los candidatos necesarios por toma para poder descartar sin quedarme corto.
- **Jamás una foto fija como plano.** Si solo hay foto, animarla con Veo 3.1 (Google AI Studio) o generar un plano nuevo.
- **No usar mouse en apps táctiles.** El apoyo ilustra literalmente lo que se nombra.
- Planos S-Log3 (28-oct, reemplaza el flujo de color-antes-de-montar): el **preview 720p se arma primero**; tras aprobarlo se crea el `.prproj` con los clips: **si el plano ya tenía color, el color va en el archivo; si no, queda normal y Cris lo colorea**, exporta en alta calidad y de ese export sale el final 16:9 en 4K (el corte coloreado se registra en la col. AB del Directorio). Nada de conversión neutra inventada ni de hornear planos neutros dentro de gráficos. El .cube de Lumetri no sirve fuera de Premiere. Para colorear con el pipeline propio: skill `colorear-plano`.
- Un plano "ya coloreado" es el que lleva Lumetri en su clip dentro del prproj (cadena `ComponentOwner/Components`); el "Sí" de la col. Z no basta.
- **Plano dentro de una tarjeta o gráfico animado:** va horneado en la capa de gráficos (sigue el 3D de la tarjeta) y congela el último cuadro si el plano es más corto que la escena; en 9:16 y 4:5 la foto sale del plano completo en horizontal, no del recorte vertical (en vertical la ventana es una tira ancha: dejarla alta, ≥130 px).

- **CTA final sobre plano (Cris, 28-oct, INTA35/36):** nada de tarjeta final suelta; el CTA va como texto sobre un plano (con la intro de marca al final).
- **Plataformas y procesos no filmables (Cris, 28-oct, INTA35):** pantallazos o interfaz recreada y animada (p. ej. Academy) y motion graphic para procesos (un certificado que se llena). **Gurú** = el botón verde de soporte; el chat/AI Bot de Gurú no sirve para ilustrarlo.

### §5. Edición
- Cortes, entradas de apoyo, zooms y gráficos caen **2-3 cuadros antes de la palabra**. No cortar al compás de la música.
- **Ningún plano dura menos de 1,5 s**, ni de motion ni de video (28-oct). Cortes dinámicos entre 1,5 y ~2,5 s: usar muchos planos, no sostener uno mientras la voz avanza (25-oct, corporativo; la regla anterior de 1,2 s promedio queda reemplazada).
- Zigzag de escala: salto fijo 100 % / cerrado. Apoyo 25-50 % del video, ~1,7 s, literal. SFX 75 ms antes del evento.
- La voz manda: cada gráfico nace en el timestamp de la palabra que lo nombra.

### §6. Audio
- **Voz en off: UNA sola receta, siempre (Cris aprobó «exp_d» en INTA37; 28-oct: «siempre voz nueva, prohíbete los otros ajustes, qué pérdida de tiempo»).** Prohibido usar `eleven_v3`, Hale directo, stability/style/speed distintos, `TEMPO` en el post o cualquier ajuste anterior; tampoco se perfilan ni se comparan variantes.
  1. **Toma fuente (Text to Speech):** voz Cristian Sánchez `o2vbTbO3g4GrKUg7rehy`, **eleven_v4**, `language_code` `es` (`es-CO` no existe), speed **1,12**, style **0,6**, stability **0,45**, `use_speaker_boost` true, mp3 44,1 kHz 192 kbps.
  2. **Guion dirigido ENÉRGICO:** etiquetas en inglés entre corchetes (`fast-paced`, `emphatic`, `rapid-fire`, `upbeat`, `short pause`…), MAYÚSCULA solo en la palabra de énfasis, cifras y siglas como se pronuncian; sin cambiar ni una palabra del guion. Archivo `Voz\guion_dirigido_v3.txt` (y `guion_limpio.txt` sin etiquetas).
  3. **Voz a voz a Hale:** destino `wWWn96OtTHu1sn8SRGEr`, `eleven_multilingual_sts_v2`, stability **0,2**, similarity_boost **0,7**, style **0,7**.
  4. **Sin acelerar ni validar con Gemini.** Solo se recortan silencios >0,22 s (umbral -38 dB) a pausas de 0,14 s, WAV mono 48 kHz, y Scribe (`scribe_v1`, `spa`) para los tiempos por palabra. Voz ≈ -18 LUFS en la mezcla.
  5. **Se entrega a Cris para que la escuche antes de montar**; la aprobada se congela en `Voz\aprobada\` y no se regenera.
- **Texto de dirección optimizado para ElevenLabs (26-oct).** La narración nunca se manda como texto plano; cada frase lleva dirección escrita para el modelo:
  1. **Etiquetas de interpretación entre corchetes** antes de la frase o del tramo, en inglés (es lo que el modelo entiende): `[warm]`, `[confident]`, `[excited]`, `[softly]`, `[short pause]`, `[emphasis]`. Probar con una toma corta qué etiquetas respeta `eleven_v4` antes de usarlas en todo el guion.
  2. **Puntuación como ritmo:** coma y punto = pausa, puntos suspensivos = suspenso, raya = quiebre; MAYÚSCULA solo en la palabra de énfasis. Frases cortas, una idea por frase.
  3. **Cifras, siglas y marcas escritas como se pronuncian.**
  4. **Un arco emocional por pieza** (gancho enérgico, desarrollo cálido, cierre seguro), anotado en el guion de dirección.
  5. **Dos guiones:** `guion_dirigido.txt` (con etiquetas; es lo que se envía a ElevenLabs) y `guion_limpio.txt` (sin etiquetas; para subtítulos y para los tiempos por palabra con Scribe).
  6. Varias tomas; medir la expresividad (rango de F0) contra una toma plana y escoger.
- **La voz aprobada no se regenera (27-oct):** cuando Cris dice que la voz/acento está bien, la toma se congela (`Voz\aprobada\`). Corregir CTA, gráficos, planos o música se hace sobre ese audio; solo se genera voz nueva si Cris lo pide o, tras preguntarle en una línea, lo autoriza.
- **Una canción distinta por pieza**, con su punto de giro justo al terminar el hook (27-oct, INTA; en INTA sin SFX).
- Voz ≈ -18 LUFS; música + SFX ≈ -24 LUFS (~6 LU por debajo). Música de percusión ≥160 BPM, energía constante. SFX discretos (volumen 0,13-0,23), afinados en la tonalidad de la música (Fashion: sol menor).
- Música y SFX por ElevenLabs o los masters de Cris (`Mezcla de música\Masterizadas`). No usar `carve.mjs`. Cris critica la música: analizar estructura y true peak antes de elegir; la marca de Premiere es la explosión tras una pausa.
- Intro de marca con su propio sonido.

### §7. Proceso
- **Una versión, aprobar, y luego** acentos, idiomas y formatos extra, en lote con `render_rental_variantes.sh` (cada uno con su ID).
- **Se entrega con link clicable** (`file:///D:/…`, espacios `%20`), nunca con "está en tal carpeta" (26-oct).
- Al aprobar, la fila se escribe en la **hoja de producción** y se relee; no basta el espejo local.
- Todo se entrega en 3 formatos: 16:9, 9:16, 4:5, **pero el preview es solo 16:9** y los otros formatos se renderizan después de aprobarlo. Proyecto de Premiere con V1 plano original, V2 gráficos con alfa, audio mezclado y el color tomado del Sheet.
- **Proceso obligatorio de 16 pasos:** los pasos de arriba, siempre en orden. **Dos puertas:** (1) **un solo preview 16:9 a 720p** para que Cris apruebe; (2) solo después el **.prproj** (color de los planos que ya lo tengan; el resto lo colorea Cris), su export de alta calidad y los formatos finales (28-oct).
- **Directorio maestro** (Sheet `1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w`): de ahí salen los planos. Columna AB = corte ya coloreado, Z = tiene color, AP = proyecto donde está el Lumetri, AQ/Y = dónde ya se usó. Un plano sin corte en AB entra al prproj de color del paso 4 (REGLAS §4).
- Honestidad: lo que no se pudo abrir o verificar (p. ej. el .prproj generado a mano) se dice.
- Cada corrección de Cris se registra en [CORRECCIONES.md](CORRECCIONES.md) y aquí en el mismo momento (la skill `video-onescreen` lo exige).

### §7b. Dónde se guarda todo (26-oct)
- **Nada se guarda en C:.** Todo lo de una pieza va en `D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\`, una **carpeta nueva por pieza** dentro del año y el mes (p. ej. `D:\OneScreen\Contenido\2026\10. Octubre\Corporativo\`). Dentro: `Exports\` (previews y exports), `Voz\`, `Audio\`, `Premiere\` y `Proyecto\` (composición HyperFrames y renders).
- TMP/TEMP, cachés (`--frames-cache-dir`) y renders intermedios también en D:. La única excepción es el código de los builders, que vive en el repo (`videos/<nombre>/`) porque va a git.

### §8. Registro, aprobación, IDs y nombres de archivo (26-oct; arquitectura v2)
- Todo video exportado queda en la **hoja "Directorio - Producción de video"** (`1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks`, fuente de verdad; ver [registro/HOJA.md](registro/HOJA.md)) y en su espejo [registro/](registro/LEEME.md). **Cuatro pestañas, cuatro dueños:** Guiones (estrategia; yo solo Estado y Versiones generadas), Producción (mía), Planner (script del planner; yo no escribo), Histórico (yo, al cerrar). Variaciones, Publicaciones, Resultados, Convenciones y README quedaron archivadas y ocultas: no se escriben.
- **No se produce sin guion aprobado:** solo desde una fila de Guiones con Estado = Aprobado y Decisión de Cris = Aprobado (hooks de `Hooks aprobados`). Sin texto o ambiguo: no inventar, avisar. Hook tipo Dato con cifra sin fuente: no producir, avisar. Dos aprobaciones independientes (guion y video); un guion aprobado no habilita publicar.
- Un cambio = **un ID nuevo** (`<PIEZA>.<NNNN>`, la pieza es el ID de ángulo, p. ej. `INTA03.0001`); nunca se reutiliza ni se sobrescribe un ID entregado. **El ID va en el nombre del archivo, nunca impreso en el video:** `<ID>_<H#C#A#>_<voz>_<formato>[_preview].<ext>`. Exports en `…\<Mes>\<Pieza>\Exports\`.
- **Aprobación:** los previews NO van a Drive (se envían por el chat); los exports aprobados, sin `_preview`, van a la carpeta de Drive "Producción de video" (`1cda9LOGC2Yb_wli88bNpmJ0BRFqOnmDm`), una subcarpeta por pieza; Cris decide en "Decisión de Cris" (columnas amarillas). Solo con *Aprobada* se pasa el Estado, se marcan los usos en el Directorio de planos y se crea el .prproj. **No creo filas de publicación:** el planner las crea solo a partir de lo Aprobada o Vigente. Solo se publica lo Aprobado o Vigente.
- **Directorio maestro de planos:** al aprobar, cada plano usado suma 1 a "# de usos" (col. Y) y recibe una línea en "Usado en" (col. AQ); la fecha queda en Producción (col. T) para no sumar dos veces.
- **Cierre:** una versión pasa a Histórico si queda Reemplazada/Rechazada/Archivada o si todas sus filas del Planner están Cerrada/Retirada (copiar, verificar, borrar; métricas a 72 h sumadas). Las columnas Usado, Usado en dónde y Fecha de uso están en desuso. Pauta de Colombia: la gestiona BigSEO; yo solo dejo creativos listos.
- Sin afirmar nada que no se haya verificado (la hoja dice lo que se anotó). La publicación la hace el planner; los archivos necesitan link de Drive.
- **Aprobación en las dos vías (26-oct):** si Cris marca Aprobada en la hoja, la sesión lo lee al empezar y ejecuta lo que sigue; si lo aprueba en la sesión, Claude lo escribe en la hoja por él (Estado, Decisión, Comentarios, Fecha). Ver `registro/HOJA.md`.

## Directorio maestro de planos (Google Sheet)
- Sheet `1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w` (pestañas **Directorio**, **Segmentos**, **Assets**, **LÉEME**). Lee con el conector de Google Sheets (`get_values`): `'Directorio'!A1:AQ`, `'Segmentos'!A1:O`, `'Assets'!A1:N`. La hoja está en es_CO (decimales con coma). Lee primero la pestaña LÉEME: es la guía viva para agentes.
- Una fila = un archivo único. Para **elegir planos**: filtra por Producto, Software en pantalla, Categoría, Lugar, Personas, Acciones / palabras clave (apoyo literal a lo que dice la voz), Calidad ≥ 4, Permisos y Vigencia vigentes, Apto vertical; usa **Segmentos** para el tramo exacto (Inicio/Fin en s) y la columna *Mejor momento*.
- **Color y uso:** columna **Z Color** (Sí = tiene Lumetri en algún proyecto), **AP Ruta de color (prproj)** = proyectos donde el plano tiene Lumetri (más reciente primero), **AQ Usado en (prproj)** y **Y # de usos**. **AM Ruta en disco** (primera línea = principal) y **AN Link de Drive**. **AA Perfil de color** (user9 = S-Log3).
- **AB Archivo graduado** = el corte ya coloreado por Cris (flujo vigente): antes de pedir color de un plano, mira si ya tiene corte en AB. Un plano "tiene color" solo si su clip lleva Lumetri dentro del prproj (el "Sí" de Z no basta). Los planos de AP sin AB sirven de punto de partida (`PLANOS=1 build_prproj.py` clona ese Lumetri). No inventes color.
- Solo planos con "Fecha de grabación" ≥ 2024 (sin fecha tampoco); vetados 103182 y 103512 (CLAUDE.md §4).
- El análisis automático con Gemini que llena las columnas amarillas vive en `directorio-video/` (README propio); si faltan datos de un plano, ahí se completan.
- Solo lectura por defecto. No escribas en el Sheet sin pedir permiso a Cris. **Única excepción permanente (H.5):** al aprobar un video se suman los usos en las columnas Y y AQ; nada más.
- Un plano que ya fue usado (AQ) se puede reutilizar, pero avisa a Cris cuándo y en qué video aparece.

## Hoja de producción v2: guiones → producción → planner → histórico (obligatorio)
**Fuente de verdad: la hoja "Directorio - Producción de video"** (Google Sheet `1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks`; columnas y flujo en `estudio-video/registro/HOJA.md`). `sheetId`: **Guiones 3001 · Producción 2001 · Planner 3002 · Histórico 3003** (archivadas y ocultas, no se escriben: Variaciones 2002, Publicaciones 1002, Resultados 2003, Convenciones 1003, README 1004; usa siempre `sheetId` en llamadas de formato). Espejo local: `registro/guiones.csv`, `produccion.csv`, `planner.csv`, `historico.csv`, `manifest.json` (los viejos, en `registro/legacy/`). Si la hoja y el espejo difieren, manda la hoja.

### H.1 Quién escribe qué
| Pestaña | Escribe | Cris (amarillas) | Yo |
|---|---|---|---|
| **Guiones** | skill de estrategia | Decisión de Cris, Hooks aprobados, Comentarios de Cris, Fecha de decisión | solo `Estado` y `Versiones generadas (IDs)` (y `Estado = Cerrado` al cerrar todo) |
| **Producción** | yo (todo menos amarillas) | Decisión de Cris, Comentarios de Cris, Fecha de decisión | todo lo demás |
| **Planner** | script del planner | Qué vimos, Decisión, Próxima variación a probar | **solo leo** (para cerrar versiones) |
| **Histórico** | yo, al cerrar | Aprendizaje (Cris) | la fila completa |

Las amarillas son de Cris: las leo, **nunca** las escribo. Única excepción: si Cris aprueba **dentro de la sesión**, escribo por él Estado, Decisión de Cris, Comentarios ("aprobado en la sesión") y Fecha (permiso explícito del 26-oct-2026) con `registro.py celdas ID --fila N --campos estado,decision_cris,comentarios_cris,fecha_decision`, y releo la fila.

### H.2 Al empezar la sesión
Lee Guiones (filas `Aprobado`), Producción (decisiones nuevas de Cris) y Planner (filas `Cerrada` o `Retirada`): guarda cada `get_values` en JSON y trae las diferencias con `registro.py importar guiones|produccion|planner|historico ARCHIVO.json`, que imprime las **ACCIONES**. La fila se ubica por ID en la columna A, nunca por posición fija. Si hay conflicto manda lo que Cris acaba de decidir. `registro.py pendientes` resume lo que espera.

### H.3 Dos aprobaciones, independientes
`GUIONES` (Cris aprueba el guion) → `PRODUCCIÓN` (Preview → Cris aprueba el video → Aprobada) → `PLANNER` (publica y mide a 24/48/72 h; lee solo Aprobada o Vigente) → `HISTÓRICO`. Un guion aprobado **no** habilita publicar nada.

### H.4 De guion aprobado a versiones (`registro.py guion ID_ANGULO` imprime el plan)
Disparador: fila de Guiones con `Estado = Aprobado` **y** `Decisión de Cris = Aprobado`. Con `Con cambios` o `Rechazado`, no produzcas.
1. **Hooks:** los de `Hooks aprobados` (p. ej. `H1,H3`); si está vacío, los que tengan texto.
2. **Se copian:** `Pieza` = `ID ángulo`; `Nombre de la pieza` = `Ángulo (la idea)`; `Vertical` y `Nivel` tal cual (columnas AC y AD).
3. **Un ID nuevo por hook:** `<PIEZA>.<NNNN>`, siguiente secuencial. El primero es la **base** (`Eje que cambia` = `Base`, `Basada en` vacía); los demás `Eje = Hook` y `Basada en` = ID de la base.
4. **Códigos:** `Hook` = H1/H2/H3 según su columna; `Contenido` = C1 y `CTA` = A1, salvo variante que Cris pida de `Otras variantes (C2, A2…)`.
5. **Voz** `neutro` (acentos/idiomas = filas aparte, solo si Cris las pide). **Formatos** `16x9, 9x16, 4x5` salvo indicación (el **preview es solo 16x9**; los otros se generan tras la aprobación). **Estado** `Preview`, **Versión** `v1`.
6. **De vuelta en Guiones**, solo dos celdas: `Estado` = `En producción` y `Versiones generadas (IDs)`.
7. **El guion no trae dirección visual:** esa capa es mía. Si falta texto o algo es ambiguo, **no inventes**: no toques la fila y dile a Cris qué falta. **Hook tipo `Dato`** con cifra sin fuente: no lo produzcas y avisa.

### H.5 IDs, nombres y reglas que se conservan
- **ID único** `<PIEZA>.<NNNN>` (p. ej. `RENT.0006`, `INTA03.0001`), secuencial por pieza (código de 2 a 8 caracteres). Un cambio = un ID nuevo, por pequeño que sea; nunca se reutiliza ni sobrescribe. Todos los formatos de una versión lo comparten. **Va solo en el nombre del archivo, nunca impreso en el video.**
- **Nombre:** `<ID>_<H#C#A#>_<voz>_<formato>[_preview].<ext>` (`registro.py nombre`, `registro.py validar CARPETA`). Formatos 16x9 · 9x16 · 4x5 · 1x1. Voz: neutro · ec · mx · co · pt-br · en. Fechas aaaa-mm-dd. Exports en `D:\OneScreen\Contenido\<año>\<mes>\<Pieza>\Exports\`. (RENT.0007 a 0010 usan `ecuador`, `mexico`, `pt-BR`: no renombrar.)
- **Una variable a la vez** por prueba (`Eje que cambia`). **Versión** (v1, v2…) = iteración por correcciones de Cris, distinta del ID.
- **Estados de Producción:** Preview → Aprobada → Vigente (Reemplazada, Rechazada, Archivada). Solo se publica Aprobada o Vigente. Con `Decisión de Cris = Aprobada` pasas a Aprobada; sin ella no hay .prproj ni usos.
- **Previews NO van a Drive:** por el chat y en `Exports` con `_preview` (`registro.py preview ID --link "chat + ruta local"`). **Exports aprobados** (sin `_preview`) a la carpeta de Drive "Producción de video" (`1cda9LOGC2Yb_wli88bNpmJ0BRFqOnmDm`), subcarpeta por pieza, con el nombre `<ID>_<H#C#A#>_<voz>_<formato>.mp4`; su link a `Export en Drive (listo para subir)` (`registro.py ruta ID --drive LINK`). Sin link, el planner no inventa la ruta y avisa a Cris.
- **Al aprobar un video:** Estado = Aprobada, marcar usos en el Directorio de planos (abajo), fecha en la columna T, `.prproj`. **No creo filas "Pendiente" de publicación:** el planner las crea solo. **Ya no toco** `Usado`, `Usado en dónde` ni `Fecha de uso` (en desuso; el uso real vive en Planner e Histórico). No publico ni marco nada como publicado; nunca `Publicada` sin la URL real.
- **Directorio maestro de planos** (`1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w`, pestaña Directorio, col. A = ID): por cada ID de `Planos usados`, suma 1 a la col. **Y (# de usos)**, agrega a la col. **AQ (Usado en)** la línea `<ID de versión> <nombre de la pieza> (video)` y escribe la fecha en `Usos marcados en el Directorio` (`registro.py usos ID` dice qué hacer; `usos-hechos` marca la fecha). Si ya tiene fecha, no sumes de nuevo; un ID nuevo de la misma pieza con los mismos planos tampoco suma salvo que Cris lo pida. El escaneo del Directorio recalcula Y desde los .prproj: si se re-escanea, reaplica los usos desde Producción e Histórico. Verifica la fila por ID antes de escribir.

### H.6 Cierre: de Producción a Histórico
Sale de Producción cuando su Estado es `Reemplazada`, `Rechazada` o `Archivada`, o cuando **todas** sus filas en Planner están `Cerrada` o `Retirada` (`registro.py cierres`). Nunca se borra ni se renumera un ID: mover = copiar, verificar, borrar.
1. Una fila por versión en Histórico: `Estado final` = su Estado, o `Cerrada` si salió por Planner; `Fecha de cierre` = hoy.
2. **Métricas a 72 h:** suma Alcance, Vistas, Clics, Leads y Costo de sus publicaciones; retención = promedio ponderado por vistas; `Decisión` = la de Planner (si difieren, la de la publicación principal y el detalle en `Notas`). `registro.py cerrar ID` lo calcula.
3. Copia `Publicada en` (plataformas y URLs) y `Export en Drive`.
4. Verifica que el ID quedó en Histórico y recién entonces borra la fila de Producción (para RENT.0001 a RENT.0005, espera la confirmación de Cris).
5. Si todas las versiones de una pieza están en Histórico, `Estado = Cerrado` en su fila de Guiones (la otra escritura permitida ahí).
6. Tras cada escritura grande, verifica el número de filas.

### H.7 Qué no hacer
No escribir en Planner ni en columnas amarillas · no escribir en Guiones salvo `Estado` y `Versiones generadas (IDs)` · no producir desde un guion no `Aprobado` por Cris · no publicar ni marcar publicado · **pauta de Colombia (Meta y Google): la gestiona BigSEO**, solo dejo creativos listos · no inventar cifras, nombres de producto ni testimonios en guiones o textos en pantalla · no escribir llaves, contraseñas ni datos de clientes en la hoja · no tocar otras hojas salvo lo del Directorio de planos · no crear pestañas ni columnas sin que Cris lo pida (si hace falta una, al final y documentada en `HOJA.md`).
Al final de cada sesión de video: `registro.py manifest` y proponer commit/push (el otro entorno solo ve git).

## Actualización automática (obligatoria)
Cada vez que Cris **corrige, aprueba o rechaza** algo de un video:
1. Agrega una entrada con fecha, video, lo que dijo (casi textual) y la regla extraída a `CORRECCIONES.md` (historial).
2. Actualiza las Reglas (§1-§8 de este archivo) (edita la regla si ya existía; si choca con una anterior, la nueva gana y se borra la vieja).
3. Si cambia el proceso o una técnica, actualiza este archivo o `sistema-diseno/LEEME.md`.
4. Actualiza o crea la nota de memoria que corresponda y corre `python estudio-video/herramientas/sync_memoria.py` para que `estudio-video/memoria/` y la memoria de Claude Code queden iguales.
5. Díselo a Cris en una línea ("guardé la regla X"). Propón commit/push cuando termine la sesión (la nube solo ve lo que está en git); no lo hagas sin su OK.
Si estás en la nube, la memoria de Claude Code se pierde al cerrar: todo lo que importe va a `estudio-video/` y a git.

## Reglas que no se negocian
- Una sola versión hasta que Cris aprueba. Un solo preview 16:9 por pieza, obligatorio antes del .prproj, del color y de renderizar los otros formatos.
- Solo se produce desde un guion aprobado; la voz aprobada no se regenera; entrega con link clicable, nunca "está en tal carpeta".
- Nada de keys ni datos de clientes en archivos del repo.
- Antes de entregar el preview, revisa tiras de fotogramas del 16:9 (cruces texto/gráfico, márgenes, cortes malos) y fotogramas fijos de las escenas críticas en 9:16 y 4:5; los demás formatos se revisan cuando se renderizan, tras la aprobación. Checklist: sección de este archivo.
- **Nada en C:.** Todo va en `D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\` (carpeta nueva por pieza; CLAUDE.md §7b).
- D: se llena: limpia `D:\hf-render\tmp\fc*` y `rfc*` antes de renderizar.

## Checklist antes de entregar

- [ ] Se produjo desde un guion aprobado (Estado y Decisión = Aprobado en Guiones); una sola versión hasta la aprobación; **preview solo en 16:9** (los demás formatos, tras aprobar).
- [ ] ID de la versión solo en el nombre del archivo (`<ID>_<H#C#A#>_<voz>_<formato>[_preview]`), nunca impreso en el video.
- [ ] Planos grabados desde 2024, sin 103182 ni 103512, sin IA ni material ya editado.
- [ ] Si la voz ya estaba aprobada, es la misma toma (`Voz\aprobada\`); no se regeneró.
- [ ] Texto sobre plano sin cajas ni píldoras; subtítulos blancos con trazo negro fino y solo donde hacen falta.
- [ ] Ningún gráfico pisa un texto: en el preview 16:9 y, con fotogramas fijos, en 9:16 y 4:5 (mirar fotogramas de cada escena). Los fijos de 9:16/4:5 salen del builder con `FMT=9`/`FMT=45` y `npx hyperframes snapshot` en las escenas críticas: **fotogramas, no render de video**.
- [ ] Márgenes seguros reales; aire a los lados.
- [ ] Motion graphics que representan lo dicho; diagramación distinta entre escenas; entrada de palabras de abajo hacia arriba con transparencia.
- [ ] Trazos gruesos y limpios (el brillo solo en halos de vidrio y aurora); sin píldoras ni redes; paleta sin amarillo ni navy; logo oficial donde se nombra OneScreen.
- [ ] Sin fotos fijas como plano; sin mouse en apps táctiles.
- [ ] Storyboard con 5 opciones por toma (3 planos + 2 motion designs, y mi favorita), planos evaluados mirándolos y sin repetirse entre los videos del lote; enviado por Cris antes de ensamblar; el montaje coincide con lo que eligió y solo se construyeron los motion graphics elegidos.
- [ ] Ningún plano ni motion dura menos de 1,5 s; planos validados (sin movimientos de cámara, describen lo dicho).
- [ ] **Un solo preview** a 720p en 16:9 (nada más renderizado antes de la aprobación); el color de Cris entra después, en el .prproj; el corte coloreado queda registrado en la col. AB del Directorio.
- [ ] Música de la carpeta de masterizados, con el punto de giro al terminar el hook.
- [ ] Fotos dentro de tarjetas/gráficos: horneadas, con último cuadro congelado y encuadre visible en 9:16 y 4:5.
- [ ] Entrega con link clicable de cada archivo; fila escrita y releída en la hoja de producción.
- [ ] Mezcla: voz ≈ -18 LUFS, música+SFX ≈ -24; SFX discretos; intro de marca con sonido.
- [ ] Tiras de fotogramas del MP4 final revisadas (no solo `snapshot`); duración y audio con `ffprobe`.
- [ ] Narración generada desde el guion dirigido (etiquetas + puntuación de ritmo) y con expresividad medida frente a una toma plana.
- [ ] Todo guardado en `D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\` (carpeta nueva por pieza); nada en C:; disco D: con espacio.
- [ ] Decir con honestidad qué no se pudo verificar.

## Herramientas y trampas

Todas se ejecutan desde la raíz del repo. Nada de keys en archivos: variables de entorno (`ELEVENLABS_API_KEY`, `GOOGLE_AI_STUDIO`/`GEMINI_API_KEY`, …).

| Tarea | Herramienta | Notas |
|---|---|---|
| Armar la composición | `videos/onescreen-quizwiz-scrybe/build_rental3.py` (`FMT=16\|9\|45`, `ALPHA=0\|1`) | HyperFrames: HTML + GSAP pausado. `ALPHA=1` = solo la capa gráfica |
| Parches del estilo | `patch_r3a…r3e.py` en la misma carpeta | historial de cambios del Rental v3; copias `build_rental3.pre_*` |
| Cortar planos | `trims_rental3.py cut` / `formats` | historial del Rental v3 (fuentes sin colorear, conversión neutra solo para ver); **el flujo vigente usa los cortes coloreados** (`trims_rental3_color.py`, fila «Color») |
| Voz | `videos/onescreen-inta/voz_exp_d.py` (receta única de §6: eleven_v4 + voz a voz a Hale) con el **guion dirigido** (etiquetas + puntuación de ritmo, REGLAS §6); luego `voz_post.py` | `voz_exp_d.py` escribe en `Voz\vNNNN\` (número libre, busca la pieza en `D:\OneScreen\Contenido`, se niega si hay `Voz\aprobada\`); `voz_post.py` recorta silencios >0,22 s a 0,14 s, **sin tempo**, y saca los tiempos por palabra con Scribe (`scribe_v1`). Bloqueados (OBSOLETO): `voz_inta.py`, `voz_hale_directa.py`, `voz_v4_dirigida.py`; `bajar_voz.py` y `voz_gen.py` del Rental no se usan |
| Mezcla | `mix_rental.py SALIDA.wav [VOZ.wav]` | lee `plan.json` del proyecto; música MASTER_Fashion, SFX afinados |
| Post | `post_rental.py FMT raw.mp4 salida.mp4` | aberración leve + intro de marca + audio |
| Instalar la skill en otro entorno | `instalar_skill.py` (`--usuario` para ~/.claude/skills) | crea el cargador `.claude/skills/video-onescreen/SKILL.md`, que remite a `estudio-video/SKILL.md`; la skill real no se duplica |
| Plantillas de motion | `estudio-video/motion/plantillas.py` (tabla en la sección «Plantillas de motion») | boceto de cada plantilla listo; el build de HyperFrames se agrega al primer uso |
| Storyboard | `python estudio-video/herramientas/storyboard.py SPEC.json SALIDA.html` → `…\<Pieza>\Storyboard\storyboard_<ID>_vN.html` | plantilla `storyboard_plantilla.html`; formato del SPEC en la cabecera del script | tabla voz \| plano con fotograma (ffmpeg) por toma, IDs `S##`, alerta <1,5 s, 5 opciones por toma (3 planos + 2 motion designs) (planos + propuesta de motion, favorita ★ preseleccionada), «ninguna sirve», comentarios, varios videos por página; `servir` recibe el botón Enviar y guarda `decisiones/<ID>.json` |
| Registro de versiones (hoja v2) | `registro.py` (ver `registro/LEEME.md`) | IDs únicos, nombres de archivo, plan desde guion aprobado (`guion`), usos en el Directorio, cierre a Histórico (`cierres`, `cerrar`), importar/celdas hoja⇄espejo; genera `registro/manifest.json` |
| Render | `render_rental_v3.sh` (en esta carpeta); **el preview se corre con `FMT=16` únicamente** | `npx hyperframes render -q delivery --video-frame-format png`; ver trampas abajo |
| Color (flujo nuevo) | `PLANOS=1 python build_prproj.py SALIDA.prproj` + `trims_rental3_color.py [16 9 45]` | genera el prproj de planos sueltos para que Cris coloree; luego alinea los cortes coloreados a la línea de tiempo del builder y genera los medios por formato (respaldo en `media_neutro`) |
| Subir a Drive | `rclone.exe copyto ... gdrivew:"RENT - Rental DaaS/<nombre>" --drive-root-folder-id 1cda9LOGC2Yb_wli88bNpmJ0BRFqOnmDm` (remoto `gdrivew`, scope drive, autorizado por Cris el 26-oct-2026; el remoto `gdrive` sigue de solo lectura) | exports aprobados sin `_preview`; verificar tamaños contra el original y escribir los links (`https://drive.google.com/file/d/<ID>/view`, sin compartir público) en la col. W de la hoja |
| Variantes en lote | `herramientas/render_rental_variantes.sh ID ACC SCRIBE VOZ "16 9 45"`, `make_pt3.py` | acentos e idiomas: reconstruye, mezcla con `PLAN_JSON`, renderiza, post y copia a `Exports\` con nombre canónico |
| Serialización prproj | `prser.py` | reproduce byte a byte los `.prproj` de Premiere (`&#10;`, UTF-8); usar siempre al escribir |
| Premiere | `build_prproj.py`, `build_xmeml.py`, `prx.py`, `prlib.py`, `validate_prproj.py` | proyecto con V1 = master coloreado, V2 gráficos alfa, A1 audio; XML de respaldo (con `PLANOS=1`: prproj de planos sueltos para colorear) |
| Color propio | skill `colorear-plano`, `grade/pipeline.py` | alternativa automática si Cris la pide; el color de Cris se hace en Premiere tras aprobar el preview |
| Video INTA (12 piezas) | `videos/onescreen-inta/`: `seleccion.py` (filtro ≥2024), `voz_inta.py` (fuente Cristian Sánchez → voz a voz a Hale; juez Gemini opcional con `JUEZ=1`) / `voz_hale_directa.py` (ruta vieja), `mix_inta.py`, `gfx_inta.py`, `armar_caso25.py`, `producir.py`, `storyboard_spec_20_22.py` (SPEC del storyboard de INTA20-22 con 3 opciones por toma; `seleccion.elegir(..., n_alt=3)` da las alternativas) y `hoja_contacto_sb.py` (hoja de contacto para validar los planos contra la frase) | referencia del flujo guion→voz→planos→montaje por lote |
| Video corporativo | `videos/onescreen-corporativo/`: `tts.py` → `cortes.py` → `build_corp.py` → `mix_corp.py` → `render_corp.sh` | |
| Directorio de planos | Sheet `1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w`, `abrir-en-pc/` | ver `memoria/directorio_video_onescreen.md` |
| Imágenes | `imagenes_fal/`, `imagenes_leonardo/`, `imagenes_canva/` | nunca foto fija como plano: animar con Veo 3.1 |

## Trampas de este equipo
- **D: se llena** (quedó en 0,6 GB). Antes de renderizar, borrar `D:\hf-render\tmp\fc*` y `rfc*` (cachés regenerables). **Nada se guarda en C:** (casi lleno): TMP/TEMP y `--frames-cache-dir` en D:, y cada pieza en `D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\` (REGLAS §7b).
- GSAP: `gsap.defaults({lazy:false})`; nada de `immediateRender:false` con estado visible; trazos con `stroke-dasharray:1 2`. Ver `memoria/hyperframes_render_trampas.md`.
- Mirar tiras de fotogramas del MP4 final (ffmpeg), no solo `snapshot`: el snapshot no reproduce algunos fallos de render.
- Heredocs de bash con tildes o `→` se rompen aquí: crear archivos con la herramienta Write o con scripts de Python.

## Proyectos de video

Cada uno vive en `videos/<nombre>/` (código) y su carpeta de pieza en `D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\Proyecto\` (composiciones y renders; movidos desde `D:\hf-render` el 26-oct-2026). `D:\hf-render\` solo conserva `tmp` (cachés), `core`, `estilos` y `estilo_feb`.

| Proyecto | Estado | Notas |
|---|---|---|
| **Rental / DaaS v3** (`videos/onescreen-quizwiz-scrybe/build_rental3.py`) | UNA versión neutra en revisión (23-oct-2026) | Entregas en `…\10. Octubre\Rental DaaS\v3\`; proyecto Premiere en `…\Rental DaaS\Premiere v3\` (regenerar tras aprobar el diseño). Después: acentos ecuatoriano/mexicano y pt-BR. Nota: `memoria/video_rental_daas.md` |
| **Corporativo / salas de reuniones** (`videos/onescreen-corporativo/`) | v3 en revisión (26-oct-2026), sin 103182 ni 103512. **Desactualizado frente a las reglas vigentes:** su voz se hizo con la ruta vieja (`voz_dirigida.py` + `hale_co.py`) y sus cortes (18 en 21,8 s, 1,2 s promedio) incumplen el mínimo de 1,5 s. Si se retoma: voz nueva con `voz_exp_d.py` (§6) y recortes ≥1,5 s, con storyboard antes de ensamblar | guion C aprobado; planos del Directorio; `tts.py` → `cortes.py` → `FMT=… build_corp.py` → `mix_corp.py` → `render_corp.sh`; renders en `D:\OneScreen\Contenido\2026\10. Octubre\Corporativo salas de reuniones\Proyecto\out` |
| **INTA** (`videos/onescreen-inta/`) | 12 piezas; versiones .0003 (≥2024) en revisión según la hoja de producción (el espejo `registro/produccion.csv` puede ir atrás: **manda la hoja**, ver H.2) | piloto de motion INTA16 (`gfx_inta.py`); INTA25 sin narrador (`armar_caso25.py`); una canción distinta por pieza. Correcciones: `CORRECCIONES.md` 26 y 27-oct |
| QuizWiz + Scrybe v2 | entregada en 3 formatos | falta versión sin subtítulos y color. `memoria/video_quizwiz_scrybe_v2.md` |
| Lessn pitch | referencia de mezcla aprobada | `videos/onescreen-lessn-pitch` |
| Flota de IA | referencia de motion "Apple" | `videos/onescreen-flota-ia` |
| Short Casa López | color estándar | `D:\OneScreen\Contenido\2026\5. Mayo\CASO DE ÉXITO. Casa López\Proyecto short`, `memoria/short_casa_lopez.md` |
| Otras líneas | ver `videos/` | Academy, Guru, intros, T7, Titan, Wandr, etc. |

## Receta del Rental v3 (ejemplo de builder; el flujo vigente son los 16 pasos)
1. `FMT=16 python build_rental3.py` (y 9, 45); mezcla con `PLAN_JSON=... python mix_rental.py`.
2. Variantes: `bash herramientas/render_rental_variantes.sh ID ACC SCRIBE VOZ "16 9 45"` (pt-BR con `make_pt3.py`).
3. IDs vigentes: RENT.0006 neutro, 0007 Ecuador, 0008 México, 0009 pt-BR (aprobadas 26-oct-2026); RENT.0001-0005 reemplazadas. El color de ese video se hizo con el flujo anterior (`PLANOS=1 build_prproj.py` + `trims_rental3_color.py`).

## Cómo trabajamos
- Cris revisa en celulares y pantallas grandes: márgenes seguros reales, menos relleno.
- Nunca keys ni datos de clientes en esta carpeta (va al repo): las claves son variables de entorno.
- Esta carpeta es solo de video: carruseles, Odoo, SEO, Todoist y reportes no se tocan aquí.
- No toques ni muevas `estilo-onescreen/`, `grade/`, `luts/` ni `videos/*`: las rutas de los builders y de la memoria dependen de ellos.
- Las notas de `memoria/` son copias de la memoria de Claude Code: si cambias una regla, actualiza las dos (`herramientas/sync_memoria.py`) y avisa a Cris. Si cambia un script de `herramientas/`, actualiza la tabla de Herramientas de este archivo.

## Archivos de referencia (no hace falta leerlos al empezar)
- [CORRECCIONES.md](CORRECCIONES.md) — historial fechado de cada corrección de Cris. Las reglas vigentes ya están arriba; se consulta solo ante una duda.
- [PROCESO-RENTAL-DAAS.md](PROCESO-RENTAL-DAAS.md) — ejemplo histórico del Rental v3, punta a punta.
- [registro/](registro/LEEME.md) y [registro/HOJA.md](registro/HOJA.md) — espejo CSV y columnas de la hoja de producción.
- [memoria/](memoria/INDEX.md) — notas de memoria de video (copias; `herramientas/sync_memoria.py`).
- [sistema-diseno/](sistema-diseno/LEEME.md) — dónde vive cada guía, logo, tipografía, color.

