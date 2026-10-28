"""Rental: escala mayor en 16:9, logo/titular sobre plano más arriba, rama de contacto sin choque."""
from pathlib import Path
f = Path(__file__).parent / "build_rental.py"
s = f.read_text(encoding="utf-8")


def rep(a, b, cnt=1):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, cnt)


rep('LAY = {"16": dict(HS=104, HY1=120, NY=520, ND=170, HY2=770, M=150, AL="left"),', 'LAY = {"16": dict(HS=118, HY1=100, NY=520, ND=190, HY2=770, M=130, AL="left"),')
# logo / titular sobre plano
rep('hy = {"16": round(H * 0.70), "9": round(H * 0.62), "45": round(H * 0.62)}[FMT]', 'hy = {"16": round(H * 0.56), "9": round(H * 0.60), "45": round(H * 0.58)}[FMT]')
# paths: más grande y más abajo en 16:9
rep('c0 = (cx0, 360); a = (cx0 - 430, NY + 40); b = (cx0 + 430, NY + 40)', 'c0 = (cx0, 380); a = (cx0 - 520, 690); b = (cx0 + 520, 690)')
rep('cy2 = a[1] + (nd // 2 + 120 if FMT == "16" else nd // 2 + 110)', 'cy2 = a[1] + (nd // 2 + 130 if FMT == "16" else nd // 2 + 110)')
# ventajas
rep('cw = {"16": 400, "9": 450, "45": 450}[FMT]; vh = {"16": 200, "9": 190, "45": 150}[FMT]; ch = {"16": 450, "9": 400, "45": 330}[FMT]', 'cw = {"16": 412, "9": 450, "45": 450}[FMT]; vh = {"16": 240, "9": 190, "45": 150}[FMT]; ch = {"16": 520, "9": 400, "45": 330}[FMT]')
rep('gap = 30\n    gx0 = (W - (cols * cw + (cols - 1) * gap)) / 2\n    gy0 = {"16": 330,', 'gap = 28\n    gx0 = (W - (cols * cw + (cols - 1) * gap)) / 2\n    gy0 = {"16": 300,')
rep("font-size:{34 if FMT == '16' else 36}px;line-height:1.1;letter-spacing:-0.02em;color:#0b0b14}} .cd2 i{{font-style:normal;font-family:'Manrope';font-weight:600;font-size:{22 if FMT == '16' else 24}px", "font-size:{40 if FMT == '16' else 36}px;line-height:1.1;letter-spacing:-0.02em;color:#0b0b14}} .cd2 i{{font-style:normal;font-family:'Manrope';font-weight:600;font-size:{26 if FMT == '16' else 24}px")
# cta
rep("size=round(LAY[\"HS\"] * 1.12), al=\"center\", w=W - 2 * LAY[\"M\"]))\n    tb =", "size=round(LAY[\"HS\"] * 1.3), al=\"center\", w=W - 2 * LAY[\"M\"]))\n    tb =")
rep('by = {"16": 520, "9": 980, "45": 650}[FMT]; bw = {"16": 560, "9": 620, "45": 560}[FMT]', 'by = {"16": 500, "9": 980, "45": 650}[FMT]; bw = {"16": 660, "9": 620, "45": 560}[FMT]')
rep('uy = by + {"16": 150, "9": 170, "45": 150}[FMT]', 'uy = by + {"16": 175, "9": 170, "45": 150}[FMT]')
rep("font-size:{round(H * 0.04) if FMT == '16' else 44}px;color:#0b0b14;letter-spacing:-0.01em}} .url b", "font-size:{round(H * 0.052) if FMT == '16' else 46}px;color:#0b0b14;letter-spacing:-0.01em}} .url b")
rep("height:{round(H * 0.095) if FMT == '16' else 120}px;border-radius:999px;background:#3976ff;color:#fff;font-family:'Rubik';font-weight:600;font-size:{round(H * 0.036) if FMT == '16' else 46}px", "height:{round(H * 0.115) if FMT == '16' else 120}px;border-radius:999px;background:#3976ff;color:#fff;font-family:'Rubik';font-weight:600;font-size:{round(H * 0.044) if FMT == '16' else 46}px")
f.write_text(s, encoding="utf-8")
print("ok patch_r2")
