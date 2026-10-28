# Cambios v3: sin "Cuando…" en la flota, más margen en el diagnóstico de Isabel,
# contacto debajo del nombre en cada agente + firma de contacto fija en su sección.
import re, os
os.chdir(os.path.join(os.path.dirname(__file__), "..", "compositions", "frames"))

def edit(p, pairs, idc=None):
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert a in s, (p, a[:80])
        s = s.replace(a, b)
    if idc:
        m = list(re.finditer(r"\n(\s*)</div>\n\s*</div>\n\s*<script", s))[-1]
        s = s[: m.start()] + "\n" + m.group(1) + "  " + idc + s[m.start():]
    open(p, "w", encoding="utf-8").write(s)

def sub(p, pattern, repl, flags=0):
    s = open(p, encoding="utf-8").read()
    s2 = re.sub(pattern, repl, s, flags=flags)
    assert s2 != s, (p, pattern[:60])
    open(p, "w", encoding="utf-8").write(s2)

# 2 · quitar la línea y los "Cuando…"
sub("02-flota-odoo.html", r'\n\s*<svg[^>]*id="s2-journey">.*?</svg>', "", re.S)
sub("02-flota-odoo.html", r'\n\s*<div[^>]*class="s2-when in"[^>]*>[^<]*</div>', "")
edit("02-flota-odoo.html", [
    ('          FX.draw(tl, q("#s2-journey [data-draw]"), T(22.0), 1.4);\n', ""),
    ('          FX.up(tl, q(".s2-when"), T(22.3), { y: 20, stagger: 0.32, d: 0.45 });\n', ""),
    ('FX.out(tl, ["#s2-t1c", "#s2-journey", ".s2-when", ".s2-tag"]', 'FX.out(tl, ["#s2-t1c", ".s2-tag"]'),
])

CHAT = '<svg><use href="#chat" /></svg>'
BELL = '<svg viewBox="0 0 48 48" style="stroke:currentColor;fill:none;stroke-width:3.6;stroke-linecap:round;stroke-linejoin:round"><path d="M12 34V22a12 12 0 0 1 24 0v12l4 4H8z" /><path d="M20 42h8" /></svg>'
CLOCK = '<svg viewBox="0 0 48 48" style="stroke:currentColor;fill:none;stroke-width:3.6;stroke-linecap:round"><circle cx="24" cy="24" r="17" /><path d="M24 14v10l7 5" /></svg>'
NAME150 = "font-size: 150px; font-weight: 700; letter-spacing: -0.045em; line-height: 0.95; }"
NAME136 = "font-size: 136px; font-weight: 700; letter-spacing: -0.045em; line-height: 0.95; }"

# 3 · Iván
edit("03-ivan.html", [
    (NAME150, NAME136),
    ("#s3-body { left: 136px; top: 520px;", "#s3-body { left: 136px; top: 600px;"),
    ("#s3-funnel { left: 134px; top: 640px; width: 360px; height: 240px; }", "#s3-funnel { left: 134px; top: 740px; width: 300px; height: 200px; }"),
    ("#s3-sale { left: 520px; top: 735px;", "#s3-sale { left: 460px; top: 810px;"),
    ("#s3-ring { left: 134px; top: 640px; width: 200px; height: 200px; }", "#s3-ring { left: 134px; top: 745px; width: 180px; height: 180px; }"),
    ("#s3-247 { left: 360px; top: 680px; font-size: 120px;", "#s3-247 { left: 345px; top: 770px; font-size: 110px;"),
    ("#s3-pill1 { left: 134px; top: 920px; }", "#s3-pill1 { left: 134px; top: 490px; }"),
    ("#s3-tiles .tile { min-height: 320px; }", "#s3-tiles .tile { min-height: 300px; }"),
    ("        #s3-pill2 { left: 50%; top: 925px; }\n", ""),
    ('FX.pop(tl, "#s3-pill1", T(51.9), { from: 0.85 });', 'FX.pop(tl, "#s3-pill1", T(42.8), { from: 0.85 });'),
    ('"#s3-247", "#s3-pill1"], T(52.45), { x: -60, d: 0.35, stagger: 0.02 });',
     '"#s3-247", "#s3-pill1"], T(52.45), { x: -60, d: 0.35, stagger: 0.02 });\n          FX.up(tl, "#s3-idc", T(52.75), { x: -30, y: 0 });'),
    ('          tl.fromTo("#s3-pill2", { opacity: 0, xPercent: -50, y: 30 }, { opacity: 1, xPercent: -50, y: 0, duration: 0.5, ease: "back.out(1.6)" }, T(78.98));\n', ""),
], idc='<div id="s3-idc" class="idc in"><b>Iván Andrade</b><span>' + CHAT + '+57 316 3260059 <i>WhatsApp</i></span></div>')
sub("03-ivan.html", r'\n\s*<div[^>]*id="s3-pill2"[^\n]*</div>', "")

