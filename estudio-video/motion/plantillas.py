"""Plantillas de motion graphics de OneScreen (biblioteca única; v3 del 28-oct-2026).

Historia: v1 «plantilluda de PowerPoint» (Cris la rechazó). v3 mezcla DOS fuentes reales:
  1. Lettering de Apple, medido en fotogramas del video «Apple Event 2018 in 108 seconds» (solo tipografía): UNA frase corta por beat (1-3 palabras),
     tamaño medio con mucho negro/blanco alrededor, tipografía bold de tracking cerrado, las palabras entran una a una, fondos que alternan negro/blanco,
     y el NOMBRE de la función lleva el texto con DEGRADADO (Super Retina cálido, Liquid Retina azul-violeta); texto montado sobre la imagen del producto.
  2. El lenguaje propio de OneScreen que Cris mostró (cotización Gurú/Academy): fondos con degradado profundo (verde Gurú, azul Academy) + textura
     (puntos o rejilla fina), tarjetas de VIDRIO (relleno translúcido + borde fino), íconos de línea, kicker en mayúsculas con ícono, título grande blanco
     y texto de apoyo atenuado, regla fina arriba.
Cada plantilla = un TIPO DE FRASE con parámetros y un `tema` (azul | verde | oscuro | claro). Dos caras con los mismos parámetros: boceto(params)
(pantallazo del storyboard, listo) y build(params,…) para HyperFrames (se implementa al primer uso; ver gfx_inta.py y estilo-onescreen/motion/fx.js)."""
import math

AZ, NE, AC, GR = "#3976ff", "#1a1a1a", "#7d00ba", "#c9ced8"
L = 100   # margen izquierdo (de los 1280 px)

TEMAS = {
    "azul":   dict(fondo={"grad": ["#2f6bea", "#0b2166"], "ang": 150, "tex": "rejilla", "luces": [[260, 780, 640, "#8fb4ff", 0.38], [1100, 0, 520, "#5b8cff", 0.22]], "grano": 0.14}, ink="#ffffff", mut="#c4d6ff", acc="#8fb4ff", tg=["#ffffff", "#9fc0ff"], oscuro=True),
    "verde":  dict(fondo={"grad": ["#0a5c34", "#3bb56d"], "ang": 150, "tex": "puntos", "luces": [[260, 790, 660, "#7dffb5", 0.40], [1120, 0, 520, "#35e08f", 0.24]], "grano": 0.14}, ink="#ffffff", mut="#cdeedd", acc="#35e08f", tg=["#ffffff", "#a7f3c8"], oscuro=True),
    "oscuro": dict(fondo={"grad": ["#1c1c1e", "#050505"], "ang": 160, "tex": "rejilla", "luces": [[900, 200, 560, "#3976ff", 0.16]], "grano": 0.12}, ink="#ffffff", mut="#9aa3b5", acc="#3976ff", tg=["#6fa2ff", "#c58bff"], oscuro=True),
    "claro":  dict(fondo={"grad": ["#ffffff", "#e8effc"], "ang": 160, "tex": "puntos", "texc": AZ, "texop": 0.07, "luces": [[640, 820, 720, AZ, 0.20], [1180, 0, 460, "#7a5cff", 0.12]]}, ink=NE, mut="#5d667a", acc=AZ, tg=[AZ, "#7a5cff"], oscuro=False),
}


ALIAS = {"gurú": "verde", "guru": "verde", "solucion": "azul", "solución": "azul", "explicar": "claro", "blanco": "claro", "enseñar": "claro"}


def tema(p, defecto):
    """Color por SIGNIFICADO (Cris, 28-oct): verde = solo cosas de Gurú; azul = solución; blanco = cuando exponemos o enseñamos algo."""
    k = p.get("tema", defecto)
    return TEMAS[ALIAS.get(k, k)]


def t(x, y, s, texto, fill="#1a1a1a", w=700, a="start", ls=0, grad=None, op=None):
    d = {"k": "txt", "x": x, "y": y, "s": s, "w": w, "fill": fill, "t": texto, "a": a, "ls": ls}
    if grad:
        d["grad"] = grad
    if op is not None:
        d["op"] = op
    return d


def _fs(texto, ancho, max_s, k=0.52):
    return int(min(max_s, ancho / (k * max(len(str(texto)), 1))))


def wrap(texto, n):
    out, lin = [], ""
    for w in str(texto).split():
        if len(lin) + len(w) + 1 > n and lin:
            out.append(lin)
            lin = w
        else:
            lin = (lin + " " + w).strip()
    return out + ([lin] if lin else [])


def vidrio(x, y, w, h, th, r=20):
    """tarjeta de vidrio: relleno translúcido + borde fino (como las tarjetas de la cotización)"""
    return {"k": "rect", "x": x, "y": y, "w": w, "h": h, "r": r, "fill": th["ink"], "op": 0.10 if th["oscuro"] else 0.05, "st": th["ink"], "sw": 1, "sop": 0.18,
            "glow": th["acc"], "brillo": True}


def kicker(texto, th, y=110, icono_n=None):
    """Ya no hay etiquetas en MAYÚSCULA tipo diapositiva (Cris, 28-oct): un título opcional es una frase normal, en negrita, sin adornos."""
    return [t(L, y + 24, 50, texto, th["ink"], 700, "start", -2)]


def regla(th, y=100):
    return {"k": "linea", "x1": L, "y1": y, "x2": 1180, "y2": y, "fill": th["ink"], "sw": 2, "op": 0.35}


