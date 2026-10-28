"""Video OneScreen Rental / DaaS v3 — estilo corregido por Cris (23-oct-2026, ver estilo-onescreen/08_TEXTO_Y_SUBTITULOS.md):
 - texto directamente sobre el plano (sin contenedores), tarjetas blancas solo para enfatizar una línea;
 - subtítulos blancos con trazo negro duro y fino, y solo donde no hay texto/gráfico que ya lo diga;
 - márgenes seguros reales; menos relleno; cada gráfico con su propio tratamiento (no una plantilla repetida).
Uso: FMT=16|9|45 ALPHA=0|1 python build_rental3.py
  ALPHA=1 -> solo la capa gráfica (sin planos), para renderizar en MOV con alfa y montarla sobre los planos en Premiere."""
import json, math, os, re
from pathlib import Path

FMT = os.environ.get("FMT", "16")
ALPHA = os.environ.get("ALPHA", "0") == "1"
CAPS = os.environ.get("CAPS", "1") == "1"
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[FMT]
PROJ = Path(os.environ.get("PROJ") or f"D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_{FMT}")
SCRIBE = os.environ.get("SCRIBE", r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-21_rental_daas/scribe_v_rv_1.json")
FPS, D, LEAD = 24, 0.10, 0.10
ACC, PUR, INK = "#3976ff", "#7d00ba", "#0b0b14"
SAFE = {"16": dict(l=270, r=270, t=150, b=170), "9": dict(l=150, r=150, t=340, b=550), "45": dict(l=150, r=150, t=210, b=310)}[FMT]
S1 = {"16": 150, "9": 118, "45": 112}[FMT]          # texto grande sobre el plano
S2 = round(S1 * 0.46)                               # texto de apoyo
S3 = round(S1 * 0.34)

words = [w for w in json.load(open(SCRIBE, encoding="utf-8"))["words"] if w.get("type") == "word"]


def norm(t):
    return re.sub(r"[¿?¡!.,;:]", "", t).lower()


def snap(t):
    return round(t * FPS) / FPS


def EV(word, n=0):
    k = [w for w in words if norm(w["text"]) == word]
    return snap(k[n]["start"] + D - LEAD)


END = snap(words[-1]["end"] + D + 1.4)
els, js, clips = [], [], []         # clips: lista de planos para el proyecto de Premiere
cnt = [0]


def nid(p):
    cnt[0] += 1
    return f"{p}{cnt[0]:02d}"


def rise(sel, t, d=0.65, stag=0.07):
    js.append(f'tl.fromTo("{sel}",{{yPercent:110,opacity:0}},{{yPercent:0,opacity:1,duration:{d},ease:"power4.out",stagger:{stag}}},{t:.4f});')


def gone(sel, t, d=0.3, x=-50):
    js.append(f'tl.to("{sel}",{{opacity:0,x:{x},duration:{d},ease:"power2.in"}},{t:.4f});')


def vid(src, t, t1, tin=0.0, scale=100, origin="50% 50%", cls="", style=""):
    """plano a pantalla completa (se omite en la capa con alfa, pero queda en la lista para Premiere)"""
    clips.append(dict(src=src, t=round(t, 4), dur=round(t1 - t, 4), tin=tin, scale=scale, origin=origin))
    if ALPHA:
        return
    i = nid("v")
    els.append(f'<video id="{i}" class="clip {cls}" src="media/{src}.mp4" muted playsinline data-start="{t:.4f}" data-duration="{t1 - t:.4f}" data-media-start="{tin:.4f}" data-track-index="1" '
               f'style="object-position:{origin.split()[0]} 50%;transform-origin:{origin};transform:scale({scale / 100:.3f});{style}"></video>')


POS = {"16": dict(bl=f"left:{SAFE['l']}px;bottom:{SAFE['b'] + 40}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);text-align:center"),
       "9": dict(bl=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 30}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 30}px;text-align:center"),
       "45": dict(bl=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 20}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 20}px;text-align:center")}[FMT]


def tx(t0, t1, lines, pos="bl", extra="", cid=None):
    """texto suelto sobre el plano; lines = [(html, tamaño)], cada línea sube por máscara"""
    i = cid or nid("t")
    body = "".join(f'<div class="ln" style="font-size:{sz}px"><span class="mk"><span class="rw">{h}</span></span></div>' for h, sz in lines)
    els.append(f'<div id="{i}" class="clip tx" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3" style="{POS[pos]};{extra}">{body}</div>')
    return i


def card(t0, t1, lines, cid=None):
    """tarjeta blanca de énfasis: una línea corta, azul, mezcla de pesos (como las de febrero)"""
    i = cid or nid("w")
    sz = {"16": 74, "9": 64, "45": 62}[FMT]
    body = "".join(f'<div class="cl" style="font-size:{sz}px"><span class="mk"><span class="rw">{h}</span></span></div>' for h in lines)
    els.append(f'<div id="{i}" class="clip white" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="2"><div class="cw">{body}</div></div>')
    js.append(f'tl.fromTo("#{i}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"power3.inOut"}},{t0:.4f});')
    rise(f"#{i} .rw", t0 + 0.2, 0.6, 0.12)
    return i


def bgs(t0, t1, color, cid=None):
    """escena de fondo liso (blanco o de color) para motion graphics; entra con un barrido"""
    i = cid or nid("b")
    els.append(f'<div id="{i}" class="clip white" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="2" style="background:{color}"></div>')
    js.append(f'tl.fromTo("#{i}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"power3.inOut"}},{t0:.4f});')
    return i


