"""v2 del video QuizWiz + Scrybe, editado con las reglas medidas de Cris (estilo-onescreen/07_EDICION.md y 06_ESTILO_ORGANICO.md).

Reglas que aplica (todas medidas en sus proyectos):
  - cada corte / entrada de plano / gráfico cae ~2-3 cuadros (0,10 s) ANTES del inicio de la palabra que lo motiva (palabras de Scribe);
  - zigzag ancho (100 %) / cerrado (144-165 %) en cada corte, salto fijo de escala, valor según el plano;
  - planos de apoyo literales a lo que se nombra (interfaz real de Scrybe y QuizWiz, docente estresada, examen, QR, cajas);
  - palabras sobre el material: entrada 0->100 % en 2 cuadros, subida ~24 % del alto en 0,21 s, sombra suave, salida flotando;
  - tarjeta blanca de una línea (texto azul) como respiro; capa de ajuste con cámara que flota + aberración cromática (post);
  - cierre: intro de marca prefabricada del Brand kit (post); música en una sola pista; SFX 60-85 ms antes del evento.
Uso: FMT=16|9|45 CAPS=1|0 python build_v2.py
"""
import json, os, re
from pathlib import Path

FMT = os.environ.get("FMT", "16")
CAPS = os.environ.get("CAPS", "1") == "1"
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[FMT]
PROJ = Path(f"D:/OneScreen/Contenido/2026/10. Octubre/QuizWiz y Scrybe/Proyecto/v2_{FMT}")
SCRIBE = r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-21_quizwiz_scrybe/scribe_v5_1p.json"
FPS = 24
D = 0.10        # la voz arranca a 0,10 s
LEAD = 0.10     # los cambios de imagen anteceden a la palabra ~2,4 cuadros (mediana medida: 90-100 ms)

words = [w for w in json.load(open(SCRIBE, encoding="utf-8"))["words"] if w.get("type") == "word"]


def norm(t):
    return re.sub(r"[¿?¡!.,;:]", "", t).lower()


def snap(t):
    return round(t * FPS) / FPS


def onset(word, n=0):
    k = [w for w in words if norm(w["text"]) == word]
    return k[n]["start"]


def EV(word, n=0):
    return snap(onset(word, n) + D - LEAD)


END_SCENE = snap(words[-1]["end"] + D + 0.95)

CLIP_LEN = {"s01": 3.21, "s02": 3.21, "s05": 3.21, "s06": 4.21, "s08": 3.62, "s09": 4.0, "s10": 3.62, "scrA": 8.0, "scrB": 5.5, "qwzGen": 9.0, "qwzQR": 8.0, "stress": 6.5, "docente": 6.0, "u1": 4.0, "u2": 4.0, "u3": 4.0, "u4": 4.0}
FILE = {"u1": "u1", "u2": "u2", "u3": "u3", "u4": "u4", "docente": "docente", "s01": "s01_pizarra_perfil", "s02": "s02_pizarra_frente", "s05": "s05_habla", "s06": "s06_qr", "s08": "s08_ok", "s09": "s09_cajas", "s10": "s10_caja_t7",
        "scrA": "scrA", "scrB": "scrB", "qwzGen": "qwzGen", "qwzQR": "qwzQR", "stress": "stress"}

# (t, tipo, fuente, entrada_en_fuente, escala %, origen)
SEG = []


def seg(t, kind, src=None, tin=0.0, scale=100, origin="50% 50%", rate=1.0):
    SEG.append(dict(t=t, kind=kind, src=src, tin=tin, scale=scale, origin=origin, rate=rate))


