"""GUION → IDEAS DE MOTION (automático). Para cada frase del guion detecta qué IDEA ABSTRACTA contiene (rapidez, confianza, siempre, gratis, equipo, orden, avance…)
y propone METÁFORAS VISUALES en animación abstracta (una estela que acelera, anillos que se cierran, un lazo infinito, caos que se ordena…), ya compuestas con el
vocabulario de elementos.py y con el estilo de las referencias. Cada frase sale con 2 ideas distintas (los 2 motion designs de cada toma del storyboard; 3 planos + 2 motion = 5 opciones).

Uso:  python estudio-video/motion/ideas.py GUION.txt [--html SALIDA.html] [--spec SPEC.json]
  GUION.txt: una frase por línea (opcional «t0-t1 | frase» con segundos). Sin tiempos se estiman por palabras.
  --html: página para ver las ideas por frase (frase, conceptos detectados, 3 pantallazos con su idea).
  --spec: SPEC del storyboard (solo las opciones de motion; los planos se agregan después, ver CLAUDE.md paso 9b).

Es determinista y no consulta nada. Para una frase con una idea que el léxico no conoce, Claude compone la escena a mano con escena() y, si la idea se repite,
la agrega aquí (CONCEPTOS) para que la próxima vez salga sola."""
import json
import re
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "herramientas"))
import plantillas  # noqa: E402,F401
import elementos   # noqa: E402
from boceto import boceto_svg, revisar  # noqa: E402


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


# ---------------- ARTE por idea: cada función recibe (ctx, R=(x, y, w, h)) y devuelve elementos ----------------
def _c(R):
    return R[0] + R[2] / 2, R[1] + R[3] / 2


def a_estela(ctx, R):
    x, y, w, h = R
    pts = [(x + 20, y + h * 0.9), (x + w * 0.3, y + h * 0.82), (x + w * 0.55, y + h * 0.62), (x + w * 0.8, y + h * 0.3), (x + w - 20, y + h * 0.1)]
    return [{"e": "curva", "puntos": pts, "neon": True, "final": True, "sw": 9, "base": y + h}, {"e": "burbuja", "x": x + w * 0.45, "y": y + h * 0.15, "t": ctx["cifra"] or "en minutos"},
            {"e": "destello", "x": x + w * 0.2, "y": y + h * 0.3, "s": 26, "fill": "#ffffff"}]


def a_reloj(ctx, R):
    cx, cy = _c(R)
    r = min(R[2], R[3]) * 0.36
    return [{"e": "anillos", "x": cx, "y": cy, "radios": [r + 60, r + 120], "estilo": "fino"}, {"e": "arco", "x": cx, "y": cy, "r": r, "frac": 0.75, "t": ctx["cifra"] or "", "s": int(r * 0.7)}]


def a_escudo(ctx, R):
    cx, cy = _c(R)
    m = min(R[2], R[3])
    return [{"e": "anillos", "x": cx, "y": cy, "radios": [m * 0.18, m * 0.3, m * 0.42], "estilo": "fino"}, {"e": "punto", "x": cx, "y": cy, "r": 26, "glow": True},
            {"e": "icono", "nombre": "check", "x": cx, "y": cy, "s": 50, "tono": "blanco"}, {"e": "destello", "x": cx + m * 0.36, "y": cy - m * 0.3, "s": 24, "fill": "#ffffff"}]


def a_infinito(ctx, R):
    cx, cy = _c(R)
    return [{"e": "infinito", "x": cx, "y": cy, "w": min(R[2] * 0.85, 460)}]


def a_gratis(ctx, R):
    cx, cy = _c(R)
    return [{"e": "fantasma", "x": R[0] + 10, "y": R[1] + R[3] * 0.85, "t": "$0", "s": int(R[3] * 0.95)}, {"e": "linea", "x1": R[0] + 20, "y1": R[1] + R[3] * 0.8, "x2": R[0] + R[2] - 20, "y2": R[1] + R[3] * 0.15, "sw": 10, "op": 0.9, "tono": "acc"},
            {"e": "burbuja", "x": cx - 70, "y": R[1] + R[3] * 0.82, "t": "sin costo"}]


