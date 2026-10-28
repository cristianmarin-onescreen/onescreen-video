---
version: alpha
name: OneScreen Lettering — Frame (video / frame layer)
description: >
  Sistema tipográfico para el film manifiesto de OneScreen. Adoptado del preset
  blue-professional y remezclado sobre los tokens de marca; la doctrina de composición
  fue reescrita a mano porque el preset asume tarjetas, píldoras y dashboards, y este
  film no tiene ninguna de las tres. La unidad es el cuadro 3840×2160. Los átomos son
  sagrados: blanco absoluto, tinta negra, un solo acento #3976ff, y Rubik en todo.
  La palabra ES la imagen.
unit: the frame — 3840×2160 (16:9 4K) primary
principle: una idea por cuadro · el acento marca sentido, nunca decora · el corte cae en la palabra

colors:
  bg: "#ffffff"
  primary: "#3976ff"
  text: "#000000"
  text-muted: "#7e7e82"
  text-light: "#c7c7cc"
  night: "#050507"
  night-text: "#ffffff"
  accent-light: "rgba(57, 118, 255, 0.08)"
  accent-medium: "rgba(57, 118, 255, 0.15)"
  border: "rgba(57, 118, 255, 0.2)"
  card-bg: "rgba(57, 118, 255, 0.04)"
  positive: "#059669"
  negative: "#dc2626"

radii:
  pill: "100px"
  card-lg: "14px"
  card-md: "12px"
  card-sm: "10px"
  bar: "6px"
  circle: "50%"

typography:
  # — rampa de lettering (Rubik en todos los niveles) —
  micro:   { fontFamily: "Rubik", cqw: 0.95, weight: 500, tracking: "0.22em", upper: true, color: "text-muted" }
  body:    { fontFamily: "Rubik", cqw: 1.9,  weight: 400, lineHeight: 1.5, color: "text-muted" }
  sub:     { fontFamily: "Rubik", cqw: 3.0,  weight: 500, lineHeight: 1.25, tracking: "-0.01em", color: "text" }
  phrase:  { fontFamily: "Rubik", cqw: 5.0,  weight: 500, lineHeight: 1.10, tracking: "-0.022em", color: "text" }
  display: { fontFamily: "Rubik", cqw: 7.6,  weight: 600, lineHeight: 1.02, tracking: "-0.030em", color: "text" }
  mega:    { fontFamily: "Rubik", cqw: 11.5, weight: 700, lineHeight: 0.96, tracking: "-0.038em", color: "text" }
  colossal:{ fontFamily: "Rubik", cqw: 16.0, weight: 800, lineHeight: 0.92, tracking: "-0.045em", color: "text" }
  # — alias que el preset original define; se conservan por compatibilidad —
  h1:      { fontFamily: "Rubik", cqw: 7.6,  weight: 600, lineHeight: 1.02, tracking: "-0.030em", color: "text" }
  h2:      { fontFamily: "Rubik", cqw: 5.0,  weight: 500, lineHeight: 1.10, tracking: "-0.022em", color: "text" }
  h3:      { fontFamily: "Rubik", cqw: 3.0,  weight: 500, lineHeight: 1.25, tracking: "-0.01em", color: "text" }

spacing:
  pad-x: "8cqw"
  pad-y: "8cqh"
  optical-lift: "-1.2cqh"
  line-gap: "0.10em"

components:
  word:
    description: "La unidad atómica. Un <span> por palabra, con overflow:hidden en su envoltura para el barrido de máscara. Nunca se anima la letra suelta."
  accent-word:
    color: "{colors.primary}"
    description: "La única palabra teñida de #3976ff en un verso — la que carga el sentido. Máximo una por cuadro; hay cuadros que no llevan ninguna."
  night-field:
    backgroundColor: "{colors.night}"
    description: "El bloque invertido. Campo de estrellas en CSS puro (radial-gradients estáticos, posiciones fijas, cero aleatoriedad). Aparece una sola vez en todo el film."
  wordmark:
    src: "assets/onescreen-wordmark.svg"
    color: "currentColor"
    description: "Logotipo oficial en vector, teñible por currentColor. Solo en el lockup de cierre."
  rule:
    backgroundColor: "{colors.primary}"
    size: "altura 0.28cqh"
    description: "Filete de acento. Se dibuja por scaleX desde el origen del texto, nunca aparece de golpe."
  touch-ring:
    borderColor: "{colors.primary}"
    description: "Anillo de toque del CTA final. Un solo pulso, no un loop."
