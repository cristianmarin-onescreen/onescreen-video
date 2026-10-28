"""Arma D:\\OneScreen\\Contenido\\2026\\10. Octubre\\QuizWiz y Scrybe\\Proyecto\\proj\\index.html: video de pauta Scrybe + QuizWiz (16:9, ~33 s).

Tiempos en segundos de video (voz Hale arranca en D=0.10). Planos de apoyo ya coloreados con grade/pipeline.py
y copiados a proj/media/. Paleta: fondo blanco, azul #3976ff, negro #1a1a1a, acento #7d00ba (sin amarillo).
"""
import os
import re
from pathlib import Path

FMT = os.environ.get("FMT") or ("9" if os.environ.get("VERT") == "1" else "16")
VERT = FMT != "16"
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[FMT]
PROJ = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\proj" + {"16": "", "9": "_v", "45": "_45"}[FMT])
ASSETS = PROJ / "assets"
FPS = 24
TOTAL = 34.0
D = 0.10


def svg(name, cls):
    s = (ASSETS / name).read_text(encoding="utf-8-sig")
    s = re.sub(r'<\?xml[^>]*\?>', "", s)
    s = re.sub(r'\s(id|data-name)="[^"]*"', "", s)
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)


WORD = svg("onescreen-wordmark.svg", "wm")
SCR = svg("Scrybe.svg", "ico")
QZ = svg("QuizWiz.svg", "ico")

# (id, archivo, inicio, fin, desplazamiento de zoom "x%")
SHOTS = [
    ("v01", "s01_pizarra_perfil", 0.0, 2.5),
    ("v02", "s02_pizarra_frente", 2.5, 5.1),
    ("v03", "s03_home", 5.1, 8.5),
    ("v04", "s04_pen", 8.5, 11.3),
    ("v05", "s05_habla", 11.3, 13.5),
    ("v06", "s06_qr", 13.5, 17.4),
    ("v07", "s07_qr2", 20.9, 22.4),
    ("v08", "s08_ok", 22.4, 26.1),
    ("v09", "s09_cajas", 26.1, 27.5),
    ("v10", "s10_caja_t7", 27.5, 29.9),
]

els = []   # html de elementos en orden
js = []    # líneas de la timeline


def clip(cid, start, end, track, inner, cls=""):
    els.append(f'<div id="{cid}" class="clip ov {cls}" data-start="{start:.2f}" data-duration="{end-start:.2f}" data-track-index="{track}">{inner}</div>')


def words(text, wid):
    """Palabras separadas en spans; **x** = acento azul."""
    out = []
    for i, w in enumerate(text.split(" ")):
        if w.startswith("*") and w.endswith("*"):
            out.append(f'<span class="w acc" id="{wid}-{i}">{w.strip("*")}</span>')
        else:
            out.append(f'<span class="w" id="{wid}-{i}">{w}</span>')
    return " ".join(out), len(out)


def cap(cid, start, end, text, pos="bl", track=3, delay=0.05, stagger=0.07, extra=""):
    inner, n = words(text, cid)
    clip(cid, start, end, track, f'<div class="cap {pos}" id="{cid}-b">{inner}{extra}</div>')
    js.append(f'tl.fromTo("#{cid}-b",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.28,ease:"power3.out"}},{start+delay:.2f});')
    js.append(f'tl.fromTo("#{cid} .w",{{opacity:0,y:26}},{{opacity:1,y:0,duration:0.3,ease:"power3.out",stagger:{stagger}}},{start+delay+0.06:.2f});')
    js.append(f'tl.to("#{cid}-b",{{opacity:0,y:-18,duration:0.16,ease:"power2.in"}},{end-0.18:.2f});')


# ── Planos de apoyo ─────────────────────────────────────────────────────────
for i, (vid, f, a, b) in enumerate(SHOTS):
    els.append(f'<video id="{vid}" class="clip" src="media/{f}.mp4" muted playsinline data-start="{a:.2f}" data-duration="{b-a:.2f}" data-track-index="1"></video>')
    s0, s1 = (1.0, 1.09) if i % 2 == 0 else (1.09, 1.0)
    js.append(f'tl.fromTo("#{vid}",{{scale:{s0}}},{{scale:{s1},duration:{b-a:.2f},ease:"none"}},{a:.2f});')