# 4 · Isaac — el número pasa de la escena final a debajo del nombre
edit("04-isaac.html", [
    (NAME150, NAME136),
    ("#s4-body { left: 136px; top: 520px;", "#s4-body { left: 136px; top: 600px;"),
    ("#s4-mega { left: 134px; top: 660px; }", "#s4-mega { left: 134px; top: 730px; }"),
    ("#s4-pill { left: 134px; top: 900px; }", "#s4-pill { left: 134px; top: 490px; }"),
    ("y = 720 + ((i * 37) % 5 - 2) * 26;", "y = 790 + ((i * 37) % 5 - 2) * 26;"),
    ("{ attr: { cx: 290, cy: 722 } }", "{ attr: { cx: 290, cy: 792 } }"),
    ('FX.out(tl, ["#s4-kick", "#s4-name", "#s4-body", "#s4-mega"], T(88.4), { x: -60, d: 0.35, stagger: 0.02 });',
     'FX.pop(tl, "#s4-pill", T(81.4), { from: 0.85 });\n          FX.out(tl, ["#s4-kick", "#s4-name", "#s4-body", "#s4-mega", "#s4-pill"], T(88.4), { x: -60, d: 0.35, stagger: 0.02 });\n          FX.up(tl, "#s4-idc", T(88.7), { x: -30, y: 0 });'),
    ('          FX.up(tl, "#s4-pill", T(125.62), { y: 30 });\n', ""),
], idc='<div id="s4-idc" class="idc in"><b>Isaac Alvarado</b><span>' + CHAT + '+57 315 1513328 <i>Línea para clientes</i></span></div>')
s = open("04-isaac.html", encoding="utf-8").read()
pill = re.search(r'\n\s*<div[^>]*id="s4-pill"[^\n]*</div>', s).group(0)
s = s.replace(pill, "")
s = re.sub(r'(\n\s*<div[^>]*id="s4-body"[^\n]*</div>)', lambda m: m.group(1) + pill, s, count=1)
open("04-isaac.html", "w", encoding="utf-8").write(s)

