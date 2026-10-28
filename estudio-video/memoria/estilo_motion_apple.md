---
name: estilo-motion-apple
description: "21-oct-2026: Cris rechazó las animaciones del video QuizWiz+Scrybe (tarjetas blancas, pop genérico) y eligió como estilo definitivo el del video Flota de IA (tipo Apple); la guía vive en estilo-onescreen/05_MOTION.md."
metadata:
  type: feedback
---

Cris dijo: "estas animaciones casi no me gustan; las que me encantaron fueron las del video de Flota de IA, tipo Apple; definamos un estilo definitivo". Mis animaciones del pitch QuizWiz+Scrybe (pastillas blancas con fade/pop sobre el plano) NO son el estilo.

Estilo de referencia: titulares Rubik enormes con tracking negativo y entrada por **máscara** (sube desde detrás de la línea), **íconos de línea dibujados** (stroke-dashoffset) como SF Symbols, nodos con pop `back.out(1.7)`, paquetes de luz, tachados/sellos, **identidad de color por sección** con barrido (clip-path), easing power3/4 y salidas a la izquierda; todo sincronizado a la palabra que dice la voz. Detalle y valores en `estilo-onescreen/05_MOTION.md`; helpers en `estilo-onescreen/motion/` (`fx.js`, `shared.css`, copiados de `videos/onescreen-flota-ia`).

**Why:** lo vio al comparar con el Flota de IA; las tarjetas/pastillas se sienten genéricas.
El estilo se llama **"Apple"** (nombre acordado con Cris el 21-oct). Cris tiene otros videos suyos con estilos distintos y quiere que aprenda de ellos: cada estilo se guarda con nombre propio y se aprende de varios ejemplos antes de fijar reglas (como con la música).
**How to apply:** en todo video nuevo usar `fx.js` y esas reglas; no volver a las pastillas blancas. Las secciones "propuesta" del 05 (piezas cortas con footage, identidad por producto) aún no las valida Cris. Ver [[zonas-seguras-videos]], [[paleta-motion-graphics]], [[marca-tipografia-onescreen]].