# ── 1–2: pregunta ───────────────────────────────────────────────────────────
cap("c1", 0.0, 2.5, "¿Cuánto tarda tu docente en *armar* *un* *examen?*", delay=0.12)
cap("c2", 2.5, 5.1, "¿Y quién le asegura que *evalúa* *lo* *que* *enseñó?*", delay=0.02)

# ── 3: Scrybe + Start ───────────────────────────────────────────────────────
clip("c3", 5.1, 8.5, 3, f"""
<div class="card tr" id="c3-card">
  <div class="lock">{SCR}<span class="nm">Scrybe</span></div>
  <div class="lbl" id="c3-lbl">Grabar la clase</div>
  <div class="btn start" id="c3-btn"><span class="tri"></span>Start</div>
  <div class="rec" id="c3-rec"><i></i>REC <b id="c3-t">00:00</b></div>
</div>""")
js += [
    'tl.fromTo("#c3-card",{opacity:0,x:80},{opacity:1,x:0,duration:0.35,ease:"power3.out"},5.2);',
    'tl.fromTo("#c3-btn",{scale:1,opacity:1},{scale:0.88,duration:0.08,ease:"power2.in"},7.40);',
    'tl.to("#c3-btn",{scale:1,duration:0.18,ease:"back.out(3)"},7.48);',
    'tl.fromTo("#c3-btn",{opacity:1},{opacity:0,duration:0.12},7.62);',
    'tl.fromTo("#c3-rec",{opacity:0,scale:0.8},{opacity:1,scale:1,duration:0.2,ease:"back.out(2)"},7.65);',
    'tl.fromTo("#c3-rec i",{opacity:1},{opacity:0.25,duration:0.35,repeat:2,yoyo:true,ease:"none"},7.7);',
    'tl.to("#c3-card",{opacity:0,x:60,duration:0.18,ease:"power2.in"},8.3);',
]

# ── 4: QuizWiz arma el examen ───────────────────────────────────────────────
clip("c4", 8.5, 11.3, 3, f"""
<div class="card tr" id="c4-card">
  <div class="lock">{QZ}<span class="nm">QuizWiz</span></div>
  <div class="lbl" id="c4-lbl">Examen en segundos</div>
  <div class="q" id="c4-q1"><i class="ck">✓</i><span>Opción múltiple</span></div>
  <div class="q" id="c4-q2"><i class="ck">✓</i><span>Verdadero o falso</span></div>
  <div class="q" id="c4-q3"><i class="ck">✓</i><span>Completar espacios</span></div>
</div>""")
js += [
    'tl.fromTo("#c4-card",{opacity:0,x:80,scale:0.94},{opacity:1,x:0,scale:1,duration:0.4,ease:"back.out(1.6)"},8.52);',
    'tl.fromTo("#c4-q1",{opacity:0,x:30},{opacity:1,x:0,duration:0.25,ease:"power3.out"},9.3);',
    'tl.fromTo("#c4-q2",{opacity:0,x:30},{opacity:1,x:0,duration:0.25,ease:"power3.out"},9.9);',
    'tl.fromTo("#c4-q3",{opacity:0,x:30},{opacity:1,x:0,duration:0.25,ease:"power3.out"},10.5);',
    'tl.to("#c4-card",{opacity:0,x:60,duration:0.18,ease:"power2.in"},11.1);',
]

# ── 5: tus palabras / tus ejemplos ──────────────────────────────────────────
clip("c5", 11.3, 13.5, 3, """
<div class="chips" id="c5-w"><span class="chip c-blue" id="c5-a">Tus palabras</span><span class="chip c-purple" id="c5-b">Tus ejemplos</span></div>""")
js += [
    'tl.fromTo("#c5-a",{opacity:0,scale:0.6,y:30},{opacity:1,scale:1,y:0,duration:0.3,ease:"back.out(2.4)"},11.5);',
    'tl.fromTo("#c5-b",{opacity:0,scale:0.6,y:30},{opacity:1,scale:1,y:0,duration:0.3,ease:"back.out(2.4)"},12.2);',
    'tl.to("#c5-w",{opacity:0,y:-16,duration:0.16,ease:"power2.in"},13.3);',
]