# 5 · Isabel — más margen entre subtítulo y cuadro de diagnóstico
edit("05-isabel.html", [
    (NAME150, NAME136),
    ("#s5-body, #s5-body2 { left: 136px; top: 520px; font-size: 36px; max-width: 700px; }", "#s5-body, #s5-body2 { left: 136px; top: 600px; font-size: 34px; max-width: 700px; }"),
    ("#s5-scr { left: 134px; top: 610px; width: 380px; height: 240px;", "#s5-scr { left: 134px; top: 760px; width: 320px; height: 190px;"),
    ("#s5-alert, #s5-ok { position: absolute; left: 130px; top: 60px; width: 120px; height: 120px; }", "#s5-alert, #s5-ok { position: absolute; left: 106px; top: 38px; width: 100px; height: 100px; }"),
    ("#s5-checks { left: 560px; top: 640px;", "#s5-checks { left: 500px; top: 785px;"),
    ("#s5-pill { left: 134px; top: 920px; }", "#s5-pill { left: 134px; top: 490px; }"),
    ("        #s5-pill2 { left: 50%; top: 925px; }\n", ""),
    ("{ y: 0 }, { y: 226, duration: 0.9", "{ y: 0 }, { y: 176, duration: 0.9"),
    ('FX.pop(tl, "#s5-pill", T(131.0), { from: 0.85 });', 'FX.pop(tl, "#s5-pill", T(129.3), { from: 0.85 });'),
    ('"#s5-pill", "#s5-bub"], T(144.2), { x: -60, d: 0.35, stagger: 0.02 });',
     '"#s5-pill", "#s5-bub"], T(144.2), { x: -60, d: 0.35, stagger: 0.02 });\n          FX.up(tl, "#s5-idc", T(144.5), { x: -30, y: 0 });'),
    ('          tl.fromTo("#s5-pill2", { opacity: 0, xPercent: -50, y: 30 }, { opacity: 1, xPercent: -50, y: 0, duration: 0.5, ease: "back.out(1.6)" }, T(158.6));\n', ""),
], idc='<div id="s5-idc" class="idc in"><b>Isabel Alarcón</b><span>' + CHAT + '+57 316 7764571 <i>WhatsApp</i></span></div>')
sub("05-isabel.html", r'\n\s*<div[^>]*id="s5-pill2"[^\n]*</div>', "")

# 6 · Harby
edit("06-harby.html", [
    ("#s6-body { left: 136px; top: 420px;", "#s6-body { left: 136px; top: 510px;"),
    ("#s6-gov { left: 134px; top: 560px; width: 220px; height: 220px; }", "#s6-gov { left: 134px; top: 630px; width: 200px; height: 200px; }"),
    (".s6-doc { top: 580px; }", ".s6-doc { top: 640px; }"),
    ("#s6-pill { left: 134px; top: 900px; }", "#s6-pill { left: 134px; top: 405px; }"),
    ("#s6-radar { left: 200px; top: 250px; width: 720px; height: 720px; }", "#s6-radar { left: 220px; top: 250px; width: 640px; height: 640px; }"),
    ('FX.pop(tl, "#s6-pill", T(165.6), { from: 0.85 });', 'FX.pop(tl, "#s6-pill", T(163.5), { from: 0.85 });'),
    ('".s6-doc", "#s6-pill"], T(168.0), { x: -60, d: 0.35, stagger: 0.02 });',
     '".s6-doc", "#s6-pill"], T(168.0), { x: -60, d: 0.35, stagger: 0.02 });\n          FX.up(tl, "#s6-idc", T(168.3), { x: -30, y: 0 });'),
], idc='<div id="s6-idc" class="idc in"><b>Harby</b><span>' + BELL + 'Está en Odoo <i>Licitaciones</i></span></div>')

# 7 · Marco
edit("07-marco.html", [
    ("#s7-body { left: 136px; top: 420px;", "#s7-body { left: 136px; top: 510px;"),
    (".s7-n { top: 520px; width: 230px; }", ".s7-n { top: 580px; width: 230px; }\n        #s7-pill { left: 134px; top: 405px; }"),
    ('d="M150 790 H830"', 'd="M150 845 H830"'),
    ('cx="350" cy="790"', 'cx="350" cy="845"'), ('cx="560" cy="790"', 'cx="560" cy="845"'), ('cx="770" cy="790"', 'cx="770" cy="845"'),
    ("left: 134px; top: 773px; }", "left: 134px; top: 828px; }"),
    ("#s7-stamp { left: 140px; top: 880px; }", "#s7-stamp { left: 140px; top: 925px; }"),
    ('FX.up(tl, "#s7-body", T(185.86), { y: 18 });', 'FX.pop(tl, "#s7-pill", T(185.5), { from: 0.85 });\n          FX.up(tl, "#s7-body", T(185.86), { y: 18 });'),
])
sub("07-marco.html", r'(\n\s*<div[^>]*id="s7-body"[^\n]*</div>)',
    lambda m: m.group(1) + '\n          <div id="s7-pill" class="pill in">' + CLOCK + '<span>Logística</span><b>Pronto disponible</b></div>')
print("ok")
