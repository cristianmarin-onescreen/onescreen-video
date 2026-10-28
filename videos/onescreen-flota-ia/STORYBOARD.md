---
format: 1920x1080
duration: 243.7s
message: "Cada agente de la flota de IA de OneScreen tiene un trabajo preciso: sabes a quién acudir, qué puede hacer y qué no"
arc: Bienvenida → AI First → la flota y Odoo → cinco agentes (uno por color) → dos reglas → la flota completa → lockup
audience: Colaboradores de OneScreen (OneScreen Academy)
mode: collaborative
---

# Flota de IA — OneScreen Academy · v3

## Changes from v2

- Usuario: "Siempre que menciones a OneScreen, usa la tipografía oficial… en caso de que no puedas usarlo, se escribe con NEVIS con distancia de letras estrecha, con el loguito de R al final."
  → Toda aparición de "OneScreen" en pantalla es el **logo vectorial** (`assets/onescreen-wordmark.svg`, currentColor) teñido con un color oficial: navy `#293052` / negro `#1a1a1a` sobre claro, blanco `#fafafa` sobre oscuro, azul `#3976ff` como acento. Respaldo: Nevis (`assets/fonts/Nevis.ttf`), tracking -0.04em, con ®.
- Usuario: "Transforma 'el espacio'. Transforma 'el futuro'. lo que está entre comillas debe estar en bold y el resto en regular, en rubik."
  → Lockup: Rubik 400 "Transforma" + Rubik 700 "el espacio." / Rubik 400 "Transforma" + Rubik 700 "el futuro.".
- Usuario: "para títulos debes usar Rubik y para textos de cuerpo debes usar manropa."
  → Titulares, nombres, roles y números grandes: **Rubik**. Etiquetas de gráficos, apoyos, pastillas de contacto y renglones de tarjetas: **Manrope** (`assets/fonts/Manrope-variable-latin.woff2`).

## Changes from v1

- Usuario: "No quiero que únicamente muestres eso, quiero que hayan también motion graphics que vayan explicando y acompañando sincronizados con lo que la voz está diciendo."
- → Cada frase de la voz tiene ahora un **gráfico explicativo animado** (ícono de línea, diagrama, flujo) que entra sobre la palabra que lo nombra. El texto pasa a ser titular corto encima del gráfico; el retrato del agente se queda como ancla.

## Decisiones

- **Formato:** 1920×1080, 30 fps, 243.72 s (la narración manda). Voz sí; música ya mezclada en la narración. Sin subtítulos.
- **Estilo:** video de producto Apple. Titulares grandes en Rubik (tracking negativo), cuerpo en Manrope, "OneScreen" siempre como logo oficial; mucho aire, cortes limpios. Retratos recortados sin fondo sobre el color de su sección.
- **Lenguaje de motion graphics:** íconos y diagramas de línea al estilo SF Symbols — trazo redondeado de 4–6 px en el color de acento de la sección, dibujados con trazo progresivo (stroke draw), rellenos planos sólo en el elemento foco. Flujos con "paquetes" de luz que viajan por las líneas. Todo SVG vectorial hecho a mano; nada de stock.
- **Sincronía:** cada gráfico arranca en el timestamp de la palabra que lo nombra (transcript/words.json) y cede el lugar al siguiente cuando la voz cambia de idea. Nada aparece antes de decirse.
- **Composición por beat:** el retrato del agente ocupa un tercio del cuadro (o se encoge a una insignia en la esquina cuando el diagrama necesita el ancho); el gráfico vive en los otros dos tercios; un titular corto encima.
- **Columna vertebral:** el retrato es el héroe de su sección y nunca sale de cuadro mientras la sección dure. Cinco retratos presentan la flota al inicio; vuelven en fila al cierre (callback).
- **Ficha de contacto:** pastilla con ícono de chat + "WhatsApp" + número en cifras tabulares. Harby: "Está en Odoo". Marco: "Pronto disponible".
- **Prohibiciones:** sin capturas falsas de WhatsApp ni de Odoo (tarjetas estilizadas genéricas); sin logos de terceros ni nombres de plataformas de gobierno; sin cifras inventadas; sin degradados lineales a pantalla completa; sin neón. Fallas a evitar: *slideshow* y *screensaver* (movimiento decorativo que no explica nada).
- **Cuadro sostenido:** el lockup final (231.7–243.7 s) queda quieto mientras termina la música.

