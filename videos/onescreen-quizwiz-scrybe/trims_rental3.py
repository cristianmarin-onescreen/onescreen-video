"""Rental v3 — planos SIN COLOREAR (Cris: "déjalos sin colorear"). Solo conversión neutra S-Log3→Rec.709 para poder ver el video;
el color real de cada plano vive en el Lumetri de sus proyectos de Premiere (ver proyecto_premiere).
python trims_rental3.py cut     (corta los planos nuevos m1..m5 en 4K, sin colorear)
python trims_rental3.py formats (medios por formato con la conversión neutra)"""
import json, os, shutil, subprocess, sys
from pathlib import Path
B = "D:/OneScreen/Contenido/"
R = Path("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto"); CUT3 = R / "cut3"; CUT = R / "cut"; LUT = R / "lut"
CUT3.mkdir(parents=True, exist_ok=True); LUT.mkdir(parents=True, exist_ok=True)
SRC = {  # nombre: (fuente, inicio, duración, punto focal x)
    "r1": (B + "2026/6. Junio/Caso de éxito. ULA Idiomas/Apoyos/C1198.MP4", 6.0, 4.0, 0.60),
    "r2": (B + "2026/6. Junio/CASO DE ÉXITO. Areandina Pereira/Apoyos/C1010.MP4", 3.0, 4.0, 0.55),
    "r3": (B + "2025/8. Agosto/Caso de éxito. UCuenca/Apoyo/C0584.MP4", 0.0, 3.0, 0.60),
    "r4": (B + "2025/9. Septiembre/Itecsur - Ecuador/Apoyo/C0510.MP4", 0.0, 3.5, 0.55),
    "m1": (B + "2026/7. Julio/CASO DE ÉXITO. Comfenalco/Apoyo/C1335.MP4", 0.0, 4.5, 0.50),
    "m2": (B + "2026/6. Junio/Caso de éxito - Gimnasio Los Cerezos/Apoyos/C1379.MP4", 0.0, 5.0, 0.45),
    "m3": (B + "2025/9. Septiembre/Cablecom. Caso de éxito/Apoyo/C0627.MP4", 1.0, 4.5, 0.50),
    "m4": (B + "2025/8. Agosto/Areandina. CASO DE ÉXITO/Apoyo/C0742.MP4", 1.0, 5.0, 0.55),
    "m5": (B + "2025/8. Agosto/Caso de éxito. UCuenca/Apoyo/C0587.MP4", 2.0, 5.0, 0.55),
}
FORM = {"16": (1920, 1080, 3840), "9": (1080, 1920, 1215), "45": (1080, 1350, 1728)}
HALF = {"16": (960, 1080), "9": (1080, 960), "45": (1080, 675)}
NEUTRO = "lut3d=sony.cube:interp=tetrahedral"          # solo S-Log3 → Rec.709, sin look


def run(cmd, **k):
    r = subprocess.run(cmd, capture_output=True, text=True, **k)
    if r.returncode:
        print("ERROR", cmd[:3], r.stderr[-500:]); sys.exit(1)
    return r


def cut_path(n):
    return CUT / f"{n}.mp4" if n.startswith("r") else CUT3 / f"{n}.mp4"


def enc(inp, vf, dst, crf=14):
    run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", os.path.abspath(inp), "-an", "-vf", vf, "-c:v", "libx264", "-crf", str(crf), "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], cwd=str(LUT))


if sys.argv[1] == "cut":
    for n, (src, ss, t, fx) in SRC.items():
        if n.startswith("r"):
            continue                                       # r1..r4 ya están cortados en cut/
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(ss), "-i", src, "-t", str(t), "-an", "-c:v", "libx264", "-crf", "11", "-preset", "veryfast", "-pix_fmt", "yuvj420p", str(cut_path(n))])
        print("cortado", n, flush=True)
else:
    shutil.copy("C:/Users/Cristian Marin/Desktop/Claudio/luts/festivalluts.com - Sony S-Log3 → Rec.709.cube", LUT / "sony.cube")
    meta = {}
    for n, (src, ss, t, fx) in SRC.items():
        for f, (w, h, cw) in FORM.items():
            x = int(min(max(fx * 3840 - cw / 2, 0), 3840 - cw))
            enc(cut_path(n), f"fps=24,{NEUTRO},crop={cw}:2160:{x}:0,scale={w}:{h}:flags=lanczos", f"D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_{f}/media/{n}.mp4")
        meta[n] = {"len": t, "o": "50% 50%"}
        print("ok", n, flush=True)
    for name, srcn, fx in (("hl", "m2", 0.45), ("hr", "m4", 0.55)):
        for f, (hw, hh) in HALF.items():
            cwid = int(min(3840, 2160 * hw / hh)); x = int(min(max(fx * 3840 - cwid / 2, 0), 3840 - cwid))
            vf = f"fps=24,{NEUTRO},crop={cwid}:2160:{x}:0,scale={hw}:{hh}:flags=lanczos,split=4[a][b][c][d];[b]reverse[r1];[d]reverse[r2];[a][r1][c][r2]concat=n=4:v=1:a=0"
            run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", os.path.abspath(cut_path(srcn)), "-an", "-filter_complex", vf, "-c:v", "libx264", "-crf", "15", "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", f"D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_{f}/media/{name}.mp4"], cwd=str(LUT))
        meta[name] = {"len": 18.0, "o": "50% 50%"}
        print("ok", name, flush=True)
    Path("C:/Users/Cristian Marin/Desktop/Claudio/videos/onescreen-quizwiz-scrybe/rental_clips3.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