T_grabar, T_con, T_start, T_el, T_esa = EV("grabar"), EV("con"), EV("start"), EV("el"), EV("esa")
seg(0.0, "vid", "u1", 0.0, 100, "48% 50%")
seg(EV("y"), "vid", "u2", 0.0, 100, "62% 50%")
seg(T_grabar, "white", "ui")
seg(EV("poner"), "white", "ia")
seg(EV("cuando"), "white", "res")
seg(EV("pero"), "vid", "u3", 0.0, 100, "45% 50%")
seg(EV("nosotros"), "vid", "u4", 0.0, 100, "50% 50%")
seg(EV("solo", 1), "white", "cta")
for i, s in enumerate(SEG):
    s["t1"] = SEG[i + 1]["t"] if i + 1 < len(SEG) else END_SCENE
    s["dur"] = round(s["t1"] - s["t"], 4)
    if i + 1 < len(SEG) and SEG[i + 1]["kind"] == "white":
        s["dur"] = round(s["dur"] + 0.6, 4)      # el plano anterior sigue debajo mientras la tarjeta blanca barre (si no, queda negro)
    if s["src"] in CLIP_LEN and s["tin"] + s["dur"] * s.get("rate", 1.0) > CLIP_LEN[s["src"]] + 0.01:
        print("AVISO: se acaba la fuente", s["src"], s["tin"], s["dur"])

# ── HTML ─────────────────────────────────────────────────────────────────────
els, js = [], []


def mask_rise(sel, t, d=0.7, stag=0.06):
    js.append(f'tl.fromTo("{sel}",{{yPercent:110,opacity:0}},{{yPercent:0,opacity:1,duration:{d},ease:"power4.out",stagger:{stag}}},{t:.4f});')



def svg(name, cls):
    t = (PROJ / "assets" / name).read_text(encoding="utf-8-sig")
    t = re.sub(r"<\?xml[^>]*\?>", "", t)
    t = re.sub(r'\s(id|data-name)="[^"]*"', "", t)
    return t.replace("<svg ", f'<svg class="{cls}" ', 1)



# ── escenas Flota IA ─────────────────────────────────────────────────────────
INK, ACC, PUR, MUT = "#0b0b14", "#3976ff", "#7d00ba", "#9a9aae"
LAY = {"16": dict(HS=104, HY1=130, NY=520, ND=176, HY2=700, M=150, AL="left"),
       "9": dict(HS=92, HY1=260, NY=650, ND=150, HY2=1060, M=80, AL="center"),
       "45": dict(HS=84, HY1=150, NY=530, ND=150, HY2=690, M=80, AL="center")}[FMT]
ICO = {"cap": ["M2 9l10-5 10 5-10 5z", "M6 11.5V16c3 2.5 9 2.5 12 0v-4.5", "M22 9v6"],
       "doc": ["M7 3h7l4 4v14H7z", "M14 3v4h4", "M10 12h5", "M10 16h5"],
       "arrow": ["M5 12h14", "M13 6l6 6-6 6"],
       "x": ["M5 5l14 14", "M19 5L5 19"],
       "chk": ["M5 12.5l4.5 4.5L19 7"],
       "chart": ["M5 20V11", "M12 20V4", "M19 20v-6"]}


def line_icon(name, size, color, sw=1.7):
    ps = "".join(f'<path d="{p}" pathLength="1"/>' for p in ICO[name])
    return (f'<svg class="li" viewBox="0 0 24 24" width="{size}" height="{size}" style="stroke:{color};stroke-width:{sw}">{ps}</svg>')


def sc_head(cid, k, html, y, t, size=None, color=INK, al=None):
    size = size or LAY["HS"]
    els_html = (f'<div id="{cid}-h{k}" class="hd" style="left:{LAY["M"]}px;width:{W - 2 * LAY["M"]}px;top:{y}px;font-size:{size}px;color:{color};text-align:{al or LAY["AL"]}">'
                f'<span class="mk"><span class="rw hr">{html}</span></span></div>')
    mask_rise(f"#{cid}-h{k} .hr", t, 0.7)
    return els_html


