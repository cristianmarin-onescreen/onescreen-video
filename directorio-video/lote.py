"""Lote del Directorio de video: copia liviana → Files API → Batch API de Gemini 3.5 Flash-Lite → pestañas Directorio y Segmentos.

Orden: datos/planos.json (lo arma armar_cola.py) ya viene en la prioridad de Cris: con color primero, luego los más recientes.
Procesa los planos con archivo en disco; con --drive también los que solo están en Drive (los baja con rclone, uno o dos a la vez,
y los borra tras la copia). Reanudable: el estado vive en datos/estado.json; si se corta, se vuelve a correr igual.
Con --reanalisis trabaja sobre datos/planos_reanalisis.json (armar_cola.py --ids) con estado y fichas aparte, manda a Gemini
imágenes de referencia de productos (datos/referencias) y en Segmentos cambia los tramos viejos por los nuevos.
Uso: python lote.py [--drive] [--reanalisis] [--limite N] [--tope USD] [--tam-lote N] [--reintentar-errores] [--max-salida N]
"""
import argparse
import collections
import concurrent.futures
import contextlib
import json
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request

import comun
from comun import API, MODELO

KEY = os.environ["GEMINI_API_KEY"]
PROXIES = os.path.join(comun.DATOS, "proxies")
FICHAS = os.path.join(comun.DATOS, "fichas")
ESTADO = os.path.join(comun.DATOS, "estado.json")
LOG = os.path.join(comun.DATOS, "lote.log")
MAX_LOTES_EN_VUELO = 3
TOKENS_MAX_LOTE = 3_000_000
ITEMS_POR_ESCRITURA = 40
MAX_SEGUNDOS = 9000  # a resolución media (91 tok/s) caben ~3 h en 1M de contexto, pero la baja da "invalid argument": se corta en 2 h 30 min
COPIAS_POR_DISCO = 2  # con -discard el HDD queda esperando seeks: una sola copia lo dejaba al 15-57 % de ocupación
# Drive: rclone con un remoto "gdrive" de solo lectura (rclone config create gdrive drive scope=drive.readonly)
RCLONE = os.environ.get("RCLONE", os.path.join(os.path.expanduser("~"), "herramientas", "rclone", "rclone.exe"))
TEMP_DRIVE = os.environ.get("LOTE_TEMP_DRIVE", r"D:\_lote_drive")
TAMANOS_DRIVE = os.path.join(comun.DATOS, "tamanos_drive.json")  # opcional: ID plano → bytes, para no llenar el disco
PLANOS = os.path.join(comun.DATOS, "planos.json")
REFERENCIAS = os.path.join(comun.DATOS, "referencias")
NOTAS_REFERENCIA = {  # archivo .jpg → lo que Gemini debe saber de la imagen
    "wandr_completo": "Wandr de OneScreen (la pantalla vertical sobre un poste, a la derecha; la de la pared es otra pantalla OneScreen).",
    "wandr_logo_trasero": "parte trasera del Wandr: blanca, con perforaciones y el logo Wandr.",
    "wandr_base": "base redonda y pesada del Wandr.",
    "t7_render": "pantalla interactiva OneScreen T7 (render oficial).",
    "NO_trituradora_IDEAL": "NO es OneScreen: trituradora de papel IDEAL (blanca, botón con luz verde).",
    "NO_impresora_Pantum": "NO es OneScreen: impresora Pantum.",
    "NO_parlante_ClaryBass": "NO es OneScreen: parlante Clary Bass (aunque tenga manija y ruedas).",
}


def usar_reanalisis():
    global PLANOS, ESTADO, FICHAS, LOG
    PLANOS = os.path.join(comun.DATOS, "planos_reanalisis.json")
    ESTADO = os.path.join(comun.DATOS, "estado_reanalisis.json")
    FICHAS = os.path.join(comun.DATOS, "fichas_reanalisis")  # las fichas del primer lote se conservan
    LOG = os.path.join(comun.DATOS, "reanalisis.log")

candado = threading.Lock()
semaforos = {}  # un semáforo por letra de disco, creado al primer uso
cupo = None  # con --drive: bytes que pueden ocupar a la vez los videos bajados de Drive
tamanos = json.load(open(TAMANOS_DRIVE, encoding="utf-8")) if os.path.exists(TAMANOS_DRIVE) else {}