### Identidad por sección

| Sección | Fondo | Tinta | Acento |
|---|---|---|---|
| Apertura y flota | `#FFFFFF` | `#0A0A0B` | `#3976FF` |
| Iván · Ventas | `#06291F` | `#F2FBF6` | `#2FD98B` |
| Isaac · Primer contacto | `#FFF3E6` | `#1E140C` | `#F25C05` |
| Isabel · Soporte | `#F0EDFF` | `#16112E` | `#6A4BFF` |
| Harby · Licitaciones | `#0A1230` | `#F4F1E8` | `#E3B341` |
| Marco · Logística | `#1B1C1F` | `#F5F5F2` | `#FFC21A` |
| Dos reglas | `#050507` | `#FFFFFF` | `#3976FF` |
| Cierre | `#FFFFFF` | `#0A0A0B` | `#3976FF` |

## Frame 1 — Bienvenida y AI First

- scene: Una pantalla OneScreen se enciende con "Academy"; cinco puntos despegan en formación; "AI First"; diagrama de procesos con la IA conectada a cada uno; reloj y barras de resultado.
- duration: 15.8s
- poster: 11
- transition_in: cut
- status: animated
- src: compositions/frames/01-apertura.html
- blueprint: kinetic-type-beats + device-surface-showcase

Motion graphics sincronizados:
- 0.0 "Hola" — el contorno de una pantalla interactiva se dibuja y se enciende en blanco.
- 2.0 "OneScreen Academy" — el texto aparece *dentro* de la pantalla.
- 4.3 "flota de IA" — cinco puntos azules despegan de la pantalla en formación en V; titular "Flota de IA".
- 8.0 "AI First" — una fila de bloques de proceso; el bloque "IA" se desliza al primer lugar. Titular colosal "AI First".
- 10.1 "integrada en todos nuestros procesos internos" — diagrama: Ventas · Prospectos · Soporte · Licitaciones · Logística; un chip "IA" central tiende una línea a cada uno, que se encienden en cadena.
- 13.9 "optimizar tiempo" — un reloj cuya aguja da la vuelta rápido; 15.1 "resultados" — tres barras suben en escalera.

## Frame 2 — La flota y Odoo

- scene: Entran los cinco retratos con su etiqueta de color; mapa del recorrido del cliente; hub de Odoo con datos que fluyen; las cinco líneas convergen en "Alexander Guarín"; tarjeta de actividad que revela al agente.
- duration: 26.1s (15.8–41.9)
- poster: 31
- transition_in: cut
- status: animated
- src: compositions/frames/02-flota-odoo.html
- blueprint: constellation-hub

Motion graphics sincronizados:
- 18.4 "flota de agentes" — los cinco retratos entran uno por uno, en círculos.
- 19.1 "diseñados para procesos distintos" — bajo cada retrato cae una etiqueta de su color: Ventas · Prospectos · Soporte · Licitaciones · Logística (adelanto de las identidades).
- 21.4 "cuáles son y en qué momento" — una línea horizontal de recorrido: lead → venta → posventa → gobierno → envío; cada retrato se posa sobre su parada.
- 28.6 "conexión permanente con nuestro ERP Odoo" — los retratos orbitan un núcleo "Odoo"; líneas se dibujan y paquetes de luz viajan en ambos sentidos (conexión permanente = flujo continuo).
- 32.3 "se comunican a través del usuario de Alexander Guarín" — las cinco líneas convergen en un solo avatar "AG · Alexander Guarín"; de él sale una sola línea hacia un avatar "Tú".
- 35.1 "si ves actividad de él" — tarjeta de actividad estilizada: "Alexander Guarín registró una actividad".
- 36.6 "probablemente sea alguno de estos agentes" — el avatar "AG" gira como moneda y revela las caras de los agentes rotando.
- 39.6 "comencemos por uno que ya has usado" — los retratos se apartan; queda Iván, que crece hacia la siguiente escena.