def sc_node(cid, k, cx, icon, label, t, color=ACC, logo=None):
    ND, NY = LAY["ND"], LAY["NY"]
    inner = logo if logo else line_icon(icon, round(ND * 0.5), color)
    h = (f'<div id="{cid}-n{k}" class="nd" style="left:{cx - ND // 2}px;top:{NY - ND // 2}px;width:{ND}px;height:{ND}px;border-color:{color}">{inner}</div>'
         f'<div id="{cid}-l{k}" class="nl" style="left:{cx - 200}px;top:{NY + ND // 2 + 20}px;width:400px">{label}</div>')
    js.append(f'tl.fromTo("#{cid}-n{k}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.7)"}},{t:.4f});')
    js.append(f'tl.fromTo("#{cid}-n{k} .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power2.inOut",stagger:0.08}},{t + 0.1:.4f});')
    mask_rise(f"#{cid}-l{k}", t + 0.2, 0.5)
    return h


def sc_conn(cid, k, x1, x2, t, dur=0.8, color=ACC):
    ND, NY = LAY["ND"], LAY["NY"]
    a, b = x1 + ND // 2 + 14, x2 - ND // 2 - 14
    h = (f'<svg class="cn" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><line id="{cid}-c{k}" x1="{a}" y1="{NY}" x2="{b}" y2="{NY}" pathLength="1" style="stroke:{color}"/></svg>'
         f'<div id="{cid}-p{k}" class="pk" style="left:{a - 11}px;top:{NY - 11}px"></div>')
    js.append(f'tl.fromTo("#{cid}-c{k}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{t:.4f});')
    js.append(f'tl.fromTo("#{cid}-p{k}",{{x:0,opacity:0}},{{x:{b - a},opacity:1,duration:{dur},ease:"power2.inOut"}},{t:.4f});')
    js.append(f'tl.to("#{cid}-p{k}",{{opacity:0,duration:0.2}},{t + dur:.4f});')
    return h


def scene_exit(cid, t_end):
    js.append(f'tl.to("#{cid} .hd,#{cid} .nd,#{cid} .nl,#{cid} .cn,#{cid} .st,#{cid} .bt,#{cid} .rg",{{opacity:0,x:-60,duration:0.3,ease:"power2.in"}},{t_end - 0.32:.4f});')


def wipe_in(cid, t):
    js.append(f'tl.fromTo("#{cid}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"power3.inOut"}},{t:.4f});')


def scene_ia(cid, t0, t1):
    wipe_in(cid, t0)
    parts = []
    parts.append(sc_head(cid, 1, 'Una IA que <span id="%s-w" class="strk2">adivina.</span><span class="xm" id="%s-x">%s</span>' % (cid, cid, line_icon("x", round(LAY["HS"] * 0.62), PUR, 2.2)), LAY["HY1"], t0 + 0.2))
    ts = EV("adivine")
    js.append(f'tl.fromTo("#{cid}-w",{{backgroundSize:"0% 8px"}},{{backgroundSize:"100% 8px",duration:0.45,ease:"power2.inOut"}},{ts:.4f});')
    js.append(f'tl.fromTo("#{cid}-x path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.inOut",stagger:0.12}},{ts + 0.3:.4f});')
    tm = EV("mejor")
    ND, NY = LAY["ND"], LAY["NY"]
    parts.append(f'<div id="{cid}-n0" class="nd" style="left:{W // 2 - ND // 2}px;top:{NY - ND // 2}px;width:{ND}px;height:{ND}px;border-color:{MUT};border-style:dashed"><span class="qm">?</span></div>'
                 f'<div id="{cid}-l0" class="nl" style="left:{W // 2 - 200}px;top:{NY + ND // 2 + 20}px;width:400px;color:{MUT}">Adivina</div>'
                 f'<div id="{cid}-bx" class="bx" style="left:{W // 2 - ND // 2 - 20}px;top:{NY - ND // 2 - 20}px">{line_icon("x", ND + 40, PUR, 1.4)}</div>')
    js.append(f'tl.fromTo("#{cid}-n0",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.7)"}},{t0 + 0.55:.4f});')
    mask_rise(f"#{cid}-l0", t0 + 0.75, 0.5)
    js.append(f'tl.fromTo("#{cid}-bx path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.45,ease:"power2.inOut",stagger:0.12}},{ts + 0.35:.4f});')
    js.append(f'tl.to("#{cid}-n0,#{cid}-l0,#{cid}-bx",{{opacity:0,x:-60,duration:0.3,ease:"power2.in"}},{tm - 0.05:.4f});')
    js.append(f'tl.to("#{cid}-h1",{{opacity:0.28,duration:0.3}},{tm:.4f});')
    parts.append(sc_head(cid, 2, 'Mejor usa <span class="ac">tu clase</span><span class="mk" style="display:inline"><span class="rw" id="%s-sg">, en segundos.</span></span>' % cid, LAY["HY2"], tm + 0.05))
    mask_rise("#%s-sg" % cid, EV("en", 3), 0.7)
    cx1, cx2 = (round(W * 0.30), round(W * 0.70))
    t1n = EV("usa") + 0.1
    parts.append(sc_node(cid, 1, cx1, "cap", "Tu clase", t1n))
    parts.append(sc_conn(cid, 1, cx1, cx2, t1n + 0.45, 0.7))
    parts.append(sc_node(cid, 2, cx2, "doc", "El examen", t1n + 1.15, PUR))
    scene_exit(cid, t1)
    return "".join(parts)


