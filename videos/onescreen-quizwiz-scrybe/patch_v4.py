"""Parche v4: toques táctiles, celular con cambio de foco (sin superponer), QR alineado, cámara más lenta; planos de salón (UISRAEL); sin grabaciones de pantalla."""
from pathlib import Path
here = Path(__file__).parent

# ── ui3d.py ──
u = here / "ui3d.py"
t = u.read_text(encoding="utf-8")
a = t.index("    # ── cámara ──")
b = t.index("    # lockups")
t = t[:a] + (here / "_newblock.txt").read_text(encoding="utf-8") + t[b:]
rep = [
    ('<div id="ring"><div class="in">{SCR_ICO}<span>Iniciar</span></div></div>', '<div id="ring"><div class="in">{SCR_ICO}<span>Iniciar</span></div><i class="tp"></i><i class="rp"></i></div>'),
    ('    <div id="cur1" class="cur"></div>\n', ''),
    ('<span id="bGen" class="bg">⚡ Generar Quiz</span>', '<span id="bGen" class="bg">⚡ Generar Quiz<i class="tp"></i><i class="rp"></i></span>'),
    ('<span id="bPub" class="bg sm">Publicar Quiz</span>', '<span id="bPub" class="bg sm">Publicar Quiz<i class="tp"></i><i class="rp"></i></span>'),
    ('  <div id="cur2" class="cur"></div>\n', ''),
    ("left:{W / 2 - 180 + 1900}px;top:{H / 2 - 370 + 140}px", "left:{W / 2 - 180 + QX + 150}px;top:{H / 2 - 370 + 90}px"),
    ('{qr_svg(cid, 250, "p")}', '{qr_svg(cid, 220, "p")}'),
    ('.vq{position:absolute;left:55px;top:200px;background:#fff;padding:10px;border-radius:6px;transform:rotate(-4deg)}',
     '.vq{position:absolute;left:46px;top:238px;background:#fff;padding:10px;border-radius:6px;width:240px;height:240px}'),
    ('.br.tl{left:50px;top:190px;border-right:0;border-bottom:0}.br.tr{right:50px;top:190px;border-left:0;border-bottom:0}.br.bl{left:50px;top:470px;border-right:0;border-top:0}.br.brr{right:50px;top:470px;border-left:0;border-top:0}',
     '.br.tl{left:36px;top:228px;border-right:0;border-bottom:0}.br.tr{right:36px;top:228px;border-left:0;border-bottom:0}.br.bl{left:36px;top:432px;border-right:0;border-top:0}.br.brr{right:36px;top:432px;border-left:0;border-top:0}'),
    ('.scan{position:absolute;left:58px;right:58px;top:200px;', '.scan{position:absolute;left:46px;right:46px;top:240px;'),
    ('.cur{position:absolute',
     '.tp{position:absolute;left:50%;top:50%;width:76px;height:76px;margin:-38px 0 0 -38px;border-radius:50%;background:rgba(125,0,186,.2);border:3px solid rgba(125,0,186,.65);box-shadow:0 6px 20px rgba(60,20,110,.3);opacity:0;pointer-events:none;z-index:30}\n'
     '.rp{position:absolute;left:50%;top:50%;width:76px;height:76px;margin:-38px 0 0 -38px;border-radius:50%;border:4px solid #7d00ba;opacity:0;pointer-events:none;z-index:29}\n.bg{position:relative}\n.cur{position:absolute'),
]
for o, n in rep:
    assert o in t, o[:50]
    t = t.replace(o, n, 1)
u.write_text(t, encoding="utf-8")

# ── build_v2.py ──
f = here / "build_v2.py"
s = f.read_text(encoding="utf-8")
a = s.index('seg(0.0, "vid", "stress", 0.2, 100)')
b = s.index('seg(T_grabar, "white", "ui")')
s = s[:a] + ('seg(0.0, "vid", "u1", 0.0, 100, "48% 50%")\n'
             'seg(EV("y"), "vid", "u2", 0.0, 100, "62% 50%")\n') + s[b:]
a = s.index('seg(EV("en", 2), "white", "ia")')
b = s.index('seg(EV("solo", 1), "white", "cta")')
s = s[:a] + ('seg(EV("poner"), "white", "ia")\n'
             'seg(EV("cuando"), "white", "res")\n'
             'seg(EV("pero"), "vid", "u3", 0.0, 100, "45% 50%")\n'
             'seg(EV("nosotros"), "vid", "u4", 0.0, 100, "50% 50%")\n') + s[b:]
s = s.replace('"stress": 6.5, "docente": 6.0}', '"stress": 6.5, "docente": 6.0, "u1": 4.0, "u2": 4.0, "u3": 4.0, "u4": 4.0}', 1)
s = s.replace('FILE = {"docente": "docente",', 'FILE = {"u1": "u1", "u2": "u2", "u3": "u3", "u4": "u4", "docente": "docente",', 1)
# "en segundos" pasa a ser parte del titular de la escena
s = s.replace('''overlay("o4", EV("segundos"), '<span class="mk"><span class="big rw">en segundos</span></span>', dur=0.8)\nmask_rise("#o4 .rw", EV("segundos"), 0.7)\n''', '', 1)
s = s.replace("""'Mejor usa <span class="ac">tu clase</span>.', LAY["HY2"], tm + 0.05))""",
              """'Mejor usa <span class="ac">tu clase</span><span class="mk" style="display:inline"><span class="rw" id="%s-sg">, en segundos.</span></span>' % cid, LAY["HY2"], tm + 0.05))\n    mask_rise("#%s-sg" % cid, EV("en", 3), 0.7)""", 1)
f.write_text(s, encoding="utf-8")
print("patch v4 ok")
