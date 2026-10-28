"""Arma public/index.html del pitch de Lessn: tarjetas + timeline GSAP.

Tiempos en segundos sobre trimmed.mp4 (video ya sin silencios).
Cada tarjeta declara sus animaciones con data-anim-*; aquí se compilan a GSAP.
"""
import json
from html import escape as html_escape
import re
from pathlib import Path

ROOT = Path(__file__).parent
PUB = ROOT / "public"
FPS = 25
VIDEO_DUR = 81.72
TOTAL = 84.6

LOGO = re.sub(r'\s(id|data-name)="[^"]*"', "", (ROOT / "logo.svg").read_text(encoding="utf-8"))
LOGO = LOGO.replace("<svg ", '<svg class="logo" ', 1)

# Rectángulos de #video-wrap
# Solo transforms + clipPath (inset en coordenadas locales del wrapper 1920x1080)
FULL = dict(x=0, y=0, scale=1, clipPath="inset(0px 0px 0px 0px round 0px)")
SPLIT = dict(x=480, y=0, scale=1, clipPath="inset(0px 480px 0px 480px round 0px)")
PIP = dict(x=1424, y=760, scale=0.225, clipPath="inset(0px 0px 0px 0px round 98px)")

HOST_FULL = (0, 0, 1920, 1080)
HOST_LEFT = (0, 0, 960, 1080)


def chars(text):
    words = ['<span class="word">' + "".join(f'<span class="char">{c}</span>' for c in w) + "</span>" for w in text.split(" ")]
    return '<span class="char">&nbsp;</span>'.join(words)


def lessn_lockup(size="lg"):
    return f'<div class="lockup {size}">{LOGO}<span class="lessn">Lessn</span></div>'


# ── Tarjetas ────────────────────────────────────────────────────────────────
# (id, start, end, host bounds, video layout, html del .root, js extra)
CARDS = []


def card(cid, start, end, host, layout, body, root_class="", extra_js=""):
    CARDS.append(dict(id=cid, start=start, end=end, host=host, layout=layout, body=body,
                      root_class=root_class, extra_js=extra_js))


card("c01", 0.10, 4.30, HOST_FULL, FULL, f"""
  <div class="scrim-left"></div>
  <div class="ov-text">
    <div class="kicker" id="c01-k" data-anim="fade-in" data-anim-at="0.1" data-anim-duration="0.4">Te lo muestro</div>
    <h1 class="h-xl" id="c01-t" data-anim="kinetic-chars" data-anim-at="0.25" data-anim-duration="0.45" data-anim-stagger="0.03">{chars("Es más simple")}<br>{chars("de lo que parece.")}</h1>
    <div class="bar accent-blue" id="c01-b" data-anim="grow-x" data-anim-at="1.6" data-anim-duration="0.6" data-anim-target-w="260"></div>
  </div>""", root_class="transparent")

card("c02", 4.36, 6.40, HOST_FULL, FULL, f"""
  <div class="scrim-left"></div>
  <div class="ov-text">
    <div class="chip chip-orange" id="c02-c" data-anim="scale-pop" data-anim-at="0.05" data-anim-duration="0.45">Primero</div>
    <h1 class="h-xl" id="c02-t" data-anim="mask-reveal" data-anim-at="0.2" data-anim-duration="0.55">Entendamos<br><span class="orange">el problema</span></h1>
  </div>""", root_class="transparent")