def scene_res(cid, t0, t1):
    wipe_in(cid, t0)
    parts = []
    parts.append(sc_head(cid, 1, 'Evalúas lo que <span class="ac">enseñaste</span>.', LAY["HY1"], t0 + 0.2))
    cx1, cx2 = (round(W * 0.30), round(W * 0.70))
    parts.append(sc_node(cid, 1, cx1, "cap", "Lo que enseñas", EV("evalúa", 1) + 0.05))
    parts.append(sc_node(cid, 2, cx2, "chart", "Lo que se evalúa", EV("enseñó", 1) + 0.05, PUR))
    tr = EV("resultados")
    parts.append(sc_conn(cid, 1, cx1, cx2, tr - 0.35, 0.6))
    d = round(LAY["ND"] * 0.7)
    parts.append(f'<div id="{cid}-rg" class="rg" style="left:{W // 2 - d // 2}px;top:{LAY["NY"] - d // 2}px;width:{d}px;height:{d}px"><svg viewBox="0 0 24 24" width="{d}" height="{d}"><circle cx="12" cy="12" r="11" pathLength="1"/><path d="M6.5 12.5l3.5 3.5 7.5-8" pathLength="1"/></svg></div>')
    js.append(f'tl.fromTo("#{cid}-rg",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.7)"}},{tr + 0.2:.4f});')
    js.append(f'tl.fromTo("#{cid}-rg circle",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.inOut"}},{tr + 0.2:.4f});')
    js.append(f'tl.fromTo("#{cid}-rg path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.4,ease:"power2.inOut"}},{tr + 0.55:.4f});')
    tf = EV("fin")
    parts.append(f'<div id="{cid}-s" class="st" style="left:{W // 2 - (330 if FMT == "16" else 400)}px;top:{LAY["HY2"] + (50 if FMT == "16" else 0)}px;width:{660 if FMT == "16" else 800}px">Resultados que dicen algo</div>')
    js.append(f'tl.fromTo("#{cid}-s",{{opacity:0,scale:2.2,rotation:0}},{{opacity:1,scale:1,rotation:-6,duration:0.35,ease:"power4.in"}},{tf:.4f});')
    scene_exit(cid, t1)
    return "".join(parts)


def scene_cta(cid, t0, t1):
    wipe_in(cid, t0)
    parts = []
    ty = {"16": 330, "9": 520, "45": 360}[FMT]
    parts.append(sc_head(cid, 1, 'Solicita tu <span class="dm2">demo<span class="ul2" id="%s-u"></span></span> aquí.' % cid, ty, t0 + 0.2, size=round(LAY["HS"] * 1.12), color=ACC))
    js.append(f'tl.fromTo("#{cid}-u",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},{EV("demo") + 0.1:.4f});')
    by = {"16": 640, "9": 1080, "45": 700}[FMT]
    bw = {"16": 520, "9": 560, "45": 520}[FMT]
    parts.append(f'<div id="{cid}-b" class="bt" style="left:{W // 2 - bw // 2}px;top:{by}px;width:{bw}px">Solicitar demo {line_icon("arrow", 44, "#fff", 2.2)}</div>')
    tb = EV("aquí") - 0.05
    js.append(f'tl.fromTo("#{cid}-b",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.7)"}},{tb:.4f});')
    js.append(f'tl.fromTo("#{cid}-b .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut",stagger:0.1}},{tb + 0.25:.4f});')
    return "".join(parts)


