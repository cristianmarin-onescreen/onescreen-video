"""Escenas de motion graphic de las piezas INTA (v2, 27-oct-2026). Estilo Flota de IA / Rental v3: lettering gigante que sube por palabra (máscara), cámara 3D (perspective, z, giros
suaves + empuje continuo), diagramas que se DIBUJAN (trazo progresivo, nodos con pop, paquetes de luz, sello), fondo de color por escena y diagramación distinta en cada una.
Cris (27-oct): "muy lentos, no se parecen a Flota de IA ni a Apple, los planos como transición se sienten raro" -> entradas de 0,5-0,7 s, escenas encadenadas con barrido de color
(sin planos entre ellas), texto de 2-3 palabras. gfx(kind, uid, t0, t1, cue, fmt, W, H, SAFE) -> (html, [js]); cue(i, frac) = tiempo de la i-ésima palabra ancla (o t0 + frac·(t1-t0))."""

ACC, INK, PUR, GRY, PAPER = "#3976ff", "#1a1a1a", "#7d00ba", "#c9ced8", "#fafafa"
STROKE = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'


def P(d, col, w=7, cls="d"):
    return f'<path class="{cls}" data-draw pathLength="1" d="{d}" {STROKE} stroke="{col}" stroke-width="{w}"/>'


def person(cx, cy, col, cls, w=7):
    return (f'<g class="{cls}"><circle data-draw pathLength="1" class="d" cx="{cx}" cy="{cy - 38}" r="26" {STROKE} stroke="{col}" stroke-width="{w}"/>'
            f'{P(f"M{cx - 52} {cy + 52} Q{cx - 52} {cy + 4} {cx} {cy + 4} Q{cx + 52} {cy + 4} {cx + 52} {cy + 52}", col, w)}</g>')


def doc(x, y, w, h, col, lines, lw=7, cls="doc", gray=False):
    out = f'<g class="{cls}">' + P(f"M{x} {y + 24} Q{x} {y} {x + 24} {y} L{x + w - 46} {y} L{x + w} {y + 46} L{x + w} {y + h - 24} Q{x + w} {y + h} {x + w - 24} {y + h} L{x + 24} {y + h} Q{x} {y + h} {x} {y + h - 24} Z", col, lw, "d dc")
    out += P(f"M{x + w - 46} {y} L{x + w - 46} {y + 46} L{x + w} {y + 46}", col, lw, "d dc")
    for ly, lx1 in lines:
        out += P(f"M{x + 36} {ly} L{lx1} {ly}", GRY if gray else col, lw - 1, "d dl")
    return out + "</g>"


def screen(x, y, w, h, col, lw=7):
    return (P(f"M{x} {y + 22} Q{x} {y} {x + 22} {y} L{x + w - 22} {y} Q{x + w} {y} {x + w} {y + 22} L{x + w} {y + h - 22} Q{x + w} {y + h} {x + w - 22} {y + h} L{x + 22} {y + h} Q{x} {y + h} {x} {y + h - 22} Z", col, lw, "d sc")
            + P(f"M{x + w / 2 - 70} {y + h + 56} L{x + w / 2 + 70} {y + h + 56}", col, lw, "d sc") + P(f"M{x + w / 2} {y + h} L{x + w / 2} {y + h + 56}", col, lw, "d sc"))