INKS = "color:#0b0b14;text-shadow:none"


def icon(name, size, sw=2, iid="", col="#fff"):
    P = {"chat": ["M4 5h16v11H9l-5 4z", "M8 9.5h8", "M8 12.5h5"], "coin": ["M12 3a9 9 0 1 0 .01 0", "M14.5 8.5c-.6-.8-1.5-1.2-2.5-1.2-1.5 0-2.6.8-2.6 2 0 3 5.3 1.3 5.3 4.2 0 1.2-1.2 2-2.7 2-1.1 0-2.1-.5-2.7-1.4", "M12 5.6v1.7", "M12 16.7v1.7"],
         "refresh": ["M20 12a8 8 0 1 1-2.6-5.9", "M20 4v5h-5"], "head": ["M4 14v-2a8 8 0 0 1 16 0v2", "M4 14h3v5H4z", "M17 14h3v5h-3z", "M20 19v1a2 2 0 0 1-2 2h-4"],
         "shield": ["M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z", "M8.5 12l2.5 2.5 4.5-5"]}[name]
    ps = "".join(f'<path d="{p}" pathLength="1"/>' for p in P)
    return f'<svg id="{iid}" class="ic" viewBox="0 0 24 24" width="{size}" height="{size}" style="stroke:{col};stroke-width:{sw};margin-left:0.18em;vertical-align:-0.08em">{ps}</svg>'


def icon_at(i, svg, t, pos_css, d=0.9):
    els.append(f'<div id="{i}" class="clip icb" data-start="{t:.4f}" data-duration="{END - t:.4f}" data-track-index="3" style="{pos_css}">{svg}</div>')
    js.append(f'tl.fromTo("#{i} path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{d},ease:"power2.inOut",stagger:0.1}},{t:.4f});')


# ── línea de tiempo (planos y texto, todo nace de la palabra) ────────────────
T = {k: EV(k) for k in ("primera", "tener", "para", "onescreen", "hay", "caminos", "contactarnos", "daas", "arrendamiento", "por", "cuota", "llenar", "toda", "pagas", "siempre", "soporte", "prioritario", "sufre", "nosotros", "quieres", "pregúntanos", "explicamos")}
T["o2"] = EV("o", 1); T["hay1"] = EV("hay", 1); T["primero0"] = EV("primero", 0); T["primero1"] = EV("primero", 1); T["encargamos"] = EV("encargamos"); T["si"] = EV("si")
t_dos = EV("dos")
E = {"split": T["hay"]}

# A · "Hoy quiero que hablemos sobre tu primera aula digital"
vid("r1", 0.0, T["tener"], 0.0)
a = tx(T["primera"], T["tener"] + 0.5, [('<span class="l">Tu primera</span>', S2 * 1.5), ('<span class="b">aula digital</span>', S1)], "bl")
rise(f"#{a} .rw", T["primera"], 0.75, 0.12); gone(f"#{a} .rw", T["tener"] + 0.2)
# B · "tener tu propia pantalla interactiva"
vid("r2", T["tener"], T["para"], 0.0, 144)
# C · "Para tener tu propia OneScreen, a tu medida"
vid("r3", T["para"], T["hay"], 0.0)
els.append(f'<div id="lg" class="clip tx" data-start="{T["onescreen"] - 0.1:.4f}" data-duration="1.7" data-track-index="3" style="{POS["c"] if FMT == "16" else POS["c"]};{"top:44%;transform:translateY(-50%)" if FMT == "16" else ""}"><span class="mk"><span class="rw lgo">@@LOGO@@</span></span></div>')
rise("#lg .rw", T["onescreen"] - 0.1, 0.7); gone("#lg .rw", T["onescreen"] + 1.2)
# F · "Por una cuota accesible, mensualmente"
vid("m1", T["por"], T["llenar"], 1.0)
# (texto de F: ver bloque 3D)
# G · "puedes llenar toda tu institución de pantallas interactivas": montaje de aulas
tG1 = EV("interactivas") + 0.7
shots = [("m2", 1.0), ("m4", 2.0), ("m3", 0.5), ("m5", 0.8), ("m1", 2.4)]
cuts = [T["llenar"] + i * (tG1 - T["llenar"]) / len(shots) for i in range(len(shots))] + [tG1]
for k, (s, tin) in enumerate(shots):
    vid(s, snap(cuts[k]), snap(cuts[k + 1]), tin, 100 if k % 2 == 0 else 125)
g = tx(T["toda"], tG1, [('<span class="l">Toda tu</span>', S2 * 1.4), ('<span class="b">institución</span>', S1)], "bl", (f"left:auto;right:{SAFE['r']}px;text-align:right" if FMT == "16" else ""))
rise(f"#{g} .rw", T["toda"], 0.7, 0.12); gone(f"#{g} .rw", tG1 - 0.25)
tJ0, tK0, tL0, tM0 = T["siempre"], T["soporte"], T["si"], T["quieres"]
# M · "¿Quieres adquirir tu pantalla?"
tN0 = T["pregúntanos"]
card(tM0, tN0 + 0.15, ['<span class="l">¿Quieres adquirir tu</span> <span class="b">pantalla</span>?'])
# N · "Pregúntanos y te explicamos cómo."
vid("m3", tN0 + 0.15, END, 0.4)
n1 = tx(tN0, END, [('<span class="b">Pregúntanos</span>', S1), ('<span class="l">onescreenlatam.com/<span class="b">rental</span></span>', S2 * 1.05)], "c")
rise(f"#{n1} .rw", tN0 + 0.15, 0.75, 0.16)


