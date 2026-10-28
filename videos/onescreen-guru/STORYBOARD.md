---
format: 3840x2160
fps: 25
duration: 27.04s
mode: collaborative
message: "Gurú es un ingeniero de OneScreen a un click, solo para tu institución"
arc: Problema → La respuesta → El servicio → Cómo se usa → Invitación
audience: Instituciones preocupadas por el soporte post-venta
music: none
---

# OneScreen — Gurú (capa de lettering)

Capa de superposición para `Apoyo/SC08 - Gurú/Gurú - Final.wav`. ProRes 4444 con alfa,
25 fps, 676 frames.

| Variante | Tinta | Acento |
| --- | --- | --- |
| `-alfa-negro.mov` | negra | `#3976ff` |
| `-alfa-blanco.mov` | blanca | **blanco** — sin azul |

**Cuatro menciones de marca**, las más de las diez piezas: f02, f04, f05 y f06. Todas en
Nevis a −0.050em; «Gurú» y todo lo demás en Rubik, con el nombre del servicio en caja
mixta y peso regular en el lockup.

## El caso que estrena esta pieza

En f06 la marca cae **dentro de una línea que no está en versalitas**, y en f05 dentro
de una línea que sí lo está. El guard `text-transform: none !important` de la clase
`.brand` es lo que impide que el wordmark salga como «ONESCREEN» — una marca en caja
alta deja de ser la marca. Es la primera vez en las diez piezas que ese guard hace
trabajo real, y funciona.

## Los 9 cuadros

| Cuadro | Entra | Contenido |
| --- | --- | --- |
| f01 | 0.00 | Cuando todo falla, / **NECESITAS ALGO CONFIABLE.** |
| f02 | 2.68 | Es por eso que en **OneScreen** te daremos un / **INGENIERO ESPECIALIZADO** / solo para tu institución |
| f03 | 7.72 | DISPONIBLE / **24/5.** |
| f04 | 9.68 | Te presentamos / **OneScreen** / Gurú. |
| f05 | 11.44 | Todos los productos **OneScreen** tienen / **EL BOTÓN VERDE GURÚ,** |
| f06 | 14.44 | donde podrás acceder a un solo click, / **CON UN INGENIERO** / de **OneScreen** listo para ayudarte |
| f07 | 19.20 | Puedes agendar / **CAPACITACIONES** / o solicitar soporte técnico |
| f08 | 22.64 | Probar cómo funciona es / **BASTANTE SENCILLO.** |
| f09 | 25.20 | Solo tienes que tocar / **ESTA PANTALLA.** |

## Tres decisiones que conviene que revises

**«El botón verde Gurú» va en la paleta del sistema, no en verde.** Podría teñir esa
palabra de verde para que sea literal, pero rompería dos cosas: el sistema de dos
colores que sostiene las diez piezas, y sobre todo la variante blanca, que va toda
blanca a propósito porque el montaje usa fondos azules. Si quieres el verde literal
solo en la variante negra, dímelo y lo hago — pero entonces las dos variantes dejan de
ser la misma pieza en dos tintas.

**«24/5» usa la barra de tu guion.** La locución dice «veinticuatro cinco» y la
transcripción lo oyó como «24-5»; la barra es la forma correcta y la que escribiste.

**La voz dice «a UN SOLO click» y tu guion escribe «a SOLO UN click».** Manda la voz,
como en todas las piezas.

## Frame 1 — Capa completa

- scene: 9 cuadros sobre suelo transparente
- duration: 27.04s
- start: 0.000s
- frames: 676
- transition_in: cut
- status: animated
- poster: 10.5s
- asset_candidates:
- assets_note: ninguno — lettering puro
- voiceover: "Cuando todo falla, necesitas algo confiable… Te presentamos, OneScreen Gurú… Solo tienes que tocar esta pantalla."
- src: compositions/frames/guru.html
