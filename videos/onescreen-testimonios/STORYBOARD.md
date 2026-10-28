---
format: 3840x2160
fps: 25
duration: 73.4s
mode: collaborative
message: "Miles de instituciones ya respondieron la pregunta; esta puede ser tu historia"
arc: Pregunta → Escala → Testimonio → Invitación
audience: Decisores de educación y empresa en LATAM
music: none
---

# OneScreen — Testimonios (capa de lettering)

**Esto no es un film, es una CAPA.** Se entrega en ProRes 4444 con canal alfa para
montarse encima de `PrevSC02.mp4` en Premiere. El suelo va siempre transparente; el
metraje lo pone el editor debajo.

Dos variantes de tinta, misma animación y mismos tiempos:
`-alfa-negro.mov` para metraje claro, `-alfa-blanco.mov` para metraje oscuro y para
los dos bloques negros del corte.

**Sin gris.** Por instrucción explícita no hay nivel intermedio de tinta: la jerarquía
la hacen la escala tipográfica y el orden de llegada de las palabras.

## Lo que se midió del corte, no se supuso

| Dato | Valor | Cómo se obtuvo |
| --- | --- | --- |
| Duración y cadencia | 73.4 s a **25 fps** (1835 frames) | `ffprobe` |
| Bloques negros | 0–19.16 s y 62.92–73.36 s | `blackdetect=d=0.15:pix_th=0.10` |
| Cortes de plano | 18 en el tramo de entrevistas | `select='gt(scene,0.25)'` |
| Posición de las caras | ninguna a la izquierda del **38 %** del ancho | YuNet, muestreo cada 0.4 s, 110 muestras, 100 % de detección |
| Palabras | 205, con timestamp propio | whisper `large-v3-turbo`, español |

El margen izquierdo libre va del 28 % al 48 % según el plano. La columna de
subtítulos se fija en el **34 %** — cuatro puntos de holgura contra el peor plano.

## Frame 1 — Apertura (bloque negro)

- scene: Locución de marca en lettering a cuadro completo, sobre el negro del corte
- duration: 19.16s
- start: 0.000s
- frames: 479
- transition_in: cut
- status: animated
- poster: 12s
- asset_candidates:
- assets_note: ninguno — lettering puro
- voiceover: "Hace 15 años nos hicimos una pregunta simple. ¿Y si una pantalla pudiera enseñar tanto como la persona frente a ella? Hasta hoy seguimos respondiéndola. Y hoy, esa pregunta ya tiene una respuesta en más de 50 países. Miles de instituciones saben lo que es. Esto es lo que dicen algunos."
- src: compositions/frames/01-apertura.html

Seis frases, un cuadro cada una, centradas. El relevo entre frases no espera a que la
anterior termine de decirse: sale 0.06 s antes de que entre la siguiente, para que el
cuadro nunca quede vacío entre verso y verso.

Una palabra azul por cuadro como máximo: **pregunta · enseñar · — · países · Miles · —**.
Dos de los seis cuadros no llevan ninguna, a propósito.

`handoff_out` — a 19.16 s la última frase sale a la izquierda (la corriente del film),
todavía en movimiento en el frame del corte.

## Frame 2 — Testimonios (columna izquierda)

- scene: Subtítulos verbatim en la columna segura, sin pisar ninguna cara
- duration: 43.76s
- start: 19.16s
- frames: 1094
- transition_in: cut-the-curve LEFT
- status: animated
- poster: 30s
- asset_candidates:
- assets_note: ninguno — el metraje lo pone el editor debajo
- voiceover: "Número uno, OneScreen, porque nosotros validamos la parte técnica… El resultado fue que la forma de operar esta pantalla es más fácil que otras, es más intuitiva… Ya no es un lujo, es una necesidad."
- src: compositions/frames/02-testimonios.html

**13 bloques de subtítulo**, de 35 a 72 caracteres, con una permanencia media de
3.39 s (mínimo 1.52 s, máximo 4.68 s). Las palabras entran una a una sobre su propio
timestamp; el bloque completo cede el sitio al siguiente en 0.14 s. Un subtítulo no
hace una salida dramática.

**Anclado por abajo**, no por arriba: los bloques de 2, 3 y 4 líneas comparten línea
base a 22 cqh del borde inferior, así el subtítulo no salta de altura al cambiar de
longitud.

El único acento azul del tramo es la marca: **OneScreen** va teñida cada vez que se
pronuncia (tres veces). Ninguna otra palabra lleva color aquí — con 13 bloques
seguidos, acentuar por sentido convertiría la columna en ruido.

`handoff_in` / `handoff_out` — entra y sale a la izquierda, en la misma corriente.

## Frame 3 — Cierre (bloque negro)

- scene: La invitación, a cuadro completo sobre el negro final
- duration: 10.48s
- start: 62.92s
- frames: 262
- transition_in: cut-the-curve LEFT
- status: animated
- poster: 6s
- asset_candidates:
- assets_note: ninguno — lettering puro
- voiceover: "En OneScreen amamos contar historias y tú puedes ser una de esas historias. Esta puede ser tu historia. ¿Comenzamos? Solo tienes que tocar la pantalla."
- src: compositions/frames/03-cierre.html

Cuatro frases. **«¿Comenzamos?» es el único cuadro en `colossal`** de toda la pieza —
11 cqw, no 15 como en el manifiesto, porque a 15 cqw sus doce caracteres se salen del
ancho útil. Lleva debajo el filete azul que se dibuja por `scaleX`, el mismo gesto que
cerraba el manifiesto.

La última frase se retira sobre la cola del corte; no hay logotipo. El cierre de marca
lo pone el editor si lo quiere — no sé qué más va a haber en ese negro.

## Decisiones que quedaron fuera

- **Sin logotipo.** No se añadió el lockup de OneScreen a ningún cuadro: es una capa
  de superposición y no sé qué más lleva el negro final en el montaje.
- **Sin identificación de entrevistados.** Haría falta nombre, cargo e institución de
  los tres; solo se alcanza a leer «UNAM ACADÉMICO» en una bata.
- **El audio va incluido** en el MOV como guía de sincronía. Es el audio del propio
  corte: en Premiere se desvincula y se borra en dos clics, pero alinear la capa por
  forma de onda es inmediato.