card("c03", 6.50, 17.80, HOST_LEFT, SPLIT, """
  <div class="panel-in">
    <div class="kicker" id="c03-k" data-anim="slide-in" data-anim-from="left" data-anim-distance="60" data-anim-at="0.25" data-anim-duration="0.5">Un docente de planta</div>
    <div class="stat" id="c03-s1" data-anim="fade-in" data-anim-at="2.45" data-anim-duration="0.3">
      <span class="num orange">28–<span id="c03-n1" data-anim="count-up" data-anim-at="2.5" data-anim-duration="1.2" data-anim-from="28" data-anim-to="30" data-anim-format="d">28</span></span><span class="unit">h</span>
    </div>
    <div class="sub" id="c03-d1" data-anim="slide-in" data-anim-from="bottom" data-anim-distance="24" data-anim-at="3.9" data-anim-duration="0.45">de clase por semana</div>
    <div class="rule" id="c03-r" data-anim="grow-x" data-anim-at="6.0" data-anim-duration="0.5" data-anim-target-w="700"></div>
    <div class="kicker small" id="c03-k2" data-anim="fade-in" data-anim-at="6.4" data-anim-duration="0.4">+ preparación</div>
    <div class="stat2" id="c03-s2" data-anim="slide-in" data-anim-from="left" data-anim-distance="50" data-anim-at="8.1" data-anim-duration="0.5">
      <span class="num-m">30 min</span><span class="arrow">→</span><span class="num-m orange">2 h</span>
    </div>
    <div class="sub" id="c03-d2" data-anim="fade-in" data-anim-at="9.9" data-anim-duration="0.45">por <b>cada</b> hora de clase</div>
  </div>""", root_class="panel")

card("c04", 17.86, 29.30, HOST_LEFT, SPLIT, """
  <div class="panel-in">
    <div class="kicker" id="c04-k" data-anim="slide-in" data-anim-from="left" data-anim-distance="60" data-anim-at="0.1" data-anim-duration="0.5">En el mejor de los casos</div>
    <div class="sub dim" id="c04-s" data-anim="fade-in" data-anim-at="1.6" data-anim-duration="0.4">Horas solo preparando clases</div>
    <div class="rows">
      <div class="row" id="c04-r1" data-anim="fade-in" data-anim-at="3.1" data-anim-duration="0.3">
        <div class="row-l"><span class="row-n" id="c04-n1" data-anim="count-up" data-anim-at="3.15" data-anim-duration="0.9" data-anim-from="0" data-anim-to="14" data-anim-format="d">0</span><span class="row-u">h</span><span class="row-p">/ semana</span></div>
        <div class="track"><div class="fill" id="c04-b1" data-anim="grow-x" data-anim-at="3.15" data-anim-duration="0.9" data-anim-target-w="70"></div></div>
      </div>
      <div class="row" id="c04-r2" data-anim="fade-in" data-anim-at="6.2" data-anim-duration="0.3">
        <div class="row-l"><span class="row-n" id="c04-n2" data-anim="count-up" data-anim-at="6.25" data-anim-duration="1.0" data-anim-from="0" data-anim-to="56" data-anim-format="d">0</span><span class="row-u">h</span><span class="row-p">/ mes</span></div>
        <div class="track"><div class="fill" id="c04-b2" data-anim="grow-x" data-anim-at="6.25" data-anim-duration="1.0" data-anim-target-w="230"></div></div>
      </div>
      <div class="row" id="c04-r3" data-anim="fade-in" data-anim-at="8.3" data-anim-duration="0.3">
        <div class="row-l"><span class="row-n orange">+<span id="c04-n3" data-anim="count-up" data-anim-at="8.35" data-anim-duration="1.4" data-anim-from="0" data-anim-to="1000" data-anim-format="esd">0</span></span><span class="row-u">h</span><span class="row-p">/ año</span></div>
        <div class="track"><div class="fill hot" id="c04-b3" data-anim="grow-x" data-anim-at="8.35" data-anim-duration="1.4" data-anim-target-w="760"></div></div>
      </div>
    </div>
  </div>""", root_class="panel")

