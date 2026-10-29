r"""Final 16:9 en 4K de una pieza INTA con el COLOR que Cris exportó de Premiere (paso 13 del proceso).
1) corta cada plano del montaje aprobado desde el export de color (INTA23_Color.mp4) usando <Pieza>.planos.json (dónde quedó cada plano en la secuencia de color);
2) arma la composición con build_inta_sb.py (SUF=c, UHD=1: el mismo diseño de 1920x1080 escalado x2 en un lienzo 4K);
3) renderiza en calidad delivery, mezcla la intro de marca en 4K y el audio, y deja el export sin _preview en Exports\.
uso: python -I final_color_inta.py INTA23 INTA23_Color.mp4 INTA23.0004_planos_para_colorear.planos.json 0004 "TEXTO CTA"   (los archivos van en <Pieza>\Premiere)"""
import json, os, shutil, subprocess, sys
from pathlib import Path

pz, color, planos_json, ver, cta = sys.argv[1:6]
AQUI = Path(__file__).parent
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre") / pz
PRE = BASE / "Premiere"
P = BASE / "Proyecto"
OUT = P / "out"; OUT.mkdir(exist_ok=True)
POST_MIX = P / "mix.wav"
INTRO4K = r"D:\OneScreen\Contenido\2026\10. Octubre\Rental DaaS\Premiere RENT.0005\intro_onescreen.mp4"
env = dict(os.environ, TMP="D:/hf-render/tmp", TEMP="D:/hf-render/tmp", PYTHONIOENCODING="utf-8")


def run(cmd, cwd=None, e=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=e or env, shell=isinstance(cmd, str))
    if r.returncode:
        raise SystemExit(f"FALLÓ {cmd}\n{(r.stdout + r.stderr)[-900:]}")
    return r.stdout


mapa = {m["src"]: m for m in json.load(open(PRE / planos_json, encoding="utf-8"))}
pls = json.load(open(P / "planos_sb.json", encoding="utf-8"))["planos"]
media = P / "v_16c" / "media"; media.mkdir(parents=True, exist_ok=True)
for p in pls:
    m = mapa["p" + p["id"]]
    ini = m["secuencia_inicio_s"] + (p["ss"] - m["origen_in_s"])
    fin_ventana = m["secuencia_inicio_s"] + (m["origen_out_s"] - m["origen_in_s"])
    dur = min(p["need"], fin_ventana - ini - 0.04)
    dst = media / f"{p['key']}.mp4"
    run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", f"{ini:.3f}", "-i", str(PRE / color), "-t", f"{dur:.3f}", "-an", "-vf", "fps=24,setsar=1", "-c:v", "libx264", "-crf", "14", "-g", "24",
         "-preset", "veryfast", "-pix_fmt", "yuv420p", str(dst)])
    print("corte", p["toma"], p["id"], f"{ini:.2f}+{dur:.2f}", flush=True)

run([sys.executable, "-I", str(AQUI / "build_inta_sb.py")], e=dict(env, PIEZA=pz, FMT="16", SUF="c", UHD="1", CTA_TXT=cta))
raw = OUT / "raw_16c_4k.mp4"
for f in OUT.glob(".raw_16c_4k.hf-transaction*"):
    shutil.rmtree(f, ignore_errors=True)
raw.unlink(missing_ok=True)
run(f'npx hyperframes render -o "{raw}" -q delivery --video-frame-format png --frames-cache-dir "D:/hf-render/tmp/rfc16c_{pz}" --quiet', cwd=str(P / "v_16c"))
shutil.rmtree(f"D:/hf-render/tmp/rfc16c_{pz}", ignore_errors=True)
final = BASE / "Exports" / f"{pz}.{ver}_H1C1A1_neutro_16x9.mp4"
fc = "[0:v]rgbashift=rh=-1:bh=1:edge=smear,format=yuv420p[a];[1:v]scale=3840:2160:flags=lanczos,setsar=1,format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[v]"
run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(raw), "-i", INTRO4K, "-i", str(POST_MIX), "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
     "-r", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", str(final)])
print(pz, "final 4K ok", final, flush=True)
