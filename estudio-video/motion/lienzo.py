"""LIENZO DE ELEMENTOS UI: una sola página con TODO el vocabulario de motion/elementos.py, cada elemento visible en los tres colores de significado
(Gurú verde · solución azul · explicar blanco) y con el código para usarlo. Sirve para ver qué hay, escoger y copiar.
Uso: python estudio-video/motion/lienzo.py [SALIDA.html]   (por defecto: D:\\OneScreen\\Contenido\\2026\\10. Octubre\\_referencias_motion\\lienzo_elementos.html)
Cuando se agrega un elemento nuevo a elementos.py, se agrega su demo en DEMOS y se regenera el lienzo."""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "herramientas"))
import plantillas  # noqa: E402,F401
import elementos   # noqa: E402
from boceto import boceto_svg  # noqa: E402

SALIDA = Path("D:/OneScreen/Contenido/2026/10. Octubre/_referencias_motion/lienzo_elementos.html")
TEMAS = (("gurú", "Gurú · verde"), ("solucion", "Solución · azul"), ("explicar", "Explicar · blanco"))
C = (640, 360)   # centro; cada demo se recorta a 800x450 alrededor de su centro (o de su "caja")

# (categoría, nombre del elemento, descripción, [dicts de elementos], opciones: {"caja": (x, y, w), "fondo": {...}})
DEMOS = [
    ("Fondos", "fondo · luz", "Degradado profundo + aurora + grano + textura casi invisible. La luz cambia de lado entre escenas (abajo, arriba-der, abajo-der, centro, izquierda, arriba).",
     [{"e": "texto", "x": 640, "y": 380, "s": 64, "a": "middle", "t": "luz: abajo", "tono": "blanco"}], {"fondo": {"luz": "abajo"}}),
    ("Fondos", "fondo · luz arriba-der + rejilla", "Misma idea con la luz desde la esquina y rejilla sutil.",
     [{"e": "texto", "x": 640, "y": 380, "s": 64, "a": "middle", "t": "arriba-der + rejilla", "tono": "blanco"}], {"fondo": {"luz": "arriba-der", "textura": "rejilla"}}),
    ("Tipografía", "titulo", "Líneas que mezclan light y bold; la última con degradado. s = tamaño, ancho = ancho máximo.",
     [{"e": "titulo", "x": 220, "y": 340, "s": 78, "ancho": 520, "lineas": [["Soporte que", 300], ["responde", 700, "grad"]]}], {}),
    ("Tipografía", "texto", "Texto suelto: peso, tono (ink, mut, acc, blanco), degradado (grad) o degradado vertical que se desvanece (gv).",
     [{"e": "texto", "x": 640, "y": 340, "s": 90, "a": "middle", "t": "texto", "grad": True}, {"e": "texto", "x": 640, "y": 420, "s": 40, "a": "middle", "t": "peso 400 · tono mut", "w": 400, "tono": "mut"}], {}),
    ("Tipografía", "marcador", "Píldora de color con halo detrás de la frase clave (ref. «50% less time»).",
     [{"e": "marcador", "x": 400, "y": 290, "w": 440, "h": 100, "t": "sin costo"}], {}),
    ("Tipografía", "fantasma", "Número o palabra gigante en contorno detrás del texto.",
     [{"e": "fantasma", "x": 330, "y": 500, "t": "24/5", "s": 330}, {"e": "texto", "x": 640, "y": 370, "s": 56, "a": "middle", "t": "soporte", "tono": "ink"}], {}),
    ("Tipografía", "boton", "Botón/etiqueta RECTANGULAR de esquinas suaves: contorno, blanca, oscura o acento. (La píldora está prohibida.)",
     [{"e": "boton", "x": 320, "y": 300, "t": "contorno", "estilo": "contorno", "s": 44}, {"e": "boton", "x": 640, "y": 300, "t": "blanca", "estilo": "blanca", "s": 44},
      {"e": "boton", "x": 320, "y": 420, "t": "oscura", "estilo": "oscura", "s": 44}, {"e": "boton", "x": 640, "y": 420, "t": "acento", "estilo": "acento", "s": 44}], {}),
    ("Contenedores", "vidrio", "Contenedor translúcido que brilla: halo de acento + borde con luz.",
     [{"e": "vidrio", "x": 440, "y": 250, "w": 400, "h": 220}, {"e": "texto", "x": 640, "y": 372, "s": 40, "a": "middle", "t": "vidrio", "tono": "ink"}], {}),
    ("Contenedores", "blanca", "Tarjeta blanca sólida con halo, para UI flotante.",
     [{"e": "blanca", "x": 440, "y": 250, "w": 400, "h": 220}, {"e": "texto", "x": 640, "y": 372, "s": 40, "a": "middle", "t": "blanca", "tono": "oscuro"}], {}),
    ("Contenedores", "chip", "Ícono en cuadro tintado + 1-2 líneas de texto.",
     [{"e": "chip", "x": 470, "y": 310, "t": "Llamada con ingeniero", "icono": "auriculares", "w": 340}], {}),
    ("Contenedores", "notificacion", "Aviso con pila de capas translúcidas detrás (ref. «Elevare»).",
     [{"e": "notificacion", "x": 340, "y": 290, "w": 600, "h": 170, "titulo": "Soporte", "t": "Ya estoy en línea, cuéntame qué pasa", "n": 28, "hora": "ahora", "icono": "auriculares"}], {}),
    ("Contenedores", "tarjeta_stat", "Cifra grande, subtítulo y dos filas de resumen.",
     [{"e": "tarjeta_stat", "x": 480, "y": 200, "w": 320, "h": 290, "valor": "13.574", "sub": "del 10 nov al 10 dic", "filas": [["Resueltas", "8.561"], ["Pendientes", "1.853"]]}], {}),
    ("Contenedores", "plano", "Marco del plano/objeto del video (nunca se dibuja contenido ajeno). Puede romper el borde de un vidrio.",
     [{"e": "vidrio", "x": 400, "y": 240, "w": 480, "h": 230}, {"e": "plano", "x": 560, "y": 150, "w": 200, "h": 420}], {}),
    ("UI", "burbuja", "Burbuja de valor o aviso flotante con halo.",
     [{"e": "burbuja", "x": 520, "y": 330, "t": "+120 aulas"}], {}),
    ("UI", "cursor", "Cursor con etiqueta de nombre que hace clic.",
     [{"e": "boton", "x": 640, "y": 330, "t": "Pedir ayuda", "estilo": "blanca", "s": 40, "centrada": True}, {"e": "cursor", "x": 700, "y": 350, "nombre": "Kate"}], {}),
    ("UI", "progreso", "Indicador de beats (el activo se alarga).",
     [{"e": "progreso", "i": 1, "n": 4}], {"caja": (340, 0, 600)}),
    ("UI", "icono", "Íconos de línea: persona, grupo, pantalla, doc, chat, check, globo, auriculares, toque.",
     [{"e": "icono", "nombre": n, "x": 330 + i * 80, "y": 360, "s": 50, "tono": "ink"} for i, n in enumerate(["persona", "grupo", "pantalla", "doc", "chat", "check", "globo", "auriculares", "toque"])], {}),
    ("UI", "punto", "Punto con halo (marcador de gráfica, paleta).",
     [{"e": "punto", "x": 560, "y": 360, "r": 22}, {"e": "punto", "x": 640, "y": 360, "r": 22, "glow": True}, {"e": "punto", "x": 720, "y": 360, "r": 22, "fill": "#ffffff", "glow": True}], {}),
    ("Gráficas", "curva", "Curva suave por puntos con área degradada, neón opcional y punto final brillante.",
     [{"e": "curva", "puntos": [(300, 520), (440, 470), (560, 490), (700, 400), (840, 330), (980, 240)], "neon": True, "final": True, "sw": 9, "base": 600}], {}),
    ("Gráficas", "barras", "Barras: resalta = índice de acento; degradado=True para el degradado vertical.",
     [{"e": "barras", "x": 420, "y": 520, "valores": [12, 30, 58, 120], "ancho": 60, "alto": 260, "resalta": 3}], {}),
    ("Gráficas", "arco", "Anillo con arco de progreso (tiempo, avance, garantía).",
     [{"e": "arco", "x": 640, "y": 360, "r": 120, "frac": 0.75, "t": "24/5", "s": 70}], {}),
    ("Gráficas", "onda", "Onda senoidal (ritmo, señal, continuidad), con neón opcional.",
     [{"e": "onda", "x": 300, "y": 360, "w": 680, "amp": 70, "ciclos": 2.5, "neon": True}], {}),
    ("Formas", "anillos", "Anillos concéntricos: fino (línea) o suave (relleno casi invisible).",
     [{"e": "anillos", "x": 640, "y": 360, "radios": [90, 170, 250], "estilo": "fino"}], {}),
    ("Formas", "orbita", "Órbita fina con destello alrededor de un texto.",
     [{"e": "texto", "x": 640, "y": 372, "s": 64, "a": "middle", "t": "frase", "tono": "ink"}, {"e": "orbita", "x": 640, "y": 350, "rx": 250, "ry": 90}], {}),
    ("Formas", "destello", "Destello de 4 puntas.",
     [{"e": "destello", "x": 560, "y": 360, "s": 30}, {"e": "destello", "x": 640, "y": 360, "s": 46}, {"e": "destello", "x": 740, "y": 360, "s": 24}], {}),
    ("Formas", "linea", "Línea fina (guía, regla, conexión).",
     [{"e": "linea", "x1": 360, "y1": 360, "x2": 920, "y2": 360, "sw": 3, "op": 0.6}], {}),
    ("Formas", "flecha", "Flecha con esquinas redondeadas que se dibuja por la pantalla.",
     [{"e": "flecha", "puntos": [(320, 520), (320, 300), (900, 300)], "sw": 7}], {}),
    ("Abstractos", "particulas · caos", "Puntos dispersos (desorden, problema, ruido).",
     [{"e": "particulas", "x": 360, "y": 220, "w": 560, "h": 280, "n": 60, "semilla": 4}], {}),
    ("Abstractos", "particulas · orden", "Los mismos puntos alineados en cuadrícula (solución, orden, sistema).",
     [{"e": "particulas", "x": 360, "y": 220, "w": 560, "h": 280, "n": 60, "orden": True}], {}),
    ("Abstractos", "infinito", "Lazo infinito con un punto que lo recorre (siempre, vitalicio, ilimitado).",
     [{"e": "infinito", "x": 640, "y": 360, "w": 420}], {}),
    ("Abstractos", "desorden · caos", "Formas rotadas y dispersas (papeleo, trámites, problema).",
     [{"e": "desorden", "x": 380, "y": 220, "w": 520, "h": 260, "n": 12, "semilla": 6}], {}),
    ("Abstractos", "desorden · orden", "Las mismas formas alineadas (todo en un solo lugar).",
     [{"e": "desorden", "x": 380, "y": 220, "w": 520, "h": 260, "n": 12, "orden": True}], {}),
    ("Abstractos", "escalera", "Escalones ascendentes (avance, nivel, mejora, capacitación).",
     [{"e": "escalera", "x": 400, "y": 520, "w": 480, "h": 280, "n": 5}], {}),
]


