---
format: 3840x2160
fps: 24
duration: 43.083s
mode: collaborative
message: "Una OneScreen no llena un espacio: lo transforma, y con él, el futuro"
arc: Premisa → Vacío → Falta → Nombre → Creencia → Prueba → Paralelismo → Clímax → Marca → Invitación
audience: Decisores de colegios, universidades y empresas en LATAM
music: none
---

# OneScreen — Transforma el espacio

Film manifiesto en **lettering puro**, estilo Apple. Blanco absoluto, tinta negra, un único
acento `#3976ff`, Rubik en todo. 3840×2160 a 24 fps.

**La locución manda.** `assets/narration.wav` ya está producida y no se toca. Los 1034 frames
del film se cuelgan de sus 124 palabras: cada aparición tipográfica cae sobre el timestamp
real de la palabra que la nombra. El mapa vive en `transcript/beats.json` y se regenera con
`node transcript/build-beats.mjs` — determinista, cuantizado a la rejilla de 24 fps, con una
deriva máxima de 40 ms (menos de un frame) por el redondeo.

**Los cortes ya caen en los huecos de la voz.** Ningún corte de escena parte una palabra:
los diez límites se eligieron dentro de las pausas reales entre frases.

## Reglas que atraviesan las diez escenas

1. **Una palabra azul por cuadro, como máximo.** El azul es subrayado semántico, no cromo.
   El cuadro 4 no lleva ninguna — a propósito: el nombre de la marca va en negro y quien
   pone el acento es el filete.
2. **La unidad de animación es la palabra**, nunca la letra. Nada de máquina de escribir.
3. **`colossal` (16cqw) aparece exactamente dos veces:** "OneScreen" en el cuadro 4 y
   "futuro" en el cuadro 8. Si aparece una tercera vez, deja de ser un golpe.
4. **Vector continuo.** Cómo sale un cuadro determina cómo entra el siguiente. Los handoffs
   están anotados frame a frame en `handoff_out` / `handoff_in`.
5. **Nada de movimiento inactivo.** Si algo se mueve, avanza hacia el siguiente beat.

---

## Frame 1 — Espacios

- scene: Dos versos que se contradicen; el segundo aterriza sobre la palabra "cambian"
- duration: 5.000s
- start: 0.000s
- frames: 120
- transition_in: cut
- status: animated
- poster: 3.6s
- blueprint: kinetic-type-beats
- asset_candidates:
- assets_note: ninguno — lettering puro
- accent_word: "cambian" (3.30–3.68 s)
- voiceover: "Hay espacios que solo ocupan un lugar. Y hay espacios que cambian lo que pasa dentro de ellos."
- src: compositions/frames/01-espacios.html

Abre en frío, sin logo y sin promesa. El primer verso entra en `phrase` y se lee neutro —
es deliberadamente aburrido, porque su trabajo es hacer que el segundo pese. En 2.02 s la
línea se va; el cuadro queda vacío 0.26 s. Ese vacío es el gesto: **el film te muestra un
espacio que solo ocupa un lugar antes de decírtelo.**

El segundo verso entra por palabra sobre sus timestamps. "cambian" llega en 3.30 s en
`#3976ff` y medio escalón por encima del resto de la línea — es la primera vez que aparece
el azul en todo el film, y aparece exactamente sobre la palabra que introduce el conflicto.

`handoff_out` — a 5.000 s el bloque de texto sale hacia arriba a 0.9× de escala, opacidad 0,
y el suelo blanco sigue en su lugar. El cuadro 2 lo recoge invirtiendo ese suelo.

## Frame 2 — Noche

- scene: Inversión a negro con campo estelar; el verso más íntimo, en blanco sobre negro
- duration: 2.500s
- start: 5.000s
- frames: 60
- transition_in: cut
- status: animated
- poster: 1.9s
- blueprint: kinetic-type-beats (adaptado — suelo invertido)
- asset_candidates:
- assets_note: ninguno — campo estelar en CSS estático, sin imágenes
- accent_word: "cualquier" (6.72–7.04 s)
- voiceover: "Hay espacios que no se llenan con cualquier cosa."
- src: compositions/frames/02-noche.html

