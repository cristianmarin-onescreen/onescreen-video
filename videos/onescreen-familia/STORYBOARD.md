---
format: 3840x2160
fps: 25
duration: 46.88s
mode: collaborative
message: "OneScreen Core: cuatro modelos, un propósito, y este es el primero"
arc: Familia → El modelo → Tamaño → Software → Uso → Hardware → Lockup
audience: Instituciones educativas en crecimiento
music: none
---

# OneScreen — La familia · Core (capa de lettering)

Capa de superposición para `SC04.wav`. ProRes 4444 con alfa, 25 fps.

| Variante | Tinta | Acento |
| --- | --- | --- |
| `-alfa-negro.mov` | negra | `#3976ff` |
| `-alfa-blanco.mov` | blanca | **blanco** — sin azul |

La variante blanca va **toda blanca** por instrucción: el montaje usa fondos azules y
un acento `#3976ff` sobre azul desaparece.

## La regla de marca

**«OneScreen» se compone en Nevis. Todo lo demás en Rubik**, incluido el modelo
(«Core»). Son cuatro menciones en la pieza: cuadros 2, 3, 8 y 24.

El tracking de Nevis es **−0.050em**, y no es una estimación. Se midió contra el
logotipo vectorial oficial: se rasterizó el wordmark a 3000 px, se recortó su tinta,
se descartó el ® y se comparó su relación ancho/alto (6.3523) con la de «OneScreen»
compuesto en Nevis a distintos trackings. El barrido de −0.120em a +0.060em da el
mínimo error en −0.050em (6.3435). Superpuestas a igual altura de caja, la desviación
de ancho es del **0.19 %** — es decir, el logotipo *es* Nevis Bold a ese tracking.

Dos consecuencias técnicas que quedaron resueltas:

- **Nevis se declara cubriendo `font-weight: 100 900`.** Es una sola tipografía Bold;
  si se declarara solo en 700, el navegador sintetizaría negrita encima al pedirle 800
  en los escalones grandes, engordaría los trazos y dejaría de coincidir con el
  logotipo. Con `font-synthesis: none` además de la declaración amplia, no hay riesgo.
- **Nevis tiene la caja alta más corta que Rubik** al mismo cuerpo, así que la marca
  lleva `font-size: 1.12em` dentro de su escalón para pesar lo mismo que una línea
  Rubik equivalente.
- **La marca nunca va en versalitas.** El wordmark es caja mixta; forzarlo a caja alta
  deja de ser la marca. La regla está blindada con `text-transform: none !important`.

## Frame 1 — Capa completa

- scene: 24 cuadros de lettering estilo producto, sobre suelo transparente
- duration: 46.88s
- start: 0.000s
- frames: 1172
- transition_in: cut
- status: animated
- poster: 13.4s
- asset_candidates:
- assets_note: ninguno — lettering puro; el metraje lo pone el editor debajo
- voiceover: "Conoce la familia OneScreen… OneScreen Core, para instituciones en crecimiento. Disponible desde 65” a 110”… Android 16 certificado Google EDLA… Paso 1, encenderla. Paso 2, usarla."
- src: compositions/frames/familia.html

Una sola composición: la pieza no tiene cortes de plano propios, es una capa continua.
Los 24 cuadros se relevan entre sí, cada uno cediendo el sitio 0.06 s antes de que
entre el siguiente.

## Los cuadros que cargan la pieza

- **f08 — el cuadro producto.** «OneScreen» en Nevis a `colossal`, «CORE» debajo en
  Rubik versalitas y en azul. Es el único sitio donde marca y modelo comparten cuadro,
  y por eso es donde la regla tipográfica se ve.
- **f10 — las medidas.** «DISPONIBLE DESDE» pequeño en versalitas, `65” a 110”` en
  `colossal`. Las comillas son las tipográficas de tu guion (”), no la recta.
- **f13 — los 4 millones.** Tres escalas en un cuadro: «O sea, más de» pequeño,
  **4 MILLONES** enorme, «de aplicaciones.» pequeño otra vez.
- **f17 / f18 — los dos pasos.** «PASO 1.» y «PASO 2.» en azul, la acción debajo en
  `display`. Es la broma del guion y necesita ese ritmo binario.
- **f24 — el lockup de cierre.** «OneScreen» en Nevis, «CORE.» en Rubik, y la frase de
  cierre pequeña debajo.

La voz termina en 44.0 s y el archivo dura 46.88 s: quedan casi 3 s de cola con la
capa retirándose.