def orbita(cx, cy, rx, ry, th, rot=-8):
    """órbita fina alrededor del texto con un destello de 4 puntas (referencia «Creative success…»)"""
    return [{"k": "elip", "x": cx, "y": cy, "rx": rx, "ry": ry, "rot": rot, "st": th["ink"], "sw": 2, "sop": 0.8},
            {"k": "estrella", "x": cx + rx - 14, "y": cy - int(ry * 0.78), "s": 30, "fill": th["ink"]}]


def puntos_paso(i, n, th):
    """indicador de progreso 01 02 03 04 (referencias 6 y 7): el activo se alarga"""
    f, x = [], 640 - (n * 34) // 2
    for k in range(n):
        act = k == i
        f.append({"k": "circ", "x": x + (9 if act else 5), "y": 46, "r": 9 if act else 5, "fill": th["ink"], "op": 0.95 if act else 0.35})
        x += (18 if act else 10) + 14
    return f


# ---- íconos de línea (trazo redondeado, sin relleno) ----
def icono(nombre, cx, cy, s, col="#1a1a1a"):
    sw = max(5, int(s * 0.07))
    r = s / 2
    if nombre == "persona":
        return [{"k": "circ", "x": cx, "y": cy - int(s * .22), "r": int(s * .2), "st": col, "sw": sw},
                {"k": "path", "d": f"M{cx - int(s * .4)} {cy + int(r)} Q{cx - int(s * .4)} {cy + int(s * .06)} {cx} {cy + int(s * .06)} Q{cx + int(s * .4)} {cy + int(s * .06)} {cx + int(s * .4)} {cy + int(r)}", "fill": col, "sw": sw}]
    if nombre == "grupo":
        return icono("persona", cx - int(s * .22), cy, int(s * .7), col) + icono("persona", cx + int(s * .22), cy, int(s * .7), col)
    if nombre == "pantalla":
        return [{"k": "rect", "x": cx - int(r), "y": cy - int(s * .4), "w": s, "h": int(s * .68), "r": int(s * .08), "st": col, "sw": sw},
                {"k": "path", "d": f"M{cx - int(s * .22)} {cy + int(s * .44)} L{cx + int(s * .22)} {cy + int(s * .44)} M{cx} {cy + int(s * .28)} L{cx} {cy + int(s * .44)}", "fill": col, "sw": sw}]
    if nombre == "doc":
        x0, y0, w_, h_ = cx - int(s * .32), cy - int(r), int(s * .64), s
        return [{"k": "path", "d": f"M{x0} {y0 + 12} Q{x0} {y0} {x0 + 12} {y0} L{x0 + w_ - 26} {y0} L{x0 + w_} {y0 + 26} L{x0 + w_} {y0 + h_ - 12} Q{x0 + w_} {y0 + h_} {x0 + w_ - 12} {y0 + h_} L{x0 + 12} {y0 + h_} Q{x0} {y0 + h_} {x0} {y0 + h_ - 12} Z", "fill": col, "sw": sw},
                {"k": "path", "d": f"M{x0 + 16} {cy - 4} L{x0 + w_ - 16} {cy - 4} M{x0 + 16} {cy + int(s * .16)} L{x0 + w_ - 34} {cy + int(s * .16)}", "fill": col, "sw": sw}]
    if nombre == "chat":
        return [{"k": "path", "d": f"M{cx - int(r)} {cy - int(s * .12)} Q{cx - int(r)} {cy - int(s * .42)} {cx - int(s * .2)} {cy - int(s * .42)} L{cx + int(s * .2)} {cy - int(s * .42)} Q{cx + int(r)} {cy - int(s * .42)} {cx + int(r)} {cy - int(s * .12)} L{cx + int(r)} {cy + int(s * .08)} Q{cx + int(r)} {cy + int(s * .3)} {cx + int(s * .2)} {cy + int(s * .3)} L{cx - int(s * .02)} {cy + int(s * .3)} L{cx - int(s * .26)} {cy + int(s * .48)} L{cx - int(s * .24)} {cy + int(s * .3)} Q{cx - int(r)} {cy + int(s * .28)} {cx - int(r)} {cy + int(s * .06)} Z", "fill": col, "sw": sw}]
    if nombre == "check":
        return [{"k": "circ", "x": cx, "y": cy, "r": int(r), "st": col, "sw": sw}, {"k": "path", "d": f"M{cx - int(s * .22)} {cy + 2} L{cx - int(s * .05)} {cy + int(s * .18)} L{cx + int(s * .26)} {cy - int(s * .16)}", "fill": col, "sw": sw + 1}]
    if nombre == "globo":
        return [{"k": "circ", "x": cx, "y": cy, "r": int(r), "st": col, "sw": sw},
                {"k": "path", "d": f"M{cx - int(r)} {cy} L{cx + int(r)} {cy} M{cx} {cy - int(r)} Q{cx - int(s * .36)} {cy} {cx} {cy + int(r)} Q{cx + int(s * .36)} {cy} {cx} {cy - int(r)}", "fill": col, "sw": sw}]
    if nombre == "auriculares":
        return [{"k": "path", "d": f"M{cx - int(r)} {cy + int(s * .1)} Q{cx - int(r)} {cy - int(r)} {cx} {cy - int(r)} Q{cx + int(r)} {cy - int(r)} {cx + int(r)} {cy + int(s * .1)}", "fill": col, "sw": sw},
                {"k": "rect", "x": cx - int(r) - 2, "y": cy + int(s * .02), "w": int(s * .22), "h": int(s * .36), "r": 10, "st": col, "sw": sw},
                {"k": "rect", "x": cx + int(r) - int(s * .22) + 2, "y": cy + int(s * .02), "w": int(s * .22), "h": int(s * .36), "r": 10, "st": col, "sw": sw}]
    if nombre == "toque":
        return [{"k": "path", "d": f"M{cx - int(s * .1)} {cy + int(r)} L{cx - int(s * .1)} {cy - int(s * .05)} Q{cx - int(s * .1)} {cy - int(s * .3)} {cx + int(s * .05)} {cy - int(s * .3)} Q{cx + int(s * .2)} {cy - int(s * .3)} {cx + int(s * .2)} {cy - int(s * .05)} L{cx + int(s * .2)} {cy + int(r)}", "fill": col, "sw": sw}]
    return [{"k": "circ", "x": cx, "y": cy, "r": int(r), "st": col, "sw": sw}]