# ── 6: QR ───────────────────────────────────────────────────────────────────
clip("c6", 13.5, 17.4, 3, """
<div class="qr-badge" id="c6-a"><b>Un QR</b></div>
<div class="cap bl" id="c6-b"><span class="w">Cada estudiante, <span class="acc">desde su celular</span></span></div>""")
js += [
    'tl.fromTo("#c6-a",{opacity:0,scale:0.5,rotation:-6},{opacity:1,scale:1,rotation:0,duration:0.34,ease:"back.out(2.6)"},14.4);',
    'tl.fromTo("#c6-b",{opacity:0,y:40},{opacity:1,y:0,duration:0.3,ease:"power3.out"},15.1);',
    'tl.to("#c6-a,#c6-b",{opacity:0,duration:0.16,ease:"power2.in"},17.2);',
]

# ── 7: escena blanca "IA que adivina" vs "tu clase" ─────────────────────────
els.append('<div id="wh1" class="clip white" data-start="17.40" data-duration="3.50" data-track-index="2"><div class="stack">'
           '<div class="big strike" id="wh1-a">Una IA que <span id="wh1-w">adivina</span></div>'
           '<div class="big" id="wh1-b">Tu <span class="acc">clase</span></div></div></div>')
js += [
    'tl.fromTo("#wh1",{clipPath:"circle(0% at 50% 50%)"},{clipPath:"circle(150% at 50% 50%)",duration:0.38,ease:"power3.inOut"},17.4);',
    'tl.fromTo("#wh1-a",{opacity:0,y:50},{opacity:1,y:0,duration:0.32,ease:"power3.out"},17.65);',
    'tl.fromTo("#wh1-w",{backgroundSize:"0% 8px"},{backgroundSize:"100% 8px",duration:0.28,ease:"power2.out"},19.1);',
    'tl.to("#wh1-a",{opacity:0.28,duration:0.25},19.3);',
    'tl.fromTo("#wh1-b",{opacity:0,y:50,scale:0.9},{opacity:1,y:0,scale:1,duration:0.34,ease:"back.out(2)"},20.55);',
]
# ── 8: en segundos ──────────────────────────────────────────────────────────
cap("c7", 20.9, 22.4, "*En* *segundos*", delay=0.45)
# ── 9: resultados ───────────────────────────────────────────────────────────
cap("c8", 22.4, 26.1, "Los resultados por fin *dicen* *algo*", delay=0.1,
    extra='<span class="tick" id="c8-t">✓</span>')
js.append('tl.fromTo("#c8-t",{scale:0,rotation:-40},{scale:1,rotation:0,duration:0.4,ease:"back.out(3)"},25.4);')
# ── 10–11: implementación ───────────────────────────────────────────────────
cap("c9", 26.1, 27.5, "Esto es solo *el* *principio*", delay=0.05)
cap("c10", 27.5, 29.9, "Nosotros lo *implementamos* por ti", delay=0.05)

# ── 12: cierre ──────────────────────────────────────────────────────────────
els.append(f"""<div id="end" class="clip white" data-start="29.90" data-duration="{TOTAL-29.9:.2f}" data-track-index="2"><div class="endc">
  <div class="logos" id="end-l"><div class="lock sm">{SCR}<span class="nm">Scrybe</span></div><span class="plus">+</span><div class="lock sm">{QZ}<span class="nm">QuizWiz</span></div></div>
  <div class="big sm" id="end-h">Solicita tu <span class="acc">demo</span> aquí</div>
  <div class="btn cta" id="end-b">Solicitar demo</div>
  <div class="by" id="end-by">{WORD}</div>
</div></div>""")
js += [
    'tl.fromTo("#end",{clipPath:"circle(0% at 50% 50%)"},{clipPath:"circle(150% at 50% 50%)",duration:0.4,ease:"power3.inOut"},29.9);',
    'tl.fromTo("#end-l",{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:"power3.out"},30.2);',
    'tl.fromTo("#end-h",{opacity:0,y:40},{opacity:1,y:0,duration:0.35,ease:"power3.out"},30.5);',
    'tl.fromTo("#end-b",{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.4,ease:"back.out(2.4)"},31.3);',
    'tl.fromTo("#end-by",{opacity:0},{opacity:1,duration:0.4,ease:"power2.out"},31.8);',
    'tl.to("#end-b",{scale:1.06,duration:0.45,yoyo:true,repeat:3,ease:"sine.inOut"},32.2);',
]

