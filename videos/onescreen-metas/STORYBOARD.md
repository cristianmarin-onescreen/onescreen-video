---
format: 3840x2160
fps: 25
duration: 58.28s
mode: collaborative
message: "Cinco metas, y la quinta es que lo veas tú mismo"
arc: Promesa → 5 metas numeradas → Invitación
audience: Decisores de educación y empresa en LATAM
music: none
---

# OneScreen — Nuestras metas (capa de lettering)

Capa de superposición para `SC03.wav`. Suelo transparente, ProRes 4444, dos tintas:
`-alfa-negro.mov` y `-alfa-blanco.mov`. **Sin gris.**

**25 fps**, como SC01 y SC02, para que entre directo en la timeline sin conformado.

## Este usa TU estilo, no el mío

Leído de tus montajes SC01 y SC02, y aplicado aquí:

| Recurso | Cómo se aplica |
| --- | --- |
| **Versalitas en la palabra héroe** | Los cinco temas van en caja alta. Mi spec del manifiesto las prohibía; estaba equivocado. |
| **Tres escalas por cuadro** | El ordinal en `sub`, el conector en `sub`/`display`, el tema en `mega`. Salto de 3.3× entre extremos. |
| **Pesos mezclados** | El conector va en 500, la carga en 600–800. |
| **El azul como hilo** | Los cinco ordinales — PRIMERO, SEGUNDO, TERCERO, CUARTO, Y QUINTO — van en `#3976ff`. Es lo único azul de la pieza junto a dos remates. |

Detalle técnico que cambió con las versalitas: en caja alta el tracking va **abierto**,
no negativo. Un `letter-spacing` cerrado junta las astas verticales y la palabra se
emplasta. El ordinal en `sub` lleva `0.16em`.

## Estructura — 24 cuadros, 5 capítulos

| | Cuadro | Entra | Texto |
| --- | --- | --- | --- |
| | i1–i3 | 0.00 | Ya te contamos nuestra historia · Ahora te contaremos nuestras metas · ¿ESTÁS LISTO? |
| ▌ | h1 | 5.80 | **PRIMERO** / AULAS INTERACTIVAS |
| | c1a–c1b | 7.80 | nativos digitales · pizarras infinitas · simuladores |
| ▌ | h2 | 13.24 | **SEGUNDO** / SALAS DE REUNIONES |
| | c2a–c2c | 14.96 | cuatro dispositivos en uno · imagen y sonido · equipo unido |
| ▌ | h3 | 23.08 | **TERCERO** / INTELIGENCIA ARTIFICIAL |
| | c3a–c3e | 24.88 | cinco horas → CINCO MINUTOS · clases · idiomas · evaluaciones |
| ▌ | h4 | 33.68 | **CUARTO** / un formato / GRAAAAAANDE. |
| | c4a–c4d | 35.88 | grandes ideas · verse EN GRANDE · LED · **108" hasta 217"** |
| ▌ | h5 | 48.12 | **Y QUINTO** / LA MÁS IMPORTANTE |
| | c5a–c5b | 49.72 | que tú lo veas · SOLO TIENES QUE TOCAR **LA PANTALLA** |

Tres remates se llevan tratamiento propio: **CINCO MINUTOS** en azul (es la promesa
concreta del capítulo 3), **GRAAAAAANDE.** en el escalón mayor con las aes de tu guion
intactas, y **108" hasta 217"** en `colossal` porque la cifra es el argumento.

La voz termina en 53.6 s y el archivo dura 58.28 s: quedan 4.7 s de cola en los que la
capa ya está vacía, para que puedas rematar con lo que quieras.

## Frame 1 — Capa completa

- scene: Los 24 cuadros de lettering, encadenados sobre suelo transparente
- duration: 58.28s
- start: 0.000s
- frames: 1457
- transition_in: cut
- status: animated
- poster: 34s
- asset_candidates:
- assets_note: ninguno — lettering puro; el metraje lo pone el editor debajo
- voiceover: "Ya te contamos nuestra historia. Ahora te contaremos nuestras metas. ¿Estás listo? Primero, aulas interactivas… Y quinto, la más importante: que tú lo veas con tus propios ojos. Solo tienes que tocar la pantalla."
- src: compositions/frames/metas.html

Una sola composición y no seis. Esta pieza no tiene cortes de plano propios — es una
capa continua —, así que no hay costuras que gobernar: los 24 cuadros se relevan entre
sí dentro de la misma escena, cada uno cediendo el sitio 0.06 s antes de que entre el
siguiente.

## Dos cosas que decidí y conviene que revises

**«LED» está escrito pero puede que no se diga.** Tu guion dice «Pantallas LED de gran
formato». Transcribí ese tramo dos veces: con el guion como prompt aparece «LED», sin
prompt no aparece. Eso es sesgo del prompt, no detección — lo más probable es que la
voz no lo diga. Lo escribí porque es tu guion y tu claim de producto, pero si prefieres
que el texto siga exactamente a la voz, se quita borrando una línea en
`transcript/build-beats.mjs` (`INSERT_AFTER`).

**Tres palabras que la voz dice y tu guion no.** «en» (aunque estén **en** diferentes
partes), «solo» (ahora **solo** le toma) e «Y» (**Y** quinto). Las conservé para que el
texto siga a la voz. Si prefieres el guion literal, están en el mismo archivo.