# ================= PLANTILLAS =================

def frase(p):
    """LETTERING APPLE: una frase corta (1-3 palabras) a tamaño medio. La palabra clave lleva DEGRADADO, o un MARCADOR que brilla si `resalta`.
    params: texto, clave, resalta (bool), orbita (bool: órbita con destello), fantasma (número gigante de fondo en contorno), tema"""
    th = tema(p, "claro")
    pal = p["texto"].split()
    s = _fs(p["texto"], 1000, 110, 0.58)
    ancho = int(s * 0.58 * len(p["texto"]))
    x0 = 640 - ancho // 2
    f = [t(640, 540, 520, p["fantasma"], th["ink"], 700, "middle", -10, None, 0.0) | {"st": th["ink"], "sw": 2, "op": 0.18}] if p.get("fantasma") else []
    x = x0
    for w_ in pal:
        clave = p.get("clave") and w_.strip(".,?!").lower() == p["clave"].lower()
        if clave and p.get("resalta"):
            f.append({"k": "rect", "x": x - 16, "y": 400 - int(s * 0.80), "w": int(s * 0.5 * len(w_)) + 32, "h": int(s * 1.06), "r": int(s * 0.2), "fill": th["acc"], "op": 0.92, "glow": th["acc"]})
            f.append(t(x, 400, s, w_, NE, 700, "start", -3))
        else:
            f.append(t(x, 400, s, w_, th["ink"] if not clave else "#ffffff", 700, "start", -3, th["tg"] if clave else None))
        x += int(s * 0.58 * (len(w_) + 1)) + 6
    if p.get("orbita"):
        f += orbita(640, 380, ancho // 2 + 90, int(s * 1.0), th)
    return {"fondo": th["fondo"], "formas": f}, "las palabras entran una a una con la voz (sube 20 px y aparece, 0,3 s, power3.out); la palabra clave llega con su degradado (o el marcador se dibuja y brilla); la órbita se traza con su destello"


def titular(p):
    """Idea corta de 2 líneas, grande. params: l1, l2 (acento con degradado), tema, kicker"""
    th = tema(p, "azul")
    s1, s2 = _fs(p["l1"], 1000, 130, 0.46), _fs(p["l2"], 1000, 170, 0.56)
    f = kicker(p["kicker"], th, 140) if p.get("kicker") else []
    f += [t(L, 380, s1, p["l1"], th["ink"], 300, "start", -3), t(L, 380 + int(s2 * 1.0), s2, p["l2"], "#ffffff", 700, "start", -4, th["tg"])]
    if p.get("orbita"):
        f += orbita(L + 540, 440, 620, 190, th)
    return {"fondo": th["fondo"], "formas": f}, "cada palabra sube desde detrás de su línea, una a una con la voz (máscara, 0,6 s, power4.out); la línea de acento lleva degradado"


def keynote(p):
    """UNA cifra gigante con degradado. params: valor, etiqueta, tema (blanco por defecto: se muestra un dato)"""
    th = tema(p, "claro")
    f = ([t(L + 40, 560, 520, p["fantasma"], th["ink"], 700, "start", -10) | {"st": th["ink"], "sw": 2, "op": 0.16}] if p.get("fantasma") else [])
    f += [t(L, 450, _fs(p["valor"], 1080, 330, 0.62), p["valor"], "#ffffff", 700, "start", -8, th["tg"]), {"k": "rect", "x": L + 6, "y": 500, "w": 120, "h": 10, "fill": th["acc"], "r": 5},
         t(L + 6, 590, _fs(p["etiqueta"], 1000, 52), p["etiqueta"], th["mut"], 400, "start", -1)]
    return {"fondo": th["fondo"], "formas": f}, "movimiento lento de cola larga (0,5-0,75 s); el número cuenta hasta su valor exacto; un barrido de luz recorre la cifra y la deja iluminada, una sola vez"


cifra = keynote


def flujo(p):
    """Proceso (2-4 pasos) con íconos de línea en tarjetas de vidrio unidas por una línea. params: nodos, iconos, titulo, tema"""
    th = tema(p, "claro")
    n = p["nodos"][:4]
    k = len(n)
    ic = p.get("iconos") or ["persona", "chat", "doc", "check"][:k]
    paso = 1080 // k
    f = (kicker(p["titulo"], th, 130) if p.get("titulo") else [])
    f.append({"k": "linea", "x1": L + paso // 2, "y1": 400, "x2": L + paso * (k - 1) + paso // 2, "y2": 400, "fill": th["ink"], "sw": 3, "op": 0.4})
    for i in range(k):
        cx = L + paso * i + paso // 2
        f += [vidrio(cx - 110, 290, 220, 220, th, 28)] + icono(ic[i % len(ic)], cx, 395, 100, th["acc"] if i < k - 1 else th["ink"])
        f.append(t(cx, 570, _fs(n[i], paso - 30, 38), n[i], th["ink"], 600, "middle", -1))
    return {"fondo": th["fondo"], "formas": f}, "las tarjetas entran en orden de la voz; cada ícono se DIBUJA con trazo progresivo; la línea las une y un paquete de luz la recorre"


def comparacion(p):
    """Antes/después: mitades a sangre, la derecha con degradado azul. params: izq, der"""
    s_i = _fs(p["izq"], 500, 90)
    f = [{"k": "rect", "x": 640, "y": 0, "w": 640, "h": 720, "fill": "#2f6bea"},
         t(80, 390, s_i, p["izq"], "#7b8394", 600, "start", -2), t(720, 390, _fs(p["der"], 500, 100), p["der"], "#ffffff", 700, "start", -3),
         {"k": "linea", "x1": 70, "y1": 358, "x2": 80 + int(s_i * 0.5 * len(p["izq"])) + 20, "y2": 358, "fill": AC, "sw": 14}]
    return {"fondo": {"grad": ["#f1f3f7", "#e2e6ee"], "ang": 160}, "formas": f}, \
        "el lado izquierdo se tacha y se apaga; el derecho avanza 40 px a la izquierda y se enciende; el cambio ocurre en la palabra de la voz"


def tarjetas(p):
    """Tres pilares en tarjetas de vidrio con ícono. params: items [{icono, titulo, texto}] (3), titulo, tema"""
    th = tema(p, "azul")
    it = p["items"][:3]
    f = (kicker(p["titulo"], th, 130) if p.get("titulo") else [])
    for i, c in enumerate(it):
        x = L + i * 365
        f += [vidrio(x, 220, 340, 340, th, 24)] + icono(c.get("icono", "check"), x + 62, 290, 56, th["acc"])
        f.append(t(x + 30, 390, _fs(c["titulo"], 290, 40), c["titulo"], th["ink"], 700, "start", -1))
        for j, ln in enumerate(wrap(c.get("texto", ""), 22)[:3]):
            f.append(t(x + 30, 440 + j * 34, 26, ln, th["mut"], 400))
    return {"fondo": th["fondo"], "formas": f}, "las tarjetas entran de izquierda a derecha con la voz (sube 40 px y aparece, stagger 0,12 s); el ícono se dibuja dentro de cada una"


def panel4(p):
    """Como la cotización de Gurú/Academy: texto a la izquierda y 4 tarjetas de vidrio a la derecha. params: cabecera, kicker, icono_kicker, titulo, subtitulo, texto, tarjetas [{icono,titulo,texto}x4], tema"""
    th = tema(p, "azul")
    f = []
    if p.get("cabecera"):
        f += [t(L, 70, 22, p["cabecera"], th["ink"], 400, "start", 0, None, 0.9), regla(th, 100)]
    f.append(t(L, 350, _fs(p["titulo"], 500, 80, 0.62), p["titulo"], th["ink"], 700, "start", -3))
    if p.get("subtitulo"):
        for j, ln in enumerate(wrap(p["subtitulo"], 30)[:3]):
            f.append(t(L, 410 + j * 40, 31, ln, th["ink"], 600))
    if p.get("texto"):
        for j, ln in enumerate(wrap(p["texto"], 40)[:4]):
            f.append(t(L, 530 + j * 32, 24, ln, th["mut"], 400))
    for i, c in enumerate(p.get("tarjetas", [])[:4]):
        x, y = 650 + (i % 2) * 275, 190 + (i // 2) * 215
        f += [vidrio(x, y, 255, 195, th, 18)] + icono(c.get("icono", "check"), x + 40, y + 42, 36, th["ink"])
        f.append(t(x + 22, y + 108, _fs(c["titulo"], 215, 28), c["titulo"], th["ink"], 700))
        for j, ln in enumerate(wrap(c.get("texto", ""), 24)[:2]):
            f.append(t(x + 22, y + 140 + j * 26, 20, ln, th["mut"], 400))
    return {"fondo": th["fondo"], "formas": f}, "el titular sube con máscara; las cuatro tarjetas entran con la voz (sube 30 px, aparece, stagger 0,1 s) y cada ícono se dibuja"


def tachado(p):
    """Algo que se elimina. params: texto, tachado, tema"""
    th = tema(p, "claro")
    s = _fs(p["tachado"], 1080, 200, 0.56)
    f = [t(L, 300, _fs(p["texto"], 1080, 120, 0.46), p["texto"], th["ink"], 300, "start", -3), t(L, 300 + int(s * 1.0), s, p["tachado"], th["mut"], 700, "start", -4),
         {"k": "linea", "x1": L - 10, "y1": 300 + int(s * 0.62), "x2": L + int(s * 0.56 * len(p["tachado"])), "y2": 300 + int(s * 0.62), "fill": th["acc"] if th["oscuro"] else AC, "sw": 20}]
    return {"fondo": th["fondo"], "formas": f}, "la palabra aparece atenuada y una barra de acento la tacha de izquierda a derecha justo cuando la voz la niega (0,35 s)"


def pantalla(p):
    """Una plataforma o software, genérica (nunca captura falsa de terceros). params: titulo, lineas [≤4], tema"""
    th = tema(p, "claro")
    f = [t(L, 300, _fs(p["titulo"], 520, 96, 0.5), p["titulo"], th["ink"], 700, "start", -3),
         {"k": "rect", "x": 640, "y": 130, "w": 760, "h": 480, "r": 20, "fill": th["ink"], "op": 0.08, "st": th["ink"], "sw": 2, "sop": 0.35},
         {"k": "rect", "x": 640, "y": 130, "w": 760, "h": 64, "r": 20, "fill": th["ink"], "op": 0.12}]
    for i, l in enumerate(p.get("lineas", [])[:4]):
        f += [{"k": "rect", "x": 690, "y": 235 + i * 85, "w": 560 - i * 70, "h": 52, "r": 14, "fill": th["acc"] if i == 0 else th["ink"], "op": None if i == 0 else 0.14},
              t(716, 270 + i * 85, 26, l, "#ffffff" if i == 0 else th["ink"], 600)]
    return {"fondo": th["fondo"], "formas": f}, "la pantalla entra desde la derecha con la cámara 3D (giro suave de 8°) y cada barra se dibuja de izquierda a derecha con su palabra"


def checklist(p):
    """Beneficios o requisitos que se marcan. params: items [2-5], titulo, tema"""
    th = tema(p, "azul")
    it = p["items"][:5]
    f = kicker(p["titulo"], th, 130) if p.get("titulo") else []
    paso = min(120, (610 - 200) // len(it))
    for i, x in enumerate(it):
        y = 240 + i * paso
        f += icono("check", L + 36, y + 6, 68, th["acc"]) + [t(L + 110, y + 28, _fs(x, 900, 66), x, th["ink"], 600, "start", -2)]
        if i < len(it) - 1:
            f.append({"k": "linea", "x1": L + 110, "y1": y + paso - 30, "x2": 1000, "y2": y + paso - 30, "fill": th["ink"], "sw": 1, "op": 0.25})
    return {"fondo": th["fondo"], "formas": f}, "cada fila se marca (el círculo se dibuja y el check traza) justo cuando la voz nombra ese punto; el texto sube con máscara"


def cta(p):
    """Cierre con llamado a la acción. params: texto, sub, tema"""
    th = tema(p, "azul")
    s = _fs(p["texto"], 1080, 150, 0.5)
    f = [t(L, 360, s, p["texto"], th["ink"], 700, "start", -4)]
    if p.get("sub"):
        f.append(t(L, 450, _fs(p["sub"], 1000, 52), p["sub"], th["mut"], 400, "start", -1))
    f.append({"k": "path", "d": "M100 600 L520 600 M470 560 L520 600 L470 640", "fill": th["ink"], "sw": 14})
    return {"fondo": th["fondo"], "formas": f}, "el texto sube con máscara; la flecha se DIBUJA hacia el contacto (trazo progresivo); la marca entra al final con su sonido"


def barras(p):
    """Data story: un gráfico, una anotación. params: valores, etiquetas, titulo, nota, tema"""
    th = tema(p, "claro")
    v, e = p["valores"], p.get("etiquetas", [""] * len(p["valores"]))
    mx, k = max(v), len(v)
    ancho = min(130, 740 // k - 40)
    f = (kicker(p["titulo"], th, 130) if p.get("titulo") else [])
    for i, val in enumerate(v):
        h = int(360 * val / mx)
        x = L + 60 + i * (ancho + 44)
        f += [{"k": "rect", "x": x, "y": 600 - h, "w": ancho, "h": h, "r": 8, "fill": th["acc"] if i == k - 1 else th["ink"], "op": None if i == k - 1 else 0.16},
              t(x, 600 - h - 20, 40, str(val), th["ink"], 700, "start", -1), t(x, 650, 28, e[i], th["mut"], 500)]
    f.append({"k": "linea", "x1": L, "y1": 600, "x2": 1180, "y2": 600, "fill": th["ink"], "sw": 2, "op": 0.5})
    if p.get("nota"):
        x_ult = L + 60 + (k - 1) * (ancho + 44)
        f += [t(x_ult + ancho + 50, 250, _fs(p["nota"], 330, 46), p["nota"], th["ink"], 700, "start", -2), {"k": "linea", "x1": x_ult + ancho + 40, "y1": 270, "x2": x_ult + ancho + 8, "y2": 600 - int(360 * v[-1] / mx) + 20, "fill": th["acc"], "sw": 3}]
    return {"fondo": th["fondo"], "formas": f}, "las barras crecen desde la línea base (20 cuadros, ease-out) una a una; la cifra cuenta hasta su valor exacto; la anotación aparece al final; un solo gráfico por pantalla"


def linea(p):
    """Una sola línea que recorre 3-4 ideas. params: puntos, titulo, tema"""
    th = tema(p, "claro")
    n = p["puntos"][:4]
    xs, ys = [150, 520, 860, 1150][: len(n)], [470, 470, 470, 330][: len(n)]
    f = kicker(p["titulo"], th, 130) if p.get("titulo") else []
    f.append({"k": "path", "d": "M150 470 C 300 200, 430 200, 520 470 S 760 700, 860 470 S 1060 190, 1150 330", "fill": th["ink"], "sw": 14})
    for i, (x, y) in enumerate(zip(xs, ys)):
        lx, ly, la = [(x, y + 80, "middle"), (x + 40, y - 70, "start"), (x + 40, y + 80, "start"), (x - 34, y - 40, "end")][i]
        f += [{"k": "circ", "x": x, "y": y, "r": 22, "fill": th["acc"]}, t(lx, ly, _fs(n[i], 260, 44), n[i], th["ink"], 700, la, -1)]
    return {"fondo": th["fondo"], "formas": f}, "UNA línea continua de grosor constante se dibuja a ~800 px/s y la cámara la sigue; en el tiempo fuerte se rellena de color una vez; sin fundidos ni texto letra por letra"


def _cubo(cx, cy, a, h, ton):
    sup, izq, der = ton
    return [{"k": "poly", "pts": f"{cx},{cy} {cx + a},{cy + a // 2} {cx},{cy + a} {cx - a},{cy + a // 2}", "fill": sup},
            {"k": "poly", "pts": f"{cx - a},{cy + a // 2} {cx},{cy + a} {cx},{cy + a + h} {cx - a},{cy + a // 2 + h}", "fill": izq},
            {"k": "poly", "pts": f"{cx + a},{cy + a // 2} {cx},{cy + a} {cx},{cy + a + h} {cx + a},{cy + a // 2 + h}", "fill": der}]


def isometrico(p):
    """Mini-mundo isométrico con etiquetas con línea guía. params: items [2-3], titulo, tema"""
    th = tema(p, "claro")
    it = p["items"][:3]
    f = kicker(p["titulo"], th, 130) if p.get("titulo") else []
    f += _cubo(840, 250, 440, 20, ("#e6e9f0", "#cfd4de", "#b4bbca") if not th["oscuro"] else ("#3a4256", "#2b3142", "#1f2432"))
    pos = [(700, 330, 110, 80), (890, 290, 110, 190), (1030, 400, 80, 60)]
    for k_, (x, y, a, h) in enumerate(pos[: len(it)]):
        f += _cubo(x, y, a, h, ("#9bbcff", AZ, "#2557c9") if k_ != 1 else ("#cf9bff", AC, "#560080"))
    for (x, y, a, h), (lx, ly), s_ in zip(pos, [(L, 330), (L, 470), (L, 610)], it):
        f += [{"k": "linea", "x1": x - a // 2, "y1": y + a // 2, "x2": lx + 330, "y2": ly - 12, "fill": th["ink"], "sw": 2, "op": 0.4}, t(lx, ly, _fs(s_, 320, 50), s_, th["ink"], 700, "start", -1)]
    return {"fondo": th["fondo"], "formas": f}, "los bloques caen 40 px con un pequeño rebote en cascada (3 cuadros); la cámara se desliza sin rotar (ortográfica); el objeto se abre para mostrar su interior en vez de cortar de escena"


def notificacion(p):
    """Notificación / aviso con PILA de capas translúcidas detrás (ref. «Elevare Consulting»). params: titulo (quién), texto, hora, icono, tema"""
    th = tema(p, "solucion")
    x, y, w, h = 170, 250, 940, 200
    acc = th["acc"] if th["oscuro"] else AZ
    f = [{"k": "rect", "x": x + 120, "y": y + 110, "w": w - 240, "h": 170, "r": 28, "fill": "#ffffff", "op": 0.35},
         {"k": "rect", "x": x + 60, "y": y + 66, "w": w - 120, "h": 170, "r": 28, "fill": "#ffffff", "op": 0.55},
         {"k": "rect", "x": x, "y": y, "w": w, "h": h, "r": 28, "fill": "#f6f8fc", "glow": acc, "brillo": True},
         {"k": "rect", "x": x + 44, "y": y + 40, "w": 120, "h": 120, "r": 30, "fill": acc}] + icono(p.get("icono", "chat"), x + 104, y + 100, 64, "#ffffff")
    f += [t(x + 200, y + 78, 42, p["titulo"], NE, 700, "start", -1), t(x + w - 44, y + 74, 26, p.get("hora", "ahora"), "#8a93a6", 400, "end")]
    for j, ln in enumerate(wrap(p["texto"], 46)[:2]):
        f.append(t(x + 200, y + 126 + j * 40, 31, ln, NE, 500, "start", -0.5))
    return {"fondo": th["fondo"], "formas": f}, "la tarjeta cae desde arriba con un rebote suave; las capas de atrás se abren en cascada (stagger 0,08 s); el texto se escribe con la voz; un barrido de luz cruza el borde"


def curva(p):
    """Gráfica de ÁREA con degradado, puntos con halo y etiqueta de valor flotante (ref. «GatesFX»). params: valores (5-8), titulo, etiqueta (burbuja final), marca (burbuja intermedia), tema"""
    th = tema(p, "claro")
    v = p["valores"]
    mn, mx = min(v), max(v)
    n = len(v)
    xs = [int(110 + i * (1060 / (n - 1))) for i in range(n)]
    ys = [int(640 - 300 * (val - mn) / max(mx - mn, 1)) for val in v]
    d = "M" + " L".join(f"{x} {y}" for x, y in zip(xs, ys))
    f = [t(L, 190, _fs(p["titulo"], 900, 96, 0.5), p["titulo"], th["ink"], 600, "start", -3)] if p.get("titulo") else []
    f += [{"k": "path", "d": d + f" L{xs[-1]} 660 L{xs[0]} 660 Z", "fill": th["acc"], "sw": 0, "relgrad": th["acc"]},
          {"k": "path", "d": d, "fill": th["acc"], "sw": 12}]
    for x in xs[1:-1]:
        f.append({"k": "linea", "x1": x, "y1": ys[xs.index(x)], "x2": x, "y2": 660, "fill": th["acc"], "sw": 2, "op": 0.3})
    ult = n - 1
    f += [{"k": "circ", "x": xs[ult], "y": ys[ult], "r": 22, "fill": "#ffffff", "st": th["acc"], "sw": 10, "glow": th["acc"]}]
    if p.get("etiqueta"):
        f += [{"k": "rect", "x": xs[ult] - 230, "y": ys[ult] - 92, "w": 210, "h": 62, "r": 12, "fill": th["acc"], "glow": th["acc"], "brillo": True}, t(xs[ult] - 125, ys[ult] - 50, 32, p["etiqueta"], "#ffffff", 700, "middle", -1)]
    if p.get("marca") and n > 3:
        k = n - 3
        f += [{"k": "circ", "x": xs[k], "y": ys[k], "r": 18, "fill": "#ffffff", "st": th["acc"], "sw": 8}, {"k": "rect", "x": xs[k] - 55, "y": ys[k] + 30, "w": 110, "h": 40, "r": 10, "fill": th["acc"], "op": 0.9}, t(xs[k], ys[k] + 58, 22, p["marca"], "#ffffff", 700, "middle")]
    return {"fondo": th["fondo"], "formas": f}, "el área se revela de izquierda a derecha siguiendo la línea (trazo progresivo, 1,2 s); cada punto hace pop con su halo y la burbuja de valor sube y rebota; la cifra cuenta hasta su valor"


def orbitas(p):
    """Anillos finos concéntricos con íconos en discos que giran lento alrededor del texto (ref. «Olist»). params: lineas [2 textos], iconos [3-4], tema"""
    th = tema(p, "solucion")
    f = [{"k": "circ", "x": 640, "y": 360, "r": r_, "st": "#ffffff", "sw": 2, "sop": 0.7} for r_ in (210, 340, 480)]
    ic = (p.get("iconos") or ["persona", "chat", "doc", "globo"])[:4]
    for i, (ang, r_) in enumerate(zip((-130, -20, 70, 160), (340, 480, 340, 480))):
        cx, cy = int(640 + r_ * math.cos(math.radians(ang))), int(360 + r_ * 0.78 * math.sin(math.radians(ang)))
        cl = "#0a1b55" if i % 2 == 0 else "#ffffff"
        f += [{"k": "circ", "x": cx, "y": cy, "r": 50, "fill": cl, "glow": "#ffffff" if cl == "#ffffff" else None}] + icono(ic[i % len(ic)], cx, cy, 44, "#ffffff" if cl == "#0a1b55" else "#0a1b55")
    for j, ln in enumerate(p["lineas"][:2]):
        f.append(t(640, 340 + j * 92, _fs(ln, 520, 84), ln, "#ffffff", 700 if j else 300, "middle", -3))
    return {"fondo": th["fondo"], "formas": [d for d in f if not (d.get("k") == "circ" and d.get("glow") is None and False)]}, \
        "los anillos se dibujan desde el centro (trazo progresivo); los discos orbitan lento a distintas velocidades con un leve brillo; el texto sube con máscara"


def chips(p):
    """Anillos suaves concéntricos con «chips» flotantes (ícono + texto) alrededor de un título (ref. «Projetura»). params: centro (2 líneas), items [{icono, texto}] (3-5), tema"""
    th = tema(p, "claro")
    f = [{"k": "circ", "x": 640, "y": 380, "r": r_, "fill": th["ink"], "op": 0.035} for r_ in (330, 250, 170)]
    pos = [(700, 90), (70, 190), (790, 270), (110, 500), (770, 520)]
    for (x, y), c in zip(pos, p["items"][:5]):
        f += [{"k": "rect", "x": x, "y": y, "w": 330, "h": 92, "r": 20, "fill": "#ffffff", "glow": th["acc"], "brillo": True}, {"k": "rect", "x": x + 16, "y": y + 16, "w": 60, "h": 60, "r": 14, "fill": th["acc"], "op": 0.18, "st": th["acc"], "sw": 2}]
        f += icono(c.get("icono", "check"), x + 46, y + 46, 30, th["ink"])
        for j, ln in enumerate(wrap(c["texto"], 18)[:2]):
            f.append(t(x + 92, y + 40 + j * 30, 25, ln, th["ink"], 700, "start", -0.5))
    for j, ln in enumerate(p["centro"][:2]):
        f.append(t(640, 395 + j * 66, _fs(ln, 600, 64), ln, th["ink"], 700 if j else 600, "middle", -2))
    return {"fondo": th["fondo"], "formas": f}, "los anillos se expanden desde el centro como una onda; los chips entran flotando uno a uno con la voz (sube 30 px, aparece) y luego se mecen sutil; el título sube con máscara"


def ruta(p):
    """Contenedor con borde de degradado que BRILLA y filas «etiqueta → resultado» en rectángulos de esquinas suaves (ref. «casa inteligente»). params: l1, l2 (degradado), filas [{etiqueta, texto}] (3), tema"""
    th = tema(p, "claro")
    f = [t(640, 150, _fs(p["l1"], 900, 86, 0.46), p["l1"], th["ink"], 300, "middle", -3), t(640, 150 + 84, _fs(p["l2"], 900, 96, 0.54), p["l2"], "#ffffff", 700, "middle", -3, ["#2563eb", "#1fb5a8"])]
    f.append({"k": "rect", "x": 150, "y": 290, "w": 980, "h": 400, "r": 90, "fill": "#1fb5a8", "op": 0.10, "stgrad": [AZ, "#1fb5a8"], "sw": 4, "glow": "#1fb5a8"})
    for i, r_ in enumerate(p["filas"][:3]):
        y = 330 + i * 110
        f += [{"k": "rect", "x": 200, "y": y, "w": 880, "h": 90, "r": 16, "fill": "#ffffff", "glow": th["acc"], "brillo": True},
              t(260, y + 58, 34, r_["etiqueta"], th["ink"], 700, "start", -1), t(260 + int(len(r_["etiqueta"]) * 19) + 56, y + 58, 34, "→  " + r_["texto"], th["ink"], 400, "start", -1)]
    return {"fondo": th["fondo"], "formas": f}, "las filas entran en cascada (sube 24 px y aparece, 0,45 s); la flecha de cada fila se dibuja; el borde de degradado recorre el contenedor como una luz y lo deja brillando"


def pregunta(p):
    """Pregunta cinética con tamaños mezclados, insignia circular, interruptor SÍ/NO y flechas que se dibujan (ref. «Protexiones»). params: l1, clave, l3, opciones [SÍ, NO], elegida (0|1), respuesta, tema"""
    th = tema(p, "claro")
    ac = th["acc"]
    op = p.get("opciones", ["SÍ", "NO"])
    f = [t(190, 168, 40, p["l1"], th["ink"], 700, "start", -1), t(186, 335, _fs(p["clave"], 700, 175, 0.62), p["clave"], ac, 700, "start", -7),
         {"k": "circ", "x": 214, "y": 398, "r": 30, "fill": th["ink"]}, t(214, 410, 30, "de", "#ffffff", 700, "middle"),
         t(266, 480, _fs(p["l3"], 700, 175, 0.62), p["l3"], ac, 700, "start", -7),
         {"k": "rect", "x": 190, "y": 520, "w": 470, "h": 120, "r": 22, "fill": th["ink"], "op": 0.07},
         t(330, 598, 60, op[0], th["ink"], 700, "middle", -2), {"k": "circ", "x": 560, "y": 580, "r": 60, "st": ac, "sw": 6, "glow": ac}, t(560, 598, 60, op[1], th["ink"], 700, "middle", -2),
         {"k": "path", "d": "M-10 700 Q60 700 60 620 L60 400 Q60 345 120 335 L165 330 M138 304 L166 330 L138 356", "fill": th["ink"], "sw": 7},
         {"k": "path", "d": "M620 580 L1010 580 Q1110 580 1110 480", "fill": ac, "sw": 6},
         {"k": "path", "d": "M330 650 L330 672 M312 656 L330 674 L348 656", "fill": ac, "sw": 5}]
    if p.get("respuesta"):
        f.append(t(190, 706, 38, p["respuesta"], th["ink"], 500, "start", -1))
    return {"fondo": th["fondo"], "formas": f}, "la pregunta entra palabra por palabra con tamaños distintos; el interruptor se enciende y el círculo salta al elegido; las flechas se DIBUJAN por la pantalla hacia la respuesta"


def tarjeta_plano(p):
    """Tarjeta de color con el PLANO que rompe el borde y texto que queda detrás (ref. «pneumonia», «día mundial da saúde»). params: l1, l2, texto, cta, tema"""
    th = tema(p, "solucion")
    f = [{"k": "rect", "x": 90, "y": 150, "w": 1100, "h": 420, "r": 48, "fill": "#ffffff", "op": 0.12, "st": "#ffffff", "sw": 1, "sop": 0.3, "glow": th["acc"], "brillo": True},
         t(150, 330, _fs(p["l1"], 560, 130, 0.5), p["l1"], th["ink"], 300, "start", -4), t(150, 330 + 120, _fs(p["l2"], 560, 140, 0.56), p["l2"], "#ffffff", 700, "start", -5, th["tg"])]
    for j, ln in enumerate(wrap(p.get("texto", ""), 34)[:2]):
        f.append(t(150, 520 + j * 36, 27, ln, th["mut"], 400))
    f += [{"k": "rect", "x": 640, "y": 70, "w": 480, "h": 600, "r": 36, "fill": "#0a1b55", "glow": "#ffffff", "brillo": True}, t(880, 380, 34, "tu plano aquí", "#ffffff", 400, "middle", 0, None, 0.8)]
    if p.get("cta"):
        f += [{"k": "rect", "x": 150, "y": 625, "w": 62, "h": 62, "r": 16, "st": th["ink"], "sw": 2, "sop": 0.6}, {"k": "path", "d": "M166 650 L196 680 M198 654 L198 680 L172 680", "fill": th["ink"], "sw": 4},
              {"k": "rect", "x": 230, "y": 625, "w": 340, "h": 62, "r": 18, "fill": "#0a1b55"}, t(400, 665, 26, p["cta"], "#ffffff", 600, "middle")]
    return {"fondo": th["fondo"], "formas": f}, "la tarjeta se abre con la voz; el plano entra y rompe el borde superior e inferior (parallax: se mueve más que la tarjeta); el título queda detrás del plano y se revela al pasar; el CTA aparece al final"


PLANTILLAS = {"frase": frase, "titular": titular, "cifra": cifra, "keynote": keynote, "flujo": flujo, "comparacion": comparacion, "tarjetas": tarjetas, "panel4": panel4,
              "tachado": tachado, "pantalla": pantalla, "checklist": checklist, "cta": cta, "barras": barras, "linea": linea, "isometrico": isometrico, "notificacion": notificacion, "curva": curva, "orbitas": orbitas, "chips": chips, "ruta": ruta, "pregunta": pregunta, "tarjeta_plano": tarjeta_plano}


FONDO_VIVO = " · FONDO VIVO (nunca estático): la aurora de color respira y deriva lento (ciclo de 8-12 s), el grano parpadea sutil y la rejilla/puntos se mueven en parallax"


def boceto(nombre, params):
    """(spec para boceto_svg, indicación de movimiento por defecto). Regla de Cris (28-oct): jamás un fondo estático, siempre algún movimiento, así sea sutil."""
    spec, mov = PLANTILLAS[nombre](params)
    if params.get("paso"):      # "2/4"
        a, b = params["paso"].split("/")
        spec["formas"] = spec["formas"] + puntos_paso(int(a) - 1, int(b), tema(params, "claro"))
    return spec, mov + FONDO_VIVO


import plantillas_ref  # noqa: E402  registra las plantillas por referencia (cada referencia de Cris = una plantilla; nunca se reemplazan)
