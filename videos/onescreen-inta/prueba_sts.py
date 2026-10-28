"""Fuente colombiana DIRIGIDA (eleven_v3 con etiquetas) -> voz a voz a Hale. Juez estricto + rango de F0. uso: python -I prueba_sts.py INTA17"""
import json, subprocess, sys, urllib.request
from pathlib import Path
src = Path(__file__).parent.joinpath("voz_inta.py").read_text(encoding="utf-8").split("for pz in PIEZAS:")[0]
pz = sys.argv[1]
sys.argv = ["x", "__n__"]
ns = {"__name__": "vi"}
exec(compile(src, "voz_inta.py", "exec"), ns)
B = ns["BASE"]; KEY = ns["KEY"]; HALE = ns["HALE"]
COL = "o2vbTbO3g4GrKUg7rehy"
dir_ = (B / pz / "Voz" / "guion_dirigido.txt").read_text(encoding="utf-8")
out = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\_inta_trabajo\acento"); out.mkdir(exist_ok=True)
srcf = out / f"{pz}_fuente_col.mp3"
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{COL}?output_format=mp3_44100_192", json.dumps({"text": dir_, "model_id": "eleven_v3", "voice_settings": {"stability": 0.3}}).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
srcf.write_bytes(urllib.request.urlopen(req).read())
print("fuente col:", [(x.get("acento"), x.get("distincion_c_z"), x.get("entonacion_espana")) for x in ns["aprobada"](srcf)[1]])
for n, vs in {"sts_a": {"stability": 0.35, "similarity_boost": 0.75, "style": 0.4}, "sts_b": {"stability": 0.5, "similarity_boost": 0.85, "style": 0.0}}.items():
    r = subprocess.run(["curl", "-s", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{HALE}?output_format=mp3_44100_192", "-H", "xi-api-key: " + KEY,
                        "-F", "model_id=eleven_multilingual_sts_v2", "-F", f"voice_settings={json.dumps(vs)}", "-F", f"audio=@{srcf}"], capture_output=True)
    f = out / f"{pz}_{n}.mp3"; f.write_bytes(r.stdout)
    if r.stdout[:1] == b"{":
        print(n, "ERROR", r.stdout[:200]); continue
    ok, j = ns["aprobada"](f)
    print(n, "OK" if ok else "no", [(x.get("acento"), x.get("distincion_c_z"), x.get("entonacion_espana"), x.get("naturalidad")) for x in j], flush=True)
