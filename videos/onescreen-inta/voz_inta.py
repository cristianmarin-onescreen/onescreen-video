"""Voz de los guiones INTA, v2 (26-oct-2026, Cris: "no estás usando Hale en español neutro"): HALE DIRECTO con eleven_v4, language_code es, guion dirigido (etiquetas) -> Scribe.
Sin voz a voz ni locutor colombiano de origen: Gemini clasificó esta ruta como "neutro latino" (v3 directo salía "España"). Cada toma se valida con Gemini (acento, claridad).
uso: python -I voz_inta.py INTA09 [INTA15 ...]   (sin argumentos: las 12). La voz anterior queda en Voz\\v0001\\."""
import sys as _s; raise SystemExit("OBSOLETO (Cris, 28-oct): la voz se genera SOLO con voz_exp_d.py (receta de CLAUDE.md §6).")

import base64, json, os, shutil, subprocess, sys, urllib.request
from pathlib import Path

BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
HALE = "wWWn96OtTHu1sn8SRGEr"
COLOMBIANA = "o2vbTbO3g4GrKUg7rehy"   # Cristian Sánchez (colombiano), solo como fuente de acento y dirección
KEY = os.environ["ELEVENLABS_API_KEY"]
GKEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_STUDIO")
PIEZAS = sys.argv[1:] or ["INTA09", "INTA15", "INTA16", "INTA17", "INTA18", "INTA19", "INTA20", "INTA21", "INTA22", "INTA23", "INTA24", "INTA25"]


PROMPT = ("Escucha esta locución en español como un hablante nativo de Colombia que detecta de inmediato el castellano de España. Responde en JSON con: "
          "acento (España / México / Colombia / neutro latino / otro), distincion_c_z (sí/no: ¿pronuncia la c ante e/i y la z como la 'th' de España, p. ej. en 'cinco', 'hacer', 'gracias', 'empresa', 'decisión', 'veinte'? En Latinoamérica suenan como s), "
          "entonacion_espana (sí/no: ¿la melodía y el ritmo suenan a España?), claridad (1-5), naturalidad (1-5), palabras_mal_dichas (lista).")


def acento(p):
    g = {"contents": [{"parts": [{"text": PROMPT},
                                 {"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(p.read_bytes()).decode()}}]}], "generationConfig": {"response_mime_type": "application/json"}}
    r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={GKEY}", json.dumps(g).encode(), {"content-type": "application/json"})
    try:
        return json.loads(json.loads(urllib.request.urlopen(r).read())["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e:
        return {"error": str(e)}


def aprobada(p):
    """Tres pasadas del juez (el juez es ruidoso: la misma toma sale España/Colombia según la pasada); pasa si la mayoría oye acento latino, sin distinción c/z ni entonación de España."""
    r = [acento(p) for _ in range(3)]
    bien = [any(x in str(a.get("acento", "")).lower() for x in ("neutro", "colombia", "méxico", "mexico", "latin")) and str(a.get("distincion_c_z", "no")).lower().startswith("no")
            and str(a.get("entonacion_espana", "no")).lower().startswith("no") for a in r]
    return sum(bien) >= 2, r


for pz in PIEZAS:
    voz = BASE / pz / "Voz"
    old = voz / "v0001"
    if (voz / f"{pz}_hale.mp3").exists() and not old.exists():
        old.mkdir()
        for f in list(voz.glob(f"{pz}_*")):
            if f.is_file():
                shutil.move(str(f), str(old / f.name))
    hale = voz / f"{pz}_hale.mp3"
    a = {}
    for intento in range(1, 9):      # el acento de v4 varía entre tomas: se repite hasta que Gemini oiga "neutro latino"
        if not hale.exists():
            # Hale suena a España en TODOS los modelos (v4, v3, multilingual v2, con etiqueta de acento): Cris lo oyó en INTA17/18 y el juez estricto lo confirma.
            # Ruta que sí funciona (27-oct): fuente colombiana DIRIGIDA (eleven_v3 + etiquetas, estabilidad 0,1) -> voz a voz a Hale (estabilidad 0,4, similarity 0,75, estilo 0,3):
            # acento colombiano, sin distinción c/z y con la entonación de la fuente (rango F0 ~120 Hz, no la toma plana de 25-oct).
            body = {"text": (voz / "guion_dirigido.txt").read_text(encoding="utf-8"), "model_id": "eleven_v3", "voice_settings": {"stability": float(os.environ.get("V3_STAB", 0.1))}}
            req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{COLOMBIANA}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
            fuente = voz / f"{pz}_fuente_col.mp3"
            fuente.write_bytes(urllib.request.urlopen(req).read())
            r = subprocess.run(["curl", "-s", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{HALE}?output_format=mp3_44100_192", "-H", "xi-api-key: " + KEY,
                                "-F", "model_id=eleven_multilingual_sts_v2", "-F", 'voice_settings=' + json.dumps({"stability": float(os.environ.get("STS_STAB", 0.4)), "similarity_boost": 0.75, "style": float(os.environ.get("STS_STYLE", 0.3))}), "-F", f"audio=@{fuente}"], capture_output=True)
            if r.stdout[:1] == b"{":
                raise SystemExit(f"STS falló {r.stdout[:300]}")
            hale.write_bytes(r.stdout)
        ok, a = aprobada(hale) if (GKEY and os.environ.get("JUEZ") == "1") else (True, {})   # juez Gemini apagado por defecto (Cris, 28-oct: no gastar en validar); JUEZ=1 lo enciende
        if ok:
            break
        print(pz, "intento", intento, "juez:", [(x.get("acento"), x.get("distincion_c_z"), x.get("entonacion_espana")) for x in a], "-> otra toma", flush=True)
        if intento < 8:
            hale.unlink()
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + KEY, "-F", "model_id=scribe_v1", "-F", "language_code=spa", "-F", f"file=@{hale}"], capture_output=True)
    sc = json.loads(r.stdout)
    (voz / f"{pz}_scribe.json").write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
    w = [x for x in sc["words"] if x.get("type") == "word"]
    print(pz, "palabras", len(w), "hablado", round(w[-1]["end"] - w[0]["start"], 1), "s | Gemini:", json.dumps(a, ensure_ascii=False), flush=True)
