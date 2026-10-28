# 06 Estilo "Orgánico" (video de Cris: Colaboradores que colaboran)

Versión 3 (3 ejemplos con su edición real: Colaboradores que colaboran, Nativos digitales y Regreso a clases), 21 de octubre de 2026. Fuente: `D:\OneScreen\Contenido\2026\7. Julio\VIDEO. Colaboradores que colaboran\` (video de julio de 2026, 46,4 s, 4K 23,976 fps; entregas 16:9, 9:16 y 1:1) y su proyecto de edición **`VIDEO. Colaboradores que colaboran.prproj`** (el de `Orgánico/` solo tiene las secuencias de entrega; yo había leído ese por error). Del `.prproj` se midieron cortes, escala, keyframes, efectos y audio del montaje 16:9 (`C1573`) y el reencuadre 9:16. "Orgánico" es el nombre provisional (viene de su carpeta); Cris aún no lo confirma.

Regla de aprendizaje: con UN video lo de abajo es medido pero **no generalizado**; fijar como regla del estilo solo con ≥3 ejemplos y la confirmación de Cris.

## Lo que lo hace "orgánico" (medido)
1. **Capa de ajuste sobre TODO el video** (0–38,3 s) con dos efectos:
   - *Transformar* animado: **escala uniforme 103,5–105,2 %** y **posición x 0,481–0,522 (±~2 %), y 0,485–0,515**, con 8 keyframes en un bucle de ~12,5 s (separados 0,8–2,5 s, interpolación Bézier). Simula una cámara en mano que flota. Se repite en bucle sobre toda la pieza.
   - *Error cromático de VR*: **rojo −3, azul +3, distancia de difuminado 10**: borde cromático leve en toda la imagen.
2. **Cámara múltiple simulada con escala**: el plano único del presentador (C1573/C1574/C1575) se corta en tramos de 1,0–3,4 s y se alterna **escala 100 % / 107–145 %** (valores 129, 145, 131, 127, 138, 107) para que parezcan dos cámaras. Corte seco, sin transiciones; solo hay disoluciones de ~2 cuadros (0,08 s) aisladas.
3. **Montaje tipo tartamudeo antes del gancho**: tramos de 0,25 / 0,08 / 0,08 s (18,1–18,6 s) justo tras un riser de 3,7 s (13,2–16,9 s); la música pasa a su 2.ª parte en 17,52 s. Es el "punto de giro" de la canción alineado con el corte.

## Estructura
Gancho a cámara con cortes cada ~1,9 s → tarjeta blanca de una línea (**"Color mate"** + texto, 1,21 s en 8,05–9,26 s) → lista hablada con **palabras sobre planos de apoyo** → demostración con planos de producto (C0070, C0072, C1567) → **intro de marca** pegada al final (38,29–46,38 s).

## Palabras sobre el material
Son **PNG exportados de Illustrator** (`Graficos/Graficos.ai`; `Recurso 1–3.png`), cada uno de ~1,04 s, en capas V3/V4: **opacidad 0→100 % en 0,08 s**, **sube en posición de y=0,872 a 0,634 (≈24 % del alto) en 0,21 s**, se queda ~0,46 s y **flota hasta y=0,382 mientras se desvanece** en los últimos 0,37 s. Llevan **sombra paralela** (distancia 5). Una palabra por vez, sincronizada con la voz.

## Planos de apoyo
Clips 4K generados con IA reutilizados de febrero 2026 (`Ellos_estn_demasiado_4k_…`, `Slow_orbiting_4k_…`, `Hes_trying_to_4k_…`, de las carpetas de febrero) en la capa V2, 1–3 s, sobre la narración.

## Cierre
No es animación hecha para este video: es la **intro de marca** `OneScreen (Intro)_ESP_16.9_NoMúsica.mp4` (8,09 s) de `D:\OneScreen\Brand kit\Varios\Audiovisual\Intro\` (hay versiones 9.16, inglés y portugués, con y sin música). APRENDE / INTERACTÚA / CONECTA / logo vienen de ahí. **Reutilizarla, no rehacerla.**

## Subtítulos
Subtítulos automáticos de Premiere (captions de transcripción), bloques de 0,2–1,1 s con 2–3 palabras, pequeños (~2,5 % del alto), blancos con sombra. En 16:9 abajo (~82 %); en 9:16 a media altura bajo la barbilla (~50 %).

## Color (confirmado por Cris y medido en el .prproj)
- **LUT: Glenderaterra** (el mismo "Kodak 2383 Glenderaterra MOD" que usa `grade/` en [[pipeline-color-slog3]]), aplicado con **Intensidad 50 %** en Lumetri > Creativo > Aspecto. Coincide con la etapa 4 del pipeline ("2383 al 50 %").
- **El color vive en Controles de efectos > "Origen"** (efecto a nivel del clip fuente, no de la secuencia). Por eso en el clip de la secuencia Lumetri se ve vacío: la corrección base está en el clip maestro, y en la línea de tiempo solo se retoca la **exposición por clip** (0,65 a 1,63 EV; hay 12 grupos de ajustes iguales).
- Base de C1573 (3 versiones casi iguales en el origen): **temperatura −27, tinción +1,75, exposición +0,3 a +1,0, contraste +88,8, altas luces +10, sombras −3,9, blancos −8,8, negros −13 (−45 en una), saturación creativa 80,7 %, temperatura creativa −9,5, viñeta muy leve (cantidad −0,78, punto medio 18,7), "Desenfocar" 11,2**.
- Otro juego para otras tomas (C1574/C1575 o planos de apoyo): temperatura −32,6, exposición +1,35, contraste +83,9, altas −33, sombras −39, blancos −29, negros −30,5, intensidad del look 40,7 %.
- Lectura: grado frío (temperatura negativa), contraste muy alto, negros/blancos recortados, saturación algo baja y viñeta casi imperceptible. NO coincide todavía con lo que hace mi pipeline en la etapa 3 (curvas por percentiles); sirve para recalibrar si Cris lo pide (no tocar parámetros calibrados sin pedírmelo). Pendiente: cómo convierte el S-Log3 (el LUT de entrada de Lumetri está en 0).

## Reencuadre por formato
Tres secuencias del mismo montaje. 1:1 y 9:16 usan **Auto Reframe** de Premiere con seguimiento de movimiento: escala 177,8 % (16:9→9:16), posición x del sujeto con keyframes cada ~0,2 s (0,46–0,66), **conservando la alternancia de escala por clip** (100 / 129 / 145 %). Subtítulos reubicados a media altura en 9:16 ([[zonas-seguras-videos]]).

## Audio
Voz limpia separada por clip (`C1573-esv2-75p-bg-10p-music-10p.wav`: *Enhance Speech v2*, voz 75 %, fondo 10 %, música 10 %), música **BearStockMusic – Funk Rock (Full Version)** de principio a fin, riser `376576__original_sound__riser-quick-2.wav` (13,2–16,9 s) y la intro de marca al final. Mezcla −16,3 LUFS, LRA 2,6, pico +0,1 dBFS (más caliente que lo aprobado en [[mezcla-audio-videos]]).

## Ejemplo 2: "Nativos digitales" (jul-2026, 46,3 s, 4K, entregas 16:9 Clean/Subs/White, 1:1, 9:16)
Fuente: carpeta `VIDEO. Nativos digitales` (mismo mes) y su `VIDEO. Nativos digitales.prproj`; secuencia `16x9` leída. **Presentadora** (otra persona, misma sala y pantalla, C1562/C1565/C1566) en vez de Cris.
**Lo que se repite igual (→ es plantilla del estilo, no casualidad):**
- La **misma capa de ajuste** con exactamente los mismos keyframes (posición, escala 103,5–105,2 %, bucle de 12,5 s) y la misma **aberración cromática de VR (R −3, B +3)**, sobre 0–38,25 s. Se copia y pega de un proyecto a otro.
- Tarjeta blanca de una línea ("La educación del **futuro**", 1,08 s en 0,71–1,79 s) hecha con **"Color mate" + imagen** (`01.jpg`).
- **Intro de marca** `OneScreen (Intro)_ESP_16.9_NoMúsica.mp4` (8,09 s) pegada desde 38,25 s.
- Palabras/gráficos PNG (`Recurso 1–3.png`) con **opacidad 0→100 y subida de y=0,753 a 0,638 en ~0,8 s** (más lenta que en el ejemplo 1: ahí 0,08 s de opacidad y 0,21 s de subida), escala 56–78 %; uno de ellos con tartamudeo de 0,12 / 0,75 / 0,38 s.
- Alternancia de escala por clip, pero **más fuerte**: tramos de **0,5–2,75 s (mediana ~1,2 s)** y escalas **138–166 %** contra 100 % (en el ejemplo 1: 107–145 %, tramos de 1–3,4 s). Corte seco, sin transiciones.
- Planos de apoyo **Envato** (`-utc`: niño con tableta, ciudad digital, niños aprendiendo ciencia, ampliados 200–260 %) más un clip `grok-video-…` (IA) y planos de pantalla/producto C1567/C1568 (4,2 s y 2–2,5 s).
**Audio distinto:** pista de **aplausos/percusión** (`claps-in…`, Envato) de principio a fin, con un `Fire Whoosh` en 7,59 s (sin riser ni música tipo funk); mezcla **−14,8 LUFS**, LRA 3,9, pico +0,1 dBFS (más caliente que el ejemplo 1: −16,3).
**Reencuadre:** igual (Auto Reframe con seguimiento, escala por clip conservada).
**Color:** solo 11 Lumetri (vs 55): casi todo ya viene graduado desde el origen; aplicó Lumetri a pocos planos de apoyo.
**Lo que cambia entre ejemplos (variables del estilo):** quién habla, música (funk con riser vs claps), ritmo de cortes (≈1,9 s vs ≈1,2 s), intensidad del zoom por clip, velocidad de entrada de los PNG.

## Ejemplo 3: "Regreso a clases" (jul-2026, 47,7 s, 4K; entregas 16:9, 9:16, 1:1 y versiones WhatsApp)
Presentador joven (C1576/C1577), mismas piezas fijas: capa de ajuste, tarjetas blancas de una línea con **pregunta** ("¿Proyección?", "¿Parlantes?"), intro de marca de 7,47 s al final (39,58 s), Auto Reframe para 9:16/1:1. **Lo nuevo:**
- **Zooms que se mueven** en algunos clips (keyframes de escala 131→145 % en 1,08 s y 100→115 % en 1,58 s), además de los saltos fijos 119–153 %.
- **Planos de apoyo** Envato más ampliados (200–209 %: proyector, parlantes, enchufes, marcador) y tomas propias de la biblioteca (C0063, C0924/C0925, C0012, C0016, C1578, C1581).
- **Rótulos directos sobre el plano** ("Todo funciona inalámbricamente", "1.07 millones de colores"), en Rubik, sin tarjeta, y una **pastilla blanca "onescreenlatam.com"** bajo el presentador al cierre.
- **Ritmo:** tramos desde 0,29 s hasta 5 s (más variado que el ejemplo 2).
- **Audio:** pista `Claps 1.wav` (una de las que él masterizó) de principio a fin; mezcla −14,3 LUFS, pico +0,4 dBFS. Color: 24 Lumetri.
**Patrón confirmado en 3 videos:** capa de ajuste + aberración cromática idénticas, escala alternada por clip, tarjeta blanca de una línea, PNG/rótulos que suben, planos de apoyo ampliados, intro de marca al final, Auto Reframe. **Variables:** presentador, música (funk con riser / claps), ritmo y fuerza del zoom, loudness (−16,3 / −14,8 / −14,3 LUFS).

## Diferencias frente a "Apple" ([[estilo-motion-apple]])
Apple = secciones de color, íconos de línea dibujados, sin presentador. Orgánico = presentador + planos de apoyo + palabras que suben + **cámara que flota** + cierre de marca prefabricado. No se mezclan en una pieza.

## Preguntas abiertas para Cris
- ¿"Orgánico" es el nombre? ¿Cuántos otros videos suyos son de este estilo?
- ¿La capa de ajuste (flotación + aberración cromática) va en todos sus videos orgánicos?
- ¿Los PNG de palabras salen de una plantilla de Illustrator ("Graficos.ai") que se reutiliza?
