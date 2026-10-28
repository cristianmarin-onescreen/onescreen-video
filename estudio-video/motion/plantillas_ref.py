"""Plantillas POR REFERENCIA (28-oct-2026). Regla de Cris: «cada idea que te he mandado sea una referencia de diseño y la guardes como plantilla; con eso siempre tendrás de dónde escoger».
Cada referencia nueva = una plantilla nueva (NUNCA se reemplaza una anterior). REFERENCIAS dice de qué imagen/video sale cada plantilla (imágenes en
D:\\OneScreen\\Contenido\\2026\\10. Octubre\\_referencias_motion\\); EJEMPLOS trae parámetros de muestra; `motion/catalogo.py` arma el catálogo visual
(referencia a la izquierda, nuestra plantilla a la derecha). Colores y tipografías de OneScreen siempre; solo se toma la idea de diseño."""
import math
from plantillas import AZ, NE, AC, L, tema, t, _fs, wrap, icono, orbita, PLANTILLAS


def escritura(p):
    """ref. «Imagine|»: texto que se escribe con cursor. params: texto, tema"""
    th = tema(p, "gurú")
    s = _fs(p["texto"], 1000, 150, 0.5)
    ancho = int(s * 0.5 * len(p["texto"]))
    f = [t(L + 40, 400, s, p["texto"], "#ffffff", 300, "start", -3, th["tg"]),
         {"k": "rect", "x": L + 40 + ancho + 14, "y": 400 - int(s * 0.78), "w": max(6, s // 18), "h": int(s * 0.95), "r": 2, "fill": th["ink"]}]
    return {"fondo": th["fondo"], "formas": f}, "el texto se escribe letra por letra con la voz y el cursor parpadea (0,5 s); al terminar, el cursor salta a la siguiente palabra"


def formas_flotantes(p):
    """ref. «Create +»: cuadros, rectángulos, parches de puntos y etiquetas rectangulares flotando alrededor de un botón con cursor que hace clic. params: boton, etiquetas [2], tema"""
    th = tema(p, "gurú")
    cl = lambda x, y, w, h, op=0.85: {"k": "rect", "x": x, "y": y, "w": w, "h": h, "fill": "#ffffff", "op": op}
    f = [cl(290, 140, 50, 50), cl(700, 150, 170, 50), {"k": "rect", "x": 200, "y": 470, "w": 50, "h": 50, "fill": th["acc"]}, cl(830, 560, 50, 50),
         {"k": "rect", "x": 880, "y": 610, "w": 200, "h": 50, "fill": th["acc"], "op": 0.8}]
    for px, py in [(250, 320), (960, 250), (540, 560), (1010, 450)]:
        f += [{"k": "circ", "x": px + i * 14, "y": py + j * 14, "r": 1.3, "fill": "#ffffff", "op": 0.28} for i in range(5) for j in range(5)]
    for (x, y), txt in zip([(70, 90), (900, 380)], (p.get("etiquetas") or ["Soporte", "Chat"])[:2]):
        f += [{"k": "rect", "x": x, "y": y, "w": 220, "h": 52, "r": 10, "fill": th["acc"], "op": 0.75}, t(x + 110, y + 35, 24, txt, NE, 500, "middle")]
    f += [{"k": "rect", "x": 490, "y": 322, "w": 300, "h": 76, "r": 14, "fill": "#ffffff", "op": 0.94, "glow": th["acc"], "brillo": True}, t(640, 372, 38, p.get("boton", "Crear +"), NE, 500, "middle", -1),
          {"k": "poly", "pts": "628,382 640,452 660,430 694,424", "fill": th["acc"]}]
    return {"fondo": th["fondo"], "formas": f}, "las formas flotan y se reacomodan con la voz; el cursor llega al botón, hace clic (el botón se hunde y rebota) y aparece lo siguiente"


def ui_burbujas(p):
    """ref. panel oscuro con burbujas de notificación. params: titulo, stats [{valor, etiqueta}] (4), burbujas [3], tema"""
    th = tema(p, "gurú")
    f = [{"k": "rect", "x": 250, "y": 140, "w": 780, "h": 480, "r": 26, "fill": "#0b0f14", "op": 0.92, "st": th["acc"], "sw": 1, "sop": 0.5, "glow": th["acc"], "brillo": True},
         t(290, 200, 28, p["titulo"], "#ffffff", 700, "start", -1)]
    for i, s in enumerate(p["stats"][:4]):
        x = 290 + i * 185
        f += [{"k": "rect", "x": x, "y": 240, "w": 170, "h": 110, "r": 14, "fill": "#ffffff", "op": 0.06, "st": "#ffffff", "sw": 1, "sop": 0.15},
              t(x + 16, 292, 42, str(s["valor"]), "#ffffff", 700, "start", -1), t(x + 16, 330, 18, s["etiqueta"], th["mut"], 400)]
    f += [{"k": "rect", "x": 290, "y": 380, "w": 700, "h": 200, "r": 14, "fill": "#ffffff", "op": 0.04, "st": "#ffffff", "sw": 1, "sop": 0.12},
          {"k": "path", "d": "M310 540 C400 480 470 560 560 500 S720 470 800 440 S930 430 970 400", "fill": th["acc"], "sw": 5}]
    for (x, y), b in zip([(170, 120), (880, 85), (930, 585)], (p.get("burbujas") or ["+14", "85", "27"])[:3]):
        f += [{"k": "rect", "x": x, "y": y, "w": 140, "h": 48, "r": 10, "fill": th["acc"], "glow": th["acc"]}, t(x + 70, y + 33, 26, b, NE, 700, "middle")]
    return {"fondo": th["fondo"], "formas": f}, "el panel sube y se acomoda; las burbujas aparecen con rebote (stagger 0,15 s) y los números cuentan hasta su valor"


def puntos_halo(p):
    """ref. paletas «Jade Horizon» / «Arctic Depths»: lista de puntos con halo + titular grande con degradado vertical. params: l1, l2, items [4], tema"""
    th = tema(p, "gurú")
    cols = [th["acc"], th["tg"][1], th["mut"], th["ink"]]
    f = []
    for i, it in enumerate(p["items"][:4]):
        y = 175 + i * 66
        f += [{"k": "circ", "x": L + 34, "y": y, "r": 30, "fill": cols[i], "op": 0.2}, {"k": "circ", "x": L + 34, "y": y, "r": 21, "fill": cols[i]}, t(L + 90, y + 11, 30, it, th["ink"], 600)]
    for k, (txt, y) in enumerate(((p["l1"], 555), (p["l2"], 688))):
        f.append(t(L, y, _fs(txt, 800, 130, 0.56), txt, th["ink"], 700, "start", -6) | {"gv": True})
    return {"fondo": th["fondo"], "formas": f}, "cada punto entra con su halo que se expande una vez (stagger 0,12 s); el titular sube con máscara y su degradado vertical se desvanece hacia abajo"


def escala_degradada(p):
    """ref. «Starry Night»: barra de degradado oscuro→blanco con etiquetas en cada tramo. params: l1, l2, pasos [4]"""
    th = tema(p, "claro")
    f = [t(640, 190, _fs(p["l1"], 900, 90, 0.5), p["l1"], th["ink"], 700, "middle", -3), t(640, 280, _fs(p["l2"], 900, 96, 0.54), p["l2"], th["ink"], 700, "middle", -3),
         {"k": "rect", "x": 100, "y": 380, "w": 1080, "h": 110, "r": 16, "fillgrad": ["#0b2166", AZ, "#9fc0ff", "#eef3ff"], "glow": AZ}]
    for i, s in enumerate(p["pasos"][:4]):
        f.append(t(100 + 60 + i * 322, 570, 32, s, th["ink"], 700, "start", -1))
    f.append({"k": "linea", "x1": 100, "y1": 630, "x2": 1180, "y2": 630, "fill": th["ink"], "sw": 1, "op": 0.3})
    return {"fondo": th["fondo"], "formas": f}, "la cápsula se llena de izquierda a derecha con el degradado (1 s); cada etiqueta sube cuando la voz llega a ese tramo"


def frase_orbita(p):
    """ref. «Creative success…»: frase de 3-4 líneas apretadas dentro de una órbita fina con destello, sobre degradado con GRANO fuerte. params: lineas, pie, tema"""
    th = tema(p, "solucion")
    fondo = dict(th["fondo"])
    fondo["grano"] = 0.4
    ln = p["lineas"][:4]
    s = _fs(max(ln, key=len), 760, 100, 0.5)
    f = [t(640, 290 + i * int(s * 1.0), s, x, "#ffffff", 700, "middle", -4) for i, x in enumerate(ln)]
    f += orbita(640, 290 + int(s * (len(ln) - 1) / 2) - 24, 430, 200, th)
    if p.get("pie"):
        f.append(t(640, 690, 20, p["pie"], th["mut"], 400, "middle", 3))
    return {"fondo": fondo, "formas": f}, "las líneas suben con máscara una a una; la órbita se TRAZA alrededor y el destello viaja sobre ella una vuelta; el grano vibra sutil"


def cita_tarjeta(p):
    """ref. tarjeta con pestañas 01-04 y sujeto que rompe el borde. params: texto, autor, tabs (4), activa, tema"""
    th = tema(p, "claro")
    n, act = p.get("tabs", 4), p.get("activa", 3) - 1
    f = []
    for i in range(n):
        f.append({"k": "rect", "x": 100 + i * 104, "y": 50, "w": 96, "h": 64 if i == act else 56, "r": 12, "fill": AZ if i == act else "#ffffff"})
        f.append(t(148 + i * 104, 92, 26, f"0{i + 1}", "#ffffff" if i == act else AZ, 600, "middle"))
    f += [{"k": "rect", "x": 100, "y": 110, "w": 1080, "h": 510, "r": 40, "fill": AZ, "glow": AZ}, t(150, 175, 26, p.get("autor", ""), "#cfe0ff", 400),
          t(150, 350, 170, "“", "#ffffff", 700, "start", 0)]
    for j, ln in enumerate(wrap(p["texto"], 26)[:5]):
        f.append(t(150, 430 + j * 50, 38, ln, "#ffffff", 400, "start", -1))
    f += [{"k": "rect", "x": 820, "y": 290, "w": 330, "h": 430, "r": 28, "fill": NE, "op": 0.88}, t(985, 520, 30, "tu plano aquí", "#ffffff", 400, "middle")]
    return {"fondo": th["fondo"], "formas": f}, "la pestaña activa se desliza y se funde con la tarjeta; la comilla cae con rebote; el texto se escribe con la voz; el plano entra desde abajo y rompe el borde (parallax)"


def editorial_rejilla(p):
    """ref. póster editorial de rejilla fina: círculo grande, etiqueta con degradado, titular apretado, objetos que rompen el marco. params: etiqueta, lineas (3), texto, paso, tema"""
    th = tema(p, "claro")
    f = [{"k": "linea", "x1": 160 * i, "y1": 0, "x2": 160 * i, "y2": 720, "fill": th["ink"], "sw": 1, "op": 0.12} for i in range(1, 8)]
    f += [{"k": "linea", "x1": 0, "y1": 144 * j, "x2": 1280, "y2": 144 * j, "fill": th["ink"], "sw": 1, "op": 0.12} for j in range(1, 5)]
    f.append({"k": "circ", "x": 640, "y": 380, "r": 340, "st": th["ink"], "sw": 1, "sop": 0.25})
    f += [{"k": "rect", "x": 330, "y": 110, "w": max(260, len(p["etiqueta"]) * 24 + 70), "h": 70, "r": 14, "fillgrad": [AZ, "#7a5cff"], "glow": AZ}, t(330 + max(260, len(p["etiqueta"]) * 24 + 70) // 2, 157, 34, p["etiqueta"], "#ffffff", 600, "middle", -1)]
    for i, ln in enumerate(p["lineas"][:3]):
        f.append(t(330, 290 + i * 92, 84, ln, th["ink"], 700, "start", -4))
    for j, ln in enumerate(wrap(p.get("texto", ""), 46)[:3]):
        f.append(t(330, 590 + j * 30, 22, ln, th["mut"], 400))
    f += [{"k": "rect", "x": -60, "y": -60, "w": 300, "h": 230, "r": 30, "fill": NE, "op": 0.85}, {"k": "rect", "x": 1000, "y": 560, "w": 340, "h": 240, "r": 30, "fill": NE, "op": 0.85}]
    spec = {"fondo": th["fondo"], "formas": f}
    return spec, "la rejilla se dibuja línea por línea; el círculo se traza; la etiqueta sube con brillo; los objetos entran desde las esquinas y rompen el marco"


def tarjetas_ilustradas(p):
    """ref. «Utilidades clínicas»: título mezclado light/bold y cinco tarjetas (3+2) con ícono y texto con negrita parcial. params: l1, l2, tarjetas [{icono, a, b}] (5), tema"""
    th = tema(p, "claro")
    f = [t(640, 190, _fs(p["l1"], 900, 76, 0.46), p["l1"], th["ink"], 300, "middle", -2), t(640, 285, _fs(p["l2"], 1000, 100, 0.56), p["l2"], th["acc"], 700, "middle", -3)]
    pos = [(70, 350, 340), (470, 350, 340), (870, 350, 340), (190, 520, 430), (660, 520, 430)]
    for (x, y, w), c in zip(pos, p["tarjetas"][:5]):
        f += [{"k": "rect", "x": x, "y": y, "w": w, "h": 140, "r": 20, "fill": "#ffffff", "glow": th["acc"], "brillo": True}] + icono(c.get("icono", "check"), x + 60, y + 70, 62, th["acc"])
        f += [t(x + 112, y + 66, 27, c["a"], th["ink"], 400, "start", -0.5), t(x + 112, y + 102, 30, c["b"], th["ink"], 700, "start", -0.5)]
    return {"fondo": th["fondo"], "formas": f}, "el título sube con máscara; las tarjetas entran en cascada (stagger 0,12 s) y cada ícono se dibuja; la negrita parcial se enciende al nombrarse"


def palabra_halo(p):
    """ref. «día mundial da saúde»: palabra gigante translúcida con halo de luz y el objeto delante. params: pre, palabra, lado [2 textos], fecha, tema"""
    th = tema(p, "solucion")
    s = _fs(p["palabra"], 760, 400, 0.58)
    f = [{"k": "rect", "x": 90, "y": 190, "w": 720, "h": 320, "r": 40, "fill": "#ffffff", "op": 0.22, "glow": "#ffffff"},
         t(L + 20, 175, 54, p["pre"], "#ffffff", 600, "start", -1), t(L + 20, 470, s, p["palabra"], "#ffffff", 700, "start", -14) | {"op": 0.92}]
    for j, tx in enumerate(p.get("lado", [])[:2]):
        for k, ln in enumerate(wrap(tx, 22)[:3]):
            f.append(t(940, 250 + j * 250 + k * 34, 25, ln, "#ffffff", 400))
    if p.get("fecha"):
        f += [t(L + 20, 560, 40, p["fecha"], "#ffffff", 400), {"k": "linea", "x1": L + 20, "y1": 576, "x2": L + 150, "y2": 576, "fill": "#ffffff", "sw": 3}]
    f += [{"k": "rect", "x": 700, "y": 200, "w": 200, "h": 480, "r": 30, "fill": "#0a1b55", "glow": "#ffffff", "brillo": True}, t(800, 650, 22, "tu objeto o plano", "#ffffff", 400, "middle")]
    return {"fondo": th["fondo"], "formas": f}, "la palabra gigante se enciende con su halo (respira lento); el objeto entra desde abajo y queda delante, tapando parte de las letras; los textos laterales suben con la voz"


def linea_neon(p):
    """ref. «When a Brand Stops Evolving»: línea de neón con punto brillante sobre piso de rejilla en perspectiva, sobre azul profundo. params: l1, clave, l2, cta"""
    th = tema(p, "solucion")
    fondo = {"grad": ["#0b2166", "#050f33"], "ang": 180, "tex": "puntos", "texop": 0.14, "luces": [[760, 330, 520, AZ, 0.28]]}
    d = "M-20 640 C120 600 200 700 330 640 S470 520 560 560 S700 610 770 520 S900 440 1010 300"
    f = [t(L, 230, 74, p["l1"] + " ", "#ffffff", 700, "start", -2), t(L + int(74 * 0.57 * (len(p["l1"]) + 1)) + 10, 230, 74, p["clave"], "#ffffff", 700, "start", -2, [th["acc"], "#4aa3ff"]),
         t(L, 316, 74, p["l2"], "#ffffff", 300, "start", -2),
         {"k": "rect", "x": L, "y": 400, "w": 250, "h": 62, "r": 12, "st": "#ffffff", "sw": 2, "sop": 0.8}, {"k": "path", "d": "M130 431 L300 431 M284 419 L300 431 L284 443", "fill": "#ffffff", "sw": 2}]
    f += [{"k": "linea", "x1": 640 + i * 32, "y1": 600, "x2": 640 + i * 150, "y2": 720, "fill": "#ffffff", "sw": 1, "op": 0.22} for i in range(-8, 9)]
    f += [{"k": "linea", "x1": 0, "y1": y, "x2": 1280, "y2": y, "fill": "#ffffff", "sw": 1, "op": 0.22} for y in (600, 625, 655, 692)]
    f += [{"k": "path", "d": d, "fill": th["acc"], "sw": 34, "op": 0.22}, {"k": "path", "d": d, "fill": th["acc"], "sw": 11},
          {"k": "circ", "x": 1010, "y": 300, "r": 24, "fill": th["acc"], "glow": th["acc"]}]
    return {"fondo": fondo, "formas": f}, "la línea de neón se DIBUJA de izquierda a derecha con su resplandor (1,4 s) hasta el punto, que late; el piso de rejilla se desplaza en perspectiva; la palabra clave entra desenfocándose a nítida"


def esfera_suave(p):
    """ref. tarjeta «Zen Space»: esfera suave de atmósfera, orbe pequeño y texto con cifra grande abajo. params: origen, etiqueta, titulo, valor, unidad, detalle"""
    th = tema(p, "solucion")
    f = [{"k": "circ", "x": 1010, "y": 400, "r": 520, "fill": "#ffffff", "op": 0.26, "glow": "#ffffff"}, {"k": "circ", "x": 560, "y": 100, "r": 26, "fill": th["acc"], "glow": th["acc"]},
         {"k": "circ", "x": L + 40, "y": 110, "r": 52, "fill": "#ffffff", "op": 0.92}] + icono("persona", L + 40, 112, 48, th["acc"])
    f += [t(L, 250, 28, p["origen"], "#ffffff", 400), t(L, 300, 26, p.get("detalle", ""), th["mut"], 400), t(L, 400, 26, p["etiqueta"], th["mut"], 400)]
    for j, ln in enumerate(wrap(p["titulo"], 30)[:3]):
        f.append(t(L, 450 + j * 46, 40, ln, "#ffffff", 700, "start", -1))
    f += [{"k": "linea", "x1": L, "y1": 590, "x2": 900, "y2": 590, "fill": "#ffffff", "sw": 2}, t(L, 680, 130, str(p["valor"]), "#ffffff", 700, "start", -6), t(L + int(len(str(p["valor"])) * 130 * 0.58) + 16, 680, 40, p["unidad"], "#ffffff", 500)]
    return {"fondo": th["fondo"], "formas": f}, "la esfera respira (escala 1→1,03 en 8 s) y el orbe orbita lento; el texto sube con máscara; la cifra grande cuenta hasta su valor"


def curvas_tarjetas(p):
    """ref. 20: dos curvas suaves que se cruzan con tarjetas ancladas a líneas finas y dos tarjetas grandes a los lados. params: izq, der (títulos de las tarjetas grandes), notas [3 textos], tema"""
    th = tema(p, "explicar")
    A = "M330 380 C 400 300 470 280 540 330 S 650 470 740 420 S 860 380 950 400"
    B = "M330 330 C 400 400 450 470 540 440 S 650 250 760 230 S 880 330 950 380"
    f = [{"k": "linea", "x1": x, "y1": y1, "x2": x, "y2": y2, "fill": th["ink"], "sw": 1, "op": 0.3} for x, y1, y2 in ((330, 120, 600), (540, 140, 600), (740, 120, 600), (950, 120, 600))]
    f += [{"k": "path", "d": A + " L950 560 L330 560 Z", "fill": AZ, "sw": 0, "relgrad": AZ, "op": 0.0}, {"k": "path", "d": B + " L950 560 L330 560 Z", "fill": AC, "sw": 0, "relgrad": AC, "op": 0.0},
          {"k": "path", "d": A, "fill": AZ, "sw": 9}, {"k": "path", "d": B, "fill": AC, "sw": 9}]
    notas = (p.get("notas") or ["Dato uno", "Dato dos", "Dato tres"])[:3]
    for (x, y), n_ in zip(((470, 110), (700, 70), (500, 500)), notas):
        f += [{"k": "rect", "x": x - 70, "y": y, "w": 220, "h": 92, "r": 12, "fill": "#ffffff", "glow": th["acc"], "brillo": True}, {"k": "rect", "x": x - 50, "y": y + 20, "w": 22, "h": 22, "r": 5, "fill": th["acc"]},
              t(x - 16, y + 38, 22, n_, th["ink"], 700, "start", -0.5), {"k": "rect", "x": x - 50, "y": y + 58, "w": 170, "h": 6, "r": 3, "fill": th["ink"], "op": 0.15}]
    for x, y, w, h, ti, col in ((60, 230, 270, 250, p.get("izq", "Antes"), AZ), (950, 190, 270, 270, p.get("der", "Después"), AC)):
        f += [{"k": "rect", "x": x, "y": y, "w": w, "h": h, "r": 16, "fill": "#ffffff", "glow": th["acc"], "brillo": True}, {"k": "rect", "x": x + 20, "y": y + 20, "w": w - 40, "h": h * 0.5, "r": 10, "fill": th["ink"], "op": 0.08},
              {"k": "rect", "x": x + 20, "y": y + h * 0.5 + 40, "w": 60, "h": 14, "r": 4, "fill": col}, t(x + 20, y + h * 0.5 + 90, 26, ti, th["ink"], 700, "start", -1),
              {"k": "rect", "x": x + 20, "y": y + h * 0.5 + 110, "w": w - 60, "h": 6, "r": 3, "fill": th["ink"], "op": 0.15}]
    return {"fondo": th["fondo"], "formas": f}, "las dos curvas se dibujan a la vez y se cruzan; las líneas finas bajan y las tarjetas se anclan con rebote en cada cruce; las tarjetas grandes entran desde los lados"


def dashboard_flotante(p):
    """ref. 21: ventana fantasma con tarjetas flotantes (resumen con etiquetas, cursor con nombre, cifra con barras, mini gráfica con burbuja). params: titulo, numero, subtitulo, ingresos, egresos, nombre"""
    th = tema(p, "explicar")
    ac = th["acc"]
    f = [{"k": "rect", "x": 150, "y": 110, "w": 720, "h": 400, "r": 22, "fill": th["ink"], "op": 0.04, "st": th["ink"], "sw": 1, "sop": 0.08},
         {"k": "rect", "x": 560, "y": 56, "w": 320, "h": 46, "r": 10, "fill": "#ffffff", "glow": ac}, t(590, 86, 20, p.get("buscar", "Buscar"), "#8a93a6", 400)]
    # tarjeta izquierda
    f += [{"k": "rect", "x": 80, "y": 200, "w": 330, "h": 170, "r": 16, "fill": "#ffffff", "glow": ac, "brillo": True}, {"k": "circ", "x": 112, "y": 236, "r": 14, "fill": th["ink"], "op": 0.18}, t(140, 244, 24, p["titulo"], th["ink"], 700, "start", -0.5)]
    f += [{"k": "rect", "x": 108, "y": 272 + i * 22, "w": 240 - i * 40, "h": 7, "r": 3, "fill": th["ink"], "op": 0.13} for i in range(3)]
    f += [{"k": "rect", "x": 108 + i * 70, "y": 340, "w": 60 if i < 2 else 90, "h": 16, "r": 6, "fill": ac if i == 0 else th["ink"], "op": 0.35 if i == 0 else 0.12} for i in range(3)]
    # cursor con nombre
    f += [{"k": "poly", "pts": "420,240 424,278 436,266 452,268", "fill": ac}, {"k": "rect", "x": 440, "y": 290, "w": 96, "h": 40, "r": 8, "fill": th["ink"]}, t(488, 317, 20, p.get("nombre", "Kate"), "#ffffff", 500, "middle")]
    # tarjeta de cifra
    f += [{"k": "rect", "x": 620, "y": 170, "w": 340, "h": 410, "r": 18, "fill": "#ffffff", "glow": ac, "brillo": True}, t(650, 232, 38, p["numero"], th["ink"], 700, "start", -1), t(650, 262, 18, p.get("subtitulo", ""), th["mut"], 400)]
    for i, h in enumerate((70, 100, 160, 62, 124, 120)):
        f.append({"k": "rect", "x": 650 + i * 48, "y": 440 - h, "w": 34, "h": h, "r": 8, "fill": ac if i == 2 else th["ink"], "op": None if i == 2 else 0.08})
    for j, (lab, val, col) in enumerate(((p.get("ingresos", ["Ingresos", "8,561"])[0], p.get("ingresos", ["Ingresos", "8,561"])[1], ac), (p.get("egresos", ["Egresos", "11,853"])[0], p.get("egresos", ["Egresos", "11,853"])[1], AC))):
        f += [{"k": "circ", "x": 676, "y": 500 + j * 62, "r": 24, "fill": col, "op": 0.25}, t(718, 494 + j * 62, 18, lab, th["mut"], 400), t(718, 522 + j * 62, 26, val, th["ink"], 700, "start", -0.5)]
    # mini gráfica con burbuja
    f += [{"k": "rect", "x": 260, "y": 420, "w": 300, "h": 140, "r": 16, "fill": "#ffffff", "glow": ac, "brillo": True},
          {"k": "path", "d": "M285 530 C320 500 340 530 380 500 S440 470 480 470 L540 440 L540 548 L285 548 Z", "fill": ac, "sw": 0, "relgrad": ac}, {"k": "path", "d": "M285 530 C320 500 340 530 380 500 S440 470 480 470 L540 440", "fill": ac, "sw": 4},
          {"k": "circ", "x": 480, "y": 470, "r": 7, "fill": "#ffffff", "st": ac, "sw": 3}, {"k": "rect", "x": 448, "y": 424, "w": 66, "h": 26, "r": 6, "fill": th["ink"], "op": 0.55}]
    return {"fondo": th["fondo"], "formas": f}, "la ventana fantasma aparece desde el fondo; las tarjetas flotan hacia su sitio con parallax distinto (cada una a su velocidad); el cursor viaja y la etiqueta con el nombre aparece; las barras crecen y las cifras cuentan"


def _sector(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return f"M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {1 if a1 - a0 > 180 else 0} 1 {x1:.1f} {y1:.1f} Z"


def infografia_paneles(p):
    """ref. 22: ilustración vectorial de paneles con barras de degradado, curvas con marcadores, pastel y mini gráfica de área. params: titulo (opcional), pct"""
    th = tema(p, "explicar")
    ac = th["acc"]
    f = [t(L, 120, _fs(p["titulo"], 700, 60, 0.5), p["titulo"], th["ink"], 700, "start", -2)] if p.get("titulo") else []
    f += [{"k": "rect", "x": 330, "y": 190, "w": 560, "h": 360, "r": 22, "fill": "#ffffff", "glow": ac, "brillo": True}, {"k": "rect", "x": 560, "y": 215, "w": 100, "h": 16, "r": 6, "fill": th["ink"], "op": 0.1}]
    for i, h in enumerate((200, 150, 90, 130, 170, 110)):
        f.append({"k": "rect", "x": 400 + i * 78, "y": 510 - h, "w": 46, "h": h, "r": 8, "fillgrad": [AC, "#ffffff"], "fgv": True})
    f += [{"k": "rect", "x": 90, "y": 270, "w": 270, "h": 300, "r": 22, "fill": "#ffffff", "glow": ac, "brillo": True}, {"k": "rect", "x": 130, "y": 295, "w": 100, "h": 14, "r": 6, "fill": th["ink"], "op": 0.1},
          {"k": "path", "d": "M120 440 C150 330 200 340 230 400 S300 440 340 340", "fill": AC, "sw": 6}, {"k": "path", "d": "M120 380 C160 400 200 470 240 450 S300 420 330 450", "fill": AZ, "sw": 6},
          {"k": "circ", "x": 190, "y": 342, "r": 12, "fill": "#ffffff", "st": AC, "sw": 4}, {"k": "circ", "x": 240, "y": 450, "r": 12, "fill": "#ffffff", "st": AZ, "sw": 4}]
    cx, cy, r = 960, 200, 95
    f += [{"k": "path", "d": _sector(cx, cy, r, -90, 60), "fill": AC, "rel": AC, "sw": 0}, {"k": "path", "d": _sector(cx, cy, r, 60, 150), "fill": AZ, "rel": AZ, "sw": 0}, {"k": "path", "d": _sector(cx, cy, r + 10, 150, 270), "fill": "#9fc0ff", "rel": "#9fc0ff", "sw": 0, "op": 0.7},
          t(cx - 30, cy - 30, 40, p.get("pct", "%"), "#ffffff", 700, "middle")]
    f += [{"k": "rect", "x": 800, "y": 420, "w": 230, "h": 170, "r": 20, "fill": "#ffffff", "glow": AZ, "brillo": True}, {"k": "path", "d": "M820 560 C850 480 880 520 910 470 S980 480 1010 450 L1010 570 L820 570 Z", "fill": AZ, "sw": 0, "relgrad": AZ},
          {"k": "path", "d": "M820 560 C850 500 880 530 910 490 S980 500 1010 470 L1010 570 L820 570 Z", "fill": AC, "sw": 0, "relgrad": AC, "op": 0.6}]
    for x_, y_ in ((140, 190), (1120, 360)):
        f += [{"k": "path", "d": f"M{x_} {y_} L{x_ + 14} {y_ + 12} L{x_ + 28} {y_} M{x_} {y_ + 16} L{x_ + 14} {y_ + 28} L{x_ + 28} {y_ + 16}", "fill": th["ink"], "sw": 4, "op": 0.25}]
    return {"fondo": th["fondo"], "formas": f}, "los paneles entran escalonados con rebote suave; las barras crecen con su degradado, las curvas se dibujan y los marcadores laten; el pastel se arma sector por sector con la voz"


NUEVAS = {"escritura": escritura, "formas_flotantes": formas_flotantes, "ui_burbujas": ui_burbujas, "puntos_halo": puntos_halo, "escala_degradada": escala_degradada,
          "frase_orbita": frase_orbita, "cita_tarjeta": cita_tarjeta, "editorial_rejilla": editorial_rejilla, "tarjetas_ilustradas": tarjetas_ilustradas,
          "palabra_halo": palabra_halo, "linea_neon": linea_neon, "esfera_suave": esfera_suave,
          "curvas_tarjetas": curvas_tarjetas, "dashboard_flotante": dashboard_flotante, "infografia_paneles": infografia_paneles}
PLANTILLAS.update(NUEVAS)

# ---- de qué referencia sale cada plantilla (imágenes en _referencias_motion; None = sin imagen guardada, solo descripción) ----
REFERENCIAS = {
    "frase": ("apple/sheets/y2018_01.jpg", "Lettering de Apple (video «Apple Event 2018 in 108 seconds»): 1-3 palabras, degradado en la palabra clave; marcador `resalta` y número fantasma de `ideas/1.webp`"),
    "titular": ("apple/sheets/y2018_02.jpg", "Titulares de Apple: dos líneas, light + bold, palabra con degradado"),
    "keynote": (None, "awesomeclaude «Dark tech keynote»: una cifra gigante, rejilla fina, un solo acento"),
    "cifra": (None, "alias de keynote"),
    "panel4": (None, "Cotización de Gurú/Academy de Cris: degradado profundo + textura + 4 tarjetas de vidrio"),
    "tarjetas": (None, "Tarjetas de vidrio de la cotización de Cris"),
    "flujo": (None, "Flujo con íconos de línea en tarjetas de vidrio (estilo Flota de IA)"),
    "comparacion": (None, "Mitades a sangre antes/después"),
    "tachado": (None, "Barra de acento que tacha (Flota de IA)"),
    "pantalla": (None, "Pantalla genérica con filas"),
    "checklist": (None, "Filas que se marcan"),
    "cta": (None, "Cierre con flecha que se dibuja"),
    "barras": (None, "awesomeclaude «Data story»: un gráfico, una anotación"),
    "linea": (None, "awesomeclaude «Single line & live drawing»: una sola línea continua"),
    "isometrico": (None, "awesomeclaude «Isometric miniature world»"),
    "notificacion": ("ideas/8.png", "Notificación con pila de capas (Elevare Consulting)"),
    "curva": ("ideas/9.png", "Gráfica de área con burbujas de valor (GatesFX)"),
    "orbitas": ("ideas/10.webp", "Anillos finos con íconos en discos (Olist)"),
    "chips": ("ideas/11.png", "Chips flotantes sobre anillos suaves (Projetura)"),
    "ruta": ("ideas/12.png", "Contenedor con borde degradado y filas con flecha (casa inteligente)"),
    "tarjetas_ilustradas": ("ideas/13.png", "Cinco tarjetas con ícono y negrita parcial (Utilidades clínicas)"),
    "pregunta": ("ideas/14.png", "Pregunta cinética con interruptor SÍ/NO y flechas (Protexiones)"),
    "tarjeta_plano": ("ideas/15.webp", "Objeto que rompe el borde de la tarjeta (pneumonia)"),
    "palabra_halo": ("ideas/16.png", "Palabra gigante con halo y objeto delante (día mundial da saúde)"),
    "escritura": ("ideas/1.webp", "«Imagine|»: texto que se escribe con cursor"),
    "formas_flotantes": ("ideas/1.webp", "«Create +»: formas flotantes y cursor que hace clic"),
    "ui_burbujas": ("ideas/1.webp", "Panel oscuro con burbujas de notificación"),
    "puntos_halo": ("ideas/2.webp", "Paletas «Jade Horizon» / «Arctic Depths» (ideas/3.webp)"),
    "escala_degradada": ("ideas/4.png", "«Starry Night»: cápsula de degradado con tramos"),
    "frase_orbita": ("ideas/5.webp", "«Creative success…»: frase en órbita con destello y grano fuerte"),
    "cita_tarjeta": ("ideas/6.png", "Tarjeta con pestañas 01-04 y sujeto que rompe el borde"),
    "editorial_rejilla": ("ideas/7.png", "Póster editorial de rejilla fina con círculo y objetos que rompen el marco"),
    "linea_neon": ("ideas/18.webp", "«When a Brand Stops Evolving»: línea de neón sobre piso de rejilla"),
    "esfera_suave": ("ideas/19.webp", "Tarjeta «Zen Space»: esfera suave y cifra grande"),
    "curvas_tarjetas": ("ideas/20.png", "Dos curvas que se cruzan con tarjetas ancladas a líneas finas y tarjetas grandes a los lados"),
    "dashboard_flotante": ("ideas/21.png", "Ventana fantasma con tarjetas flotantes: resumen, cursor con nombre, cifra con barras, mini gráfica"),
    "infografia_paneles": ("ideas/22.png", "Ilustración vectorial de paneles: barras de degradado, curvas con marcadores, pastel y mini gráfica"),
}

EJEMPLOS = {
    "frase": {"texto": "Imagina ahorrar 50% de tiempo", "clave": "50%", "resalta": True, "fantasma": "50%", "tema": "gurú"},
    "titular": {"l1": "Cuando todo falla", "l2": "necesitas algo confiable", "tema": "solucion"},
    "keynote": {"valor": "+20", "etiqueta": "idiomas en una sola pantalla", "tema": "explicar"},
    "panel4": {"titulo": "OneScreen Gurú", "subtitulo": "Soporte técnico 24/5, vitalicio y sin costo.", "texto": "Ingenieros reales acompañan a tu equipo.", "tarjetas": [{"icono": "auriculares", "titulo": "Canales", "texto": "Chat, llamada o videollamada."}, {"icono": "toque", "titulo": "A un botón", "texto": "Presiona el botón verde."}, {"icono": "pantalla", "titulo": "Sesiones", "texto": "1:1 con ingenieros."}, {"icono": "grupo", "titulo": "Toda la familia", "texto": "Incluido en todo."}], "tema": "gurú"},
    "tarjetas": {"items": [{"icono": "check", "titulo": "Siempre actualizada", "texto": "Mejoras sin costo."}, {"icono": "auriculares", "titulo": "Soporte prioritario", "texto": "Ingenieros reales."}, {"icono": "globo", "titulo": "Sin sorpresas", "texto": "Cuota mensual fija."}], "tema": "solucion"},
    "flujo": {"titulo": "Se transcribe sola", "nodos": ["Voz", "Texto", "Acta", "Listo"], "tema": "explicar"},
    "comparacion": {"izq": "Papeleo", "der": "Una pantalla"},
    "tachado": {"texto": "Nadie arma", "tachado": "el acta", "tema": "explicar"},
    "pantalla": {"titulo": "Soporte en vivo", "lineas": ["Chat con ingeniero", "Videollamada", "Manuales", "Agendar"], "tema": "explicar"},
    "checklist": {"titulo": "Incluye", "items": ["Instalación", "Capacitación", "Soporte técnico"], "tema": "solucion"},
    "cta": {"texto": "Escríbenos por WhatsApp", "sub": "onescreenlatam.com", "tema": "solucion"},
    "barras": {"valores": [12, 30, 58, 120], "etiquetas": ["2022", "2023", "2024", "2025"], "nota": "se duplicó en un año", "tema": "explicar"},
    "linea": {"puntos": ["Aula", "Escuela", "Ciudad", "País"], "tema": "explicar"},
    "isometrico": {"items": ["Pantalla", "Cámara", "Soporte"], "tema": "explicar"},
    "notificacion": {"titulo": "OneScreen Gurú", "texto": "Un ingeniero ya está disponible para tu videollamada", "hora": "ahora", "icono": "auriculares", "tema": "solucion"},
    "curva": {"titulo": "Aulas conectadas", "valores": [12, 18, 16, 30, 28, 44, 58, 90], "etiqueta": "+120 aulas", "marca": "2024", "tema": "explicar"},
    "orbitas": {"lineas": ["preguntas y", "respuestas"], "iconos": ["auriculares", "chat", "doc", "globo"], "tema": "solucion"},
    "chips": {"centro": ["Todas las", "herramientas que necesitas"], "items": [{"icono": "chat", "texto": "Chat en vivo"}, {"icono": "auriculares", "texto": "Llamada con ingeniero"}, {"icono": "pantalla", "texto": "Videollamada 1:1"}, {"icono": "doc", "texto": "Manuales y guías"}, {"icono": "grupo", "texto": "Capacitación del equipo"}], "tema": "explicar"},
    "ruta": {"l1": "Un día con", "l2": "soporte vitalicio", "filas": [{"etiqueta": "Mañana", "texto": "agendas tu capacitación"}, {"etiqueta": "Tarde", "texto": "el ingeniero resuelve en vivo"}, {"etiqueta": "Noche", "texto": "tu aula queda lista"}], "tema": "explicar"},
    "tarjetas_ilustradas": {"l1": "Acciones que", "l2": "mejoran tu aula", "tarjetas": [{"icono": "persona", "a": "Capacitar a tus", "b": "docentes"}, {"icono": "auriculares", "a": "Tener soporte", "b": "vitalicio"}, {"icono": "pantalla", "a": "Usar tu pantalla", "b": "a diario"}, {"icono": "grupo", "a": "Involucrar a", "b": "todo el equipo"}, {"icono": "check", "a": "Medir los", "b": "resultados"}], "tema": "explicar"},
    "pregunta": {"l1": "¿Ya tienes", "clave": "soporte", "l3": "técnico?", "opciones": ["SÍ", "NO"], "respuesta": "¡Felicitaciones!", "tema": "explicar"},
    "tarjeta_plano": {"l1": "Soporte", "l2": "vitalicio", "texto": "Ingenieros reales acompañan a tu equipo.", "cta": "Escríbenos por WhatsApp", "tema": "gurú"},
    "palabra_halo": {"pre": "tu aula con", "palabra": "soporte", "lado": ["Ingenieros reales acompañan a tu equipo.", "Sin tiempos de espera ni tickets."], "fecha": "24/5", "tema": "solucion"},
    "escritura": {"texto": "Imagina", "tema": "gurú"},
    "formas_flotantes": {"boton": "Pedir ayuda +", "etiquetas": ["Chat", "Llamada"], "tema": "gurú"},
    "ui_burbujas": {"titulo": "Tus sesiones", "stats": [{"valor": 15, "etiqueta": "este mes"}, {"valor": 120, "etiqueta": "consultas"}, {"valor": 30, "etiqueta": "docentes"}, {"valor": 5, "etiqueta": "sedes"}], "burbujas": ["+14", "85", "27"], "tema": "gurú"},
    "puntos_halo": {"l1": "Soporte", "l2": "vitalicio", "items": ["Chat en vivo", "Llamada", "Videollamada", "Sesión 1:1"], "tema": "gurú"},
    "escala_degradada": {"l1": "De la duda", "l2": "a la solución", "pasos": ["Escribes", "Hablas", "Resolvemos", "Listo"], "tema": "explicar"},
    "frase_orbita": {"lineas": ["Un aula sin", "soporte no es", "una aula", "conectada"], "pie": "onescreenlatam.com", "tema": "solucion"},
    "cita_tarjeta": {"texto": "El soporte vitalicio cambió la forma en que usamos la pantalla.", "autor": "Colegio Nueva Inglaterra", "tema": "explicar"},
    "editorial_rejilla": {"etiqueta": "Soporte vitalicio", "lineas": ["No es solo", "una pantalla.", "Es un equipo."], "texto": "Ingenieros reales acompañan a tus docentes, sin tickets ni esperas.", "paso": "3/4", "tema": "explicar"},
    "linea_neon": {"l1": "Cuando un aula", "clave": "no evoluciona", "l2": "se queda atrás"},
    "curvas_tarjetas": {"izq": "Antes", "der": "Después", "notas": ["Consulta", "Respuesta", "Solución"], "tema": "explicar"},
    "dashboard_flotante": {"titulo": "Gestión de soporte", "numero": "13.574", "subtitulo": "Del 10 de nov al 10 de dic", "ingresos": ["Resueltas", "8.561"], "egresos": ["Pendientes", "1.853"], "nombre": "Kate", "buscar": "Buscar", "tema": "explicar"},
    "infografia_paneles": {"titulo": "Todo en un solo lugar", "pct": "%", "tema": "explicar"},
    "esfera_suave": {"origen": "OneScreen Academy", "detalle": "Ruta para docentes", "etiqueta": "Certificación", "titulo": "Certificamos a todo tu equipo, con formación de por vida.", "valor": 24, "unidad": "horas"},
}
