"""Especificación de cada pieza INTA (preview). Los textos en pantalla salen del propio guion; las anclas son palabras de la voz (word, n-ésima aparición).
ov: texto sobre el plano (de a hasta b) · color: escena de fondo azul con texto · cierre: tarjeta blanca final (slogan o CTA) desde su palabra.
Línea = (texto, 'l' ligera | 'b' negrita). Sin la palabra 'OneScreen' escrita en los textos (la marca va con logo): salvo el slogan, que es el logo."""

EDU = dict(lugares=["Aula"], sectores=["Educación superior", "Educación básica", "Formación técnica"], exige_pantalla=True)
CORP = dict(lugares=["Sala de reuniones", "Oficina"], sectores=["Corporativo"], exige_pantalla=True)
MIX = dict(lugares=["Sala de reuniones", "Aula", "Oficina"], sectores=["Corporativo", "Educación superior"], exige_pantalla=False)


def ov(a, b, *lines, pos="bl"):
    return dict(a=a, b=b, lines=list(lines), pos=pos)


def pal(a, b, *items):
    """palabras sueltas que entran una a una con su palabra de la voz (estilo del video de Beneficios en educación). items = (texto, (palabra, n))"""
    return dict(a=a, b=b, pal=list(items))


SPECS = {
"INTA09": dict(tema=dict(EDU, kw=["estudiantes", "tactil", "toca"]),
    ov=[ov(("tocando", 0), ("cuando", 0), ("Creció tocando", "l"), ("pantallas", "b")),
        ov(("tocar", 0), ("cuando", 1), ("Tocar. Deslizar.", "l"), ("Escribir.", "b")),
        ov(("mismo", 0), ("notan", 0), ("Lo mismo", "l"), ("de siempre", "b")),
        ov(("habla", 0), ("visita", 0), ("Habla de", "l"), ("tu institución", "b"))],
    color=dict(a=("escribe", 0), b=("docente", 0), lines=[("Se escribe. Se toca.", "l"), ("Cobra vida.", "b")]),
    cierre=dict(word=("transforma", 0), slogan=True, lines=[])),
"INTA15": dict(tema=dict(CORP, caso="Palmas del Cesar", kw=["plantacion", "viaje"]),
    ov=[ov(("viaja", 0), ("acá", 0), ("Viajar para", "l"), ("reunirse", "b")),
        ov(("palmas", 0), ("gente", 0), ("Palmas", "b"), ("del Cesar", "l")),
        ov(("plantación", 0), ("hoy", 0), ("De la plantación", "l"), ("a Bucaramanga", "b")),
        ov(("comunicación", 0), ("distancia", 0), ("“La comunicación", "l"), ("fue fluida.”", "b")),
        ov(("cambió", 0), ("si", 1), ("Ya no hay que", "l"), ("recorrerla", "b"))],
    color=dict(a=("están", 0), b=("comunicación", 0), lines=[("En la misma", "l"), ("reunión", "b")]),
    cierre=dict(word=("si", 1), slogan=False, lines=[("Te regalamos una", "l"), ("demostración en vivo", "b")])),
"INTA16": dict(tema=dict(CORP, kw=["escribe", "documento"]),
    ov=[ov(("transcribe", 0), ("si", 1), ("Se", "l"), ("transcribe", "b"), pos="c"),
        ov(("ahora", 0), ("escríbenos", 0), ("Todos", "l"), ("participan.", "b"), pos="bl")],
    gfx=[dict(kind="acta", a=("nadie", 0), b=("reunión", 0), cues=[("hacerlo", 0)]),
         dict(kind="idiomas", a=("habla", 0), b=("terminar", 0), cues=[("traduce", 0)]),
         dict(kind="resumen", a=("resume", 0), b=("antes", 0), cues=[("resume", 0), ("word", 0)])],
    color=None,
    cierre=dict(word=("escríbenos", 0), slogan=False, lines=[("Escríbenos", "b"), ("por WhatsApp", "l")])),
"INTA17": dict(tema=dict(CORP, kw=["soporte", "tecnico", "ingeniero"]),
    ov=[ov(("pasa", 0), ("hay", 0), ("¿Qué pasa el día", "l"), ("que falle?", "b")),
        ov(("tres", 0), ("primero", 0), ("Tres cosas", "b"), ("que mirar", "l")),
        ov(("primero", 0), ("segundo", 0), ("Qué hace", "l"), ("la pantalla", "b")),
        ov(("segundo", 0), ("tercero", 0), ("Con qué", "l"), ("se conecta", "b")),
        ov(("gurú", 0), ("escríbenos", 0), ("Gurú", "b"), ("chat, llamada o videollamada", "l"))],
    color=dict(a=("tercero", 0), b=("onescreen", 0), lines=[("Quién responde", "b"), ("cuando algo falla", "l")]),
    cierre=dict(word=("escríbenos", 0), slogan=False, lines=[("Escríbenos", "b"), ("y revisamos juntos", "l")])),
"INTA18": dict(tema=dict(MIX, kw=["dinero", "pago"]),
    ov=[ov(("comprar", 0), ("te", 0), ("Comprar", "l"), ("de una sola vez", "b")),
        ov(("paga", 0), ("con", 0), ("Se paga entera", "l"), ("el mismo día", "b")),
        ov(("instalación", 0), ("eliges", 0), ("Instalación, mantenimiento", "l"), ("y soporte incluidos", "b")),
        ov(("renting", 1), ("escríbenos", 0), ("Renting, leasing", "b"), ("o una mezcla", "l"))],
    color=dict(a=("renting", 0), b=("instalación", 0), lines=[("Una cuota", "l"), ("mensual", "b")]),
    cierre=dict(word=("escríbenos", 0), slogan=False, lines=[("Calcula tu cuota", "l"), ("con un asesor", "b")])),
"INTA19": dict(tema=dict(MIX, kw=["fabrica", "produccion", "instalacion"]),
    ov=[ov(("directo", 0), ("pantallas", 0), ("Directo", "l"), ("de fábrica", "b")),
        ov(("fabricamos", 0), ("así", 0), ("Las fabricamos", "l"), ("nosotros", "b")),
        ov(("instala", 0), ("si", 0), ("Quien arrienda", "l"), ("instala y responde", "b")),
        ov(("reparamos", 0), ("cotiza", 0), ("Reparamos o", "l"), ("reemplazamos", "b"))],
    color=dict(a=("sin", 1), b=("quien", 0), lines=[("Sin", "l"), ("intermediarios", "b")]),
    cierre=dict(word=("cotiza", 0), slogan=False, lines=[("Cotiza tu renting", "b"), ("con un asesor", "l")])),
"INTA20": dict(tema=dict(MIX, kw=["tecnologia", "actualiza"]),
    ov=[ov(("cinco", 0), ("esa", 0), ("¿Hace", "l"), ("cinco años?", "b")),
        ov(("esa", 0), ("con", 0), ("Esa pantalla", "l"), ("ya no es la de hoy", "b")),
        ov(("actualizaciones", 0), ("así", 0), ("Actualizaciones", "b"), ("de software", "l")),
        ov(("alcanzaste", 0), ("pide", 0), ("Lo que alcanzaste", "l"), ("a comprar", "b"))],
    color=dict(a=("leasing", 1), b=("guru", 0), lines=[("Con leasing", "l"), ("se renueva", "b")]),
    cierre=dict(word=("pide", 0), slogan=False, lines=[("Pide información", "b"), ("con un asesor", "l")])),
"INTA21": dict(tema=dict(MIX, kw=["instalacion", "tecnico", "soporte"]),
    ov=[ov(("instala", 0), ("renting", 0), ("Instala, mantiene", "l"), ("y da soporte", "b")),
        ov(("instalamos", 0), ("si", 0), ("Instalamos y", "l"), ("capacitamos", "b")),
        ov(("sin", 0), ("lo", 0), ("Sin costo", "l"), ("adicional", "b")),
        ov(("lo", 0), ("pide", 0), ("Lo demás", "l"), ("va por nuestra cuenta", "b"))],
    color=dict(a=("una", 1), b=("llevamos", 0), lines=[("Una sola cuota", "l"), ("mensual", "b")]),
    cierre=dict(word=("pide", 0), slogan=False, lines=[("Pide tu cotización", "b"), ("en menos de 24 horas", "l")])),
"INTA22": dict(tema=dict(CORP, kw=["pizarra", "escribe", "marcador"]),
    ov=[ov(("foto", 0), ("esto", 0), ("Una foto", "l"), ("a la pizarra", "b")),
        ov(("guardas", 0), ("nadie", 0), ("PDF, imagen,", "l"), ("Drive, OneDrive o QR", "b")),
        ov(("nadie", 0), ("escríbenos", 0), ("Nadie", "l"), ("borra nada", "b"))],
    color=dict(a=("pizarra", 1), b=("terminar", 0), lines=[("Pizarra", "l"), ("infinita", "b")]),
    cierre=dict(word=("escríbenos", 0), slogan=False, lines=[("Escríbenos", "b"), ("por WhatsApp", "l")])),
"INTA23": dict(tema=dict(EDU, kw=["examen", "computador", "documento"]),
    ov=[ov(("examen", 0), ("una", 1), ("El examen", "l"), ("de tu clase", "b")),
        ov(("saber", 0), ("por", 0), ("Una IA que sabe", "l"), ("lo que le enseñaste", "b")),
        ov(("arma", 0), ("responde", 0), ("QuizWiz", "b"), ("examen desde tu PDF", "l")),
        ov(("responde", 0), ("contesta", 0), ("SuprNotes", "b"), ("responde con tus fuentes", "l")),
        ov(("contesta", 0), ("citada", 0), ("Gurú", "b"), ("con la fuente citada", "l"))],
    color=dict(a=("por", 0), b=("arma", 0), lines=[("Trabaja con", "l"), ("tus fuentes", "b")]),
    cierre=dict(word=("escríbenos", 0), slogan=False, lines=[("Escríbenos", "b"), ("y conversemos", "l")])),
"INTA24": dict(tema=dict(EDU, caso="Areandina|Area Andina", solo_caso=True, kw=["docente", "universidad"]),
    ov=[ov(("universidad", 0), ("ariandina", 0), ("Una universidad de", "l"), ("más de 40 años", "b")),
        ov(("funcionalidad", 0), ("después", 0), ("Funcionalidad, conectividad,", "l"), ("seguridad, certificados", "b")),
        ov(("después", 0), ("dejamos", 0), ("Después,", "l"), ("los docentes", "b")),
        ov(("intuitiva", 0), ("hoy", 0), ("Más intuitiva.", "l"), ("Más fácil de usar.", "b")),
        ov(("pizarra", 0), ("si", 1), ("Pizarra y monitor", "b"), ("sin marcadores", "l"))],
    color=dict(a=("dejamos", 0), b=("les", 0), lines=[("“Dejamos que los", "l"), ("docentes decidieran”", "b")]),
    cierre=dict(word=("si", 1), slogan=False, lines=[("Te regalamos una", "l"), ("demostración en vivo", "b")])),
"INTA25": dict(tema=dict(lugares=["Hospital / clínica", "Aula", "Auditorio"], sectores=["Salud", "Educación superior"], exige_pantalla=False, caso="Maxilofacial|Bucofacial|Cl.nica del Caribe", salud=True, kw=["cirugia", "estudiantes"]),
    ov=[ov(("ver", 0), ("clínica", 0), ("Ver en vivo", "l"), ("un procedimiento", "b")),
        ov(("proyectan", 0), ("esa", 0), ("En la pantalla,", "l"), ("en vivo", "b")),
        ov(("conferencista", 0), ("hace", 0), ("Dibuja, borra", "l"), ("y presenta", "b")),
        ov(("muchas", 0), ("aprender", 0), ("¿Muchas funciones?", "l"), ("Sí.", "b")),
        ov(("aprender", 0), ("con", 0), ("Aprender a usarla", "l"), ("no es un reto", "b")),
        ov(("con", 0), ("si", 1), ("Gurú y Academy", "b"), ("sin costo adicional", "l"))],
    color=dict(a=("entiendan", 0), b=("muchas", 0), lines=[("“Entiendan todo", "l"), ("más fácil”", "b")]),
    cierre=dict(word=("si", 1), slogan=False, lines=[("Escríbenos y", "l"), ("armamos tu proyecto", "b")])),
"INTA27": dict(tema=dict(EDU, kw=["pantalla", "docente", "estudiantes", "universidad", "empresa", "colegio"]),
    ov=[],
    color=None,
    cierre=dict(word=("si", 1), slogan=False, lines=[("Escríbenos y", "l"), ("armamos tu proyecto", "b")])),
"INTA35": dict(tema=dict(EDU, kw=["academy", "curso", "capacitacion", "docentes", "aprende", "certificacion"]),
    ov=[],
    cards=[dict(a=0.0, b=("por", 0), lines=[("¿Tus docentes", "l", ("docentes", 0)), ("la van a usar?", "b", ("usar", 0))]),
           dict(a=("todo", 0), b=("hay", 0), lines=[("Todo tu equipo", "l", ("equipo", 0)), ("certificado", "b", ("certifica", 0)), ("sin costo adicional", "l", ("sin", 0))]),
           dict(a=("cursos", 0), b=("aprende", 0), lines=[("Tu pantalla", "b", ("pantalla", 0)), ("Su software", "b", ("software", 0)), ("Inteligencia artificial", "b", ("inteligencia", 0))])],
    tags=[dict(a=("academy", 0), b=("una", 0), name="Academy"),
          dict(a=("certificamos", 0), b=("conoce", 0), name="Academy")],
    color=None,
    cierre=dict(word=("conoce", 0), grafico=True, slogan=False, lines=[],
                texto="Conoce los **cursos** en onescreenlatam.com/**academy**")),
"INTA36": dict(tema=dict(MIX, exige_pantalla=True, kw=["soporte", "tecnico", "ingeniero", "videollamada"]),
    ov=[],
    cards=[dict(a=0.0, b=("cada", 0), lines=[("Cuando todo falla,", "l", ("cuando", 0)), ("confiable", "b", ("confiable", 0))]),
           dict(a=("chat", 0), b=("puedes", 0), lines=[("Chat", "b", ("chat", 0)), ("llamada", "b", ("llamada", 0)), ("videollamada", "b", ("videollamada", 0))]),
           dict(a=("gratis", 0), b=("te", 0), lines=[("Gratis e", "l", ("gratis", 0)), ("ilimitadas", "b", ("ilimitadas", 0))])],
    tags=[dict(a=("botón", 0), b=("lo", 0), name="Gurú"),
          dict(a=("presentamos", 0), b=("pide", 0), name="Gurú")],
    color=None,
    cierre=dict(word=("pide", 0), grafico=True, slogan=False, lines=[],
                texto="Pide tu **cotización** y te contamos qué incluye **Gurú** desde el primer día")),
"INTA37": dict(tema=dict(EDU, kw=["pizarra", "escribe", "write", "dibuja", "marcador", "docente"]),
    ov=[], color=None,
    cierre=dict(word=("pero", 1), slogan=False, lines=[("Te agendamos una", "l"), ("demostración sin costo", "b")])),
}


# INTA25 se arma con las voces del caso (armar_caso25.py escribe spec_caso.json: sin narrador, anclas sobre las palabras de los entrevistados)
import json as _j
from pathlib import Path as _P
_f = _P(r"D:\OneScreen\Contenido\2026\10. Octubre\INTA25\Proyecto\spec_caso.json")
if _f.exists():
    _s = _j.loads(_f.read_text(encoding="utf-8"))
    SPECS["INTA25"] = dict(tema=SPECS["INTA25"]["tema"],
                           ov=[ov(tuple(o["a"]), tuple(o["b"]), *[tuple(x) for x in o["lines"]], pos=o["pos"]) for o in _s["ov"]],
                           color=dict(a=tuple(_s["color"]["a"]), b=tuple(_s["color"]["b"]), lines=[tuple(x) for x in _s["color"]["lines"]]),
                           cierre=dict(word=tuple(_s["cierre"]["word"]), slogan=False, lines=[tuple(x) for x in _s["cierre"]["lines"]]))
