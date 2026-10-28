"""SISTEMA DE DISEÑO DE MOTION (28-oct-2026): el vocabulario con el que COMPONGO escenas nuevas, sin depender de plantillas.

Corrección de Cris: las referencias eran referencias de ESTILO, no plantillas para copiar; Claude debe poder CREAR por su cuenta, para cada frase, escenas nuevas
basadas en esos estilos. Por eso aquí no hay «escenas» sino ELEMENTOS (el vocabulario que sale de las referencias) y un compositor libre:

    escena({"tema": "solucion", "fondo": {"luz": "abajo"},
            "elementos": [ {"e": "titulo", "x": 100, "y": 300, "lineas": [["Un ingeniero real", 300], ["responde en minutos", 700, "grad"]]},
                           {"e": "vidrio", "x": 700, "y": 200, "w": 400, "h": 300}, {"e": "chip", ...}, ... ]})   ->  (spec para boceto_svg, movimiento)

Las plantillas de plantillas.py / plantillas_ref.py son solo EJEMPLOS de composición (few-shot), no el límite: lo normal es componer una escena a la medida de la frase,
mezclando elementos de varias referencias. Principios de composición: CLAUDE.md, «Sistema de diseño de motion».

Elementos (cada uno es un dict con "e": nombre): texto, titulo, marcador, vidrio, chip, boton, burbuja, punto, anillos, orbita, destello, cursor, curva, barras,
icono, linea, flecha, fantasma, plano, progreso, notificacion, tarjeta_stat."""
import math

from plantillas import AZ, NE, AC, GR, TEMAS, ALIAS, t, _fs, wrap, icono, orbita, puntos_paso

LUCES = {   # posición de la aurora: de dónde sube la luz (el movimiento la hace respirar y derivar)
    "abajo": [(260, 790, 660), (1120, 40, 520)], "abajo-der": [(1040, 790, 660), (160, 20, 480)], "arriba-der": [(1120, 0, 640), (200, 760, 460)],
    "arriba": [(640, -40, 700), (1180, 740, 420)], "centro": [(640, 360, 720), (1200, 760, 380)], "izquierda": [(0, 380, 640), (1180, 60, 440)],
}


def th_de(nombre):
    return TEMAS[ALIAS.get(nombre, nombre)]


def fondo(tema="solucion", luz="abajo", grano=True, textura="sutil", brillo=1.0):
    """fondo con degradado, aurora que sube desde donde se diga, grano fino y textura casi imperceptible (puntos|rejilla|None)"""
    th = th_de(tema)
    base = dict(th["fondo"]) if isinstance(th["fondo"], dict) else {"grad": [th["fondo"], th["fondo"]]}
    c1 = (base.get("luces") or [[0, 0, 0, th["acc"], 0.3]])[0][3]
    c2 = (base.get("luces") or [[0, 0, 0, th["acc"], 0.3], [0, 0, 0, th["acc"], 0.2]])[-1][3]
    pos = LUCES.get(luz, LUCES["abajo"])
    base["luces"] = [[pos[0][0], pos[0][1], pos[0][2], c1, round(0.38 * brillo, 2)], [pos[1][0], pos[1][1], pos[1][2], c2, round(0.22 * brillo, 2)]]
    base["grano"] = 0.14 if grano else 0
    base.pop("tex", None)
    if textura:
        base["tex"] = "rejilla" if textura == "rejilla" else "puntos"
    return base


def _c(th, tono):
    return {"ink": th["ink"], "mut": th["mut"], "acc": th["acc"], "blanco": "#ffffff", "oscuro": "#0a1b55", "navy": "#0a1b55"}.get(tono, tono)


# ---------------- elementos ----------------
def e_texto(d, th):
    f = t(d["x"], d["y"], d.get("s", 56), d["t"], _c(th, d.get("tono", "ink")), d.get("w", 700), d.get("a", "start"), d.get("ls", -2), th["tg"] if d.get("grad") else None, d.get("op"))
    if d.get("gv"):
        f["gv"] = True
    return [f]


