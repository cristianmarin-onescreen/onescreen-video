"""Mezcla v2: voz Hale (notas de dirección v4, -18 LUFS) + MASTER_Fashion (explosión de Cris en 12,4 s sobre el corte a QuizWiz) + SFX 60-85 ms antes de cada evento."""
import json, re, subprocess, sys
from pathlib import Path
A = Path(r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-21_quizwiz_scrybe")
MUS = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\Mezcla de música\Masterizadas\MASTER_Fashion.wav")
PLAN = json.load(open(r"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2_16\plan.json", encoding="utf-8"))
OUT = Path(sys.argv[1])
D = 0.10
INTRO = 8.0914
END = PLAN["END_SCENE"]
TOTAL = round(END + INTRO, 3)
ev = PLAN["events"]
segs = PLAN["segs"]
white = {sg["src"]: sg["t"] for sg in segs if sg["kind"] == "white"}
DROP_V = ev["el"] + 0.083          # la explosión cae 2 cuadros después del paneo a QuizWiz
DROP_M = 12.40
MOFF = DROP_M - DROP_V
EARLY = 0.075                      # los efectos van 60-85 ms antes del evento visual (medido en los proyectos de Cris)
SFX = [("pop", ev["scribe"]), ("tick", ev["start"]), ("hit", DROP_V + EARLY), ("pop", ev["quizwiz"]), ("tick", ev["arma"]), ("tick", ev["entregarlo"] + 0.1),
       ("scan", ev["qr"]), ("whoosh", ev["estudiante"] - 0.3), ("scan", ev["escanea"]), ("swipe", white["ia"]), ("ding", ev["resultados"]),
       ("swipe", white["res"]), ("whoosh", ev["pero"]), ("swipe", white["cta"])]


def lufs(args):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r.stderr)[-1])


voz = str(A / "v5_1.wav")
g_voz = -18 - lufs(["-i", voz])
seg_m = ["-ss", str(MOFF), "-t", str(TOTAL), "-i", str(MUS)]
g_mus = -24 - lufs(seg_m)
inputs = ["-i", voz] + seg_m
parts = [f"[0:a]volume={g_voz}dB,adelay={int(D * 1000)}|{int(D * 1000)}[v]",
         f"[1:a]volume={g_mus}dB,afade=t=in:st=0:d=0.25,volume='if(lt(t,{END - 0.3}),1,if(lt(t,{END + 0.5}),1-0.65*(t-{END - 0.3})/0.8,0.35))':eval=frame,afade=t=out:st={TOTAL - 1.8}:d=1.8[m]"]
labels = ["[v]", "[m]"]
SEMI = {"camera": 0, "pop": 0, "tick": 0, "hit": -4, "scan": 0, "swipe": 0, "ding": 2, "whoosh": -5}   # tonos para caer en Sol (MASTER_Fashion está en Sol menor)
vol = {"camera": .22, "pop": .16, "tick": .22, "hit": .30, "scan": .20, "swipe": .16, "ding": .20, "whoosh": .16}
for i, (n, t) in enumerate(SFX):
    t = max(0.0, t - EARLY) if n != "hit" else t
    inputs += ["-i", str(A / f"sfx_{n}.mp3")]
    st = SEMI[n]
    shift = "" if st == 0 else f"asetrate={int(44100 * 2 ** (st / 12))},aresample=48000,atempo={1 / 2 ** (st / 12):.5f},"
    parts.append(f"[{i + 2}:a]{shift}volume={vol[n]},adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]")
    labels.append(f"[s{i}]")
k = len(labels) + 0
inputs += ["-i", "D:/OneScreen/Contenido/2026/10. Octubre/QuizWiz y Scrybe/Proyecto/v2work/intro_aud_169.wav"]
parts.append(f"[{k}:a]atrim=0:{INTRO},volume=0.9,adelay={int(END * 1000)}|{int(END * 1000)}[intro]")
labels.append("[intro]")
parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89[o]")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(parts), "-map", "[o]", "-ar", "48000", "-ac", "2", str(OUT)], check=True)
print("mezcla", TOTAL, "s |", round(lufs(["-i", str(OUT)]), 1), "LUFS | soltar explosión en", round(DROP_V, 2), "| ganancias voz", round(g_voz, 1), "música", round(g_mus, 1))
