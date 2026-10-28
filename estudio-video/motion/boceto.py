"""Renderizador de pantallazos estáticos de motion graphics (1280x720) a partir de un spec corto. Lo usan las plantillas y storyboard.py.

b = {"fondo": "#fff" | {"grad": ["#2f6bea", "#0a1b55"], "ang": 135,
                        "luces": [[x, y, r, "#8fb4ff", 0.3], ...]   # «aurora»: manchas de luz suaves (en el motion SE MUEVEN: el fondo jamás es estático)
                        "tex": "puntos"|"rejilla"|None, "texc": color, "texop": 0-1, "grano": 0-1 (ruido fino sobre el degradado)},
     "formas": [ {"k": "rect", "x":, "y":, "w":, "h":, "fill":, "r":, "st":, "sw":, "op": relleno, "sop": trazo,
                  "glow": color (la tarjeta «brilla»: halo difuso detrás), "brillo": true (borde con luz que se apaga en diagonal)},
                 {"k": "circ", "x":, "y":, "r":, "fill":, "st":, "sw":, "op":, "glow": color},
                 {"k": "elip", "x":, "y":, "rx":, "ry":, "rot":, "st":, "sw":, "sop":},          # órbita fina alrededor de un texto
                 {"k": "estrella", "x":, "y":, "s":, "fill":},                                     # destello de 4 puntas
                 {"k": "txt", "x":, "y":, "s":, "w":, "fill":, "grad": [c1, c2], "gv": true (degradado vertical que se desvanece),
                  "st": color (solo contorno, para el número «fantasma»), "t":, "a": start|middle|end, "ls":, "op":},
                 {"k": "linea", ...}, {"k": "poly", "pts":, "fill":}, {"k": "path", "d":, "fill": trazo, "rel": relleno, "sw":, "op":},
                 {"k": "flecha", "x1":, "y1":, "x2":, "y2":, "col":, "nota":} ]}"""
import itertools
import math

_CNT = itertools.count(1)   # ids únicos por pantallazo: varios SVG conviven en una misma página


