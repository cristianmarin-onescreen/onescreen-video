"""Imagen -> video con Gemini Omni Flash (Google AI Studio, Interactions API).
Los Veo 3.1 fueron retirados por Google (28-oct-2026): este script los reemplaza.
Uso: python veo_i2v.py IMAGEN.png SALIDA.mp4 "prompt" [--aspecto 9:16] [--res 720p]
Clave: GEMINI_API_KEY o GOOGLE_AI_STUDIO (variable de entorno). Audio: se genera siempre, se descarta en el montaje."""
import argparse, base64, json, mimetypes, os, sys, time, urllib.request, urllib.error

KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_STUDIO")
URL = "https://generativelanguage.googleapis.com/v1beta/interactions"


def buscar_video(obj):
    """Devuelve los bytes base64 del primer bloque de video que encuentre en la respuesta."""
    if isinstance(obj, dict):
        if obj.get("type") == "video" and obj.get("data"):
            return obj["data"]
        for v in obj.values():
            r = buscar_video(v)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = buscar_video(v)
            if r:
                return r
    return None


def generar(imagen, salida, prompt, aspecto="9:16", res="720p", intentos=6):
    mime = mimetypes.guess_type(imagen)[0] or "image/png"
    b64 = base64.b64encode(open(imagen, "rb").read()).decode()
    cuerpo = {"model": "gemini-omni-1.1-flash",
              "input": [{"type": "image", "data": b64, "mime_type": mime}, {"type": "text", "text": prompt}],
              "generation_config": {"video_config": {"task": "image_to_video"}},
              "response_format": {"type": "video", "aspect_ratio": aspecto, "resolution": res}}
    for n in range(1, intentos + 1):
        req = urllib.request.Request(URL, data=json.dumps(cuerpo).encode(),
                                     headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                resp = json.load(r)
        except urllib.error.HTTPError as e:
            print(f"intento {n}: HTTP {e.code} {e.read()[:200]}", file=sys.stderr)
            if e.code == 429:  # limite de tasa (4/min en Tier 1): no se cobra, se espera y se repite
                time.sleep(75)
                continue
            raise SystemExit(f"HTTP {e.code}: no se reintenta (cuesta dinero real)")
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:   # corte de red/SSL: no hubo respuesta, se repite pocas veces
            print(f"intento {n}: red {e}", file=sys.stderr)
            if n >= 4:
                raise SystemExit(f"sin red tras {n} intentos: {e}")
            time.sleep(20)
            continue
        datos = buscar_video(resp)
        if not datos:
            open(salida + ".json", "w").write(json.dumps(resp)[:5000])
            raise SystemExit(f"sin video (ver {salida}.json): no se reintenta (cuesta dinero real)")
        open(salida, "wb").write(base64.b64decode(datos))
        return salida
    raise SystemExit("Omni no devolvio video")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("imagen"); p.add_argument("salida"); p.add_argument("prompt")
    p.add_argument("--aspecto", default="9:16"); p.add_argument("--res", default="720p")
    a = p.parse_args()
    print(generar(a.imagen, a.salida, a.prompt, a.aspecto, a.res))
