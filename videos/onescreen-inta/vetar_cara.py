"""Revisa con Gemini (visión) los planos elegidos: ¿sale el hombre de barba con camisa OneScreen y/o audífonos que Cris vetó (103182)? Los que sí se suman a vetados_extra.json.
uso: python -I vetar_cara.py  (lee los planos.json de las piezas INTA)"""
import base64, glob, json, os, subprocess, sys, urllib.request
from pathlib import Path
B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre"); T = B / "_inta_trabajo"
KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_STUDIO")
cache_f = T / "veto_cache.json"
cache = json.load(open(cache_f, encoding="utf-8")) if cache_f.exists() else {}
ext_f = T / "vetados_extra.json"
ext = set(json.load(open(ext_f, encoding="utf-8"))) if ext_f.exists() else set()
ref = T / "ref_103182.png"
rows = {r["ID"]: r for r in json.load(open(T / "directorio_rows.json", encoding="utf-8"))}
if not ref.exists():
    r = rows["103182"]; p = r["Ruta en disco"].split("\n")[0]
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", "2", "-i", p, "-frames:v", "1", "-vf", "scale=512:-1", str(ref)])
planos = {}
for f in glob.glob(str(B / "INTA*" / "Proyecto" / "planos.json")):
    for t in json.load(open(f, encoding="utf-8"))["planos"]:
        if t["id"]:
            planos[t["id"]] = t
nuevos = 0
for i, t in planos.items():
    if i in cache:
        continue
    fr = T / f"_f_{i}.png"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(t["ss"] + 0.6), "-i", t["ruta"], "-frames:v", "1", "-vf", "scale=512:-1", str(fr)])
    if not fr.exists():
        continue
    g = {"contents": [{"parts": [{"text": "Primera imagen: referencia de una persona (hombre de barba, camisa de OneScreen, quizá audífonos). Segunda imagen: un plano. ¿En el plano aparece esa misma persona o un hombre con barba y camisa/uniforme de OneScreen? Responde JSON: {\"aparece\": true|false, \"seguridad\": 0-1, \"detalle\": \"...\"}"},
                                 {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(ref.read_bytes()).decode()}},
                                 {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(fr.read_bytes()).decode()}}]}], "generationConfig": {"response_mime_type": "application/json"}}
    rq = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={KEY}", json.dumps(g).encode(), {"content-type": "application/json"})
    try:
        j = json.loads(json.loads(urllib.request.urlopen(rq).read())["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e:
        j = {"error": str(e)}
    cache[i] = j
    if j.get("aparece") is True and float(j.get("seguridad", 0) or 0) >= 0.5:
        ext.add(i); nuevos += 1; print("VETADO", i, j.get("detalle", "")[:80], flush=True)
    fr.unlink(missing_ok=True)
json.dump(cache, open(cache_f, "w", encoding="utf-8"), ensure_ascii=False)
json.dump(sorted(ext), open(ext_f, "w", encoding="utf-8"))
print("revisados", len(cache), "vetados nuevos", nuevos, "total extra", len(ext))
