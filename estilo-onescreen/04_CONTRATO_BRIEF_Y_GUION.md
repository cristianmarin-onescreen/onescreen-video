# 04 Contrato de brief y guion

Versión 1, 14 de octubre de 2026. Define lo que entra (brief) y lo que sale (guion) de este proyecto. Es el mismo contrato que usarán las otras etapas del flujo: la investigación de mercado y la generación de ideas y briefs.

## El flujo

1. Investigación de mercado y de competencia (herramientas tipo Apify) produce datos.
2. Otra IA convierte esos datos en ideas de contenido y briefs cortos.
3. Cris revisa y aprueba los briefs.
4. Este proyecto recibe los briefs aprobados y escribe los guiones. Cris los revisa y los aprueba.
5. Más adelante, al aprobar, la producción arrancaría con stock y automatizaciones. Todavía no se arma y este proyecto no la considera.

Este proyecto es el paso 4. Tiene que funcionar solo: recibe un brief y entrega guiones, sin hacer preguntas y sin tablas.

## Regla de oro: no preguntar

- Un brief mínimo alcanza: la idea y el formato. Todo lo demás es opcional.
- Si falta un campo, Claude lo completa con los valores por defecto de abajo y lo declara en una línea de "Supuestos". No pregunta.
- Solo pregunta si es imposible escribir: no se sabe de qué producto se habla, o no hay forma de saber el formato, o falta un dato de producto que no está en Drive. Aun así entrega lo que pueda y hace una sola pregunta, al final.
- Los datos de producto los busca en Drive, en la carpeta "Recursos OneScreen LATAM", sin avisar.
- Un pedido de Cris puede ser una sola línea ("video de 20 segundos de T7 vs Core") o un brief con campos que llega de otra herramienta. Los dos valen.

## Brief (entrada)

```
brief_id:        opcional, por ejemplo B-2026-001
idea:            OBLIGATORIO. Una línea: qué se quiere decir
formato:         OBLIGATORIO. video_corto | video_explicativo | manifiesto | carrusel | testimonial | blog | correo | ficha | whatsapp
duracion_seg:    solo video
producto:        T7, Core, Titan, Wandr, LED, software, Gurú, Academy, el conjunto
lector:          rector | coordinador | docente | ti | lider_empresa | gobierno
etapa:           no_conoce_problema | conoce_problema | conoce_soluciones | conoce_onescreen | listo_para_decidir
angulo:          uno solo
hook:            frase o idea de entrada
pais:            regional | colombia | ecuador | peru | mexico
cta:             texto del CTA
material_crudo:  escenas, citas, objeciones, enlaces
evidencia:       datos de la investigación que respaldan el brief
restricciones:   lo que no debe decirse, tono
```

## Valores por defecto

| Si falta… | Claude usa… |
| --- | --- |
| duracion_seg | 20 en video_corto, 60 en video_explicativo |
| producto | el que nombre la idea. Si no hay ninguno, el conjunto OneScreen |
| lector | educación: rector o coordinador académico. Empresa: líder de empresa. Si la pieza compara modelos, quien decide la compra |
| etapa | video_corto: conoce_soluciones. Comparación entre modelos: conoce_onescreen. Manifiesto: no_conoce_problema |
| angulo | la diferencia más fuerte y verificable en la ficha vigente. Uno solo |
| hook | construido desde el ángulo con un recurso de 01, sección 8. En piezas cortas, entrada condicional u objeto del pasado |
| pais | regional (se escribe "pizarra") |
| cta | "Solicita tu demo" |
| material_crudo | una escena aprobada de 02, sección 13. Si ninguna sirve, una escena nueva marcada [DESVÍO: escena propuesta] |
| evidencia | datos de la ficha. Nunca cifras de competidores |
| restricciones | las de 02 |

## Salida: qué entrega Claude por cada brief

Lo que entrega es el guion, escrito como escribe Cris: párrafos cortos, de corrido. Sin tablas, sin columnas, sin tiempos por escena y sin búsquedas de stock.

```
Supuestos: una línea con lo que completó.
Intención: una línea. Qué promete, a quién y contra qué dolor.

OPCIÓN A (recomendada) · patrón · 64 palabras

El texto del guion, en párrafos cortos.

Otra frase.

Cierre con CTA.

OPCIÓN B · patrón · 61 palabras

...

OPCIÓN C · patrón · 66 palabras

...

Por qué recomiendo la A: una línea.
Banderas: [REVISAR: motivo], solo si hay alguna.
```

Reglas de la entrega:

- Tres opciones con patrones distintos, una marcada como recomendada y el motivo en una línea.
- Cada opción lleva en su encabezado el patrón y el conteo de palabras. Nada más.
- Las indicaciones de imagen se escriben solo si el guion no se entiende sin ellas, entre corchetes y dentro del mismo texto, como en los guiones de Cris ("[señala el botón verde]"). Máximo dos o tres por pieza.
- Para otros formatos, el texto como lo escribiría Cris: carrusel con una línea numerada por lámina, blog con secciones y títulos, correo con asunto y cuerpo, testimonial con titular, cita y cierre. El formato exacto de cada uno se afina con el uso y con la matriz de formato por etapa.

## Aprobación

- Cuando Cris apruebe una opción (dice "aprobado", "va la A" o algo equivalente), Claude entrega el guion final limpio, sin alternativas ni comentarios, con el brief_id y el estado "aprobado".
- Anota la pieza aprobada en el Registro de correcciones, como entrada E.

## Para quien genere los briefs (etapa 2)

Para que este proyecto no tenga que preguntar nada, cada brief que salga de datos de mercado debería:

- Traer idea y formato.
- Traer en "evidencia" el dato que lo respalda y de dónde sale.
- Plantear un solo ángulo.
- Comparar contra categorías (proyector, televisor, "cualquier IA"), no nombrar marcas competidoras como protagonistas.
- Dejar vacío lo que no sepa. No inventar lector ni etapa para llenar el campo.
