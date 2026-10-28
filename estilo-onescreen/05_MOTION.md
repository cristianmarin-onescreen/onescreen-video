# 05 Estilo de motion "Apple" (OneScreen)

Versión 1, 21 de octubre de 2026. Sale de revisar el video **Flota de IA** (`videos/onescreen-flota-ia`, 243 s, el que Cris eligió como referencia: "las que me encantaron fueron las de tipo Apple"). Lo que sigue describe lo que ese video HACE, medido en su código (`compositions/frames/*.html`, `assets/fx.js`, `assets/shared.css`). Los ayudantes reutilizables están copiados en `motion/`. Las secciones marcadas **[propuesta]** son decisiones nuevas que Cris aún no ha validado.

## 1. Principio
- **La voz manda.** Cada gráfico arranca en el timestamp de la palabra que lo nombra (`T(cue)`); nada aparece antes de decirse y cede su lugar cuando la voz cambia de idea.
- **Un foco por beat.** Un titular + un gráfico. Mucho aire. Cortes limpios, sin adornos que no expliquen.
- **Explicar, no decorar.** Cada frase de la voz tiene un gráfico que la dibuja (ícono, diagrama, flujo), no una tarjeta genérica.

## 2. Identidad por sección
Cada sección tiene su propio **fondo + tinta + acento** (Iván verde `#06291F`/`#2FD98B`, Isaac crema `#FFF3E6`/`#F25C05`, Isabel lila, Harby azul noche, Marco grafito; apertura y cierre blancos con `#3976FF`). La sección entra con **barrido de color** (`clip-path: inset(0 100% 0 0)` → `inset(0)`, 0,6 s, `power3.inOut`). [propuesta] En piezas cortas: una identidad por producto (p. ej. Scrybe / QuizWiz) y cierre blanco con azul `#3976FF`; paleta de la regla [[paleta-motion-graphics]] (sin amarillo) manda sobre la de Harby/Marco en piezas nuevas.

## 3. Tipografía y texto
- Titulares **Rubik 600–700**, tracking **-0,03 a -0,045 em**, interlineado ~1,0; grandes (76–136 px a 1080p; el nombre héroe 136 px).
- **Kicker** Manrope 800, 22 px, mayúsculas, tracking 0,16 em, color de acento. Cuerpo Manrope 500; etiquetas Manrope 700.
- Palabra clave del titular en el color de acento; el resto en tinta (o apagado `mut` para lo que se niega).
- **Entrada de nombres/titulares grandes: máscara** — el texto sube desde detrás de su línea (`overflow:hidden`; `yPercent 110→0`, `power4.out`, 0,7 s, stagger 0,06–0,12). Titulares normales: `FX.up` (sube 24–40 px y aparece, 0,5–0,6 s, `power3.out`).
- "OneScreen" siempre logo oficial; slogan con bold parcial ([[marca-tipografia-onescreen]]).

## 4. Íconos y diagramas (el sello del estilo)
- **Línea tipo SF Symbols**: trazo redondeado de 3–7 px en el acento, **dibujado con trazo progresivo** (`pathLength=1`, `stroke-dasharray:1 2`, `dashoffset 1→0`, 0,8–1,1 s, `power2.inOut`, stagger 0,08).
- **Nodos**: disco con borde de 6 px que entra con `back.out(1.7)` desde escala 0,6 (el único rebote del estilo, solo para íconos, nodos y sellos).
- Conexiones: línea que se dibuja + **paquete de luz** que la recorre; lo negado se **tacha** (barra `scaleX 0→1`) o lleva una X dibujada; lo afirmado se resalta con contorno `on` en la tarjeta.
- **Sello** ("ACTUALIZADO", "PRONTO DISPONIBLE"): `scale 2.2→1`, rotación -6°, `power4.in`, 0,35 s.
- Tarjetas estilizadas genéricas, **nunca capturas falsas** de WhatsApp/Odoo/terceros.

## 5. Movimiento y easing
- Entradas `power3.out` / `power4.out` (0,4–0,9 s; el héroe 0,9 s y 200–260 px de recorrido). Salidas `power2.in` 0,3–0,4 s, **hacia la izquierda** (`x:-60`, stagger 0,02). Cambios de plano: `power3.inOut`.
- Cuadrículas se **pliegan** al salir (`scale .85`, `y 40`, `opacity 0`, stagger desde el centro). El héroe puede encogerse a insignia (`scale .68` desde la esquina).
- Prohibido: parpadeos, "idle wobble", movimiento que no sea causal con la voz, degradados lineales de relleno.
- Retratos/héroes **recortados sin fondo**, entran desde abajo y no salen de cuadro mientras dure su sección.

## 6. Planos de video (cuando hay footage) [propuesta]
El Flota no usó footage. Para anuncios con planos reales: plano a pantalla completa, coloreado con [[pipeline-color-slog3]]; el titular va **directo sobre el plano** con máscara y tinta blanca/azul, sin tarjetas blancas tipo "pastilla"; los gráficos de línea del producto (micrófono de Scrybe, lupa de QuizWiz, QR) se dibujan encima en el acento; las secciones cambian con barrido de color o corte seco. Zonas seguras por formato: [[zonas-seguras-videos]].

## 7. Técnica (innegociable)
`gsap.defaults({lazy:false})`; timeline pausado por escena; `FX.show` para aparecer; nada de `immediateRender:false` con estado visible ([[hyperframes-render-trampas]]). Helpers: `motion/fx.js` (`FX.up/pop/rise/out/wipe/draw/packet/show/prep`) y `motion/shared.css` (componentes: `.h .k .pill .badge .node .disc .tile .stamp .idc`).

## 8. Actualización 28-oct-2026 (Cris): degradados, texturas y color por significado
- **Ya se usan degradados profundos y texturas** (puntos o rejilla fina) en los fondos y **tarjetas de vidrio** (relleno translúcido + borde fino), como en las cotizaciones de Gurú y Academy. Esto **reemplaza** la prohibición de «degradados lineales de relleno» de la sección 5.
- **Color por significado:** verde solo para Gurú; azul para la solución; blanco cuando exponemos o enseñamos algo.
- **Sin rótulos en MAYÚSCULA** tipo título de diapositiva.
- **Lettering Apple (medido en el video de 108 s):** una frase corta por beat, tamaño medio, las palabras entran una a una y el nombre de la función lleva degradado dentro del texto.
- Biblioteca de plantillas: `estudio-video/motion/plantillas.py` (ver CLAUDE.md, «Plantillas de motion»).