**El único bloque oscuro del film**, y resuelve la acotación «(fondo espacial)» del guion.
El corte a `#050507` es duro, en un solo frame: sin fundido, sin barrido. Un fundido lo
convertiría en un efecto; el corte lo convierte en un hecho.

El campo estelar son puntos CSS de 1–3 px a opacidades fijas entre 0.15 y 0.7 — escritos a
mano, **sin `Math.random()`**, porque el render tiene que ser determinista. No parpadean.
La única deriva es un desplazamiento lentísimo de todo el campo, de unos 12 px en 2.5 s, que
se lee como profundidad y no como animación.

"cualquier" en `#3976ff` sobre negro es el punto más brillante de los 43 segundos. Es el
mismo azul de siempre; lo que cambia es el suelo. Por eso la inversión no rompe la marca:
**el azul es la constante que atraviesa el corte.**

`handoff_out` — a 7.500 s el negro se retira hacia arriba como una persiana (`clip-path`
vertical, 3 frames), no en fundido. Debajo ya está el blanco del cuadro 3.

## Frame 3 — Falta una cosa

- scene: Vuelve el blanco; el verso queda abierto, esperando un nombre
- duration: 3.583s
- start: 7.500s
- frames: 86
- transition_in: wipe (persiana vertical desde el cuadro 2)
- status: animated
- poster: 2.6s
- blueprint: kinetic-type-beats
- asset_candidates:
- assets_note: ninguno — lettering puro
- accent_word: "falta" (9.50–9.86 s)
- voiceover: "Y hay espacios a los que solo les falta una cosa."
- src: compositions/frames/03-falta-una-cosa.html

El regreso al blanco tiene que sentirse como respirar. El verso entra en `phrase`, con
"falta" en azul en 9.50 s.

El movimiento clave está al final: **"una cosa." aterriza sola en 9.86 s y se queda quieta
1.2 segundos**, mientras el resto del verso baja a `text-muted`. Esa quietud es lo que
prepara el corte. El cuadro no se apaga: se enfoca.

`handoff_out` — a 11.083 s, las palabras "una cosa." quedan en pantalla en su posición
exacta, escala 1, opacidad 1. Todo lo demás ya se fue. El cuadro 4 **recoge esas dos
palabras en la misma posición** y continúa desde ahí.

## Frame 4 — OneScreen

- scene: Match-cut sobre "cosa"; el nombre de la marca entra en el escalón más grande del film
- duration: 2.667s
- start: 11.083s
- frames: 64
- transition_in: cut (match-cut sobre la palabra "cosa")
- status: animated
- poster: 2.3s
- blueprint: kinetic-type-beats (payoff spring-pop)
- asset_candidates:
- assets_note: ninguno — la marca se escribe en Rubik, el logotipo NO aparece aquí
- accent_word: ninguna — el acento lo pone el filete `rule`
- voiceover: "Esa cosa. Es una OneScreen."
- src: compositions/frames/04-onescreen.html

**El corte más importante del film.** El cuadro 3 termina con "una cosa." en pantalla; el
cuadro 4 abre con "Esa cosa." en el mismo lugar, mismo tamaño, misma línea de base. Durante
un frame el espectador no sabe que hubo corte — solo ve que la palabra "cosa" sobrevivió y
que "una" se convirtió en "Esa". El guion hizo esa rima; el montaje solo tiene que no
estorbarla.

Luego, "Es una" entra pequeño y **"OneScreen." llega en 12.96 s en `colossal`** — 16cqw,
peso 800, tracking −0.045em. Primera de las dos únicas apariciones de ese escalón. Negro
sobre blanco, sin azul: el nombre no necesita ayuda.

Bajo la palabra, un filete `rule` de `#3976ff` se dibuja por `scaleX` desde el origen del
texto en 0.35 s. Es el único acento del cuadro.

`handoff_out` — a 13.750 s "OneScreen." sale reduciéndose a 0.62× hacia el centro óptico.
El cuadro 5 entra en esa misma escala reducida: la marca se encoge para dejar hablar al
argumento.

## Frame 5 — Más que tecnología

- scene: La marca habla en primera persona; "más" carga el sentido
- duration: 4.417s
- start: 13.750s
- frames: 106
- transition_in: scale-down handoff
- status: animated
- poster: 3.4s
- blueprint: kinetic-type-beats
- asset_candidates:
- assets_note: ninguno — lettering puro
- accent_word: "más" (16.78–16.98 s)
- voiceover: "Porque para nosotros, transformar un espacio es mucho más que solo tecnología."
- src: compositions/frames/05-mas-que-tecnologia.html