cells = "".join(f'<div class="cell{" part" if i == 41 else ""}"></div>' for i in range(42))
card("c05", 29.36, 41.60, HOST_FULL, PIP, f"""
  <div class="hero">
    <div class="kicker" id="c05-k" data-anim="fade-in" data-anim-at="0.1" data-anim-duration="0.4">Es decir, hoy tus docentes gastan</div>
    <div class="hero-row">
      <div class="hero-num" id="c05-num" data-anim="scale-pop" data-anim-at="4.3" data-anim-duration="0.5"><span id="c05-n" data-anim="count-up" data-anim-at="4.4" data-anim-duration="2.0" data-anim-from="0" data-anim-to="41.66" data-anim-format="es2">0</span></div>
      <div class="hero-side">
        <div class="hero-unit" id="c05-u" data-anim="slide-in" data-anim-from="right" data-anim-distance="40" data-anim-at="6.4" data-anim-duration="0.45">días seguidos</div>
        <div class="hero-sub" id="c05-s" data-anim="fade-in" data-anim-at="7.7" data-anim-duration="0.45">solo preparando clase</div>
      </div>
    </div>
    <div class="cal" id="c05-cal">{cells}</div>
    <div class="foot" id="c05-f" data-anim="fade-in" data-anim-at="9.2" data-anim-duration="0.5">* Sin contar la evaluación de estudiantes ni demás actividades.</div>
  </div>""", root_class="dark",
     extra_js="""
  tl.fromTo('#c05-cal .cell', {opacity:0, scale:0.4}, {opacity:1, scale:1, duration:0.25, ease:'back.out(2)', stagger:0.045}, T(29.36+4.4));
  tl.to('#c05-cal .cell:not(.part)', {backgroundColor:'#ff8a3d', duration:0.2, stagger:0.045}, T(29.36+4.55));
""")

card("c06", 41.66, 45.20, HOST_FULL, FULL, f"""
  <div class="scrim-left"></div>
  <div class="ov-text">
    <div class="kicker" id="c06-k" data-anim="fade-in" data-anim-at="0.1" data-anim-duration="0.4">Entonces</div>
    <h1 class="h-xl" id="c06-t" data-anim="kinetic-chars" data-anim-at="0.9" data-anim-duration="0.45" data-anim-stagger="0.028">{chars("Lo hicimos")}<br><span class="blue">{chars("más sencillo.")}</span></h1>
  </div>""", root_class="transparent")

card("c07", 45.26, 50.40, HOST_FULL, FULL, """
  <div class="scrim-left"></div>
  <div class="ov-text">
    <div class="chip chip-blue" id="c07-c" data-anim="scale-pop" data-anim-at="0.2" data-anim-duration="0.45">Primer en su tipo</div>
    <h1 class="h-xl" id="c07-t" data-anim="blur-in" data-anim-at="1.45" data-anim-duration="0.6">Ecosistema de<br><span class="blue">Inteligencia Artificial</span></h1>
    <div class="sub" id="c07-s" data-anim="slide-in" data-anim-from="bottom" data-anim-distance="24" data-anim-at="3.6" data-anim-duration="0.45">para espacios de formación</div>
  </div>""", root_class="transparent")

card("c08", 50.46, 54.60, HOST_FULL, PIP, f"""
  <div class="hero center">
    <div class="sub dim" id="c08-a" data-anim="fade-in" data-anim-at="0.05" data-anim-duration="0.35">Vamos por partes</div>
    <div class="chip chip-blue big" id="c08-c" data-anim="scale-pop" data-anim-at="1.0" data-anim-duration="0.45">01 · Antes de clase</div>
    <div id="c08-l" data-anim="scale-pop" data-anim-at="3.05" data-anim-duration="0.6">{lessn_lockup("xl")}</div>
  </div>""", root_class="dark")

card("c09", 54.66, 66.70, HOST_LEFT, SPLIT, f"""
  <div class="panel-in">
    <div id="c09-l" data-anim="fade-in" data-anim-at="0.1" data-anim-duration="0.4">{lessn_lockup("sm")}</div>
    <div class="kicker" id="c09-k" data-anim="fade-in" data-anim-at="1.3" data-anim-duration="0.4">Toda la clase lista en</div>
    <div class="stat" id="c09-s"><span class="num blue">~<span id="c09-n" data-anim="count-up" data-anim-at="3.6" data-anim-duration="1.1" data-anim-from="60" data-anim-to="2" data-anim-format="d">60</span></span><span class="unit">min</span></div>
    <div class="steps">
      <div class="step" id="c09-p1" data-anim="slide-in" data-anim-from="left" data-anim-distance="50" data-anim-at="5.55" data-anim-duration="0.45"><span class="dot">1</span>Eliges el tema y la clase</div>
      <div class="step" id="c09-p2" data-anim="slide-in" data-anim-from="left" data-anim-distance="50" data-anim-at="7.85" data-anim-duration="0.45"><span class="dot">2</span>Lessn crea toda la clase</div>
      <div class="tags">
        <span class="tag" id="c09-t1" data-anim="scale-pop" data-anim-at="10.4" data-anim-duration="0.4">Estructura</span>
        <span class="tag" id="c09-t2" data-anim="scale-pop" data-anim-at="11.25" data-anim-duration="0.4">Presentación</span>
      </div>
    </div>
  </div>""", root_class="panel")

