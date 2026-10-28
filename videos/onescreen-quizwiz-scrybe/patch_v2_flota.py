"""Parche: capa gráfica de la v2 en estilo Flota IA (máscara, rebote, trazos, barrido) + fuente qwzGen nueva + subtítulos oscuros sobre tarjetas blancas."""
from pathlib import Path
f = Path(__file__).parent / "build_v2.py"
s = f.read_text(encoding="utf-8")

# 1) fuente qwzGen
s = s.replace('seg(T_el, "vid", "qwzGen", 2.4, 100, "55% 50%")                          # el quiz aparece en 269,8 s = palabra "arma"',
              'seg(T_el, "vid", "qwzGen", 2.08, 100, "55% 50%")                         # el quiz aparece en 244,9 s de la grabación = palabra "esa"')
s = s.replace('seg(T_esa, "vid", "qwzGen", 2.4 + (T_esa - T_el), 150, "73% 42%")', 'seg(T_esa, "vid", "qwzGen", 2.08 + (T_esa - T_el), 150, "73% 42%")')
s = s.replace('seg(EV("en", 3), "vid", "qwzGen", 5.5, 150, "73% 45%")', 'seg(EV("en", 3), "vid", "qwzGen", 5.4, 150, "73% 45%")')

# 2) capa gráfica estilo Flota
i = s.index("# palabras sobre el material")
j = s.index("# subtítulos")
new = '''# capa gráfica estilo Flota IA ("Apple", estilo-onescreen/05_MOTION.md): titulares que suben por máscara, nodos con rebote, trazos que se dibujan, barrido
YF = {"16": 0.62, "9": 0.56, "45": 0.60}[FMT]


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


overlay("o1", EV("scribe"), lock("o1", "Scrybe", "Graba y transcribe en tiempo real.", SCR_ICO, EV("scribe")))
overlay("o2", EV("quizwiz"), lock("o2", "QuizWiz", "Genera exámenes con IA en segundos.", QZ_ICO, EV("quizwiz")))
overlay("o4", EV("segundos"), '<span class="mk"><span class="big rw">en segundos</span></span>', dur=1.3)
mask_rise("#o4 .rw", EV("segundos"), 0.7)

# anillo con check que se dibuja al decir "resultados" (línea redonda, trazo dibujado como los íconos de Flota)
tR = EV("resultados")
els.append(f'<div id="chk" class="clip chk" data-start="{tR:.4f}" data-duration="1.6" data-track-index="3"><svg viewBox="0 0 120 120" width="{round(H * 0.17)}" height="{round(H * 0.17)}">'
           f'<circle cx="60" cy="60" r="52" pathLength="1"/><path d="M34 62 L53 80 L88 42" pathLength="1"/></svg></div>')
js.append(f'tl.fromTo("#chk circle",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.7,ease:"power2.inOut"}},{tR:.4f});')
js.append(f'tl.fromTo("#chk path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.inOut"}},{tR + 0.45:.4f});')
js.append(f'tl.to("#chk",{{opacity:0,x:-60,duration:0.35,ease:"power2.in"}},{tR + 1.25:.4f});')

'''
s = s[:i] + new + s[j:]

# 3) tarjetas blancas
a1 = '''            body = '<div class="wl" id="%s-a">Una IA que <span id="%s-w" class="strk">adivina</span></div>' % (cid, cid)
            t_strike = EV("adivine")
            js.append(f'tl.fromTo("#{cid}-a",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.21,ease:"power3.out"}},{s["t"] + 0.08:.4f});')
            js.append(f'tl.fromTo("#{cid}-w",{{backgroundSize:"0% 6px"}},{{backgroundSize:"100% 6px",duration:0.25,ease:"power2.out"}},{t_strike:.4f});')
            js.append(f'tl.to("#{cid}-a",{{opacity:0.35,duration:0.2}},{t_strike + 0.25:.4f});')'''
