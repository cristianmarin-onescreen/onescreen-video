"""Hale con acento colombiano (Cris, 25-oct-2026: "la misma voz de Hale pero con español colombiano").
Hale por texto a voz sale con acento de España, así que se prueban dos caminos:
  sts  -> la locución colombiana (Cristian Sánchez) pasa por voz a voz a Hale: conserva acento y ritmo, cambia el timbre
  v3   -> Hale con eleven_v3 y la etiqueta [acento colombiano]
uso: python -I hale_co.py sts FUENTE.mp3 PREFIJO   |   python -I hale_co.py v3 PREFIJO N"""
import json, os, subprocess, sys, urllib.request
from pathlib import Path

OUT = Path(r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-25_corporativo")
HALE = "dXtC3XhB9GtPusIpNtQx"
KEY = os.environ["ELEVENLABS_API_KEY"]
_src = (Path(__file__).parent / "tts.py").read_text(encoding="utf-8")     # mismo guion que tts.py (que no se puede importar: corre al cargarse)
TEXTO = eval(_src.split("TEXTO = ", 1)[1].split(chr(10) + "KEY", 1)[0])


def scribe(p, pre):
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + KEY, "-F", "model_id=scribe_v1", "-F", "language_code=spa", "-F", f"file=@{p}"], capture_output=True)
    sc = json.loads(r.stdout); (OUT / f"scribe_{pre}.json").write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
    w = [x for x in sc["words"] if x.get("type") == "word"]
    print(pre, "palabras", len(w), "hablado", round(w[-1]["end"] - w[0]["start"], 1), "s")


if sys.argv[1] == "sts":
    src, pre = Path(sys.argv[2]), sys.argv[3]
    r = subprocess.run(["curl", "-s", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{HALE}?output_format=mp3_44100_192", "-H", "xi-api-key: " + KEY,
                        "-F", "model_id=eleven_multilingual_sts_v2", "-F", 'voice_settings={"stability":0.5,"similarity_boost":0.85,"style":0.0,"use_speaker_boost":true}',
                        "-F", "remove_background_noise=false", "-F", f"audio=@{src}", "-o", str(OUT / f"{pre}_0.mp3"), "-w", "%{http_code}"], capture_output=True, text=True)
    print("http", r.stdout)
    scribe(OUT / f"{pre}_0.mp3", f"{pre}_0")
else:
    pre, n = sys.argv[2], int(sys.argv[3])
    tag = sys.argv[4] if len(sys.argv) > 4 else "[acento colombiano, locutor comercial de Bogotá]"
    for i in range(n):
        body = json.dumps({"text": tag + " " + TEXTO, "model_id": "eleven_v3"}).encode()
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{HALE}?output_format=mp3_44100_192", body, {"xi-api-key": KEY, "content-type": "application/json"})
        (OUT / f"{pre}_{i}.mp3").write_bytes(urllib.request.urlopen(req).read())
        scribe(OUT / f"{pre}_{i}.mp3", f"{pre}_{i}")
