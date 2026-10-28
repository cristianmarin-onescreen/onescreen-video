"""Video OneScreen Rental / DaaS (arrendar vs comprar) — mismo método que QuizWiz+Scrybe v2:
cortes 0,10 s antes de cada palabra, escenas de pantalla completa estilo Flota IA, planos de casos de éxito coloreados, cámara que flota.
Uso: FMT=16|9|45 CAPS=1|0 python build_rental.py"""
import json, os, re
from pathlib import Path

FMT = os.environ.get("FMT", "16")
CAPS = os.environ.get("CAPS", "1") == "1"
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[FMT]
PROJ = Path(f"D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_{FMT}")
SCRIBE = os.environ.get("SCRIBE", r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-21_rental_daas/scribe_v_rv_1.json")
CLIPS = json.load(open(Path(__file__).parent / "rental_clips.json", encoding="utf-8"))   # {"r1": {"len": 4.0, "fx": 0.5}, ...}
FPS = 24
D = 0.10
LEAD = 0.10
INK, ACC, PUR, MUT = "#0b0b14", "#3976ff", "#7d00ba", "#9a9aae"

words = [w for w in json.load(open(SCRIBE, encoding="utf-8"))["words"] if w.get("type") == "word"]


def norm(t):
    return re.sub(r"[¿?¡!.,;:]", "", t).lower()


def snap(t):
    return round(t * FPS) / FPS


def EV(word, n=0):
    k = [w for w in words if norm(w["text"]) == word]
    return snap(k[n]["start"] + D - LEAD)


END_SCENE = snap(words[-1]["end"] + D + 1.1)

# ── línea de tiempo ──────────────────────────────────────────────────────────
SEG = []


def seg(t, kind, src, tin=0.0, scale=100, origin="50% 50%"):
    SEG.append(dict(t=t, kind=kind, src=src, tin=tin, scale=scale, origin=origin))


seg(0.0, "vid", "r1", 0.0, 100, CLIPS["r1"].get("o", "50% 50%"))                  # "Hoy quiero que hablemos sobre tu primera aula digital"
seg(EV("tener"), "vid", "r2", 0.0, 144, CLIPS["r2"].get("o", "50% 50%"))          # "tener tu propia pantalla interactiva"
seg(EV("para"), "vid", "r3", 0.0, 100, CLIPS["r3"].get("o", "50% 50%"))           # "Para tener tu propia OneScreen"
seg(EV("hay"), "white", "paths")                                                   # "hay dos caminos" ... comprar ... "O segundo"
seg(EV("daas"), "white", "daas")
seg(EV("por"), "white", "cuota")                                                   # cuota mensual ... llenar toda tu institución
seg(EV("hay", 1), "vid", "r4", 0.0, 144, CLIPS["r4"].get("o", "50% 50%"))         # "Hay muchas ventajas"
seg(EV("primero", 1), "white", "ventajas")
seg(EV("quieres"), "white", "cta")
for i, s in enumerate(SEG):
    s["t1"] = SEG[i + 1]["t"] if i + 1 < len(SEG) else END_SCENE
    s["dur"] = round(s["t1"] - s["t"], 4)
    if i + 1 < len(SEG) and SEG[i + 1]["kind"] == "white":
        s["dur"] = round(s["dur"] + 0.6, 4)
    if s["src"] in CLIPS and s["tin"] + s["dur"] > CLIPS[s["src"]]["len"] + 0.01:
        print("AVISO: se acaba la fuente", s["src"], s["tin"], s["dur"])

els, js = [], []


def mask_rise(sel, t, d=0.7, stag=0.06):
    js.append(f'tl.fromTo("{sel}",{{yPercent:110,opacity:0}},{{yPercent:0,opacity:1,duration:{d},ease:"power4.out",stagger:{stag}}},{t:.4f});')


def out_left(sel, t, d=0.35):
    js.append(f'tl.to("{sel}",{{opacity:0,x:-60,duration:{d},ease:"power2.in"}},{t:.4f});')


def svg_inline(name, cls):
    t = (PROJ / "assets" / name).read_text(encoding="utf-8-sig")
    t = re.sub(r"<\?xml[^>]*\?>", "", t)
    t = re.sub(r'\s(id|data-name)="[^"]*"', "", t)
    return t.replace("<svg ", f'<svg class="{cls}" ', 1)


LOGO = svg_inline("onescreen-wordmark.svg", "logo")

LAY = {"16": dict(HS=118, HY1=100, NY=520, ND=190, HY2=770, M=130, AL="left"),
       "9": dict(HS=92, HY1=270, NY=720, ND=150, HY2=1090, M=80, AL="center"),
       "45": dict(HS=84, HY1=150, NY=520, ND=150, HY2=760, M=80, AL="center")}[FMT]
ICO = {"cart": ["M3 4h2.5l2 10h10l2-7.5H6.5", "M9 19.5a1 1 0 1 0 .01 0", "M17 19.5a1 1 0 1 0 .01 0"],
       "cal": ["M4 6h16v14H4z", "M4 10h16", "M8 3v4", "M16 3v4", "M8 14h3", "M13 14h3"],
       "chat": ["M4 5h16v11H9l-5 4z", "M8 9.5h8", "M8 12.5h5"],
       "mon": ["M3 5h18v12H3z", "M8 21h8", "M12 17v4"],
       "chk": ["M5 12.5l4.5 4.5L19 7"],
       "coin": ["M12 3a9 9 0 1 0 .01 0", "M14.5 8.5c-.6-.8-1.5-1.2-2.5-1.2-1.5 0-2.6.8-2.6 2 0 3 5.3 1.3 5.3 4.2 0 1.2-1.2 2-2.7 2-1.1 0-2.1-.5-2.7-1.4", "M12 5.6v1.7", "M12 16.7v1.7"],
       "refresh": ["M20 12a8 8 0 1 1-2.6-5.9", "M20 4v5h-5"],
       "head": ["M4 14v-2a8 8 0 0 1 16 0v2", "M4 14h3v5H4z", "M17 14h3v5h-3z", "M20 19v1a2 2 0 0 1-2 2h-4"],
       "shield": ["M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z", "M8.5 12l2.5 2.5 4.5-5"],
       "arrow": ["M5 12h14", "M13 6l6 6-6 6"]}


def line_icon(name, size, color, sw=1.7):
    ps = "".join(f'<path d="{p}" pathLength="1"/>' for p in ICO[name])
    return f'<svg class="li" viewBox="0 0 24 24" width="{size}" height="{size}" style="stroke:{color};stroke-width:{sw}">{ps}</svg>'


def sc_head(cid, k, html, y, t, size=None, color=INK, al=None, w=None):
    size = size or LAY["HS"]
    h = (f'<div id="{cid}-h{k}" class="hd" style="left:{LAY["M"]}px;width:{(w or W - 2 * LAY["M"])}px;top:{y}px;font-size:{size}px;color:{color};text-align:{al or LAY["AL"]}">'
         f'<span class="mk"><span class="rw hr">{html}</span></span></div>')
    mask_rise(f"#{cid}-h{k} .hr", t, 0.7)
    return h


def node(cid, k, cx, cy, icon, label, t, color=ACC, nd=None, sub=None):
    ND = nd or LAY["ND"]
    h = (f'<div id="{cid}-n{k}" class="nd" style="left:{cx - ND // 2}px;top:{cy - ND // 2}px;width:{ND}px;height:{ND}px;border-color:{color}">{line_icon(icon, round(ND * 0.5), color)}</div>'
         f'<div id="{cid}-l{k}" class="nl" style="left:{cx - 230}px;top:{cy + ND // 2 + 18}px;width:460px">{label}</div>')
    js.append(f'tl.fromTo("#{cid}-n{k}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.7)"}},{t:.4f});')
    js.append(f'tl.fromTo("#{cid}-n{k} .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power2.inOut",stagger:0.08}},{t + 0.1:.4f});')
    mask_rise(f"#{cid}-l{k}", t + 0.2, 0.5)
    return h


def conn(cid, k, x1, y1, x2, y2, t, dur=0.8, color=ACC, packet=True):
    h = (f'<svg class="cn" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><line id="{cid}-c{k}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" pathLength="1" style="stroke:{color}"/></svg>')
    js.append(f'tl.fromTo("#{cid}-c{k}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{t:.4f});')
    if packet:
        h += f'<div id="{cid}-p{k}" class="pk" style="left:{x1 - 11}px;top:{y1 - 11}px"></div>'
        js.append(f'tl.fromTo("#{cid}-p{k}",{{x:0,y:0,opacity:0}},{{x:{x2 - x1},y:{y2 - y1},opacity:1,duration:{dur},ease:"power2.inOut"}},{t:.4f});')
        js.append(f'tl.to("#{cid}-p{k}",{{opacity:0,duration:0.2}},{t + dur:.4f});')
    return h


def wipe_in(cid, t):
    js.append(f'tl.fromTo("#{cid}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"power3.inOut"}},{t:.4f});')


def scene_exit(cid, t_end):
    js.append(f'tl.to("#{cid} .hd,#{cid} .nd,#{cid} .nl,#{cid} .cn,#{cid} .pk,#{cid} .cd,#{cid} .gr,#{cid} .tg2",{{opacity:0,x:-60,duration:0.3,ease:"power2.in"}},{t_end - 0.32:.4f});')


# ── escena: dos caminos ──
def scene_paths(cid, t0, t1):
    wipe_in(cid, t0)
    p = []
    cx0 = W // 2
    p.append(sc_head(cid, 1, 'Dos <span class="ac">caminos</span>.', LAY["HY1"], t0 + 0.15, size=round(LAY["HS"] * 1.0)))
    NY = LAY["NY"]
    if FMT == "16":
        c0 = (cx0, 380); a = (cx0 - 520, 690); b = (cx0 + 520, 690)
    else:
        c0 = (cx0, 500 if FMT == "9" else 430); a = (cx0 - 250, 1180 if FMT == "9" else 780); b = (cx0 + 250, 1180 if FMT == "9" else 780)
    p.append(node(cid, 0, c0[0], c0[1], "mon", "Tu OneScreen", t0 + 0.55, ACC, nd=LAY["ND"] - 20))
    tc = EV("caminos")
    ta, tb = EV("primero"), EV("o", 1)
    nd = LAY["ND"] - 10
    p.append(conn(cid, 1, c0[0] - 130, c0[1] + 82, a[0] + 30, a[1] - nd // 2 - 12, ta - 0.2, 0.7))
    p.append(node(cid, 1, a[0], a[1], "cart", "Comprarla", ta + 0.3, ACC, nd=nd))
    p.append(conn(cid, 2, c0[0] + 130, c0[1] + 82, b[0] - 30, b[1] - nd // 2 - 12, tb - 0.2, 0.7, PUR))
    p.append(node(cid, 2, b[0], b[1], "cal", "Arrendarla", tb + 0.3, PUR, nd=nd))
    # contactarnos: burbuja de chat bajo "Comprarla"
    tcn = EV("contactarnos")
    cy2 = a[1] + (nd // 2 + 130 if FMT == "16" else nd // 2 + 110)
    p.append(f'<div id="{cid}-ct" class="cd" style="left:{a[0] - 200}px;top:{cy2 - 32}px;width:400px;color:{ACC}">{line_icon("chat", 46, ACC, 2)}<span>Contáctanos</span></div>')
    js.append(f'tl.fromTo("#{cid}-ct",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.7)"}},{tcn - 0.1:.4f});')
    js.append(f'tl.fromTo("#{cid}-ct .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut",stagger:0.1}},{tcn:.4f});')
    scene_exit(cid, t1)
    return "".join(p)


def scene_daas(cid, t0, t1):
    wipe_in(cid, t0)
    p = []
    big = {"16": 300, "9": 250, "45": 230}[FMT]
    p.append(f'<div id="{cid}-b" class="hd bigd" style="left:0;width:{W}px;top:{round(H * (0.27 if FMT == "16" else 0.2))}px;font-size:{big}px;color:{PUR};text-align:center"><span class="mk"><span class="rw hr dm2">DaaS<span class="ul2" id="{cid}-u"></span></span></span></div>')
    mask_rise(f"#{cid}-b .hr", t0 + 0.15, 0.8)
    js.append(f'tl.fromTo("#{cid}-u",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},{t0 + 0.7:.4f});')
    ta = EV("arrendamiento")
    p.append(sc_head(cid, 1, 'nuestro modelo de <span class="ac">arrendamiento.</span>', round(H * (0.62 if FMT == "16" else 0.5)), ta - 0.5, size=round(LAY["HS"] * 0.8), al="center", w=W - 2 * LAY["M"]))
    scene_exit(cid, t1)
    return "".join(p)


def scene_cuota(cid, t0, t1):
    wipe_in(cid, t0)
    p = []
    p.append(sc_head(cid, 1, 'Una cuota <span class="ac">mensual</span>, accesible.', LAY["HY1"], t0 + 0.15, size=round(LAY["HS"] * 0.9)))
    ncx = W // 2
    nyy = {"16": 560, "9": 640, "45": 480}[FMT]
    p.append(node(cid, 5, ncx, nyy, "cal", "Cada mes", t0 + 0.5, PUR, nd=LAY["ND"] + 10))
    js.append(f'tl.to("#{cid}-n5,#{cid}-l5",{{opacity:0,scale:0.6,duration:0.35,ease:"power2.in"}},{EV("llenar") - 0.2:.4f});')
    # cuadrícula de pantallas que se llena
    tl_ = EV("llenar"); tp = EV("pantallas")
    cols, rows = (6, 3) if FMT == "16" else (4, 4) if FMT == "9" else (4, 3)
    cell = {"16": 190, "9": 170, "45": 170}[FMT]
    gw, gh = cols * cell, rows * (cell * 0.72)
    gx0 = (W - gw) / 2
    gy0 = {"16": 340, "9": 1040, "45": 620}[FMT]
    cells = []
    for r in range(rows):
        for c in range(cols):
            x = gx0 + c * cell + cell * 0.1; y = gy0 + r * cell * 0.72
            cells.append(f'<div class="gr" style="left:{x:.0f}px;top:{y:.0f}px;width:{cell * 0.8:.0f}px;height:{cell * 0.6:.0f}px">{line_icon("mon", round(cell * 0.46), ACC, 1.6)}</div>')
    p.append(f'<div id="{cid}-g">{"".join(cells)}</div>')
    n = rows * cols
    js.append(f'tl.fromTo("#{cid}-g .gr",{{opacity:0,scale:0.5,y:20}},{{opacity:1,scale:1,y:0,duration:0.45,ease:"back.out(1.7)",stagger:{{each:{(tp - tl_ + 0.5) / n:.4f},from:"center",grid:[{rows},{cols}]}}}},{tl_ - 0.1:.4f});')
    js.append(f'tl.fromTo("#{cid}-g .gr .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut",stagger:{{each:0.01,from:"center"}}}},{tl_:.4f});')
    p.append(sc_head(cid, 2, 'Toda tu <span class="ac">institución</span>.', {"16": 770, "9": 740, "45": 345}[FMT], EV("toda") + 0.1, size=round(LAY["HS"] * (0.72 if FMT == "16" else 0.62))))
    scene_exit(cid, t1)
    return "".join(p)


def scene_ventajas(cid, t0, t1):
    wipe_in(cid, t0)
    p = []
    p.append(sc_head(cid, 1, 'Las <span class="ac">ventajas</span> de arrendar.', LAY["HY1"] - (60 if FMT == "9" else 0), t0 + 0.12, size=round(LAY["HS"] * 0.88)))
    items = [("coin", "Pagas por lo que usas", "Sin comprar de golpe", EV("pagas"), "c1"),
             ("refresh", "Siempre actualizada", "Las últimas actualizaciones", EV("siempre"), "c2"),
             ("head", "Soporte técnico prioritario", "Atención primero", EV("soporte"), "c3"),
             ("shield", "Nosotros nos encargamos", "Si sufre algún daño", EV("si"), "c4")]
    cols = 4 if FMT == "16" else 2
    cw = {"16": 412, "9": 450, "45": 450}[FMT]; vh = {"16": 200, "9": 170, "45": 120}[FMT]; ch = {"16": 510, "9": 420, "45": 340}[FMT]
    gap = 28
    gx0 = (W - (cols * cw + (cols - 1) * gap)) / 2
    gy0 = {"16": 300, "9": 450, "45": 330}[FMT]
    cols_clr = [ACC, ACC, PUR, PUR]
    for i, (ic, ti, su, tt, clip) in enumerate(items):
        x = gx0 + (i % cols) * (cw + gap); y = gy0 + (i // cols) * (ch + gap)
        if FMT == "9":
            y = 450 if i < 2 else 1010
        p.append(f'<div id="{cid}-k{i}" class="cd2 cd" style="left:{x:.0f}px;top:{y:.0f}px;width:{cw}px;height:{ch}px;border-color:{cols_clr[i]};padding-top:{vh + 122}px">'
                 f'<div class="ci" style="border-color:{cols_clr[i]};top:{vh + 14}px">{line_icon(ic, 46, cols_clr[i], 1.8)}</div><b>{ti}</b><i>{su}</i></div>')
        els.append(f'<video id="{cid}-v{i}" class="clip cv" src="media/{clip}.mp4" muted playsinline data-start="{tt - 0.05:.4f}" data-duration="{max(t1 - tt + 0.5, 1):.4f}" data-media-start="0" data-track-index="3" '
                   f'style="left:{x + 5:.0f}px;top:{y + 5:.0f}px;width:{cw - 10}px;height:{vh}px;border-radius:22px 22px 0 0"></video>')
        js.append(f'tl.fromTo("#{cid}-k{i},#{cid}-v{i}",{{opacity:0,y:50,scale:0.88}},{{opacity:1,y:0,scale:1,duration:0.55,ease:"back.out(1.5)"}},{tt - 0.05:.4f});')
        js.append(f'tl.fromTo("#{cid}-k{i} .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power2.inOut",stagger:0.08}},{tt + 0.1:.4f});')
        js.append(f'tl.to("#{cid}-v{i}",{{opacity:0,x:-60,duration:0.3,ease:"power2.in"}},{t1 - 0.32:.4f});')
    scene_exit(cid, t1)
    return "".join(p)


def scene_cta(cid, t0, t1):
    wipe_in(cid, t0)
    p = []
    ty = {"16": 250, "9": 520, "45": 330}[FMT]
    p.append(sc_head(cid, 1, '¿Quieres tu <span class="ac">pantalla</span>?', ty, t0 + 0.15, size=round(LAY["HS"] * 1.3), al="center", w=W - 2 * LAY["M"]))
    tb = EV("pregúntanos") - 0.05
    by = {"16": 500, "9": 1040, "45": 650}[FMT]; bw = {"16": 660, "9": 620, "45": 560}[FMT]
    p.append(f'<div id="{cid}-b" class="bt" style="left:{W // 2 - bw // 2}px;top:{by}px;width:{bw}px">Pregúntanos {line_icon("arrow", 44, "#fff", 2.2)}</div>')
    js.append(f'tl.fromTo("#{cid}-b",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.7)"}},{tb:.4f});')
    js.append(f'tl.fromTo("#{cid}-b .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut",stagger:0.1}},{tb + 0.25:.4f});')
    uy = by + {"16": 175, "9": 190, "45": 150}[FMT]
    p.append(f'<div id="{cid}-u" class="url" style="left:0;width:{W}px;top:{uy}px">onescreenlatam.com/<b>rental</b></div>')
    js.append(f'tl.fromTo("#{cid}-u",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.6,ease:"power3.out"}},{EV("explicamos") - 0.1:.4f});')
    return "".join(p)


SCN = {"paths": scene_paths, "daas": scene_daas, "cuota": scene_cuota, "ventajas": scene_ventajas, "cta": scene_cta}

# ── montaje ──
cnt = 0
for s in SEG:
    cnt += 1
    cid = f"s{cnt:02d}"
    if s["kind"] == "vid":
        els.append(f'<video id="{cid}" class="clip" src="media/{s["src"]}.mp4" muted playsinline data-start="{s["t"]:.4f}" data-duration="{s["dur"]:.4f}" '
                   f'data-media-start="{s["tin"]:.4f}" data-track-index="1" style="object-position:{s["origin"].split()[0]} 50%;transform-origin:{s["origin"]};transform:scale({s["scale"] / 100:.3f})"></video>')
    else:
        body = SCN[s["src"]](cid, s["t"], s["t1"])
        els.append(f'<div id="{cid}" class="clip white scn" data-start="{s["t"]:.4f}" data-duration="{s["dur"]:.4f}" data-track-index="2">{body}</div>')

# titular sobre el primer plano (máscara blanca, como los planos con texto del Flota) + logo oficial cuando se nombra la marca
hy = {"16": round(H * 0.56), "9": round(H * 0.60), "45": round(H * 0.58)}[FMT]
els.append(f'<div id="t1" class="clip ov2" data-start="{EV("primera") - 0.1:.4f}" data-duration="{EV("tener") - EV("primera") + 0.35:.4f}" data-track-index="3" style="top:{hy}px"><span class="mk"><span class="rw bigw">Tu primera <span class="ac2">aula digital</span></span></span></div>')
mask_rise("#t1 .bigw", EV("primera") - 0.1, 0.8)
out_left("#t1 .bigw", EV("tener") + 0.0)
els.append(f'<div id="t2" class="clip ov2" data-start="{EV("onescreen") - 0.1:.4f}" data-duration="1.6" data-track-index="3" style="top:{hy}px"><span class="mk lg2">{LOGO}</span></div>')
mask_rise("#t2 .lg2", EV("onescreen") - 0.1, 0.7)
out_left("#t2 .lg2", EV("onescreen") + 1.1)

# subtítulos
caps_html = []
if CAPS:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 3 or re.search(r"[?.,;]$", w["text"]):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    for k, c in enumerate(chunks):
        t0 = snap(c[0]["start"] + D)
        t1 = snap(chunks[k + 1][0]["start"] + D) if k + 1 < len(chunks) else END_SCENE
        txt = " ".join(x["text"].replace("DaaS", "DaaS") for x in c)
        tm = t0 + 0.05
        blanco = any(sg["kind"] == "white" and sg["t"] - 0.05 <= tm < sg["t1"] for sg in SEG)
        caps_html.append(f'<div class="clip cap{" capd" if blanco else ""}" data-start="{t0:.4f}" data-duration="{max(t1 - t0 - 0.05, 0.2):.4f}" data-track-index="5">{txt}</div>')

# cámara que flota
POS = [(0, .5, .5), (1.04, .5141, .5), (1.88, .4958, .487), (2.88, .4908, .4849), (5.04, .4842, .5093), (6.32, .5138, .515), (7.96, .4811, .4963), (9.48, .5217, .5213),
       (12.04, .5, .5), (13.28, .5141, .5), (14.12, .4958, .487), (15.12, .4908, .4849), (17.28, .4842, .5093), (18.56, .5138, .515), (20.2, .4811, .4963), (22.4, .5217, .5213),
       (25.0, .5, .5), (26.04, .5141, .5), (26.88, .4958, .487), (27.88, .4908, .4849), (30.04, .4842, .5093), (31.32, .5138, .515), (32.96, .4811, .4963), (34.48, .5217, .5213),
       (37.04, .5, .5), (38.28, .5141, .5), (39.12, .4958, .487)]
SCL = [(0, 104), (1.88, 103.5), (3.44, 104.4), (5.44, 103.6), (7.4, 105.2), (10.0, 104.9), (12.04, 104.4), (14.12, 103.5), (15.68, 104.4), (17.68, 103.6), (19.64, 105.2),
       (22.92, 104.9), (25.0, 104), (26.88, 103.5), (28.44, 104.4), (30.44, 103.6), (32.4, 105.2), (35.0, 104.9), (37.04, 104.4), (39.12, 103.5)]
js.append('gsap.set("#cam",{transformOrigin:"50% 50%"});')
for (t, x, y), (t2, x2, y2) in zip(POS, POS[1:]):
    if t >= END_SCENE:
        break
    js.append(f'tl.fromTo("#cam",{{x:{(x - .5) * W:.1f},y:{(y - .5) * H:.1f}}},{{x:{(x2 - .5) * W:.1f},y:{(y2 - .5) * H:.1f},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t});')
for (t, s_), (t2, s2) in zip(SCL, SCL[1:]):
    if t >= END_SCENE:
        break
    js.append(f'tl.fromTo("#cam",{{scale:{s_ / 100 * 1.012:.4f}}},{{scale:{s2 / 100 * 1.012:.4f},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t});')

CAPY = {"16": "89%", "9": "49%", "45": "84%"}[FMT]
CAPS_SIZE = {"16": 36, "9": 44, "45": 40}[FMT]
BIG = {"16": 112, "9": 96, "45": 88}[FMT]
CSS = f"""
@font-face {{ font-family:'Rubik'; src:url('fonts/Rubik-variable-latin.woff2') format('woff2'); font-weight:300 900; font-display:block; }}
@font-face {{ font-family:'Manrope'; src:url('fonts/Manrope-variable-latin.woff2') format('woff2'); font-weight:200 800; font-display:block; }}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10;font-family:'Manrope',sans-serif}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10}}
#cam{{position:absolute;inset:0;width:{W}px;height:{H}px}}
video{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover}}
.white{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:#fafafa}}
.scn{{display:block;padding:0}}
.mk{{display:block;overflow:hidden;padding:0.08em 0.1em 0.14em}} .rw{{display:inline-block}}
.hd{{position:absolute;font-family:'Rubik';font-weight:700;line-height:1.02;letter-spacing:-0.04em}} .hd .ac{{color:#3976ff}}
.bigd{{letter-spacing:-0.05em}} .dm2{{position:relative}}
.ul2{{position:absolute;left:0;bottom:0.02em;height:0.06em;width:100%;background:#3976ff;border-radius:6px;transform-origin:0 50%}}
.li{{overflow:visible;fill:none;stroke-linecap:round;stroke-linejoin:round}} .li path{{stroke-dasharray:1 2;stroke-dashoffset:0}}
.nd{{position:absolute;border:6px solid;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(20,20,60,.08)}}
.nl{{position:absolute;text-align:center;font-family:'Manrope';font-weight:800;font-size:{round(H * 0.028) if FMT == '16' else 36}px;color:#0b0b14;overflow:hidden}}
.cn{{position:absolute;left:0;top:0;pointer-events:none}} .cn line{{fill:none;stroke-width:6;stroke-linecap:round;stroke-dasharray:1 2;stroke-dashoffset:1}}
.pk{{position:absolute;width:22px;height:22px;border-radius:50%;background:#3976ff;box-shadow:0 0 18px 6px rgba(57,118,255,.45);opacity:0}}
.cd{{position:absolute}} .cd:not(.cd2){{display:flex;align-items:center;justify-content:center;gap:14px;font-family:'Manrope';font-weight:800;font-size:{round(H * 0.03) if FMT == '16' else 38}px}}
.gr{{position:absolute;border:4px solid #3976ff;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 22px rgba(20,20,60,.08)}}
.cd2{{position:absolute;border:5px solid;border-radius:28px;background:#fff;padding:26px 26px;box-shadow:0 14px 34px rgba(20,20,60,.10);display:flex;flex-direction:column;align-items:flex-start;gap:12px}}
.cd2 .ci{{position:absolute;left:24px;width:84px;height:84px;border:5px solid;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}} .cv{{position:absolute;object-fit:cover;z-index:5}}
.cd2 b{{font-family:'Rubik';font-weight:700;font-size:{40 if FMT == '16' else 36}px;line-height:1.1;letter-spacing:-0.02em;color:#0b0b14}} .cd2 i{{font-style:normal;font-family:'Manrope';font-weight:600;font-size:{26 if FMT == '16' else 24}px;color:#6a6a7e}}
.bt{{position:absolute;display:flex;align-items:center;justify-content:center;gap:18px;height:{round(H * 0.115) if FMT == '16' else 120}px;border-radius:999px;background:#3976ff;color:#fff;font-family:'Rubik';font-weight:600;font-size:{round(H * 0.044) if FMT == '16' else 46}px;box-shadow:0 14px 34px rgba(57,118,255,.35)}}
.url{{position:absolute;text-align:center;font-family:'Rubik';font-weight:500;font-size:{round(H * 0.052) if FMT == '16' else 46}px;color:#0b0b14;letter-spacing:-0.01em}} .url b{{color:#7d00ba;font-weight:700}}
.ov2{{position:absolute;left:0;width:{W}px;display:flex;justify-content:center;pointer-events:none}}
.bigw{{font-family:'Rubik';font-weight:700;font-size:{BIG}px;color:#fff;letter-spacing:-0.04em;text-shadow:0 5px 22px rgba(0,0,0,.55)}} .bigw .ac2{{color:#fff}}
.lg2 .logo{{height:{round(BIG * 0.5)}px;width:auto;filter:drop-shadow(0 4px 18px rgba(0,0,0,.5))}}
.cap{{position:absolute;left:0;width:{W}px;top:{CAPY};text-align:center;font-family:'Rubik';font-weight:500;font-size:{CAPS_SIZE}px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.75),0 0 2px rgba(0,0,0,.6);pointer-events:none}}
.capd{{color:#1a1a1a;text-shadow:none}}
"""
html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8" /><style>{CSS}</style></head>
<body>
<div id="stage" data-composition-id="rental" data-start="0" data-duration="{END_SCENE:.4f}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
  <div id="cam">
    {chr(10).join('    ' + e for e in els)}
  </div>
  {chr(10).join('  ' + c for c in caps_html)}
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    window.gsap.defaults({{ lazy: false }});
    const tl = window.gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in js)}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["rental"] = tl;
  }})();
  </script>
</div>
</body></html>
"""
PROJ.mkdir(parents=True, exist_ok=True)
(PROJ / "index.html").write_text(html, encoding="utf-8")
EVS = {k: EV(k) for k in ("hay", "primero", "caminos", "daas", "arrendamiento", "por", "llenar", "pagas", "siempre", "soporte", "quieres", "pregúntanos", "onescreen", "contactarnos", "si")}
EVS["o2"] = EV("o", 1)
json.dump(dict(END_SCENE=END_SCENE, segs=SEG, events=EVS), open(PROJ / "plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", FMT, "escena", END_SCENE, "segmentos", len(SEG))