def a_equipo(ctx, R):
    x, y, w, h = R
    f = []
    for k in range(5):
        px, py = x + w * (0.12 + 0.19 * k), y + h * (0.62 - 0.12 * (1 - abs(k - 2) / 2))
        f += ([{"e": "punto", "x": px, "y": py, "r": 46, "glow": True}] if k == 2 else []) + [{"e": "icono", "nombre": "persona", "x": px, "y": py, "s": 62 if k == 2 else 52, "tono": "blanco" if k == 2 else "ink"}]
    return f + [{"e": "destello", "x": x + w * 0.5, "y": y + h * 0.2, "s": 28, "fill": "#ffffff"}]


def a_crecimiento(ctx, R):
    x, y, w, h = R
    return [{"e": "escalera", "x": x + 10, "y": y + h * 0.95, "w": w - 20, "h": h * 0.7, "n": 5}, {"e": "curva", "puntos": [(x + 40, y + h * 0.7), (x + w * 0.4, y + h * 0.55), (x + w * 0.7, y + h * 0.3), (x + w - 40, y + h * 0.08)], "area": False, "neon": True, "final": True, "sw": 7}]


def a_ahorro(ctx, R):
    x, y, w, h = R
    return [{"e": "barras", "x": x + 20, "y": y + h * 0.92, "valores": [100, 78, 58, 38, 22], "ancho": w / 7, "alto": h * 0.7, "sep": w / 14, "resalta": 4}, {"e": "burbuja", "x": x + w * 0.55, "y": y + h * 0.1, "t": ctx["cifra"] or "menos"}]


def a_aprendizaje(ctx, R):
    x, y, w, h = R
    return [{"e": "escalera", "x": x + 10, "y": y + h * 0.95, "w": w - 20, "h": h * 0.6, "n": 4}, {"e": "icono", "nombre": "doc", "x": x + w - 60, "y": y + h * 0.2, "s": 70, "tono": "acc"}, {"e": "destello", "x": x + w - 60, "y": y + h * 0.06, "s": 24, "fill": "#ffffff"}]


def a_soporte(ctx, R):
    x, y, w, h = R
    return [{"e": "notificacion", "x": x, "y": y + h * 0.28, "w": w, "h": 150, "titulo": "Soporte", "t": "Aquí estoy, cuéntame", "n": 20, "hora": "ahora", "icono": "auriculares"},
            {"e": "burbuja", "x": x + w * 0.55, "y": y + h * 0.12, "t": "en línea"}, {"e": "cursor", "x": x + w * 0.7, "y": y + h * 0.78, "nombre": "Tú"}]


def a_orden(ctx, R):
    x, y, w, h = R
    return [{"e": "desorden", "x": x, "y": y + h * 0.25, "w": w * 0.42, "h": h * 0.5, "n": 10, "semilla": 6}, {"e": "flecha", "puntos": [(x + w * 0.46, y + h * 0.5), (x + w * 0.54, y + h * 0.5)], "sw": 6},
            {"e": "desorden", "x": x + w * 0.58, "y": y + h * 0.25, "w": w * 0.42, "h": h * 0.5, "n": 12, "orden": True}]


def a_simple(ctx, R):
    cx, cy = _c(R)
    return [{"e": "anillos", "x": cx, "y": cy, "radios": [110, 190, 270], "estilo": "fino"}, {"e": "boton", "x": cx, "y": cy + 14, "t": "un botón", "estilo": "blanca", "s": 44, "centrada": True}, {"e": "cursor", "x": cx + 40, "y": cy + 30}]


def a_tecnologia(ctx, R):
    x, y, w, h = R
    return [{"e": "particulas", "x": x, "y": y + h * 0.1, "w": w, "h": h * 0.55, "n": 60, "orden": True}, {"e": "onda", "x": x, "y": y + h * 0.82, "w": w, "amp": 34, "ciclos": 3, "neon": True}, {"e": "destello", "x": x + w * 0.8, "y": y + h * 0.15, "s": 30, "fill": "#ffffff"}]