SCR_ICO, QZ_ICO = svg("Scrybe.svg", "ico"), svg("QuizWiz.svg", "ico")
exec(open(Path(__file__).parent / "ui3d.py", encoding="utf-8").read())
cnt = 0
for s in SEG:
    cnt += 1
    cid = f"s{cnt:02d}"
    if s["kind"] == "vid":
        el = (f'<video id="{cid}" class="clip" src="media/{FILE[s["src"]]}.mp4" muted playsinline data-start="{s["t"]:.4f}" data-duration="{s["dur"]:.4f}" '
              f'data-media-start="{s["tin"]:.4f}" data-playback-rate="{s["rate"]:.3f}" data-track-index="1" style="object-position:{s["origin"].split()[0]} 50%;transform-origin:{s["origin"]};'
              f'transform:scale({s["scale"] / 100:.3f})"></video>')
        els.append(el)
    elif s["kind"] == "img":
        els.append(f'<img id="{cid}" class="clip" src="media/examen.png" data-start="{s["t"]:.4f}" data-duration="{s["dur"]:.4f}" data-track-index="1" style="object-position:62% 50%">')
        js.append(f'tl.fromTo("#{cid}",{{scale:1.0}},{{scale:1.10,duration:{s["dur"]:.3f},ease:"none"}},{s["t"]:.4f});')
    else:
        t_end = s["t1"]
        if s["src"] == "ui":
            els.append(build_ui3d(s["t"], t_end, cid)); continue
        body = {"ia": scene_ia, "res": scene_res, "cta": scene_cta}[s["src"]](cid, s["t"], t_end)
        els.append(f'<div id="{cid}" class="clip white scn" data-start="{s["t"]:.4f}" data-duration="{s["dur"]:.4f}" data-track-index="2">{body}</div>')

# capa gráfica estilo Flota IA ("Apple", estilo-onescreen/05_MOTION.md): titulares que suben por máscara, nodos con rebote, trazos que se dibujan, barrido
YF = {"16": 0.62, "9": 0.65, "45": 0.60}[FMT]


def mask_rise(sel, t, d=0.7, stag=0.06):
    js.append(f'tl.fromTo("{sel}",{{yPercent:110,opacity:0}},{{yPercent:0,opacity:1,duration:{d},ease:"power4.out",stagger:{stag}}},{t:.4f});')


def out_left(sel, t, d=0.35):
    js.append(f'tl.to("{sel}",{{opacity:0,x:-60,duration:{d},ease:"power2.in"}},{t:.4f});')


def overlay(oid, t, html, dur=1.5):
    els.append(f'<div id="{oid}-s" class="clip scrim" data-start="{t - 0.1:.4f}" data-duration="{dur + 0.2:.4f}" data-track-index="2"></div>')
    js.append(f'tl.fromTo("#{oid}-s",{{opacity:0}},{{opacity:1,duration:0.3,ease:"power2.out"}},{t - 0.1:.4f});')
    js.append(f'tl.to("#{oid}-s",{{opacity:0,duration:0.3,ease:"power2.in"}},{t + dur - 0.2:.4f});')
    els.append(f'<div id="{oid}" class="clip ov" data-start="{t:.4f}" data-duration="{dur}" data-track-index="3" style="top:{YF * 100:.2f}%">{html}</div>')
    out_left(f"#{oid} .rw,#{oid} .pop,#{oid} .ul", t + dur - 0.4)


