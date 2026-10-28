"""Video corporativo OneScreen (guion C aprobado por Cris, 25-oct-2026): salas de reuniones, planos del Directorio de video.
Mismo método y estilo del Rental v3 (texto sobre el plano sin contenedores, diagramas que representan lo que dice la voz,
subtítulos solo donde nada más lo dice) y la regla nueva de Cris: corte promedio de 1,2 a 2 s, muchos planos.
Uso: FMT=16|9|45 python build_corp.py   (antes: python cortes.py)"""
import json, os, re
from pathlib import Path

FMT = os.environ.get("FMT", "16")
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[FMT]
PROJ = Path(os.environ.get("PROJ") or f"D:/OneScreen/Contenido/2026/10. Octubre/Corporativo salas de reuniones/Proyecto/v_{FMT}")
SCRIBE = r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-25_corporativo/scribe_v_hyv3_0_0.json"
FPS, D, LEAD = 24, 0.10, 0.10
ACC, PUR, INK = "#3976ff", "#7d00ba", "#1a1a1a"
SAFE = {"16": dict(l=270, r=270, t=150, b=170), "9": dict(l=150, r=150, t=340, b=550), "45": dict(l=150, r=150, t=210, b=310)}[FMT]
S1 = {"16": 150, "9": 118, "45": 112}[FMT]          # texto grande sobre el plano
S2 = round(S1 * 0.46)

words = [w for w in json.load(open(SCRIBE, encoding="utf-8"))["words"] if w.get("type") == "word"]


def norm(t):
    """sin signos ni tildes: Scribe a veces escribe Guru/gurú"""
    return re.sub(r"[¿?¡!.,;:]", "", t).lower().translate(str.maketrans("áéíóú", "aeiou"))


def snap(t):
    return round(t * FPS) / FPS


def EV(word, n=0):
    """la palabra suena en start + D; el evento cae LEAD antes (2-3 cuadros)"""
    k = [w for w in words if norm(w["text"]) == norm(word)]
    return snap(k[n]["start"] + D - LEAD)


END = snap(words[-1]["end"] + D + 1.6)
els, js, clips = [], [], []
cnt = [0]


def nid(p):
    cnt[0] += 1
    return f"{p}{cnt[0]:02d}"


def gone(sel, t, d=0.3, x=-50):
    js.append(f'tl.to("{sel}",{{opacity:0,x:{x},duration:{d},ease:"power2.in"}},{t:.4f});')


def vid(src, t, t1, scale=100, origin="50% 50%"):
    clips.append(dict(src=src, t=round(t, 4), dur=round(t1 - t, 4), scale=scale))
    i = nid("v")
    els.append(f'<video id="{i}" class="clip" src="media/{src}.mp4" muted playsinline data-start="{t:.4f}" data-duration="{t1 - t:.4f}" data-media-start="0" data-track-index="1" '
               f'style="transform-origin:{origin};transform:scale({scale / 100:.3f})"></video>')


POS = {"16": dict(bl=f"left:{SAFE['l']}px;bottom:{SAFE['b'] + 40}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);text-align:center"),
       "9": dict(bl=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 30}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:60%;transform:translateY(-50%);text-align:center"),
       "45": dict(bl=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 20}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:60%;transform:translateY(-50%);text-align:center")}[FMT]


def tx(t0, t1, lines, pos="bl", extra=""):
    """texto suelto sobre el plano; cada palabra sube de abajo hacia arriba con transparencia (>=1 s, power3.out)"""
    i = nid("t")
    body = "".join(f'<div class="ln" style="font-size:{sz}px">' + " ".join(f'<span class="mk"><span class="lw {c}">{w}</span></span>' for w in h.split(" ")) + "</div>" for h, sz, c in lines)
    els.append(f'<div id="{i}" class="clip tx" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3" style="{POS[pos]};{extra}">{body}</div>')
    js.append(f'tl.fromTo("#{i} .lw",{{yPercent:60,opacity:0}},{{yPercent:0,opacity:1,duration:1.0,ease:"power3.out",stagger:0.12}},{t0:.4f});')
    return i


def bgs(t0, t1, color):
    i = nid("b")
    els.append(f'<div id="{i}" class="clip full" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="2" style="background:{color}"></div>')
    js.append(f'tl.fromTo("#{i}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"power3.inOut"}},{t0:.4f});')
    return i


def pth(d, extra=""):
    return f'<path d="{d}" pathLength="1" style="stroke-dasharray:1 2;stroke-dashoffset:1" {extra}/>'


def draw(sel, t, d=0.6, stag=0.08):
    js.append(f'tl.fromTo("{sel}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{d},ease:"power2.inOut",stagger:{stag}}},{t:.4f});')


def pop(sel, t, d=0.45, frm=0.5, stag=0.0):
    js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:{frm}}},{{opacity:1,scale:1,duration:{d},ease:"back.out(1.7)",stagger:{stag}}},{t:.4f});')