def main(salida=SALIDA):
    secciones, cats = {}, []
    for cat, nombre, desc, els, opc in DEMOS:
        x, y, w = opc.get("caja", (240, 135, 800))
        h = int(w * 9 / 16)
        vistas = []
        for tm, etiqueta in TEMAS:
            spec = {"tema": tm, "elementos": els}
            if "fondo" in opc:
                spec["fondo"] = opc["fondo"]
            sp, _ = elementos.escena(spec)
            svg = boceto_svg(sp).replace('viewBox="0 0 1280 720"', f'viewBox="{x} {y} {w} {h}"', 1).replace("<svg ", "<svg style='width:100%;display:block;border-radius:8px' ", 1)
            vistas.append(f"<div><div class='et'>{etiqueta}</div>{svg}</div>")
        codigo = json.dumps(els if len(els) > 1 else els[0], ensure_ascii=False)
        if cat not in secciones:
            secciones[cat] = []
            cats.append(cat)
        secciones[cat].append(f"<section><h3>{nombre}</h3><p>{desc}</p><div class='tres'>{''.join(vistas)}</div><pre>{codigo.replace('<', '&lt;')}</pre></section>")
    nav = " · ".join(f'<a href="#{c}">{c}</a>' for c in cats)
    cuerpo = "".join(f'<h2 id="{c}">{c}</h2>' + "".join(secciones[c]) for c in cats)
    html = ('<!doctype html><meta charset="utf-8"><title>Lienzo de elementos UI</title><style>body{font:15px/1.4 Manrope,system-ui,sans-serif;background:#12151b;color:#eceff6;margin:0;padding:24px}'
            'a{color:#8fb4ff}h1,h2{margin:0 0 8px}h2{margin-top:34px;border-bottom:1px solid #2c313d;padding-bottom:6px}section{background:#1b2029;border:1px solid #2c313d;border-radius:14px;padding:14px;margin:14px 0}'
            'h3{margin:0;color:#8fb4ff}p{color:#9aa3b5;font-size:13px;margin:4px 0 10px}.tres{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.et{font-size:12px;color:#9aa3b5;margin-bottom:4px}'
            'pre{background:#0d1015;border-radius:8px;padding:8px;font-size:12px;color:#b9c3d6;overflow:auto;margin:10px 0 0;white-space:pre-wrap}@media(max-width:1000px){.tres{grid-template-columns:1fr}}</style>'
            f'<h1>Lienzo de elementos UI</h1><p>{len(DEMOS)} elementos del vocabulario de motion, cada uno en los tres colores de significado, con el código para usarlo en <code>escena({{...}})</code>.</p><p>{nav}</p>{cuerpo}')
    Path(salida).write_text(html, encoding="utf-8")
    print("lienzo:", salida, "|", len(DEMOS), "elementos")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else SALIDA)