def lock(oid, name, sub, ico, t):
    js.append(f'tl.fromTo("#{oid} .pop",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.7)"}},{t:.4f});')
    mask_rise(f"#{oid} .rw", t + 0.12, 0.7, 0.1)
    js.append(f'tl.fromTo("#{oid} .ul",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},{t + 0.35:.4f});')
    return (f'<div class="lk"><span class="sq pop">{ico}</span><span class="tx"><span class="mk"><b class="rw">{name}</b></span>'
            f'<span class="mk"><i class="rw">{sub}</i></span><span class="ul"></span></span></div>')


# overlay("o1", EV("scribe"), lock("o1", "Scrybe", "Graba y transcribe en tiempo real.", SCR_ICO, EV("scribe")))
# overlay("o2", EV("quizwiz"), lock("o2", "QuizWiz", "Genera exámenes con IA en segundos.", QZ_ICO, EV("quizwiz")))

# subtítulos (pequeños, blancos, sin fondo, 2-3 palabras; en vertical a media altura, como los pone Cris)
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
        txt = " ".join(x["text"].replace("Scribe", "Scrybe") for x in c)
        tm = t0 + 0.05
        blanco = any((sg["kind"] == "white" or sg["src"] in ("scrA", "scrB", "qwzQR", "qwzGen")) and sg["t"] - 0.05 <= tm < sg["t1"] for sg in SEG)
        pill = any(sg["src"] == "ui" and sg["t"] - 0.05 <= tm < sg["t1"] for sg in SEG)
        caps_html.append(f'<div class="clip cap{" capd" if blanco else ""}{" capp" if pill else ""}" data-start="{t0:.4f}" data-duration="{max(t1 - t0 - 0.05, 0.2):.4f}" data-track-index="5">{("<span class=pl>" + txt + "</span>") if pill else txt}</div>')

# cámara que flota (capa de ajuste de Cris: posición ±2 % y escala 103,5-105,2 % en bucle de ~12 s)
POS = [(0, .5, .5), (1.04, .5141, .5), (1.88, .4958, .487), (2.88, .4908, .4849), (5.04, .4842, .5093), (6.32, .5138, .515), (7.96, .4811, .4963), (9.48, .5217, .5213),
       (12.04, .5, .5), (13.28, .5141, .5), (14.12, .4958, .487), (15.12, .4908, .4849), (17.28, .4842, .5093), (18.56, .5138, .515), (20.2, .4811, .4963), (22.4, .5217, .5213),
       (25.0, .5, .5), (26.04, .5141, .5), (26.88, .4958, .487), (27.88, .4908, .4849), (30.04, .4842, .5093), (31.32, .5138, .515), (32.96, .4811, .4963), (34.48, .5217, .5213), (37.04, .5, .5), (38.28, .5141, .5), (39.12, .4958, .487)]
SCL = [(0, 104), (1.88, 103.5), (3.44, 104.4), (5.44, 103.6), (7.4, 105.2), (10.0, 104.9), (12.04, 104.4), (14.12, 103.5), (15.68, 104.4), (17.68, 103.6), (19.64, 105.2),
       (22.92, 104.9), (25.0, 104), (26.88, 103.5), (28.44, 104.4), (30.44, 103.6), (32.4, 105.2), (35.0, 104.9), (37.04, 104.4), (39.12, 103.5)]
js.append(f'gsap.set("#cam",{{transformOrigin:"50% 50%"}});')
for (t, x, y), (t2, x2, y2) in zip(POS, POS[1:]):
    if t >= END_SCENE:
        break
    js.append(f'tl.fromTo("#cam",{{x:{(x - .5) * W:.1f},y:{(y - .5) * H:.1f}}},{{x:{(x2 - .5) * W:.1f},y:{(y2 - .5) * H:.1f},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t});')
for (t, s), (t2, s2) in zip(SCL, SCL[1:]):
    if t >= END_SCENE:
        break
    js.append(f'tl.fromTo("#cam",{{scale:{s / 100 * 1.012:.4f}}},{{scale:{s2 / 100 * 1.012:.4f},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t});')

