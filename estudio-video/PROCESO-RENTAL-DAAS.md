# Proceso del video Rental / DaaS (21 al 23 de octubre de 2026)

Documento para convertir lo que hicimos en un proceso repetible. Describe el camino completo, las correcciones de Cris y lo que sigue pendiente. Las reglas resumidas están en [CLAUDE.md](CLAUDE.md); las rutas de cada herramienta, en [CLAUDE.md (Herramientas)](CLAUDE.md (Herramientas)).

> **Documento histórico (v3 del 21-23 oct).** Donde habla de planos "sin colorear", conversión neutra S-Log3→Rec.709 o Lumetri clonado del Sheet, quedó reemplazado: el color lo hace Cris en el .prproj tras aprobar el preview (28-oct). El flujo vigente está en [CLAUDE.md](CLAUDE.md) y las reglas en [CLAUDE.md](CLAUDE.md); este archivo sirve como ejemplo de punta a punta, no como receta.

## 0. Resultado
- Video de ~37 s de contenido + 8 s de intro de marca (45 s), 16:9, 9:16 y 4:5, voz neutra (`v_rv_1`), planos de casos de éxito **sin colorear**, música MASTER_Fashion, efectos de sonido y mezcla propia.
- Cinco escenas de diagrama sobre fondo de color/blanco (con cámara 3D y lettering que sube por palabra), cuatro tarjetas de ventajas con plano + mini-diagrama, planos con texto directo y subtítulos solo donde hacen falta.
- Entregas: MP4 en `D:\OneScreen\Contenido\2026\10. Octubre\Rental DaaS\Proyecto\out_r3\`; proyecto de Premiere (V1 planos 4K, V2 gráficos con alfa, audio, Lumetri del Sheet) en `…\10. Octubre\Rental DaaS\Premiere v3\` (generado con el diseño anterior: hay que regenerarlo tras aprobar).

## 1. Brief y guion
- Entrada: guion de Cris ("tu primera aula digital → dos caminos: comprarla o DaaS (arrendamiento) → ventajas: pagas por lo que usas, siempre actualizada, soporte técnico prioritario, si sufre daño nos encargamos → ¿quieres adquirir tu pantalla? Pregúntanos") y la URL `onescreenlatam.com/rental`. Pedido: casos de éxito variados, "voz chimba", "todo lo que ya viste" (el método de [[video-quizwiz-scrybe-v2]]).
- Estructura en beats (cada uno nace de una palabra de la voz): A primera aula digital · B pantalla interactiva · C OneScreen a tu medida · D dos caminos (comprarla/contáctanos/arrendarla) · E DaaS · F cuota mensual · G toda tu institución · H–L muchas ventajas (4 tarjetas) · M ¿quieres adquirir tu pantalla? · N pregúntanos + URL · cierre con intro de marca.

## 2. Voz (dirección)
1. **Generación:** ElevenLabs `eleven_v4` (MCP `creative_generate_speech`), voz Hale, español neutro. Varias tomas por frase; se escoge una.
2. **Bajar las tomas** del historial por API (`bajar_voz.py`/`bajar_ids.py`); el historial no trae la voz, así que se mapean por orden de timestamp por llamada.
3. **Post de voz (`voz_gen.py`):** recortar silencios >0,16 s a 0,09 s, tempo 1,06, EQ. Esto da el ritmo de edición de Cris (voz compacta, sin muletillas).
4. **Tiempos por palabra:** Scribe (`scribe_v1`, `language_code` spa/por) → `scribe_*.json`. Todo el montaje (cortes, textos, gráficos, SFX) se ancla a esos timestamps.
5. **Variantes:** acento ecuatoriano marcado y mexicano (tomas `ec_b1`, `mx_d1`), y pt-BR con guion adaptado (`LOCALIZACION-PT-BR.md`). Regla de Cris: **se hacen después de aprobar la versión neutra**, con el estilo ya corregido.
6. Dirección que funcionó: frases cortas, tono cálido y firme, énfasis en "dos caminos", "DaaS", "pagas por lo que usas", "nos encargamos" y la pregunta final con subida.

## 3. Planos (material)
- **Fuentes:** casos de éxito 4K de Cris: ULA (C1198), Areandina Pereira (C1010), UCuenca (C0584, C0587), Itecsur (C0510), Comfenalco (C1335), Gimnasio Los Cerezos (C1379), Cablecom (C0627), Areandina (C0742). Elegidos del Sheet "Directorio de video" por lo que muestran (docente en pantalla, interacción táctil, aula completa, soporte).
- **Cortes:** `trims_rental3.py cut` saca la ventana de cada plano en 4K (sin audio, CRF 11). `formats` genera la versión por formato con recorte desde el punto focal x del sujeto + conversión neutra S-Log3→Rec.709 solo para poder ver.
- **Reglas de Cris sobre planos:** sin foto fija jamás (animar con Veo 3.1); sin mouse en apps táctiles; planos **sin colorear** en el ensamble; el color real viene del Lumetri de sus proyectos (ver §8).
- Zoom de planos como Escala (100/125/144 %) para dar el zigzag de edición.

## 4. Estilo de edición (de Cris, medido en sus 28 videos)
- Cortes, entradas de apoyo, zooms y gráficos caen **2-3 cuadros antes de la palabra**; no al compás de la música.
- Zigzag de escala alternando 100 % y cerrado; apoyo literal; montaje G de 5 planos en una frase ("toda tu institución") con una pantalla que se suma por plano.
- Cámara que flota suave sobre los planos (posición y escala por tramos) solo en el MP4; en Premiere va como ajuste.

## 5. Diseño visual: cómo llegamos al estilo final
**v1 (21-oct):** escenas "Flota de IA" (nodos conectados, tarjetas con plano y mini-íconos, texto en cajas). A Cris le encantaron los nodos y las tarjetas de ventajas con plano.

**Correcciones de Cris (23-oct), en orden, y qué cambió:**
1. *Estilo de texto:* "muchos videos de OneScreen combinan texto sobre el plano, no tanto fondo blanco; el blanco se usa para enfatizar". → texto directo sobre el plano; tarjetas blancas solo para una línea de énfasis. Guía en `estilo-onescreen/08_TEXTO_Y_SUBTITULOS.md`.
2. *Subtítulos:* siempre blancos con trazo negro duro y muy fino; no se usan si un gráfico/texto ya lo dice.
3. *Sin contenedores:* texto sobre plano nunca en cuadros/píldoras (reiterado después con la píldora de "Contáctanos").
4. *Márgenes:* "muy pegado… la gente lo ve en celulares grandes y pantallas grandes". → zonas seguras reales; luego subidas otra vez (16:9: 270 px laterales).
5. *Motion graphics repetidos:* "te quedaste en los mismos diseños de Flota". → cada gráfico con su propio tratamiento, descriptivo y sincronizado con la voz.
6. *Balance:* "mataste los motion graphics?… quiero más balance, no todo motion ni todo texto". → mezcla de plano+texto, escenas de color y plano limpio.
7. *Fondos de color:* "puedes poner los motion graphics sobre fondos blancos o de colores, variado". → escenas D azul, E morado, tarjetas blancas.
8. *Trazo y brillo:* "muy delgados, ni ese brillo; me gustaban más como en Flota". → trazo ~7 % del ícono; sin sombras difusas (el brillo se reserva).
9. *Íconos animados:* "no puede ser solo un iconito animado… cosas que representan otras cosas". → diagramas: bifurcación con nodos y paquetes de luz, órbita de monedas, fila de pagos que se marcan, barras de uso con moneda que las sigue, cola donde el ticket salta al frente, pantalla agrietada que se repara y queda protegida.
10. *Tarjetas:* "¿por qué quitaste las tarjeticas…? esas me encantaban" y "en las tarjeticas habías puesto planos, estaban chéveres". → tarjetas de ventajas de vuelta, con plano arriba + mini-diagrama + título + subtítulo.
11. *Píldoras:* "en contenedores no uses píldoras". → "Contáctanos" quedó como texto con ícono, sin contenedor.
12. *Cruces:* "estás pisando textos con gráficos". → revisión de cruces en los tres formatos; se reubicaron esquinas de enfoque, ondas de toque, "DaaS" y la cuadrícula de pagos.
13. *Diagramación repetida:* "título grande a la izquierda y gráfico a la derecha: se siente plantilla; sé más juguetón, estilo lettering de Apple, tipo cámara 3D". → diagramación distinta por escena (ver §6).
14. *Entrada del lettering:* "no me gusta cómo aparecen… de abajo hacia arriba por palabra, con transparencia, nada brusco; la estirada me recuerda a PowerPoint". → cada palabra sube con fundido, ≥1 s, `power3.out`; sin giros.

## 6. Diagramación final por escena (16:9; en vertical se centra o se apila)
- **A** plano ULA + "Tu primera / aula digital" (abajo izq.) + esquinas de enfoque que se cierran sobre la pantalla.
- **B** plano táctil + subtítulo + ondas de toque.
- **C** plano + logo oficial centrado + subtítulo.
- **D (azul):** "Dos caminos." gigante (la palabra *Dos* ligera, *caminos.* bold) entra por palabras; se encoge a encabezado en la esquina mientras la bifurcación se levanta del "piso" en 3D: pantalla → carrito (Comprarla) y calendario (Arrendarla), con paquete de luz bajando por cada camino y "Contáctanos" con ícono de chat.
- **E (morado):** "DaaS" enorme al centro, tres monedas azules **orbitan en 3D** alrededor (pasan por detrás y por delante), "modelo de arrendamiento" abajo.
- **F:** plano + "Una cuota / **mensual**" centrado y grande + fila de 12 casillas que se van marcando (cuota cada mes).
- **G:** montaje de 5 planos, texto a la derecha, fila de pantallas que se suma por plano.
- **H–L (blanco):** "Muchas ventajas." centrado; las 4 tarjetas llegan una a una **desde la profundidad** con giro de cámara suave, cada una con su plano y mini-diagrama.
- **M:** tarjeta blanca de énfasis "¿Quieres adquirir tu pantalla?".
- **N:** plano + "Pregúntanos" centrado + URL + globo de chat con puntos.
- **Cierre:** intro de marca de 8,09 s con su propio sonido.

## 7. Cámara 3D y lettering (técnica)
- Contenedor `.w3` con `perspective:1500px` y mundo `.wd` con `transform-style:preserve-3d`; la cámara es animar `z`, `rotationX/Y` del mundo (acercarse y girar 5-10° con `power3.out`/`sine.inOut`).
- Lettering `big()` + `lets()` (una palabra = un elemento `.lw`) + `flip()` (nombre histórico; ahora sube de abajo hacia arriba con opacidad).
- Órbita 3D: las monedas se animan con keyframes de x/z precalculados (círculo con ease inOut), de frente a cámara; la rotación anidada con CSS dio monedas de canto.
- Fork "del piso": `rotationX 64→0` + `y` + opacidad con `transformPerspective:1500`.
- Tarjetas desde la profundidad: `z:-1200`, `rotationY` según la posición, `transformPerspective:1500`, mismo origen para tarjeta y plano.
- Trampas: sin `immediateRender:false` con estado visible; trazos con `stroke-dasharray:1 2`; los hijos de `.wd` no son clips.

## 8. Color y Premiere
- Planos sin colorear (decisión de Cris: "déjalos sin colorear"). El **.cube de Lumetri no sirve** fuera de Premiere.
- Proyecto de Premiere (`build_prproj.py`): sobre la plantilla C1186.prproj (secuencia 4K, 23,976 fps, ticks 254016000000/s); V1 planos 4K con Escala; V2 el MOV de gráficos con alfa (ProRes 4444, 24000/1001); V3–V6 los planos de las tarjetas con Posición/Escala; A1 la mezcla. El **Lumetri se clona** del proyecto original de cada plano según la columna AP del Sheet (hecho en 5 planos; C1198 y C0627 no tienen proyecto con color; C1010 y C1379 tienen proyecto pero sus clips ahí no llevan Lumetri (reverificado el 26-oct); la capa alfa se regeneró tras aprobar porque las tarjetas habían cambiado). Se entrega mapa de color y un XML de respaldo sin Lumetri.
- No verificado: que Premiere lo abra sin pedir reparar; que el alfa se interprete como alfa recto.

## 9. Música, SFX y mezcla
- Música: **MASTER_Fashion** (master propio de Cris, 161 BPM, sol menor). La "explosión" de la canción (12,40 s) se alinea con el corte a "Dos caminos" (más 2 cuadros); Cris corta después del hook.
- SFX discretos (volumen 0,13–0,30), **75 ms antes** del evento y afinados a sol menor (pop, tick, swipe, ding, scan, whoosh, hit).
- Niveles: voz ≈ -18 LUFS, música ≈ -24 LUFS, SFX aún más bajos; música baja 0,35 durante el cierre; intro de marca con su sonido; limitador a 0,89.
- Para elegir música nueva: analizar estructura (pausa → subida) y true peak antes; rechazar > -1 dBTP.

## 10. Render y entrega
- `FMT=16|9|45 python build_rental3.py` → `D:\OneScreen\Contenido\2026\10. Octubre\Rental DaaS\Proyecto\v_<FMT>`; verificar con `hyperframes check` y `snapshot --at …` mirando cada escena, los tres formatos y los cruces.
- `mix_rental.py` → `mix_rental3.wav`; `render_rental_v3.sh` (render PNG 24 fps, post con aberración leve + intro + audio); `ffprobe` para duración y pistas; copiar a Octubre.
- Trampas del equipo: disco D: lleno (borrar cachés `fc*`/`rfc*`), C: casi lleno; los renders pesan 30–55 MB por formato.

## 11. Qué hacer la próxima vez (proceso)
1. Brief + guion → beats ligados a palabras.
2. Voz neutra (ElevenLabs v4) + post + Scribe.
3. Elegir planos del Sheet; cortar 4K sin colorear.
4. Diseñar cada escena **con diagramación distinta**, motion que representa, lettering por palabra, cámara 3D suave; texto sin cajas; subtítulos solo donde no hay gráfico.
5. Revisar fotogramas de los tres formatos (cruces, márgenes).
6. Mezcla y render; enviar **una** versión a Cris.
7. Con su aprobación: proyecto de Premiere (+ Lumetri) y luego acentos/idiomas/formatos extra.

## 12. Pendiente de esta pieza
- Aprobación de Cris del diseño v3 (especialmente cámara 3D y las tarjetas).
- Regenerar el MOV de gráficos y el proyecto de Premiere con el diseño final.
- Versiones ecuatoriana, mexicana y pt-BR con el estilo corregido.
- Recuperar las entregas anteriores de `…\Rental DaaS\` (la carpeta apareció vacía el 26-oct).
