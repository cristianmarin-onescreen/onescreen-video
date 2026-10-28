"""Hale DIRECTO, eleven_v4, guion dirigido (REGLAS §6), validado con el juez de voz_inta (3 pasadas, neutro latino). uso: python -I voz_v4_dirigida.py INTA37 [max_tomas]"""
import sys as _s; raise SystemExit("OBSOLETO (Cris, 28-oct): la voz se genera SOLO con voz_exp_d.py (receta de CLAUDE.md §6).")

import json, os, subprocess, sys, urllib.request
from pathlib import Path
sys.argv, _a = sys.argv[:1], sys.argv[1:]
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
HALE = "wWWn96OtTHu1sn8SRGEr"
KEY = os.environ["ELEVENLABS_API_KEY"]
pz = _a[0]; n = int(_a[1]) if len(_a) > 1 else 6
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
src = (Path(__file__).parent / "voz_inta.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("for pz in PIEZAS:")[0].replace("sys.argv[1:] or", "[] or"), ns)   # reutiliza acento() y aprobada()
voz = BASE / pz / "Voz"; voz.mkdir(parents=True, exist_ok=True)
txt = (voz / "guion_dirigido.txt").read_text(encoding="utf-8")
for i in range(1, n + 1):
    body = {"text": txt, "model_id": "eleven_v4", "language_code": os.environ.get("LC", "es-CO"), "voice_settings": {"stability": float(os.environ.get("ST", 0.45)), "similarity_boost": 0.8, "style": float(os.environ.get("SY", 0.35)), "use_speaker_boost": True}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{HALE}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
    f = voz / f"{pz}_hale_{os.environ.get("LC","es-CO")}_{i}.mp3"
    f.write_bytes(urllib.request.urlopen(req).read())
    ok, r = ns["aprobada"](f)
    print(f.name, "OK" if ok else "no", [(x.get("acento"), x.get("distincion_c_z"), x.get("entonacion_espana"), x.get("claridad"), x.get("palabras_mal_dichas")) for x in r], flush=True)
    if ok:
        break
