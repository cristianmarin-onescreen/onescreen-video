"""Planos de salón de UISRAEL ya coloreados (skill colorear-plano) -> medios por formato (recorte desde 4K con punto focal)."""
import subprocess, sys
G = "D:/OneScreen/Contenido/2026/10. Octubre/QuizWiz y Scrybe/Proyecto/uis/graded"
FOCAL = {"u1": 0.67, "u2": 0.62, "u3": 0.45, "u4": 0.40}
FORM = {"16": (1920, 1080, 3840), "9": (1080, 1920, 1215), "45": (1080, 1350, 1728)}   # ancho de recorte sobre 4K (alto 2160)
for u, fx in FOCAL.items():
    src = f"{G}/{u}_{'a' if u in ('u3', 'u4') else 'g'}.mp4"
    for f, (w, h, cw) in FORM.items():
        x = int(min(max(fx * 3840 - cw / 2, 0), 3840 - cw))
        vf = f"fps=24,crop={cw}:2160:{x}:0,scale={w}:{h}:flags=lanczos"
        dst = f"D:/OneScreen/Contenido/2026/10. Octubre/QuizWiz y Scrybe/Proyecto/v2_{f}/media/{u}.mp4"
        r = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", src, "-an", "-vf", vf, "-c:v", "libx264", "-crf", "14", "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], capture_output=True, text=True)
        if r.returncode:
            print(u, f, r.stderr[-300:]); sys.exit(1)
    print("ok", u, flush=True)
