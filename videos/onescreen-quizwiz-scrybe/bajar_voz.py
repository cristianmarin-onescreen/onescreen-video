"""Baja las N tomas más recientes del historial de ElevenLabs a una carpeta: python bajar_voz.py CARPETA PREFIJO N"""
import json, os, subprocess, sys, urllib.request
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
pre, n = sys.argv[2], int(sys.argv[3])
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
d = json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/history?page_size={n}", headers=H)))
for i, h in enumerate(d["history"]):
    a = urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/history/{h['history_item_id']}/audio", headers=H)).read()
    p = out / f"{pre}_{i}.mp3"; p.write_bytes(a)
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + H["xi-api-key"], "-F", "model_id=scribe_v1", "-F", "language_code=spa", "-F", f"file=@{p}"], capture_output=True)
    sc = json.loads(r.stdout); (out / f"scribe_{pre}_{i}.json").write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
    w = [x for x in sc["words"] if x.get("type") == "word"]
    gaps = [b["start"] - a_["end"] for a_, b in zip(w, w[1:])]
    print(i, h["history_item_id"], len(a), "hablado", round(w[-1]["end"] - w[0]["start"], 1), "s | huecos>0.2:", sum(g > 0.2 for g in gaps), "suma", round(sum(g for g in gaps if g > 0.2), 1))