card("c10", 66.76, 71.20, HOST_FULL, FULL, """
  <div class="lt" id="c10-box" data-anim="slide-in" data-anim-from="bottom" data-anim-distance="60" data-anim-at="0.25" data-anim-duration="0.5">
    <div class="lt-icon">✎</div>
    <div>
      <div class="lt-t">100&nbsp;% editable</div>
      <div class="lt-s" id="c10-s" data-anim="fade-in" data-anim-at="2.7" data-anim-duration="0.4">Hazla más personal, con total libertad</div>
    </div>
  </div>""", root_class="transparent")

card("c11", 71.26, VIDEO_DUR, HOST_LEFT, SPLIT, """
  <div class="panel-in">
    <div class="kicker" id="c11-k" data-anim="fade-in" data-anim-at="0.1" data-anim-duration="0.4">¿De dónde sale el contenido?</div>
    <h2 class="h-l" id="c11-t" data-anim="slide-in" data-anim-from="left" data-anim-distance="50" data-anim-at="0.6" data-anim-duration="0.5">IA con <span class="blue">criterio</span></h2>
    <div class="vs bad" id="c11-b" data-anim="fade-in" data-anim-at="2.45" data-anim-duration="0.4">
      <span class="mark">✕</span><span class="vs-t">Información de internet<span class="strike" id="c11-x" data-anim="grow-x" data-anim-at="5.05" data-anim-duration="0.45" data-anim-target-w="440"></span></span>
    </div>
    <div class="vs good" id="c11-g" data-anim="slide-in" data-anim-from="left" data-anim-distance="50" data-anim-at="6.3" data-anim-duration="0.5">
      <span class="mark">✓</span><span class="vs-t">Estándares curriculares<br><b>de América y Europa</b></span>
    </div>
    <div class="badge" id="c11-k12" data-anim="scale-pop" data-anim-at="9.75" data-anim-duration="0.4">K-12</div>
  </div>""", root_class="panel")

card("c12", VIDEO_DUR, TOTAL, HOST_FULL, None, f"""
  <div class="hero center">
    <div id="c12-l" data-anim="scale-pop" data-anim-at="0.15" data-anim-duration="0.6">{lessn_lockup("xl")}</div>
    <div class="sub" id="c12-s" data-anim="fade-in" data-anim-at="0.8" data-anim-duration="0.5">Tu clase, lista en 2 minutos.</div>
  </div>""", root_class="dark")


# ── Compilación de data-anim → GSAP ────────────────────────────────────────
def T(x):
    return f"{round(x * FPS) / FPS:.4f}"


ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')


