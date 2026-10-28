"""Voz del video corporativo (guion C, aprobado por Cris el 25-oct-2026): N tomas con Hale vía API y Scribe de cada una.
uso: python -I tts.py PREFIJO VOZ_ID N [MODELO]  -> audio_elevenlabs/2026-10-25_corporativo/<PREFIJO>_<i>.mp3 + scribe_<PREFIJO>_<i>.json
Cris (25-oct): la voz debe ser colombiana; Hale sonó española (seseo)."""
import json, os, subprocess, sys, urllib.request
from pathlib import Path

OUT = Path(r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-25_corporativo")
TEXTO = ("Si tu sala de reuniones depende de un proyector, una cámara web, micrófonos aparte y cables por todos lados, esto te interesa. "
         "Una OneScreen los reemplaza a todos. "
         "Compartes pantalla sin cables. Cámara y audio integrados. Y cada reunión termina transcrita, con su resumen. "
         "Si tu equipo necesita ayuda, el botón Gurú lo conecta en vivo con ingenieros de OneScreen. "
         "Solicita tu demo.")
KEY = os.environ["ELEVENLABS_API_KEY"]
PRE, VOZ, n = sys.argv[1], sys.argv[2], int(sys.argv[3]); modelo = sys.argv[4] if len(sys.argv) > 4 else "eleven_multilingual_v2"
for i in range(n):
    body = json.dumps({"text": TEXTO, "model_id": modelo}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_192", body, {"xi-api-key": KEY, "content-type": "application/json"})
    try:
        a = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError as e:
        print("ERROR", e.code, e.read()[:300]); sys.exit(1)
    p = OUT / f"{PRE}_{i}.mp3"; p.write_bytes(a)
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + KEY, "-F", "model_id=scribe_v1", "-F", "language_code=spa", "-F", f"file=@{p}"], capture_output=True)
    sc = json.loads(r.stdout); (OUT / f"scribe_{PRE}_{i}.json").write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
    w = [x for x in sc["words"] if x.get("type") == "word"]
    gaps = [b["start"] - a_["end"] for a_, b in zip(w, w[1:])]
    print(i, "hablado", round(w[-1]["end"] - w[0]["start"], 1), "s | huecos>0.2:", sum(g > 0.2 for g in gaps), "|", sc.get("text", "")[:400].encode("ascii", "replace").decode())
