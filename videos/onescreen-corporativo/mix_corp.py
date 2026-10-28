"""Mezcla del video corporativo: Hale con acento colombiano (Yorman Zapata dirigido en eleven_v3 → voz a voz a Hale) (-18 LUFS) + MASTER_Fashion (la explosión cae sobre el barrido blanco de 'Una OneScreen', -24 LUFS)
+ SFX afinados a Sol menor + sonido de la intro de marca. Mismo criterio que mix_rental.py.
uso: python mix_corp.py SALIDA.wav"""
import json, re, subprocess, sys
from pathlib import Path

A = Path(r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-21_quizwiz_scrybe")
VOZ = r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-25_corporativo\v_hyv3_0_0.wav"
MUS = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\Mezcla de música\Masterizadas\MASTER_Fashion.wav")
PLAN = json.load(open(r"D:\OneScreen\Contenido\2026\10. Octubre\Corporativo salas de reuniones\Proyecto\v_16\plan.json", encoding="utf-8"))
OUT = Path(sys.argv[1])
D = 0.10
INTRO = 8.0914
END = PLAN["END_SCENE"]
TOTAL = round(END + INTRO, 3)
ev = PLAN["events"]
DROP_V = ev["una1"] + 0.083          # la explosión cae 2 cuadros después del barrido blanco
DROP_M = 12.40                       # explosión del master (igual que en el Rental)
MOFF = DROP_M - DROP_V
EARLY = 0.075
cuts = ev["cuts"]
SFX = ([("tick", t) for t in cuts[1:6]]                                   # la ráfaga de equipos
       + [("hit", DROP_V + EARLY), ("swipe", ev["reemplaza"]), ("pop", ev["reemplaza"] + 0.9),
          ("swipe", ev["transcrita"]), ("ding", ev["resumen"] + 0.1), ("pop", ev["gurú"]), ("whoosh", ev["solicita"] - 0.05), ("ding", ev["solicita"] + 0.25)])


def lufs(args):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r.stderr)[-1])


g_voz = -18 - lufs(["-i", VOZ])
seg_m = ["-ss", str(MOFF), "-t", str(TOTAL), "-i", str(MUS)]
g_mus = -24 - lufs(seg_m)
inputs = ["-i", VOZ] + seg_m
parts = [f"[0:a]volume={g_voz}dB,adelay={int(D * 1000)}|{int(D * 1000)}[v]",
         f"[1:a]volume={g_mus}dB,afade=t=in:st=0:d=0.25,volume='if(lt(t,{END - 0.3}),1,if(lt(t,{END + 0.5}),1-0.65*(t-{END - 0.3})/0.8,0.35))':eval=frame,afade=t=out:st={TOTAL - 1.8}:d=1.8[m]"]
labels = ["[v]", "[m]"]
SEMI = {"pop": 0, "tick": 0, "hit": -4, "scan": 0, "swipe": 0, "ding": 2, "whoosh": -5}   # tonos para caer en Sol (Fashion está en Sol menor)
vol = {"pop": .15, "tick": .14, "hit": .30, "scan": .18, "swipe": .15, "ding": .18, "whoosh": .16}
for i, (n, t) in enumerate(SFX):
    t = max(0.0, t - EARLY) if n != "hit" else t
    inputs += ["-i", str(A / f"sfx_{n}.mp3")]
    st = SEMI[n]
    shift = "" if st == 0 else f"asetrate={int(44100 * 2 ** (st / 12))},aresample=48000,atempo={1 / 2 ** (st / 12):.5f},"
    parts.append(f"[{i + 2}:a]{shift}volume={vol[n]},adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]")
    labels.append(f"[s{i}]")
k = len(labels)
inputs += ["-i", "D:/OneScreen/Contenido/2026/10. Octubre/QuizWiz y Scrybe/Proyecto/v2work/intro_aud_169.wav"]
parts.append(f"[{k}:a]atrim=0:{INTRO},volume=0.9,adelay={int(END * 1000)}|{int(END * 1000)}[intro]")
labels.append("[intro]")
parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89[o]")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(parts), "-map", "[o]", "-ar", "48000", "-ac", "2", str(OUT)], check=True)
print("mezcla", TOTAL, "s |", round(lufs(["-i", str(OUT)]), 1), "LUFS | explosión en", round(DROP_V, 2), "| voz", round(g_voz, 1), "música", round(g_mus, 1))