def e_titulo(d, th):
    """lineas = [[texto, peso, 'grad'?], ...] apiladas, mezclando light/bold como Apple; s = tamaño base; ancho = ancho máximo"""
    out, y = [], d["y"]
    s0 = d.get("s", 96)
    for ln in d["lineas"]:
        txt, peso = ln[0], ln[1]
        s = min(s0, int(d.get("ancho", 1000) / (0.5 * max(len(txt), 1)))) if peso < 500 else min(s0, int(d.get("ancho", 1000) / (0.56 * max(len(txt), 1))))
        out.append(t(d["x"], y, s, txt, _c(th, d.get("tono", "ink")), peso, d.get("a", "start"), -3 if peso < 500 else -4, th["tg"] if len(ln) > 2 and ln[2] == "grad" else None))
        y += int(s * d.get("interlinea", 1.0))
    return out


def e_marcador(d, th):
    """píldora de color que se dibuja detrás de una frase clave y brilla (ref. «50% less time»); texto opcional"""
    f = [{"k": "rect", "x": d["x"], "y": d["y"], "w": d["w"], "h": d["h"], "r": min(d.get("r", 12), 12), "fill": d.get("fill", th["acc"]), "op": 0.92, "glow": d.get("fill", th["acc"])}]
    if d.get("t"):
        f.append(t(d["x"] + d["w"] / 2, d["y"] + d["h"] * 0.72, int(d["h"] * 0.68), d["t"], d.get("tono_t", "#0a1b55"), 700, "middle", -2))
    return f


def e_vidrio(d, th):
    """contenedor de vidrio que BRILLA: relleno translúcido, borde con luz y halo de acento"""
    ac = d.get("glow", th["acc"])
    return [{"k": "rect", "x": d["x"], "y": d["y"], "w": d["w"], "h": d["h"], "r": d.get("r", 24), "fill": th["ink"], "op": d.get("op", 0.10 if th["oscuro"] else 0.05), "st": th["ink"], "sw": 1, "sop": 0.18, "glow": ac, "brillo": True}]


def e_blanca(d, th):
    """tarjeta blanca sólida con halo (para escenas claras o UI flotante)"""
    return [{"k": "rect", "x": d["x"], "y": d["y"], "w": d["w"], "h": d["h"], "r": d.get("r", 20), "fill": "#ffffff", "glow": d.get("glow", th["acc"]), "brillo": True}]


def e_chip(d, th):
    """chip flotante: ícono en cuadro tintado + 1-2 líneas de texto (ref. «Projetura»)"""
    x, y, w, h = d["x"], d["y"], d.get("w", 320), d.get("h", 90)
    f = e_blanca({"x": x, "y": y, "w": w, "h": h, "r": 20}, th)
    f += [{"k": "rect", "x": x + 16, "y": y + (h - 58) / 2, "w": 58, "h": 58, "r": 14, "fill": th["acc"], "op": 0.18, "st": th["acc"], "sw": 2}] + icono(d.get("icono", "check"), x + 45, y + h / 2, 30, NE)
    for j, ln in enumerate(wrap(d["t"], d.get("n", 18))[:2]):
        f.append(t(x + 90, y + h / 2 + (-4 if len(wrap(d["t"], d.get("n", 18))) > 1 else 9) + j * 28, 24, ln, NE, 700, "start", -0.5))
    return f


def e_boton(d, th):
    """botón o etiqueta RECTANGULAR de esquinas suaves (la píldora está PROHIBIDA): estilo contorno | blanca | oscura | acento"""
    s_ = d.get("s", 44)
    w = int(len(d["t"]) * s_ * 0.56) + 56
    h = int(s_ * 1.5)
    est, x, y = d.get("estilo", "blanca"), d["x"], d["y"]
    if d.get("centrada"):
        x -= w // 2
    base = {"k": "rect", "x": x, "y": y - int(s_ * 1.0), "w": w, "h": h, "r": 14}
    if est == "contorno":
        c0 = "#ffffff" if th["oscuro"] else th["ink"]
        return [dict(base, st=c0, sw=2, sop=0.8), t(x + w / 2, y, s_, d["t"], c0, 700, "middle", -2)]
    if est == "blanca":
        return [dict(base, fill="#ffffff", glow="#ffffff"), t(x + w / 2, y, s_, d["t"], "#0a1b55", 700, "middle", -2)]
    if est == "acento":
        return [dict(base, fill=th["acc"], glow=th["acc"]), t(x + w / 2, y, s_, d["t"], "#0a1b55", 700, "middle", -2)]
    return [dict(base, fill="#0a1b55"), t(x + w / 2, y, s_, d["t"], "#ffffff", 700, "middle", -2)]


