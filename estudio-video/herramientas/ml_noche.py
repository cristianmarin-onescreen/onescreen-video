"""Cadena desatendida de los videos de Mercado Libre que faltan (Cris, 28-oct: "mañana a las 6 am todos listos").
Espera a que Google reinicie la cuota diaria de la API (2:00 a. m. hora de Colombia = medianoche del Pacífico) y luego:
  1. mueve a veo/rechazados los clips malos del Poster y genera 2 clips por SKU (un intento por clip; solo se espera ante 429)
  2. revisa cada clip contra el render de la ficha con un modelo de visión barato (producto igual / distinto) y regenera UNA vez,
     como máximo REDOS veces en total, los que salgan distintos (se le dice al modelo qué cambió)
  3. voz (receta única), armado y render de cada video
  4. copia los 12 videos a Entrega_Alejandro/<SKU>.mp4 y escribe Informe_entrega.md con lo que NO se pudo verificar
Uso: python ml_noche.py [--ahora]   (--ahora no espera la hora)   |   python ml_noche.py verificar SKU k"""
import base64, datetime as dt, json, os, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ml_producto as m  # noqa: E402
from veo_i2v import generar  # noqa: E402

BASE = m.BASE
LOG = BASE / "noche_log.txt"
NUEVOS = ["OSP-72", "MC1500", "OCMIC60", "CAMWEB", "OPSL7I7"]
LISTOS = ["A10W", "CAST2", "OCWL10C", "CAMSNAP2", "CAMPTZ", "MC1800", "LAPIZP"]
REDOS = 4
KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_STUDIO")
MODELO_VISION = "gemini-3.5-flash-lite"


def log(*a):
    linea = f"{dt.datetime.now():%H:%M:%S} " + " ".join(str(x) for x in a)
    print(linea, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def esperar(hora=2, minuto=3):
    ahora = dt.datetime.now()
    meta = ahora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
    if meta <= ahora:
        meta += dt.timedelta(days=1) if ahora.hour >= 12 else dt.timedelta(0)
    log("espero hasta", meta)
    while dt.datetime.now() < meta:
        time.sleep(30)


def jpg(b):
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(b).decode()}}


def fotogramas(clip, n=3):
    salida = []
    for t in (1.5, 4.5, 8.0)[:n]:
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(clip), "-frames:v", "1", "-vf", "scale=512:-1",
                            "-f", "mjpeg", "-"], capture_output=True)
        if r.stdout:
            salida.append(r.stdout)
    return salida


