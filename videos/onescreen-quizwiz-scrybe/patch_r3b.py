"""build_rental3 — gráficos descriptivos, cada uno con su propio tratamiento (Cris: variarlos, no quitarlos).
Se insertan antes de los subtítulos; el texto sigue suelto sobre el plano, sin cajas."""
from pathlib import Path
f = Path(__file__).parent / "build_rental3.py"
s = f.read_text(encoding="utf-8")

GFX = r'''
# ── gráficos descriptivos (líneas que se dibujan, sin contenedores) ─────────────────────────────────
GW, GH = {"16": (560, 390), "9": (700, 470), "45": (620, 410)}[FMT]
GX = {"16": W - SAFE["r"] - GW, "9": (W - GW) // 2, "45": (W - GW) // 2}[FMT]
GY = {"16": (H - GH) // 2 - 10, "9": SAFE["t"] + 30 + round(S1 * 2.25), "45": SAFE["t"] + 20 + round(S1 * 2.2)}[FMT]
SW = 7


def gfx(i, t0, t1, inner, x=None, y=None, w=None, h=None, vb="0 0 560 390", stroke="#fff", shadow=True):
    x = GX if x is None else x; y = GY if y is None else y; w = GW if w is None else w; h = GH if h is None else h
    flt = "filter:drop-shadow(0 3px 14px rgba(0,0,0,.5));" if shadow else ""
    els.append(f'<div id="{i}" class="clip gfx" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{flt}">'
               f'<svg viewBox="{vb}" width="100%" height="100%" fill="none" stroke="{stroke}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{inner}</svg></div>')


def draw(sel, t, d=0.8, stag=0.08, ease="power2.inOut"):
    js.append(f'tl.fromTo("{sel}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{d},ease:"{ease}",stagger:{stag}}},{t:.4f});')


def pth(d, extra=""):
    return f'<path d="{d}" pathLength="1" style="stroke-dasharray:1 2;stroke-dashoffset:1" {extra}/>'


# A · "primera aula digital": marco de enfoque sobre la pantalla (esquinas que se dibujan y se cierran)
gA = nid("g")
gfx(gA, T["primera"] + 0.2, T["tener"] + 0.4,
    pth("M30 110V30H110", 'class="a1"') + pth("M450 30H530V110", 'class="a1"') + pth("M530 280V360H450", 'class="a1"') + pth("M110 360H30V280", 'class="a1"'))
draw(f"#{gA} .a1", T["primera"] + 0.25, 0.7, 0.1)
js.append(f'tl.fromTo("#{gA} svg",{{scale:1.22,transformOrigin:"50% 50%"}},{{scale:1,duration:0.9,ease:"power3.out"}},{T["primera"] + 0.25:.4f});')
gone(f"#{gA}", T["tener"] + 0.1)
# B · "pantalla interactiva": toque con ondas
gB = nid("g")
gfx(gB, T["tener"] + 0.5, T["para"], '<circle cx="280" cy="195" r="26" fill="#fff" stroke="none" class="b0"/>' + "".join(f'<circle cx="280" cy="195" r="{r}" class="b1" style="opacity:0"/>' for r in (60, 105, 150)))
js.append(f'tl.fromTo("#{gB} .b0",{{scale:0.3,transformOrigin:"280px 195px"}},{{scale:1,duration:0.45,ease:"back.out(2)"}},{T["tener"] + 0.5:.4f});')
js.append(f'tl.fromTo("#{gB} .b1",{{opacity:0.9,scale:0.35,transformOrigin:"280px 195px"}},{{opacity:0,scale:1.1,duration:1.1,ease:"power2.out",stagger:0.28,repeat:1}},{T["tener"] + 0.85:.4f});')
# D · "dos caminos": bifurcación dibujada bajo el texto de la tarjeta blanca (trazo azul)
gD = nid("g")
fx_, fy_ = (W // 2 - 320, round(H * 0.58)) if FMT == "16" else (W // 2 - 310, round(H * 0.56))
gfx(gD, T["hay"] + 0.45, T["primero0"] + 0.1,
    pth("M320 0V70", 'class="d1"') + pth("M320 70C320 130 140 110 140 200", 'class="d1"') + pth("M320 70C320 130 500 110 500 200", 'class="d1"')
    + pth("M115 175L140 205L165 175", 'class="d1"') + pth("M475 175L500 205L525 175", 'class="d1"'),
    x=fx_, y=fy_, w=640, h=230, vb="0 0 640 230", stroke=ACC, shadow=False)
draw(f"#{gD} .d1", T["hay"] + 0.55, 0.8, 0.12)
# F · "cuota mensual": calendario que se llena mes a mes
gF = nid("g")
cells = "".join(f'<circle class="f2" cx="{95 + c * 123}" cy="{205 + r * 62}" r="17" fill="#fff" stroke="none" style="opacity:0"/>' for r in range(3) for c in range(4))
gfx(gF, T["cuota"] - 0.1, T["llenar"], pth("M20 60H540V370H20Z", 'class="f1"') + pth("M20 120H540", 'class="f1"') + pth("M150 20V80", 'class="f1"') + pth("M410 20V80", 'class="f1"') + cells)
draw(f"#{gF} .f1", T["cuota"], 0.8, 0.1)
js.append(f'tl.fromTo("#{gF} .f2",{{opacity:0,scale:0.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",stagger:{(T["llenar"] - T["cuota"] - 0.9) / 12:.3f}}},{T["cuota"] + 0.8:.4f});')
gone(f"#{gF}", T["llenar"] - 0.2)
# G · "llenar toda tu institución": una fila de pantallas que se va llenando con cada plano
gG = nid("g")
n_ = len(shots); sz_ = {"16": 120, "9": 110, "45": 100}[FMT]; gap_ = 26
rw_ = n_ * sz_ + (n_ - 1) * gap_
mons = "".join(f'<g class="g1" style="opacity:0" transform="translate({k * (sz_ + gap_)} 0)"><rect x="4" y="6" width="{sz_ - 8}" height="{sz_ * 0.62:.0f}" rx="9"/><path d="M{sz_ * 0.3:.0f} {sz_ * 0.86:.0f}H{sz_ * 0.7:.0f}"/><path d="M{sz_ / 2:.0f} {sz_ * 0.7:.0f}V{sz_ * 0.86:.0f}"/></g>' for k in range(n_))
gfx(gG, T["llenar"], tG1, mons, x=(W - rw_) // 2, y=SAFE["t"] + 10, w=rw_, h=sz_, vb=f"0 0 {rw_} {sz_}")
for k in range(n_):
    js.append(f'tl.fromTo("#{gG} .g1:nth-child({k + 1})",{{opacity:0,scale:0.4,transformOrigin:"{k * (sz_ + gap_) + sz_ / 2}px {sz_ / 2}px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{snap(cuts[k]):.4f});')
gone(f"#{gG}", tG1 - 0.25)
# I · "pagas por lo que usas": medidor de uso (arco y aguja)
gI = nid("g")
import math
ticks_ = "".join(pth("M%d %dL%d %d" % (280 + 190 * math.cos(math.radians(a_)), 300 - 190 * math.sin(math.radians(a_)), 280 + 215 * math.cos(math.radians(a_)), 300 - 215 * math.sin(math.radians(a_))), 'class="i1"') for a_ in range(20, 170, 30))
gfx(gI, T["pagas"] + 0.2, tJ0, pth("M60 300A220 220 0 0 1 500 300", 'class="i1"') + ticks_ + '<path class="i2" d="M280 300L280 130" stroke-width="9"/><circle cx="280" cy="300" r="14" fill="#fff" stroke="none"/>')
draw(f"#{gI} .i1", T["pagas"] + 0.25, 0.7, 0.05)
js.append(f'tl.fromTo("#{gI} .i2",{{rotation:-70,transformOrigin:"280px 300px"}},{{rotation:28,duration:{tJ0 - T["pagas"] - 0.9:.3f},ease:"power2.inOut"}},{T["pagas"] + 0.6:.4f});')
gone(f"#{gI}", tJ0 - 0.25)
# J · "siempre actualizada": barra de progreso que se llena y marca de listo
gJ = nid("g")
gfx(gJ, tJ0 + 0.1, tK0, '<path d="M30 190H530" stroke-opacity="0.35"/>' + pth("M30 190H530", 'class="j1" stroke-width="14"') + pth("M455 90L500 135L545 90", 'class="j2" transform="translate(0 -40)"') + pth("M240 270L275 305L335 235", 'class="j3"'))
js.append(f'tl.fromTo("#{gJ} .j1",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{tK0 - tJ0 - 0.9:.3f},ease:"power1.inOut"}},{tJ0 + 0.3:.4f});')
draw(f"#{gJ} .j3", tK0 - 0.8, 0.5, 0.0)
gone(f"#{gJ}", tK0 - 0.25)
# K · "soporte técnico prioritario": ondas de atención que salen del auricular
gK = nid("g")
gfx(gK, tK0 + 0.2, tL0, '<circle cx="280" cy="195" r="30" fill="#fff" stroke="none"/>' + "".join(f'<circle cx="280" cy="195" r="{r}" class="k1" style="opacity:0"/>' for r in (70, 115, 160)))
js.append(f'tl.fromTo("#{gK} .k1",{{opacity:0.95,scale:0.3,transformOrigin:"280px 195px"}},{{opacity:0,scale:1.15,duration:1.0,ease:"power2.out",stagger:0.25,repeat:2}},{tK0 + 0.3:.4f});')
gone(f"#{gK}", tL0 - 0.25)
# L · "si sufre algún daño, nosotros nos encargamos": pantalla agrietada que se repara y queda protegida
gL = nid("g")
gfx(gL, tL0 - 0.05, tM0, pth("M60 40H500V270H60Z", 'class="l0"') + pth("M280 270V330M180 335H380", 'class="l0"')
    + pth("M250 40L290 120L240 170L300 230L270 270", 'class="l1" style="stroke:#ff6b5a;stroke-dasharray:1 2;stroke-dashoffset:1" stroke-width="9"')
    + pth("M280 80C330 100 380 100 420 95C420 190 370 235 280 255C190 235 140 190 140 95C180 100 230 100 280 80Z", 'class="l2" stroke-width="9"') + pth("M225 160L265 200L340 120", 'class="l3" stroke-width="10"'))
draw(f"#{gL} .l0", tL0, 0.7, 0.1)
draw(f"#{gL} .l1", tL0 + 0.55, 0.45, 0.0)
js.append(f'tl.to("#{gL} .l1",{{opacity:0,duration:0.35}},{T["nosotros"] + 0.35:.4f});')
draw(f"#{gL} .l2", T["nosotros"] + 0.3, 0.7, 0.0)
draw(f"#{gL} .l3", T["encargamos"] + 0.3, 0.5, 0.0)
gone(f"#{gL}", tM0 - 0.25)
# N · "Pregúntanos": globo de conversación con puntos que escriben
gN = nid("g")
gfx(gN, tN0 + 0.2, END, pth("M30 40H530V250H200L90 340V250H30Z", 'class="n1"') + "".join(f'<circle class="n2" cx="{200 + k * 80}" cy="145" r="14" fill="#fff" stroke="none" style="opacity:0"/>' for k in range(3)))
draw(f"#{gN} .n1", tN0 + 0.25, 0.7)
js.append(f'tl.fromTo("#{gN} .n2",{{opacity:0.15,y:6}},{{opacity:1,y:-6,duration:0.35,ease:"sine.inOut",stagger:0.18,repeat:5,yoyo:true}},{tN0 + 0.9:.4f});')

'''
anchor = "# ── subtítulos:"
assert anchor in s
s = s.replace(anchor, GFX + anchor, 1)
f.write_text(s, encoding="utf-8")
print("ok r3b")