El verso más largo del guion (12 palabras) y el que más riesgo tiene de leerse como una
diapositiva. Se resuelve en dos tiempos, no en uno:

"Porque para nosotros," entra en `sub` y se queda arriba como pie de entrada. El cuerpo
—"transformar un espacio es mucho más que solo tecnología"— entra en `phrase` debajo,
palabra por palabra sobre sus timestamps.

"más" en `#3976ff` en 16.78 s. Y "tecnología." cierra en 17.46 s **bajando a `text-muted`
en el mismo gesto en que aparece** — la palabra se dice y se descarta a la vez, que es
exactamente lo que hace la frase.

`handoff_out` — a 18.167 s todo el bloque sale hacia la izquierda, 0 opacidad, dejando el
eje izquierdo libre. El cuadro 6 construye sobre ese eje.

## Frame 6 — Las tres pruebas

- scene: Tres versos que se acumulan sobre un mismo eje; el tercero se queda con el cuadro
- duration: 6.375s
- start: 18.167s
- frames: 153
- transition_in: cut
- status: animated
- poster: 5.6s
- blueprint: grid-card-assemble (adaptado — lista tipográfica que acumula, sin tarjetas)
- asset_candidates:
- assets_note: ninguno — lettering puro
- accent_word: "grande." (24.20–24.44 s)
- voiceover: "Es una clase que por fin se entiende. Es un equipo que toma mejores decisiones. Es una idea, que ahora se ve en grande."
- src: compositions/frames/06-tres-pruebas.html

**El cuadro más denso del film, y el único con tres líneas simultáneas.** Es también el
único momento en que el guion baja a lo concreto: un salón, una junta, una idea.

Las tres entran en `sub`, alineadas a un eje izquierdo común, en 18.34 / 20.24 / 22.40 s.
Cada línea que entra empuja a las anteriores a `text-muted` — no las borra, las apaga. Al
final del cuadro las tres están en pantalla y solo la tercera está en negro.

El remate es la palabra "grande.": entra en 24.20 s en azul y **escala de `sub` a `display`
en 0.30 s**, rompiendo el eje de las otras dos. La frase dice que ahora se ve en grande; la
tipografía lo hace en vez de decirlo.

`handoff_out` — a 24.542 s las tres líneas salen hacia arriba escalonadas (la primera
primero, 2 frames de diferencia entre cada una), en cascada invertida.

## Frame 7 — Creemos / transformar

- scene: Una frase-ancla fija mientras el objeto cambia dos veces: educación, empresas
- duration: 7.250s
- start: 24.542s
- frames: 174
- transition_in: cut
- status: animated
- poster: 6.2s
- blueprint: fixed-anchor-cycle
- asset_candidates:
- assets_note: ninguno — lettering puro
- accent_word: "futuro." (31.32–31.70 s)
- voiceover: "Creemos en eso. En transformar la educación normal, en educación del futuro. En transformar empresas, en empresas del futuro."
- src: compositions/frames/07-creemos.html

**El cuadro más largo (7.25 s) y el que resuelve el problema estructural del guion:** el
paralelismo. "En transformar X, en X del futuro", dos veces. Repetirlo como dos versos
sueltos lo aplana; anclarlo lo convierte en una figura.

"Creemos en eso." entra en 24.64 s en `display`, centrado, y se sostiene 1.1 s sola. Es la
firma de la marca y merece su propio silencio.

Luego entra el ancla: **"En transformar"** en `phrase`, y **no se mueve más durante 6
segundos.** A su derecha, el objeto rota:

- 26.62 s — "la educación normal," entra
- 27.66 s — "normal" cae y "del futuro" ocupa su lugar (sustitución, no fundido)
- 29.22 s — el ancla parpadea una vez al reiniciarse el paralelismo; entra "empresas,"
- 30.64 s — "empresas del futuro" completa el par

"futuro." final en `#3976ff` en 31.32 s. La quietud del ancla ES el argumento: lo que cambia
es el objeto, nunca el verbo.

