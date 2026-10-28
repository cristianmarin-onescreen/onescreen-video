"""Reemplaza solo la frase final (CTA) de una voz ya aprobada: corta la toma buena antes del CTA viejo, genera la frase nueva por la misma ruta (fuente colombiana v3 -> voz a voz a Hale)
validándola con el juez, y las une. uso: python -I cta_empalme.py INTA16 "Escríbenos por WhatsApp y lo vemos en tu sala." "[inviting]" """
import json, os, subprocess, sys, urllib.request
from pathlib import Path
src = Path(__file__).parent.joinpath("voz_inta.py").read_text(encoding="utf-8").split("for pz in PIEZAS:")[0]
pz, frase, tag = sys.argv[1], sys.argv[2], sys.argv[3]
sys.argv = ["x", "__n__"]
ns = {"__name__": "vi"}
exec(compile(src, "voz_inta.py", "exec"), ns)
B = ns["BASE"]; KEY = ns["KEY"]; HALE = ns["HALE"]; COL = ns["COLOMBIANA"]
voz = B / pz / "Voz"
old = voz / "v0005"
sc = [w for w in json.load(open(old / f"{pz}_scribe.json", encoding="utf-8"))["words"] if w.get("type") == "word"]
k = max(i for i, w in enumerate(sc) if w["text"].lower().startswith("escr") and "benos" in w["text"].lower())
corte = (sc[k - 1]["end"] + sc[k]["start"]) / 2
print("corte en", round(corte, 2), "antes de", sc[k]["text"])
base = voz / "_base.wav"
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(old / f"{pz}_hale.mp3"), "-t", str(corte), "-ar", "44100", "-ac", "1", str(base)], check=True)
for intento in range(1, 13):
    body = {"text": f"{tag} {frase}", "model_id": "eleven_v3", "voice_settings": {"stability": 0.3}}
    rq = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{COL}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
    fu = voz / "_cta_fuente.mp3"; fu.write_bytes(urllib.request.urlopen(rq).read())
    r = subprocess.run(["curl", "-s", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{HALE}?output_format=mp3_44100_192", "-H", "xi-api-key: " + KEY, "-F", "model_id=eleven_multilingual_sts_v2",
                        "-F", 'voice_settings={"stability":0.35,"similarity_boost":0.75,"style":0.4}', "-F", f"audio=@{fu}"], capture_output=True)
    cta = voz / "_cta.mp3"; cta.write_bytes(r.stdout)
    ok, j = ns["aprobada"](cta)
    print("CTA intento", intento, "OK" if ok else "no", [x.get("acento") for x in j], flush=True)
    if ok:
        break
else:
    raise SystemExit("ningún CTA pasó el juez")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(base), "-i", str(cta), "-filter_complex",
                "[0:a]aresample=44100[a];[1:a]silenceremove=start_periods=1:start_threshold=-40dB,aresample=44100[b];[a][b]concat=n=2:v=0:a=1[o]", "-map", "[o]", "-b:a", "192k", str(voz / f"{pz}_hale.mp3")], check=True)
sc2 = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + KEY, "-F", "model_id=scribe_v1", "-F", "language_code=spa", "-F", f"file=@{voz / (pz + '_hale.mp3')}"], capture_output=True)
(voz / f"{pz}_scribe.json").write_text(json.dumps(json.loads(sc2.stdout), ensure_ascii=False), encoding="utf-8")
print("listo", pz)
