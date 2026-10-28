"""Rental v4: diseño de dos zonas en vertical (el subtítulo ocupa la franja media) y 4:5 con subtítulo más abajo."""
from pathlib import Path
here = Path(__file__).parent
f = here / "build_rental.py"
s = f.read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# paths
rep('c0 = (cx0, 560); a = (cx0 - 230, 890 if FMT == "9" else 800); b = (cx0 + 230, 890 if FMT == "9" else 800)',
    'c0 = (cx0, 500 if FMT == "9" else 430); a = (cx0 - 250, 1180 if FMT == "9" else 780); b = (cx0 + 250, 1180 if FMT == "9" else 780)')
# cuota
rep('nyy = {"16": 560, "9": 900, "45": 700}[FMT]', 'nyy = {"16": 560, "9": 640, "45": 480}[FMT]')
rep('gy0 = {"16": 340, "9": 680, "45": 480}[FMT]', 'gy0 = {"16": 340, "9": 1040, "45": 620}[FMT]')
rep('{"16": 770, "9": 1330, "45": 960}[FMT], EV("toda") + 0.1, size=round(LAY["HS"] * 0.72)))', '{"16": 770, "9": 740, "45": 345}[FMT], EV("toda") + 0.1, size=round(LAY["HS"] * (0.72 if FMT == "16" else 0.62))))')
# ventajas
rep('cw = {"16": 412, "9": 450, "45": 450}[FMT]; vh = {"16": 200, "9": 190, "45": 150}[FMT]; ch = {"16": 510, "9": 470, "45": 400}[FMT]',
    'cw = {"16": 412, "9": 450, "45": 450}[FMT]; vh = {"16": 200, "9": 170, "45": 120}[FMT]; ch = {"16": 510, "9": 420, "45": 340}[FMT]')
rep('x = gx0 + (i % cols) * (cw + gap); y = gy0 + (i // cols) * (ch + gap)\n        p.append(f\'<div id="{cid}-k{i}" class="cd2 cd"',
    'x = gx0 + (i % cols) * (cw + gap); y = gy0 + (i // cols) * (ch + gap)\n        if FMT == "9":\n            y = 450 if i < 2 else 1010\n        p.append(f\'<div id="{cid}-k{i}" class="cd2 cd"\'')
rep('gy0 = {"16": 300, "9": 560, "45": 360}[FMT]', 'gy0 = {"16": 300, "9": 450, "45": 330}[FMT]')
# cta
rep('by = {"16": 500, "9": 980, "45": 650}[FMT]', 'by = {"16": 500, "9": 1040, "45": 650}[FMT]')
rep('uy = by + {"16": 175, "9": 170, "45": 150}[FMT]', 'uy = by + {"16": 175, "9": 190, "45": 150}[FMT]')
rep('CAPY = {"16": "89%", "9": "49%", "45": "70%"}[FMT]', 'CAPY = {"16": "89%", "9": "49%", "45": "80%"}[FMT]')
f.write_text(s, encoding="utf-8")

t = here / "trims_rental.py"
x = t.read_text(encoding="utf-8")
x = x.replace('CARD = {"16": (390, 200), "9": (440, 190), "45": (440, 150)}', 'CARD = {"16": (402, 200), "9": (440, 170), "45": (440, 120)}')
t.write_text(x, encoding="utf-8")
print("ok patch_r4")
