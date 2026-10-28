"""Hoja de contacto para validar a ojo los planos de un storyboard (REGLAS §4: ver el fotograma contra la frase).
uso: python -I hoja_contacto_sb.py INTA20 [filas_por_hoja]  -> <Pieza>\Storyboard\contacto_<Pieza>_N.jpg (columna A = plano actual, B-D = alternativas)"""
import json, subprocess, sys, io
from pathlib import Path
from PIL import Image, ImageDraw
B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre"); LUT = B / "_inta_trabajo" / "lut"
pz = sys.argv[1]; k = int(sys.argv[2]) if len(sys.argv) > 2 else 6
alts = json.load(open(B / "_inta_trabajo" / "alts_sb_20_22.json", encoding="utf-8"))[pz]
cur = json.load(open(B / pz / "Proyecto" / "planos.json", encoding="utf-8"))["planos"]
def fr(p):
    vf = ("lut3d=sony.cube:interp=tetrahedral," if p.get("log") else "") + "scale=320:-2"
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{p['ss'] + p['need'] / 2:.2f}", "-i", p["ruta"], "-frames:v", "1", "-vf", vf, "-f", "image2pipe", "-vcodec", "mjpeg", "-"],
                       capture_output=True, cwd=str(LUT) if p.get("log") else None)
    return Image.open(io.BytesIO(r.stdout)) if r.stdout else Image.new("RGB", (320, 180), "#444")
out = B / pz / "Storyboard"; out.mkdir(exist_ok=True)
filas = []
for i, a in enumerate(alts):
    c = cur[i] if i < len(cur) else None
    opts = ([c] if c and c.get("id") else []) + a.get("alts", [])
    filas.append((i + 1, a["texto"], a["t0"], a["t1"], opts))
for h in range(0, len(filas), k):
    lote = filas[h:h + k]
    im = Image.new("RGB", (1500, 215 * len(lote)), "white"); d = ImageDraw.Draw(im)
    for j, (n, tx, t0, t1, opts) in enumerate(lote):
        y = 215 * j
        d.text((8, y + 8), f"S{n:02d} {t0:.1f}-{t1:.1f}s", fill="black"); d.text((8, y + 28), tx[:34], fill="black"); d.text((8, y + 44), tx[34:68], fill="black")
        for m, o in enumerate(opts[:4]):
            x = 180 + m * 330; im.paste(fr(o), (x, y + 4)); d.text((x, y + 188), f"{'ACTUAL' if m == 0 and o is (opts[0]) and 'why' in o else 'alt'} {o['id']} ss{o['ss']}", fill="red")
    p = out / f"contacto_{pz}_{h // k + 1}.jpg"; im.save(p, quality=80); print(p)