def e_burbuja(d, th):
    """burbuja de valor/notificación flotante con halo (ref. «+$2.300», «65 · 14 · 53»)"""
    w = max(90, int(len(d["t"]) * 17) + 44)
    return [{"k": "rect", "x": d["x"], "y": d["y"], "w": w, "h": 48, "r": 10, "fill": d.get("fill", th["acc"]), "glow": d.get("fill", th["acc"]), "brillo": True}, t(d["x"] + w / 2, d["y"] + 33, 26, d["t"], d.get("tono_t", "#0a1b55"), 700, "middle")]


def e_punto(d, th):
    """punto con halo (paletas Jade/Arctic, marcadores de gráfica)"""
    col = d.get("fill", th["acc"])
    return [{"k": "circ", "x": d["x"], "y": d["y"], "r": d.get("r", 20) * 1.6, "fill": col, "op": 0.2}, {"k": "circ", "x": d["x"], "y": d["y"], "r": d.get("r", 20), "fill": col, "glow": col if d.get("glow") else None}]


def e_anillos(d, th):
    """anillos concéntricos: fino (línea) o suave (relleno casi invisible)"""
    if d.get("estilo", "fino") == "suave":
        return [{"k": "circ", "x": d["x"], "y": d["y"], "r": r, "fill": th["ink"], "op": 0.035} for r in d["radios"]]
    return [{"k": "circ", "x": d["x"], "y": d["y"], "r": r, "st": th["ink"], "sw": 2, "sop": 0.6} for r in d["radios"]]


def e_orbita(d, th):
    return orbita(d["x"], d["y"], d["rx"], d["ry"], th, d.get("rot", -8))


def e_destello(d, th):
    return [{"k": "estrella", "x": d["x"], "y": d["y"], "s": d.get("s", 34), "fill": d.get("fill", th["ink"])}]


def e_cursor(d, th):
    x, y = d["x"], d["y"]
    f = [{"k": "poly", "pts": f"{x},{y} {x + 4},{y + 38} {x + 16},{y + 26} {x + 34},{y + 28}", "fill": d.get("fill", th["acc"])}]
    if d.get("nombre"):
        f += [{"k": "rect", "x": x + 20, "y": y + 44, "w": len(d["nombre"]) * 14 + 40, "h": 38, "r": 8, "fill": th["ink"] if not th["oscuro"] else "#0a1b55"}, t(x + 20 + (len(d["nombre"]) * 14 + 40) / 2, y + 71, 20, d["nombre"], "#ffffff", 500, "middle")]
    return f


def e_curva(d, th):
    """curva suave por puntos [(x,y),...] con área degradada y marcador final con halo; también acepta d['d'] (path)"""
    col = d.get("fill", th["acc"])
    pts = d.get("puntos")
    if pts:
        path = f"M{pts[0][0]} {pts[0][1]}"
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            mx = (x0 + x1) / 2
            path += f" C{mx} {y0} {mx} {y1} {x1} {y1}"
    else:
        path = d["d"]
    f = []
    if d.get("area", True) and pts:
        f.append({"k": "path", "d": path + f" L{pts[-1][0]} {d.get('base', 660)} L{pts[0][0]} {d.get('base', 660)} Z", "fill": col, "sw": 0, "relgrad": col})
    if d.get("neon"):
        f.append({"k": "path", "d": path, "fill": col, "sw": d.get("sw", 10) * 3, "op": 0.22})
    f.append({"k": "path", "d": path, "fill": col, "sw": d.get("sw", 10)})
    if d.get("final") and pts:
        f += e_punto({"x": pts[-1][0], "y": pts[-1][1], "r": 18, "fill": "#ffffff", "glow": True}, th)
        f.append({"k": "circ", "x": pts[-1][0], "y": pts[-1][1], "r": 18, "st": col, "sw": 8})
    return f


def e_barras(d, th):
    """barras con degradado: valores, resalta = índice de la barra de acento"""
    vs, ancho, alto, x0, base = d["valores"], d.get("ancho", 50), d.get("alto", 300), d["x"], d["y"]
    mx = max(vs)
    f = []
    for i, v in enumerate(vs):
        h = int(alto * v / mx)
        x = x0 + i * (ancho + d.get("sep", 26))
        if i == d.get("resalta", -1):
            f.append({"k": "rect", "x": x, "y": base - h, "w": ancho, "h": h, "r": 10, "fill": th["acc"]})
        elif d.get("degradado"):
            f.append({"k": "rect", "x": x, "y": base - h, "w": ancho, "h": h, "r": 10, "fillgrad": [AC, "#ffffff"], "fgv": True})
        else:
            f.append({"k": "rect", "x": x, "y": base - h, "w": ancho, "h": h, "r": 10, "fill": th["ink"], "op": 0.1})
    return f


