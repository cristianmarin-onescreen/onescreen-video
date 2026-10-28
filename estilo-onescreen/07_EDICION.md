# 07 Edición de Cris: ritmo, zoom, planos de apoyo y voz

Versión 2, 21 de octubre de 2026. Aprendido de **33 videos** (28 + 5 casos de éxito 2026, sección 8) de las 31 carpetas que Cris señaló (feb 2026, caso de éxito de 2025, series "Titled" de mayo–jun 2025). Método: se leyó el `.prproj` principal de cada carpeta (solo el de la raíz, nunca autoguardados; la secuencia que coincide en duración con el render final) y se cruzó con lo que dice la persona: captions de Premiere cuando el proyecto los tiene, SRT exportado, o transcripción por palabras (ElevenLabs Scribe) cuando no. Herramientas en `estilo-onescreen/tools/` (`edit_vs_voz.py`, `edit_vs_voz_lote.py`, `analiza_prproj.py`); guiones de edición línea por línea de cada video en `estilo-onescreen/edicion_guiones/`.

Qué es **medido** y qué es **interpretación** está marcado. Con 28 videos del mismo autor las medidas son sólidas; las interpretaciones sobre "por qué" las debe confirmar Cris.

No se pudieron leer: Perú (no hay `.prproj`), UISRAEL (la carpeta solo trae una subcarpeta) y Tu pantalla ya es buena (sin proyecto en la raíz). En Itecsur el analizador eligió una secuencia anidada y no midió nada. En las series de 2025 el clip principal aparece duplicado en dos pistas, así que su "cobertura de apoyo" sale inflada y no se usó.

## 1. La voz manda; la música no
**Medido.** Los cortes del plano principal, las entradas de plano de apoyo, los inicios de zoom y la aparición de los gráficos caen en promedio **100 ms (2–3 cuadros) ANTES del inicio de una palabra**: 63,6 % de los cortes y 63,6 % de los zooms caen en la ventana 0–120 ms antes de una palabra (azar 36 %); 54 % de las entradas de apoyo y 60 % de los gráficos (azar 36 %). El resultado se repite en 25–27 de los videos. Las **salidas** de los planos de apoyo caen en el final de una palabra (±1,5 cuadros: 44 % contra 25 % de azar, diferencia mediana +10 ms).
**Lo que NO hace.** No corta al compás: el alineamiento de los cortes con el pulso de la música es igual al del azar en casi todos (p. ej. 24 % contra 23 %; 5,6 % contra 20 % en uno de julio). El ritmo de cortes **no depende de la velocidad del habla** (correlación palabras/s contra duración de plano: −0,04). Es un ritmo objetivo por formato (sección 2), tratado con la voz como regla de colocación. La música (una sola pista de punta a punta, tempo 100–132 BPM; 160 en dos shorts) se pone debajo y no manda sobre los cortes.
**Interpretación.** Anticipar 2–3 cuadros el cambio de imagen respecto a la palabra hace que la imagen "llegue" antes de que el oído lo registre; el cambio parece causado por la frase, no por el montaje.

## 2. Ritmo por tipo de pieza (plano principal = A-roll)
**Medido** (cortes del A-roll por minuto; mediana de duración de plano):
- **Explicativos con presentador, feb 2026** (Ecosistema, Lessn, Scrybe, QuizWiz, SuprNotes, Beneficios ×2, inversión pública, "qué hace…", vs otros, Academy, Actualización T7): 33–41 cortes/min, plano mediano 1,25–1,7 s.
- **Casos de éxito con entrevista** (Cablecom, Areandina, UCuenca): 22–27 cortes/min, plano mediano 2,1–2,6 s (el entrevistado habla a 3–4 palabras/s; más aire por plano).
- **Cortos "Titled" de 2025** (Class, IA, Prepara tu clase, Scrybe traduce, Ser distribuidor, Ahorra tiempo, Google EDLA, Apps de ingeniería): 37–47 cortes/min, plano mediano 1,0–1,4 s.
- Excepciones de toma larga y cero zoom: Itecsur, Beacon, Infocom y Academy (tutorial): sin alternancia.

## 3. Zoom: alternancia constante entre ancho y cerrado
**Medido.** El plano principal **alterna plano ancho (100 %) y plano cerrado en cada corte**: mediana de alternancia **92 %**; 22 de 27 videos ≥ 80 %. Casi la mitad de los clips (46–50 %) van cerrados. Es un salto fijo de escala (no un zoom animado: solo 3 clips en todo el conjunto tienen zoom animado, p. ej. 131→145 % y 100→115 % en "Regreso a clases").
- Valores del cerrado (los más frecuentes): **137 y 144 %** en entrevistas (casos de éxito), **150–188 %** en presentadores (más usados: 178, 163, 174, 176, 157, 164 %), 166–180 % en los cortos.
- El inicio de un clip cerrado cae en promedio en el 26–50 % de la frase, y el de uno ancho en el 32 %: **no se cierra "para enfatizar una palabra"**; es un zigzag rítmico que simula dos cámaras con una sola toma. La lógica es: cada corte cambia el encuadre; la anticipación de 2–3 cuadros de la sección 1 oculta el salto.
**Confirmado por Cris (21-oct):** el zigzag **siempre es un salto fijo de escala**. Lo usa (1) para que no se noten los cortes cuando borra muletillas o silencios de una misma toma (jump cut) y (2) para dar ritmo. No es énfasis semántico.
**Los valores dependen del plano:** con presentadores los planos son muy parecidos entre sí (por eso se repiten 150–188 %); en casos de éxito la composición cambia mucho según el lugar (por eso 137–144 % y mucha más variación). El valor se elige mirando el encuadre de cada toma para que el cerrado quede bien compuesto, no por una cifra fija.