class Cupo:
    """Reserva de espacio en TEMP_DRIVE: el disco está casi lleno y un video de Drive puede pesar 12 GB."""

    def __init__(self, total):
        self.total, self.usado, self.cond = total, 0, threading.Condition()

    @contextlib.contextmanager
    def reservar(self, n):
        n = min(n, self.total)
        with self.cond:
            self.cond.wait_for(lambda: self.usado + n <= self.total)
            self.usado += n
        try:
            yield
        finally:
            with self.cond:
                self.usado -= n
                self.cond.notify_all()


def log(*partes):
    linea = comun.ahora() + " " + " ".join(str(p) for p in partes)
    print(linea, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def pedir(url, datos=None, metodo="GET", headers=None, reintentos=5, espera=180):
    """espera = segundos sin recibir nada antes de cortar: una conexión colgada frenó el lote 17 min con 900."""
    for intento in range(reintentos):
        req = urllib.request.Request(url, data=datos, method=metodo, headers={"x-goog-api-key": KEY, **(headers or {})})
        try:
            r = urllib.request.urlopen(req, timeout=espera)
            return r, r.read()
        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode("utf-8", "replace")[:400]
            if e.code not in (429, 500, 502, 503, 504) or intento == reintentos - 1:
                raise RuntimeError(f"HTTP {e.code}: {cuerpo}") from e
        except (ConnectionError, OSError):
            if intento == reintentos - 1:
                raise
        time.sleep(15 * (intento + 1))


def guardar(est):
    with candado:
        tmp = ESTADO + ".tmp"
        json.dump(est, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        os.replace(tmp, ESTADO)


def duracion(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True, timeout=120)
    return float(r.stdout.strip() or 0)


def subir(ruta, nombre, tipo="video/mp4"):
    tam = os.path.getsize(ruta)
    for intento in range(4):  # si la conexión se cae a mitad de la subida, se abre una sesión nueva
        r, _ = pedir(f"{API}/upload/v1beta/files", json.dumps({"file": {"display_name": nombre}}).encode(), "POST",
                     {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
                      "X-Goog-Upload-Header-Content-Length": str(tam), "X-Goog-Upload-Header-Content-Type": tipo,
                      "Content-Type": "application/json"})
        try:
            _, cuerpo = pedir(r.headers["x-goog-upload-url"], open(ruta, "rb").read(), "POST",
                              {"Content-Length": str(tam), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, 1)
            break
        except (OSError, RuntimeError):
            if intento == 3:
                raise
            time.sleep(15 * (intento + 1))
    archivo = json.loads(cuerpo)["file"]
    while archivo.get("state") == "PROCESSING":
        time.sleep(4)
        archivo = json.loads(pedir(f"{API}/v1beta/{archivo['name']}")[1])
    if archivo.get("state") != "ACTIVE":
        raise RuntimeError(f"archivo no quedó activo: {str(archivo)[:200]}")
    return archivo


def borrar_archivo(nombre):
    try:
        pedir(f"{API}/v1beta/{nombre}", metodo="DELETE", reintentos=2)
    except Exception:
        pass  # caduca solo a las 48 h


def bajar_de_drive(p):
    fid = re.search(r"/d/([\w-]+)", p["links"][0]).group(1)
    destino = os.path.join(TEMP_DRIVE, p["id"] + os.path.splitext(p["clip"])[1].lower())
    r = subprocess.run([RCLONE, "backend", "copyid", "gdrive:", fid, destino], capture_output=True, timeout=4 * 3600)
    if r.returncode != 0 or not os.path.exists(destino):
        if os.path.exists(destino):
            os.remove(destino)
        raise RuntimeError("rclone: " + r.stderr.decode("utf-8", "replace")[-300:])
    return destino


def producir(p, rapido_ok=True):
    """Copia liviana y subida a la Files API. Si el plano solo está en Drive (y se corre con --drive), lo baja antes y lo borra después."""
    ruta = next((r for r in p["rutas"] if os.path.exists(r)), None)
    if ruta:
        return copiar_y_subir(p, ruta, rapido_ok)
    if not (cupo and p["links"]):
        return {"estado": "omitido", "motivo": "sin archivo en disco"}
    with cupo.reservar(tamanos.get(p["id"], 6e9)):
        t0 = time.time()
        local = bajar_de_drive(p)
        seg_bajada = round(time.time() - t0, 1)
        try:
            res = copiar_y_subir(p, local, rapido_ok)
        finally:
            os.remove(local)
    res.update(ruta=p["links"][0], seg_bajada=seg_bajada)
    return res


def copiar_y_subir(p, ruta, rapido_ok):
    """Copia a 720p y 1 cuadro/s (con audio) y la sube a la Files API. Se borra la copia local al terminar."""
    proxy = os.path.join(PROXIES, p["id"] + ".mp4")
    # a 1 cuadro/s bastan los cuadros clave (cámara y celular tienen GOP de ≤1 s) y -discard hace que el demuxer ni lea los demás:
    # 7 s en vez de 68 s en un archivo de 3,2 GB del disco D:. Los archivos chicos se decodifican enteros: los clips de IA
    # traen un solo cuadro clave y las grabaciones de pantalla los espacian mucho.
    rapido = rapido_ok and p["origen"] != "Grabación de pantalla" and os.path.getsize(ruta) > 200e6
    entrada = ["-discard:v", "nokey"] if rapido else []
    recortado = (p["dur_s"] or 0) > MAX_SEGUNDOS
    # en el reintento: algunos ProRes de stock traen color_trc desconocido y libx264 no abre (error -129/-22)
    filtro = ("" if rapido_ok else "setparams=color_trc=bt709,") + "scale=-2:'trunc(min(720,ih)/2)*2',fps=1"
    cmd = ["ffmpeg", "-y", "-v", "error", *entrada, "-i", ruta, *(["-t", str(MAX_SEGUNDOS)] if recortado else []),
           "-map", "0:v:0", "-map", "0:a:0?",
           "-vf", filtro, "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-g", "10",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-movflags", "+faststart", proxy]
    t0 = time.time()
    try:
        with semaforos.setdefault(ruta[0].upper(), threading.Semaphore(COPIAS_POR_DISCO)):
            r = subprocess.run(cmd, capture_output=True, timeout=max(900, (p["dur_s"] or 600) * 2))
        if r.returncode != 0 or not os.path.exists(proxy) or os.path.getsize(proxy) < 1000:
            raise RuntimeError("ffmpeg: " + r.stderr.decode("utf-8", "replace")[-300:])
        seg_copia = round(time.time() - t0, 1)
        dur = duracion(proxy) or p["dur_s"] or 0
        mb = round(os.path.getsize(proxy) / 1e6, 1)
        archivo = subir(proxy, f"{p['id']}_{p['clip']}"[:120])
    finally:
        if os.path.exists(proxy):
            os.remove(proxy)
    return {"estado": "subido", "archivo": archivo["name"], "uri": archivo["uri"], "dur_s": round(dur, 1), "ruta": ruta,
            "seg_copia": seg_copia, "mb": mb, "subido": time.time(), "recortado": recortado}


def texto_respuesta(resp):
    partes = resp["candidates"][0]["content"]["parts"]
    return "".join(x.get("text", "") for x in partes if not x.get("thought"))


class Lote:
    def __init__(self, args):
        self.args = args
        self.planos = json.load(open(PLANOS, encoding="utf-8"))
        self.por_id = {p["id"]: p for p in self.planos}
        self.orden = {p["id"]: n for n, p in enumerate(self.planos)}
        universo = [p for p in self.planos if p["rutas"] or (args.drive and p["links"])]
        if args.limite:
            universo = universo[:args.limite]
        self.universo = [p["id"] for p in universo]
        self.est = json.load(open(ESTADO, encoding="utf-8")) if os.path.exists(ESTADO) else {"items": {}, "lotes": {}, "gastado": 0.0}
        self.items = self.est["items"]
        self.sin_rapido = set()  # los que ffmpeg no pudo copiar leyendo solo cuadros clave
        if args.reintentar_errores:
            for i in self.universo:
                if self.items.get(i, {}).get("estado") == "error":
                    if self.items[i].get("motivo", "").startswith("copia/subida: ffmpeg"):
                        self.sin_rapido.add(i)
                    self.items[i] = {"estado": "pendiente"}
        self.cola = [i for i in self.universo if self.items.get(i, {}).get("estado") in (None, "pendiente")]
        self.en_curso = {}
        self.sin_presupuesto = False
        self.referencias = self.subir_referencias() if args.reanalisis else None
        self.reanudar()

    def subir_referencias(self):
        """Las imágenes caducan a las 48 h como los videos: se vuelven a subir si las guardadas ya están viejas."""
        if self.est.get("referencias") and time.time() - self.est.get("referencias_subidas", 0) < 40 * 3600:
            return self.est["referencias"]
        refs = [[nota, subir(os.path.join(REFERENCIAS, nombre + ".jpg"), "ref_" + nombre, "image/jpeg")["uri"]]
                for nombre, nota in NOTAS_REFERENCIA.items()]
        self.est.update(referencias=refs, referencias_subidas=time.time())
        guardar(self.est)
        return refs

    # ---------- estado ----------
    def reanudar(self):
        """Archivos subidos hace más de 40 h ya no sirven (caducan a las 48 h): se vuelven a copiar."""
        for i, it in self.items.items():
            if it.get("estado") == "subido" and time.time() - it.get("subido", 0) > 40 * 3600:
                self.items[i] = {"estado": "pendiente"}
                self.cola.append(i)
        self.cola.sort(key=self.orden.get)

    def con_estado(self, *estados):
        return sorted((i for i, it in self.items.items() if it.get("estado") in estados), key=self.orden.get)

    def dur(self, i):
        return self.items.get(i, {}).get("dur_s") or self.por_id[i]["dur_s"] or 600

    def comprometido(self):
        en_vuelo = self.con_estado("subido", "enviado") + list(self.en_curso.values())
        return self.est["gastado"] + sum(comun.costo_estimado(self.dur(i)) for i in en_vuelo)

    # ---------- 1. copias y subidas ----------
    def alimentar(self, pool):
        ventana = int(self.args.tam_lote * 1.5)
        while self.cola and not self.sin_presupuesto and len(self.en_curso) + len(self.con_estado("subido")) < ventana:
            i = self.cola[0]
            if self.comprometido() + comun.costo_estimado(self.dur(i)) > self.args.tope:
                self.sin_presupuesto = True
                log(f"TOPE: con {i} se pasaría de USD {self.args.tope}; no se copian más planos")
                break
            self.cola.pop(0)
            self.en_curso[pool.submit(producir, self.por_id[i], i not in self.sin_rapido)] = i

    def cosechar(self):
        for f in [f for f in self.en_curso if f.done()]:
            i = self.en_curso.pop(f)
            try:
                res = f.result()
            except Exception as e:
                # sin índice (copia o grabación cortada a medias) no hay nada que analizar: no se reintenta
                estado = "dañado" if "Invalid data found" in str(e) else "error"
                res = {"estado": estado, "motivo": f"copia/subida: {str(e)[:300]}"}
            self.items[i] = res
            if res["estado"] == "subido":
                bajada = f"bajada {res['seg_bajada']} s, " if "seg_bajada" in res else ""
                log(f"subido {i} {self.por_id[i]['clip']} | {res['dur_s']} s | {bajada}copia {res['seg_copia']} s, {res['mb']} MB")
            else:
                log(f"{res['estado']} {i} {self.por_id[i]['clip']}: {res.get('motivo')}")
            guardar(self.est)

    # ---------- 2. lotes de Gemini ----------
    def enviar(self, final):
        listos = self.con_estado("subido")
        if not listos or len(self.est["lotes"]) >= MAX_LOTES_EN_VUELO:
            return
        if len(listos) < self.args.tam_lote and not final:
            return
        ids, tokens = [], 0
        for i in listos[:self.args.tam_lote]:
            t = self.dur(i) * comun.resolucion(self.dur(i))[1]
            if ids and tokens + t > TOKENS_MAX_LOTE:
                break
            ids.append(i)
            tokens += t
        pedidos = [{"request": comun.solicitud(self.por_id[i], self.items[i]["uri"], self.dur(i), self.referencias), "metadata": {"key": i}}
                   for i in ids]
        cuerpo = {"batch": {"display_name": f"directorio-{int(time.time())}", "input_config": {"requests": {"requests": pedidos}}}}
        op = json.loads(pedir(f"{API}/v1beta/models/{MODELO}:batchGenerateContent", json.dumps(cuerpo).encode(), "POST",
                              {"Content-Type": "application/json"}, espera=600)[1])
        self.est["lotes"][op["name"]] = {"ids": ids, "creado": time.time()}
        for i in ids:
            self.items[i]["estado"] = "enviado"
            self.items[i]["lote"] = op["name"]
        guardar(self.est)
        log(f"lote {op['name']} enviado: {len(ids)} planos, ~{int(tokens):,} tokens de video")

    def fallo(self, i, motivo):
        it = self.items[i]
        it["intentos"] = it.get("intentos", 0) + 1
        it["motivo"] = str(motivo)[:300]
        if it["intentos"] < 2:
            it["estado"] = "subido"  # se reintenta en otro lote con el mismo archivo
        else:
            it["estado"] = "error"
            borrar_archivo(it["archivo"])
        log(f"falló {i} (intento {it['intentos']}): {it['motivo']}")

    def sondear(self):
        for nombre, lote in list(self.est["lotes"].items()):
            op = json.loads(pedir(f"{API}/v1beta/{nombre}")[1])
            estado = (op.get("metadata") or {}).get("state") or op.get("state")
            if estado in ("BATCH_STATE_PENDING", "BATCH_STATE_RUNNING"):
                continue
            vistos = set()
            if estado == "BATCH_STATE_SUCCEEDED":
                salida = (op.get("response") or {}).get("inlinedResponses") or op["metadata"]["output"]["inlinedResponses"]
                for r in salida.get("inlinedResponses", []):
                    i = (r.get("metadata") or {}).get("key")
                    if i in lote["ids"]:
                        vistos.add(i)
                        self.recibir(i, r)
            for i in lote["ids"]:
                if i not in vistos:
                    self.fallo(i, f"lote {estado}")
            del self.est["lotes"][nombre]
            guardar(self.est)
            log(f"lote {nombre} {estado} ({round((time.time() - lote['creado']) / 60, 1)} min) | gastado USD {self.est['gastado']:.3f}")

    def recibir(self, i, r):
        if "error" in r:
            return self.fallo(i, r["error"])
        resp = r["response"]
        uso = resp.get("usageMetadata", {})
        costo = comun.costo_real(uso)
        self.est["gastado"] += costo
        it = self.items[i]
        it.update(costo=round(costo, 5), tok_entrada=uso.get("promptTokenCount", 0),
                  tok_salida=uso.get("candidatesTokenCount", 0) + uso.get("thoughtsTokenCount", 0),
                  fin=(resp.get("candidates") or [{}])[0].get("finishReason"))
        try:
            ficha = json.loads(texto_respuesta(resp))
            if "segmentos" not in ficha:
                raise ValueError("respuesta incompleta")
        except Exception as e:
            return self.fallo(i, f"respuesta ilegible ({it['fin']}): {e}")
        json.dump({"ficha": ficha, "uso": uso, "modelo": resp.get("modelVersion")}, open(os.path.join(FICHAS, i + ".json"), "w",
                  encoding="utf-8"), ensure_ascii=False, indent=1)
        it["estado"] = "para_hoja"
        borrar_archivo(it["archivo"])

    # ---------- 3. Sheet ----------
    def escribir(self):
        ids = self.con_estado("para_hoja")
        if not ids:
            return
        if self.args.reanalisis:
            return self.reescribir(ids)
        col_a = comun.sheets("valores", "'Directorio'!A1:A")["values"][0]
        fila = {v.replace(".", "").replace(",", ""): n for n, v in enumerate(col_a)}
        info = (comun.sheets("valores", "'Directorio'!P1:P").get("values") or [[]])[0]
        seg_a = comun.sheets("valores", "'Segmentos'!A1:A")["values"][0]
        if col_a[0] != "ID" or seg_a[0] != "ID plano":  # sin encabezado la lectura vino mal: no escribir encima de nada
            raise RuntimeError(f"encabezados inesperados: Directorio {col_a[:1]}, Segmentos {seg_a[:1]}")
        ya = {v.replace(".", "").replace(",", "") for v in seg_a[1:]}
        siguiente = len(seg_a)
        filas_seg = next(s["properties"]["gridProperties"]["rowCount"] for s in comun.sheets("meta", "-")["sheets"]
                         if s["properties"]["sheetId"] == 9007)
        grupos = []
        for i in ids:
            if i not in fila:
                self.items[i].update(estado="error", motivo="el ID ya no está en el Directorio")
                continue
            ficha = json.load(open(os.path.join(FICHAS, i + ".json"), encoding="utf-8"))["ficha"]
            if self.items[i].get("recortado"):
                ficha["informacion_adicional"] = "Analizadas solo las primeras 2 h 30 min. " + ficha["informacion_adicional"]
            n = fila[i]
            reqs = comun.celdas_directorio(n, ficha, self.por_id[i], info[n] if n < len(info) else "", self.dur(i))
            if i not in ya:
                segs = comun.filas_segmentos(self.por_id[i], ficha, self.dur(i))
                reqs += comun.celdas_segmentos(siguiente, segs)
                siguiente += len(segs)
            grupos.append((i, reqs))
        if siguiente > filas_seg:
            grupos.insert(0, (None, [{"appendDimension": {"sheetId": 9007, "dimension": "ROWS",
                                                          "length": siguiente - filas_seg + 2000}}]))
        for k in range(0, len(grupos), ITEMS_POR_ESCRITURA):
            parte = grupos[k:k + ITEMS_POR_ESCRITURA]
            archivo = os.path.join(comun.DATOS, "escritura.json")
            json.dump([r for _, reqs in parte for r in reqs], open(archivo, "w", encoding="utf-8"), ensure_ascii=False)
            resp = comun.sheets("batch", archivo)
            if "replies" not in resp:
                raise RuntimeError(f"Sheets no aceptó la escritura: {str(resp)[:400]}")
            for i, _ in parte:
                if i:
                    self.items[i]["estado"] = "hecho"
            guardar(self.est)
        log(f"Sheet: {len([g for g in grupos if g[0]])} filas del Directorio escritas; Segmentos va en la fila {siguiente}")

    def reescribir(self, ids):
        """Re-análisis: sobrescribe la fila del Directorio, llena la duración si faltaba y cambia los tramos viejos del plano por
        los nuevos. Va de a ITEMS_POR_ESCRITURA planos y relee las columnas antes de cada tanda: borrar tramos corre las filas."""
        for k in range(0, len(ids), ITEMS_POR_ESCRITURA):
            parte = ids[k:k + ITEMS_POR_ESCRITURA]
            col_a = comun.sheets("valores", "'Directorio'!A1:A")["values"][0]
            info = (comun.sheets("valores", "'Directorio'!P1:P").get("values") or [[]])[0]
            duraciones = (comun.sheets("crudos", "'Directorio'!AE1:AE").get("values") or [[]])[0]
            seg_a = comun.sheets("valores", "'Segmentos'!A1:A")["values"][0]
            if col_a[0] != "ID" or seg_a[0] != "ID plano":  # sin encabezado la lectura vino mal: no escribir encima de nada
                raise RuntimeError(f"encabezados inesperados: Directorio {col_a[:1]}, Segmentos {seg_a[:1]}")
            fila = {v.replace(".", "").replace(",", ""): n for n, v in enumerate(col_a)}
            viejas = sorted((n for n, v in enumerate(seg_a) if v.replace(".", "").replace(",", "") in parte), reverse=True)
            reqs = [{"deleteDimension": {"range": {"sheetId": 9007, "dimension": "ROWS", "startIndex": n, "endIndex": n + 1}}}
                    for n in viejas]
            siguiente = len(seg_a) - len(viejas)
            hechos = []
            for i in parte:
                if i not in fila:
                    self.items[i].update(estado="error", motivo="el ID ya no está en el Directorio")
                    continue
                ficha = json.load(open(os.path.join(FICHAS, i + ".json"), encoding="utf-8"))["ficha"]
                if self.items[i].get("recortado"):
                    ficha["informacion_adicional"] = "Analizadas solo las primeras 2 h 30 min. " + ficha["informacion_adicional"]
                n = fila[i]
                reqs += comun.celdas_directorio(n, ficha, self.por_id[i], info[n] if n < len(info) else "", self.dur(i))
                if n >= len(duraciones) or duraciones[n] in ("", None):
                    reqs.append({"updateCells": {"rows": [{"values": [comun._num(round(self.dur(i)))]}], "fields": "userEnteredValue",
                                                 "start": {"sheetId": 0, "rowIndex": n, "columnIndex": 30}}})
                segs = comun.filas_segmentos(self.por_id[i], ficha, self.dur(i))
                reqs += comun.celdas_segmentos(siguiente, segs)
                siguiente += len(segs)
                hechos.append(i)
            archivo = os.path.join(comun.DATOS, "escritura.json")
            json.dump(reqs, open(archivo, "w", encoding="utf-8"), ensure_ascii=False)
            resp = comun.sheets("batch", archivo)
            if "replies" not in resp:
                raise RuntimeError(f"Sheets no aceptó la escritura: {str(resp)[:400]}")
            for i in hechos:
                self.items[i]["estado"] = "hecho"
            guardar(self.est)
            log(f"Sheet: {len(hechos)} planos re-escritos, {len(viejas)} tramos viejos cambiados")

    def resumen(self):
        c = collections.Counter(self.items[i].get("estado", "pendiente") if i in self.items else "pendiente" for i in self.universo)
        c["copiando"] = len(self.en_curso)
        c["pendiente"] -= len(self.en_curso)
        log("avance:", dict(c), f"| gastado USD {self.est['gastado']:.3f} | comprometido USD {self.comprometido():.3f}")

    def correr(self):
        log(f"inicio: {len(self.universo)} planos en el universo, {len(self.cola)} por copiar, tope USD {self.args.tope}")
        ultimo_sondeo = ultimo_resumen = 0
        with concurrent.futures.ThreadPoolExecutor(self.args.hilos) as pool:
            while True:
                self.cosechar()
                self.alimentar(pool)
                sin_copias = not self.en_curso and (not self.cola or self.sin_presupuesto)
                try:
                    self.enviar(final=sin_copias)
                    if time.time() - ultimo_sondeo > 60:
                        ultimo_sondeo = time.time()
                        self.sondear()
                        self.escribir()
                except Exception as e:  # una caída de red o de Sheets no debe tumbar el lote: se reintenta en la próxima vuelta
                    log("ERROR (se reintenta):", str(e)[:400])
                if time.time() - ultimo_resumen > 600:
                    ultimo_resumen = time.time()
                    self.resumen()
                if sin_copias and not self.est["lotes"] and not self.con_estado("subido", "enviado", "para_hoja"):
                    break
                time.sleep(5)
        self.resumen()
        log("fin")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int)
    ap.add_argument("--tope", type=float, default=30.0)
    ap.add_argument("--tam-lote", type=int, default=100)
    ap.add_argument("--reintentar-errores", action="store_true", help="vuelve a copiar los que fallaron al copiar o subir")
    ap.add_argument("--hilos", type=int, default=8, help="copias+subidas en paralelo (las copias igual van de a 1 por disco duro)")
    ap.add_argument("--copias-por-disco", type=int, default=COPIAS_POR_DISCO)
    ap.add_argument("--max-salida", type=int, default=comun.MAX_SALIDA, help="tope de tokens de la respuesta de Gemini")
    ap.add_argument("--drive", action="store_true", help="incluye los planos que solo están en Drive (los baja con rclone)")
    ap.add_argument("--reanalisis", action="store_true", help="re-analiza datos/planos_reanalisis.json con imágenes de referencia")
    args = ap.parse_args()
    if args.reanalisis:
        usar_reanalisis()
        os.makedirs(FICHAS, exist_ok=True)
    comun.MAX_SALIDA = args.max_salida
    if args.drive:
        os.makedirs(TEMP_DRIVE, exist_ok=True)
        cupo = Cupo(shutil.disk_usage(TEMP_DRIVE).free - 3e9)
    COPIAS_POR_DISCO = args.copias_por_disco
    Lote(args).correr()
