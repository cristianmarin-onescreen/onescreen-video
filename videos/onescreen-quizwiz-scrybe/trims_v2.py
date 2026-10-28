"""Prepara los medios de la v2 (planos reales de interfaz, docente estresada y cierre de marca) para cada formato."""
import subprocess, sys, os
R5 = r"D:/OneScreen/Contenido/2026/8. Agosto/Video Demo/Apoyo/SC07 - Software/20260824_192731.mp4"
ST = r"D:/OneScreen/Contenido/2026/8. Agosto/Video Demo/Apoyo/SC07 - Software/stressed-woman-with-glasses-sitting-at-classroom-d-2025-12-18-00-22-19-utc.mov"
INTRO169 = r"D:/OneScreen/Brand kit/Varios/Audiovisual/Intro/Español/OneScreen (Intro)_ESP_16.9_NoMúsica.mp4"
INTRO916 = r"D:/OneScreen/Brand kit/Varios/Audiovisual/Intro/Español/OneScreen (Intro)_ESP_9.16_NoMúsica.mp4"
FORM = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}
# nombre, fuente, inicio, duración
CLIPS = [("scrA", R5, 23.5, 8.0), ("scrB", R5, 35.0, 5.5), ("qwzGen", R5, 241.0, 9.0), ("qwzQR", R5, 285.0, 8.0), ("stress", ST, 0.8, 6.5)]
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-400:]); sys.exit(1)
for f, (W, H) in FORM.items():
    d = f"D:/OneScreen/Contenido/2026/10. Octubre/QuizWiz y Scrybe/Proyecto/v2_{f}"
    os.makedirs(d + "/media", exist_ok=True)
    for n, src, ss, dur in CLIPS:
        out = f"{d}/media/{n}.mp4"
        if os.path.exists(out): continue
        vf = f"fps=24,scale=-2:{H}:flags=lanczos"
        run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", src, "-an", "-vf", vf, "-c:v", "libx264", "-crf", "14", "-g", "24", "-keyint_min", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", out])
        print("ok", f, n, flush=True)
    intro = f"{d}/media/intro.mp4"
    if not os.path.exists(intro):
        if f == "16":
            vf = "fps=24,scale=1920:1080:flags=lanczos"; src = INTRO169
        elif f == "9":
            vf = "fps=24,scale=1080:1920:flags=lanczos"; src = INTRO916
        else:
            vf = "fps=24,crop=2160:2700:0:570,scale=1080:1350:flags=lanczos"; src = INTRO916
        run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", src, "-an", "-vf", vf, "-c:v", "libx264", "-crf", "14", "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", intro]); print("ok intro", f, flush=True)
