---
workflow: product-launch-video
flow: automation
storyboard: yes
message: "Una OneScreen no llena un espacio: lo transforma, y con él, el futuro"
destination: youtube
aspect: 3840x2160
language: es
length: 43s
angle: manifiesto
audience: "Decisores de colegios, universidades y empresas en LATAM"
narration: yes
vo_mode: verbatim
capture: brand-only
fps: 24
---

## Intent

Film manifiesto de marca para OneScreen, en estilo **Apple lettering**: tipografía
grande, blanco absoluto, cortes secos y una sola idea por pantalla. Sin locutor a
cuadro, sin capturas de producto, sin stock. La palabra ES la imagen.

El arco del guion es una escalera retórica: cuatro definiciones de "espacio" que se
van estrechando hasta el nombre de la marca, luego tres pruebas concretas (clase,
equipo, idea), una declaración de creencia, y un cierre en llamado a la acción
físico — "tocar la pantalla".

Tono: sobrio, con autoridad, sin euforia publicitaria. El dinamismo viene del ritmo
del corte y de la escala tipográfica, no de efectos.

## Assets

- D:\OneScreen\Contenido\2026\8. Agosto\Video Demo\Main_V1.wav — locución final
  ya producida (ElevenLabs, voz Hale). 43.08 s, PCM 48 kHz estéreo. Es la banda
  maestra: **todo el video se sincroniza a ella**, no al revés.
- Logo oficial OneScreen — a resolver desde onescreenlatam.com. Uso exclusivo en
  el lockup de cierre.

## Customizations

- **Tipografía:** familia **Rubik** en todo el film. Sin excepciones.
- **Paleta:** fondo blanco, tinta negra, acento único **#3976ff**. El azul marca
  solo la palabra que carga el sentido de cada verso — nunca decora.
- **Formato:** 3840x2160 a 24 fps. El 24 fps es una decisión de textura (cine),
  no de peso: los cortes deben caer en frontera de frame a 24.
- **Inversión a negro** en el verso «Hay espacios que no se llenan con cualquier
  cosa» — la acotación «(fondo espacial)» del guion. Fondo negro profundo con
  campo estelar sutil, texto en blanco y #3976ff. Regresa a blanco en «Y hay
  espacios a los que solo les falta una cosa». Es el único bloque oscuro del film.
- **Sincronía a nivel palabra:** timings reales extraídos de la locución
  (whisper large-v3-turbo, 124 palabras). Cada aparición tipográfica cae sobre
  su palabra hablada.
- **Cierre:** logo OneScreen + «Transforma el espacio. Transforma el futuro.»,
  y el CTA físico «solo tienes que tocar la pantalla» resuelto como un toque real
  sobre la superficie del cuadro.

## Decisiones confirmadas durante el run

- **Sin música.** Verificado en el espectrograma que la locución entregada es voz sola,
  sin lecho musical. El usuario confirmó: «No modifiques el audio, solo quiero el texto
  animado». `music: none` en el storyboard, y la narración va enganchada entera —
  un solo elemento `<audio>` de 43.084 s en la pista 10, sin cortes. Partirla en diez
  pedazos (que es lo que pide el contrato por cuadro de `audio_meta.json`) habría
  tijereteado las colas de reverberación que cruzan los límites de escena.
- **Inversión a negro** en el verso «(fondo espacial)»: confirmada, un solo bloque.
- **Logotipo solo en el cierre**: confirmado. Se resolvió con el vector oficial
  encontrado en el disco de la empresa, no con un mapa de bits.
- **Revisión con storyboard y bocetos**: los diez layouts se confirmaron antes de animar.

## Notes

- La locución es **verbatim e intocable**: no se regenera, no se recorta, no se
  reordena. El guion escrito y el audio coinciden palabra por palabra (verificado).
- Sin capturas del sitio: es lettering puro. La única excepción es el logotipo.
- Nada de stock photography, nada de mockups de producto, nada de gradientes
  decorativos. Si un elemento no es texto, logo o campo de color, no entra.
- El audio termina en 41.84 s; quedan ~1.2 s de cola para el hold final del logo.
