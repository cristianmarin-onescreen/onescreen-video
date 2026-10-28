"""build_rental3: diagramación variada tipo lettering de Apple con cámara 3D (perspective + z/rotación de GSAP).
D: letras gigantes que se encogen a encabezado mientras la bifurcación se levanta del piso; E: DaaS enorme con monedas que orbitan en 3D;
F: 'mensual' centrado con fila de pagos; tarjetas que llegan desde la profundidad; N centrado. Fin de la plantilla 'título izquierda / gráfico derecha'."""
from pathlib import Path
f = Path(__file__).parent / "build_rental3.py"
s = f.read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# ── F: texto centrado grande (se arma en el bloque 3D de abajo); se quita el tx de la izquierda
i = s.index('f1 = tx(T["cuota"] - 0.1')
j = s.index("\n", s.index('rise(f"#{f1} .rw"'))
s = s[:i] + "# (texto de F: ver bloque 3D)" + s[j:]
# G: texto a la derecha en horizontal
rep('g = tx(T["toda"], tG1, [(\'<span class="l">Toda tu</span>\', S2 * 1.4), (\'<span class="b">institución</span>\', S1)], "bl")',
    'g = tx(T["toda"], tG1, [(\'<span class="l">Toda tu</span>\', S2 * 1.4), (\'<span class="b">institución</span>\', S1)], "bl", (f"left:auto;right:{SAFE[\'r\']}px;text-align:right" if FMT == "16" else ""))')
# N: centrado
rep('S2 * 1.05)], "bl")\nrise(f"#{n1} .rw", tN0 + 0.15, 0.75, 0.16)', 'S2 * 1.05)], "c")\nrise(f"#{n1} .rw", tN0 + 0.15, 0.75, 0.16)')
rep('x=(W - SAFE["r"] - 430 if FMT == "16" else None), y=(190 if FMT == "16" else None), w=(430 if FMT == "16" else None), h=(300 if FMT == "16" else None)',
    'x=((W - 344) // 2 if FMT == "16" else None), y=(105 if FMT == "16" else None), w=(344 if FMT == "16" else None), h=(240 if FMT == "16" else None)')

