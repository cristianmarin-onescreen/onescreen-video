"""Storyboard HTML de una pieza INTA (REGLAS paso 9b): voz a la izquierda, plano a la derecha, ID de toma S01..., fotogramas reales, duración y alerta <1,5 s.
Lee <Pieza>/Proyecto/planos.json. uso: python -I storyboard_inta.py INTA37 INTA37.0001 v2 ["texto del CTA"]
Los fotogramas de planos S-Log3 llevan conversión neutra solo para verlos (el color real lo hace Cris)."""
import html, json, subprocess, sys
from pathlib import Path
pz, vid = sys.argv[1], sys.argv[2]
ver = sys.argv[3] if len(sys.argv) > 3 else "v1"
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre") / pz
LUT = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\_inta_trabajo\lut")
out = BASE / "Storyboard"; img = out / f"img_{vid}_{ver}"; img.mkdir(parents=True, exist_ok=True)
plan = json.load(open(BASE / "Proyecto" / "planos.json", encoding="utf-8"))
rows = ""
for i, p in enumerate(plan["planos"], 1):
    d = round(p["t1"] - p["t0"], 2); fr = []
    for k, f in enumerate((0.15, 0.5, 0.85)):
        dst = img / f"S{i:02d}_{k}.jpg"
        vf = ("lut3d=sony.cube:interp=tetrahedral," if p["log"] else "") + "scale=360:-2"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", f"{p['ss'] + p['need'] * f:.2f}", "-i", p["ruta"], "-frames:v", "1", "-vf", vf, "-q:v", "4", str(dst)], cwd=str(LUT))
        fr.append(dst.name)
    rojo = ' style="color:#c00;font-weight:700"' if d < 1.5 else ""
    ims = "".join(f'<img src="{img.name}/{n}">' for n in fr)
    aviso = ' · <b style="color:#b36b00">requiere aprobación del cliente</b>' if "aprobaci" in p.get("permisos", "") else ""
    rows += (f'<tr><td><b>S{i:02d}</b><br>{p["t0"]:.1f}–{p["t1"]:.1f} s<br><span{rojo}>{d:.1f} s</span></td><td class="v">{html.escape(p["texto"])}</td>'
             f'<td>{ims}<div class="m">plano <b>{p["id"]}</b> · tramo {p["ss"]}–{round(p["ss"] + p["need"], 1)} s · {html.escape(p.get("lugar") or "")}{aviso}<br>{html.escape(p.get("desc", ""))}</div></td></tr>')
cta = sys.argv[4] if len(sys.argv) > 4 else "(CTA)"
rows += f'<tr><td><b>S{len(plan["planos"]) + 1:02d}</b><br>{plan["cierre_t"]:.1f} s→</td><td class="v">{html.escape(cta)}</td><td><i>Tarjeta final + intro de marca (motion graphic)</i></td></tr>'
dst = out / f"storyboard_{vid}_{ver}.html"
dst.write_text(f'''<!doctype html><meta charset="utf-8"><title>Storyboard {vid}</title><style>
body{{font:14px Rubik,Arial,sans-serif;margin:20px;color:#1a1a1a}}table{{border-collapse:collapse;width:100%}}td{{border-bottom:1px solid #ddd;padding:8px;vertical-align:top}}
.v{{width:26%;font-size:16px}}img{{width:31%;margin-right:1%;border-radius:4px}}.m{{font-size:12px;color:#555;margin-top:4px}}</style>
<h2>Storyboard {vid} · {ver}</h2><p>Corrige por ID de toma, p. ej. «en S04 pon el plano 101066».</p><table>{rows}</table>''', encoding="utf-8")
print(dst)