## 4. Planos de apoyo (B-roll) frente a lo que dice la persona
**Medido.**
- Cubren **25–50 % del video**; duran **1,7 s de mediana** (p10 0,9 s, p90 3,2 s). El primero entra a los **3,75 s** de mediana (p25–p75: 0,8–5,2 s): se abre con el presentador y el apoyo llega con la primera idea concreta.
- Entran 0–120 ms antes de una palabra (ver sección 1) y salen en el final de una palabra.
- Tipos: tomas propias de la biblioteca (C####, la mayoría: pantalla en uso, planos del T7, botón Gurú), clips generados con IA (grok y similares, ampliados a **200–293 %, mediana 260 %**, para recortar bordes y marcas) y stock de Envato (ampliado 200–300 %). Las tomas propias van a 100–137 %.
**Criterio, observado en el guion de edición (interpretación respaldada por ejemplos):** el apoyo **ilustra literalmente lo que se dice en ese instante**, no el tema general.
- "Un proyector que solo se ve bien con un salón oscuro" → clip de luz en una sala oscura.
- "Audio integrado, dos parlantes… subwoofer" → plano de los puertos y parlantes; "micrófonos incorporados" → plano de los micrófonos.
- "Play Store y todas las apps de Google" → pantalla con Play Store y el video de Google I/O.
- "Compartir todo con un QR" → plano de escaneo de QR; "botón Gurú… en vivo con un ingeniero" → los planos del botón Gurú.
- "Logística… centros de distribución" → T7 en caja y bodega; "soporte gratuito e ilimitado" → clip de IA.
- Productos con pasos ("Lessn: seleccionas el tema y la clase…") → **ráfaga de 2–4 tomas cortas (0,3–1 s)** de la pantalla, cada una con su gráfico PNG numerado (Recurso 5, 6, 7, 8) que cambia con el paso.
- Cifras ("28 a 30 horas", "56 horas por mes", "1.000 horas al año", "41 días") → gráfico animado que aparece con la cifra, sin apoyo de video.
El presentador sigue como audio por debajo; el apoyo nunca cubre el inicio completo de una frase: el A-roll queda visible en el primer segundo de casi todas las frases y el apoyo entra a media frase (posición relativa mediana en la frase: 0,33–0,5).

## 5. Gráficos, sonido y música
- Gráficos: PNG de Illustrator con animación de entrada rápida (opacidad 0→100 en ~2 cuadros, subida en pocos cuadros; ver `06_ESTILO_ORGANICO.md`), escala 56–80 % en Titled, 62 % en listas de cifras.
- Efectos de sonido: en los 7 proyectos que los usan, el efecto se coloca **60–85 ms ANTES del evento visual** (75 % de los casos). Nombres: Swoosh, Swoosh Transition, Zoom, Bubble, Camera 2 (clic de cámara en tomas tipo foto).
- Música: una sola pista de principio a fin por video (Food Recipes, Cooking, Food, Percussion, Cooking Competition Show, Funk Rock, Documentary/Documentaries, Class/funk en los shorts), sin recorte a compás. En el proyecto no hay keyframes de volumen legibles (el nivel va por pista o por la mezcla); los niveles aprobados siguen siendo los de `mezcla-audio-videos` (voz ≈ −18 LUFS, música ≈ 6 LU abajo). Hallazgo útil: varias de esas pistas son las que Cris masterizó después (Cooking, Food, Percussion).

## 6. Receta para replicar un video (para el agente)
1. Transcribir la voz **por palabras** (Scribe) y marcar el inicio de cada palabra.
2. Fijar el ritmo objetivo según el formato (sección 2) y repartir cortes del A-roll alternando **100 % / zoom cerrado** (137–144 en entrevistas, 150–180 en presentadores).
3. **Mover cada corte, entrada de apoyo, zoom y gráfico a 2–3 cuadros antes de la palabra más cercana** que cae cerca del ritmo objetivo.
4. Elegir apoyos por **lo que se nombra en ese momento** (sección 4), duración 1–2,5 s, sin pasar el final de la palabra; listas de pasos en ráfagas de 2–4 tomas con PNG numerado; cifras como gráfico.
5. SFX 60–85 ms antes de cada entrada visual; música en una pista continua (no cortar al pulso).
6. Cierre: intro de marca prefabricada (ver `06_ESTILO_ORGANICO.md`).

## 7. Pendiente / dudas para Cris
- Falta analizar carpetas sin proyecto o con proyecto anidado (Perú, UISRAEL, Tu pantalla ya es buena, Itecsur) si Cris indica dónde están.
- La relación música–voz (ducking) no se pudo medir en los proyectos; se puede medir directamente sobre las pistas de audio de los renders si Cris lo quiere.

## 8. Casos de éxito 2026 (junio–julio): 5 carpetas más
Gimnasio Los Cerezos, Areandina Pereira, ULA Idiomas, Gimnasio Jireh y Comfenalco (proyecto principal de cada carpeta; cada una con 1 o 2 proyectos duplicados que se ignoraron). **Medido:**
- **Ritmo más lento y más apoyo que en los explicativos:** 12–24 cortes/min (plano mediano 1,8–4,2 s; ULA Idiomas es el más pausado: 12 cortes/min, 4,2 s). El **apoyo cubre 63–67 % del video** y dura **2,6–4,0 s** (en los explicativos: 25–50 % y 1,7 s): en un caso de éxito se enseña el lugar mientras la persona habla.
- **La regla de la voz se confirma y es más fuerte:** los cortes caen 0–120 ms antes de una palabra en **67–78 %** de los casos (azar 34–41 %), mediana 70–110 ms.
- **Zigzag:** alternancia 52–86 %; el cerrado es **un valor único por entrevistado** cuando la toma se repite (ULA 136 %, Jireh 148 %, Comfenalco 144 %) y **varios valores** cuando hay varios lugares o encuadres (Areandina Pereira: 120, 137, 163, 164, 172 %; Los Cerezos: 131, 135, 144 %). Confirma lo que dijo Cris: el valor se ajusta a la composición de cada plano.

## 9. Video Demo (agosto–septiembre 2026): 12 escenas, voz generada
**Corrección (21-oct):** antes escribí que no tenía montaje final; era falso. Solo había mirado el proyecto de la raíz. Estructura real: `Demo_OneScreen.prproj` (último guardado 25-sep) trae las escenas **SC01–SC05** (secuencias de 28 a 78 s) y las demás viven en proyectos propios dentro de `Apoyo/SCxx/` (SC06 VirtualWall, SC07 Softwares, SC08 Gurú, SC09 Wandr, SC10 Academy, SC11 Write, SC12 Rental), cada una con su export en `Exports/`. Sirve de modelo porque es **locución generada (ElevenLabs, voz Hale)** con música (phonk) y no tiene presentador.
**Medido por escena** (todos los eventos visuales: cortes de A-roll, entradas de apoyo y gráficos, contra las palabras de la voz):
- SC01 (apertura "Hay espacios que solo ocupan un lugar…"): 66 eventos/min; **65 % entra 0–120 ms antes de una palabra** (azar 36 %), mediana 90 ms; cambio de imagen casi por frase (0,2–1,7 s) y un PNG de texto (Recurso 1, 2, 3, 4, 5, 8, 9) que cambia con cada idea; el fondo cambia con la imagen literal de lo que se dice (aula vacía, oficina iluminada, nebulosa).
- SC03: 63 % (azar 32 %). SC09: 50 % (36 %). SC08: 45 %. SC10: 44 %. SC07: 41 %. SC11: 40 %. SC12: 36 %. SC06: 38 %. SC04: 39 %. SC05: 33 %. SC02: 32 %.
- Promedio de las 12 escenas: **44 % contra 34 % de azar**: la voz sigue mandando pero mucho menos que en los videos con presentador; a partir de SC04 las escenas son demos de software de 2–5 s por toma (mediana 2–5,5 s) y los cambios van más con la acción de la pantalla que con las palabras.
- Escenas con peor ajuste de duración (secuencia elegida frente al render de 2–4 s): SC06 (secuencia "LED" de 19,3 s frente a 22,3 s de render) y SC07: revisar a mano.

## 10. Qué tan confiable es cada medida (auditoría de la selección)
Para cada carpeta se eligió el `.prproj` de la raíz y, dentro, la secuencia cuya duración coincide con el render final. **En 30 de 33 carpetas la diferencia es 0–1 s.** Tres para revisar: Scrybe (2,1 s de diferencia), Pantalla interactiva vs otros (2,1 s) e **Itecsur (la secuencia elegida es un clip anidado; sus cifras no valen)**. Perú, UISRAEL y "Tu pantalla ya es buena" no tienen proyecto en la raíz. En 9 videos con transcripción de Scribe (sin captions) el agrupamiento en bloques es mío, así que la sincronía por **bloques** no es comparable; la medida por **palabra** sí. En las series de 2025 el clip principal está duplicado en dos pistas, por eso no se usó su cobertura de apoyo.