CAPY = {"16": "81%", "9": "49%", "45": "66%"}[FMT]
CAPS_SIZE = {"16": 36, "9": 44, "45": 40}[FMT]
BIG = {"16": 130, "9": 120, "45": 112}[FMT]
LK = {"16": 1.0, "9": 0.85, "45": 0.85}[FMT]
CSS = f"""
@font-face {{ font-family:'Rubik'; src:url('fonts/Rubik-variable-latin.woff2') format('woff2'); font-weight:300 900; font-display:block; }}
@font-face {{ font-family:'Manrope'; src:url('fonts/Manrope-variable-latin.woff2') format('woff2'); font-weight:200 800; font-display:block; }}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10;font-family:'Manrope',sans-serif}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10}}
#cam{{position:absolute;inset:0;width:{W}px;height:{H}px}}
video,img.clip{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover}}
.white{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;box-sizing:border-box;padding-bottom:{round(H*0.24) if FMT=='9' else 0}px;background:#fafafa;display:flex;align-items:center;justify-content:center;text-align:center}}
.wl{{font-family:'Rubik';font-weight:400;font-size:{round(H * 0.062) if FMT == '16' else round(W * 0.075)}px;color:#3976ff;line-height:1.15;padding:0 {round(W * 0.1)}px;letter-spacing:-0.01em}}
.wl b{{font-weight:700}}
.strk{{font-weight:700;background-image:linear-gradient(#7d00ba,#7d00ba);background-repeat:no-repeat;background-position:0 58%;background-size:0% 6px}}
.ov{{position:absolute;left:0;width:{W}px;display:flex;justify-content:center;align-items:center;transform:translateY(0);margin-top:-1em;pointer-events:none}}
.big{{font-family:'Rubik';font-weight:700;font-size:{BIG}px;color:#fff;text-shadow:0 5px 22px rgba(0,0,0,.55);letter-spacing:-0.03em;display:inline-block}}
.mk{{display:block;overflow:hidden;padding:0.08em 0.1em 0.14em}} .rw{{display:inline-block}}
.scrim{{position:absolute;left:0;top:{round(H * 0.30)}px;width:{W}px;height:{round(H * 0.70)}px;background:linear-gradient(180deg,rgba(8,0,18,0) 0%,rgba(8,0,18,.62) 100%);pointer-events:none}}
.ul{{display:block;height:5px;width:100%;margin-top:10px;background:#7d00ba;border-radius:3px;transform-origin:0 50%}}
.dm{{position:relative;display:inline-block;font-weight:700}} .ul2{{position:absolute;left:0;bottom:-0.12em;height:0.07em;width:100%;background:#3976ff;border-radius:3px;transform-origin:0 50%}}
.chk{{position:absolute;left:0;top:{round(H * (0.25 if FMT=='9' else 0.36))}px;width:{W}px;display:flex;justify-content:center}} .chk svg{{overflow:visible;filter:drop-shadow(0 4px 14px rgba(0,0,0,.5))}}
.chk circle,.chk path{{fill:none;stroke:#fff;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 2;stroke-dashoffset:1}}
.lk{{display:flex;align-items:center;gap:{round(22 * LK)}px;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.5)}}
.lk .sq{{width:{round(110 * LK)}px;height:{round(110 * LK)}px;border-radius:{round(26 * LK)}px;background:#7d00ba;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 24px rgba(0,0,0,.35)}}
.lk .sq .ico{{height:{round(62 * LK)}px;width:auto}} .lk .sq .ico path{{fill:#fff}}
.lk .tx{{display:flex;flex-direction:column}} .lk b{{font-family:'Rubik';font-weight:700;font-size:{round(70 * LK)}px;line-height:1}} .lk i{{font-style:normal;font-family:'Manrope';font-weight:600;font-size:{round(30 * LK)}px;margin-top:6px}}
.cap{{position:absolute;left:0;width:{W}px;top:{CAPY};text-align:center;font-family:'Rubik';font-weight:500;font-size:{CAPS_SIZE}px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.75),0 0 2px rgba(0,0,0,.6);pointer-events:none}}
.capd{{color:#1a1a1a;text-shadow:none}}
.pl{{background:rgba(255,255,255,.9);padding:4px 18px;border-radius:12px;color:#1a1a1a;text-shadow:none}}
.capp{{background:none}} .capp span{{}}

.scn{{display:block;padding:0}} .qm{{font-family:Rubik;font-weight:700;font-size:{round(LAY["ND"]*0.55)}px;color:#9a9aae}} .bx{{position:absolute}} .bx path{{stroke-dasharray:1 2;stroke-dashoffset:0}}
.hd{{position:absolute;font-family:'Rubik';font-weight:700;line-height:1.02;letter-spacing:-0.04em}} .hd .ac{{color:#3976ff}}
.strk2{{background-image:linear-gradient(#7d00ba,#7d00ba);background-repeat:no-repeat;background-position:0 58%;background-size:0% 8px}}
.xm{{display:inline-block;margin-left:0.18em;vertical-align:-0.05em}} .xm svg{{overflow:visible}}
.li{{overflow:visible;fill:none;stroke-linecap:round;stroke-linejoin:round}} .li path{{stroke-dasharray:1 2;stroke-dashoffset:0}}
.nd{{position:absolute;border:6px solid;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(20,20,60,.08)}}
.nl{{position:absolute;text-align:center;font-family:'Manrope';font-weight:800;font-size:{round(H * 0.026) if FMT == '16' else 34}px;color:#0b0b14;overflow:hidden}}
.cn{{position:absolute;left:0;top:0;pointer-events:none}} .cn line{{fill:none;stroke-width:6;stroke-linecap:round;stroke-dasharray:1 2;stroke-dashoffset:1}}
.pk{{position:absolute;width:22px;height:22px;border-radius:50%;background:#3976ff;box-shadow:0 0 18px 6px rgba(57,118,255,.45);opacity:0}}
.rg{{position:absolute}} .rg circle,.rg path{{fill:none;stroke:#3976ff;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 2;stroke-dashoffset:1}}
.st{{position:absolute;border:7px solid #7d00ba;color:#7d00ba;font-family:'Manrope';font-weight:800;font-size:{round(H * 0.03) if FMT == '16' else 29}px;letter-spacing:0.06em;white-space:nowrap;text-transform:uppercase;text-align:center;padding:18px 20px;border-radius:16px;background:rgba(255,255,255,.9)}}
.dm2{{position:relative;display:inline-block}} .ul2{{position:absolute;left:0;bottom:-0.06em;height:0.07em;width:100%;background:#7d00ba;border-radius:4px;transform-origin:0 50%}}
.bt{{position:absolute;display:flex;align-items:center;justify-content:center;gap:18px;height:{round(H * 0.095) if FMT == '16' else 120}px;border-radius:999px;background:#3976ff;color:#fff;font-family:'Rubik';font-weight:600;font-size:{round(H * 0.036) if FMT == '16' else 46}px;box-shadow:0 14px 34px rgba(57,118,255,.35)}}
"""
CSS += UI_CSS
html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8" /><style>{CSS}</style></head>
<body>
<div id="stage" data-composition-id="qs2" data-start="0" data-duration="{END_SCENE:.4f}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
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
    window.__timelines["qs2"] = tl;
  }})();
  </script>
</div>
</body></html>
"""
(PROJ / "index.html").write_text(html, encoding="utf-8")
json.dump(dict(END_SCENE=END_SCENE, segs=SEG, events={k: EV(k) for k in ("scribe", "quizwiz", "qr", "segundos", "start", "el", "resultados", "implementarlo", "arma", "entregarlo", "estudiante", "escanea", "celular", "poner", "cuando", "pero", "nosotros")}),
          open(PROJ / "plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", FMT, "escena", END_SCENE, "segmentos", len(SEG), "cortes/min", round(60 * (len(SEG) - 1) / END_SCENE, 1))
