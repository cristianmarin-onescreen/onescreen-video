---
format: 3840x2160
fps: 25
duration: 81.36s
mode: collaborative
message: "El ecosistema de IA de OneScreen cubre antes, durante y después de la clase"
arc: Lo que importa por dentro → La meta → Tres momentos → Lessn · Scrybe · QuizWiz · SuprNotes → Invitación
audience: Docentes e instituciones
music: none
---

# OneScreen — Ecosistema de software (capa de lettering)

Capa de superposición para `Apoyo/SC07 - Software/Software - Narrador.wav`.
ProRes 4444 con alfa, 25 fps, 2034 frames. **La pieza más larga del proyecto.**

| Variante | Tinta | Acento |
| --- | --- | --- |
| `-alfa-negro.mov` | negra | `#3976ff` |
| `-alfa-blanco.mov` | blanca | **blanco** — sin azul |

## Dos modos en una misma pieza

La pieza cambia de registro a la mitad, porque la mitad se monta sobre otra cosa.

| Tramo | Cuadros | Modo |
| --- | --- | --- |
| Apertura y promesa | f01 – f07 | **pantalla completa** — lettering centrado |
| Recorrido de producto | f08 – f24b | **subtítulo en tercio inferior** |
| Cierre | f25 – f27 | **pantalla completa** |

El tramo de producto va encima de **pantallazos del software**. Ahí el lettering
centrado taparía justo lo que hay que mirar, así que el texto se comporta como
subtítulo: bloque anclado abajo —todos terminan en el 87 % de altura— y medida de
80 cqw. Ningún bloque sube por encima del 65 % de altura; el más alto es f14b
(«a más de / 28 IDIOMAS / con subtítulos en la pantalla»), a 64.8 %.

En ese modo el rango de cuerpos es **casi plano: 2.9 a 3.9 cqw, apenas 1.3×**. El
énfasis lo llevan el peso y el color, no el tamaño. Las versalitas se desactivan salvo
en el escalón de remate («28 IDIOMAS», «CHATBOT»): una línea larga de subtítulo en caja
alta se vuelve un grito y cuesta leerla. El movimiento también baja: la palabra entra
con 20 px de recorrido en vez de 62, y la salida es casi un encadenado —26 px— en lugar
del barrido de 170 px del modo a pantalla completa, que repetido cada pocos segundos
sobre una interfaz marea.

## El contraste de tamaños, más corto

El escalón tipográfico iba de 3.0 a 12.5 cqw — un factor de **4.2×** entre la línea más
pequeña y la más grande, y el salto resultaba brusco. Ahora va de **3.4 a 9.6 cqw
(2.8×)**, corregido por los dos extremos a la vez: sube el piso y baja el techo. La
jerarquía se sostiene igual porque la llevan el peso y el color, que no dependen del
tamaño.

| Escalón | Antes | Ahora |
| --- | --- | --- |
| sub | 3.0 cqw | **3.4** |
| phrase | 5.0 | **5.2** |
| display | 7.0 | **6.4** |
| mega | 10.0 | **8.2** |
| colossal | 12.5 | **9.6** |

Efecto colateral bueno: con el techo más bajo **ninguna línea desborda ya la caja**, así
que `tools/fit-lines.py` no tiene que reducir ningún cuerpo (`fit.json` queda vacío).

## Cuadros partidos

Cinco cuadros llegaban a **cinco filas de texto a la vez** — eso ya no es un subtítulo, y
empujaba el bloque hasta el 57 % de altura. Se partieron en dos, siempre por la frontera
de la cláusula (la coma, la conjunción), nunca por número de palabras:

| Original | Se parte en | Corte |
| --- | --- | --- |
| f10 | f10 + f10b | tras «…seleccionar un tema,» |
| f14 | f14 + f14b | tras «…traducir en tiempo real» |
| f18 | f18 + f18b | tras «…fuentes que sí confíes,» |
| f23 | f23 + f23b | antes de «y prepararse con…» |
| f24 | f24 + f24b | tras «SuprNotes crea un CHATBOT» |