# ── montaje: cada corte cae 2-3 cuadros antes de la palabra; zigzag 100 % / cerrado ─────────────
t_una1 = EV("una", 1)
CUTS = [("102648", 0.0), ("101968", EV("depende")), ("105957", EV("una", 0)), ("102227", EV("micrófonos")), ("102731", EV("y", 0)),
        ("101944", EV("todos", 0)), ("101421", EV("esto")), (None, t_una1), ("101939", EV("compartes")), ("101927", EV("cámara", 1)),  ("101831", EV("y", 2)), (None, EV("transcrita")), ("101875", EV("si", 1)), ("102711", EV("el")),
        ("101042", EV("conecta")), ("106200", EV("ingenieros")), ("101799", EV("solicita"))]
ZOOM = {"16": 122, "9": 115, "45": 118}[FMT]
for k, (src, t) in enumerate(CUTS):
    t1 = CUTS[k + 1][1] if k + 1 < len(CUTS) else END
    if src:
        vid(src, t, t1 + (0.5 if CUTS[k + 1:k + 2] and CUTS[k + 1][0] is None else 0), 100 if k % 2 == 0 else ZOOM)

# 1-4 · la lista de equipos: una palabra grande por plano, con su número
LIST = [("Un", "proyector", "proyector", 0, EV("una", 0)), ("Una", "cámara web", "cámara", 0, EV("micrófonos")),
        ("", "Micrófonos", "micrófonos", 0, EV("y", 0)), ("Y cables", "por todos lados", "cables", 0, EV("esto"))]
for n, (a, b, wd, idx, t1) in enumerate(LIST):
    t0 = EV(wd, idx)
    lines = ([(a, S2 * 1.2, "l")] if a else []) + [(b, S1, "b")]
    i = tx(t0, t1, lines, "bl")
    els[-1] = els[-1].replace('<div class="ln"', f'<div class="nm"><span class="mk"><span class="lw">0{n + 1}</span></span></div><div class="ln"', 1)

# 7 · "Una OneScreen los reemplaza a todos": los cuatro equipos se juntan en una sola pantalla (fondo blanco)
t7a, t7b = t_una1, EV("compartes")
bgs(t7a - 0.35, t7b, "#fafafa")          # el barrido termina justo en "Una OneScreen"
g7 = nid("g")
GW = {"16": 1100, "9": 780, "45": 780}[FMT]
GH = round(GW * 0.62)
GX, GY = (W - GW) // 2, {"16": (H - GH) // 2 + 30, "9": round(H * 0.5 - GH / 2), "45": round(H * 0.5 - GH / 2) + 20}[FMT]
ICX = [125, 375, 625, 875]
ICONS = [  # proyector, cámara web, micrófono, cable (trazos de línea, ~7 % del ícono)
    pth("M-70 -30H70V40H-70Z") + '<circle cx="30" cy="5" r="22" pathLength="1" style="stroke-dasharray:1 2;stroke-dashoffset:1"/>' + pth("M-50 40V58M50 40V58"),
    pth("M-70 -28H70V28H-70Z") + '<circle cx="0" cy="0" r="16" pathLength="1" style="stroke-dasharray:1 2;stroke-dashoffset:1"/>' + pth("M-30 28L-40 60H40L30 28"),
    pth("M-22 -60H22V10H-22Z") + pth("M-46 -6C-46 30 46 30 46 -6") + pth("M0 30V62M-28 62H28"),
    pth("M-70 50C-70 -20 -10 -20 0 0C10 20 70 20 70 -50") + pth("M-84 50H-56M56 -50H84"),
]
ics = "".join(f'<g class="dv" transform="translate({x} 300) scale(1.4)"><g class="dvi">{ic}</g></g>' for x, ic in zip(ICX, ICONS))
scr = pth("M300 70H700V360H300Z", 'class="sc"') + pth("M500 360V420M420 420H580", 'class="sc"')
els.append(f'<div id="{g7}" class="clip gfx" data-start="{t7a:.4f}" data-duration="{t7b - t7a:.4f}" data-track-index="3" style="left:{GX}px;top:{GY}px;width:{GW}px;height:{GH}px">'
           f'<svg viewBox="0 0 1000 620" width="100%" height="100%" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{ics}{scr}</svg>'
           f'<div class="lgw" style="left:{round(GW * 0.33)}px;top:{round(GH * 0.29)}px;width:{round(GW * 0.34)}px">@@LOGOC@@</div></div>')
