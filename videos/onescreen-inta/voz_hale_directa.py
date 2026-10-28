"""Prueba de Hale DIRECTO en español latino neutro (Cris, 26-oct: "no estás usando Hale en español neutro"): eleven_v3, etiqueta de acento al inicio, estabilidad natural.
Luego Gemini escucha cada toma y dice acento y claridad. uso: python -I voz_hale_directa.py INTA09 [variante: v3a|v3b|v4]"""
import sys as _s; raise SystemExit("OBSOLETO (Cris, 28-oct): la voz se genera SOLO con voz_exp_d.py (receta de CLAUDE.md §6).")

import base64, json, os, sys, urllib.request
from pathlib import Path

BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
HALE = "dXtC3XhB9GtPusIpNtQx"
KEY = os.environ["ELEVENLABS_API_KEY"]
GKEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_STUDIO")
pz, var = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "v3a")
voz = BASE / pz / "Voz"
dirigido = (voz / "guion_dirigido.txt").read_text(encoding="utf-8")
limpio = (voz / "guion_limpio.txt").read_text(encoding="utf-8")
if var == "v3a":
    body = {"text": "[neutral Latin American Spanish accent, no Spain accent, no lisp] " + dirigido, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5}}
elif var == "v3b":
    body = {"text": "[neutral Latin American Spanish accent, no Spain accent, no lisp] " + dirigido, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}, "language_code": "es"}
else:   # v4 con texto limpio y ajustes de estilo
    body = {"text": limpio, "model_id": "eleven_v4", "language_code": "es", "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}}
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{HALE}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
out = voz / f"{pz}_hale_directa_{var}.mp3"
try:
    out.write_bytes(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    raise SystemExit(f"{var}: HTTP {e.code} {e.read()[:300]}")
print("ok", out)
if GKEY:
    g = {"contents": [{"parts": [{"text": "Escucha esta locución en español. Responde en JSON con: acento (España / México / Colombia / neutro latino / otro), seseo_o_ceceo (sí/no), claridad (1-5), naturalidad (1-5), lee_etiquetas_en_voz_alta (sí/no), palabras_mal_dichas (lista)."},
                                   {"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(out.read_bytes()).decode()}}]}], "generationConfig": {"response_mime_type": "application/json"}}
    r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={GKEY}", json.dumps(g).encode(), {"content-type": "application/json"})
    try:
        print(json.loads(urllib.request.urlopen(r).read())["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e:
        print("Gemini falló:", e)
