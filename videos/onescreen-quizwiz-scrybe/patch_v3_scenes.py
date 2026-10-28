"""Parche v3: escenas de pantalla completa estilo Flota IA (titular con máscara, nodos con rebote, líneas que se dibujan con paquete de luz,
tachado, sello) en lugar de etiquetas pequeñas sobre el footage. Tres escenas: 'ia' (comparación), 'res' (resultados), 'cta'."""
from pathlib import Path
f = Path(__file__).parent / "build_v2.py"
s = f.read_text(encoding="utf-8")

# 1) línea de tiempo: escenas Flota en lugar de tarjeta blanca + s02 + s08
old = '''seg(EV("en", 2), "white", "ia")
seg(EV("mejor"), "vid", "s02", 1.3, 100)
seg(EV("en", 3), "vid", "qwzGen", 5.4, 150, "73% 45%")
seg(EV("cuando"), "vid", "s08", 0.0, 100)
seg(EV("resultados"), "vid", "s08", 1.4, 144, "78% 62%")
seg(EV("pero"), "vid", "s09", 0.0, 100)'''
new = '''seg(EV("en", 2), "white", "ia")
seg(EV("en", 3), "vid", "qwzGen", 5.4, 150, "73% 45%")
seg(EV("cuando"), "white", "res")
seg(EV("pero"), "vid", "s09", 0.0, 100)'''
assert old in s
s = s.replace(old, new)

# 2) cola más larga para que el CTA se lea completo
s = s.replace('END_SCENE = snap(words[-1]["end"] + D + 0.35)', 'END_SCENE = snap(words[-1]["end"] + D + 0.95)')

# 3) generador de escenas
helpers = r'''
# ── escenas Flota IA ─────────────────────────────────────────────────────────
INK, ACC, PUR, MUT = "#0b0b14", "#3976ff", "#7d00ba", "#9a9aae"
LAY = {"16": dict(HS=104, HY1=130, NY=520, ND=176, HY2=700, M=150, AL="left"),
       "9": dict(HS=92, HY1=300, NY=780, ND=150, HY2=1090, M=80, AL="center"),
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
    js.append(f'tl.to("#{cid}-h1",{{opacity:0.28,duration:0.3}},{tm:.4f});')
    parts.append(sc_head(cid, 2, 'Mejor usa <span class="ac">tu clase</span>.', LAY["HY2"], tm + 0.05))
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
    parts.append(sc_node(cid, 1, cx1, "cap", "Lo que enseñas", EV("evalúa") + 0.05))
    parts.append(sc_node(cid, 2, cx2, "chart", "Lo que se evalúa", EV("enseñó") + 0.05, PUR))
    tr = EV("resultados")
    parts.append(sc_conn(cid, 1, cx1, cx2, tr - 0.35, 0.6))
    d = round(LAY["ND"] * 0.7)
    parts.append(f'<div id="{cid}-rg" class="rg" style="left:{W // 2 - d // 2}px;top:{LAY["NY"] - d // 2}px;width:{d}px;height:{d}px"><svg viewBox="0 0 24 24" width="{d}" height="{d}"><circle cx="12" cy="12" r="11" pathLength="1"/><path d="M6.5 12.5l3.5 3.5 7.5-8" pathLength="1"/></svg></div>')
    js.append(f'tl.fromTo("#{cid}-rg",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.7)"}},{tr + 0.2:.4f});')
    js.append(f'tl.fromTo("#{cid}-rg circle",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.inOut"}},{tr + 0.2:.4f});')
    js.append(f'tl.fromTo("#{cid}-rg path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.4,ease:"power2.inOut"}},{tr + 0.55:.4f});')
    tf = EV("fin")
    parts.append(f'<div id="{cid}-s" class="st" style="left:{W // 2 - 330}px;top:{LAY["HY2"]}px;width:660px">Resultados que dicen algo</div>')
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


'''
anchor = "SCR_ICO, QZ_ICO = svg("
assert anchor in s
s = s.replace(anchor, helpers + anchor, 1)

# 4) rama 'white' → escenas
i = s.index('    else:\n        if s["src"] == "ia":')
j = s.index("# capa gráfica estilo Flota IA")
branch = '''    else:
        t_end = s["t1"]
        body = {"ia": scene_ia, "res": scene_res, "cta": scene_cta}[s["src"]](cid, s["t"], t_end)
        els.append(f'<div id="{cid}" class="clip white scn" data-start="{s["t"]:.4f}" data-duration="{s["dur"]:.4f}" data-track-index="2">{body}</div>')

'''
s = s[:i] + branch + s[j:]

# 5) fuera el anillo suelto sobre footage (ahora vive en la escena de resultados)
a = s.index("# anillo con check que se dibuja")
b = s.index("# subtítulos (pequeños")
s = s[:a] + s[b:]

# 6) CSS
css = """
.scn{{display:block;padding:0}}
.hd{{position:absolute;font-family:'Rubik';font-weight:700;line-height:1.02;letter-spacing:-0.04em}} .hd .ac{{color:#3976ff}}
.strk2{{background-image:linear-gradient(#7d00ba,#7d00ba);background-repeat:no-repeat;background-position:0 58%;background-size:0% 8px}}
.xm{{display:inline-block;margin-left:0.18em;vertical-align:-0.05em}} .xm svg{{overflow:visible}}
.li{{overflow:visible;fill:none;stroke-linecap:round;stroke-linejoin:round}} .li path{{stroke-dasharray:1 2;stroke-dashoffset:0}}
.nd{{position:absolute;border:6px solid;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(20,20,60,.08)}}
.nl{{position:absolute;text-align:center;font-family:'Manrope';font-weight:800;font-size:{round(H * 0.026) if FMT == '16' else 34}px;color:#0b0b14;overflow:hidden}}
.cn{{position:absolute;left:0;top:0;pointer-events:none}} .cn line{{fill:none;stroke-width:6;stroke-linecap:round;stroke-dasharray:1 2;stroke-dashoffset:1}}
.pk{{position:absolute;width:22px;height:22px;border-radius:50%;background:#3976ff;box-shadow:0 0 18px 6px rgba(57,118,255,.45);opacity:0}}
.rg{{position:absolute}} .rg circle,.rg path{{fill:none;stroke:#3976ff;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 2;stroke-dashoffset:1}}
.st{{position:absolute;border:7px solid #7d00ba;color:#7d00ba;font-family:'Manrope';font-weight:800;font-size:{round(H * 0.03) if FMT == '16' else 38}px;letter-spacing:0.08em;text-transform:uppercase;text-align:center;padding:18px 20px;border-radius:16px;background:rgba(255,255,255,.9)}}
.dm2{{position:relative;display:inline-block}} .ul2{{position:absolute;left:0;bottom:-0.06em;height:0.07em;width:100%;background:#7d00ba;border-radius:4px;transform-origin:0 50%}}
.bt{{position:absolute;display:flex;align-items:center;justify-content:center;gap:18px;height:{round(H * 0.095) if FMT == '16' else 120}px;border-radius:999px;background:#3976ff;color:#fff;font-family:'Rubik';font-weight:600;font-size:{round(H * 0.036) if FMT == '16' else 46}px;box-shadow:0 14px 34px rgba(57,118,255,.35)}}
"""
s = s.replace('.capd{{color:#1a1a1a;text-shadow:none}}\n', '.capd{{color:#1a1a1a;text-shadow:none}}\n' + css, 1)

# 7) los subtítulos oscuros sobre escenas Flota también
f.write_text(s, encoding="utf-8")
print("parche v3 aplicado")
