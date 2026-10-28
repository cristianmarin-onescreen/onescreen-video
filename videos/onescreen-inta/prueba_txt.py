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
import itertools
exec(open(r"D:/OneScreen/Contenido/2026/10. Octubre/_inta_trabajo/f0.py", encoding="utf-8").read().split("for n in")[0])
T = {
 "A_viejas_tags_caps": "[direct, knowing] Si en tu empresa a alguien SIEMPRE le toca armar el acta de memoria, hay una forma de que nadie tenga que hacerlo: [excited, clear] Con una pantalla OneScreen, tu reunión SE TRANSCRIBE mientras la tienes. [quick, impressed] Si alguien habla otro idioma, se traduce al instante, en MÁS de veinte idiomas. [warm, confident] Al terminar, la IA RESUME lo que se dijo, y lo exportas en Word o en PDF. [reflective, then upbeat] Antes, uno escribía y los demás miraban. AHORA todos participan, y la pantalla ESCRIBE. [inviting] Escríbenos por WhatsApp y te mostramos, punto por punto, qué cambia en tus reuniones con la OneScreen T siete.",
 "B_sin_exclamacion": "[confident, engaging] Si en tu empresa a alguien SIEMPRE le toca armar el acta de memoria, hay una forma de que nadie tenga que hacerlo: [excited, clear] Con una pantalla OneScreen, tu reunión SE TRANSCRIBE mientras la tienes. [quick, impressed] Si alguien habla otro idioma, se traduce al instante, en MÁS de veinte idiomas. [warm, confident] Al terminar, la IA RESUME lo que se dijo, y lo exportas en Word o en PDF. [reflective, then upbeat] Antes, uno escribía y los demás miraban. AHORA todos participan, y la pantalla ESCRIBE. [inviting] Escríbenos por WhatsApp y te mostramos, punto por punto, qué cambia en tus reuniones con la OneScreen T siete.",
}
for k, txt in T.items():
    for rep in range(2):
        srcf = out / f"{pz}_t_{k}{rep}.mp3"
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{COL}?output_format=mp3_44100_192", json.dumps({"text": txt, "model_id": "eleven_v3", "voice_settings": {"stability": 0.2}}).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
        srcf.write_bytes(urllib.request.urlopen(req).read())
        sa = ns["aprobada"](srcf)[1]
        r = subprocess.run(["curl", "-s", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{HALE}?output_format=mp3_44100_192", "-H", "xi-api-key: " + KEY, "-F", "model_id=eleven_multilingual_sts_v2", "-F", "voice_settings=" + json.dumps({"stability": 0.4, "similarity_boost": 0.75, "style": 0.3}), "-F", f"audio=@{srcf}"], capture_output=True)
        f = out / f"{pz}_u_{k}{rep}.mp3"; f.write_bytes(r.stdout)
        ok, j = ns["aprobada"](f)
        print(k, rep, "OK" if ok else "no", "fuente:", [x.get("acento") for x in sa], "final:", [x.get("acento") for x in j], "F0", f0(str(f)), flush=True)
