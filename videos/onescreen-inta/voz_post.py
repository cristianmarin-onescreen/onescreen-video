"""Post de la voz: las pausas largas del modelo (silencios >0,22 s a -38 dB) se acortan a 0,14 s para que el montaje tenga ritmo (el corporativo hacía lo mismo),
se pasa a WAV 48 kHz y se repite Scribe sobre la voz final (los tiempos del montaje salen de ahí). uso: python -I voz_post.py INTA09 ..."""
import json, os, re, subprocess, sys
from pathlib import Path
CONTENIDO = Path(os.environ.get("CONTENIDO", r"D:\OneScreen\Contenido"))
KEY = os.environ["ELEVENLABS_API_KEY"]
PAUSA, UMBRAL = float(os.environ.get("PAUSA", 0.14)), float(os.environ.get("UMBRAL", 0.22))   # Cris 27-oct: "muchos silencios en el narrador"
TEMPO = 1.0   # Cris 28-oct: nunca se acelera en el post (la velocidad 1,12 va en la toma, voz_exp_d.py)                                                       # y "súper lenta": se acelera sin cambiar el tono

for pz in sys.argv[1:]:
    voz = sorted(CONTENIDO.glob(f"*/*/{pz}/Voz"))[-1]
    vers = sorted(voz.glob(f"v[0-9][0-9][0-9][0-9]/{pz}_hale.mp3"))   # la toma más reciente de voz_exp_d.py
    src = vers[-1] if vers else voz / f"{pz}_hale.mp3"
    voz = src.parent
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(src), "-af", f"silencedetect=noise=-38dB:d={UMBRAL}", "-f", "null", "-"], capture_output=True, text=True)
    ini = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).group(1)) * 3600 + float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).group(2)) * 60 + float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).group(3))
    cortes, t = [], 0.0   # tramos de voz que se conservan; de cada silencio largo queda PAUSA/2 a cada lado
    for a, b in zip(ini, fin):
        a = max(a, 0)
        cortes.append((t, a + PAUSA / 2)); t = b - PAUSA / 2
    cortes.append((t, dur))
    cortes = [(a, b) for a, b in cortes if b - a > 0.05]
    fc = ";".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{i}]" for i, (a, b) in enumerate(cortes))
    fc += ";" + "".join(f"[s{i}]" for i in range(len(cortes))) + f"concat=n={len(cortes)}:v=0:a=1,atempo={TEMPO},aresample=48000[o]"
    out = voz / f"{pz}_voz.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(src), "-filter_complex", fc, "-map", "[o]", "-ac", "1", str(out)], check=True)
    sc = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + KEY, "-F", "model_id=scribe_v1", "-F", "language_code=spa", "-F", f"file=@{out}"], capture_output=True)
    j = json.loads(sc.stdout)
    (voz / f"{pz}_voz_scribe.json").write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    w = [x for x in j["words"] if x.get("type") == "word"]
    print(pz, "de", round(dur, 1), "a", round(w[-1]["end"], 1), "s;", len(w), "palabras", flush=True)
