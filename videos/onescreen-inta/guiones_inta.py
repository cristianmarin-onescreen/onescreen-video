"""Guiones dirigidos (ElevenLabs) de los 12 borradores aprobados en sesión el 26-oct-2026 (hoja Guiones, solo H1).
Texto = hook H1 + cuerpo C1 + CTA A1 de la hoja, sin añadir datos. Se quitan solo las marcas editoriales ("extracto de caso de éxito").
Cifras y siglas escritas como se dicen (REGLAS §6). Etiquetas en inglés entre corchetes; arco: gancho enérgico, desarrollo cálido, cierre seguro.
uso: python -I guiones_inta.py   -> escribe guion_dirigido.txt y guion_limpio.txt en D:\\OneScreen\\Contenido\\2026\\10. Octubre\\<Pieza>\\Voz\\"""
import re
from pathlib import Path

BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")

# cada pieza: lista de (etiqueta, frase). Las frases concatenadas son el guion limpio.
G = {
"INTA09": [
 ("[curious, drawing the listener in]", "¿Qué ve un estudiante que creció tocando pantallas cuando entra al aula de tu institución?"),
 ("[warm, matter-of-fact]", "Ellos ya aprendieron a tocar, deslizar y escribir sobre una pantalla. Cuando entran a un salón y encuentran lo mismo de siempre, lo notan."),
 ("[excited, proud]", "Con una pantalla interactiva OneScreen, la clase se escribe, se toca y cobra VIDA, y el docente enseña sin pelearse con nada."),
 ("[confident, softly]", "Un aula así también habla de tu institución, desde el primer día que alguien la visita."),
 ("[calm, assured, short pause]", "OneScreen. Transforma el espacio. Transforma el futuro."),
],
"INTA15": [
 ("[direct, a bit serious]", "Si tu equipo todavía viaja para sentarse en la misma sala, acá te cuento lo que vimos en una empresa:"),
 ("[warm, storytelling]", "En Palmas del Cesar, una empresa agroindustrial, la gente viajaba de la plantación hasta Bucaramanga para reunirse."),
 ("[pleased, lifting]", "Hoy el equipo financiero está en una sala, la plantación en otra, y están en la misma reunión."),
 ("[quoting, natural]", "«La comunicación fue fluida.»"),
 ("[confident, reflective]", "La distancia sigue ahí. Lo que cambió es que ya no hay que recorrerla."),
 ("[inviting, energetic]", "Si tu empresa es la siguiente, te regalamos una demostración en vivo para que veas cómo funcionaría con tus sedes."),
],
"INTA16": [
 ("[direct, knowing]", "Si en tu empresa a alguien siempre le toca armar el acta de memoria, hay una forma de que nadie tenga que hacerlo:"),
 ("[excited, clear]", "Con una pantalla OneScreen, tu reunión se transcribe mientras la tienes."),
 ("[quick, impressed]", "Si alguien habla otro idioma, se traduce al instante, en más de veinte idiomas."),
 ("[warm, confident]", "Al terminar, la IA resume lo que se dijo y lo exportas en Word o en PDF."),
 ("[reflective, then upbeat]", "Antes, uno escribía y los demás miraban. Ahora todos participan, y la pantalla escribe."),
 ("[inviting]", "Escríbenos por WhatsApp y lo vemos en tu sala."),
],
"INTA17": [
 ("[curious, serious]", "Antes de elegir una pantalla para tu sala de reuniones, ¿ya preguntaste qué pasa el día que falle?"),
 ("[calm, explaining]", "Hay tres cosas que mirar. Primero, qué hace la pantalla. Segundo, con qué se conecta."),
 ("[emphasis, leaning in]", "Y tercero, la que casi nadie mira: quién RESPONDE cuando algo falla."),
 ("[warm, reassuring]", "En OneScreen la respuesta está en la propia pantalla: Gurú te conecta con un ingeniero por chat, llamada o videollamada, gratis y de por vida."),
 ("[inviting, confident]", "Escríbenos y revisamos juntos qué necesita tu sala, para que elijas con todo claro."),
],
"INTA18": [
 ("[direct, concerned]", "Comprar tecnología de una sola vez le puede pegar duro a tu flujo de caja. Te explico por qué."),
 ("[matter-of-fact]", "Una compra grande se paga entera el mismo día, y ese dinero ya no está para nada más."),
 ("[brightening, clear]", "Con renting o leasing pagas una cuota mensual, y lo grande sigue en tu caja."),
 ("[warm, enumerating]", "La instalación, el mantenimiento y el soporte Gurú Plus van incluidos."),
 ("[confident]", "Y tú eliges el camino: renting, leasing, o una mezcla de los dos."),
 ("[inviting, upbeat]", "Escríbenos y un asesor calcula contigo tu cuota mensual, para que compares antes de decidir."),
],
"INTA19": [
 ("[curious, bright]", "¿Sabías que puedes arrendar tecnología directo de fábrica, sin intermediarios?"),
 ("[proud, confident]", "Las pantallas OneScreen las fabricamos nosotros, así que negocias directamente con la fábrica: sin intermediarios y con condiciones claras."),
 ("[warm]", "Y quien te las arrienda es quien las instala y quien responde."),
 ("[reassuring, steady]", "Si una pantalla falla por dentro durante el contrato, la reparamos o la reemplazamos sin costo adicional."),
 ("[inviting, upbeat]", "Cotiza tu renting y un asesor te arma el plan a tu medida, para que veas tu cuota mensual con todo lo que incluye."),
],
"INTA20": [
 ("[curious, a little wry]", "¿Sigues usando la misma tecnología que compraste hace cinco años?"),
 ("[matter-of-fact]", "Esa pantalla ya no es la de hoy."),
 ("[bright, explaining]", "Con renting o leasing, los equipos llegan actualizados, y con leasing, la tecnología se renueva cuando termina el contrato."),
 ("[warm, reassuring]", "Gurú Plus, durante todo el contrato, te trae las actualizaciones de software."),
 ("[confident, softly]", "Así tu espacio no se queda con lo que alcanzaste a comprar."),
 ("[inviting]", "Pide información y un asesor te cuenta cómo sería la renovación de tus equipos con cada modelo."),
],
"INTA21": [
 ("[curious, direct]", "Cuando compras una pantalla, ¿quién te instala, mantiene y da soporte?"),
 ("[excited, clear]", "En el renting todo incluido, una sola cuota mensual cubre la pantalla, la instalación, el software, el soporte Gurú Plus y el mantenimiento."),
 ("[warm]", "Llevamos los equipos hasta tu espacio, los instalamos y capacitamos a tu equipo para que empiece a trabajar desde el primer día."),
 ("[reassuring, steady]", "Si una pantalla falla por dentro durante el contrato, la reparamos o la reemplazamos sin costo adicional. Lo demás va por nuestra cuenta."),
 ("[inviting, upbeat]", "Pide tu cotización y en menos de veinticuatro horas un especialista te dice cuánto sería tu cuota mensual y qué incluye."),
],
"INTA22": [
 ("[knowing, light humor]", "Si al final de cada reunión alguien le toma una foto a la pizarra para no perder lo que se escribió, esto tiene arreglo:"),
 ("[excited, clear]", "En una pantalla OneScreen, la pizarra es infinita y todo tu equipo puede escribir en ella a la vez."),
 ("[warm, enumerating]", "Al terminar, la guardas en PDF o en imagen, en tu Drive o en tu OneDrive, o la compartes con un código QR."),
 ("[confident, softly]", "Nadie borra nada, y nadie tiene que acordarse de nada."),
 ("[inviting]", "Escríbenos por WhatsApp y te mostramos todo lo que trae la pizarra de la OneScreen T siete para empresas."),
],
"INTA23": [
 ("[curious, serious]", "¿Qué pasa cuando le pides a una IA que haga el examen de tu clase y ella no estuvo en tu clase?"),
 ("[calm, firm]", "Una IA debería saber lo que tú le enseñaste, y quedarse callada en lo demás."),
 ("[warm, explaining]", "Por eso las IA de OneScreen trabajan con las fuentes que tú les das. QuizWiz arma el examen a partir de tu PDF, tu enlace o la foto de una página."),
 ("[clear, steady]", "SuprNotes responde solo con lo que hay en tus fuentes, y su tutor orienta sin revelar las respuestas. Y Gurú te contesta con la fuente citada."),
 ("[confident, softly]", "Una IA que responde desde lo que tú le diste."),
 ("[inviting]", "Escríbenos y conversemos cómo se vería con los materiales de tu institución."),
],
"INTA24": [
 ("[direct, engaging]", "Si estás comparando pantallas interactivas para tu institución, acá te cuento cómo eligió una universidad de más de cuarenta años:"),
 ("[warm, storytelling]", "Areandina llega a casi todas las regiones de Colombia. Primero validaron la parte técnica: funcionalidad, conectividad, seguridad y certificados. Después trajeron a sus docentes y compararon con otras marcas."),
 ("[quoting, natural]", "«Dejamos que los docentes decidieran, y el resultado fue que OneScreen.»"),
 ("[pleased, clear]", "Les pareció más intuitiva y más fácil de usar, y hoy la misma pantalla es su pizarra y su monitor, sin marcadores."),
 ("[inviting, upbeat]", "Si tu institución es la siguiente, te regalamos una demostración en vivo para que tus docentes la prueben."),
],
"INTA25": [
 ("[curious, intriguing]", "¿Cómo hacen los estudiantes para ver en vivo un procedimiento quirúrgico sin estar dentro de la sala?"),
 ("[warm, storytelling]", "La Clínica Maxilofacial del Caribe también funciona como instituto, y allí los procedimientos de la sala se proyectan en la pantalla para que los estudiantes los vean en vivo."),
 ("[clear]", "En esa misma pantalla, el conferencista dibuja, borra y presenta."),
 ("[quoting, natural]", "«La pantalla de OneScreen hace que nuestros estudiantes entiendan todo más fácil, incluso los procedimientos quirúrgicos en vivo.»"),
 ("[reassuring, warm]", "¿Muchas funciones? Sí, y aprender a usarla no tiene que ser un reto: con Gurú y Academy tu equipo se capacita sin costo adicional."),
 ("[inviting, confident]", "Si tu institución es la siguiente, escríbenos y juntos armamos tu proyecto."),
],
"INTA27": [
 ("[curious, warm]", "¿Sabes qué pregunta nos hicimos hace quince años, y todavía seguimos respondiendo?"),
 ("[thoughtful, direct]", "La pregunta era simple: ¿y si una pantalla pudiera enseñar tanto como la persona frente a ella?"),
 ("[warm, proud]", "Hasta hoy la seguimos respondiendo, en colegios, universidades y empresas de más de cincuenta países."),
 ("[calm, confident, short pause]", "Y esto no lo decimos nosotros:"),
 ("[warm, storytelling]", "En OneScreen amamos contar historias. Y la de tu institución puede ser la siguiente."),
 ("[inviting, upbeat]", "Si tu institución es la siguiente historia, escríbenos y juntos armamos tu proyecto."),
],
"INTA35": [
 ("[curious, direct]", "¿Tus docentes realmente van a usar la tecnología que compras?"),
 ("[warm, reassuring]", "Por eso creamos OneScreen Academy. Una plataforma en línea donde todo tu equipo se certifica en el ecosistema OneScreen, sin costo adicional."),
 ("[warm, enumerating]", "Hay cursos para aprender a usar tu pantalla, para el software de tu pantalla, e incluso cursos de inteligencia artificial."),
 ("[confident, proud, short pause]", "Tu equipo aprende a su ritmo, y nosotros lo certificamos."),
 ("[inviting, upbeat]", "Conoce los cursos de Academy y mira cómo se certificaría tu equipo."),
],
"INTA36": [
 ("[serious, direct]", "Cuando todo falla, necesitas algo confiable."),
 ("[warm, reassuring]", "Cada pantalla OneScreen trae el botón verde Gurú. Lo tocas y hablas con un ingeniero de OneScreen, por chat, llamada o videollamada."),
 ("[warm, enumerating]", "Puedes pedir soporte técnico, o agendar todas las capacitaciones que tu equipo necesite, gratis e ilimitadas."),
 ("[confident, proud, short pause]", "Te presentamos OneScreen Gurú."),
 ("[inviting, upbeat]", "Pide tu cotización y te contamos todo lo que incluye Gurú desde el primer día."),
],
"INTA37": [
 ("[curious, raised eyebrow, quick]", "Las instituciones han evolucionado, pero, ¿y la pizarra?"),
 ("[enthusiastic, fast-paced, upbeat]", "Todas las pantallas OneScreen tienen una pizarra interactiva INFINITA. Con todos los trazos que te imagines."),
 ("[excited, rapid-fire, enumerating]", "Una tabla periódica integrada. Reglas, transportador y compás. Simulaciones interactivas de física, química y biología."),
 ("[amazed, delighted]", "Y reconoce tu escritura a mano, para que tu letra se vuelva texto."),
 ("[proud, emphatic, short pause]", "Esta es una pizarra que REALMENTE evoluciona."),
 ("[friendly, upbeat, quick]", "Pero implementar esto no debe ser difícil, escríbenos y te agendamos una demostración sin costo."),
],
}

if __name__ == "__main__":
    import sys
    for pieza, frases in ((k, v) for k, v in G.items() if k in (sys.argv[1:] or G)):
        voz = BASE / pieza / "Voz"
        voz.mkdir(parents=True, exist_ok=True)
        dirigido = " ".join(f"{t} {f}" for t, f in frases).replace("SuprNotes", "Súper Nouts")
        limpio = " ".join(f for _, f in frases)
        (voz / "guion_dirigido.txt").write_text(dirigido, encoding="utf-8")
        (voz / "guion_limpio.txt").write_text(limpio, encoding="utf-8")
        print(pieza, len(limpio.split()), "palabras")
