"""Mezcla de las piezas INTA: voz Hale (-18 LUFS) + una canción DISTINTA por pieza (-24 LUFS) con su punto de giro (la marca de Cris en Premiere) justo al terminar el hook + sonido de la intro de marca.
27-oct-2026 (Cris): "no uses la misma canción siempre, además la pusiste mal": antes el giro caía en la tarjeta final, tarde. Cris pone el giro/explosión al terminar el hook y el corte va después.
Sin SFX (los de antes "están terribles"). uso: python -I mix_inta.py INTA09 SALIDA.wav"""
import json, re, subprocess, sys
from pathlib import Path

PZ, OUT = sys.argv[1], Path(sys.argv[2])
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre") / PZ
M = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\Mezcla de música\Masterizadas")
# pieza -> (master, giro en s). Marcas de Cris (memoria musica_punto_de_giro). Fashion queda libre.
CANCION = {
    "INTA09": ("MASTER_WAV_MusicHusky_Promo_Opener_Main_Version.wav", 14.92), "INTA15": ("MASTER_Food Menu.wav", 8.40),
    "INTA16": ("MASTER_stepanbel_funk_main-01.wav", 16.64), "INTA17": ("MASTER_upbeat-drum-energetic-percussion.wav", 10.44),
    "INTA18": ("MASTER_Percussion Stomps Claps Energetic.wav", 22.80), "INTA19": ("MASTER_Phonk_Opener.wav", 7.32),
    "INTA20": ("MASTER_SierraAudio - Energetic Stomp Trap Percussion - Full - 190.wav", 10.16), "INTA21": ("MASTER_Cooking.wav", 19.04),
    "INTA22": ("MASTER_stepanbel_percussion_main-01.wav", 13.08), "INTA23": ("MASTER_331music_rock_main-01_full.wav", 14.68),
    "INTA24": ("MASTER_Inspired and Uplifting Hip Hop.wav", 21.48), "INTA25": ("MASTER_Claps 1.wav", 20.16),
    "INTA36": ("MASTER_For cooking fire.wav", 17.88),
    "INTA27": ("MASTER_WAV_MusicHusky_Promo_Opener_Main_Version.wav", 14.92),   # todas las canciones ya tenían pieza: se repite Husky (INTA09); Cris decide si prefiere otra
    "INTA37": ("MASTER_Fashion.wav", 12.40),   # marca de Cris (21-oct); Fashion no se había usado en INTA
}
MUS = M / CANCION[PZ][0]
DROP_M = CANCION[PZ][1]
VOZ = BASE / "Voz" / f"{PZ}_voz.wav"
PLAN = json.load(open(BASE / "Proyecto" / "v_16" / "plan.json", encoding="utf-8"))
D, INTRO = 0.10, 8.0914
END = PLAN["END_SCENE"]
TOTAL = round(END + INTRO, 3)
sc = [w for w in json.load(open(BASE / "Voz" / f"{PZ}_voz_scribe.json", encoding="utf-8"))["words"] if w.get("type") == "word"]
hook = next((w["end"] for w in sc if re.search(r"[.:?!]$", w["text"].strip()) and w["end"] > (1.5 if PZ == "INTA36" else 3.0)), sc[min(8, len(sc) - 1)]["end"])
DROP_V = round(hook + D, 3)          # la explosión cae justo al terminar el hook
MOFF = DROP_M - DROP_V


def lufs(args):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r.stderr)[-1])


g_voz = -18 - lufs(["-i", str(VOZ)])
seg_m = ["-ss", str(MOFF), "-t", str(TOTAL), "-i", str(MUS)] if MOFF >= 0 else ["-t", str(TOTAL + MOFF), "-i", str(MUS)]
g_mus = -24 - lufs(["-ss", str(DROP_M), "-t", "20", "-i", str(MUS)])      # nivel medido sobre el tramo POSTERIOR al giro (el intro suena más bajo por diseño)
inputs = ["-i", str(VOZ)] + seg_m
mdelay = "" if MOFF >= 0 else f",adelay={int(-MOFF * 1000)}|{int(-MOFF * 1000)}"
parts = [f"[0:a]volume={g_voz}dB,adelay={int(D * 1000)}|{int(D * 1000)}[v]",
         f"[1:a]volume={g_mus}dB{mdelay},afade=t=in:st=0:d=0.25,volume='if(lt(t,{END - 0.3}),1,if(lt(t,{END + 0.5}),1-0.65*(t-{END - 0.3})/0.8,0.35))':eval=frame,afade=t=out:st={TOTAL - 1.8}:d=1.8[m]"]
labels = ["[v]", "[m]"]
inputs += ["-i", r"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2work\intro_aud_169.wav"]
parts.append(f"[2:a]atrim=0:{INTRO},volume=0.9,adelay={int(END * 1000)}|{int(END * 1000)}[intro]")
labels.append("[intro]")
parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89[o]")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(parts), "-map", "[o]", "-ar", "48000", "-ac", "2", str(OUT)], check=True)
print("mezcla", PZ, TOTAL, "s |", round(lufs(["-i", str(OUT)]), 1), "LUFS | giro en", round(DROP_V, 2), "s (hook", round(hook, 2), ") con", MUS.name, "| inicio de música", "recortado" if MOFF >= 0 else f"retrasado {round(-MOFF, 2)} s", flush=True)