`handoff_out` — a 31.792 s el ancla se desvanece en su sitio (2 frames) y el objeto sale
hacia la derecha. El cuadro queda limpio antes del clímax.

## Frame 8 — El futuro también

- scene: El clímax; "futuro" ocupa el cuadro entero en azul
- duration: 3.000s
- start: 31.792s
- frames: 72
- transition_in: cut
- status: animated
- poster: 2.5s
- blueprint: kinetic-type-beats (payoff)
- asset_candidates:
- assets_note: ninguno — lettering puro
- accent_word: "futuro" (33.82–34.16 s) — en `colossal`, la única palabra grande teñida del film
- voiceover: "Porque cuando un espacio cambia. El futuro también."
- src: compositions/frames/08-el-futuro-tambien.html

"Porque cuando un espacio cambia." entra en `phrase` y se va completa en 33.40 s. **Hay
0.34 s de cuadro totalmente vacío** — el hueco real que dejó la voz. No se rellena. Ese
vacío es el resorte del golpe.

En 33.82 s entra **"futuro"** en `colossal`, `#3976ff`, ocupando casi todo el ancho útil.
Segunda y última aparición del escalón más grande, y la única vez que una palabra `colossal`
va teñida. "El" y "también." la acompañan en `sub`, muy pequeñas, arriba y abajo — su
trabajo es dar escala por contraste.

`handoff_out` — a 34.792 s "futuro" no sale: **se contrae hacia el centro y hacia el ancho
exacto del logotipo**, cambiando de azul a negro en los últimos 6 frames. El cuadro 9 lo
recoge convertido en marca.

## Frame 9 — Lockup

- scene: La palabra se convierte en logotipo; firma de marca sobre el filete azul
- duration: 3.417s
- start: 34.792s
- frames: 82
- transition_in: morph (la palabra "futuro" se contrae al ancho del logotipo)
- status: animated
- poster: 2.7s
- blueprint: logo-assemble-lockup
- asset_candidates: assets/onescreen-wordmark.svg — logotipo oficial en vector, teñido por `currentColor`
- accent_word: "futuro." (37.76–38.06 s)
- voiceover: "OneScreen. Transforma el espacio. Transforma el futuro."
- src: compositions/frames/09-lockup.html

**La única aparición del logotipo en todo el film**, y por eso pesa. Llega en 35.00 s,
exactamente sobre la palabra hablada "OneScreen.", en vector negro, centrado.

Bajo él, el filete `rule` de `#3976ff` se dibuja por `scaleX` — el mismo gesto del cuadro 4,
ahora cerrando el arco.

En 35.70 s entra "Transforma el espacio." en `phrase`; en 37.08 s, "Transforma el futuro."
debajo. Las dos comparten la estructura, así que la segunda entra **reusando la posición de
la primera desplazada una línea**, no como un bloque nuevo. "futuro." final en azul.

`handoff_out` — a 38.208 s el logotipo y el filete se mantienen; solo salen las dos líneas
de texto. El cierre no borra la marca, la deja.

## Frame 10 — Toca la pantalla

- scene: El CTA físico; un solo toque sobre la superficie del cuadro y la cola final
- duration: 4.875s
- start: 38.208s
- frames: 117
- transition_in: cut (el logotipo persiste desde el cuadro 9)
- status: animated
- poster: 3.2s
- blueprint: cta-morph-press (adaptado — sin cursor; el dedo es el anillo)
- asset_candidates: assets/onescreen-wordmark.svg — persiste del cuadro 9, reducido
- accent_word: "pantalla." (41.48–41.84 s)
- voiceover: "Tu transformación puede comenzar ya, solo tienes que tocar la pantalla."
- src: compositions/frames/10-toca-la-pantalla.html

El verso entra en `display` en 38.34 s. "Tu transformación puede comenzar ya," se sostiene y
sale en 40.06 s.

"solo tienes que tocar la pantalla." entra en 40.42 s — y sobre la palabra **"tocar"
(41.10 s) el `touch-ring` se dispara**: un anillo de `#3976ff` que se expande desde el punto
de contacto y se desvanece, **un solo pulso, no un loop**. Es el único movimiento del film
que no es tipografía, y dura 0.5 s.

"pantalla." cierra en azul en 41.48 s.

