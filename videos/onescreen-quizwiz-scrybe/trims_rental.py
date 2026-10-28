"""Planos de casos de éxito del video Rental: corta -> colorea (skill colorear-plano) -> medios por formato.
python trims_rental.py cut_grade   (lento, en segundo plano)
python trims_rental.py formats     (rápido)"""
import json, os, subprocess, sys
from pathlib import Path
B = "D:/OneScreen/Contenido/"
R = Path("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto"); CUT = R / "cut"; GR = R / "graded"
CUT.mkdir(parents=True, exist_ok=True); GR.mkdir(parents=True, exist_ok=True)
# nombre: (fuente, inicio, duración, ancho de salida de la copia a colorear, punto focal x, aspecto de tarjeta por formato)
CL = {
    "r1": (B + "2026/6. Junio/Caso de éxito. ULA Idiomas/Apoyos/C1198.MP4", 6.0, 4.0, 3840, 0.60),
    "r2": (B + "2026/6. Junio/CASO DE ÉXITO. Areandina Pereira/Apoyos/C1010.MP4", 3.0, 4.0, 3840, 0.55),
    "r3": (B + "2025/8. Agosto/Caso de éxito. UCuenca/Apoyo/C0584.MP4", 0.0, 3.0, 3840, 0.60),
    "r4": (B + "2025/9. Septiembre/Itecsur - Ecuador/Apoyo/C0510.MP4", 0.0, 3.5, 3840, 0.55),
    "c1": (B + "2026/7. Julio/CASO DE ÉXITO. Comfenalco/Apoyo/C1335.MP4", 0.0, 4.5, 1920, 0.50),
    "c2": (B + "2026/6. Junio/Caso de éxito - Gimnasio Los Cerezos/Apoyos/C1379.MP4", 0.0, 5.0, 1920, 0.45),
    "c3": (B + "2025/9. Septiembre/Cablecom. Caso de éxito/Apoyo/C0628.MP4", 0.0, 2.5, 1920, 0.50),
    "c4": (B + "2025/8. Agosto/Areandina. CASO DE ÉXITO/Apoyo/C0742.MP4", 1.0, 5.0, 1920, 0.55),
}
CARD = {"16": (402, 200), "9": (440, 170), "45": (440, 120)}


def run(cmd, **k):
    r = subprocess.run(cmd, capture_output=True, text=True, **k)
    if r.returncode:
        print("ERROR", cmd[:3], r.stderr[-400:]); sys.exit(1)
    return r


if sys.argv[1] == "cut_grade":
    for n, (src, ss, t, wd, fx) in CL.items():
        vf = "scale=1920:-2" if wd == 1920 else "null"
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(ss), "-i", src, "-t", str(t), "-an", "-vf", vf, "-c:v", "libx264", "-crf", "11", "-preset", "veryfast", "-pix_fmt", "yuvj420p", str(CUT / f"{n}.mp4")])
        print("cortado", n, flush=True)
    for n in CL:
        run(["python", "-I", "grade/pipeline.py", str(CUT / f"{n}.mp4"), "--out", str(GR), "--sufijo", "g"], cwd="C:/Users/Cristian Marin/Desktop/Claudio")
        print("coloreado", n, flush=True)
    (GR / "DONE").write_text("ok")
else:
    meta = {}
    for n, (src, ss, t, wd, fx) in CL.items():
        g = GR / f"{n}_g.mp4"
        for f, (w, h, cw) in {"16": (1920, 1080, 3840), "9": (1080, 1920, 1215), "45": (1080, 1350, 1728)}.items():
            dst = f"D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_{f}/media/{n}.mp4"
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if n.startswith("r"):
                x = int(min(max(fx * 3840 - cw / 2, 0), 3840 - cw))
                vf = f"fps=24,crop={cw}:2160:{x}:0,scale={w}:{h}:flags=lanczos"
                run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(g), "-an", "-vf", vf, "-c:v", "libx264", "-crf", "14", "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst])
            else:
                cwid, chei = CARD[f]
                ar = cwid / chei
                cwp = int(min(1920, 1080 * ar)); x = int(min(max(fx * 1920 - cwp / 2, 0), 1920 - cwp))
                vf = f"fps=24,crop={cwp}:1080:{x}:0,scale={cwid * 2}:{chei * 2}:flags=lanczos,split=4[a][b][c][d];[b]reverse[r1];[d]reverse[r2];[a][r1][c][r2]concat=n=4:v=1:a=0"
                run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(g), "-an", "-filter_complex", vf, "-c:v", "libx264", "-crf", "16", "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst])
        d = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst]).stdout.strip())
        meta[n] = {"len": round(d, 2), "o": "50% 50%"}
        print("ok", n, meta[n], flush=True)
    meta["c1"]["len"] = meta["c1"]["len"]
    Path("C:/Users/Cristian Marin/Desktop/Claudio/videos/onescreen-quizwiz-scrybe/rental_clips.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
