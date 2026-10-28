"""Variantes de voz a voz con más dirección y ritmo (INTA37). uso: python -I voz_prueba37.py INTA37"""
import json, os, subprocess, sys, urllib.request
from pathlib import Path
KEY = os.environ["ELEVENLABS_API_KEY"]; HALE = "wWWn96OtTHu1sn8SRGEr"; COL = "o2vbTbO3g4GrKUg7rehy"
pz = sys.argv[1]; voz = Path(rf"D:\OneScreen\Contenido\2026\10. Octubre\{pz}\Voz")
txt = (voz / "guion_dirigido.txt").read_text(encoding="utf-8")
def fuente(nombre, stab):
    body = {"text": txt, "model_id": "eleven_v4", "language_code": "es", "voice_settings": {"stability": stab, "style": 0.6, "speed": 1.12, "use_speaker_boost": True}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{COL}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
    f = voz / f"{pz}_{nombre}_fuente.mp3"; f.write_bytes(urllib.request.urlopen(req).read()); return f
def sts(f, nombre, stab, style):
    r = subprocess.run(["curl", "-s", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{HALE}?output_format=mp3_44100_192", "-H", "xi-api-key: " + KEY,
        "-F", "model_id=eleven_multilingual_sts_v2", "-F", "voice_settings=" + json.dumps({"stability": stab, "similarity_boost": 0.7, "style": style}), "-F", f"audio=@{f}"], capture_output=True)
    if r.stdout[:1] == b"{": raise SystemExit(r.stdout[:300])
    o = voz / f"{pz}_{nombre}.mp3"; o.write_bytes(r.stdout); return o
def dur(f):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)],capture_output=True,text=True).stdout)
def f0(f):
    try:
        import librosa, numpy as np
        y, sr = librosa.load(str(f), sr=16000)
        f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr); v = f0[~np.isnan(f0)]
        return round(float(np.percentile(v, 95) - np.percentile(v, 5)), 1)
    except Exception as e:
        return f"n/d ({type(e).__name__})"
print("anterior F0", f0(voz/f"{pz}_hale.mp3"), "dur", round(dur(voz/f"{pz}_hale.mp3"),1))
for nombre, vs, ss, sy in [("exp_c", 0.3, 0.2, 0.7), ("exp_d", 0.45, 0.2, 0.7)]:
    fu = fuente(nombre, vs); o = sts(fu, nombre, ss, sy)
    print(nombre, "fuente", round(dur(fu), 1), "s F0", f0(fu), "| hale", round(dur(o), 1), "s F0", f0(o), flush=True)