def e_icono(d, th):
    return icono(d["nombre"], d["x"], d["y"], d.get("s", 60), _c(th, d.get("tono", "acc")))


def e_linea(d, th):
    return [{"k": "linea", "x1": d["x1"], "y1": d["y1"], "x2": d["x2"], "y2": d["y2"], "fill": _c(th, d.get("tono", "ink")), "sw": d.get("sw", 2), "op": d.get("op", 0.4)}]


def e_flecha(d, th):
    """flecha con esquina redondeada que se dibuja por la pantalla (ref. «Protexiones»): puntos [(x,y),...]"""
    pts = d["puntos"]
    path = f"M{pts[0][0]} {pts[0][1]}"
    for i in range(1, len(pts) - 1):
        (xa, ya), (xb, yb), (xc, yc) = pts[i - 1], pts[i], pts[i + 1]
        r = d.get("r", 50)
        k1 = (math.copysign(min(r, abs(xb - xa) or r, abs(yb - ya) or r), xb - xa) if xb != xa else 0, math.copysign(min(r, abs(yb - ya) or r), yb - ya) if yb != ya else 0)
        path += f" L{xb - (k1[0] if xb != xa else 0)} {yb - (k1[1] if yb != ya else 0)} Q{xb} {yb} {xb + (math.copysign(r, xc - xb) if xc != xb else 0)} {yb + (math.copysign(r, yc - yb) if yc != yb else 0)}"
    xe, ye = pts[-1]
    path += f" L{xe} {ye}"
    xp, yp = pts[-2]
    ang = math.atan2(ye - yp, xe - xp)
    for da in (0.5, -0.5):
        path += f" M{xe} {ye} L{xe - 30 * math.cos(ang + da):.1f} {ye - 30 * math.sin(ang + da):.1f}"
    return [{"k": "path", "d": path, "fill": _c(th, d.get("tono", "ink")), "sw": d.get("sw", 7)}]


def e_fantasma(d, th):
    """número o palabra GIGANTE en contorno, detrás del texto (ref. «50%»)"""
    return [t(d["x"], d["y"], d.get("s", 480), d["t"], th["ink"], 700, d.get("a", "start"), -10) | {"st": th["ink"], "sw": 2, "op": d.get("op", 0.17)}]


def e_plano(d, th):
    """marco del plano/objeto del video; puede romper el borde de un vidrio (se sale del contenedor): nunca se dibuja contenido ajeno"""
    return [{"k": "rect", "x": d["x"], "y": d["y"], "w": d["w"], "h": d["h"], "r": d.get("r", 30), "fill": "#0a1b55", "glow": "#ffffff", "brillo": True}, t(d["x"] + d["w"] / 2, d["y"] + d["h"] / 2, 22, d.get("t", "tu plano aquí"), "#ffffff", 400, "middle")]


def e_progreso(d, th):
    return puntos_paso(d["i"], d["n"], th)


def e_notificacion(d, th):
    """aviso con pila de capas translúcidas (ref. «Elevare»)"""
    x, y, w, h = d["x"], d["y"], d.get("w", 900), d.get("h", 190)
    f = [{"k": "rect", "x": x + 120, "y": y + 100, "w": w - 240, "h": 160, "r": 30, "fill": "#ffffff", "op": 0.35}, {"k": "rect", "x": x + 60, "y": y + 60, "w": w - 120, "h": 160, "r": 30, "fill": "#ffffff", "op": 0.55}]
    f += e_blanca({"x": x, "y": y, "w": w, "h": h, "r": 28}, th)
    f += [{"k": "rect", "x": x + 40, "y": y + 36, "w": 118, "h": 118, "r": 30, "fill": th["acc"]}] + icono(d.get("icono", "chat"), x + 99, y + 95, 62, "#ffffff")
    f += [t(x + 190, y + 74, 40, d["titulo"], NE, 700, "start", -1), t(x + w - 40, y + 70, 24, d.get("hora", "ahora"), "#8a93a6", 400, "end")]
    for j, ln in enumerate(wrap(d["t"], d.get("n", 44))[:2]):
        f.append(t(x + 190, y + 122 + j * 38, 30, ln, NE, 500, "start", -0.5))
    return f