## Frame 3 — Iván Andrade · Coach de ventas

- scene: Bosque profundo. Retrato de Iván como ancla; diagramas de venta.
- duration: 37.85s (41.9–79.75)
- poster: 60
- transition_in: wipe (el verde barre el blanco)
- status: animated
- src: compositions/frames/03-ivan.html
- blueprint: fixed-anchor-cycle

Motion graphics sincronizados:
- 42.2 "Iván Andrade" / 43.9 "coach de ventas" — nombre y rol; pastilla "WhatsApp +57 316 3260059".
- 47.4 "ayudar al equipo a concretar más ventas" — embudo de línea; puntos (oportunidades) caen y salen por abajo marcados con ✓ "Venta".
- 50.9 "disponible 24/7" — anillo de 24 h que se completa; sol y luna se alternan en el borde.
- 52.9 "no se encarga de atender clientes" — diagrama de tres nodos: Cliente — Tú — Iván. La línea Iván→Cliente se dibuja punteada y se tacha.
- 54.4 "ayudarte a atender los tuyos" — la línea Iván→Tú se enciende verde y Tú→Cliente pulsa: el apoyo pasa por ti.
- 59.0 "precios más actualizados… gerencia comercial" — una etiqueta de precio con un sello "Actualizado" que la golpea; firma "Gerencia comercial".
- 62.1 "tarifas y rutas de precios" — una ruta de tres nodos (lista → canal → cliente) que se traza con la etiqueta viajando.
- 65.3 "fichas técnicas" — una hoja con renglones de especificaciones que se escriben.
- 66.5 "comparativos" — dos columnas con barras que se comparan lado a lado.
- 67.4 "políticas de producto" — documento con escudo.
- 69.4 "estrategias comerciales" — tablero con flechas de jugada que se dibujan hacia una meta.
- (los seis íconos quedan en una cuadrícula a medida que se nombran; el último entra en foco)
- 72.5 "tu principal apoyo comercial" — la cuadrícula se pliega detrás de Iván.
- 76.2 "revisada y auditada prácticamente a diario" — tira de calendario de 7 días; un ✓ verde cae en cada día, uno tras otro.
- 79.3 "confiable" — ✓ final grande; retrato centrado con el número en grande.

## Frame 4 — Isaac Alvarado · Primer contacto

- scene: Crema cálido. Retrato de Isaac; flujo de leads; recorrido de 4 estaciones; tarjeta de lead que se llena; filtro de clientes reales.
- duration: 47.35s (79.75–127.1)
- poster: 96
- transition_in: wipe
- status: animated
- src: compositions/frames/04-isaac.html
- blueprint: fixed-anchor-cycle + agent-progress-theater

