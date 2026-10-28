"""Baja tomas de ElevenLabs por id de historial y las transcribe: python bajar_ids.py CARPETA nombre=id ..."""
import json, os, subprocess, sys, urllib.request
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
LANG = os.environ.get("LANG_CODE", "spa")
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
for kv in sys.argv[2:]:
    name, hid = kv.split("=")
    a = urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/history/{hid}/audio", headers=H)).read()
    p = out / f"{name}.mp3"; p.write_bytes(a)
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + H["xi-api-key"], "-F", "model_id=scribe_v1", "-F", f"language_code={LANG}", "-F", f"file=@{p}"], capture_output=True)
    sc = json.loads(r.stdout); (out / f"scribe_{name}.json").write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
    w = [x for x in sc["words"] if x.get("type") == "word"]
    gaps = [b["start"] - a_["end"] for a_, b in zip(w, w[1:])]
    print(name, hid, "hablado", round(w[-1]["end"] - w[0]["start"], 1), "s | huecos>0.2:", sum(g > 0.2 for g in gaps), "suma", round(sum(g for g in gaps if g > 0.2), 1), "|", " ".join(x["text"] for x in w[:5]), flush=True)