def a_pregunta(ctx, R):
    x, y, w, h = R
    cx, _ = _c(R)
    return [{"e": "fantasma", "x": cx - 130, "y": y + h * 0.8, "t": "?", "s": int(h * 0.95), "op": 0.2}, {"e": "boton", "x": x + w * 0.25, "y": y + h * 0.9, "t": "SÍ", "estilo": "blanca", "s": 40, "centrada": True}, {"e": "boton", "x": x + w * 0.7, "y": y + h * 0.9, "t": "NO", "estilo": "acento", "s": 40, "centrada": True}]


def a_cifra(ctx, R):
    x, y, w, h = R
    return [{"e": "fantasma", "x": x - 10, "y": y + h * 0.78, "t": ctx["cifra"] or "100", "s": int(h * 0.85), "op": 0.2}, {"e": "curva", "puntos": [(x + 20, y + h * 0.85), (x + w * 0.4, y + h * 0.6), (x + w - 30, y + h * 0.2)], "neon": True, "final": True, "area": False, "sw": 8}]


def a_pantalla(ctx, R):
    x, y, w, h = R
    return [{"e": "blanca", "x": x, "y": y + h * 0.15, "w": w, "h": h * 0.62, "r": 24}, {"e": "icono", "nombre": "pantalla", "x": x + w * 0.5, "y": y + h * 0.42, "s": 90, "tono": "acc"}, {"e": "cursor", "x": x + w * 0.6, "y": y + h * 0.55, "nombre": "Docente"}]


def a_conexion(ctx, R):
    x, y, w, h = R
    cy = y + h * 0.5
    return [{"e": "icono", "nombre": "pantalla", "x": x + w * 0.1, "y": cy, "s": 90, "tono": "acc"}, {"e": "icono", "nombre": "persona", "x": x + w * 0.9, "y": cy, "s": 90, "tono": "acc"},
            {"e": "onda", "x": x + w * 0.22, "y": cy, "w": w * 0.56, "amp": 36, "ciclos": 2, "neon": True}, {"e": "destello", "x": x + w * 0.5, "y": cy - 70, "s": 24, "fill": "#ffffff"}]


def a_contacto(ctx, R):
    cx, cy = _c(R)
    return [{"e": "boton", "x": cx - 40, "y": cy + 40, "t": "escríbenos", "estilo": "blanca", "s": 46, "centrada": True}, {"e": "burbuja", "x": cx + 90, "y": cy - 120, "t": "¡hola!"},
            {"e": "flecha", "puntos": [(cx + 150, cy - 60), (cx + 150, cy - 10), (cx + 100, cy + 10)], "sw": 6, "r": 20}, {"e": "destello", "x": cx - 200, "y": cy - 90, "s": 26, "fill": "#ffffff"}]


def a_ancla(ctx, R):
    cx, cy = _c(R)
    return [{"e": "onda", "x": R[0], "y": cy, "w": R[2], "amp": 26, "ciclos": 3, "neon": True}, {"e": "punto", "x": cx, "y": cy, "r": 28, "glow": True}, {"e": "icono", "nombre": "check", "x": cx, "y": cy, "s": 46, "tono": "blanco"}]