def e_tarjeta_stat(d, th):
    """tarjeta con cifra grande, subtítulo y filas de resumen (ref. dashboard)"""
    x, y, w, h = d["x"], d["y"], d.get("w", 330), d.get("h", 300)
    f = e_blanca({"x": x, "y": y, "w": w, "h": h, "r": 18}, th) + [t(x + 28, y + 62, 40, str(d["valor"]), NE, 700, "start", -1), t(x + 28, y + 92, 18, d.get("sub", ""), "#6b7385", 400)]
    for j, (lab, val) in enumerate(d.get("filas", [])[:2]):
        f += [{"k": "circ", "x": x + 52, "y": y + 160 + j * 62, "r": 22, "fill": th["acc"] if j == 0 else AC, "op": 0.25}, t(x + 92, y + 155 + j * 62, 17, lab, "#6b7385", 400), t(x + 92, y + 182 + j * 62, 24, val, NE, 700, "start", -0.5)]
    return f


ELEMENTOS = {"texto": e_texto, "titulo": e_titulo, "marcador": e_marcador, "vidrio": e_vidrio, "blanca": e_blanca, "chip": e_chip, "boton": e_boton, "burbuja": e_burbuja,
             "punto": e_punto, "anillos": e_anillos, "orbita": e_orbita, "destello": e_destello, "cursor": e_cursor, "curva": e_curva, "barras": e_barras, "icono": e_icono,
             "linea": e_linea, "flecha": e_flecha, "fantasma": e_fantasma, "plano": e_plano, "progreso": e_progreso, "notificacion": e_notificacion, "tarjeta_stat": e_tarjeta_stat}

# ---------------- elementos ABSTRACTOS (para convertir ideas en animación abstracta) ----------------
def _azar(sem):
    """generador determinista (la misma semilla da siempre el mismo desorden)"""
    est = [sem * 9301 + 49297]

    def r():
        est[0] = (est[0] * 9301 + 49297) % 233280
        return est[0] / 233280
    return r