CSS = r"""
@font-face { font-family:'Rubik'; src:url('fonts/Rubik-variable-latin.woff2') format('woff2'); font-weight:300 900; font-display:block; }
@font-face { font-family:'Manrope'; src:url('fonts/Manrope-variable-latin.woff2') format('woff2'); font-weight:200 800; font-display:block; }
:root { --blue:#3976ff; --ink:#1a1a1a; --purple:#7d00ba; --white:#fafafa; }
*{box-sizing:border-box} html,body{margin:0;padding:0;width:1920px;height:1080px;overflow:hidden;background:#fafafa;font-family:'Manrope',sans-serif;color:var(--ink)}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;background:#fafafa}
video{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;transform-origin:50% 50%}
.ov{position:absolute;left:0;top:0;width:1920px;height:1080px;pointer-events:none}
.white{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#fafafa;display:flex;align-items:center;justify-content:center}
.acc{color:var(--blue)}
.cap{position:absolute;background:var(--white);border-radius:30px;padding:30px 48px;font-family:'Rubik';font-weight:700;font-size:68px;line-height:1.12;letter-spacing:-0.02em;color:var(--ink);box-shadow:0 18px 50px rgba(0,0,0,.28);max-width:1560px}
.cap.bl{left:96px;bottom:96px}
.cap .w{display:inline-block}
.cap .tick{display:inline-flex;align-items:center;justify-content:center;width:84px;height:84px;margin-left:22px;border-radius:50%;background:var(--blue);color:#fff;font-size:54px;vertical-align:middle}
.card{position:absolute;background:var(--white);border-radius:32px;padding:38px 46px;width:560px;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.card.tr{right:96px;top:110px}
.lock{display:flex;align-items:center;gap:18px}
.lock .ico{height:64px;width:auto;fill:var(--blue);color:var(--blue)}
.lock .ico path{fill:var(--blue)}
.lock .nm{font-family:'Rubik';font-weight:700;font-size:64px;letter-spacing:-0.02em;color:var(--ink)}
.lock.sm .ico{height:84px} .lock.sm .nm{font-size:84px}
.lbl{font-family:'Manrope';font-weight:800;font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:var(--purple);margin:22px 0 18px}
.btn{display:inline-flex;align-items:center;gap:16px;font-family:'Rubik';font-weight:700;font-size:52px;background:var(--blue);color:#fff;border-radius:999px;padding:18px 54px}
.btn .tri{width:0;height:0;border-left:30px solid #fff;border-top:19px solid transparent;border-bottom:19px solid transparent}
.rec{position:absolute;left:46px;bottom:38px;display:flex;align-items:center;gap:14px;font-family:'Rubik';font-weight:700;font-size:44px;color:var(--ink);opacity:0}
.rec i{display:block;width:26px;height:26px;border-radius:50%;background:#e5322d}
.q{display:flex;align-items:center;gap:18px;font-family:'Manrope';font-weight:700;font-size:32px;padding:14px 0;border-top:2px solid #e8e8ee;opacity:0}
.q .ck{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;background:var(--blue);color:#fff;font-style:normal;font-size:28px}
.chips{position:absolute;left:96px;bottom:96px;display:flex;gap:24px}
.chip{font-family:'Rubik';font-weight:700;font-size:70px;border-radius:999px;padding:22px 56px;color:#fff;box-shadow:0 18px 50px rgba(0,0,0,.28)}
.c-blue{background:var(--blue)} .c-purple{background:var(--purple)}
.qr-badge{position:absolute;right:120px;top:130px;background:var(--purple);color:#fff;font-family:'Rubik';font-size:110px;padding:20px 64px;border-radius:36px;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.stack{display:flex;flex-direction:column;align-items:center;gap:36px}
.big{font-family:'Rubik';font-weight:700;font-size:150px;letter-spacing:-0.03em;line-height:1.05;color:var(--ink);text-align:center}
.big.sm{font-size:96px}
.strike span{background-image:linear-gradient(var(--purple),var(--purple));background-repeat:no-repeat;background-position:0 55%;background-size:0% 8px}
.endc{display:flex;flex-direction:column;align-items:center;gap:40px}
.logos{display:flex;align-items:center;gap:44px} .plus{font-family:'Rubik';font-weight:700;font-size:80px;color:var(--purple)}
.btn.cta{font-size:56px;padding:26px 80px}
.by{display:flex;justify-content:center;color:var(--ink);margin-top:8px}
.wm{height:44px;width:auto;fill:currentColor}
"""

