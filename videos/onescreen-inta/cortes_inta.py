"""Corta los planos de planos.json a 16:9, 9:16 y 4:5 para el preview. Conversión neutra S-Log3->Rec.709 SOLO PARA VER (el color real lo hace Cris con el flujo del Directorio):
queda anotado en el preview. Stock/IA/planos ya graduados van tal cual. uso: python -I cortes_inta.py INTA09 [...]"""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
FORM = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}
LUTSRC = r"C:\Users\Cristian Marin\Desktop\Claudio\luts\festivalluts.com - Sony S-Log3 → Rec.709.cube"


def uno(args):
    pz, p = args
    for f, (w, h) in ((k, v) for k, v in FORM.items() if k in os.environ.get("FORMS", "16 9 45").split()):
        dst = BASE / pz / "Proyecto" / f"v_{f}" / "media" / f"{p.get('key', p['id'])}.mp4"
        if dst.exists() and dst.stat().st_size > 10000:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        fx = p.get("fx", 0.5)
        crop = f"crop='min(iw,ih*{w}/{h})':'min(ih,iw*{h}/{w})':'max(0,min(iw-min(iw,ih*{w}/{h}),{fx}*iw-min(iw,ih*{w}/{h})/2))':'(ih-min(ih,iw*{h}/{w}))/2'"
        vf = ("lut3d=sony.cube:interp=tetrahedral," if p["log"] else "") + f"fps=24,{crop},scale={w}:{h}:flags=lanczos,setsar=1"
        r = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(p["ss"]), "-i", p["ruta"], "-t", str(p["need"]), "-an", "-vf", vf, "-c:v", "libx264", "-crf", "16",
                            "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(dst)], capture_output=True, text=True, cwd=str(LUT))
        if r.returncode:
            return f"ERROR {pz} {p['id']} {f} {r.stderr[-200:]}"
    return None


LUT = BASE / "_inta_trabajo" / "lut"
LUT.mkdir(parents=True, exist_ok=True)
shutil.copy(LUTSRC, LUT / "sony.cube")
for pz in sys.argv[1:]:
    plan = json.load(open(BASE / pz / "Proyecto" / os.environ.get("PLANOS", "planos.json"), encoding="utf-8"))
    items = [(pz, p) for p in plan["planos"] if p["id"]]
    err = 0
    with ThreadPoolExecutor(3) as ex:
        for m in ex.map(uno, items):
            if m:
                err += 1; print(m, flush=True)
    print(pz, "planos", len(items), "errores", err, flush=True)