LBL = {"16": 66, "9": 54, "45": 52}[FMT]
lb7 = nid("t")
els.append(f'<div id="{lb7}" class="clip tx ink" data-start="{t7a:.4f}" data-duration="{t7b - t7a:.4f}" data-track-index="3" style="left:0;width:{W}px;top:{GY + GH + 10}px;text-align:center;font-size:{LBL}px">'
           f'<span class="mk"><span class="lw l">Los reemplaza</span></span> <span class="mk"><span class="lw b">a todos.</span></span></div>')
draw(f"#{g7} .dvi path,#{g7} .dvi circle", t7a + 0.1, 0.45, 0.03)
pop(f"#{g7} .dv", t7a + 0.05, 0.4, 0.5, 0.06)
t_rem = EV("reemplaza")
for k, x in enumerate(ICX):                       # cada equipo vuela al centro de la pantalla y se apaga
    js.append(f'tl.to("#{g7} .dv:nth-child({k + 1})",{{x:{500 - x},y:-85,scale:0.25,opacity:0,duration:0.55,ease:"power3.in"}},{t_rem + 0.06 * k:.4f});')
draw(f"#{g7} .sc", t_rem + 0.35, 0.55, 0.12)
js.append(f'tl.fromTo("#{g7} .lgw",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},{EV("todos", 1) - 0.3:.4f});')
js.append(f'tl.fromTo("#{lb7} .lw",{{yPercent:60,opacity:0}},{{yPercent:0,opacity:1,duration:1.0,ease:"power3.out",stagger:0.15}},{t_rem:.4f});')
logo_top = tx(t7a, t_rem - 0.1, [("@@LOGOI@@", S1, "lgi")], "c", f"top:{SAFE['t'] + 20}px;transform:none")
els[-1] = els[-1].replace('class="clip tx"', 'class="clip tx ink"')
js.append(f'tl.to("#{logo_top}",{{opacity:0,duration:0.3,ease:"power2.in"}},{t_rem - 0.35:.4f});')

# 8 · "Compartes pantalla sin cables"
tx(EV("sin"), EV("cámara", 1), [("Sin", S2 * 1.2, "l"), ("cables", S1, "b")], "bl")
# 9-10 · "Cámara y audio integrados"
tx(EV("cámara", 1), EV("y", 2), [("Cámara y audio", S2 * 1.2, "l"), ("integrados", S1, "b")], "bl")

# 11b · "termina transcrita, con su resumen": la onda de voz se vuelve texto y el texto se resume (fondo azul)
tT0, tT1 = EV("transcrita"), EV("si", 1)
bgs(tT0 - 0.35, tT1, ACC)
gT = nid("g")
TW = {"16": 1300, "9": 820, "45": 820}[FMT]
TH = round(TW * 0.42)
TX, TY = (W - TW) // 2, (H - TH) // 2 + (40 if FMT == "16" else 0)
bars = "".join(f'<rect class="wv" x="{20 + j * 34}" y="{210 - h}" width="18" height="{2 * h}" rx="9" fill="#fff" stroke="none"/>' for j, h in enumerate([30, 70, 45, 110, 80, 130, 60, 95, 40, 75, 25]))
lines_ = "".join(pth(f"M560 {90 + j * 60}H{560 + L}", 'class="tl"') for j, L in enumerate([400, 330, 420, 260, 380]))
summ = (f'<g class="sm"><rect x="560" y="70" width="440" height="280" rx="34" fill="#fff" stroke="none"/>'
        + "".join(f'<circle cx="615" cy="{150 + j * 70}" r="12" fill="{ACC}" stroke="none"/><rect x="650" y="{140 + j * 70}" width="{w_}" height="20" rx="10" fill="{ACC}" stroke="none" opacity=".85"/>' for j, w_ in enumerate([290, 220, 260]))
        + '</g>')
pk = "".join(f'<circle class="pk" cx="400" cy="210" r="11" fill="#fff" stroke="none" opacity="0"/>' for _ in range(3))
els.append(f'<div id="{gT}" class="clip gfx" data-start="{tT0:.4f}" data-duration="{tT1 - tT0:.4f}" data-track-index="3" style="left:{TX}px;top:{TY}px;width:{TW}px;height:{TH}px">'
           f'<svg viewBox="0 0 1000 420" width="100%" height="100%" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" style="overflow:visible">{bars}{lines_}{summ}{pk}</svg></div>')
