"""Prueba de variantes de Hale contra el juez estricto. uso: python -I prueba_acento.py INTA17"""
import json, sys, urllib.request
from pathlib import Path
src = Path(__file__).parent.joinpath("voz_inta.py").read_text(encoding="utf-8").split("for pz in PIEZAS:")[0]
sys.argv = ["x", "__n__"]
ns = {"__name__": "vi"}
exec(compile(src, "voz_inta.py", "exec"), ns)
pz = sys.argv[1] if False else "INTA17"
B = ns["BASE"]; KEY = ns["KEY"]; HALE = ns["HALE"]
dir_ = (B / pz / "Voz" / "guion_dirigido.txt").read_text(encoding="utf-8")
limp = (B / pz / "Voz" / "guion_limpio.txt").read_text(encoding="utf-8")
out = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\_inta_trabajo\acento"); out.mkdir(exist_ok=True)
V = {
 "v4_esCO": dict(text=dir_, model_id="eleven_v4", language_code="es-CO"),
 "v4_esMX": dict(text=dir_, model_id="eleven_v4", language_code="es-MX"),
 "v4_es419": dict(text=dir_, model_id="eleven_v4", language_code="es-419"),
 "v4_tag": dict(text="[Colombian Spanish accent, Latin American pronunciation, seseo] " + dir_, model_id="eleven_v4", language_code="es"),
 "mv2": dict(text=limp, model_id="eleven_multilingual_v2", language_code="es"),
 "v3_tag": dict(text="[Latin American Spanish accent, seseo, no Spain accent] " + dir_, model_id="eleven_v3"),
}
for n, b in V.items():
    b["voice_settings"] = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True} if "v4" in n or "mv2" in n else {"stability": 0.5}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{HALE}?output_format=mp3_44100_192", json.dumps(b).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
    f = out / f"{pz}_{n}.mp3"
    try:
        f.write_bytes(urllib.request.urlopen(req).read())
    except Exception as e:
        print(n, "ERROR", getattr(e, "read", lambda: b"")()[:160]); continue
    ok, r = ns["aprobada"](f)
    print(n, "OK" if ok else "no", [(x.get("acento"), x.get("distincion_c_z"), x.get("entonacion_espana")) for x in r], flush=True)
