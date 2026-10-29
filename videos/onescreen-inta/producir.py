"""Produce el preview de una pieza INTA de punta a punta: planos -> montaje x3 -> render x3 -> mezcla -> post (intro de marca) -> Exports con nombre canónico.
Preview: render en calidad 'draft' (el definitivo se re-renderiza en delivery al aprobar). uso: python -I producir.py INTA09 [INTA15 ...]"""
import os, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).parent
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
POST = r"C:\Users\Cristian Marin\Desktop\Claudio\videos\onescreen-quizwiz-scrybe\post_rental.py"
VER = os.environ.get("VER", "0002")
SB = os.environ.get("SB") == "1"      # SB=1: arma desde el storyboard aprobado (montaje_aprobado.json) con build_inta_sb.py
SOLO = os.environ.get("SOLO")        # SOLO=16 renderiza un solo formato
NOMBRE = {"16": "16x9", "9": "9x16", "45": "4x5"}
env = dict(os.environ, TMP="D:/hf-render/tmp", TEMP="D:/hf-render/tmp", PYTHONIOENCODING="utf-8")


def run(cmd, cwd=None, e=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=e or env, shell=isinstance(cmd, str))
    if r.returncode:
        raise SystemExit(f"FALLÓ {cmd}\n{(r.stdout + r.stderr)[-800:]}")
    return r.stdout


for pz in sys.argv[1:]:
    P = BASE / pz / "Proyecto"
    out = P / "out"; out.mkdir(parents=True, exist_ok=True)
    exp = BASE / pz / "Exports"; exp.mkdir(parents=True, exist_ok=True)
    run([sys.executable, "-I", str(AQUI / "cortes_inta.py"), pz], e=dict(env, PLANOS="planos_sb.json") if SB else None)
    for f in os.environ.get("FORMS", "16 9 45").split():
        run([sys.executable, "-I", str(AQUI / ("build_inta_sb.py" if SB else "build_inta.py"))], e=dict(env, PIEZA=pz, FMT=f, **({"CTA_TXT": os.environ.get("CTA_TXT", "")} if SB else {})))
    run([sys.executable, "-I", str(AQUI / "mix_inta.py"), pz, str(P / "mix.wav")])
    for f in ((SOLO,) if SOLO else ("16", "9", "45")):
        raw = out / f"raw_{f}.mp4"
        run(f'npx hyperframes render -o "{raw}" -q draft --video-frame-format png --frames-cache-dir "D:/hf-render/tmp/rfc{f}_{pz}" --quiet', cwd=str(P / f"v_{f}"))
        shutil.rmtree(f"D:/hf-render/tmp/rfc{f}_{pz}", ignore_errors=True)
        final = exp / f"{pz}.{VER}_H1C1A1_neutro_{NOMBRE[f]}_preview.mp4"
        run([sys.executable, "-I", POST, f, str(raw), str(final)], e=dict(env, MIX=str(P / "mix.wav")))
        print(pz, f, "ok", final, flush=True)