b1 = '''            body = '<div class="mk"><div class="wl rw" id="%s-a">Una IA que <span id="%s-w" class="strk">adivina</span></div></div>' % (cid, cid)
            t_strike = EV("adivine")
            js.append(f'tl.fromTo("#{cid}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"power3.inOut"}},{s["t"]:.4f});')
            mask_rise(f"#{cid}-a", s["t"] + 0.18, 0.7)
            js.append(f'tl.fromTo("#{cid}-w",{{backgroundSize:"0% 6px"}},{{backgroundSize:"100% 6px",duration:0.45,ease:"power2.inOut"}},{t_strike:.4f});')
            js.append(f'tl.to("#{cid}-a",{{opacity:0.35,duration:0.2}},{t_strike + 0.5:.4f});')'''
assert a1 in s
s = s.replace(a1, b1)
a2 = '''            body = '<div class="wl" id="%s-a">Solicita tu <b>demo</b> aquí</div>' % cid
            js.append(f'tl.fromTo("#{cid}-a",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.21,ease:"power3.out"}},{s["t"] + 0.08:.4f});')'''
b2 = '''            body = '<div class="mk"><div class="wl rw" id="%s-a">Solicita tu <span class="dm">demo<span class="ul2" id="%s-u"></span></span> aquí</div></div>' % (cid, cid)
            js.append(f'tl.fromTo("#{cid}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"power3.inOut"}},{s["t"]:.4f});')
            mask_rise(f"#{cid}-a", s["t"] + 0.18, 0.7)
            js.append(f'tl.fromTo("#{cid}-u",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},{EV("demo") + 0.1:.4f});')'''
assert a2 in s
s = s.replace(a2, b2)

# 4) CSS
old = ".big{{font-family:'Rubik';font-weight:700;font-size:{BIG}px;color:#fff;text-shadow:0 5px 22px rgba(0,0,0,.55);letter-spacing:-0.02em}}"
assert old in s
s = s.replace(old, old.replace("letter-spacing:-0.02em}}", "letter-spacing:-0.03em;display:inline-block}}") + """
.mk{{display:block;overflow:hidden;padding:0.08em 0.1em 0.14em}} .rw{{display:inline-block}}
.scrim{{position:absolute;left:0;top:{round(H * 0.30)}px;width:{W}px;height:{round(H * 0.70)}px;background:linear-gradient(180deg,rgba(8,0,18,0) 0%,rgba(8,0,18,.62) 100%);pointer-events:none}}
.ul{{display:block;height:5px;width:100%;margin-top:10px;background:#7d00ba;border-radius:3px;transform-origin:0 50%}}
.dm{{position:relative;display:inline-block;font-weight:700}} .ul2{{position:absolute;left:0;bottom:-0.12em;height:0.07em;width:100%;background:#3976ff;border-radius:3px;transform-origin:0 50%}}
.chk{{position:absolute;left:0;top:{round(H * 0.36)}px;width:{W}px;display:flex;justify-content:center}} .chk svg{{overflow:visible;filter:drop-shadow(0 4px 14px rgba(0,0,0,.5))}}
.chk circle,.chk path{{fill:none;stroke:#fff;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 2;stroke-dashoffset:1}}""")

# 5) subtítulos oscuros sobre tarjetas blancas
a3 = '''        caps_html.append(f'<div class="clip cap" data-start="{t0:.4f}" data-duration="{max(t1 - t0, 0.2):.4f}" data-track-index="5">{txt}</div>')'''
b3 = '''        blanco = any(sg["kind"] == "white" and sg["t"] - 0.05 <= t0 < sg["t1"] for sg in SEG)
        caps_html.append(f'<div class="clip cap{" capd" if blanco else ""}" data-start="{t0:.4f}" data-duration="{max(t1 - t0, 0.2):.4f}" data-track-index="5">{txt}</div>')'''
assert a3 in s
s = s.replace(a3, b3)
s = s.replace("pointer-events:none}}\n\"\"\"\nhtml", "pointer-events:none}}\n.capd{{color:#1a1a1a;text-shadow:none}}\n\"\"\"\nhtml")
f.write_text(s, encoding="utf-8")
print("parche aplicado")