# ---------------- LÉXICO: idea abstracta → raíces + metáforas ----------------
# (id, descripción de la ANIMACIÓN ABSTRACTA, arte)
CONCEPTOS = [
    {"nombre": "rapidez", "peso": 1.5, "raices": ["rapid", "minuto", "segundo", "inmediat", "instant", "veloc", "enseguida", "pronto", "al momento", "sin espera", "ya mismo"], "tema": "solucion", "ideas": [
        ("estela", "La rapidez como una estela: una línea de neón acelera desde la esquina dejando rastro y llega a un punto que late; el tiempo se «comprime» en una burbuja.", a_estela),
        ("reloj", "El tiempo como un anillo que se llena: un arco recorre el círculo a toda velocidad y se detiene justo en la palabra clave.", a_reloj)]},
    {"nombre": "siempre", "peso": 1.2, "raices": ["siempre", "vitalici", "ilimitad", "24", "todos los dias", "sin limite", "nunca", "permanent", "de por vida"], "tema": "solucion", "ideas": [
        ("infinito", "Lo que no se acaba como un lazo infinito: una línea de neón dibuja un ocho sin cortes y un punto de luz la recorre para siempre.", a_infinito),
        ("reloj", "La disponibilidad como un anillo que nunca termina de cerrarse: el arco da vueltas continuas alrededor de la cifra.", a_reloj)]},
    {"nombre": "confianza", "peso": 1.2, "raices": ["confiab", "confianz", "segur", "garant", "respald", "protec", "firme", "solid", "cuando todo falla"], "tema": "solucion", "ideas": [
        ("escudo", "La confianza como anillos que se cierran: tres círculos concéntricos se dibujan hacia un punto central que se enciende con un check; protección en capas.", a_escudo),
        ("ancla", "Lo firme como un núcleo estable: ondas que se expanden pero el centro no se mueve.", a_ancla)]},
    {"nombre": "gratis", "peso": 2.0, "raices": ["gratis", "sin costo", "sin cargo", "sin tickets", "sin pagar", "incluid", "cero", "gratuit"], "tema": "solucion", "ideas": [
        ("gratis", "Lo gratuito como un precio que se desvanece: un «$0» enorme en contorno se tacha con una línea de acento y la burbuja «sin costo» cae sobre él.", a_gratis)]},
    {"nombre": "equipo", "peso": 0.8, "raices": ["equipo", "todos", "docente", "familia", "comunidad", "juntos", "colabor", "personas", "toda tu", "institucion", "colegio"], "tema": "explicar", "ideas": [
        ("equipo", "El equipo como personas que se encienden: cinco figuras aparecen una a una con la voz y la central se ilumina con un halo cuando se nombra a todos.", a_equipo)]},
    {"nombre": "conexion", "peso": 0.9, "raices": ["conect", "integra", "une ", "juntar", "comunic", "videollamada", "llamada", "chat", "canal"], "tema": "solucion", "ideas": [
        ("conexion", "La conexión como una señal que viaja: una onda de neón sale de la pantalla y llega a la persona, y un destello recorre el trayecto.", a_conexion)]},
    {"nombre": "avance", "raices": ["crece", "crecimiento", "aument", "mejora", "avanza", "evoluciona", "escala", "mas ", "progres", "resultado"], "tema": "explicar", "ideas": [
        ("escalera", "El avance como escalones que suben: cada peldaño aparece con la voz y una línea de neón sube hasta el punto más alto.", a_crecimiento)]},
    {"nombre": "ahorro", "raices": ["ahorr", "menos", "reduc", "disminu", "baja", "recort"], "tema": "explicar", "ideas": [
        ("barras_bajan", "El ahorro como barras que descienden: cada barra es más corta que la anterior y la última, la más pequeña, se enciende.", a_ahorro)]},
    {"nombre": "aprendizaje", "raices": ["capacit", "formaci", "aprend", "certific", "curso", "ense", "academy", "ruta de aprendizaje", "agenda"], "tema": "explicar", "ideas": [
        ("peldanos", "Aprender como subir peldaños: escalones que se llenan uno a uno hasta un documento que brilla en la cima (el certificado).", a_aprendizaje)]},
    {"nombre": "soporte", "peso": 0.8, "raices": ["soporte", "ayuda", "ingeniero", "atencion", "asisten", "resuelv", "acompan", "responde", "tecnic"], "tema": "solucion", "ideas": [
        ("respuesta", "La ayuda como un aviso que llega: una notificación cae con una pila de capas, aparece «en línea» y un cursor la abre.", a_soporte)]},
    {"nombre": "orden", "raices": ["falla", "error", "problema", "caos", "complic", "papeleo", "desorden", "tramite", "se cae", "dolor", "todo en un solo", "ordena", "organiza"], "tema": "explicar", "ideas": [
        ("caos_orden", "Del desorden al orden: formas rotadas y dispersas se alinean en una cuadrícula limpia al pasar la flecha.", a_orden)]},
    {"nombre": "sencillez", "raices": ["boton", "facil", "sencill", "simple", "un clic", "un click", "directo", "sin complic"], "tema": "solucion", "ideas": [
        ("boton", "Lo simple como un solo botón: anillos de onda salen del botón cuando el cursor hace clic, y todo lo demás queda en calma.", a_simple)]},
    {"nombre": "tecnologia", "raices": ["ia ", "inteligen", "automat", "digital", "tecnolog", "transcrib", "app ", "plataforma", "software"], "tema": "solucion", "ideas": [
        ("particulas", "La tecnología como puntos que se ordenan solos: una nube de partículas se alinea en cuadrícula y una onda de señal las atraviesa.", a_tecnologia)]},
    {"nombre": "contacto", "raices": ["escrib", "whatsapp", "contact", "llamanos", "cotiz", "pide ", "pidelo", "solicita", "visita", "escribenos"], "tema": "solucion", "peso": 1.4, "ideas": [
        ("mensaje", "El llamado a la acción como un mensaje que sale: una burbuja de chat despega del botón «escríbenos» y una flecha se dibuja hacia el contacto.", a_contacto)]},
    {"nombre": "pregunta", "raices": ["?", "pregunt", "duda", "ya tienes", "sabias", "como "], "tema": "explicar", "ideas": [
        ("pregunta", "La pregunta como un signo gigante en contorno: «¿?» late de fondo y dos botones rectangulares, SÍ y NO, esperan la respuesta.", a_pregunta)]},
    {"nombre": "cifra", "raices": [], "tema": "explicar", "ideas": [
        ("cifra", "El dato como número fantasma: la cifra gigante en contorno aparece detrás y una curva de neón sube hasta ella.", a_cifra)]},
    {"nombre": "aula", "raices": ["pantalla", "interactiv", "aula", "clase", "pizarra", "tablero", "salon", "estudiant"], "tema": "explicar", "ideas": [
        ("pantalla", "La pantalla como una ventana a la clase: un marco blanco con un ícono de pantalla y un cursor de docente que la activa.", a_pantalla)]},
]

