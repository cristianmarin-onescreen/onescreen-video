"""Hojas de contacto de los planos de apoyo de varios casos de éxito (1 cuadro por clip, con nombre y duración)."""
import glob, os, subprocess, sys
from PIL import Image, ImageDraw
BASE = "D:/OneScreen/Contenido/"
CASOS = {
    "cablecom": "2025/9. Septiembre/Cablecom. Caso de éxito",
    "itecsur": "2025/9. Septiembre/Itecsur - Ecuador",
    "areandina": "2025/8. Agosto/Areandina. CASO DE ÉXITO",
    "ucuenca": "2025/8. Agosto/Caso de éxito. UCuenca",
    "cerezos": "2026/6. Junio/Caso de éxito - Gimnasio Los Cerezos",
    "pereira": "2026/6. Junio/CASO DE ÉXITO. Areandina Pereira",
    "ula": "2026/6. Junio/Caso de éxito. ULA Idiomas",
    "jireh": "2026/6. Junio/Caso de éxito - Gimnasio Jireh",
    "comfenalco": "2026/7. Julio/CASO DE ÉXITO. Comfenalco",
}
OUT = "D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/scout/"
os.makedirs(OUT, exist_ok=True)
EXC = ("entrev", "subs", "clean", "_16.9", "9.16", "auto-save", "preview", "render", "final", "audio", "__macosx", "pista", "vertical")
for key, rel in CASOS.items():
    files = []
    for ext in ("mp4", "MP4", "mov", "MOV"):
        files += glob.glob(BASE + rel + "/**/*." + ext, recursive=True)
    files = sorted({f.replace("\\", "/") for f in files if os.path.getsize(f) > 3_000_000 and not any(x in f.lower() for x in EXC)})
    info = []
    for f in files:
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
        try: d = float(d)
        except: continue
        if d < 2.5: continue
        n = os.path.basename(f)[:14]
        p = OUT + f"{key}_{len(info):03d}.jpg"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(min(2.0, d / 3)), "-i", f, "-frames:v", "1", "-vf", "scale=300:-2", p])
        if os.path.exists(p): info.append((f, n, d, p))
    W, Hh, cols = 300, 169, 6
    per = 36
    for part in range(0, len(info), per):
        sub = info[part:part + per]
        rows = (len(sub) + cols - 1) // cols
        sh = Image.new("RGB", (cols * W, rows * Hh), "black")
        for i, (f, n, d, p) in enumerate(sub):
            im = Image.open(p).resize((W, Hh)); dr = ImageDraw.Draw(im)
            dr.rectangle([0, 0, 150, 14], fill="black"); dr.text((3, 2), f"{part + i} {n} {d:.0f}s", fill="white")
            sh.paste(im, ((i % cols) * W, (i // cols) * Hh))
        sh.save(OUT + f"sheet_{key}_{part // per}.jpg")
    with open(OUT + f"lista_{key}.txt", "w", encoding="utf-8") as fh:
        for i, (f, n, d, p) in enumerate(info):
            fh.write(f"{i}\t{d:.1f}\t{f}\n")
    print(key, len(info), flush=True)