def compile_anims(c):
    out = []
    for m in re.finditer(r"<[a-z0-9]+\s([^>]*data-anim=[^>]*)>", c["body"]):
        a = dict(ATTR.findall(m.group(1)))
        el_id, kind = a.get("id"), a["data-anim"]
        sel = f"#{el_id}"
        t = T(c["start"] + float(a.get("data-anim-at", 0)))
        d = a.get("data-anim-duration", "0.5")
        if kind == "fade-in":
            out.append(f"tl.fromTo('{sel}',{{opacity:0}},{{opacity:1,duration:{d},ease:'power2.out'}},{t});")
        elif kind == "slide-in":
            dist = float(a.get("data-anim-distance", 80))
            fr = a.get("data-anim-from", "left")
            prop = "x" if fr in ("left", "right") else "y"
            sign = -1 if fr in ("left", "top") else 1
            out.append(f"tl.fromTo('{sel}',{{opacity:0,{prop}:{sign * dist}}},{{opacity:1,{prop}:0,duration:{d},ease:'power3.out'}},{t});")
        elif kind == "kinetic-chars":
            s = a.get("data-anim-stagger", "0.04")
            out.append(f"tl.from('{sel} .char',{{opacity:0,y:28,scale:0.85,duration:{d},ease:'power3.out',stagger:{s}}},{t});")
        elif kind == "count-up":
            fmt = a.get("data-anim-format", "d")
            out.append(f"(function(){{const o={{v:{a['data-anim-from']}}};tl.to(o,{{v:{a['data-anim-to']},duration:{d},ease:'power2.out',onUpdate:function(){{const el=document.querySelector('{sel}');if(el)el.textContent=__fmt(o.v,'{fmt}');}}}},{t});}})();")
        elif kind == "grow-x":
            out.append(f"tl.fromTo('{sel}',{{width:0}},{{width:{a['data-anim-target-w']},duration:{d},ease:'power3.out'}},{t});")
        elif kind == "scale-pop":
            out.append(f"tl.fromTo('{sel}',{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:{d},ease:'back.out(1.7)'}},{t});")
        elif kind == "blur-in":
            out.append(f"tl.fromTo('{sel}',{{opacity:0,filter:'blur(18px)'}},{{opacity:1,filter:'blur(0px)',duration:{d},ease:'power2.out'}},{t});")
        elif kind == "mask-reveal":
            out.append(f"tl.fromTo('{sel}',{{clipPath:'inset(0 100% 0 0)'}},{{clipPath:'inset(0 0% 0 0)',duration:{d},ease:'power3.inOut'}},{t});")
        else:
            raise ValueError(kind)
    return out


js = []
hosts = []
SFX = []  # (nombre, tiempo, volumen)
prev_layout = FULL
for c in CARDS:
    x, y, w, h = c["host"]
    dur = c["end"] - c["start"]
    hosts.append(
        f'<div id="card-{c["id"]}" class="card-host clip" data-card-id="{c["id"]}" data-start="{c["start"]:.4f}" data-duration="{dur:.4f}" data-track-index="2" '
        f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;visibility:hidden;opacity:0;">\n'
        f'<div class="card" data-card-id="{c["id"]}"><div class="root {c["root_class"]}">{c["body"]}\n</div></div>\n</div>'
    )
    (PUB / "cards" / f'{c["id"]}.html').write_text(
        f'<div class="card" data-card-id="{c["id"]}"><div class="root {c["root_class"]}">{c["body"]}\n</div></div>\n', encoding="utf-8")

    hs = f".card-host[data-card-id=\"{c['id']}\"]"
    js.append(f"// {c['id']}")
    # Cambio de encuadre del video
    lay = c["layout"]
    if lay is not None and lay != prev_layout:
        tt = T(max(0, c["start"] - 0.35))
        SFX.append(("whoosh", max(0, c["start"] - 0.45), 0.55))
        js.append(f"tl.set('#video-wrap',{{zIndex:{5 if lay is PIP else 0}}},{tt if lay is PIP else T(c['start'])});")
        js.append(f"tl.to('#video-wrap',{{x:{lay['x']},y:{lay['y']},scale:{lay['scale']},clipPath:'{lay['clipPath']}',duration:0.55,ease:'power3.inOut'}},{tt});")
        prev_layout = lay
    enter = "{opacity:0,x:-40},{opacity:1,x:0" if c["host"] == HOST_LEFT else "{opacity:0},{opacity:1"
    js.append(f"tl.set('{hs}',{{visibility:'visible'}},{T(c['start'])});")
    js.append(f"tl.fromTo('{hs}',{enter},duration:0.35,ease:'power2.out'}},{T(c['start'])});")
    js.extend(compile_anims(c))
    if c["extra_js"]:
        js.append(c["extra_js"].replace("T(29.36+4.4)", T(29.36 + 4.4)).replace("T(29.36+4.55)", T(29.36 + 4.55)))
    if c["end"] < TOTAL - 0.01:
        js.append(f"tl.to('{hs}',{{opacity:0,duration:0.25,ease:'power2.in'}},{T(c['end'] - 0.25)});")
        js.append(f"tl.set('{hs}',{{visibility:'hidden'}},{T(c['end'])});")

# Punch-in en cada corte de silencio (disimula el salto): alterna 1.0 ↔ 1.14
cuts = json.loads((ROOT / "cuts.json").read_text())
acc, cut_times = 0.0, []
for a, b in cuts[:-1]:
    acc += b - a
    cut_times.append(acc)