def _e(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _op(f, k="op", nombre="opacity"):
    return f' {nombre}="{f[k]}"' if f.get(k) is not None else ""


def boceto_svg(b, anim=False):
    az, ne, ac = "#3976ff", "#1a1a1a", "#7d00ba"
    defs, cuerpo, n = [], [], [0]
    u = f"s{next(_CNT)}"
    usa_glow = [False]

    def grad(cols, vertical=False, fade=False):
        n[0] += 1
        gid = f"{u}g{n[0]}"
        x2, y2 = (0, 1) if vertical else (1, 0)
        if fade:
            stops = f'<stop offset="0" stop-color="{cols[0]}"/><stop offset="1" stop-color="{cols[0]}" stop-opacity="0.35"/>'
        else:
            stops = "".join(f'<stop offset="{i / max(len(cols) - 1, 1)}" stop-color="{c}"/>' for i, c in enumerate(cols))
        defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{stops}</linearGradient>')
        return gid

    def _fill(f):
        if f.get("fillgrad"):
            return f"url(#{grad(f['fillgrad'], vertical=bool(f.get('fgv')))})"
        return f.get("fill", "none" if f.get("st") else az)

    def glow_def():
        if not usa_glow[0]:
            defs.append(f'<filter id="{u}gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>')
            usa_glow[0] = True
        return f"{u}gl"

    fondo = b.get("fondo", "#ffffff")
    if isinstance(fondo, dict):
        n[0] += 1
        gid = f"{u}bg{n[0]}"
        cols = fondo["grad"]
        stops = "".join(f'<stop offset="{i / max(len(cols) - 1, 1)}" stop-color="{c}"/>' for i, c in enumerate(cols))
        ang = fondo.get("ang", 135)
        dx, dy = math.cos(math.radians(ang - 90)), math.sin(math.radians(ang - 90))
        defs.append(f'<linearGradient id="{gid}" x1="{0.5 - dx / 2:.3f}" y1="{0.5 - dy / 2:.3f}" x2="{0.5 + dx / 2:.3f}" y2="{0.5 + dy / 2:.3f}">{stops}</linearGradient>')
        cuerpo.append(f'<rect width="1280" height="720" fill="url(#{gid})"/>')
        luces = list(fondo.get("luces", []))
        if fondo.get("luz"):
            luces.append(fondo["luz"])
        for i, (x, y, r, c, op) in enumerate(luces):
            defs.append(f'<radialGradient id="{u}lz{i}"><stop offset="0" stop-color="{c}" stop-opacity="{op}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
            cuerpo.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{u}lz{i})"/>')
        tex = fondo.get("tex")
        if tex == "puntos":
            defs.append(f'<pattern id="{u}tx" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{fondo.get("texc", "#fff")}" fill-opacity="{fondo.get("texop", 0.09)}"/></pattern>')
            cuerpo.append(f'<rect width="1280" height="720" fill="url(#{u}tx)"/>')
        elif tex == "rejilla":
            defs.append(f'<pattern id="{u}tx" width="88" height="88" patternUnits="userSpaceOnUse"><path d="M88 0H0V88" fill="none" stroke="{fondo.get("texc", "#fff")}" stroke-opacity="{fondo.get("texop", 0.04)}" stroke-width="1"/></pattern>')
            cuerpo.append(f'<rect width="1280" height="720" fill="url(#{u}tx)"/>')
        if fondo.get("grano"):
            defs.append(f'<filter id="{u}gr" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/></filter>')
            cuerpo.append(f'<rect width="1280" height="720" filter="url(#{u}gr)" opacity="{fondo["grano"]}" style="mix-blend-mode:overlay"/>')
    else:
        cuerpo.append(f'<rect width="1280" height="720" fill="{fondo}"/>')
    for f in b.get("formas", []):
        k = f.get("k")
        _n0 = len(cuerpo)
        if k in ("rect", "circ") and f.get("glow"):     # el contenedor «brilla»: halo difuso del color de acento detrás
            gf = glow_def()
            if k == "rect":
                cuerpo.append(f'<rect x="{f["x"]}" y="{f["y"]}" width="{f["w"]}" height="{f["h"]}" rx="{f.get("r", 0)}" fill="{f["glow"]}" opacity="0.38" filter="url(#{gf})"/>')
            else:
                cuerpo.append(f'<circle cx="{f["x"]}" cy="{f["y"]}" r="{f["r"]}" fill="{f["glow"]}" opacity="0.45" filter="url(#{gf})"/>')
        if k == "rect":
            st = f' stroke="{f["st"]}" stroke-width="{f.get("sw", 8)}"' + _op(f, "sop", "stroke-opacity") if f.get("st") else ""
            cuerpo.append(f'<rect x="{f["x"]}" y="{f["y"]}" width="{f["w"]}" height="{f["h"]}" rx="{f.get("r", 0)}" fill="{_fill(f)}"{_op(f, "op", "fill-opacity")}{st}{(' transform="rotate(' + str(f['rot']) + ' ' + str(f['x'] + f['w'] / 2) + ' ' + str(f['y'] + f['h'] / 2) + ')"') if f.get("rot") else ""}/>')
            if f.get("stgrad"):
                gg = grad(f["stgrad"])
                cuerpo.append(f'<rect x="{f["x"]}" y="{f["y"]}" width="{f["w"]}" height="{f["h"]}" rx="{f.get("r", 0)}" fill="none" stroke="url(#{gg})" stroke-width="{f.get("sw", 4)}"/>')
            if f.get("brillo"):     # borde con luz: blanco arriba-izquierda que se apaga hacia abajo-derecha
                n[0] += 1
                bid = f"{u}b{n[0]}"
                defs.append(f'<linearGradient id="{bid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.85"/><stop offset="0.45" stop-color="#fff" stop-opacity="0.12"/><stop offset="1" stop-color="#fff" stop-opacity="0.35"/></linearGradient>')
                cuerpo.append(f'<rect x="{f["x"]}" y="{f["y"]}" width="{f["w"]}" height="{f["h"]}" rx="{f.get("r", 0)}" fill="none" stroke="url(#{bid})" stroke-width="2.5"/>')
        elif k == "circ":
            st = f' stroke="{f["st"]}" stroke-width="{f.get("sw", 8)}"' + _op(f, "sop", "stroke-opacity") if f.get("st") else ""
            cuerpo.append(f'<circle cx="{f["x"]}" cy="{f["y"]}" r="{f["r"]}" fill="{f.get("fill", "none" if f.get("st") else az)}"{_op(f, "op", "fill-opacity")}{st}/>')
        elif k == "elip":
            cuerpo.append(f'<ellipse cx="{f["x"]}" cy="{f["y"]}" rx="{f["rx"]}" ry="{f["ry"]}" transform="rotate({f.get("rot", 0)} {f["x"]} {f["y"]})" fill="none" stroke="{f.get("st", "#fff")}" stroke-width="{f.get("sw", 2)}"{_op(f, "sop", "stroke-opacity")}/>')
        elif k == "estrella":
            x, y, s = f["x"], f["y"], f.get("s", 40)
            cuerpo.append(f'<path d="M{x} {y - s} Q{x + s * .12} {y - s * .12} {x + s} {y} Q{x + s * .12} {y + s * .12} {x} {y + s} Q{x - s * .12} {y + s * .12} {x - s} {y} Q{x - s * .12} {y - s * .12} {x} {y - s} Z" fill="{f.get("fill", "#fff")}"/>')
        elif k == "txt":
            if f.get("st"):
                fill, trazo = "none", f' stroke="{f["st"]}" stroke-width="{f.get("sw", 2)}"'
            else:
                fill = f'url(#{grad(f["grad"])})' if f.get("grad") else (f'url(#{grad([f.get("fill", ne)], True, True)})' if f.get("gv") else f.get("fill", ne))
                trazo = ""
            cuerpo.append(f'<text x="{f["x"]}" y="{f["y"]}" font-size="{f.get("s", 56)}" font-weight="{f.get("w", 700)}" fill="{fill}"{trazo} text-anchor="{f.get("a", "start")}" letter-spacing="{f.get("ls", 0)}"{_op(f)}>{_e(f["t"])}</text>')
        elif k == "poly":
            cuerpo.append(f'<polygon points="{f["pts"]}" fill="{f.get("fill", az)}"{_op(f, "op", "fill-opacity")}/>')
        elif k == "path":
            if f.get("relgrad"):
                n[0] += 1
                rid = f"{u}a{n[0]}"
                defs.append(f'<linearGradient id="{rid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{f["relgrad"]}" stop-opacity="0.6"/><stop offset="1" stop-color="{f["relgrad"]}" stop-opacity="0"/></linearGradient>')
                f = dict(f, rel=f"url(#{rid})")
            cuerpo.append(f'<path d="{f["d"]}" fill="{f.get("rel", "none")}" stroke="{f.get("fill", ne)}" stroke-width="{f.get("sw", 8)}" stroke-linecap="round" stroke-linejoin="round"{_op(f, "op", "stroke-opacity")}/>')
        elif k == "linea":
            cuerpo.append(f'<line x1="{f["x1"]}" y1="{f["y1"]}" x2="{f["x2"]}" y2="{f["y2"]}" stroke="{f.get("fill", az)}" stroke-width="{f.get("sw", 8)}" stroke-linecap="round"{_op(f, "op", "stroke-opacity")}/>')
        elif k == "flecha":
            cuerpo.append(f'<line x1="{f["x1"]}" y1="{f["y1"]}" x2="{f["x2"]}" y2="{f["y2"]}" stroke="{f.get("col", ac)}" stroke-width="6" stroke-dasharray="14 12" marker-end="url(#{u}ah)"/>')
            if f.get("nota"):
                cuerpo.append(f'<text x="{(f["x1"] + f["x2"]) / 2 + 16}" y="{(f["y1"] + f["y2"]) / 2 - 10}" font-size="30" font-weight="600" fill="{f.get("col", ac)}">{_e(f["nota"])}</text>')
        if anim and len(cuerpo) > _n0:      # animación (build): cada forma es un grupo `.f` que entra escalonado
            cuerpo[_n0:] = ['<g class="f">' + "".join(cuerpo[_n0:]) + '</g>']
    defs.append(f'<marker id="{u}ah" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="context-stroke"/></marker>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Rubik,Manrope,system-ui,sans-serif"><defs>' + "".join(defs) + "</defs>" + "".join(cuerpo) + "</svg>")


def _caja_txt(f):
    ancho = len(str(f["t"])) * f.get("s", 56) * (0.54 if f.get("w", 700) >= 600 else 0.5) + abs(f.get("ls", 0)) * -len(str(f["t"])) * 0.4
    ancho = max(ancho, 8)
    x = f["x"] - (ancho / 2 if f.get("a") == "middle" else (ancho if f.get("a") == "end" else 0))
    s = f.get("s", 56)
    return x, f["y"] - s * 0.8, x + ancho, f["y"] + s * 0.2


def revisar(b):
    """Revisor de armado: avisa si un texto se sale del lienzo o se pisa con otro texto (cajas estimadas). Devuelve lista de avisos (vacía = sin problemas)."""
    av, cajas = [], []
    for f in b.get("formas", []):
        if f.get("k") != "txt" or f.get("st") or (f.get("op") is not None and f["op"] < 0.4):
            continue
        x0, y0, x1, y1 = _caja_txt(f)
        if x0 < 10 or x1 > 1270 or y0 < 0 or y1 > 720:
            av.append(f"texto fuera del lienzo: «{str(f['t'])[:28]}» ({int(x0)}-{int(x1)}, {int(y0)}-{int(y1)})")
        for g, (a0, b0, a1, b1) in cajas:
            ox, oy = min(x1, a1) - max(x0, a0), min(y1, b1) - max(y0, b0)
            if ox > 6 and oy > 0.35 * min(y1 - y0, b1 - b0):
                av.append(f"se pisan: «{str(f['t'])[:22]}» con «{str(g['t'])[:22]}»")
        cajas.append((f, (x0, y0, x1, y1)))
    for f in b.get("formas", []):     # PROHIBIDO (Cris, 28-oct): píldoras, o sea cualquier rectángulo con las esquinas redondeadas como cápsula
        if f.get("k") == "rect" and min(f["w"], f["h"]) >= 20 and f.get("r", 0) >= 0.4 * min(f["w"], f["h"]):
            av.append(f"píldora prohibida en ({int(f['x'])}, {int(f['y'])}) {int(f['w'])}x{int(f['h'])} r={f['r']}: usar esquinas de 8-16 px")
    return av