**La cola:** la voz termina en 41.840 s y quedan 1.243 s. El texto se retira; el logotipo
sube al centro óptico y se queda solo sobre blanco hasta el frame 1034. El film no termina
en una palabra: termina en la marca, en silencio.

---

## Lo que cambió entre el plan y la construcción

Cuatro desviaciones respecto al plan aprobado. Ninguna toca el guion, los tiempos ni la
estructura; son decisiones de ejecución que el plan no podía anticipar.

1. **Cuadro 8 → 9 no es un morph geométrico, es un inverse zoom de llegada.** El plan
   decía que «futuro» se contraería hasta el ancho exacto del logotipo. Para que el
   verificador de costuras acepte un morph, las cajas de salida y entrada tienen que
   coincidir dentro de un 5 % de tamaño, y una palabra de 22cqw y un logotipo de
   proporción 6.57:1 no coinciden en alto por mucho que se ajuste el ancho: forzarlo
   habría deformado la marca. Se resolvió con el vector reservado que el catálogo
   destina exactamente a esto: la palabra se repliega y el logotipo llega
   sobredimensionado y se asienta, en el mismo centro. Se lee como una transformación
   y respeta la geometría del logotipo. **Verificado:** signo de escala idéntico en
   ambos lados, sin entradas que peleen el sentido.
2. **Cuadro 7: el objeto ocupa dos líneas, no una.** «la educación normal, en educación
   del futuro.» en un solo renglón a 5cqw mide 4493 px y se sale de un cuadro de
   3840 px. Partirlo en dos refuerza además el paralelismo, que es lo que el cuadro
   argumenta.
3. **Los vectores de costura los cargan los CONTENEDORES, no las palabras sueltas.**
   Sobre fondo blanco no hay superficie visible que se vea viajar, así que el portador
   tiene que ser el bloque de texto. La salida palabra por palabra (waterfall cut) se
   conservó donde sí corresponde: el relevo interno del cuadro 7, a los 29.22 s.
4. **El gris de apoyo pasó de `#8a8a8e` a `#7e7e82`.** El primero se quedaba en 2.7:1
   de contraste sobre blanco y no pasaba WCAG AA. Con el nuevo, las 26 comprobaciones
   de contraste pasan.

## Verificación

| Puerta                                    | Resultado                                     |
| ----------------------------------------- | --------------------------------------------- |
| `lint`                                    | 0 errores, 0 avisos                           |
| `check` — runtime · layout · motion       | 0 errores                                     |
| `check` — contraste                       | 26/26 pasan WCAG AA                           |
| Seam Gate (`ledger.json`, 9 costuras)     | **PASSED** — 0 fallos, 3 avisos de velocidad  |
| Match-cut «cosa» (11.083 s)               | Δposición 0.0 px · Δtamaño 0.0 %              |
| Match-cut del logotipo (38.208 s)         | Δposición 0.0 px · Δtamaño 0.0 %              |

Los tres avisos son de `speed-match`: la velocidad de salida queda por debajo de la de
entrada en las tres costuras cut-the-curve. Subirla más obligaría a alargar el fundido
y la palabra saliente empezaría a arrastrarse. Es un aviso, no un fallo, y el catálogo
lo trata como tal.

## Decisiones que este plan deja abiertas

1. **Música.** `music: none`. La locución entregada es **voz sola** — lo verifiqué en el
   espectrograma: no hay lecho musical, solo voz y cola de reverberación. Un manifiesto de
   43 s aguanta perfectamente sin música, y el silencio refuerza el registro Apple. Pero en
   la carpeta del proyecto ya tienes dos packs descargados
   (`inspirational-and-uplifting-motivation`, `inspirational-hip-hop`), lo que sugiere que sí
   contemplabas una cama. Si la quieres, va al 8–10 % y con salida larga sobre la cola.
2. **Una costura en el audio maestro.** El espectrograma muestra un cambio de carácter en
   ~12.9–13.9 s: la primera parte trae un techo de banda en 17.6 kHz (huella de una fuente
   comprimida) y la segunda no. Es decir, `Main_V1.wav` está armado con dos renders
   distintos. No es un bloqueo y puede que ya lo sepas, pero si notas un cambio sutil de
   "sala" a los 13 s, viene de ahí y se arregla en el máster, no en el video.
