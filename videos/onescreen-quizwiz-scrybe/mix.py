"""Mezcla: voz Hale (-18 LUFS) + MASTER_Fashion (drop de Cris en 12,4 s -> cae en 8,3 s del video) + SFX discretos."""
import subprocess, re, sys
from pathlib import Path
A = Path(r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-21_quizwiz_scrybe")
MUS = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\Mezcla de música\Masterizadas\MASTER_Fashion.wav")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mix.wav")
D = 0.10            # arranque de la voz
TOTAL = 34.0
DROP_V = 8.50       # instante del video donde cae la explosión
DROP_M = 12.40      # marca de Cris en la pista
MOFF = DROP_M - DROP_V
# (archivo, t, volumen)
SFX = [("whoosh", 5.0, .16), ("tick", 7.45, .22), ("hit", DROP_V, .30), ("pop", 11.5, .16), ("pop", 12.2, .16),
       ("scan", 14.4, .20), ("pop", 15.1, .14), ("whoosh", 17.3, .16), ("swipe", 19.1, .16), ("whoosh", 20.45, .16),
       ("pop", 20.6, .14), ("ding", 25.4, .20), ("whoosh", 26.0, .14), ("whoosh", 27.4, .14), ("whoosh", 29.8, .16), ("pop", 31.3, .16)]

def lufs(args):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r.stderr)[-1])

voz = str(A / "voz_e2.wav")
g_voz = -18 - lufs(["-i", voz])
seg = ["-ss", str(MOFF), "-t", str(TOTAL), "-i", str(MUS)]
g_mus = -24 - lufs(seg)
print("ganancia voz", round(g_voz, 2), "musica", round(g_mus, 2))
inputs = ["-i", voz] + seg
parts = [f"[0:a]volume={g_voz}dB,adelay={int(D*1000)}|{int(D*1000)}[v]",
         f"[1:a]volume={g_mus}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={TOTAL-1.8}:d=1.8[m]"]
labels = ["[v]", "[m]"]
for i, (n, t, vol) in enumerate(SFX):
    inputs += ["-i", str(A / f"sfx_{n}.mp3")]
    parts.append(f"[{i+2}:a]volume={vol},adelay={int(t*1000)}|{int(t*1000)}[s{i}]")
    labels.append(f"[s{i}]")
parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89[o]")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(parts), "-map", "[o]", "-ar", "48000", "-ac", "2", str(OUT)], check=True)
print("mezcla:", lufs(["-i", str(OUT)]), "LUFS integrados")