Motion graphics sincronizados:
- 80.7 "Isaac Alvarado" / 82.8 "primera cara comercial" — nombre, rol.
- 85.7 "contactar a todos los clientes potenciales de marketing" — un ícono de megáfono "Marketing" emite una lluvia de puntos (leads) que fluyen hacia Isaac.
- 88.9 "no tiene como tarea vender" — signo $ que se tacha.
- 92.5 "primer contacto" — un punto-lead entra a la estación 1, aparece una burbuja de chat; 93.5 "sin importar la hora" — reloj a medianoche con luna, la burbuja igual responde.
- 94.7 "calificar" — estación 2: el lead pasa por una balanza/estrellas que se llenan.
- 96.1 "calentar la necesidad" — estación 3: termómetro que sube a naranja.
- 97.6 "agendar demostraciones" — estación 4: casilla de calendario que se llena con "Demo".
- 99.3 "contacto directo con Odoo" — la burbuja de chat vuela hacia una tarjeta de lead estilizada con la etiqueta "Odoo".
- 103.9 "registra las actividades" — cada burbuja se convierte en un renglón de actividad firmado "Isaac" que se apila en la tarjeta.
- 107.9 "agendar demostraciones para el equipo comercial" — la tarjeta entrega una invitación "Demo" a tres avatares del equipo.
- 110.7 "siempre que recibas un lead, revisa las actividades" — zoom a la tarjeta; un resaltador naranja barre los renglones.
- 115.9 "no está diseñado para uso interno" — ícono de equipo interno con candado.
- 119.1 "solo para clientes potenciales" — el candado se abre hacia el lado de los clientes.
- 122.3 "identifica a quienes tienen una necesidad real" — un embudo/criba: muchos puntos entran, sólo algunos pasan encendidos.
- 125.3 "te los entrega listos para la demostración" — los puntos que pasaron llegan a un avatar "Tú" con ✓. Pastilla "WhatsApp +57 315 1513328 · línea para clientes".

## Frame 5 — Isabel Alarcón · Soporte técnico

- scene: Lavanda. Retrato de Isabel; pantalla con falla diagnosticada; vínculo con el equipo Gurú; cuatro capacidades animadas.
- duration: 32.35s (127.1–159.45)
- poster: 151
- transition_in: wipe
- status: animated
- src: compositions/frames/05-isabel.html
- blueprint: fixed-anchor-cycle + grid-card-assemble

Motion graphics sincronizados:
- 128.7 "Isabel Alarcón" / 130.1 "soporte técnico posventa" — nombre, rol, pastilla "WhatsApp +57 316 7764571".
- 133.5 "diagnosticar posibles fallas técnicas" — una pantalla con un ícono de alerta; una línea de escaneo la recorre y aparece una lista de chequeo que se marca.
- 137.3 "la primera cara cuando necesita soporte" — burbuja de chat de un cliente llega directo a Isabel.
- 141.4 "ayuda a revisar sus problemas técnicos" — la alerta de la pantalla cambia a ✓.
- 144.6 "mano derecha de nuestro equipo de soporte Gurú" — Isabel se conecta con un grupo "Equipo Gurú"; una línea violeta los une.
- 149.2 "casos de servicio" — un ticket cuya etiqueta avanza: Abierto → En proceso → Resuelto.
- 150.9 "seriales" — código de barras con línea de lectura.
- 152.1 "garantías" — escudo que se llena con ✓.
- 153.5 "capacitaciones" — casilla de calendario + pizarra.
- 154.8 "si necesitas apoyo técnico, consulta al equipo Gurú o a Isabel" — dos caminos que salen de un "?" hacia "Equipo Gurú" e "Isabel".

## Frame 6 — Harby · Licitaciones

- scene: Azul noche con oro. Edificio institucional; radar que barre plataformas; mapa con zona; notificación en Odoo.
- duration: 23.5s (159.45–182.95)
- poster: 172
- transition_in: wipe
- status: animated
- src: compositions/frames/06-harby.html
- blueprint: fixed-anchor-cycle

Motion graphics sincronizados:
- 160.8 "licitaciones y ventas a gobierno" — un edificio de columnas se dibuja en línea dorada.
- 163.0 "Harby" — nombre; pastilla "Está en Odoo".
- 164.5 "monitor y analista de licitaciones públicas y privadas" — dos pilas de documentos: "Públicas" y "Privadas".
- 169.3 "constantemente monitoreando las plataformas del gobierno" — radar dorado que barre en loop sobre tarjetas de plataforma genéricas; aparecen puntos.
- 173.4 "trayendo aquellas en las que OneScreen puede estar como proveedor" — algunos puntos se encienden en oro y viajan hacia Harby con el sello "OneScreen puede ser proveedor"; el resto se apaga.
- 177.4 "te notificará de las licitaciones disponibles en tu zona" — mapa estilizado por regiones; una región se enciende con un pin.
- 180.3 "a través de Odoo" — campana de notificación con tarjeta "Nueva licitación en tu zona" dentro de un marco "Odoo".
- 181.5 "para que hagas la gestión" — el ✓ de la tarjeta pasa a un avatar "Tú".