# ── D, E y F-gráfico: se reemplazan por escenas 3D
a = s.index('# D · "hay dos caminos": una sola pantalla')
b = s.index('# H–L · "muchas ventajas"')
NEW3D = r'''
# ══ lettering con cámara 3D (perspective, z, rotación) ═════════════════════════════════════════════
BIGF = {"16": 300, "9": 190, "45": 190}[FMT]


def lets(word, cls=""):
    return f'<span class="{cls}">' + "".join(f'<span class="lt">{c}</span>' if c != " " else '<span class="lt">&nbsp;</span>' for c in word) + "</span>"


def big(i, html, size, css, color="#fff"):
    return f'<div id="{i}" class="big" style="font-size:{size}px;color:{color};{css}">{html}</div>'


def w3(i, t0, t1, inner):
    els.append(f'<div id="{i}" class="clip w3" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3"><div class="wd">{inner}</div></div>')


def flip(sel, t, d=0.9, stag=0.05, frm=-95):
    js.append(f'tl.fromTo("{sel}",{{rotationX:{frm},y:{round(H * 0.05)},opacity:0,transformPerspective:1300,transformOrigin:"50% 100%"}},{{rotationX:0,y:0,opacity:1,duration:{d},ease:"power4.out",stagger:{stag}}},{t:.4f});')


def camera(sel, t, d, z=-300, rx=0, ry=0):
    js.append(f'tl.fromTo("{sel}",{{z:{z},rotationX:{rx},rotationY:{ry}}},{{z:0,rotationX:0,rotationY:0,duration:{d},ease:"power3.out"}},{t:.4f});')


SHD = "text-shadow:0 3px 26px rgba(0,0,0,.45)"

# D · "hay dos caminos": DOS / caminos. gigantes; se encogen a encabezado y la bifurcación se levanta del piso (azul)
bgs(T["hay"], T["daas"], ACC)
gD = nid("g")
tcL, tcR = T["primero0"], T["o2"]
top0 = SAFE["t"]
dl1 = big(f"{gD}a", lets("Dos", "l"), BIGF, f"left:{SAFE['l']}px;top:{top0}px")
dl2 = big(f"{gD}b", lets("caminos.", "b"), BIGF, f"right:{SAFE['r']}px;top:{top0 + round(BIGF * 0.88)}px;text-align:right")
FW = {"16": 800, "9": W - 2 * SAFE["l"], "45": W - 2 * SAFE["l"]}[FMT]
FH = round(FW * 740 / 800)
FY = {"16": (H - FH) // 2 + 70, "9": SAFE["t"] + 230, "45": SAFE["t"] + 150}[FMT]
fork = (pth("M400 174V230C400 320 170 270 170 358", 'class="dl"') + pth("M400 174V230C400 320 630 270 630 358", 'class="dl"')
        + '<g class="nd s0"><circle cx="400" cy="100" r="74" fill="#3976ff"/>' + pth("M358 78H442V122H358Z", 'class="s1"') + pth("M400 122V138M372 138H428", 'class="s1"') + '</g>'
        + '<g transform="translate(170 440)"><g class="nd nL"><circle r="82" fill="#3976ff"/>' + pth("M-40 -40H-22L-6 14H40L52 -22H-18", 'class="cL"')
        + '<circle cx="-2" cy="42" r="8" fill="#fff" stroke="none"/><circle cx="36" cy="42" r="8" fill="#fff" stroke="none"/></g></g>'
        + '<g transform="translate(630 440)"><g class="nd nR"><circle r="82" fill="#3976ff"/>' + pth("M-46 -30H46V46H-46Z", 'class="cR"') + pth("M-46 -4H46", 'class="cR"') + pth("M-20 -48V-22M20 -48V-22", 'class="cR"') + '</g></g>'
        + '<text class="lb lbL" x="170" y="600" text-anchor="middle">Comprarla</text><text class="lb lbR" x="630" y="600" text-anchor="middle">Arrendarla</text>'
        + '<g class="nd pill"><g transform="translate(40 640) scale(1.55)" stroke="#fff" stroke-width="2.3"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8"/><path d="M8 12.5h5"/></g>'
        + '<text x="100" y="684" style="font:600 40px Rubik;fill:#fff;stroke:none;letter-spacing:-0.02em">Contáctanos</text></g>'
        + '<circle id="pkL" r="15" fill="#fff" stroke="none" opacity="0"/><circle id="pkR" r="15" fill="#fff" stroke="none" opacity="0"/>')
forkdiv = (f'<div id="{gD}f" class="fk" style="left:{(W - FW) // 2}px;top:{FY}px;width:{FW}px;height:{FH}px"><svg viewBox="0 0 800 740" width="100%" height="100%" fill="none" stroke="#fff" '
           f'stroke-width="14" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{fork}</svg></div>')
w3(gD, T["hay"] + 0.05, T["daas"], f'<div id="{gD}t" class="ttl">{dl1}{dl2}</div>{forkdiv}')
camera(f"#{gD} .wd", T["hay"] + 0.05, 1.3, -260, 7, -8)
flip(f"#{gD}a .lt", T["hay"] + 0.2, 0.9, 0.07)
flip(f"#{gD}b .lt", T["caminos"] - 0.1, 0.9, 0.045)
# las letras se encogen a encabezado (esquina) y la bifurcación sube del piso
js.append(f'tl.to("#{gD}t",{{scale:0.36,z:-60,transformOrigin:"{SAFE["l"]}px {top0}px",duration:0.9,ease:"power3.inOut"}},{tcL - 0.55:.4f});')
js.append(f'tl.fromTo("#{gD}f",{{rotationX:64,y:240,opacity:0,transformPerspective:1500,transformOrigin:"50% 100%"}},{{rotationX:0,y:0,opacity:1,duration:1.0,ease:"power3.out"}},{tcL - 0.45:.4f});')
pop(f"#{gD} .s0", tcL - 0.1); draw(f"#{gD} .s1", tcL, 0.7, 0.1)
draw(f"#{gD} .dl", tcL + 0.1, 0.7, 0.18)
pop(f"#{gD} .nL", tcL + 0.45); draw(f"#{gD} .cL", tcL + 0.6, 0.7, 0.1)
js.append(f'tl.fromTo("#{gD} .lbL",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{tcL + 0.65:.4f});')
packet(f"#{gD} #pkL", [(400, 170), (400, 232), (285, 300), (170, 365)], tcL + 0.1, 0.55)
pop(f"#{gD} .pill", T["contactarnos"] - 0.1, 0.5, 0.7)
pop(f"#{gD} .nR", tcR + 0.15); draw(f"#{gD} .cR", tcR + 0.3, 0.7, 0.1)
js.append(f'tl.fromTo("#{gD} .lbR",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{tcR + 0.35:.4f});')
packet(f"#{gD} #pkR", [(400, 170), (400, 232), (515, 300), (630, 365)], tcR - 0.1, 0.55)
js.append(f'tl.to("#{gD} .wd",{{rotationY:-5,duration:{T["daas"] - tcR - 0.4:.2f},ease:"sine.inOut"}},{tcR:.4f});')
gone(f"#{gD}", T["daas"] - 0.25)

# E · "DaaS": palabra enorme en el centro y monedas que la ORBITAN en 3D (pasan por detrás y por delante) (morado)
bgs(T["daas"], T["por"], PUR)
gE = nid("g")
DS = round(BIGF * 1.3)
R_ = {"16": 430, "9": 300, "45": 300}[FMT]
coins = "".join(f'<div class="coin" style="transform:rotateY({a_}deg) translateZ({R_}px)"><i></i></div>' for a_ in (0, 120, 240))
dE = big(f"{gE}a", lets("DaaS", "b"), DS, f"left:0;width:{W}px;text-align:center;top:{round(H * 0.5 - DS * 0.55)}px")
sE = big(f"{gE}s", '<span class="l">modelo de</span> <span class="b">arrendamiento</span>', S2, f"left:0;width:{W}px;text-align:center;top:{round(H * 0.5 + DS * 0.5)}px;letter-spacing:-0.02em")
orb = f'<div class="orb0" style="left:{W // 2}px;top:{round(H * 0.5)}px"><div class="orb">{coins}</div></div>'
w3(gE, T["daas"] + 0.05, T["por"], dE + sE + orb)
camera(f"#{gE} .wd", T["daas"] + 0.05, 1.5, -400, 10, 0)
flip(f"#{gE}a .lt", T["daas"] + 0.15, 0.95, 0.09)
js.append(f'tl.fromTo("#{gE} .orb",{{rotationY:-40,opacity:0}},{{rotationY:320,opacity:1,duration:{T["por"] - T["daas"] - 0.3:.2f},ease:"power2.inOut"}},{T["daas"] + 0.2:.4f});')
js.append(f'tl.fromTo("#{gE}s",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.6,ease:"power3.out"}},{T["arrendamiento"] - 0.5:.4f});')
gone(f"#{gE}", T["por"] - 0.25)

# F · "una cuota mensual": 'mensual' enorme y centrado sobre el plano, fila de pagos que se va marcando
gF = nid("g")
FS = BIGF
cx_ = {"16": 0.42, "9": 0.40, "45": 0.40}[FMT]
fa = big(f"{gF}a", lets("Una cuota", "l"), round(FS * 0.30), f"left:0;width:{W}px;text-align:center;top:{round(H * cx_ - FS * 0.2)}px;{SHD}")
fb = big(f"{gF}b", lets("mensual", "b"), FS, f"left:0;width:{W}px;text-align:center;top:{round(H * cx_ + FS * 0.12)}px;{SHD}")
nT = 12
gp = 12 if FMT == "16" else 8
sz_ = min(78, (W - SAFE["l"] - SAFE["r"] - (nT - 1) * gp) // nT)
rowW = nT * sz_ + (nT - 1) * gp
row = "".join(pth(f"M{k * (sz_ + gp)} 0H{k * (sz_ + gp) + sz_}V{sz_}H{k * (sz_ + gp)}Z", 'class="fr"') + pth(f"M{k * (sz_ + gp) + sz_ * .25:.0f} {sz_ * .52:.0f}L{k * (sz_ + gp) + sz_ * .43:.0f} {sz_ * .72:.0f}L{k * (sz_ + gp) + sz_ * .76:.0f} {sz_ * .28:.0f}", 'class="fc"') for k in range(nT))
rdiv = (f'<div id="{gF}r" class="fk" style="left:{(W - rowW) // 2}px;top:{H - SAFE["b"] - sz_ - 10}px;width:{rowW}px;height:{sz_}px"><svg viewBox="0 0 {rowW} {sz_}" width="100%" height="100%" fill="none" stroke="#fff" '
        f'stroke-width="{max(6, sz_ // 8)}" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{row}</svg></div>')
w3(gF, T["cuota"] - 0.15, T["llenar"], fa + fb + rdiv)
camera(f"#{gF} .wd", T["cuota"] - 0.15, 1.1, -220, 9, 5)
flip(f"#{gF}a .lt", T["cuota"] - 0.1, 0.8, 0.04)
flip(f"#{gF}b .lt", T["cuota"] + 0.12, 0.9, 0.055)
draw(f"#{gF} .fr", T["cuota"] + 0.3, 0.5, 0.03)
draw(f"#{gF} .fc", T["cuota"] + 0.8, 0.3, (T["llenar"] - T["cuota"] - 1.9) / nT)
gone(f"#{gF}", T["llenar"] - 0.2)

'''
s = s[:a] + NEW3D + s[b:]

