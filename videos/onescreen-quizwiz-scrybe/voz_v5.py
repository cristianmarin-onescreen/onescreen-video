"""Voz v5: recorta los silencios entre frases (Cris nunca deja aire), acelera un poco y da presencia/brillo.
uso: python -I voz_v5.py N   (N = toma hale_v5_N)"""
import json, subprocess, sys
import numpy as np
from pathlib import Path
import soundfile as sf

A = Path(r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-21_quizwiz_scrybe")
N = sys.argv[1]
SR = 48000
GAP_KEEP = 0.085      # lo que queda de aire entre palabras tras el recorte (s)
GAP_MIN = 0.16        # solo se recortan huecos mayores a esto
TEMPO = 1.06
XF = int(0.012 * SR)

raw = A / f"tmp_v5_{N}.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(A / f"hale_v5_{N}.mp3"), "-ar", str(SR), "-ac", "1", str(raw)], check=True)
y, sr = sf.read(raw)
d = json.load(open(A / f"scribe_v5_{N}.json", encoding="utf-8"))
w = [x for x in d["words"] if x.get("type") == "word"]

# intervalos a conservar: desde el inicio de cada palabra (-GAP_KEEP/2) hasta su fin (+GAP_KEEP/2); los huecos grandes se encogen a GAP_KEEP
keep = []
t0 = max(0.0, w[0]["start"] - 0.03)
for a, b in zip(w, w[1:]):
    gap = b["start"] - a["end"]
    if gap > GAP_MIN:
        keep.append((t0, a["end"] + GAP_KEEP / 2))
        t0 = b["start"] - GAP_KEEP / 2
keep.append((t0, min(len(y) / SR, w[-1]["end"] + 0.12)))

out = np.zeros(0)
for s, e in keep:
    seg = y[int(s * SR):int(e * SR)].copy()
    f = min(XF, len(seg) // 2)
    seg[:f] *= np.linspace(0, 1, f)
    seg[-f:] *= np.linspace(1, 0, f)
    if len(out) >= f:
        out[-f:] += seg[:f]
        out = np.concatenate([out, seg[f:]])
    else:
        out = np.concatenate([out, seg])
cut = A / f"tmp_v5_{N}_cut.wav"
sf.write(cut, out, SR)

# tempo + presencia: realce 3 kHz, brillo 9 kHz, compresión suave, limpieza de graves
af = (f"atempo={TEMPO},highpass=f=70,equalizer=f=3200:t=q:w=1.0:g=2.5,equalizer=f=180:t=q:w=1.0:g=-1.5,"
      f"highshelf=f=9000:g=2.0,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=60:makeup=2,alimiter=limit=0.95")
dst = A / f"v5_{N}.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(cut), "-af", af, "-ar", str(SR), "-ac", "1", str(dst)], check=True)
raw.unlink(); cut.unlink()
print("ok", dst, round(len(out) / SR / TEMPO, 2), "s (antes", round(len(y) / SR, 2), ")")
