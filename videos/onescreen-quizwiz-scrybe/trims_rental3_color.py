"""Rental v3 con el COLOR de Cris: sustituye los medios neutros (S-Log3 -> Rec.709 solo para ver) por los cortes coloreados en Premiere.
Fuente: Rental DaaS/Colorear planos/cortes/<src>_<clip>_color.mp4 + RENT.0005_planos_para_colorear.planos.json (ventana de origen de cada corte).
Cada medio se alinea a la linea de tiempo que espera build_rental3 (t=0 del medio = inicio SS del plano en la fuente) y luego se recorta/escala por formato
igual que trims_rental3.py formats, pero SIN el LUT neutro (el color ya viene aplicado).
Uso: python trims_rental3_color.py [16 9 45]   (por defecto 16)"""
import json, os, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
R = Path("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto")
CP = Path("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Colorear planos")
FORM = {"16": (1920, 1080, 3840), "9": (1080, 1920, 1215), "45": (1080, 1350, 1728)}
HALF = {"16": (960, 1080), "9": (1080, 960), "45": (1080, 676)}
# nombre: (inicio SS en la fuente, duración del medio, punto focal x) -- igual que trims_rental3.SRC
SRC = {"r1": (6.0, 4.0, 0.60), "r2": (3.0, 4.0, 0.55), "r3": (0.0, 3.0, 0.60), "m1": (0.0, 4.5, 0.50), "m2": (0.0, 5.0, 0.45),
       "m3": (1.0, 4.5, 0.50), "m4": (1.0, 5.0, 0.55), "m5": (2.0, 5.0, 0.55)}
ALIGN = R / "color_alineado"
ALIGN.mkdir(exist_ok=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print("ERROR", cmd[:4], r.stderr[-600:]); sys.exit(1)


mapa = {m["src"]: m for m in json.load(open(CP / "RENT.0005_planos_para_colorear.planos.json", encoding="utf-8"))}
for n, (ss, t, fx) in SRC.items():
    m = mapa[n]
    cut = CP / "cortes" / f"{n}_{m['archivo'].split('.')[0]}_color.mp4"
    d = ss - m["origen_in_s"]               # >0: el corte empieza antes que SS (se recorta); <0: empieza después (se rellena con el primer cuadro)
    vf = "fps=24000/1001," + (f"trim=start={d:.4f},setpts=PTS-STARTPTS," if d > 0 else "") + (f"tpad=start_duration={-d:.4f}:start_mode=clone," if d < 0 else "") + \
         f"tpad=stop_duration=30:stop_mode=clone,trim=duration={t:.4f},setpts=PTS-STARTPTS"
    run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(cut), "-an", "-vf", vf, "-c:v", "libx264", "-crf", "11", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(ALIGN / f"{n}.mp4")])
    print("alineado", n, "desfase", round(d, 3), flush=True)

for f in (sys.argv[1:] or ["16"]):
    w, h, cw = FORM[f]
    media = R / f"v_{f}" / "media"
    bak = R / f"v_{f}" / "media_neutro"
    if not bak.exists():
        shutil.copytree(media, bak)           # respaldo de los medios neutros
    for n, (ss, t, fx) in SRC.items():
        x = int(min(max(fx * 3840 - cw / 2, 0), 3840 - cw))
        run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(ALIGN / f"{n}.mp4"), "-an", "-vf", f"fps=24,crop={cw}:2160:{x}:0,scale={w}:{h}:flags=lanczos",
             "-c:v", "libx264", "-crf", "14", "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(media / f"{n}.mp4")])
    for name, srcn, fxh in (("hl", "m2", 0.45), ("hr", "m4", 0.55)):
        hw, hh = HALF[f]
        cwid = int(min(3840, 2160 * hw / hh)); x = int(min(max(fxh * 3840 - cwid / 2, 0), 3840 - cwid))
        vf = f"fps=24,crop={cwid}:2160:{x}:0,scale={hw}:{hh}:flags=lanczos,split=4[a][b][c][d];[b]reverse[r1];[d]reverse[r2];[a][r1][c][r2]concat=n=4:v=1:a=0"
        run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(ALIGN / f"{srcn}.mp4"), "-an", "-filter_complex", vf, "-c:v", "libx264", "-crf", "15", "-g", "24",
             "-preset", "veryfast", "-pix_fmt", "yuv420p", str(media / f"{name}.mp4")])
    print("medios con color listos para", f, flush=True)
