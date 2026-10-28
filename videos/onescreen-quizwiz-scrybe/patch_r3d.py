"""build_rental3: motion graphics como diagramas que REPRESENTAN cosas (no íconos animados), sobre fondos de color/blanco,
y de vuelta las tarjetas de ventajas (Pagas por lo que usas / Siempre actualizada / Soporte prioritario / Nos encargamos),
cada una con un mini-diagrama que se mueve. F pasa a plano con texto + calendario de pagos; D, E y las tarjetas van sobre fondo."""
from pathlib import Path
f = Path(__file__).parent / "build_rental3.py"
s = f.read_text(encoding="utf-8")


def cut(a, b, new=""):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + s[j:]


# ── beats: D y E se mueven al bloque de escenas; F vuelve al plano; H–L se reemplazan por la escena de tarjetas
cut('# D · "hay dos caminos"', '# F · "Por una cuota accesible, mensualmente"')
cut('bgs(T["por"], T["llenar"], "#fafafa")', '# G · "puedes llenar',
    '''vid("m1", T["por"], T["llenar"], 1.0)
f1 = tx(T["cuota"] - 0.1, T["llenar"], [('<span class="l">Una cuota</span>', S2 * 1.4), ('<span class="b">mensual</span>', S1)], "bl")
rise(f"#{f1} .rw", T["cuota"] - 0.1, 0.7, 0.12); gone(f"#{f1} .rw", T["llenar"] - 0.25)
''')
cut('# H · "Hay muchas ventajas', '# M · "¿Quieres adquirir tu pantalla?"',
    'tJ0, tK0, tL0, tM0 = T["siempre"], T["soporte"], T["si"], T["quieres"]\n')

# ── gráficos viejos de D, E, F, I, J, K, L (los de A, B, G y N se quedan)
cut('# D · "dos caminos": bifurcación', '# G · "llenar toda tu institución"')
cut('# I · "pagas por lo que usas": medidor', '# N · "Pregúntanos": globo')
cut('# E · ciclo mensual', '# ── subtítulos:')

