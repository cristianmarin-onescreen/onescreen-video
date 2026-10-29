r"""Recortes 9:16, 4:5 y 1:1 de una pieza INTA desde los cortes coloreados que ya dejo final_color_inta.py (v_16c/media).
uso: python -I final_formatos_inta.py INTA23 0006 "CTA" 9 45 1"""
import os, shutil, subprocess, sys
from pathlib import Path

pz, ver, cta, *fmts = sys.argv[1:]
AQUI = Path(__file__).parent
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre") / pz
P = BASE / "Proyecto"
POST = r"C:\Users\Cristian Marin\Desktop\Claudio\videos\onescreen-quizwiz-scrybe\post_rental.py"
NOMBRE = {"9": "9x16", "45": "4x5", "1": "1x1"}
INTRO = {"9": r"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2_9\media\intro.mp4",
         "45": r"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2_45\media\intro.mp4",
         "1": str(P / "intro_1x1.mp4")}
env = dict(os.environ, TMP="D:/hf-render/tmp", TEMP="D:/hf-render/tmp", PYTHONIOENCODING="utf-8")


def run(cmd, cwd=None, e=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=e or env, shell=isinstance(cmd, str))
    if r.returncode:
        raise SystemExit(f"FALLÓ {cmd}\n{(r.stdout + r.stderr)[-900:]}")
    return r.stdout


for f in fmts:
    d = P / f"v_{f}c"
    (d / "media").mkdir(parents=True, exist_ok=True)
    for m in (P / "v_16c" / "media").glob("*.mp4"):
        shutil.copy(m, d / "media" / m.name)
    run([sys.executable, "-I", str(AQUI / "build_inta_sb.py")], e=dict(env, PIEZA=pz, FMT=f, SUF="c", CTA_TXT=cta))
    raw = P / "out" / f"raw_{f}c.mp4"
    for x in (P / "out").glob(f".raw_{f}c.hf-transaction*"):
        shutil.rmtree(x, ignore_errors=True)
    raw.unlink(missing_ok=True)
    run(f'npx hyperframes render -o "{raw}" -q delivery --video-frame-format png --frames-cache-dir "D:/hf-render/tmp/rfc{f}c_{pz}" --quiet', cwd=str(d))
    shutil.rmtree(f"D:/hf-render/tmp/rfc{f}c_{pz}", ignore_errors=True)
    final = BASE / "Exports" / f"{pz}.{ver}_H1C1A1_neutro_{NOMBRE[f]}.mp4"
    run([sys.executable, "-I", POST, f, str(raw), str(final)], e=dict(env, MIX=str(P / "mix.wav"), INTRO=INTRO[f]))
    print(pz, f, "ok", final, flush=True)