js.append(f'tl.fromTo("#{gT} .wv",{{scaleY:0.1,transformOrigin:"50% 50%"}},{{scaleY:1,duration:0.35,ease:"back.out(2)",stagger:0.03}},{tT0 + 0.05:.4f});')
js.append(f'tl.to("#{gT} .wv",{{scaleY:0.35,duration:0.18,ease:"sine.inOut",stagger:{{each:0.04,yoyo:true,repeat:5}}}},{tT0 + 0.45:.4f});')
for j in range(3):                                # paquetes de luz: de la voz al texto
    js.append(f'tl.fromTo("#{gT} .pk:nth-of-type({j + 1})",{{attr:{{cx:400,cy:210}},opacity:0}},{{attr:{{cx:560,cy:{90 + j * 120}}},opacity:1,duration:0.35,ease:"power2.in"}},{tT0 + 0.3 + j * 0.12:.4f});')
    js.append(f'tl.to("#{gT} .pk:nth-of-type({j + 1})",{{opacity:0,duration:0.1}},{tT0 + 0.65 + j * 0.12:.4f});')
draw(f"#{gT} .tl", tT0 + 0.4, 0.4, 0.08)
for g_, t_ in ((gT, tT0), (g7, t7a)):            # el gráfico aparece cuando el barrido de fondo ya cubrió el plano
    js.append(f'tl.fromTo("#{g_}",{{opacity:0}},{{opacity:1,duration:0.15,ease:"none"}},{t_ + 0.05:.4f});')
t_res = EV("resumen")
js.append(f'tl.to("#{gT} .tl",{{opacity:0,duration:0.25}},{t_res - 0.05:.4f});')
js.append(f'tl.fromTo("#{gT} .sm",{{opacity:0,scale:0.7,transformOrigin:"780px 210px"}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.6)"}},{t_res:.4f});')
LT = {"16": 76, "9": 64, "45": 60}[FMT]
lT = nid("t")
els.append(f'<div id="{lT}" class="clip tx" data-start="{tT0:.4f}" data-duration="{tT1 - tT0:.4f}" data-track-index="3" style="left:0;width:{W}px;top:{TY - LT * 1.9:.0f}px;text-align:center;font-size:{LT}px">'
           f'<span class="mk"><span class="lw b k1">Transcrita</span></span><span class="mk"><span class="lw l k2">,&nbsp;con su&nbsp;</span></span><span class="mk"><span class="lw b k2">resumen.</span></span></div>')
js.append(f'tl.fromTo("#{lT} .k1",{{yPercent:60,opacity:0}},{{yPercent:0,opacity:1,duration:1.0,ease:"power3.out"}},{tT0:.4f});')
js.append(f'tl.fromTo("#{lT} .k2",{{yPercent:60,opacity:0}},{{yPercent:0,opacity:1,duration:1.0,ease:"power3.out",stagger:0.12}},{EV("con") :.4f});')

# 13 · "el botón Gurú": toque con ondas sobre el plano + palabra
tG0, tG1 = EV("gurú"), EV("conecta")
tx(EV("botón"), tG1, [("El botón", S2 * 1.2, "l"), ("Gurú", S1, "b")], "bl")
# 15 · "ingenieros de OneScreen": texto + logo (cada vez que se nombra la marca)
tx(EV("ingenieros"), EV("solicita"), [("Ingenieros de", S2 * 1.2, "l"), ("@@LOGOW@@", S1, "lgi")], "bl")
# 16 · CTA
tC = EV("solicita")
tx(tC, END, [("Solicita tu", S2 * 1.5, "l"), ("demo", S1 * 1.25, "b"), ("onescreenlatam.com", S2 * 0.9, "l")], "c")

# ── subtítulos: solo donde ningún texto o gráfico lo dice ────────────────────────────────────────
caps = []
VENT = [(0.0, EV("proyector")), (EV("esto"), t_una1 - 0.3), (EV("compartes"), EV("sin")), (EV("y", 2), tT0 - 0.3), (EV("si", 1), EV("el")), (tG1, EV("ingenieros"))]
per = {"16": 6, "9": 3, "45": 4}[FMT]
for a, b in VENT:
    ws = [w for w in words if a <= snap(w["start"] + D - LEAD) < b]
    ch = [ws[i:i + per] for i in range(0, len(ws), per)]
    for k, c in enumerate(ch):
        t0 = max(a, snap(c[0]["start"] + D - LEAD))
        t1 = min(b, snap(ch[k + 1][0]["start"] + D - LEAD)) if k + 1 < len(ch) else b
        if t1 - t0 > 0.2:
            caps.append(f'<div class="clip cap" data-start="{t0:.4f}" data-duration="{t1 - t0 - 0.04:.4f}" data-track-index="5">{" ".join(x["text"].rstrip(",.") for x in c)}</div>')