NEW = r'''
# ══ escenas de diagrama: cada gráfico REPRESENTA lo que dice la voz (nodos, flujos, paquetes de luz) ══════
STG = {"16": (W - SAFE["r"] - 870, 130, 870, 820), "9": (100, SAFE["t"] + 30 + round(S1 * 2.25), 880, H - SAFE["b"] - (SAFE["t"] + 30 + round(S1 * 2.25))),
       "45": (100, SAFE["t"] + 20 + round(S1 * 2.2), 880, H - SAFE["b"] - (SAFE["t"] + 20 + round(S1 * 2.2)))}[FMT]


def stg(i, t0, t1, inner, col="#fff", sw=14):
    x, y, w, h = STG
    els.append(f'<div id="{i}" class="clip gfx" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;color:{col}">'
               f'<svg viewBox="0 0 800 740" width="100%" height="100%" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{inner}</svg></div>')


def pop(sel, t, d=0.5, frm=0.55, stag=0.0):
    js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:{frm}}},{{opacity:1,scale:1,duration:{d},ease:"back.out(1.7)",stagger:{stag}}},{t:.4f});')


def packet(sel, pts, t, d):
    """paquete de luz que recorre una polilínea de puntos (x,y)"""
    n = len(pts) - 1
    js.append(f'tl.fromTo("{sel}",{{x:{pts[0][0]},y:{pts[0][1]},opacity:0}},{{opacity:1,duration:0.12}},{t:.4f});')
    for k in range(1, len(pts)):
        js.append(f'tl.to("{sel}",{{x:{pts[k][0]},y:{pts[k][1]},duration:{d / n:.3f},ease:"{"power2.in" if k == 1 else "none" if k < n else "power2.out"}"}},{t + (k - 1) * d / n:.4f});')
    js.append(f'tl.to("{sel}",{{opacity:0,duration:0.15}},{t + d:.4f});')


# D · "hay dos caminos": una sola pantalla se bifurca en comprarla / arrendarla (azul)
bgs(T["hay"], T["daas"], ACC)
dd = tx(T["hay"] + 0.2, T["daas"], [('<span class="l">Dos</span> <span class="b">caminos.</span>', S1 * 0.86)], "bl", "text-shadow:none")
rise(f"#{dd} .rw", T["hay"] + 0.25, 0.7, 0.1); gone(f"#{dd} .rw", T["daas"] - 0.25)
gD = nid("g")
tcL, tcR = T["primero0"], T["o2"]
stg(gD, T["hay"] + 0.1, T["daas"],
    pth("M400 174V230C400 320 170 270 170 358", 'class="dl"') + pth("M400 174V230C400 320 630 270 630 358", 'class="dl"')
    + '<g class="nd s0"><circle cx="400" cy="100" r="74" fill="#3976ff"/>' + pth("M358 78H442V122H358Z", 'class="s1"') + pth("M400 122V138M372 138H428", 'class="s1"') + '</g>'
    + '<g transform="translate(170 440)"><g class="nd nL"><circle r="82" fill="#3976ff"/>' + pth("M-40 -40H-22L-6 14H40L52 -22H-18", 'class="cL"')
    + '<circle cx="-2" cy="42" r="8" fill="#fff" stroke="none"/><circle cx="36" cy="42" r="8" fill="#fff" stroke="none"/></g></g>'
    + '<g transform="translate(630 440)"><g class="nd nR"><circle r="82" fill="#3976ff"/>' + pth("M-46 -30H46V46H-46Z", 'class="cR"') + pth("M-46 -4H46", 'class="cR"') + pth("M-20 -48V-22M20 -48V-22", 'class="cR"') + '</g></g>'
    + '<text class="lb lbL" x="170" y="596" text-anchor="middle">Comprarla</text><text class="lb lbR" x="630" y="596" text-anchor="middle">Arrendarla</text>'
    + '<g class="nd pill"><rect x="10" y="626" width="320" height="72" rx="36" fill="#fff" stroke="none"/><g transform="translate(36 641) scale(1.5)" stroke="#3976ff" stroke-width="2.3"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8"/><path d="M8 12.5h5"/></g>'
    + '<text x="96" y="676" style="font:600 38px Rubik;fill:#3976ff;stroke:none;letter-spacing:-0.02em">Contáctanos</text></g>'
    + '<circle id="pkL" r="15" fill="#fff" stroke="none" opacity="0"/><circle id="pkR" r="15" fill="#fff" stroke="none" opacity="0"/>')
pop(f"#{gD} .s0", T["hay"] + 0.3); draw(f"#{gD} .s1", T["hay"] + 0.45, 0.7, 0.1)
draw(f"#{gD} .dl", T["hay"] + 0.9, 0.7, 0.18)
pop(f"#{gD} .nL", tcL + 0.15); draw(f"#{gD} .cL", tcL + 0.3, 0.7, 0.1)
js.append(f'tl.fromTo("#{gD} .lbL",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{tcL + 0.35:.4f});')
packet(f"#{gD} #pkL", [(400, 170), (400, 232), (285, 300), (170, 365)], tcL - 0.1, 0.55)
pop(f"#{gD} .pill", T["contactarnos"] - 0.1, 0.5, 0.7)
pop(f"#{gD} .nR", tcR + 0.15); draw(f"#{gD} .cR", tcR + 0.3, 0.7, 0.1)
js.append(f'tl.fromTo("#{gD} .lbR",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{tcR + 0.35:.4f});')
packet(f"#{gD} #pkR", [(400, 170), (400, 232), (515, 300), (630, 365)], tcR - 0.1, 0.55)
gone(f"#{gD}", T["daas"] - 0.25)

# E · "DaaS": la pantalla en el centro y el pago que vuelve cada mes (morado)
bgs(T["daas"], T["por"], PUR)
e1 = tx(T["daas"], T["por"], [('<span class="b">DaaS</span>', round(S1 * 1.9)), ('<span class="l">modelo de</span> <span class="b">arrendamiento</span>', S2)], "bl", "letter-spacing:-0.02em;text-shadow:none")
rise(f"#{e1} .ln:nth-child(1) .rw", T["daas"], 0.8)
rise(f"#{e1} .ln:nth-child(2) .rw", T["arrendamiento"] - 0.5, 0.7)
gone(f"#{e1} .rw", T["por"] - 0.25)
gE = nid("g")
coins = "".join(f'<g class="nd cn"><circle cx="{400 + 250 * math.cos(math.radians(a_)):.0f}" cy="{370 + 250 * math.sin(math.radians(a_)):.0f}" r="40" fill="#fff" stroke="none"/>'
                f'<circle cx="{400 + 250 * math.cos(math.radians(a_)):.0f}" cy="{370 + 250 * math.sin(math.radians(a_)):.0f}" r="22" stroke="#7d00ba" stroke-width="8"/></g>' for a_ in (-90, 30, 150))
stg(gE, T["daas"] + 0.1, T["por"],
    '<circle class="er" cx="400" cy="370" r="250" pathLength="1" style="stroke-dasharray:1 2;stroke-dashoffset:1" stroke-opacity="0.55"/>'
    + pth("M310 290H490V400H310Z", 'class="es"') + pth("M400 400V440M350 440H450", 'class="es"') + pth("M346 338H454", 'class="es"')
    + f'<g class="orb">{coins}</g>')
draw(f"#{gE} .er", T["daas"] + 0.3, 1.0, 0.0)
draw(f"#{gE} .es", T["daas"] + 0.5, 0.8, 0.12)
pop(f"#{gE} .cn", T["daas"] + 1.0, 0.45, 0.4, 0.15)
js.append(f'tl.to("#{gE} .orb",{{rotation:360,svgOrigin:"400 370",duration:{T["por"] - T["daas"] - 1.5:.2f},ease:"power1.inOut"}},{T["daas"] + 1.2:.4f});')
gone(f"#{gE}", T["por"] - 0.25)

# F · "una cuota mensual": mes a mes se marca el pago (sobre el plano)
gF = nid("g")
tl_ = ""
for r_ in range(3):
    for c_ in range(4):
        x_, y_ = 30 + c_ * 195, 120 + r_ * 150
        tl_ += pth(f"M{x_} {y_}H{x_ + 150}V{y_ + 110}H{x_}Z", 'class="fr"') + pth(f"M{x_ + 42} {y_ + 58}L{x_ + 68} {y_ + 82}L{x_ + 112} {y_ + 30}", 'class="fc"')
stg(gF, T["cuota"] - 0.1, T["llenar"], tl_)
draw(f"#{gF} .fr", T["cuota"], 0.6, 0.05)
draw(f"#{gF} .fc", T["cuota"] + 0.5, 0.35, (T["llenar"] - T["cuota"] - 1.4) / 12)
gone(f"#{gF}", T["llenar"] - 0.2)

# H–L · "muchas ventajas": las cuatro tarjetas, cada una con su mini-diagrama (fondo blanco)
tV0 = T["hay1"]
bgs(tV0, tM0, "#fafafa")
hv = tx(tV0 + 0.1, tM0, [('<span class="l">Muchas</span> <span class="b" style="color:#3976ff">ventajas.</span>', round(S1 * 0.62))], "bl", INKS + f";bottom:auto;top:{SAFE['t']}px")
rise(f"#{hv} .rw", tV0 + 0.15, 0.7, 0.1); gone(f"#{hv} .rw", tM0 - 0.25)
TS, SS = {"16": (31, 22), "9": (34, 24), "45": (32, 23)}[FMT]
CW, CH, GAP = {"16": (366, 470, 24), "9": (429, 400, 28), "45": (429, 290, 28)}[FMT]
cols_ = 4 if FMT == "16" else 2
gx0 = (W - (cols_ * CW + (cols_ - 1) * GAP)) // 2
gy0 = {"16": 290, "9": 520, "45": 330}[FMT]
CARDS = [("coin", "Pagas por lo que usas", "Sin comprar de golpe", T["pagas"], ACC),
         ("refresh", "Siempre actualizada", "Las últimas actualizaciones", T["siempre"], ACC),
         ("head", "Soporte técnico prioritario", "Atención primero", T["soporte"], PUR),
         ("shield", "Nosotros nos encargamos", "Si sufre algún daño", T["si"], PUR)]


def mini(k, col):
    if k == 0:    # barras de uso y la moneda que las sigue: pagas según lo que usas
        hs = [50, 95, 70, 140, 110]
        bars = "".join(f'<rect class="bar" x="{40 + i * 66}" y="{176 - h}" width="44" height="{h}" rx="10" fill="{col}" stroke="none"/>' for i, h in enumerate(hs))
        return (pth("M16 180H384", 'class="m0"') + bars + f'<g id="mc0"><circle r="24" fill="#fff" stroke="{col}" stroke-width="9"/><circle r="8" fill="{col}" stroke="none"/></g>'), hs
    if k == 1:    # la pantalla se actualiza: barra que se llena y sello de listo
        return (pth("M110 20H290V140H110Z", 'class="m1"') + pth("M200 140V170M160 170H240", 'class="m1"')
                + f'<rect x="140" y="82" width="120" height="16" rx="8" fill="{col}" stroke="none" opacity=".22"/><rect class="fill1" x="140" y="82" width="120" height="16" rx="8" fill="{col}" stroke="none"/>'
                + f'<g class="nd bdg"><circle cx="300" cy="24" r="30" fill="{col}" stroke="none"/>' + pth("M286 24L296 34L316 12", 'class="m1c" stroke="#fff" stroke-width="9"') + '</g>'), None
    if k == 2:    # la cola: el ticket del cliente salta al frente
        def tile(x, c, fill):
            return (f'<g class="{c}"><rect x="{x}" y="50" width="92" height="92" rx="16" fill="{col if fill else "none"}" stroke="{col}" stroke-opacity="{1 if fill else .38}" stroke-width="9"/>'
                    f'<path d="M{x + 22} 80H{x + 70}M{x + 22} 104H{x + 56}" stroke="{"#fff" if fill else col}" stroke-opacity="{1 if fill else .38}" stroke-width="9"/></g>')
        return tile(40, "q1", False) + tile(150, "q2", False) + tile(260, "q3", True), None
    # k == 3: pantalla dañada que se repara y queda protegida
    return (pth("M90 15H310V135H90Z", 'class="m3"') + pth("M200 135V165M155 165H245", 'class="m3"')
            + pth("M190 15L215 58L180 85L215 118L200 135", 'class="cr" style="stroke:#ff6b5a;stroke-dasharray:1 2;stroke-dashoffset:1" stroke-width="10"')
            + f'<g class="nd shd"><path d="M200 38C225 46 247 46 265 44C265 88 243 110 200 124C157 110 135 88 135 44C153 46 175 46 200 38Z" fill="#fff" stroke="{col}" stroke-width="11"/></g>'
            + pth("M172 80L194 102L232 60", 'class="ck" style="stroke-dasharray:1 2;stroke-dashoffset:1" stroke-width="11" stroke="' + col + '"')), None


for k, (ic, ti, su, tt, col) in enumerate(CARDS):
    i = f"ky{k}"
    x = gx0 + (k % cols_) * (CW + GAP); y = gy0 + (k // cols_) * (CH + GAP)
    svg_, hs = mini(k, col)
    els.append(f'<div id="{i}" class="clip cd" data-start="{tt - 0.05:.4f}" data-duration="{tM0 - tt + 0.05 - 0.0:.4f}" data-track-index="3" style="left:{x}px;top:{y}px;width:{CW}px;height:{CH}px;border-color:{col}">'
               f'<div class="mini"><svg viewBox="0 0 400 200" fill="none" stroke="{col}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round">{svg_}</svg></div>'
               f'<div class="bd"><div class="dc" style="border-color:{col}">{icon(ic, 30, 2.6, "", col)}</div><div><b>{ti}</b><i>{su}</i></div></div></div>')
    js.append(f'tl.fromTo("#{i}",{{opacity:0,y:50,scale:0.88}},{{opacity:1,y:0,scale:1,duration:0.55,ease:"back.out(1.5)"}},{tt - 0.05:.4f});')
    js.append(f'tl.to("#{i}",{{opacity:0,x:-60,duration:0.3,ease:"power2.in"}},{tM0 - 0.3:.4f});')
    t0_ = tt + 0.35
    if k == 0:
        js.append(f'tl.fromTo("#{i} .bar",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:0.5,ease:"back.out(1.4)",stagger:0.16}},{t0_:.4f});')
        draw(f"#{i} .m0", t0_ - 0.1, 0.5, 0)
        px = [40 + j * 66 + 22 for j in range(5)]; py = [176 - h - 36 for h in hs]
        js.append(f'tl.fromTo("#{i} #mc0",{{x:{px[0]},y:{py[0]},opacity:0}},{{opacity:1,duration:0.2}},{t0_ + 0.3:.4f});')
        for j in range(1, 5):
            js.append(f'tl.to("#{i} #mc0",{{x:{px[j]},y:{py[j]},duration:0.42,ease:"power2.inOut"}},{t0_ + 0.5 + (j - 1) * 0.5:.4f});')
    elif k == 1:
        draw(f"#{i} .m1", t0_, 0.7, 0.1)
        js.append(f'tl.fromTo("#{i} .fill1",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:1.4,ease:"power1.inOut"}},{t0_ + 0.5:.4f});')
        pop(f"#{i} .bdg", t0_ + 1.9, 0.45, 0.4); draw(f"#{i} .m1c", t0_ + 2.0, 0.35, 0)
    elif k == 2:
        pop(f"#{i} .q1,#{i} .q2,#{i} .q3", t0_, 0.45, 0.6, 0.1)
        js.append(f'tl.to("#{i} .q3",{{x:-220,duration:0.75,ease:"power3.inOut"}},{t0_ + 0.9:.4f});')
        js.append(f'tl.to("#{i} .q3",{{y:-46,duration:0.375,ease:"power2.out",yoyo:true,repeat:1}},{t0_ + 0.9:.4f});')
        js.append(f'tl.to("#{i} .q1,#{i} .q2",{{x:110,duration:0.75,ease:"power3.inOut"}},{t0_ + 0.9:.4f});')
    else:
        draw(f"#{i} .m3", t0_, 0.6, 0.1); draw(f"#{i} .cr", t0_ + 0.5, 0.45, 0)
        js.append(f'tl.to("#{i} .cr",{{opacity:0,duration:0.3}},{t0_ + 1.5:.4f});')
        pop(f"#{i} .shd", t0_ + 1.5, 0.5, 0.5); draw(f"#{i} .ck", t0_ + 1.9, 0.45, 0)
'''
anchor = "# ── subtítulos:"
assert anchor in s
s = s.replace(anchor, NEW + anchor, 1)