js.append("// punch-ins")
js.append(f"tl.set('#video-zoom',{{scale:1}},0);")
for i, ct in enumerate(cut_times):
    js.append(f"tl.set('#video-zoom',{{scale:{1.14 if i % 2 == 0 else 1.0}}},{T(ct)});")
# Al final del video, escondo el wrapper para el cierre
js.append(f"tl.to('#video-wrap',{{opacity:0,duration:0.3}},{T(VIDEO_DUR - 0.3)});")

# Efectos puntuales (tiempos de composición)
SFX += [
    ("swipe", 0.15, 0.35), ("pop", 4.41, 0.45), ("swipe", 41.7, 0.35), ("swipe", 45.3, 0.35), ("pop", 45.46, 0.45),
    ("pop", 9.0, 0.4), ("pop", 21.0, 0.35), ("pop", 24.1, 0.35), ("pop", 26.2, 0.4),
    ("pop", 33.66, 0.5), ("tick", 35.8, 0.35),
    ("pop", 51.46, 0.45), ("ding", 53.45, 0.45), ("pop", 58.25, 0.4),
    ("tick", 60.2, 0.3), ("tick", 62.5, 0.3), ("pop", 65.06, 0.35), ("pop", 65.91, 0.35),
    ("swipe", 67.0, 0.35), ("tick", 73.7, 0.3), ("swipe", 76.3, 0.35), ("tick", 77.55, 0.3),
    ("pop", 81.0, 0.45), ("ding", 81.85, 0.5),
]
SFX_LEN = {"whoosh": 1.2, "swipe": 1.0, "pop": 0.7, "tick": 0.5, "ding": 2.48}
SFX.sort(key=lambda x: x[1])
track_end = {}
audio_tags = []
for i, (name, t0, vol) in enumerate(SFX):
    d = SFX_LEN[name]
    tr = next(k for k in range(4, 20) if track_end.get(k, -1) <= t0)
    track_end[tr] = t0 + d
    audio_tags.append(f'<audio id="sfx-{i:02d}-{name}" src="audio/sfx_{name}.mp3" data-start="{T(t0)}" data-duration="{d}" data-track-index="{tr}" data-volume="{round(vol * 0.45, 3)}"></audio>')
bed_auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
    {"t": 0, "v": 0}, {"t": 0.5, "v": 0.26}, {"t": 81.4, "v": 0.26}, {"t": 81.9, "v": 0.6}, {"t": 84.0, "v": 0.6}, {"t": TOTAL, "v": 0}]}]})
audio_tags.insert(0, f"<audio id=\"music-bed\" src=\"audio/bgm_drums.mp3\" data-start=\"0\" data-duration=\"{TOTAL}\" data-track-index=\"3\" data-automation=\"{html_escape(bed_auto)}\"></audio>")
AUDIO = "\n  ".join(audio_tags)

CSS = (ROOT / "style.css").read_text(encoding="utf-8")
html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<style>
{CSS}
</style>
</head>
<body>
<div id="stage" data-composition-id="talking-head-recut" data-start="0" data-duration="{TOTAL}" data-fps="{FPS}" data-width="1920" data-height="1080">
  <div class="bg-fill"></div>
  <div class="video-wrapper" id="video-wrap">
    <div id="video-zoom">
      <video id="bg-video" src="input-video.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{VIDEO_DUR}" data-track-index="1"></video>
    </div>
  </div>
{chr(10).join(hosts)}
  {AUDIO}
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    window.__fmt = function (v, fmt) {{
      if (fmt === 'es2') return Number(v).toFixed(2).replace('.', ',');
      if (fmt === 'esd') return String(Math.round(v)).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, '.');
      return String(Math.round(v));
    }};
    window.gsap.defaults({{ lazy: false }});
    const tl = window.gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in js)}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["talking-head-recut"] = tl;
  }})();
  </script>
</div>
</body>
</html>
"""
(PUB / "index.html").write_text(html, encoding="utf-8")
print("ok", len(CARDS), "tarjetas,", len(cut_times), "punch-ins")