---

# OneScreen Lettering — Frame (video / frame layer)

## Adaptación de marca (LEER PRIMERO — el frontmatter manda)

Adoptado de **blue-professional** y remezclado sobre `capture/extracted/tokens.json`
(canvas → `#ffffff`, acento → `#3976ff`, tinta → `#000000`, display y body → **Rubik**).

Dos correcciones a mano sobre la salida del remix, ambas necesarias:

1. **`text-muted` llegó como `#f4f6fa`** — un casi-blanco, invisible sobre fondo blanco.
   Reemplazado por `#8a8a8e`, un gris neutro que sostiene contraste AA a tamaños de lettering.
2. **La doctrina de composición del preset fue reescrita.** El preset original describe
   tarjetas teñidas, cromo de píldora, barras de progreso y un cuadro dashboard. Este film
   no tiene ninguno de esos elementos: es lettering puro. Los componentes heredados
   (`card-tinted`, `tag-pill`, `bar-track`, …) se retiraron del frontmatter y se
   reemplazaron por los seis que este film sí usa.

Lo que se conservó intacto del preset: la ley del contenedor, el piso de legibilidad,
la disciplina de **un solo acento**, y la regla de que los titulares nunca van teñidos.

## Overview

Un film de **una idea por cuadro**. El fondo es blanco absoluto y no se mueve nunca —
salvo un único bloque invertido a negro. La tinta es negra. El azul `#3976ff` existe para
una sola cosa: **marcar la palabra que carga el sentido del verso**. Si el azul aparece en
más de una palabra por cuadro, está decorando, y decorar está prohibido.

El dinamismo no viene de efectos. Viene de tres cosas, en este orden:

1. **Escala.** Un verso largo entra en `phrase`; la palabra que remata entra en `mega` o
   `colossal`. El salto de tamaño entre versos consecutivos es el corte.
2. **Ritmo.** Cada palabra aparece sobre su propio timestamp de locución. Nada aparece
   antes de que se diga, nada sobrevive mucho después.
3. **Vector.** La dirección con la que un cuadro sale determina cómo entra el siguiente.
   Un cuadro que salió hacia arriba entrega a uno que entra desde abajo.

**Referencia:** un anuncio de producto Apple con el audio de un manifiesto. El fracaso se
ve como una plantilla de citas motivacionales: texto centrado que hace fade-in, fondo con
degradado, y una palabra en cursiva.

## The Frame

- **Primario:** 3840×2160 (16:9), 24 fps. Todo el display se escribe en **`cqw`**
  (`px ÷ 3840 × 100 = cqw`), así que el sistema es independiente de la resolución.
- **La ley del contenedor:** el suelo de cada cuadro declara `container-type: size`;
  toda unidad relativa al cuadro es `cqw`/`cqh`, nunca `vw`.
- **Área segura:** `pad-x` 8cqw. El texto nunca toca el borde del cuadro.
- **Levante óptico:** un bloque centrado se sube `-1.2cqh` respecto al centro geométrico.
  El centro matemático se lee bajo; el ojo pide el texto un poco más arriba.
- **24 fps es una restricción, no un ajuste.** Todo corte cae en frontera de cuadro
  (múltiplos de 1/24 s = 0.041667 s). Un corte a mitad de cuadro produce medio frame de
  transición y se lee como error de render.

## Colors

`{colors.bg}` blanco es el suelo universal. `{colors.text}` negro es toda la tipografía
de peso. `{colors.primary}` es el **único** acento, y su regla es estricta:

- **Máximo una palabra teñida por cuadro.** Hay cuadros que no llevan ninguna — eso es
  correcto y deseable. El azul gana fuerza por escasez.