LUCES = ["abajo", "arriba-der", "abajo-der", "centro", "izquierda", "arriba"]
LAYOUTS = ["izq", "der", "centro"]


def analizar(frase):
    n = " " + norm(frase) + " "
    cifra = re.search(r"\+?\d[\d.,]*\s?(?:%|/\d+|[a-z]+)?", frase)
    ctx = {"frase": frase.strip(), "n": n, "cifra": cifra.group(0).strip() if cifra and re.search(r"\d", cifra.group(0)) else None, "gurú": "guru" in n}
    hits = []
    for c in CONCEPTOS:
        raices = [r for r in c["raices"] if r in n]
        if c["nombre"] == "cifra" and ctx["cifra"]:
            raices = [ctx["cifra"]]
        if raices:
            hits.append((len(raices) * c.get("peso", 1.0) + (0.5 if c["nombre"] == "cifra" else 0), c, raices))
    hits.sort(key=lambda h: -h[0])
    ctx["hits"] = hits
    # palabra clave: la raíz más larga detectada, o la última palabra significativa
    palabras = [w for w in re.findall(r"[\wáéíóúñü%$+/]+", frase) if len(norm(w)) > 3]
    clave = None
    for _, c, rs in hits:
        for w in palabras:
            if any(r.strip() and r.strip() in norm(w) for r in rs):
                clave = w
                break
        if clave:
            break
    ctx["clave"] = clave or (palabras[-1] if palabras else frase.split()[-1])
    return ctx