def verificar(sku, k):
    """(igual, diferencias) del producto del clip frente al render oficial de la ficha. Un modelo de vision barato: no sustituye mirar."""
    clip = BASE / "veo" / f"{sku}_{k}.mp4"
    refs = []
    for nombre in ("hero", "prod"):
        ruta = BASE / "img" / f"{sku}_{nombre}.png"
        if ruta.exists():
            r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ruta), "-frames:v", "1", "-vf", "scale=640:-1", "-f", "mjpeg", "-"], capture_output=True)
            refs.append(r.stdout)
    texto = ("Las primeras imágenes son el render OFICIAL del producto (puede aparecer solo o en una escena). Las últimas son fotogramas de un video "
             "generado con IA que debe mostrar ese MISMO producto. Compara forma, proporciones (alto/ancho/grosor), colores, materiales, puertos, "
             "luces, botones y cualquier elemento que el video haya inventado, deformado o agrandado. Ignora la escena, las personas y el texto de la "
             "publicidad en pantallas. Responde SOLO JSON: {\"igual\": true|false, \"diferencias\": [\"...\"]}. 'igual' es false si un comprador "
             "pensaría que es otro producto o que tiene características que no tiene.")
    partes = [{"text": texto}] + [jpg(x) for x in refs] + [{"text": "Fotogramas del video generado:"}] + [jpg(x) for x in fotogramas(clip)]
    cuerpo = {"contents": [{"parts": partes}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO_VISION}:generateContent",
                                 json.dumps(cuerpo).encode(), {"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        res = json.load(r)
    j = json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
    return bool(j.get("igual")), j.get("diferencias", [])


def clips_nuevos():
    veo = BASE / "veo"
    malos = veo / "rechazados"
    malos.mkdir(exist_ok=True)
    for f in veo.glob("OSP-72_*.mp4"):          # los del 28-oct alteraron el producto (Cris: "no es igual al real")
        shutil.move(str(f), str(malos / f"{f.stem}_28oct.mp4"))
    m.clips(NUEVOS)


def revisar_y_rehacer():
    redos, estado = REDOS, {}
    for sku in NUEVOS:
        for k in "abc":
            clip = BASE / "veo" / f"{sku}_{k}.mp4"
            if not clip.exists():
                continue
            try:
                igual, dif = verificar(sku, k)
            except Exception as e:   # sin verificador: queda marcado, no se reintenta a ciegas
                estado[f"{sku}_{k}"] = ("SIN VERIFICAR", [str(e)[:120]]); log(sku, k, "verificador falló", e); continue
            log(sku, k, "igual" if igual else "DISTINTO", dif)
            if not igual and redos > 0:
                redos -= 1
                shutil.move(str(clip), str(BASE / "veo" / "rechazados" / f"{sku}_{k}_distinto.mp4"))
                imagen = "prod" if (k == "b" and sku in ("MC1500", "OCMIC60", "OPSL7I7")) or (k == "a" and sku == "MC1500") else "hero"
                extra = " The previous attempt was wrong because: " + "; ".join(dif)[:400] + ". Fix exactly that and stay faithful to the reference."
                try:
                    generar(str(BASE / "img" / f"{sku}_{imagen}.png"), str(clip), m.P[sku][k] + " " + m.NO_CAMBIAR + extra)
                    igual, dif = verificar(sku, k)
                    log(sku, k, "reintento:", "igual" if igual else "SIGUE DISTINTO", dif)
                except BaseException as e:
                    log(sku, k, "reintento falló", e); igual, dif = False, [f"reintento falló: {e}"]
            estado[f"{sku}_{k}"] = ("igual" if igual else "REVISAR", dif)
    (BASE / "revision_clips.json").write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")
    return estado


def medir(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    lu = subprocess.run(["ffmpeg", "-nostdin", "-i", str(f), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = [x for x in lu.splitlines() if x.strip().startswith("I:")]
    return r.stdout.split("\n")[0], (lufs[-1].split()[1] if lufs else "?")


def entrega(estado):
    destino = BASE / "Entrega_Alejandro"
    destino.mkdir(exist_ok=True)
    filas = ["# Entrega a Alejandro: videos de Mercado Libre", "", f"Generado {dt.datetime.now():%Y-%m-%d %H:%M}. Un archivo por SKU, vertical 1080x1920.", "",
             "| SKU | Estado | Ancho,alto,duración (s) | Volumen (LUFS) | Aviso |", "|---|---|---|---|---|"]
    for sku in LISTOS[:-1] + NUEVOS + ["LAPIZP"]:
        f = BASE / "Exports" / f"{sku}.mp4"
        if not f.exists():
            filas.append(f"| {sku} | FALTA | - | - | no se generó |"); continue
        shutil.copy(f, destino / f"{sku}.mp4")
        info, lufs = medir(f)
        avisos = [f"{k}: {v[0]} {'; '.join(v[1])}" for k, v in estado.items() if k.startswith(sku + "_") and v[0] != "igual"]
        filas.append(f"| {sku} | listo | {info} | {lufs} | {' / '.join(avisos) if avisos else ''} |")
    filas += ["", "Los clips de IA se compararon con el render de la ficha con un modelo de visión barato (no sustituye una mirada humana).",
              "Mic-60 sale como 'Amplifyr' (nombre de la ficha OCMIC60.0001) y la webcam usa solo specs comunes a WebCam 101/102."]
    (BASE / "Informe_entrega.md").write_text("\n".join(filas), encoding="utf-8")
    log("entrega lista en", destino)


def main():
    if "--ahora" not in sys.argv:
        esperar()
    log("== inicio de la cadena nocturna ==")
    clips_nuevos()
    estado = revisar_y_rehacer()
    m.voz([s for s in NUEVOS if sum((BASE / "veo" / f"{s}_{k}.mp4").exists() for k in "abc") >= 2])
    armables = [s for s in NUEVOS if sum((BASE / "veo" / f"{s}_{k}.mp4").exists() for k in "abc") >= 2]
    m.build(armables)
    m.render(armables)
    entrega(estado)
    log("== fin ==")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verificar":
        print(verificar(sys.argv[2], sys.argv[3]))
    else:
        main()
