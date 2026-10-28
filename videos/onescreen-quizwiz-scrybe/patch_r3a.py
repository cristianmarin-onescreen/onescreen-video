"""build_rental3: íconos dentro de la línea, 'Contáctanos' en el mismo bloque, sin planos bajo las tarjetas."""
from pathlib import Path
f = Path(__file__).parent / "build_rental3.py"
s = f.read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# ícono con id propio
rep('def icon(name, size, sw=2):', 'def icon(name, size, sw=2, iid=""):')
rep("""return f'<svg class="ic" viewBox""", """return f'<svg id="{iid}" class="ic" viewBox""")
rep('''style="stroke:#fff;stroke-width:{sw}">{ps}</svg>\'''', '''style="stroke:#fff;stroke-width:{sw};margin-left:0.18em;vertical-align:-0.08em">{ps}</svg>\'''')
# D: Contáctanos como segunda línea del mismo bloque
a = s.index("d1 = tx(T[\"primero0\"] + 0.15")
b = s.index("vid(\"m4\", T[\"o2\"], T[\"daas\"], 0.5)")
s = s[:a] + '''d1 = tx(T["primero0"] + 0.15, T["o2"], [('<span class="b">Comprarla</span>', S1), ('<span class="l">Contáctanos</span>' + icon("chat", round(S2 * 0.9), 2, "icChat"), S2)], "bl")
rise(f"#{d1} .ln:nth-child(1) .rw", T["primero0"] + 0.15, 0.7)
rise(f"#{d1} .ln:nth-child(2) .rw", T["contactarnos"] - 0.1, 0.6)
js.append(f'tl.fromTo("#icChat path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power2.inOut",stagger:0.1}},{T["contactarnos"] + 0.1:.4f});')
gone(f"#{d1} .rw", T["o2"] - 0.25)
''' + s[b:]
# H y M: sin plano debajo de la tarjeta
rep('vid("r4", T["hay1"], T["primero1"], 0.0)          # debajo de la tarjeta (la tarjeta lo cubre: queda para Premiere)\n', '')
rep('vid("m4", tM0, tN0 + 0.15, 1.2)\n', '')
# I: moneda en la línea de "usas"
a = s.index('ii = tx(T["pagas"] - 0.05')
b = s.index("# J ·")
s = s[:a] + '''ii = tx(T["pagas"] - 0.05, tJ0, [('<span class="l">Pagas por lo que</span>', S2 * 1.2), ('<span class="b">usas</span>' + icon("coin", round(S1 * 0.62), 2, "icCoin"), S1)], "bl")
rise(f"#{ii} .rw", T["pagas"] - 0.05, 0.7, 0.14); gone(f"#{ii} .rw", tJ0 - 0.25)
js.append(f'tl.fromTo("#icCoin path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.9,ease:"power2.inOut",stagger:0.1}},{T["pagas"] + 0.5:.4f});')
js.append(f'tl.fromTo("#icCoin",{{rotationY:0}},{{rotationY:360,duration:1.0,ease:"power2.inOut",transformOrigin:"50% 50%"}},{T["pagas"] + 1.2:.4f});')
''' + s[b:]
# J: flechas que giran junto a "Siempre"
a = s.index('jj = tx(tJ0 - 0.05')
b = s.index("# K ·")
s = s[:a] + '''jj = tx(tJ0 - 0.05, tK0, [('<span class="b">Siempre</span>' + icon("refresh", round(S1 * 0.62), 2, "icRef"), S1), ('<span class="l">actualizada</span>', S1 * 0.62)], "bl")
rise(f"#{jj} .rw", tJ0 - 0.05, 0.7, 0.14); gone(f"#{jj} .rw", tK0 - 0.25)
js.append(f'tl.fromTo("#icRef path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power2.inOut",stagger:0.1}},{tJ0 + 0.4:.4f});')
js.append(f'tl.fromTo("#icRef",{{rotation:0}},{{rotation:720,duration:{tK0 - tJ0 - 0.9:.3f},ease:"power1.inOut",transformOrigin:"50% 50%"}},{tJ0 + 0.8:.4f});')
''' + s[b:]
# K: auricular junto a "prioritario", sin subrayado
a = s.index('kk = tx(tK0 - 0.05')
b = s.index("# L ·")
s = s[:a] + '''kk = tx(tK0 - 0.05, tL0, [('<span class="l">Soporte técnico</span>', S2 * 1.2), ('<span class="b">prioritario</span>' + icon("head", round(S1 * 0.62), 2, "icHead"), S1)], "bl")
rise(f"#{kk} .rw", tK0 - 0.05, 0.7, 0.14); gone(f"#{kk} .rw", tL0 - 0.25)
js.append(f'tl.fromTo("#icHead path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.9,ease:"power2.inOut",stagger:0.1}},{T["prioritario"]:.4f});')
''' + s[b:]
# L: escudo junto a "encargamos"
a = s.index('ll1 = tx(tL0 - 0.05')
b = s.index("# M ·")
s = s[:a] + '''ll = tx(tL0 - 0.05, tM0, [('<span class="l">Si sufre algún daño,</span>', S2 * 1.1), ('<span class="b">nosotros nos</span>', S1 * 0.78), ('<span class="b">encargamos</span>' + icon("shield", round(S1 * 0.55), 2, "icShield"), S1 * 0.78)], "bl")
rise(f"#{ll} .ln:nth-child(1) .rw", tL0 - 0.05, 0.7)
rise(f"#{ll} .ln:nth-child(2) .rw", T["nosotros"] - 0.05, 0.7)
rise(f"#{ll} .ln:nth-child(3) .rw", T["encargamos"] - 0.05, 0.7)
js.append(f'tl.fromTo("#icShield path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.9,ease:"power2.inOut",stagger:0.1}},{T["encargamos"] + 0.3:.4f});')
gone(f"#{ll} .rw", tM0 - 0.25)
''' + s[b:]
rep('.ic path{{stroke-dasharray:1 2;stroke-dashoffset:0}}', '.ic path{{stroke-dasharray:1 2;stroke-dashoffset:0}} .ic{{display:inline-block;filter:drop-shadow(0 3px 14px rgba(0,0,0,.45))}}')
f.write_text(s, encoding="utf-8")
print("ok r3a")