# ── cámara que flota (deriva suave, sin "respirar" en bucle) ───────────────────────────────────
js.append('gsap.set("#cam",{transformOrigin:"50% 50%"});')
pts = [(0, 0, 0, 1.03), (5.5, -0.012, 0.008, 1.045), (11, 0.01, -0.01, 1.035), (16.5, -0.008, 0.006, 1.05), (END, 0.006, -0.004, 1.04)]
js.append(f'tl.set("#cam",{{x:0,y:0,scale:{pts[0][3]}}},0);')
for (t, x, y, s), (t2, x2, y2, s2) in zip(pts, pts[1:]):
    js.append(f'tl.to("#cam",{{x:{x2 * W:.1f},y:{y2 * H:.1f},scale:{s2},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t});')

LOGO = (PROJ / "assets" / "onescreen-wordmark.svg").read_text(encoding="utf-8-sig")
LOGO = re.sub(r"<\?xml[^>]*\?>", "", LOGO)
LOGO = re.sub(r'\s(id|data-name)="[^"]*"', "", LOGO).replace("<svg ", '<svg class="logo" ', 1)
CAP_FS = {"16": 42, "9": 50, "45": 44}[FMT]
CAP_POS = {"16": f"left:{SAFE['l']}px;right:{SAFE['r']}px;bottom:{SAFE['b']}px", "9": f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:49%", "45": f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:63%"}[FMT]
CSS = f"""
@font-face {{ font-family:'Rubik'; src:url('fonts/Rubik-variable-latin.woff2') format('woff2'); font-weight:300 900; font-display:block; }}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10;font-family:'Rubik',sans-serif}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10}}
#cam{{position:absolute;inset:0;width:{W}px;height:{H}px}}
video{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover}}
.full{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}
.tx{{position:absolute;color:#fff;font-family:'Rubik';line-height:1.0;letter-spacing:-0.035em;text-shadow:0 3px 26px rgba(0,0,0,.5),0 1px 3px rgba(0,0,0,.25)}}
.tx.ink{{color:{INK};text-shadow:none}}
.ln{{display:block}} .mk{{display:inline-block;overflow:hidden;padding:0.06em 0.04em 0.14em;vertical-align:bottom}} .lw{{display:inline-block}} .b{{font-weight:700}} .l{{font-weight:300}}
.nm{{font-size:{round(S1 * 0.22)}px;font-weight:600;letter-spacing:0.08em;opacity:.85;margin-bottom:0.4em}}
.gfx{{position:absolute}} .dv,.dvi{{transform-box:fill-box;transform-origin:center}} .wv{{transform-box:fill-box}} .sm{{transform-box:view-box}}
.lgw{{position:absolute;color:{ACC}}} .lgw .logo{{width:100%;height:auto;display:block}}
.lgi .logo{{height:0.62em;width:auto;display:block;margin-top:0.12em}} .tx .lgi{{color:#fff}} .tx.ink .lgi{{color:{INK}}}
.cap{{position:absolute;{CAP_POS};text-align:center;font-family:'Rubik';font-weight:500;font-size:{CAP_FS}px;line-height:1.15;color:#fff;-webkit-text-stroke:{max(3, round(CAP_FS * 0.11))}px #000;paint-order:stroke fill;text-shadow:none;pointer-events:none}}
"""
body = chr(10).join("    " + e for e in els)
for k in ("@@LOGOC@@", "@@LOGOI@@", "@@LOGOW@@"):
    body = body.replace(k, LOGO)
html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8" /><style>{CSS}</style></head>
<body>
<div id="stage" data-composition-id="corporativo" data-start="0" data-duration="{END:.4f}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
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
    window.__timelines["corporativo"] = tl;
  }})();
  </script>
</div>
</body></html>
"""
PROJ.mkdir(parents=True, exist_ok=True)
(PROJ / "index.html").write_text(html, encoding="utf-8")
ev = {"una1": t_una1, "reemplaza": t_rem, "transcrita": tT0, "resumen": t_res, "gurú": tG0, "solicita": tC, "cuts": [c[1] for c in CUTS]}
json.dump(dict(END_SCENE=END, clips=clips, events=ev), open(PROJ / "plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dur = [b - a for a, b in zip([c[1] for c in CUTS], [c[1] for c in CUTS[1:]] + [END])]
print("ok", FMT, "escena", END, "cortes", len(CUTS), "promedio", round(sum(dur) / len(dur), 2), "min", round(min(dur), 2), "max", round(max(dur), 2))
