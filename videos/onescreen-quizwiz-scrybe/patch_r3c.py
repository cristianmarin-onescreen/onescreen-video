"""build_rental3: escenas de motion graphics sobre fondos de color y blancos, alternados (Cris: 'variado'), junto a las de texto sobre plano."""
import re
from pathlib import Path
f = Path(__file__).parent / "build_rental3.py"
s = f.read_text(encoding="utf-8")


def rep(a, b, cnt=1):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, cnt)


def line(prefix, new):
    """reemplaza la línea completa que empieza con prefix"""
    global s
    m = re.search(r"^" + re.escape(prefix) + r".*$", s, re.M)
    assert m, prefix
    s = s[:m.start()] + new + s[m.end():]


# fondos de color
rep("def icon(name, size, sw=2, iid=\"\"):", '''def bgs(t0, t1, color, cid=None):
    """escena de fondo liso (blanco o de color) para motion graphics; entra con un barrido"""
    i = cid or nid("b")
    els.append(f'<div id="{i}" class="clip white" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="2" style="background:{color}"></div>')
    js.append(f'tl.fromTo("#{i}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"power3.inOut"}},{t0:.4f});')
    return i


INKS = "color:#0b0b14;text-shadow:none"


def icon(name, size, sw=2, iid="", col="#fff"):''')
rep('style="stroke:#fff;stroke-width:{sw};margin-left:0.18em;vertical-align:-0.08em">', 'style="stroke:{col};stroke-width:{sw};margin-left:0.18em;vertical-align:-0.08em">')
# gfx hereda el color (relleno currentColor)
rep('''style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{flt}">\'''', '''style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;color:{stroke};{flt}">\'''')
a = s.index("# ── gráficos descriptivos")
s = s[:a] + s[a:].replace('fill="#fff"', 'fill="currentColor"')

# D · azul
line('card(T["hay"], T["primero0"] + 0.55',
     '''bgs(T["hay"], T["primero0"] + 0.55, ACC)
dd = tx(T["hay"] + 0.2, T["primero0"] + 0.5, [('<span class="l">Dos</span> <span class="b">caminos.</span>', S1 * 0.86)], "bl")
rise(f"#{dd} .rw", T["hay"] + 0.25, 0.7, 0.1); gone(f"#{dd} .rw", T["primero0"] + 0.25)''')
a = s.index('gD = nid("g")')
b = s.index("# F · \"cuota mensual\"")
s = s[:a] + '''gD = nid("g")
gfx(gD, T["hay"] + 0.35, T["primero0"] + 0.55,
    pth("M280 10V120", 'class="d1"') + pth("M280 120C280 205 110 190 110 290", 'class="d1"') + pth("M280 120C280 205 450 190 450 290", 'class="d1"')
    + pth("M82 262L110 294L138 262", 'class="d1"') + pth("M422 262L450 294L478 262", 'class="d1"')
    + '<circle cx="280" cy="10" r="14" fill="currentColor" stroke="none"/>')
draw(f"#{gD} .d1", T["hay"] + 0.45, 0.85, 0.12)
gone(f"#{gD}", T["primero0"] + 0.25)
''' + s[b:]

# E · morado
line('vid("m5", T["daas"], T["por"], 1.0, 100)', 'bE = bgs(T["daas"], T["por"], PUR)')
a = s.index('gfx(gA')  # asegura que existe
s = s.replace('# ── subtítulos:', '''# E · ciclo mensual que gira junto a "DaaS"
gE = nid("g")
gfx(gE, T["daas"] + 0.2, T["por"], '<g transform="translate(70 20) scale(16)" stroke-width="0.44">' + pth("M20 12a8 8 0 1 1-2.6-5.9", 'class="e1"') + pth("M20 4v5h-5", 'class="e1"') + '</g>')
draw(f"#{gE} .e1", T["daas"] + 0.3, 0.9, 0.2)
js.append(f'tl.fromTo("#{gE} svg",{{rotation:0,transformOrigin:"50% 50%"}},{{rotation:360,duration:{T["por"] - T["daas"] - 0.5:.2f},ease:"power1.inOut"}},{T["daas"] + 0.9:.4f});')
gone(f"#{gE}", T["por"] - 0.25)
# ── subtítulos:''', 1)

# F · blanco
line('vid("m1", T["por"], T["llenar"], 1.0)', 'bgs(T["por"], T["llenar"], "#fafafa")')
rep('''f1 = tx(T["cuota"] - 0.1, T["llenar"], [('<span class="l">Una cuota</span>', S2 * 1.4), ('<span class="b">mensual</span>', S1)], "bl")''',
    '''f1 = tx(T["cuota"] - 0.1, T["llenar"], [('<span class="l">Una cuota</span>', S2 * 1.4), ('<span class="b" style="color:#3976ff">mensual</span>', S1)], "bl", INKS)''')
rep('''pth("M20 60H540V370H20Z", 'class="f1"')''', '''pth("M20 60H540V370H20Z", 'class="f1"')''')
a = s.index('gfx(gF')
b = s.index("\n", a)
s = s[:b] + ',stroke=ACC' + s[b:] if False else s
rep('''gfx(gF, T["cuota"] - 0.1, T["llenar"], ''', '''gfx(gF, T["cuota"] - 0.1, T["llenar"], stroke=ACC, inner=''')
rep("def gfx(i, t0, t1, inner, x=None", "def gfx(i, t0, t1, inner=\"\", x=None")

# I · lila
line('vid("m1", T["primero1"], tJ0, 1.8)', 'bgs(T["primero1"], tJ0, "#efe3fb")')
rep('''[('<span class="l">Pagas por lo que</span>', S2 * 1.2), ('<span class="b">usas</span>' + icon("coin", round(S1 * 0.62), 2, "icCoin"), S1)], "bl")''',
    '''[('<span class="l">Pagas por lo que</span>', S2 * 1.2), ('<span class="b" style="color:#7d00ba">usas</span>' + icon("coin", round(S1 * 0.62), 2, "icCoin", PUR), S1)], "bl", INKS)''')
rep('''gfx(gI, T["pagas"] + 0.2, tJ0, pth(''', '''gfx(gI, T["pagas"] + 0.2, tJ0, stroke=PUR, inner=pth(''')

# K · azul
line('vid("m3", tK0, tL0, 2.0)', 'bgs(tK0, tL0, ACC)')
f.write_text(s, encoding="utf-8")
print("ok r3c")