def gfx(kind, uid, t0, t1, cue, fmt, W, H, SAFE):
    V = fmt != "16"
    bg, fg = {"acta": (PAPER, INK), "transcribe": (ACC, "#fff"), "idiomas": (PAPER, INK), "resumen": (INK, "#fff"), "participan": (PAPER, INK)}[kind]
    ac = "#fff" if bg == ACC else ACC          # color de acento sobre el fondo de la escena
    sz = {"16": 125, "9": 92, "45": 92}[fmt]
    L, R, T = SAFE["l"], SAFE["r"], SAFE["t"]
    CW = W - L - R
    d = t1 - t0
    TT = lambda i, fr: cue(i, t0 + fr * d)
    js, J = [], None
    J = js.append
    sel = lambda c: f"#{uid} .{c}"
    draw = lambda tgt, at, dur=0.55, st=0.06: J(f'tl.fromTo("{tgt}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut",stagger:{st}}},{at:.4f});')
    pop = lambda tgt, at, st=0.0, fr=0.5: J(f'tl.fromTo("{tgt}",{{opacity:0,scale:{fr}}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.7)",stagger:{st}}},{at:.4f});')
    show = lambda tgt, at: J(f'tl.fromTo("{tgt}",{{opacity:0}},{{opacity:1,duration:0.01,ease:"none"}},{at:.4f});')

    def hl(lines, x, y, size, align="left", w=None):
        """lettering gigante: cada palabra sube desde detrás de su línea (máscara); líneas = [(texto, 'l'|'b', color|None)]"""
        out = ""
        for text, k, col in lines:
            fs = min(size, (w or CW) / ((0.56 if k == "b" else 0.5) * max(len(text), 1)))
            ws = "".join(f'<span class="lw {k}" style="display:inline-block">{wd}</span> ' for wd in text.split(" "))
            out += f'<div class="ln" style="font-size:{fs:.0f}px;font-weight:{700 if k == "b" else 300};color:{col or fg}">{ws}</div>'
        wcss = f"width:{w}px;" if w else ""
        return f'<div class="big" style="left:{x}px;top:{y}px;{wcss}text-align:{align}">{out}</div>'

    def box(x, y, w, vbw, vbh, inner, cls=""):
        return f'<svg class="gfxs {cls}" viewBox="0 0 {vbw} {vbh}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;overflow:visible">{inner}</svg>'

    body = ""
    hs = []   # tiempos de entrada del lettering
    if kind == "acta":                        # Nadie arma el acta: la hoja se escribe y se tacha
        dw = 290 if not V else min(CW * 0.5, 330)
        dx = (W - R - dw - 120) if not V else (W - dw) / 2
        dy = 300 if not V else T + sz * 2.6
        body += hl([("Nadie arma", "l", None), ("el acta.", "b", ac)], L, T, sz)
        body += box(dx, dy, dw, 340, 440, doc(0, 0, 340, 440, fg, [(120, 300), (172, 250), (224, 300), (276, 210), (328, 270)]) + P("M36 60 L304 380 M304 60 L36 380", PUR, 15, "d xx"))
        draw(sel("dc"), t0 + 0.30, 0.5, 0.0); draw(sel("dl"), t0 + 0.55, 0.4, 0.1)
        draw(sel("xx"), TT(0, 0.5), 0.35, 0.1)
        J(f'tl.to("{sel("doc")}",{{opacity:0.3,duration:0.3,ease:"power2.out"}},{TT(0, 0.5) + 0.25:.4f});')
        cam = (-260, 7, -8)
    elif kind == "transcribe":                # la voz se vuelve texto en la pantalla (fondo azul, título abajo)
        sw = CW if V else 600
        sx = L if V else W - R - sw - 60
        sy = (T + sz * 2.4) if V else 300
        body += box(sx, sy, sw, 780, 520, screen(0, 0, 780, 440, "#fff")
                    + "".join(f'<rect class="bar" x="{70 + i * 46}" y="{220 - h}" width="20" height="{2 * h}" rx="10" fill="#fff"/>' for i, h in enumerate([34, 70, 112, 60, 96, 40, 76]))
                    + "".join(P(f"M420 {ly} L{x2} {ly}", "#fff", 7, "d tl") for ly, x2 in [(110, 720), (170, 660), (230, 720), (290, 610), (350, 690)]))
        body += hl([("Se transcribe", "b", None), ("sola.", "l", None)], L, T, sz)
        draw(sel("sc"), t0 + 0.30, 0.5, 0.08)
        J(f'tl.fromTo("{sel("bar")}",{{opacity:0,scaleY:0.2,transformOrigin:"50% 50%"}},{{opacity:1,scaleY:1,duration:0.35,ease:"power3.out",stagger:0.05}},{t0 + 0.7:.4f});')
        for i in range(7):
            J(f'tl.to("#{uid} .bar:nth-of-type({i + 1})",{{scaleY:{0.4 + 0.18 * (i % 3)},duration:0.28,ease:"sine.inOut",yoyo:true,repeat:{max(2, int(d / 0.56))},transformOrigin:"50% 50%"}},{t0 + 1.1 + 0.04 * i:.4f});')
        draw(sel("tl"), t0 + 0.9, 0.45, 0.22)
        cam = (-300, 6, 8)
    elif kind == "idiomas":                   # conteo +20 gigante y globo con nodos y paquetes de luz
        gw = CW * 0.55 if V else 440
        gx = (W - gw) / 2 if V else W - R - gw - 80
        gy = (H - SAFE["b"] - gw - 30) if V else 300
        body += hl([("+20", "b", ACC)], L, T - 10, sz * 1.9 if not V else sz * 1.6)
        body += hl([("idiomas", "b", None)], L, T + (sz * 1.85 if not V else sz * 1.55), sz * 0.85)
        nodes = [(70, 110), (390, 90), (430, 250), (330, 410), (60, 380), (10, 240)]
        body += box(gx, gy, gw, 440, 440,
                    f'<circle data-draw pathLength="1" class="d gb" cx="220" cy="220" r="170" {STROKE} stroke="{INK}" stroke-width="7"/>'
                    + P("M50 220 L390 220", INK, 6, "d gb") + P("M220 50 Q70 220 220 390 Q370 220 220 50", INK, 6, "d gb") + P("M75 140 Q220 175 365 140 M75 300 Q220 265 365 300", INK, 6, "d gb")
                    + "".join(f'<g class="nd"><circle cx="{x}" cy="{y}" r="26" fill="{ACC}"/><path d="M{x - 11} {y - 5} h22 M{x - 11} {y + 6} h14" stroke="#fff" stroke-width="5" stroke-linecap="round" fill="none"/></g>' for x, y in nodes)
                    + "".join(f'<circle class="pk" cx="220" cy="220" r="9" fill="{PUR}" opacity="0"/>' for _ in nodes))
        draw(sel("gb"), t0 + 0.30, 0.5, 0.08)
        pop(sel("nd"), TT(0, 0.3), 0.07)
        for i, (x, y) in enumerate(nodes):
            at = TT(0, 0.3) + 0.45 + 0.09 * i
            J(f'tl.fromTo("#{uid} .pk:nth-of-type({i + 1})",{{opacity:1,attr:{{cx:220,cy:220}}}},{{attr:{{cx:{x},cy:{y}}},duration:0.45,ease:"power2.out"}},{at:.4f});')
            J(f'tl.to("#{uid} .pk:nth-of-type({i + 1})",{{opacity:0,duration:0.1}},{at + 0.45:.4f});')
        cam = (-240, 8, 6)
    elif kind == "resumen":                   # La IA resume: el documento largo se condensa en tres líneas (destello) y sale en Word y PDF
        body += hl([("La IA", "l", None), ("resume.", "b", "#fff")], L, T, sz, "left")
        yy = (T + sz * 2.15) if not V else T + sz * 2.4
        scw = min(CW, 760)
        body += box((W - scw) / 2 + (0 if V else 120), yy, scw, 1000, 440,
                    doc(40, 20, 300, 400, "#fff", [(130, 290), (182, 240), (234, 290), (286, 250), (338, 280)], cls="doc big0")
                    + P("M395 230 L560 230 M520 190 L560 230 L520 270", ACC, 9, "d ar")
                    + '<path class="spk" d="M478 80 L492 128 L540 142 L492 156 L478 204 L464 156 L416 142 L464 128 Z" fill="#fff" opacity="0"/>'
                    + doc(620, 80, 230, 300, ACC, [(190, 800), (250, 740), (310, 800)], cls="doc sm")
                    + f'<g class="bg1"><rect x="880" y="280" width="100" height="62" rx="16" fill="{ACC}"/><text x="930" y="324" text-anchor="middle" font-family="Rubik" font-weight="700" font-size="32" fill="#fff">W</text></g>'
                    + f'<g class="bg1"><rect x="880" y="356" width="100" height="62" rx="16" fill="{PUR}"/><text x="930" y="400" text-anchor="middle" font-family="Rubik" font-weight="700" font-size="28" fill="#fff">PDF</text></g>')
        draw(sel("big0 .dc"), t0 + 0.2, 0.4, 0.0); draw(sel("big0 .dl"), t0 + 0.4, 0.35, 0.07)
        draw(sel("ar"), TT(0, 0.25), 0.3, 0.0)
        J(f'tl.fromTo("{sel("spk")}",{{opacity:0,scale:0.2,rotation:-90,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(1.7)"}},{TT(0, 0.25) + 0.1:.4f});')
        draw(sel("sm .dc"), TT(0, 0.25) + 0.25, 0.4, 0.0)
        J(f'tl.to("{sel("big0 .dl")}",{{x:330,y:-10,scaleX:0.5,opacity:0,duration:0.5,ease:"power3.in",stagger:0.05,transformOrigin:"0% 50%"}},{TT(0, 0.25) + 0.3:.4f});')
        draw(sel("sm .dl"), TT(0, 0.25) + 0.7, 0.3, 0.12)
        pop(sel("bg1"), TT(1, 0.6), 0.12)
        cam = (-280, 6, -7)
    else:                                     # participan: cinco personas se encienden
        pw = min(CW, 700)
        body += hl([("Todos", "l", None), ("participan.", "b", ACC)], L, T, sz)
        xs = [150, 330, 510, 690, 870]
        body += box((W - pw) / 2, T + sz * 2.4 + 60 if not V else T + sz * 2.4, pw, 1020, 300,
                    "".join(person(x + 20, 120, GRY if i != 2 else INK, f"pn p{i}") for i, x in enumerate(xs)) + P("M60 270 L960 270", INK, 8, "d base")
                    + "".join(f'<circle class="ac" cx="{x + 20}" cy="62" r="13" fill="{ACC}" opacity="0"/>' for x in xs))
        draw(sel("pn .d"), t0 + 0.30, 0.45, 0.04); draw(sel("base"), t0 + 0.4, 0.5, 0.0)
        for i in range(5):
            J(f'tl.to("#{uid} .p{i} .d",{{stroke:"{ACC}",duration:0.25,ease:"power2.out"}},{TT(0, 0.3) + 0.16 * i:.4f});')
        J(f'tl.fromTo("{sel("ac")}",{{opacity:0,scale:0.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.7)",stagger:0.16}},{TT(0, 0.3):.4f});')
        cam = (-240, 7, 7)
    z, rx, ry = cam
    html = (f'<div id="{uid}" class="clip gscene w3" data-start="{t0:.4f}" data-duration="{d:.4f}" data-track-index="3" style="background:{bg};color:{fg}">'
            f'<div class="wd"><div class="wd2">{body}</div></div></div>')
    # barrido de color, cámara 3D (entra desde atrás con giro suave) y empuje continuo
    pre = [f'tl.fromTo("#{uid}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"power3.inOut"}},{t0:.4f});',
           f'tl.fromTo("#{uid} .wd",{{z:{int(z * 2)},rotationX:{rx * 1.7:.0f},rotationY:{ry * 1.7:.0f}}},{{z:0,rotationX:0,rotationY:0,duration:1.15,ease:"power3.out"}},{t0 + 0.05:.4f});',
           f'tl.fromTo("#{uid} .wd2",{{z:0,rotationY:0}},{{z:120,rotationY:{-ry * 0.25:.1f},duration:{max(d - 0.9, 0.6):.3f},ease:"none"}},{t0 + 0.9:.4f});',
           f'tl.fromTo("#{uid} .lw",{{opacity:0,scale:0.55,transformOrigin:"50% 60%"}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.7)",stagger:0.08}},{t0 + 0.12:.4f});']
    if bg == PAPER:
        pre = pre[1:]          # Cris 27-oct: nada de barridos sobre blanco, corte directo
    return html, pre + js
