---
format: 3840x2160
fps: 25
duration: 19.28s
mode: collaborative
message: "Las VirtualWalls son el formato gigante de OneScreen"
arc: Grande → Gigante → El producto → Medidas → Invitación
audience: Espacios que necesitan gran formato
music: none
---

# OneScreen — VirtualWalls / LED (capa de lettering)

Capa de superposición para `Apoyo/SC06/LED_1.wav`. ProRes 4444 con alfa, 25 fps,
482 frames.

| Variante | Tinta | Acento |
| --- | --- | --- |
| `-alfa-negro.mov` | negra | `#3976ff` |
| `-alfa-blanco.mov` | blanca | **blanco** — sin azul |

## Dos particularidades de esta pieza

**La marca va DETRÁS del modelo.** El guion dice «las VirtualWalls de OneScreen», no
«OneScreen VirtualWalls». Así que aquí «OneScreen» no ocupa línea propia como en Core,
T7 o Titan: aparece **en línea** dentro de la frase «de OneScreen.», compuesta en Nevis
dentro de una línea Rubik. El generador ya soportaba ese caso.

**Las versalitas de «MUY GRANDE» y «GIGANTE» son tuyas, no mías.** Tu guion las escribe
en caja alta, y lo leí como instrucción de énfasis. Van en el escalón `colossal`.

## Los 9 cuadros

| Cuadro | Entra | Contenido |
| --- | --- | --- |
| f01 | 0.00 | Vamos a hablar ahora sobre algo / **GRANDE.** |
| f02 | 2.48 | Algo / **MUY GRANDE** |
| f03 | 3.96 | Hay espacios que necesitan un formato / **GIGANTE.** |
| f04 | 7.00 | Estas son las / **VirtualWalls** / de **OneScreen.** |
| f05 | 9.08 | DESDE / **108” hasta 217”** |
| f06 | 12.44 | Imagen en / **4K.** |
| f07 | 13.88 | Cuando tu idea es grande, / **TU PANTALLA TAMBIÉN.** |
| f08 | 16.36 | ¿Quieres saber más de nuestras / **LED?** |
| f09 | 18.04 | Solo toca / **ESTA PANTALLA.** |

## Dos cosas del audio que conviene que sepas

**La última línea de tu guion no está en la locución.** «Ahora, sobre esta» no se
pronuncia: la voz termina en «Solo toca esta pantalla.» a los 18.96 s. No se letró,
porque el lettering sigue a la voz. Si esa línea debe existir, hace falta grabarla.

**El último cuadro no lleva fundido de salida.** La cola es de 0.64 s desde la última
palabra, y un fundido de 0.6 s arrancaría casi encima de ella: el texto daría un
parpadeo en vez de retirarse. Se sostiene hasta el último frame y el corte lo das tú en
el montaje. El generador ahora decide esto solo — solo programa la salida si cabe.

## Frame 1 — Capa completa

- scene: 9 cuadros de gran formato sobre suelo transparente
- duration: 19.28s
- start: 0.000s
- frames: 482
- transition_in: cut
- status: animated
- poster: 10.5s
- asset_candidates:
- assets_note: ninguno — lettering puro
- voiceover: "Vamos a hablar ahora sobre algo grande. Algo muy grande… Estas son las VirtualWalls de OneScreen. Desde 108” hasta 217”… Solo toca esta pantalla."
- src: compositions/frames/virtualwalls.html