- **La palabra de acento puede estar en cualquier escalón**, incluido `colossal`. Aquí el
  azul no es cromo secundario: es el subrayado semántico del film, y en el clímax le toca
  el tamaño más grande. (Esta regla reemplaza el "nunca un titular teñido" que traía el
  preset original, escrito para láminas de consultoría, no para lettering.)
- **Nunca un verso completo en azul.** El acento es una palabra, no una frase.
- **Nunca como fondo**, salvo el propio filete `rule` y el anillo del CTA.

`{colors.night}` `#050507` es el suelo del único bloque invertido. Dentro de él la tinta
se invierte a `{colors.night-text}` blanco y el acento sigue siendo `#3976ff` — el azul es
la constante que atraviesa la inversión, y por eso el corte a negro no rompe la marca.

`{colors.text-muted}` gris queda para cromo y para versos deliberadamente secundarios.

## Typography

Una sola familia, **Rubik**, en siete escalones. La familia no cambia nunca; lo que cambia
es peso y tamaño.

| Escalón    | cqw  | Peso | Uso                                                        |
| ---------- | ---- | ---- | ---------------------------------------------------------- |
| `micro`    | 0.95 | 500  | Cromo en versalitas. Casi no se usa.                       |
| `body`     | 1.9  | 400  | Texto de apoyo.                                            |
| `sub`      | 3.0  | 500  | Verso secundario que acompaña a uno mayor.                 |
| `phrase`   | 5.0  | 500  | El verso largo — la mayoría del guion vive aquí.           |
| `display`  | 7.6  | 600  | El verso que sube el tono.                                 |
| `mega`     | 11.5 | 700  | La palabra que remata. Una o dos palabras, nunca una frase.|
| `colossal` | 16.0 | 800  | El golpe. Se usa **dos veces en todo el film**.            |

Reglas duras:

- **Tracking negativo crece con el tamaño.** A 16cqw, Rubik sin `-0.045em` se lee suelto.
- **Interlineado se cierra con el tamaño.** `phrase` 1.10 → `colossal` 0.92.
- **Piso de legibilidad:** cualquier línea que carga sentido ≥ **3.0cqw**.
- **Ajuste a la medida:** ≤2 palabras → `mega`/`colossal`; 3–5 → `display`; 6+ → `phrase`.
  Un bloque de texto nunca pasa de **80cqw** de ancho.
- **Sin cursiva. Sin versalitas en versos. Sin subrayado. Sin sombra de texto.**
- **Sin sustitutos de fuente.** Rubik se embebe local en el proyecto; si no carga, el
  render se detiene, no cae a system-ui.

## Depth & Surface

No hay profundidad. No hay sombras, ni degradados, ni bordes, ni tarjetas, ni blur salvo
el blur direccional de un corte en movimiento. El plano es plano. La única excepción en
todo el film es el campo estelar del bloque nocturno, y ahí el "relieve" son puntos de
1–3 px a opacidades entre 0.15 y 0.7 — sin animación de parpadeo.

**Techo:** cero `box-shadow`. Cero `border-radius` en tipografía. Cero degradados sobre
blanco.

## Frame Treatments

> Receta: suelo · compone · foco · acento · silencio · densidad.

### 1 · Verso (el cuadro base del film)

**Suelo** blanco. **Compone** una o dos líneas en `phrase`/`display`, centradas, con levante
óptico. **Foco** la línea completa; el ojo la lee de una. **Acento** como mucho una palabra
en `#3976ff`. **Silencio** ≥ 55% del cuadro. **Densidad** baja.

### 2 · Golpe (la palabra que remata)

**Suelo** blanco. **Compone** una o dos palabras en `mega`/`colossal`. **Foco** absoluto —
no hay nada más en el cuadro. **Acento** opcional, y solo si el verso anterior no lo tuvo.
**Silencio** ~65%. **Densidad** mínima.

### 3 · Noche (aparece una sola vez)

**Suelo** `{colors.night}` con campo estelar CSS estático. **Compone** un verso en `display`
blanco. **Foco** el texto blanco sobre negro. **Acento** una palabra en `#3976ff`, que aquí
brilla más que en ningún otro cuadro. **Silencio** ~70%. **Densidad** mínima.

### 4 · Enumeración (las tres pruebas)