# CSS: tarjetas, etiquetas, nodos (el bloque de estilos del builder es un f-string: llaves dobles y {TS}/{SS})
CSS = (".nd{{transform-box:fill-box;transform-origin:center}} .bar{{transform-box:fill-box}} .fill1{{transform-box:fill-box}} .lb{{font:700 58px Rubik;fill:#fff;stroke:none;letter-spacing:-0.02em}} "
       ".cd{{position:absolute;background:#fff;border:6px solid;border-radius:28px;display:flex;flex-direction:column;overflow:hidden;box-sizing:border-box}} "
       ".cd .mini{{flex:1;min-height:0;padding:14px 18px 0}} .cd .mini svg{{width:100%;height:100%;overflow:visible}} "
       ".cd .bd{{display:flex;gap:14px;align-items:center;padding:8px 20px 20px}} .cd .dc{{flex:none;width:56px;height:56px;border-radius:50%;border:5px solid;display:flex;align-items:center;justify-content:center}} "
       ".cd .dc svg{{margin:0 !important;vertical-align:0 !important}} "
       ".cd b{{font-family:'Rubik';font-weight:700;font-size:{TS}px;letter-spacing:-0.02em;color:#0b0b14;line-height:1.05;display:block}} "
       ".cd i{{font-style:normal;font-family:'Rubik';font-weight:400;font-size:{SS}px;color:#555;display:block;margin-top:4px}} ")
a = ".ln{{display:block}} .gfx{{position:absolute}}"
assert a in s
s = s.replace(a, a + " " + CSS, 1)
if "import math" not in s.split("# ── gráficos")[0]:
    s = s.replace("import json, os, re", "import json, math, os, re", 1)
f.write_text(s, encoding="utf-8")
print("ok r3d")
