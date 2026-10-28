"""Rental: tarjetas de ventajas con un plano de caso de éxito cada una; ajuste de la línea de tiempo."""
from pathlib import Path
f = Path(__file__).parent / "build_rental.py"
s = f.read_text(encoding="utf-8")

# línea de tiempo
a = s.index('seg(0.0, "vid", "r1", 0.0, 100)')
b = s.index("for i, s in enumerate(SEG):")
s = s[:a] + '''seg(0.0, "vid", "r1", 0.0, 100, CLIPS["r1"].get("o", "50% 50%"))                  # "Hoy quiero que hablemos sobre tu primera aula digital"
seg(EV("tener"), "vid", "r2", 0.0, 144, CLIPS["r2"].get("o", "50% 50%"))          # "tener tu propia pantalla interactiva"
seg(EV("para"), "vid", "r3", 0.0, 100, CLIPS["r3"].get("o", "50% 50%"))           # "Para tener tu propia OneScreen"
seg(EV("hay"), "white", "paths")                                                   # "hay dos caminos" ... comprar ... "O segundo"
seg(EV("daas"), "white", "daas")
seg(EV("por"), "white", "cuota")                                                   # cuota mensual ... llenar toda tu institución
seg(EV("hay", 1), "vid", "r4", 0.0, 144, CLIPS["r4"].get("o", "50% 50%"))         # "Hay muchas ventajas"
seg(EV("primero", 1), "white", "ventajas")
seg(EV("quieres"), "white", "cta")
''' + s[b:]

# ventajas con video por tarjeta
a = s.index("def scene_ventajas")
b = s.index("def scene_cta")
new = '''def scene_ventajas(cid, t0, t1):
    wipe_in(cid, t0)
    p = []
    p.append(sc_head(cid, 1, 'Las <span class="ac">ventajas</span> de arrendar.', LAY["HY1"], t0 + 0.12, size=round(LAY["HS"] * 0.88)))
    items = [("coin", "Pagas por lo que usas", "Sin comprar de golpe", EV("pagas"), "c1"),
             ("refresh", "Siempre actualizada", "Las últimas actualizaciones", EV("siempre"), "c2"),
             ("head", "Soporte técnico prioritario", "Atención primero", EV("soporte"), "c3"),
             ("shield", "Nosotros nos encargamos", "Si sufre algún daño", EV("si"), "c4")]
    cols = 4 if FMT == "16" else 2
    cw = {"16": 400, "9": 450, "45": 450}[FMT]; vh = {"16": 200, "9": 190, "45": 150}[FMT]; ch = {"16": 450, "9": 400, "45": 330}[FMT]
    gap = 30
    gx0 = (W - (cols * cw + (cols - 1) * gap)) / 2
    gy0 = {"16": 330, "9": 560, "45": 360}[FMT]
    cols_clr = [ACC, ACC, PUR, PUR]
    for i, (ic, ti, su, tt, clip) in enumerate(items):
        x = gx0 + (i % cols) * (cw + gap); y = gy0 + (i // cols) * (ch + gap)
        p.append(f'<div id="{cid}-k{i}" class="cd2 cd" style="left:{x:.0f}px;top:{y:.0f}px;width:{cw}px;height:{ch}px;border-color:{cols_clr[i]};padding-top:{vh + 60}px">'
                 f'<div class="ci" style="border-color:{cols_clr[i]};top:{vh - 46}px">{line_icon(ic, 54, cols_clr[i], 1.8)}</div><b>{ti}</b><i>{su}</i></div>')
        els.append(f'<video id="{cid}-v{i}" class="clip cv" src="media/{clip}.mp4" muted playsinline data-start="{tt - 0.05:.4f}" data-duration="{max(t1 - tt + 0.5, 1):.4f}" data-media-start="0" data-track-index="3" '
                   f'style="left:{x + 5:.0f}px;top:{y + 5:.0f}px;width:{cw - 10}px;height:{vh}px;border-radius:22px 22px 0 0"></video>')
        js.append(f'tl.fromTo("#{cid}-k{i},#{cid}-v{i}",{{opacity:0,y:50,scale:0.88}},{{opacity:1,y:0,scale:1,duration:0.55,ease:"back.out(1.5)"}},{tt - 0.05:.4f});')
        js.append(f'tl.fromTo("#{cid}-k{i} .li path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power2.inOut",stagger:0.08}},{tt + 0.1:.4f});')
        js.append(f'tl.to("#{cid}-v{i}",{{opacity:0,x:-60,duration:0.3,ease:"power2.in"}},{t1 - 0.32:.4f});')
    scene_exit(cid, t1)
    return "".join(p)


'''
s = s[:a] + new + s[b:]
s = s.replace(".cd2 .ci{{width:112px;height:112px;border:5px solid;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:6px}}",
              ".cd2 .ci{{position:absolute;left:24px;width:92px;height:92px;border:5px solid;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}} .cv{{position:absolute;object-fit:cover;z-index:5}}")
f.write_text(s, encoding="utf-8")
print("ok patch_r1")
