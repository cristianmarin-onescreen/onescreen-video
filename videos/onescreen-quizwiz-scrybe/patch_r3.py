"""Rental v3: titular corto en 'dos caminos', nodo de cuota antes de la cuadrícula, chip de tarjeta bajo el video, subtítulo más abajo en 16:9."""
from pathlib import Path
f = Path(__file__).parent / "build_rental.py"
s = f.read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


rep("""'Dos caminos <span class="ac">para tener tu OneScreen.</span>', LAY["HY1"], t0 + 0.15, size=round(LAY["HS"] * 0.86)))""",
    """'Dos <span class="ac">caminos</span>.', LAY["HY1"], t0 + 0.15, size=round(LAY["HS"] * 1.0)))""")
rep("    p.append(conn(cid, 3, a[0], a[1] + nd // 2 + 58, a[0], cy2 - 52, tcn - 0.35, 0.5, ACC, False))\n", "")
# cuota: nodo + cuadrícula más arriba + titular inferior
rep("""    # cuadrícula de pantallas que se llena
    tl_ = EV("llenar"); tp = EV("pantallas")""",
    """    ncx = W // 2
    nyy = {"16": 560, "9": 900, "45": 700}[FMT]
    p.append(node(cid, 5, ncx, nyy, "cal", "Cada mes", t0 + 0.5, PUR, nd=LAY["ND"] + 10))
    js.append(f'tl.to("#{cid}-n5,#{cid}-l5",{{opacity:0,scale:0.6,duration:0.35,ease:"power2.in"}},{EV("llenar") - 0.2:.4f});')
    # cuadrícula de pantallas que se llena
    tl_ = EV("llenar"); tp = EV("pantallas")""")
rep('gy0 = {"16": 400, "9": 680, "45": 480}[FMT]', 'gy0 = {"16": 340, "9": 680, "45": 480}[FMT]')
rep("""{"16": 800, "9": 1330, "45": 960}[FMT], EV("toda") + 0.1, size=round(LAY["HS"] * 0.8)))""", """{"16": 770, "9": 1330, "45": 960}[FMT], EV("toda") + 0.1, size=round(LAY["HS"] * 0.72)))""")
# tarjetas: chip bajo el video
rep('padding-top:{vh + 60}px">\'', 'padding-top:{vh + 122}px">\'')
rep("""style="border-color:{cols_clr[i]};top:{vh - 46}px">{line_icon(ic, 54, cols_clr[i], 1.8)}""", """style="border-color:{cols_clr[i]};top:{vh + 14}px">{line_icon(ic, 46, cols_clr[i], 1.8)}""")
rep('vh = {"16": 240, "9": 190, "45": 150}[FMT]; ch = {"16": 520, "9": 400, "45": 330}[FMT]', 'vh = {"16": 200, "9": 190, "45": 150}[FMT]; ch = {"16": 510, "9": 470, "45": 400}[FMT]')
rep(".cd2 .ci{{position:absolute;left:24px;width:92px;height:92px;", ".cd2 .ci{{position:absolute;left:24px;width:84px;height:84px;")
rep('CAPY = {"16": "84%", "9": "49%", "45": "70%"}[FMT]', 'CAPY = {"16": "89%", "9": "49%", "45": "70%"}[FMT]')
f.write_text(s, encoding="utf-8")
print("ok patch_r3")
