"""Voz de pauta: recorta huecos entre frases (Cris no deja aire), acelera y da presencia.
uso: python -I voz_gen.py CARPETA PREFIJO N [TEMPO] [GAP_KEEP]  -> CARPETA/v_PREFIJO_N.wav"""
import json, subprocess, sys
import numpy as np
from pathlib import Path
import soundfile as sf

A = Path(sys.argv[1]); P = sys.argv[2]; N = sys.argv[3]
TEMPO = float(sys.argv[4]) if len(sys.argv) > 4 else 1.06
GAP_KEEP = float(sys.argv[5]) if len(sys.argv) > 5 else 0.09
GAP_MIN = 0.16
SR = 48000
XF = int(0.012 * SR)

raw = A / f"tmp_{P}_{N}.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(A / f"{P}_{N}.mp3"), "-ar", str(SR), "-ac", "1", str(raw)], check=True)
y, sr = sf.read(raw)
d = json.load(open(A / f"scribe_{P}_{N}.json", encoding="utf-8"))
w = [x for x in d["words"] if x.get("type") == "word"]
keep = []
t0 = max(0.0, w[0]["start"] - 0.03)
for a, b in zip(w, w[1:]):
    if b["start"] - a["end"] > GAP_MIN:
        keep.append((t0, a["end"] + GAP_KEEP / 2))
        t0 = b["start"] - GAP_KEEP / 2
keep.append((t0, min(len(y) / SR, w[-1]["end"] + 0.12)))
out = np.zeros(0)
for s, e in keep:
    seg = y[int(s * SR):int(e * SR)].copy()
    f = min(XF, len(seg) // 2)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    if len(out) >= f:
        out[-f:] += seg[:f]; out = np.concatenate([out, seg[f:]])
    else:
        out = np.concatenate([out, seg])
cut = A / f"tmp_{P}_{N}_cut.wav"
sf.write(cut, out, SR)
af = (f"atempo={TEMPO},highpass=f=70,equalizer=f=3200:t=q:w=1.0:g=2.5,equalizer=f=180:t=q:w=1.0:g=-1.5,"
      f"highshelf=f=9000:g=2.0,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=60:makeup=2,alimiter=limit=0.95")
dst = A / f"v_{P}_{N}.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(cut), "-af", af, "-ar", str(SR), "-ac", "1", str(dst)], check=True)
raw.unlink(); cut.unlink()
r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + __import__("os").environ["ELEVENLABS_API_KEY"], "-F", "model_id=scribe_v1", "-F", "language_code=" + __import__("os").environ.get("LANG_CODE", "spa"), "-F", f"file=@{dst}"], capture_output=True)
sc = json.loads(r.stdout); (A / f"scribe_v_{P}_{N}.json").write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
ww = [x for x in sc["words"] if x.get("type") == "word"]
print("ok", dst, round(len(out) / SR / TEMPO, 2), "s | antes", round(len(y) / SR, 2), "| palabras", len(ww), "| fin", round(ww[-1]["end"], 2))