# ── tarjetas: titular con lettering centrado y llegada desde la profundidad
i = s.index('hv = tx(tV0 + 0.1')
j = s.index("\n", s.index('rise(f"#{hv} .rw"'))
HV = '''HS_ = {"16": 118, "9": 104, "45": 100}[FMT]
hvid = nid("g")
hv = big(f"{hvid}a", lets("Muchas ", "l") + lets("ventajas.", "b"), HS_, f"left:0;width:{W}px;text-align:center;top:{SAFE['t']}px", "#0b0b14")
w3(hvid, tV0 + 0.05, tM0, hv)
els[-1] = els[-1].replace('class="clip w3"', 'class="clip w3 hvx"')
flip(f"#{hvid}a .lt", tV0 + 0.15, 0.85, 0.04)
js.append(f'tl.fromTo("#{hvid}a .b",{{color:"#0b0b14"}},{{color:"#3976ff",duration:0.5,ease:"none"}},{tV0 + 0.8:.4f});')
gone(f"#{hvid}", tM0 - 0.25)'''
s = s[:i] + HV + s[j:]
rep('''    js.append(f'tl.fromTo("#{i},#{i}v",{{opacity:0,y:50,scale:0.88}},{{opacity:1,y:0,scale:1,duration:0.55,ease:"back.out(1.5)"}},{tt - 0.05:.4f});')''',
    '''    ox_ = f"{CW // 2}px {CH // 2}px"; oxv_ = f"{CW // 2 - 6}px {CH // 2 - 6}px"
    ry0 = round((k - 1.5) * 38)
    for sel_, o_ in ((f"#{i}", ox_), (f"#{i}v", oxv_)):
        js.append(f'tl.fromTo("{sel_}",{{opacity:0,z:-1200,rotationY:{ry0},y:90,transformPerspective:1500,transformOrigin:"{o_}"}},{{opacity:1,z:0,rotationY:0,y:0,duration:0.95,ease:"power3.out"}},{tt - 0.05:.4f});')
        js.append(f'tl.to("{sel_}",{{rotationY:{round(-(k - 1.5) * 5)},duration:{max(tM0 - tt - 1.5, 0.5):.2f},ease:"sine.inOut"}},{tt + 0.9:.4f});')''')

# CSS 3D
a_ = ".ln{{display:block}} .gfx{{position:absolute}}"
assert a_ in s
CSS3 = (".w3{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;perspective:1500px;perspective-origin:50% 50%}} .wd{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-style:preserve-3d}} "
        ".ttl{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-style:preserve-3d}} .fk{{position:absolute}} "
        ".big{{position:absolute;font-family:'Rubik';line-height:0.9;letter-spacing:-0.045em;white-space:nowrap;transform-style:preserve-3d}} .big .b{{font-weight:700}} .big .l{{font-weight:300}} .lt{{display:inline-block}} "
        ".orb0{{position:absolute;width:0;height:0;transform-style:preserve-3d;transform:rotateX(-16deg)}} .orb{{position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d}} "
        ".coin{{position:absolute;left:-60px;top:-60px;width:120px;height:120px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}} "
        ".coin i{{display:block;width:62px;height:62px;border-radius:50%;border:9px solid #7d00ba;box-sizing:border-box}} ")
s = s.replace(a_, CSS3 + a_, 1)
f.write_text(s, encoding="utf-8")
print("ok r3e")
