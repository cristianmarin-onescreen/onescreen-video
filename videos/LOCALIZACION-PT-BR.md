# Versiones en portugués de Brasil

Todas las piezas de lettering, localizadas a **pt-BR**. Un archivo por pieza y por tinta,
ProRes 4444 con alfa, 3840×2160, 25 fps, en `D:\Lettering OneScreen\`.

## La regla que gobierna todo: los cuadros no se mueven

No existe locución en portugués. Las capas españolas están sincronizadas al habla
española, así que había dos caminos posibles y elegí el que conserva tus montajes:

> **Cada cuadro y cada línea conservan su instante de entrada y de salida al fotograma.
> Lo único que se redistribuye son las palabras dentro de su propia línea.**

Se ancla a nivel de LÍNEA, no de cuadro, porque lo que el ojo percibe como «el ritmo»
es el momento en que cambia una línea, no el goteo de cada palabra. El resultado es que
cada capa portuguesa dura exactamente lo mismo que su equivalente española y cae en los
mismos golpes: es un **reemplazo directo** en la línea de tiempo.

Si más adelante grabas locución portuguesa **doblada a imagen** (la práctica normal de
localización), encaja sin tocar nada. Si la relocutas libre, habrá que resincronizar —
pero eso pasaría con cualquier método, porque no hay audio portugués al que seguir.

## Vocabulario: decisiones que no salen solas del español

| Español | pt-BR | Por qué |
| --- | --- | --- |
| pantalla | **tela** | En Brasil «pantalla» no existe; «tela» es el término del producto. |
| tablero / pizarra | **lousa** | «Lousa digital» es el término establecido en el mercado educativo brasileño. |
| docente | **professor** | «Docente» existe pero suena administrativo. |
| clase (la lección) | **aula** | |
| aula (el espacio) | **sala de aula** | Falso amigo clásico: `aula` en portugués es la clase, no el salón. |
| capacitación | **treinamento** | |
| arrendamiento | **locação** | Registro B2B; «aluguel» es más doméstico. |
| cuota mensual | **mensalidade** | |
| stand (feria) | **estande** | |
| aplicaciones | **aplicativos** | |
| puntos táctiles | **pontos de toque** | |

Los nombres de producto no se traducen: Core, T7, Titan, Wandr, VirtualWalls, Lessn,
Scrybe, QuizWiz, SuprNotes, Gurú, Academy.

## Dos cifras que había que corregir, no traducir

**1 · «6 billones de operaciones por segundo» (T7).** En español «billón» es 10¹². Brasil
usa **escala corta**, así que el equivalente correcto es **«6 trilhões»**. Traducirlo como
«6 bilhões» —el cognado obvio— habría dicho mil veces menos. Lo puse como *trilhões*
asumiendo una NPU de 6 TOPS; **si el chip es otro, avísame y lo cambio**.

**2 · «1.07 billones de colores» (Titan).** La cifra real de un panel de 10 bits son
1.073 **mil millones**, no billones — el español tenía ahí un anglicismo. En portugués va
**«1,07 bilhão»**, que además es la cifra correcta.

## Tipografía

- **Rubik** cubre todo el portugués, incluida la **Ç mayúscula** y los tildes sobre
  versalitas (`INTELIGÊNCIA`, `CORREÇÃO`). Verificado rasterizando cada carácter y
  comparándolo con la caja de glifo ausente, no fiándose del nombre de la fuente.
- **Nevis no trae ningún diacrítico.** No afecta: Nevis solo compone «OneScreen», que no
  lleva ninguno.
- Las líneas en versalitas se escriben en **caja natural** en los archivos de traducción;
  las pone en mayúsculas el CSS, igual que en español, para no romper el tracking.

## Verificación de desbordes: contra el español, no contra un umbral

Se midieron las 14 piezas **en los dos idiomas** con el mismo instrumento y se comparó.
Solo cuenta lo que **empeora** respecto al español:

- **Ninguna pieza gana un desborde nuevo.** Los avisos que aparecen ya existían en
  español — por ejemplo «graaaaaande.» mide 3553 px en un área útil de 3302 en ambos
  idiomas, porque la palabra es idéntica.
- **Dos piezas mejoran.** En Gurú, «capacitaciones» desbordaba y «treinamentos» no. En
  Academy, «certificarse» desbordaba y «se certificar» no.
- **Una regresión, corregida.** En Titan el cuadro f05 pasaba de 3 a 4 filas; se acortó
  la frase hasta igualar el español.
- En testimonios los subtítulos quedan **más ligeros** que en español (c1 y c8 bajan de 4
  a 3 filas; c3 sube de 2 a 3).

## Las tres piezas con generador propio

**intros** — las cuatro tarjetas no tienen locución, así que su ritmo sale de un modelo
de lectura (2.7 palabras/s, entrada, salto de línea, reposo). En portugués las duraciones
**se recalculan solas** con el conteo de palabras portugués: SuprNotes pasa de 6.76 s a
7.12 s porque su descriptor tiene una palabra más. Ahí «el mismo ritmo» significa el
mismo modelo, no la misma duración — no hay voz que seguir.

**testimonios** — los subtítulos son de entrevistas rodadas **en español**. En la versión
portuguesa son subtítulos portugueses sobre habla española: localización normal. Sus
ventanas no se tocan, porque cada rótulo tiene que cambiar cuando cambia lo que se dice.
De paso se arreglaron los cortes de línea que en español partían la frase por la mitad
(«o / sea,», «que / otras,»).

**transforma** — el manifiesto. Es la única pieza con coreografía escrita a mano (809
líneas: portadores, héroes, la explosión de «grande», el lockup, las costuras de
velocidad) que referencia las palabras por índice absoluto. En vez de re-coreografiarla,
la traducción se hizo con una **restricción dura: cada escena conserva exactamente el
mismo número de palabras que el español**. Resultado: cero cambios en la coreografía, y
los acentos caen en la palabra correcta en las diez escenas — `mudam`, `qualquer`,
`falta`, `mais`, `grande.`, `futuro.`, `tela.`

Donde el portugués quería menos palabras se compensó sin inflar el sentido:

| Escena | Español | pt-BR |
| --- | --- | --- |
| 01 | «lo que pasa dentro de ellos» | «tudo o que acontece dentro deles» |
| 03 | «a los que solo les falta» | «por aí em que só falta» |
| 07 | «en eso.» | «muito nisso.» |
| 10 | «solo tienes que tocar» | «é só você tocar» |

## Qué queda en tu lado

**Revisión de un hablante nativo antes de publicar.** La traducción es mía y está
razonada, pero es copy de marca en un mercado nuevo. Las decisiones que más conviene
que valide alguien de Brasil:

- `lousa` vs `quadro` para el tablero interactivo.
- `locação` como término comercial del modelo DaaS.
- El tuteo con `você` en todo el material (es lo estándar en Brasil, pero conviene
  confirmarlo con la línea de la marca).
- Si el registro debe ser más formal para instituciones públicas.

## Cómo se regenera

```bash
# mapas de tiempos portugueses (once piezas de cuadros)
python make-pt-beats.py

# una pieza cualquiera, en portugués
cd onescreen-<pieza> && HF_BEATS=beats.pt.json HF_INK="#000000" node tools/build-frames.mjs

# las tarjetas
cd onescreen-intros && HF_LANG=pt HF_INK="#000000" HF_ONLY=c01 node tools/build-cards.mjs
```

Sin `HF_BEATS` / `HF_LANG` todo sigue saliendo en español exactamente como antes: el
idioma es una variable de entorno, no una bifurcación del proyecto.