def recorte(frase, clave, maximo=8):
    pal = frase.split()
    if len(pal) <= maximo:
        return frase
    k = next((i for i, w in enumerate(pal) if clave and clave.lower() in w.lower()), len(pal) // 2)
    a = max(0, min(k - maximo // 2, len(pal) - maximo))
    return " ".join(pal[a:a + maximo])


def titulo_elementos(ctx, layout, y_ancla=None):
    txt = recorte(ctx["frase"].rstrip(".!¿?"), ctx["clave"])
    pal = txt.split()
    if layout == "centro":
        mitad = (len(pal) + 1) // 2
        l1, l2 = " ".join(pal[:mitad]), " ".join(pal[mitad:])
        return [{"e": "titulo", "x": 640, "y": 170, "s": 64, "a": "middle", "ancho": 1000, "lineas": [[l1, 300]] + ([[l2, 700, "grad"]] if l2 else [])}]
    lineas, act = [], ""
    for w in pal:
        if len(act) + len(w) + 1 > 18 and act:
            lineas.append(act)
            act = w
        else:
            act = (act + " " + w).strip()
    lineas.append(act)
    lineas = lineas[:4]
    estructura = [[ln, 300] for ln in lineas[:-1]] + [[lineas[-1], 700, "grad"]]
    x = 100 if layout == "izq" else 700
    return [{"e": "titulo", "x": x, "y": 330 - 30 * (len(lineas) - 1), "s": 80, "ancho": 520 if layout == "izq" else 480, "lineas": estructura}]


def componer(ctx, arte, layout, luz, tema):
    R = {"izq": (660, 110, 520, 500), "der": (80, 110, 520, 500), "centro": (200, 270, 880, 400)}[layout]
    return {"tema": tema, "fondo": {"luz": luz}, "elementos": titulo_elementos(ctx, layout) + arte(ctx, R)}


def tema_de(ctx, concepto):
    if ctx["gurú"]:
        return "gurú"
    return concepto["tema"] if concepto else "solucion"


def ideas_para(frase, i, luz_prev=None, idea_prev=None):
    """2 ideas para una frase: [{'idea', 'texto', 'por', 'escena', 'fav'}]"""
    ctx = analizar(frase)
    cand = []
    vistos = set()
    for sc, c, rs in ctx["hits"]:
        for nid, texto, arte in c["ideas"]:
            if nid not in vistos:
                vistos.add(nid)
                cand.append((c, nid, texto, arte, ", ".join(r.strip() for r in rs)))
    if idea_prev and len(cand) > 1 and cand[0][1] == idea_prev:
        cand = cand[1:] + cand[:1]
    # relleno: ideas genéricas pero válidas, siempre una tipográfica estilo Apple
    genericas = [(None, "tipografia", "Solo la frase, como Apple: las palabras suben una a una y la palabra clave se enciende con degradado; la aurora respira detrás.", lambda c_, R: [{"e": "destello", "x": R[0] + R[2] * 0.85, "y": R[1] + 40, "s": 30, "fill": "#ffffff"}, {"e": "anillos", "x": R[0] + R[2] / 2, "y": R[1] + R[3] / 2, "radios": [90, 170, 250], "estilo": "fino"}], "—"),
                 (None, "particulas", "Idea abstracta de fondo: puntos que se ordenan solos en una cuadrícula, orden naciendo de la nada.", a_tecnologia, "—")]
    for g in genericas:
        if g[1] not in vistos:
            cand.append(g)
    out = []
    for j, (c, nid, texto, arte, por) in enumerate(cand[:2]):
        layout = LAYOUTS[(i + j) % 3]
        luz = LUCES[(i * 2 + j) % len(LUCES)]
        if luz == luz_prev:
            luz = LUCES[(LUCES.index(luz) + 1) % len(LUCES)]
        tema = tema_de(ctx, c)
        escena = componer(ctx, arte, layout, luz, tema)
        out.append({"id": nid, "idea": texto, "por": por, "layout": layout, "luz": luz, "tema": tema, "escena": escena, "fav": j == 0})
    return out, ctx


def leer_guion(ruta):
    tomas, t = [], 0.0
    for k, ln in enumerate(l.strip() for l in Path(ruta).read_text(encoding="utf-8").splitlines() if l.strip() and not l.strip().startswith("#")):
        m = re.match(r"^(\d+(?:[.,]\d+)?)\s*-\s*(\d+(?:[.,]\d+)?)\s*\|\s*(.+)$", ln)
        if m:
            t0, t1, fr = float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", ".")), m.group(3)
        else:
            fr = ln
            t0, t1 = t, t + max(1.5, 0.38 * len(fr.split()))
        t = t1
        tomas.append({"id": f"S{k + 1:02d}", "t0": round(t0, 2), "t1": round(t1, 2), "voz": fr})
    return tomas


def generar(ruta):
    tomas = leer_guion(ruta)
    luz_prev, idea_prev, res = None, None, []
    for i, tm in enumerate(tomas):
        ops, ctx = ideas_para(tm["voz"], i, luz_prev, idea_prev)
        luz_prev, idea_prev = ops[0]["luz"], ops[0]["id"]
        res.append((tm, ops, ctx))
    return res


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    res = generar(a[0])
    html_p = a[a.index("--html") + 1] if "--html" in a else None
    spec_p = a[a.index("--spec") + 1] if "--spec" in a else None
    cards = []
    for tm, ops, ctx in res:
        conceptos = ", ".join(f"{c['nombre']} ({', '.join(r.strip() for r in rs)})" for _, c, rs in ctx["hits"]) or "ninguno (se usa lo genérico)"
        print(f"{tm['id']} · {tm['voz']}\n   conceptos: {conceptos}")
        vistas = []
        for o in ops:
            av = revisar(o["escena"] and elementos.escena(o["escena"])[0])
            print(f"   {'★' if o['fav'] else ' '} {o['id']:<11} [{o['tema']}, luz {o['luz']}, {o['layout']}] {'AVISO ' + '; '.join(av) if av else ''}")
            svg = boceto_svg(elementos.escena(o["escena"])[0]).replace("<svg ", "<svg style='width:100%;display:block;border-radius:8px' ", 1)
            vistas.append(f"<div>{svg}<p><b>{'★ ' if o['fav'] else ''}{o['id']}</b> · {o['idea']}<br><small>por: {o['por']}</small></p></div>")
        cards.append(f"<section><h3>{tm['id']} · {tm['t0']}-{tm['t1']} s</h3><p class='fr'>{tm['voz']}</p><p><small>Conceptos: {conceptos}</small></p><div class='tres'>{''.join(vistas)}</div></section>")
    if html_p:
        Path(html_p).write_text('<!doctype html><meta charset="utf-8"><title>Ideas de motion del guion</title><style>body{font:15px/1.4 Manrope,system-ui,sans-serif;background:#12151b;color:#eceff6;margin:0;padding:24px}'
                                'section{background:#1b2029;border:1px solid #2c313d;border-radius:14px;padding:14px;margin:14px 0}h3{margin:0;color:#8fb4ff}.fr{font-size:20px;margin:6px 0}p{margin:4px 0}small{color:#9aa3b5}'
                                '.tres{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:8px}@media(max-width:1000px){.tres{grid-template-columns:1fr}}</style>'
                                f'<h1>Ideas de motion del guion ({len(res)} frases)</h1>' + "".join(cards), encoding="utf-8")
        print("html:", html_p)
    if spec_p:
        tomas = [dict(tm, opciones=[{"tipo": "motion", "escena": o["escena"], "desc": o["idea"], "fav": o["fav"]} for o in ops]) for tm, ops, _ in res]
        Path(spec_p).write_text(json.dumps({"videos": [{"id": "IDEAS", "titulo": "Ideas de motion del guion", "tomas": tomas}]}, ensure_ascii=False, indent=1), encoding="utf-8")
        print("spec:", spec_p)


if __name__ == "__main__":
    main()