## Frame 7 — Marco · Logística

- scene: Grafito con amarillo señal. Retrato de Marco; ruta de importación; despacho; rastreo; sello "Pronto disponible".
- duration: 13.15s (182.95–196.1)
- poster: 192
- transition_in: wipe
- status: animated
- src: compositions/frames/07-marco.html
- blueprint: fixed-anchor-cycle

Motion graphics sincronizados:
- 184.1 "logística" / 185.1 "Marco" / 185.9 "el agente de logística" — nombre, rol.
- 188.7 "revisar importaciones" — un contenedor recorre una ruta marítima punteada.
- 191.0 "despachos" — una caja sale por la puerta de una bodega.
- 191.9 "rastreo de envíos" — ruta con puntos de control; un pin/camión avanza y cada punto se marca.
- 193.4 "tareas útiles para el departamento de logística" — los tres íconos se ordenan en fila.
- 194.5 — sello "Pronto disponible" golpea en amarillo.

## Frame 8 — Dos reglas

- scene: Noche. "Dos reglas." colosal; diagrama de base de conocimiento; respuesta inventada que se disuelve; diagrama de decisión en manos de la persona.
- duration: 24.6s (196.1–220.7)
- poster: 213
- transition_in: cut
- status: animated
- src: compositions/frames/08-reglas.html
- blueprint: kinetic-type-beats

Motion graphics sincronizados:
- 196.3 "dos reglas" — "Dos reglas." colosal, dos barras verticales a la izquierda.
- 200.7 "primero" — "1" + 201.3 "sólo responden desde nuestra base de conocimiento": una pregunta entra en un agente, éste consulta una pila de documentos "Base de conocimiento" y la respuesta sale con un hilo que la une al documento.
- 204.9 "si no tienen información o no saben" — una pregunta llega y la pila no tiene documento que coincida.
- 207.1 "no se lo van a inventar" — una burbuja de respuesta inventada se dibuja y se tacha/disuelve.
- 208.3 "te lo van a decir directamente" — burbuja honesta: "No tengo esa información."
- 210.2 "segundo" — "2" + 210.7 "apoyar tu trabajo": el agente le pasa tarjetas de información a una persona.
- 212.3 "no para decidir por ti" — el botón "Decidir" queda en la mano de la persona; el agente no lo toca.
- 215.5 "optimizar procesos, ahorrar tiempo" — un proceso largo de muchos pasos se comprime a pocos; reloj que ahorra arco.
- 217.9 "jamás reemplazar el trabajo de una persona real" — silueta de persona sólida al frente; el agente queda detrás como apoyo.

## Frame 9 — La flota y lockup

- scene: Blanco. Los cinco retratos vuelven en fila con nombre, color y canal; logotipo y "Transforma el espacio. Transforma el futuro."
- duration: 23.02s (220.7–243.72)
- poster: 235
- transition_in: cut
- status: animated
- src: compositions/frames/09-cierre.html
- blueprint: logo-assemble-lockup

Motion graphics sincronizados:
- 221.7 "esta es la flota de IA de OneScreen" — los cinco retratos entran en fila; bajo cada uno un hilo de su color, nombre y canal (número / "Está en Odoo" / "Pronto disponible").
- 225.2 "para servir a los colaboradores… como a sus clientes" — dos íconos "Colaboradores" y "Clientes" se encienden y líneas los unen a la fila.
- 228.4 "OneScreen" — los retratos se repliegan en cinco puntos que forman el logotipo.
- 228.4 logotipo oficial (navy `#293052`) en grande.
- 229.4 "Transforma **el espacio**." · 231.1 "Transforma **el futuro**." — Rubik regular con lo destacado en Rubik bold; "el futuro" en azul `#3976ff`.
- cuadro sostenido hasta 243.72.