def e_particulas(d, th):
    """puntos dispersos (caos) o alineados en cuadrícula (orden) dentro de una región; n, semilla, orden"""
    x0, y0, w, h, n = d["x"], d["y"], d["w"], d["h"], d.get("n", 40)
    r = _azar(d.get("semilla", 3))
    f = []
    if d.get("orden"):
        cols = max(2, int(math.sqrt(n * w / h)))
        filas = max(2, n // cols)
        for i in range(cols):
            for j in range(filas):
                f.append({"k": "circ", "x": x0 + (i + 0.5) * w / cols, "y": y0 + (j + 0.5) * h / filas, "r": 5, "fill": th["acc"], "op": 0.8})
    else:
        for _ in range(n):
            f.append({"k": "circ", "x": x0 + r() * w, "y": y0 + r() * h, "r": 3 + r() * 5, "fill": th["ink"], "op": 0.25 + r() * 0.5})
    return f


def e_onda(d, th):
    """onda senoidal (ritmo, señal, continuidad): x, y, w, amplitud, ciclos, neon"""
    x0, y0, w, a, c = d["x"], d["y"], d["w"], d.get("amp", 60), d.get("ciclos", 2.5)
    pts = [(x0 + w * i / 60, y0 + a * math.sin(2 * math.pi * c * i / 60)) for i in range(61)]
    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    col = d.get("fill", th["acc"])
    return ([{"k": "path", "d": path, "fill": col, "sw": d.get("sw", 8) * 3, "op": 0.2}] if d.get("neon") else []) + [{"k": "path", "d": path, "fill": col, "sw": d.get("sw", 8)}]


def e_arco(d, th):
    """anillo con arco de progreso (tiempo, avance, garantía): x, y, r, frac 0-1, sw, texto central opcional"""
    x, y, r, fr = d["x"], d["y"], d["r"], d.get("frac", 0.75)
    ang = -90 + 360 * fr
    x1, y1 = x + r * math.cos(math.radians(ang)), y + r * math.sin(math.radians(ang))
    f = [{"k": "circ", "x": x, "y": y, "r": r, "st": th["ink"], "sw": d.get("sw", 16), "sop": 0.12},
         {"k": "path", "d": f"M{x} {y - r} A{r} {r} 0 {1 if fr > 0.5 else 0} 1 {x1:.1f} {y1:.1f}", "fill": th["acc"], "sw": d.get("sw", 16)}]
    f += e_punto({"x": x1, "y": y1, "r": d.get("sw", 16) * 0.9, "fill": "#ffffff", "glow": True}, th)
    if d.get("t"):
        f.append(t(x, y + d.get("s", 90) * 0.3, d.get("s", 90), d["t"], th["ink"], 700, "middle", -3))
    return f


def e_infinito(d, th):
    """lazo infinito (siempre, vitalicio, ilimitado): x, y, w; un punto brillante lo recorre"""
    x, y, w = d["x"], d["y"], d["w"]
    pts = []
    for i in range(0, 81):
        a = 2 * math.pi * i / 80
        den = 1 + math.sin(a) ** 2
        pts.append((x + w / 2 * math.cos(a) / den * 1.4, y + w / 2 * math.sin(a) * math.cos(a) / den * 1.4))
    path = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    col = d.get("fill", th["acc"])
    return [{"k": "path", "d": path, "fill": col, "sw": 30, "op": 0.18}, {"k": "path", "d": path, "fill": col, "sw": 9}] + e_punto({"x": pts[10][0], "y": pts[10][1], "r": 14, "fill": "#ffffff", "glow": True}, th)


def e_desorden(d, th):
    """formas rotadas y dispersas (caos) o alineadas (orden): x, y, w, h, n, orden"""
    x0, y0, w, h, n = d["x"], d["y"], d["w"], d["h"], d.get("n", 12)
    r = _azar(d.get("semilla", 5))
    f = []
    cols = 4
    for i in range(n):
        if d.get("orden"):
            f.append({"k": "rect", "x": x0 + (i % cols) * (w / cols) + 8, "y": y0 + (i // cols) * (h / math.ceil(n / cols)) + 8, "w": w / cols - 16, "h": h / math.ceil(n / cols) - 16, "r": 8, "fill": th["acc"], "op": 0.75})
        else:
            f.append({"k": "rect", "x": x0 + r() * (w - 60), "y": y0 + r() * (h - 60), "w": 40 + r() * 40, "h": 30 + r() * 40, "r": 6, "fill": th["ink"], "op": 0.18 + r() * 0.3, "rot": int(r() * 90 - 45)})
    return f


def e_escalera(d, th):
    """escalones ascendentes (avance, nivel, mejora): x, y (base), w, h, n, resalta el último"""
    x0, y0, w, h, n = d["x"], d["y"], d["w"], d["h"], d.get("n", 5)
    ancho = w / n
    return [{"k": "rect", "x": x0 + i * ancho + 4, "y": y0 - h * (i + 1) / n, "w": ancho - 8, "h": h * (i + 1) / n, "r": 10, "fill": th["acc"] if i == n - 1 else th["ink"], "op": None if i == n - 1 else 0.10 + 0.04 * i} for i in range(n)]


ELEMENTOS.update({"particulas": e_particulas, "onda": e_onda, "arco": e_arco, "infinito": e_infinito, "desorden": e_desorden, "escalera": e_escalera})


FONDO_VIVO = " · FONDO VIVO: la aurora respira y deriva (8-12 s), el grano parpadea sutil y la textura se mueve en parallax; los vidrios brillan al entrar (barrido de luz)"


def escena(spec):
    """compone una escena LIBRE: spec = {"tema": gurú|solucion|explicar, "fondo": {luz, grano, textura, brillo} | color, "elementos": [{"e": ..., ...}], "mov": "indicación de movimiento"}
    Los elementos se dibujan en el orden dado (el primero queda al fondo): así un plano o una palabra puede quedar DETRÁS o DELANTE de otro."""
    tm = spec.get("tema", "solucion")
    th = th_de(tm)
    fo = spec.get("fondo")
    if isinstance(fo, dict):
        fondo_spec = fondo(tm, **fo)
    elif isinstance(fo, str):
        fondo_spec = fo
    else:
        fondo_spec = fondo(tm) if th["oscuro"] else (th["fondo"] if not isinstance(th["fondo"], dict) else fondo(tm, "abajo"))
    formas = []
    for el in spec["elementos"]:
        formas += ELEMENTOS[el["e"]](el, th)
    return {"fondo": fondo_spec, "formas": [f for f in formas if f is not None]}, spec.get("mov", "los elementos entran en el orden de la voz (sube 30 px y aparece, stagger 0,1 s)") + FONDO_VIVO