**Suelo** blanco. **Compone** tres versos en `sub`/`phrase` que se acumulan, uno por
timestamp, alineados a un mismo eje izquierdo. **Foco** el verso que acaba de entrar; los
anteriores bajan a `text-muted`. **Acento** una palabra por verso, y solo en el tercero.
**Silencio** moderado. **Densidad** media — es el cuadro más denso del film.

### 5 · Lockup (el cierre de marca)

**Suelo** blanco. **Compone** el `wordmark` en vector, negro, centrado, con el filete `rule`
azul debajo, y dos líneas en `phrase` bajo el filete. **Foco** el logotipo. **Acento** el
filete y la segunda ocurrencia de "futuro". **Silencio** ~60%. **Densidad** baja.

### 6 · Toque (el CTA físico)

**Suelo** blanco. **Compone** un verso en `display` y el `touch-ring`. **Foco** el punto de
contacto. **Acento** el anillo. **Silencio** ~65%. **Densidad** mínima.

## Composition Rules

### Do

- Empezar cada cuadro en **blanco absoluto**; dejar que el negro cargue el peso.
- Reservar `#3976ff` para **una palabra por cuadro**, la que sostiene la idea.
- Sincronizar cada aparición con el **timestamp real** de su palabra en la locución.
- Cerrar el interlineado y el tracking a medida que sube la escala.
- Cortar en frontera de cuadro a 24 fps.
- Dejar que el cuadro **respire después** del golpe: el silencio posterior es parte del golpe.

### Don't

- No teñir un verso completo de azul. No hay segundo color de acento.
- No usar fade-in genérico como transición por defecto — el texto entra por máscara,
  desplazamiento o escala, con una razón por cuadro.
- No dejar texto en pantalla mucho después de que la voz pasó de largo.
- No animar letra por letra: **la unidad de animación es la palabra**.
- No introducir imágenes, mockups, fotos de stock ni degradados decorativos.
- No poner el logotipo antes del cierre. Aparece una vez, y por eso pesa.
- No usar movimiento inactivo (flotar, respirar, pulsar en loop). Si algo se mueve, avanza.

## Aspect-Ratio Behavior

Este film se autoriza **solo en 16:9 a 3840×2160**. No hay corte vertical ni cuadrado
aprobado: el lettering está dimensionado para el ancho, y a 9:16 los versos largos
romperían el piso de 3.0cqw. Si más adelante se pide vertical, se re-escalona la rampa
completa, no se reencuadra.

## Approved Entities

El único logotipo aprobado es `assets/onescreen-wordmark.svg` (marca oficial de OneScreen,
vector, incluye ®). No hay clientes, aliados ni marcas de terceros en este film.

## Numerals & Claims (hard rule)

Este guion no contiene cifras, y no se le agrega ninguna. Nada de "+40% de atención" ni
métricas inventadas. El texto en pantalla sale **palabra por palabra del guion aprobado**;
no se parafrasea, no se resume, no se agrega copy que la voz no diga.

## Pre-Render Self-Audit

- **Ortografía** — cada palabra en pantalla coincide con `user_script.txt`, tildes incluidas.
- **Sincronía** — cada aparición cae sobre su timestamp en `transcript/words.json`.
- **Acento** — ningún cuadro tiene dos palabras azules.
- **Escala** — `colossal` aparece exactamente dos veces en todo el film.
- **Tipo** — Rubik en el 100% del texto; ningún fallback de sistema en el render.
- **Plano** — cero sombras, cero degradados sobre blanco, cero bordes decorativos.
- **Rejilla de tiempo** — todo inicio y duración es múltiplo de 1/24 s.
- **Cola** — el film cierra en 43.08 s, con la voz terminando en 41.84 s.

## Known Gaps

- **La animación está fuera de alcance aquí.** `frame.md` fija marca y composición; el
  movimiento vive en `STORYBOARD.md` y en las reglas de `/hyperframes-animation`.
- **Rubik se embebe local** como woff2 en el proyecto. No se sirve desde Google Fonts:
  el render debe ser determinista y sin red.
- El campo estelar del cuadro nocturno es CSS estático y **no puede usar `Math.random()`**;
  las posiciones se escriben a mano.