Los tiempos se recalculan solos: cada cuadro arranca en la primera palabra que le toca.
La pieza pasa de 27 a **32 cuadros** sin que cambie un solo fotograma de duración.

## Los cuatro iconos de producto

Cada vez que se nombra un software aparece **su icono oficial** junto al lockup, y el
lockup sigue el patrón de siempre: «OneScreen» en Nevis a −0.050em, el nombre del
producto en Rubik caja mixta y peso regular.

| Cuadro | Entra | Producto | Icono |
| --- | --- | --- | --- |
| f09 | 26.32 | **Lessn** | página con engranaje |
| f13 | 38.56 | **Scrybe** | micrófono |
| f17 | 51.40 | **QuizWiz** | lupa |
| f22 | 66.56 | **SuprNotes** | libro con play |

Como estos cuatro cuadros caen dentro del tramo de subtítulo, el icono **ya no va
apilado encima del nombre sino en la misma fila**, como una chapa identificadora:
apilados, el bloque quedaba demasiado alto para caber en el tercio inferior. Por lo
mismo «OneScreen» y el nombre del producto comparten ahora una sola línea.

Los archivos salen de tu propia carpeta de marca — `Material de marca/Logotipo -
OneScreen <producto>.png`, 1500×1500 con alfa. **Los cuatro traen su propio fondo
morado con esquinas redondeadas**, así que el mismo archivo sirve para la variante de
tinta negra y para la blanca: no dependen del color del texto que los rodea. Eso
también significa que el morado entra en la paleta de esta pieza — es el color de los
iconos de app, no una decisión mía.

El icono entra **0.02 s antes que el nombre** y con un ligero *scale-in* desde 0.86:
primero se reconoce la marca, después se lee. Y llega, no aparece.

## La grafía de los cuatro nombres

Whisper parte las marcas en dos tokens («One» + «Screen») y transcribe los nombres
fonéticamente: **Lesson**, **Scribe**, **Super Notes**. Los corregí a la grafía oficial
—**Lessn**, **Scrybe**, **QuizWiz**, **SuprNotes**— contra los nombres de archivo de tu
carpeta de marca. Es el mismo tipo de verificación que hice con «Wandr».

## Tres cosas del audio que tu guion no trae

**1 · «con subtítulos en la pantalla».** La voz añade esa frase después de «28 idiomas»
y tu guion no la tiene. La conservé; va en el cuadro 14.

**2 · La voz dice «traducir en tiempo real», no «traducir tu clase en tiempo real».**
Manda la voz.

**3 · Los números van como cifra, no como palabra.** «5 horas», «5 minutos»,
«3 momentos», «28 idiomas». En lettering una cifra pega más que la palabra escrita, y
es coherente con las otras piezas —65”, 110”, 4 millones, 6 billones—.

## Sobre la insignia verde de Gurú

Entre las imágenes que adjuntaste venía el badge verde de **Gurú**, que no es uno de los
cuatro softwares de esta pieza. No lo usé aquí. Si querías que apareciera en algún
cuadro, dime en cuál.

## Frame 1 — Capa completa

- scene: 32 cuadros — 10 a pantalla completa y 22 en subtítulo de tercio inferior, sobre suelo transparente
- duration: 81.36s
- start: 0.000s
- frames: 2034
- transition_in: cut
- status: animated
- poster: 26.9s
- asset_candidates:
- assets_note: assets/icons/{lessn,scrybe,quizwiz,suprnotes}.png — logotipos oficiales de marca
- voiceover: "Sin embargo, lo que verdaderamente importa es lo que está por dentro… tenemos OneScreen Lessn… te acompaña OneScreen Scrybe… OneScreen QuizWiz… OneScreen SuprNotes."
- src: compositions/frames/software.html
