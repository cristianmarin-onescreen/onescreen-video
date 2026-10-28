"""INTA27: voz compuesta = narración hasta «nosotros» + pausa + extracto de Yolanda Velázquez (Areandina, clip 102494, 163,36-171,72 s) + pausa + resto de la narración.
Deja la voz original como INTA27_voz_orig.wav / _scribe_orig.json y escribe INTA27_voz.wav e INTA27_voz_scribe.json con los tiempos corridos (mismos corrimientos del storyboard).
uso: python -I voz_compuesta_27.py"""
import json, subprocess
from pathlib import Path

V = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\INTA27\Voz")
T1, GAP = 15.58, 0.25
EXT_IN, EXT_OUT = 163.36, 171.72
EXT_DUR = EXT_OUT - EXT_IN
SHIFT = GAP + EXT_DUR + GAP
rows = {r["ID"]: r for r in json.load(open(r"D:\OneScreen\Contenido\2026\10. Octubre\_inta_trabajo\directorio_rows.json", encoding="utf-8"))}
clip = rows["102494"]["Ruta en disco"].split("\n")[0].strip()

orig, osc = V / "INTA27_voz_orig.wav", V / "INTA27_voz_scribe_orig.json"
if not orig.exists():
    (V / "INTA27_voz.wav").replace(orig)
    (V / "INTA27_voz_scribe.json").replace(osc)

ext = V / "INTA27_extracto.wav"
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(EXT_IN), "-t", f"{EXT_DUR:.3f}", "-i", clip, "-vn", "-ac", "1", "-ar", "48000",
                "-af", "highpass=f=80,loudnorm=I=-18:TP=-2:LRA=7", str(ext)], check=True)
fc = (f"[0:a]atrim=0:{T1},asetpts=PTS-STARTPTS[a];[1:a]asetpts=PTS-STARTPTS[e];[0:a]atrim={T1},asetpts=PTS-STARTPTS[b];"
      f"aevalsrc=0:d={GAP}:s=48000:c=mono[s1];aevalsrc=0:d={GAP}:s=48000:c=mono[s2];[a][s1][e][s2][b]concat=n=5:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(orig), "-i", str(ext), "-filter_complex", fc, "-map", "[o]", "-ac", "1", "-ar", "48000", str(V / "INTA27_voz.wav")], check=True)

sc = json.load(open(osc, encoding="utf-8"))
cw = json.load(open(r"D:\OneScreen\Contenido\2026\10. Octubre\INTA27\Caso\102494.json", encoding="utf-8"))
nuevo = []
for w in sc["words"]:
    if w.get("type") != "word":
        continue
    if w["start"] < T1:
        nuevo.append(w)
for w in cw["words"]:
    if w.get("type") == "word" and EXT_IN - 0.02 <= w["start"] and w["end"] <= EXT_OUT + 0.05:
        nuevo.append(dict(w, start=round(w["start"] - EXT_IN + T1 + GAP, 3), end=round(w["end"] - EXT_IN + T1 + GAP, 3)))
for w in sc["words"]:
    if w.get("type") == "word" and w["start"] >= T1:
        nuevo.append(dict(w, start=round(w["start"] + SHIFT, 3), end=round(w["end"] + SHIFT, 3)))
out = dict(sc, words=nuevo, audio_duration_secs=round(nuevo[-1]["end"] + 0.1, 3))
out["text"] = " ".join(w["text"] for w in nuevo)
json.dump(out, open(V / "INTA27_voz_scribe.json", "w", encoding="utf-8"), ensure_ascii=False)
print("palabras", len(nuevo), "fin", nuevo[-1]["end"], "s")
