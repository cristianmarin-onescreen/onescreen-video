"""Transcribe con Scribe los clips de un caso de éxito (entrevistas) para armar la pieza con las voces de ellos. uso: python -I transcribir_caso.py CARPETA_SALIDA ID1 ID2 ..."""
import json, os, subprocess, sys
from pathlib import Path
T = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\_inta_trabajo")
rows = {r["ID"]: r for r in json.load(open(T / "directorio_rows.json", encoding="utf-8"))}
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
KEY = os.environ["ELEVENLABS_API_KEY"]
for i in sys.argv[2:]:
    r = rows[i]
    p = r["Ruta en disco"].split("\n")[0].strip()
    if not os.path.exists(p):
        for c in (r"D:\OneScreen" + p, r"D:\OneScreen\Contenido" + p):
            if os.path.exists(c): p = c; break
    a = out / f"{i}.mp3"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", p, "-vn", "-ac", "1", "-ar", "22050", "-b:a", "64k", str(a)], check=True)
    r2 = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + KEY, "-F", "model_id=scribe_v1", "-F", "language_code=spa", f"-F", f"file=@{a}"], capture_output=True)
    sc = json.loads(r2.stdout)
    (out / f"{i}.json").write_text(json.dumps(dict(ruta=p, clip=r["Clip"], text=sc.get("text"), words=sc.get("words")), ensure_ascii=False), encoding="utf-8")
    print(i, r["Clip"], p[-50:], "|", (sc.get("text") or "")[:300].replace("\n", " "), flush=True)