# ── gráficos descriptivos (líneas que se dibujan, sin contenedores) ─────────────────────────────────
GW, GH = {"16": (560, 390), "9": (700, 470), "45": (620, 410)}[FMT]
GX = {"16": W - SAFE["r"] - GW, "9": (W - GW) // 2, "45": (W - GW) // 2}[FMT]
GY = {"16": (H - GH) // 2 - 10, "9": SAFE["t"] + 30 + round(S1 * 2.25), "45": SAFE["t"] + 20 + round(S1 * 2.2)}[FMT]
SW = 28


def gfx(i, t0, t1, inner="", x=None, y=None, w=None, h=None, vb="0 0 560 390", stroke="#fff", shadow=False):
    x = GX if x is None else x; y = GY if y is None else y; w = GW if w is None else w; h = GH if h is None else h
    flt = "filter:drop-shadow(0 3px 14px rgba(0,0,0,.5));" if shadow else ""
    els.append(f'<div id="{i}" class="clip gfx" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;color:{stroke};{flt}">'
               f'<svg viewBox="{vb}" width="100%" height="100%" fill="none" stroke="{stroke}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{inner}</svg></div>')


def draw(sel, t, d=0.8, stag=0.08, ease="power2.inOut"):
    js.append(f'tl.fromTo("{sel}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{d},ease:"{ease}",stagger:{stag}}},{t:.4f});')


def pth(d, extra=""):
    return f'<path d="{d}" pathLength="1" style="stroke-dasharray:1 2;stroke-dashoffset:1" {extra}/>'


# A · "primera aula digital": marco de enfoque sobre la pantalla (esquinas que se dibujan y se cierran)
gA = nid("g")
gfx(gA, T["primera"] + 0.2, T["tener"] + 0.4, x=(W - SAFE["r"] - 470 if FMT == "16" else None), y=((H - 327) // 2 - 10 if FMT == "16" else None), w=(470 if FMT == "16" else None), h=(327 if FMT == "16" else None), inner=
    pth("M30 110V30H110", 'class="a1"') + pth("M450 30H530V110", 'class="a1"') + pth("M530 280V360H450", 'class="a1"') + pth("M110 360H30V280", 'class="a1"'))
draw(f"#{gA} .a1", T["primera"] + 0.25, 0.7, 0.1)
js.append(f'tl.fromTo("#{gA} svg",{{scale:1.22,transformOrigin:"50% 50%"}},{{scale:1,duration:0.9,ease:"power3.out"}},{T["primera"] + 0.25:.4f});')
gone(f"#{gA}", T["tener"] + 0.1)
# B · "pantalla interactiva": toque con ondas
gB = nid("g")
gfx(gB, T["tener"] + 0.5, T["para"], y=(SAFE["t"] + 20 if FMT != "16" else None), inner='<circle cx="280" cy="195" r="26" fill="currentColor" stroke="none" class="b0"/>' + "".join(f'<circle cx="280" cy="195" r="{r}" class="b1" style="opacity:0"/>' for r in (60, 105, 150)))
js.append(f'tl.fromTo("#{gB} .b0",{{scale:0.3,transformOrigin:"280px 195px"}},{{scale:1,duration:0.45,ease:"back.out(2)"}},{T["tener"] + 0.5:.4f});')
js.append(f'tl.fromTo("#{gB} .b1",{{opacity:0.9,scale:0.35,transformOrigin:"280px 195px"}},{{opacity:0,scale:1.1,duration:1.1,ease:"power2.out",stagger:0.28,repeat:1}},{T["tener"] + 0.85:.4f});')
# G · "llenar toda tu institución": una fila de pantallas que se va llenando con cada plano
gG = nid("g")
n_ = len(shots); sz_ = {"16": 120, "9": 110, "45": 100}[FMT]; gap_ = 26
rw_ = n_ * sz_ + (n_ - 1) * gap_
mons = "".join(f'<g class="g1" stroke-width="9" style="opacity:0" transform="translate({k * (sz_ + gap_)} 0)"><rect x="4" y="6" width="{sz_ - 8}" height="{sz_ * 0.62:.0f}" rx="9"/><path d="M{sz_ * 0.3:.0f} {sz_ * 0.86:.0f}H{sz_ * 0.7:.0f}"/><path d="M{sz_ / 2:.0f} {sz_ * 0.7:.0f}V{sz_ * 0.86:.0f}"/></g>' for k in range(n_))
gfx(gG, T["llenar"], tG1, mons, x=(W - rw_) // 2, y=(SAFE["t"] + 10 if FMT == "16" else SAFE["t"] + 30 + round(S2 * 1.4 + S1 * 1.25) + 50), w=rw_, h=sz_, vb=f"0 0 {rw_} {sz_}")
for k in range(n_):
    js.append(f'tl.fromTo("#{gG} .g1:nth-child({k + 1})",{{opacity:0,scale:0.4,transformOrigin:"{k * (sz_ + gap_) + sz_ / 2}px {sz_ / 2}px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{snap(cuts[k]):.4f});')
gone(f"#{gG}", tG1 - 0.25)
# N · "Pregúntanos": globo de conversación con puntos que escriben
gN = nid("g")
gfx(gN, tN0 + 0.2, END, x=((W - 344) // 2 if FMT == "16" else None), y=(105 if FMT == "16" else None), w=(344 if FMT == "16" else None), h=(240 if FMT == "16" else None), inner=pth("M30 40H530V250H200L90 340V250H30Z", 'class="n1"') + "".join(f'<circle class="n2" cx="{200 + k * 80}" cy="145" r="14" fill="currentColor" stroke="none" style="opacity:0"/>' for k in range(3)))
draw(f"#{gN} .n1", tN0 + 0.25, 0.7)
js.append(f'tl.fromTo("#{gN} .n2",{{opacity:0.15,y:6}},{{opacity:1,y:-6,duration:0.35,ease:"sine.inOut",stagger:0.18,repeat:5,yoyo:true}},{tN0 + 0.9:.4f});')


# ══ escenas de diagrama: cada gráfico REPRESENTA lo que dice la voz (nodos, flujos, paquetes de luz) ══════
STG = {"16": (W - SAFE["r"] - 780, 150, 780, 760), "9": (SAFE["l"], SAFE["t"] + 30 + round(S1 * 2.25), W - 2 * SAFE["l"], H - SAFE["b"] - (SAFE["t"] + 30 + round(S1 * 2.25))),
       "45": (SAFE["l"], SAFE["t"] + 20 + round(S1 * 2.2), W - 2 * SAFE["l"], H - SAFE["b"] - (SAFE["t"] + 20 + round(S1 * 2.2)))}[FMT]


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



# ══ lettering con cámara 3D (perspective, z, rotación) ═════════════════════════════════════════════
BIGF = {"16": 300, "9": 190, "45": 190}[FMT]


def lets(word, cls=""):
    """cada palabra es una unidad que sube de abajo hacia arriba con transparencia (lettering Apple)"""
    return f'<span class="{cls}">' + "".join(f'<span class="lw">{w}</span>' + ("&nbsp;" if k < len(word.split(" ")) - 1 else "") for k, w in enumerate(word.split(" "))) + "</span>"


def big(i, html, size, css, color="#fff"):
    return f'<div id="{i}" class="big" style="font-size:{size}px;color:{color};{css}">{html}</div>'


def w3(i, t0, t1, inner):
    els.append(f'<div id="{i}" class="clip w3" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3"><div class="wd">{inner}</div></div>')


def flip(sel, t, d=1.1, stag=0.14, frm=0):
    sel = sel.replace(" .lt", " .lw"); d = max(d, 1.0); stag = max(stag, 0.12)
    js.append(f'tl.fromTo("{sel}",{{yPercent:55,opacity:0}},{{yPercent:0,opacity:1,duration:{d},ease:"power3.out",stagger:{stag}}},{t:.4f});')


def camera(sel, t, d, z=-300, rx=0, ry=0):
    js.append(f'tl.fromTo("{sel}",{{z:{z},rotationX:{rx},rotationY:{ry}}},{{z:0,rotationX:0,rotationY:0,duration:{d},ease:"power3.out"}},{t:.4f});')


SHD = "text-shadow:0 3px 26px rgba(0,0,0,.45)"

# D · "hay dos caminos": DOS / caminos. gigantes; se encogen a encabezado y la bifurcación se levanta del piso (azul)
bgs(T["hay"], T["daas"], ACC)
gD = nid("g")
tcL, tcR = T["primero0"], T["o2"]
top0 = SAFE["t"]
dl1 = big(f"{gD}a", lets("Dos", "l"), BIGF, f"left:{SAFE['l']}px;top:{top0}px")
dl2 = big(f"{gD}b", lets("caminos.", "b"), BIGF, f"right:{SAFE['r']}px;top:{top0 + round(BIGF * 0.88)}px;text-align:right")
FW = {"16": 800, "9": W - 2 * SAFE["l"], "45": W - 2 * SAFE["l"]}[FMT]
FH = round(FW * 740 / 800)
FY = {"16": (H - FH) // 2 + 70, "9": SAFE["t"] + 230, "45": SAFE["t"] + 150}[FMT]
fork = (pth("M400 174V230C400 320 170 270 170 358", 'class="dl"') + pth("M400 174V230C400 320 630 270 630 358", 'class="dl"')
        + '<g class="nd s0"><circle cx="400" cy="100" r="74" fill="#3976ff"/>' + pth("M358 78H442V122H358Z", 'class="s1"') + pth("M400 122V138M372 138H428", 'class="s1"') + '</g>'
        + '<g transform="translate(170 440)"><g class="nd nL"><circle r="82" fill="#3976ff"/>' + pth("M-40 -40H-22L-6 14H40L52 -22H-18", 'class="cL"')
        + '<circle cx="-2" cy="42" r="8" fill="#fff" stroke="none"/><circle cx="36" cy="42" r="8" fill="#fff" stroke="none"/></g></g>'
        + '<g transform="translate(630 440)"><g class="nd nR"><circle r="82" fill="#3976ff"/>' + pth("M-46 -30H46V46H-46Z", 'class="cR"') + pth("M-46 -4H46", 'class="cR"') + pth("M-20 -48V-22M20 -48V-22", 'class="cR"') + '</g></g>'
        + '<text class="lb lbL" x="170" y="600" text-anchor="middle">Comprarla</text><text class="lb lbR" x="630" y="600" text-anchor="middle">Arrendarla</text>'
        + '<g class="nd pill"><g transform="translate(40 640) scale(1.55)" stroke="#fff" stroke-width="2.3"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8"/><path d="M8 12.5h5"/></g>'
        + '<text x="100" y="684" style="font:600 40px Rubik;fill:#fff;stroke:none;letter-spacing:-0.02em">Contáctanos</text></g>'
        + '<circle id="pkL" r="15" fill="#fff" stroke="none" opacity="0"/><circle id="pkR" r="15" fill="#fff" stroke="none" opacity="0"/>')
forkdiv = (f'<div id="{gD}f" class="fk" style="left:{(W - FW) // 2}px;top:{FY}px;width:{FW}px;height:{FH}px"><svg viewBox="0 0 800 740" width="100%" height="100%" fill="none" stroke="#fff" '
           f'stroke-width="14" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{fork}</svg></div>')
w3(gD, T["hay"] + 0.05, T["daas"], f'<div id="{gD}t" class="ttl">{dl1}{dl2}</div>{forkdiv}')
camera(f"#{gD} .wd", T["hay"] + 0.05, 1.3, -260, 7, -8)
flip(f"#{gD}a .lt", T["hay"] + 0.2, 0.9, 0.07)
flip(f"#{gD}b .lt", T["caminos"] - 0.1, 0.9, 0.045)
# las letras se encogen a encabezado (esquina) y la bifurcación sube del piso
js.append(f'tl.to("#{gD}t",{{scale:0.36,z:-60,transformOrigin:"{SAFE["l"]}px {top0}px",duration:0.85,ease:"power3.inOut"}},{tcL + 0.05:.4f});')
js.append(f'tl.fromTo("#{gD}f",{{rotationX:64,y:240,opacity:0,transformPerspective:1500,transformOrigin:"50% 100%"}},{{rotationX:0,y:0,opacity:1,duration:1.0,ease:"power3.out"}},{tcL + 0.15:.4f});')
pop(f"#{gD} .s0", tcL + 0.4); draw(f"#{gD} .s1", tcL + 0.5, 0.7, 0.1)
draw(f"#{gD} .dl", tcL + 0.7, 0.7, 0.18)
pop(f"#{gD} .nL", tcL + 1.15); draw(f"#{gD} .cL", tcL + 1.3, 0.7, 0.1)
js.append(f'tl.fromTo("#{gD} .lbL",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{tcL + 1.35:.4f});')
packet(f"#{gD} #pkL", [(400, 170), (400, 232), (285, 300), (170, 365)], tcL + 0.7, 0.55)
pop(f"#{gD} .pill", T["contactarnos"] - 0.1, 0.5, 0.7)
pop(f"#{gD} .nR", tcR + 0.15); draw(f"#{gD} .cR", tcR + 0.3, 0.7, 0.1)
js.append(f'tl.fromTo("#{gD} .lbR",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{tcR + 0.35:.4f});')
packet(f"#{gD} #pkR", [(400, 170), (400, 232), (515, 300), (630, 365)], tcR - 0.1, 0.55)
js.append(f'tl.to("#{gD} .wd",{{rotationY:-5,duration:{T["daas"] - tcR - 0.4:.2f},ease:"sine.inOut"}},{tcR:.4f});')
gone(f"#{gD}", T["daas"] - 0.25)

# E · "DaaS": palabra enorme en el centro y monedas que la ORBITAN en 3D (pasan por detrás y por delante) (morado)
bgs(T["daas"], T["por"], PUR)
gE = nid("g")
DS = round(BIGF * 1.3)
R_ = {"16": 560, "9": 330, "45": 330}[FMT]
coins = "".join(f'<div class="coin c{a_}"><i></i></div>' for a_ in (0, 120, 240))
dE = big(f"{gE}a", lets("DaaS", "b"), DS, f"left:0;width:{W}px;text-align:center;top:{round(H * 0.5 - DS * 0.55)}px")
sE = big(f"{gE}s", '<span class="l">modelo de</span> <span class="b">arrendamiento</span>', S2, f"left:0;width:{W}px;text-align:center;top:{round(H * 0.5 + DS * 0.5)}px;letter-spacing:-0.02em")
orb = f'<div class="orb0" style="left:{W // 2}px;top:{round(H * 0.5)}px">{coins}</div>'
w3(gE, T["daas"] + 0.05, T["por"], dE + sE + orb)
camera(f"#{gE} .wd", T["daas"] + 0.05, 1.5, -400, 10, 0)
flip(f"#{gE}a .lt", T["daas"] + 0.15, 0.95, 0.09)
dE_ = T["por"] - T["daas"] - 0.3
NS_ = 36
for a_ in (0, 120, 240):
    kf = []
    for q in range(NS_ + 1):
        u = q / NS_
        e = 2 * u * u if u < 0.5 else 1 - 2 * (1 - u) ** 2
        ph = math.radians(a_ - 40 + 360 * e)
        kf.append(dict(x=round(R_ * math.sin(ph)), z=round(R_ * math.cos(ph))))
    js.append(f'tl.set("#{gE} .c{a_}",{{x:{kf[0]["x"]},z:{kf[0]["z"]},opacity:0}},0);')
    js.append(f'tl.to("#{gE} .c{a_}",{{opacity:1,duration:0.3}},{T["daas"] + 0.2:.4f});')
    js.append(f'tl.to("#{gE} .c{a_}",{{keyframes:{json.dumps(kf[1:])},duration:{dE_:.3f},ease:"none"}},{T["daas"] + 0.2:.4f});')
js.append(f'tl.fromTo("#{gE}s",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.6,ease:"power3.out"}},{T["arrendamiento"] - 0.5:.4f});')
gone(f"#{gE}", T["por"] - 0.25)

# F · "una cuota mensual": 'mensual' enorme y centrado sobre el plano, fila de pagos que se va marcando
gF = nid("g")
FS = BIGF
cx_ = {"16": 0.42, "9": 0.40, "45": 0.40}[FMT]
fa = big(f"{gF}a", lets("Una cuota", "l"), round(FS * 0.30), f"left:0;width:{W}px;text-align:center;top:{round(H * cx_ - FS * 0.2)}px;{SHD}")
fb = big(f"{gF}b", lets("mensual", "b"), FS, f"left:0;width:{W}px;text-align:center;top:{round(H * cx_ + FS * 0.12)}px;{SHD}")
nT = 12
gp = 12 if FMT == "16" else 8
sz_ = min(78, (W - SAFE["l"] - SAFE["r"] - (nT - 1) * gp) // nT)
rowW = nT * sz_ + (nT - 1) * gp
row = "".join(pth(f"M{k * (sz_ + gp)} 0H{k * (sz_ + gp) + sz_}V{sz_}H{k * (sz_ + gp)}Z", 'class="fr"') + pth(f"M{k * (sz_ + gp) + sz_ * .25:.0f} {sz_ * .52:.0f}L{k * (sz_ + gp) + sz_ * .43:.0f} {sz_ * .72:.0f}L{k * (sz_ + gp) + sz_ * .76:.0f} {sz_ * .28:.0f}", 'class="fc"') for k in range(nT))
rdiv = (f'<div id="{gF}r" class="fk" style="left:{(W - rowW) // 2}px;top:{H - SAFE["b"] - sz_ - 10}px;width:{rowW}px;height:{sz_}px"><svg viewBox="0 0 {rowW} {sz_}" width="100%" height="100%" fill="none" stroke="#fff" '
        f'stroke-width="{max(6, sz_ // 8)}" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{row}</svg></div>')
w3(gF, T["cuota"] - 0.15, T["llenar"], fa + fb + rdiv)
camera(f"#{gF} .wd", T["cuota"] - 0.15, 1.1, -220, 9, 5)
flip(f"#{gF}a .lt", T["cuota"] - 0.1, 0.8, 0.04)
flip(f"#{gF}b .lt", T["cuota"] + 0.12, 0.9, 0.055)
draw(f"#{gF} .fr", T["cuota"] + 0.3, 0.5, 0.03)
draw(f"#{gF} .fc", T["cuota"] + 0.8, 0.3, (T["llenar"] - T["cuota"] - 1.9) / nT)
gone(f"#{gF}", T["llenar"] - 0.2)

# H–L · "muchas ventajas": las cuatro tarjetas, cada una con su mini-diagrama (fondo blanco)
tV0 = T["hay1"]
bgs(tV0, tM0, "#fafafa")
HS_ = {"16": 118, "9": 104, "45": 100}[FMT]
hvid = nid("g")
hv = big(f"{hvid}a", lets("Muchas ", "l") + lets("ventajas.", "b"), HS_, f"left:0;width:{W}px;text-align:center;top:{SAFE['t']}px", "#0b0b14")
w3(hvid, tV0 + 0.05, tM0, hv)
els[-1] = els[-1].replace('class="clip w3"', 'class="clip w3 hvx"')
flip(f"#{hvid}a .lt", tV0 + 0.15, 0.85, 0.04)
js.append(f'tl.fromTo("#{hvid}a .b",{{color:"#0b0b14"}},{{color:"#3976ff",duration:0.5,ease:"none"}},{tV0 + 0.8:.4f});')
gone(f"#{hvid}", tM0 - 0.25)
TS, SS = {"16": (35, 24), "9": (32, 23), "45": (30, 22)}[FMT]
GAP = {"16": 24, "9": 28, "45": 24}[FMT]
CH = {"16": 600, "9": 400, "45": 340}[FMT]
CW = (W - SAFE["l"] - SAFE["r"] - ((4 if FMT == "16" else 2) - 1) * GAP) // (4 if FMT == "16" else 2)
VH = {"16": 200, "9": 170, "45": 130}[FMT]            # alto de la foto de la tarjeta (en vertical, más alto para que se vea algo)
CLIPS_C = ["m1", "m2", "m3", "m5"]
cols_ = 4 if FMT == "16" else 2
gx0 = (W - (cols_ * CW + (cols_ - 1) * GAP)) // 2
gy0 = {"16": 300, "9": SAFE["t"] + 190, "45": SAFE["t"] + 130}[FMT]
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
               f'<div style="height:{VH}px;flex:none"></div><div class="mini"><svg viewBox="0 0 400 200" fill="none" stroke="{col}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round">{svg_}</svg></div>'
               f'<div class="bd"><div class="dc" style="border-color:{col}">{icon(ic, 30, 2.6, "", col)}</div><div><b>{ti}</b><i>{su}</i></div></div></div>')
    if ALPHA and not os.environ.get("CARDVID"):
        els.append(f'<div id="{i}v" class="clip" data-start="{tt - 0.05:.4f}" data-duration="{tM0 - tt + 0.05:.4f}" data-track-index="4" style="position:absolute;left:{x + 6}px;top:{y + 6}px;width:{CW - 12}px;height:{VH}px;background:#dfe3ec;border-radius:22px 22px 0 0"></div>')
    else:
        els.append(f'<video id="{i}v" class="clip cvv" src="media/{"" if FMT == "16" else "c_"}{CLIPS_C[k]}.mp4" muted playsinline data-start="{tt - 0.05:.4f}" data-duration="{tM0 - tt + 0.05:.4f}" data-media-start="1.0" data-track-index="4" '
                   f'style="left:{x + 6}px;top:{y + 6}px;width:{CW - 12}px;height:{VH}px;object-fit:cover;border-radius:22px 22px 0 0"></video>')
    clips.append(dict(src=CLIPS_C[k], t=round(tt - 0.05, 4), dur=round(tM0 - tt + 0.05, 4), tin=1.0, scale=100, origin="50% 50%", card=dict(x=x + 6, y=y + 6, w=CW - 12, h=VH)))
    ox_ = f"{CW // 2}px {CH // 2}px"; oxv_ = f"{CW // 2 - 6}px {CH // 2 - 6}px"
    ry0 = round((k - 1.5) * 38)
    for sel_, o_ in ((f"#{i}", ox_), (f"#{i}v", oxv_)):
        js.append(f'tl.fromTo("{sel_}",{{opacity:0,z:-1200,rotationY:{ry0},y:90,transformPerspective:1500,transformOrigin:"{o_}"}},{{opacity:1,z:0,rotationY:0,y:0,duration:0.95,ease:"power3.out"}},{tt - 0.05:.4f});')
        js.append(f'tl.to("{sel_}",{{rotationY:{round(-(k - 1.5) * 5)},duration:{max(tM0 - tt - 1.5, 0.5):.2f},ease:"sine.inOut"}},{tt + 0.9:.4f});')
    js.append(f'tl.to("#{i},#{i}v",{{opacity:0,x:-60,duration:0.3,ease:"power2.in"}},{tM0 - 0.3:.4f});')
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
# ── subtítulos: blancos con trazo negro duro y fino; solo donde ninguna palabra o gráfico ya lo dice ──
caps = []
if CAPS:
    ventanas = [(0.0, T["primera"] - 0.1), (T["tener"], T["hay"])]
    per = {"16": 6, "9": 3, "45": 4}[FMT]
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= per or re.search(r"[?.,;]$", w["text"]):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    for k, c in enumerate(chunks):
        t0 = snap(c[0]["start"] + D)
        t1 = snap(chunks[k + 1][0]["start"] + D) if k + 1 < len(chunks) else END
        if any(a <= t0 < b for a, b in ventanas):
            t1 = min(t1, [b for a, b in ventanas if a <= t0 < b][0])
            if t1 - t0 < 0.15:
                continue
            txt = " ".join(x["text"] for x in c)
            caps.append(f'<div class="clip cap" data-start="{t0:.4f}" data-duration="{t1 - t0 - 0.04:.4f}" data-track-index="5">{txt}</div>')

# ── cámara que flota (solo en la versión completa; en Premiere va como capa de ajuste) ──
POSC = [(0, .5, .5), (1.04, .5141, .5), (1.88, .4958, .487), (2.88, .4908, .4849), (5.04, .4842, .5093), (6.32, .5138, .515), (7.96, .4811, .4963), (9.48, .5217, .5213),
        (12.04, .5, .5), (13.28, .5141, .5), (14.12, .4958, .487), (15.12, .4908, .4849), (17.28, .4842, .5093), (18.56, .5138, .515), (20.2, .4811, .4963), (22.4, .5217, .5213),
        (25.0, .5, .5), (26.04, .5141, .5), (26.88, .4958, .487), (27.88, .4908, .4849), (30.04, .4842, .5093), (31.32, .5138, .515), (32.96, .4811, .4963), (34.48, .5217, .5213), (37.04, .5, .5), (38.28, .5141, .5), (39.12, .4958, .487)]
SCL = [(0, 104), (1.88, 103.5), (3.44, 104.4), (5.44, 103.6), (7.4, 105.2), (10.0, 104.9), (12.04, 104.4), (14.12, 103.5), (15.68, 104.4), (17.68, 103.6), (19.64, 105.2),
       (22.92, 104.9), (25.0, 104), (26.88, 103.5), (28.44, 104.4), (30.44, 103.6), (32.4, 105.2), (35.0, 104.9), (37.04, 104.4), (39.12, 103.5)]
if not ALPHA:
    js.append('gsap.set("#cam",{transformOrigin:"50% 50%"});')
    for (t, x, y), (t2, x2, y2) in zip(POSC, POSC[1:]):
        if t >= END:
            break
        js.append(f'tl.fromTo("#cam",{{x:{(x - .5) * W:.1f},y:{(y - .5) * H:.1f}}},{{x:{(x2 - .5) * W:.1f},y:{(y2 - .5) * H:.1f},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t});')
    for (t, s_), (t2, s2) in zip(SCL, SCL[1:]):
        if t >= END:
            break
        js.append(f'tl.fromTo("#cam",{{scale:{s_ / 100 * 1.012:.4f}}},{{scale:{s2 / 100 * 1.012:.4f},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t});')

LOGO = (PROJ / "assets" / "onescreen-wordmark.svg").read_text(encoding="utf-8-sig")
LOGO = re.sub(r"<\?xml[^>]*\?>", "", LOGO)
LOGO = re.sub(r'\s(id|data-name)="[^"]*"', "", LOGO).replace("<svg ", '<svg class="logo" ', 1)
CAP_FS = {"16": 42, "9": 50, "45": 44}[FMT]
CAP_POS = {"16": f"left:{SAFE['l']}px;right:{SAFE['r']}px;bottom:{SAFE['b']}px", "9": f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:49%", "45": f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:63%"}[FMT]
BG = "transparent" if ALPHA else "#0b0b10"
CSS = f"""
@font-face {{ font-family:'Rubik'; src:url('fonts/Rubik-variable-latin.woff2') format('woff2'); font-weight:300 900; font-display:block; }}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden;background:{BG};font-family:'Rubik',sans-serif}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{BG}}}
#cam{{position:absolute;inset:0;width:{W}px;height:{H}px}}
video{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover}}
.white{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:#fafafa}}
.cw{{position:absolute;left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);text-align:center;color:{ACC};font-family:'Rubik';line-height:1.18;letter-spacing:-0.02em}}
.cl{{display:block}} .cw .b,.tx .b{{font-weight:700}} .cw .l,.tx .l{{font-weight:300}}
.mk{{display:block;overflow:hidden;padding:0.06em 0.08em 0.16em}} .rw{{display:inline-block}}
.tx{{position:absolute;color:#fff;font-family:'Rubik';line-height:1.0;letter-spacing:-0.035em;text-shadow:0 3px 26px rgba(0,0,0,.5),0 1px 3px rgba(0,0,0,.25)}}
.w3{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;perspective:1500px;perspective-origin:50% 50%}} .wd{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-style:preserve-3d}} .ttl{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-style:preserve-3d}} .fk{{position:absolute}} .big{{position:absolute;font-family:'Rubik';line-height:0.9;letter-spacing:-0.045em;white-space:nowrap;transform-style:preserve-3d}} .big .b{{font-weight:700}} .big .l{{font-weight:300}} .lw{{display:inline-block}} .orb0{{position:absolute;width:0;height:0;transform-style:preserve-3d;transform:rotateX(-16deg)}} .orb{{position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d}} .cp{{position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d}} .coin{{position:absolute;left:-80px;top:-80px;width:160px;height:160px;border-radius:50%;background:#3976ff;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 8px #fff inset}} .coin i{{display:block;width:78px;height:78px;border-radius:50%;border:12px solid #fff;box-sizing:border-box}} .ln{{display:block}} .gfx{{position:absolute}} .nd{{transform-box:fill-box;transform-origin:center}} .bar{{transform-box:fill-box}} .fill1{{transform-box:fill-box}} .lb{{font:700 58px Rubik;fill:#fff;stroke:none;letter-spacing:-0.02em}} .cd{{position:absolute;background:#fff;border:6px solid;border-radius:28px;display:flex;flex-direction:column;overflow:hidden;box-sizing:border-box}} .cd .mini{{flex:1;min-height:0;padding:14px 18px 0}} .cd .mini svg{{width:100%;height:100%;overflow:visible}} .cd .bd{{display:flex;gap:14px;align-items:center;padding:8px 20px 20px;{"flex-direction:column;align-items:flex-start;" if FMT == "16" else ""}}} .cd .dc{{flex:none;width:56px;height:56px;border-radius:50%;border:5px solid;display:flex;align-items:center;justify-content:center}} .cd .dc svg{{margin:0 !important;vertical-align:0 !important}} .cd b{{font-family:'Rubik';font-weight:700;font-size:{TS}px;letter-spacing:-0.02em;color:#0b0b14;line-height:1.05;display:block}} .cd i{{font-style:normal;font-family:'Rubik';font-weight:400;font-size:{SS}px;color:#555;display:block;margin-top:4px}} 
.icb{{position:absolute;filter:none}} .ic{{overflow:visible;fill:none;stroke-linecap:round;stroke-linejoin:round}} .ic path{{stroke-dasharray:1 2;stroke-dashoffset:0}} .ic{{display:inline-block;filter:none}}
.ulb{{position:absolute;height:{max(6, round(S1 * 0.05))}px;background:#fff;border-radius:3px;box-shadow:0 2px 14px rgba(0,0,0,.4)}}
.lgo .logo{{height:{round(S1 * 0.62)}px;width:auto;display:block}} .lgo .logo path,.lgo .logo polygon,.lgo .logo rect,.lgo .logo circle{{fill:#fff!important}}
.cap{{position:absolute;{CAP_POS};text-align:center;font-family:'Rubik';font-weight:500;font-size:{CAP_FS}px;line-height:1.15;color:#fff;-webkit-text-stroke:{max(3, round(CAP_FS * 0.11))}px #000;paint-order:stroke fill;text-shadow:none;pointer-events:none}}
"""
body = chr(10).join("    " + e for e in els).replace("@@LOGO@@", LOGO)
html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8" /><style>{CSS}</style></head>
<body>
<div id="stage" data-composition-id="rental3" data-start="0" data-duration="{END:.4f}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
  <div id="cam">
{body}
  </div>
  {chr(10).join('  ' + c for c in caps)}
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    window.gsap.defaults({{ lazy: false }});
    const tl = window.gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in js)}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["rental3"] = tl;
  }})();
  </script>
</div>
</body></html>
"""
PROJ.mkdir(parents=True, exist_ok=True)
(PROJ / "index.html").write_text(html, encoding="utf-8")
ev = {k: v for k, v in T.items()}
whites = [(T["hay"], "dos"), (T["hay1"], "muchas"), (tM0, "quieres")]
json.dump(dict(END_SCENE=END, clips=clips, events=ev, whites=whites), open(PROJ / ("plan_alpha.json" if ALPHA else "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", FMT, "ALPHA" if ALPHA else "completo", "escena", END, "planos", len(clips))