CSS = CSS.replace("1920px;height:1080px", f"{W}px;height:{H}px")

# ── Zonas seguras (px) por formato: texto, logos y botones SIEMPRE dentro; el video sí sangra ──
# 9:16 (Reels/TikTok/Shorts): guías de Meta para anuncios en Reels: 14 % arriba, 35 % abajo, 6 % a los lados;
#   más ~190 px a la derecha por la columna de botones. Caja segura ≈ 823×960 (x 65–888, y 288–1248).
# 4:5 (feed): 80 px por lado y arriba, 100 abajo; contenido dentro del recorte central 3:4 de la cuadrícula (1012 px).
# 16:9 (YouTube/LinkedIn/web): 96 px a los lados (zona de acción 5 %), 108 arriba y 120 abajo (barra de reproducción).
SAFE = {"16": dict(l=96, r=96, t=108, b=120), "9": dict(l=65, r=192, t=288, b=672), "45": dict(l=80, r=80, t=80, b=100)}[FMT]
SL, SR, ST, SB = SAFE["l"], SAFE["r"], SAFE["t"], SAFE["b"]
CSS += f"""
.cap,.cap.bl{{left:{SL}px;bottom:{SB}px;max-width:{W-SL-SR}px}}
.chips{{left:{SL}px;bottom:{SB}px;max-width:{W-SL-SR}px}}
.card.tr{{right:{SR}px;top:{ST}px}}
.qr-badge{{right:{SR}px;top:{ST}px}}
.white{{padding:{ST}px {SR}px {SB}px {SL}px}}
"""
if VERT:
    inner = W - SL - SR
    CSS += f"""
.cap{{font-size:{54 if FMT=='9' else 60}px;padding:26px 36px}}
.cap .tick{{width:64px;height:64px;font-size:40px}}
.card{{width:{inner}px;padding:34px 44px}}
.card.tr{{left:{SL}px}}
.lock .ico{{height:68px}}.lock .nm{{font-size:68px}}
.lbl{{font-size:28px}}
.btn{{font-size:52px}}.rec{{font-size:46px}}
.q{{font-size:34px}}.q .ck{{width:46px;height:46px;font-size:30px}}
.chips{{flex-wrap:wrap;gap:18px}}
.chip{{font-size:{54 if FMT=='9' else 60}px;padding:18px 40px}}
.qr-badge{{font-size:{84 if FMT=='9' else 92}px;padding:16px 48px}}
.big{{font-size:{80 if FMT=='9' else 104}px}}.big.sm{{font-size:{76 if FMT=='9' else 80}px;text-align:center}}
.logos{{flex-direction:column;gap:18px}}.plus{{font-size:56px}}
.lock.sm .ico{{height:84px}}.lock.sm .nm{{font-size:84px}}
.endc{{gap:{44 if FMT=='9' else 40}px}}.btn.cta{{font-size:52px;padding:24px 60px}}
.wm{{height:48px}}
"""

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<style>{CSS}</style>
</head>
<body>
<div id="stage" data-composition-id="quizwiz-scrybe" data-start="0" data-duration="{TOTAL}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
  {chr(10).join('  ' + e for e in els)}
  <audio id="mix" src="audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-has-audio="true"></audio>
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    window.gsap.defaults({{ lazy: false }});
    const tl = window.gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in js)}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["quizwiz-scrybe"] = tl;
  }})();
  </script>
</div>
</body>
</html>
"""
(PROJ / "index.html").write_text(html, encoding="utf-8")
print("ok", len(els), "elementos")
