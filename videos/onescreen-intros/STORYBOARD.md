---
format: 3840x2160
fps: 25
duration: 21.6s (las cuatro seguidas; se entregan sueltas)
mode: collaborative
message: "Cuatro tarjetas de presentación de producto, una por software"
arc: Conoce → el producto → qué hace
audience: Docentes e instituciones
music: none
---

# OneScreen — Tarjetas de intro (Lessn · Scrybe · QuizWiz · SuprNotes)

Cuatro tarjetas de presentación, **diseñadas para fondo blanco**, sin locución.
ProRes 4444 con alfa, 25 fps.

| Variante | Tinta | Acento |
| --- | --- | --- |
| `-alfa-negro.mov` | negra | `#3976ff` en el antetítulo |
| `-alfa-blanco.mov` | blanca | **blanco** — sin azul |

Se entregan **como ocho clips sueltos**, no como una pieza continua: cada tarjeta
precede a la sección de su producto, así que juntarlas en un solo archivo obligaría a
cortarlas otra vez en el montaje. Si quieres además el rollo continuo de 21.6 s, se
saca sin volver a diseñar nada.

## El ritmo: de dónde salen las duraciones

No hay voz que marque el paso, así que el tiempo de cada tarjeta **se deriva de un
modelo de lectura explícito** (en `tools/build-cards.mjs`, constante `READING`), no de
una estimación a ojo:

| Constante | Valor | Qué paga |
| --- | --- | --- |
| `WPS` | 2.7 palabras/s | Velocidad de lectura en pantalla. El rango cómodo de los estándares de subtitulado (≈160 ppm) bajado un punto, porque aquí además hay que leer un nombre de marca desconocido. |
| `ACQUIRE` | 0.62 s | El ojo encuentra la tarjeta y el icono aterriza **antes** de que haya nada que leer. |
| `LINEBRK` | 0.30 s | Cada salto de línea cuesta una sacada extra. |
| `HOLD` | 1.00 s | Reposo tras la última palabra. Una tarjeta que corta en la última sílaba se siente arrebatada aunque el tiempo de lectura fuera suficiente. |
| `FADE` | 0.50 s | El fundido de salida, que ya no es tiempo de lectura. |

Cambiar el ritmo es cambiar un número: si las quieres más rápidas, sube `WPS`; si las
quieres más reposadas, sube `HOLD`. Las cuatro duraciones se recalculan solas.

| Tarjeta | Producto | Descriptor | Palabras | Duración | Frames |
| --- | --- | --- | --- | --- | --- |
| c01 | **Lessn** | Crea presentaciones en segundos | 4 | 4.60 s | 115 |
| c02 | **Scrybe** | Graba, traduce y transcribe / tus reuniones | 6 | 5.64 s | 141 |
| c03 | **QuizWiz** | Crea evaluaciones en segundos | 4 | 4.60 s | 115 |
| c04 | **SuprNotes** | Un entorno de estudio / hecho solo con tus fuentes | 9 | 6.76 s | 169 |

Las tarjetas **no duran lo mismo a propósito**: duran lo que cuesta leerlas. Igualarlas
castigaría a SuprNotes o dejaría a Lessn y QuizWiz esperando en pantalla sin motivo.

## El orden en que se arma la tarjeta

1. **El icono aterriza** en t=0, con un *scale-in* desde 0.86. Primero se reconoce la
   marca, después se lee.
2. **«CONOCE»** a los 0.30 s — el antetítulo, en versalitas tracadas.
3. **El nombre** a los 0.62 s, en cascada palabra a palabra.
4. **El descriptor**, tras un respiro de 0.25 s.
5. **Reposo** y fundido limpio de 0.5 s.

La salida es un fundido sin desplazamiento. Cada tarjeta es un clip suelto y el corte lo
das tú en el montaje; un barrido de salida solo estorbaría al empalmar.

## Tipografía y marca

Se hereda la calibración de las piezas anteriores. **«OneScreen» va en Nevis a
−0.050em**; el nombre del producto y todo lo demás en Rubik, caja mixta y peso regular
—como quedó definido en la corrección de la Core—.

| Elemento | Cuerpo | Peso |
| --- | --- | --- |
| Antetítulo «CONOCE» | 3.0 cqw | 600, versalitas, tracking 0.16em |
| Nombre del producto | 7.2 cqw | 400 |
| Descriptor | 4.4 cqw | 400 |

El descriptor va en **regular, no en 500**: a 500 pesaba casi tanto como el nombre —que
también va en regular— y los dos competían. El nombre debe ganar por tamaño, no a
empujones. Por lo mismo lleva 2.5 cqh de aire encima: pegado, se leía como una segunda
línea del lockup en vez de como un descriptor.

El contraste entre el cuerpo más pequeño y el más grande es de **2.4×**, dentro del
rango corto que fijamos para las últimas piezas.

**El acento vive solo en «CONOCE».** No se tiñe el nombre: el wordmark de OneScreen es
negro o blanco, nunca azul, y teñirlo dejaría de ser el logotipo. En la variante blanca
no hay acento — todo blanco, como en las demás piezas.

## Los iconos

Los cuatro logotipos salen de tu carpeta de marca, los mismos que ya usamos en la pieza
de Software. **Traen su propio mosaico morado**, así que el mismo archivo sirve para la
tinta negra y para la blanca: no dependen del color del texto. Sobre fondo blanco el
morado funciona bien; es el mismo aviso de siempre para fondos azules.

## Frame 1 — Capa completa

- scene: 4 tarjetas de producto a pantalla completa, sobre suelo transparente
- duration: 21.6s
- start: 0.000s
- frames: 540
- transition_in: cut
- status: animated
- poster: 2.0s
- asset_candidates:
- assets_note: assets/icons/{lessn,scrybe,quizwiz,suprnotes}.png — logotipos oficiales de marca
- voiceover: none
- src: compositions/frames/intros.html
