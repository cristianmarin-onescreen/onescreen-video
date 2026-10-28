"""Fuente colombiana v3 FRASE A FRASE (cada línea con su propia dirección) -> STS a Hale -> acelera. INTA37."""
import json, os, re, subprocess, sys, urllib.request
from pathlib import Path
exec(open("voz_prueba37.py", encoding="utf-8").read().split("for nombre, vs")[0].replace("pz = sys.argv[1]", "pz = 'INTA37'"))
lineas = re.findall(r"(\[[^\]]+\])\s*([^\[]+)", txt)
partes = []
for i, (tag, fr) in enumerate(lineas):
    body = {"text": f"{tag} {fr.strip()}", "model_id": "eleven_v3", "voice_settings": {"stability": 0.0}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{COL}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
    f = voz / f"{pz}_fr{i}.mp3"; f.write_bytes(urllib.request.urlopen(req).read()); partes.append(f)
lst = voz / "lista.txt"; lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
cat = voz / f"{pz}_exp_e_fuente.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(lst),"-ar","44100","-ac","1",str(cat)],check=True)
for n, ss, sy in [("exp_e", 0.2, 0.7)]:
    o = sts(cat, n, ss, sy)
    fast = voz / f"{pz}_{n}_rapida.mp3"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(o),"-filter:a","atempo=1.15","-b:a","192k",str(fast)],check=True)
    print(n, "fuente", round(dur(cat),1), "F0", f0(cat), "| hale", round(dur(o),1), "F0", f0(o), "| rapida", round(dur(fast),1), "F0", f0(fast), flush=True)
