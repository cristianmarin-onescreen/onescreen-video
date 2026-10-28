"""Piezas compartidas del lote: instrucciones y esquema para Gemini, y paso de la ficha a celdas del Sheet."""
import ctypes
import datetime
import json
import os
import re
import subprocess
import time
import unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, "datos")  # cola, estado, fichas y copias: rutas con nombres de clientes, fuera de git
MODELO = "gemini-3.5-flash-lite"
API = "https://generativelanguage.googleapis.com"
# Batch API = mitad del precio estándar (ai.google.dev/gemini-api/docs/pricing, 3.5 Flash-Lite)
PRECIO_ENTRADA_BATCH = 0.15 / 1e6
PRECIO_SALIDA_BATCH = 1.25 / 1e6
# Resolución según duración, para no pasar el millón de tokens de contexto: (hasta s, resolución, tokens por segundo medidos/estimados)
RESOLUCIONES = [(2400, "MEDIA_RESOLUTION_HIGH", 290), (10 ** 9, "MEDIA_RESOLUTION_MEDIUM", 91)]  # LOW: "invalid argument"
MAX_SALIDA = 6000  # tokens de respuesta; un video de 49 min se pasó de este tope dos veces
SHEET_ID = "1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w"

PLANOS = ["Gran plano general", "Plano general", "Plano entero", "Plano americano", "Plano medio", "Plano medio corto",
          "Primer plano", "Primerísimo primer plano", "Plano detalle"]
MOVIMIENTOS = ["Fijo", "Paneo", "Tilt", "Travelling / dolly", "Zoom", "Cámara en mano", "Gimbal", "Dron", "Combinado"]
ANGULOS = ["Frontal", "Lateral", "Picado", "Contrapicado", "Cenital", "Sobre el hombro", "POV", "Holandés"]
PERSONAS = ["Ninguna", "Docente", "Estudiantes", "Niños", "Presentador / vocero", "Cliente / entrevistado", "Equipo OneScreen", "Público"]

INSTRUCCIONES = """Eres asistente de catalogación de video de OneScreen LATAM (pantallas interactivas y tecnología educativa y corporativa).
Mira y escucha el video COMPLETO. Puede estar grabado en S-Log3 (se ve lavado y con poco contraste): no lo describas como defecto.
La ficha alimenta un pipeline automático de edición: una IA elegirá planos de apoyo según lo que diga un guion, así que sé concreto.

- producto: hardware OneScreen visible. Escribe SOLO estos nombres, exactos, varios separados por " + ":
  "Pantalla interactiva OneScreen T7", "Pantalla interactiva OneScreen TL7", "Pantalla interactiva OneScreen Titan",
  "Pantalla interactiva OneScreen Core", "Pantalla interactiva OneScreen AIO", "Wandr", "Pantalla LED / videowall", "Tótem",
  "Proyector VPA", "Cámara MS10", "Cámara SnapCam", "Micrófono A10", "Soporte MC200", "Soporte con ruedas", "Computador OPS",
  "Marcador o lápiz", "Control remoto". Pantalla OneScreen sin modelo seguro: "Pantalla interactiva OneScreen (modelo no identificable)".
  Sin producto OneScreen: "Ninguno visible". No pongas un modelo si no lo ves con claridad (logo, forma inconfundible o lo dicen en el audio).
  Wandr: pantalla táctil de ~27" sobre UN poste delgado con base redonda pesada y ruedas, parte trasera blanca con perforaciones y logo
  "Wandr"; se lleva de un cuarto a otro (ver imágenes de referencia). Una pantalla grande en soporte de dos patas o colgada en la pared NO es Wandr.
  NO son productos OneScreen: impresoras, fotocopiadoras, escáneres, trituradoras de papel, parlantes, televisores, monitores de PC, proyectores
  de techo, celulares ni pantallas de otras marcas. En stock o video generado con IA solo pon un producto OneScreen si se ve su logo.
- software: lo que se ve en la pantalla. Usa estos nombres: Write, QuizWiz, Scrybe, Lessn, SuprNotes, Gurú, Central, Class, LearningHub,
  Attend, Share, Account, Google EDLA, Android / apps, Windows / OPS. Si en el audio se nombra un software o su nombre aparece escrito
  en pantalla (logo, título de ventana), úsalo; otro programa reconocible (Zoom, Teams, YouTube, Excel…) va con su nombre.
  Varios con " + ". Si no hay pantalla con software: "Ninguno".
- personas y cantidad_personas deben coincidir: "Ninguna" en las dos o en ninguna.
- valor_de_plano, movimiento y angulo: el dominante del clip (los cambios van en segmentos).
- acciones: hasta 10 verbos u objetos concretos de lo que pasa, separados por comas (escribe en la pantalla, señala, conecta celular, aplauden).
- calidad: 1 inservible a 5 excelente (foco, exposición, estabilidad, encuadre). motivo_descarte: lo que baja la calidad o "Ninguno".
- mejor_momento_s: segundo del clip con el momento más útil para un video.
- posicion_sujeto y apto_vertical: si se puede recortar a 9:16 o 4:5 sin perder rostro ni pantalla.
- permisos: "Menores en cámara" si se ven niños o adolescentes identificables; "Licencia stock" si es material de stock;
  "Requiere aprobación del cliente" si es un cliente o institución externa; si no, "Libre".
- segmentos: tramos con inicio_s y fin_s. Clips de 30 s o menos: 1 tramo. Hasta 2 min: máximo 3. Más largos: un tramo nuevo cada
  vez que cambie la acción, el encuadre o el tema, y ninguno de más de 60 s salvo un plano fijo donde no cambia nada (máximo 12).
  Los tramos cubren el archivo de principio a fin: el último termina en la duración total. En videos largos (entrevistas, charlas)
  usa los 12 tramos repartidos por tema a lo largo de todo el video.
  descripcion: máximo 20 palabras. texto_hablado: lo que se dice en el tramo, resumido en máximo 30 palabras ("" si no hay voz).
- TIEMPOS: mejor_momento_s, inicio_s y fin_s van en SEGUNDOS desde el inicio del archivo (1:15 son 75, no 115) y nunca pasan
  de la duración total.
- informacion_adicional: una frase de resumen y luego hasta 4 marcas de tiempo, con este formato:
  "<resumen>. [m:ss] <qué pasa> | [m:ss] <qué pasa>"
"""

ESQUEMA = {
    "type": "OBJECT",
    "properties": {
        "producto": {"type": "STRING"},
        "software": {"type": "STRING"},
        "categoria": {"type": "STRING", "enum": ["Caso de éxito", "Academy / tutorial", "Demostración de producto", "Comercial / pauta",
                                                 "Evento / feria", "Entrevista / testimonio", "Institucional / equipo", "Unboxing", "Otro"]},
        "valor_de_plano": {"type": "STRING", "enum": PLANOS},
        "movimiento": {"type": "STRING", "enum": MOVIMIENTOS},
        "angulo": {"type": "STRING", "enum": ANGULOS},
        "lugar": {"type": "STRING", "enum": ["Aula", "Auditorio", "Oficina", "Sala de reuniones", "Laboratorio", "Hospital / clínica",
                                             "Entidad de gobierno", "Feria / evento", "Estudio / set", "Tienda / retail", "Exterior", "Hogar", "Otro"]},
        "sector": {"type": "STRING", "enum": ["Educación básica", "Educación superior", "Formación técnica", "Corporativo", "Salud", "Gobierno",
                                              "Retail", "Interno OneScreen", "Otro"]},
        "personas": {"type": "ARRAY", "items": {"type": "STRING", "enum": PERSONAS}},
        "cantidad_personas": {"type": "STRING", "enum": ["Ninguna", "Una", "2 a 5", "6 o más"]},
        "acciones": {"type": "STRING"},
        "tipo_audio": {"type": "STRING", "enum": ["Entrevista / voz a cámara", "Voz en off", "Sonido directo útil", "Ambiente", "Música", "Sin audio útil"]},
        "idioma": {"type": "STRING", "enum": ["Español", "Inglés", "Portugués", "Árabe", "Varios", "Sin voz"]},
        "calidad": {"type": "INTEGER"},
        "motivo_descarte": {"type": "ARRAY", "items": {"type": "STRING", "enum": [
            "Ninguno", "Fuera de foco", "Subexpuesto", "Sobreexpuesto", "Movido / inestable", "Mira a cámara", "Logo de competencia",
            "Ruido / audio malo", "Otro"]}},
        "mejor_momento_s": {"type": "NUMBER"},
        "posicion_sujeto": {"type": "STRING", "enum": ["Izquierda", "Centro", "Derecha", "Varios", "Sin sujeto"]},
        "apto_vertical": {"type": "STRING", "enum": ["Sí", "Con ajuste", "No"]},
        "permisos": {"type": "ARRAY", "items": {"type": "STRING", "enum": [
            "Libre", "Menores en cámara", "Requiere aprobación del cliente", "Licencia stock", "No usar"]}},
        "informacion_adicional": {"type": "STRING"},
        "segmentos": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {
            "inicio_s": {"type": "NUMBER"}, "fin_s": {"type": "NUMBER"}, "descripcion": {"type": "STRING"},
            "valor_de_plano": {"type": "STRING", "enum": PLANOS}, "movimiento": {"type": "STRING", "enum": MOVIMIENTOS},
            "angulo": {"type": "STRING", "enum": ANGULOS}, "personas": {"type": "ARRAY", "items": {"type": "STRING", "enum": PERSONAS}},
            "acciones": {"type": "STRING"}, "texto_hablado": {"type": "STRING"}, "calidad": {"type": "INTEGER"}, "usable": {"type": "BOOLEAN"}},
            "required": ["inicio_s", "fin_s", "descripcion", "valor_de_plano", "movimiento", "angulo", "personas", "acciones",
                         "texto_hablado", "calidad", "usable"]}},
    },
    "required": ["producto", "software", "categoria", "valor_de_plano", "movimiento", "angulo", "lugar", "sector", "personas",
                 "cantidad_personas", "acciones", "tipo_audio", "idioma", "calidad", "motivo_descarte", "mejor_momento_s",
                 "posicion_sujeto", "apto_vertical", "permisos", "informacion_adicional", "segmentos"],
}


def resolucion(dur_s):
    return next((r, t) for hasta, r, t in RESOLUCIONES if (dur_s or 600) <= hasta)


def solicitud(plano, file_uri, dur_s, referencias=None):
    """referencias: [(texto, file_uri de imagen)] que van antes del video, para que Gemini compare productos."""
    texto = INSTRUCCIONES + (f"\nArchivo: {plano['clip']}\nCarpeta: {os.path.dirname(plano['rutas'][0]) if plano['rutas'] else ''}\n"
                             f"Duración total: {round(dur_s)} s\n")
    partes = []
    for nota, uri in referencias or []:
        partes += [{"text": "Imagen de referencia: " + nota}, {"file_data": {"mime_type": "image/jpeg", "file_uri": uri}}]
    if partes:
        partes.append({"text": "Fin de las referencias. Este es el video a catalogar:"})
    partes += [{"file_data": {"mime_type": "video/mp4", "file_uri": file_uri}}, {"text": texto}]
    return {"contents": [{"role": "user", "parts": partes}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json", "responseSchema": ESQUEMA,
                                 "mediaResolution": resolucion(dur_s)[0], "maxOutputTokens": MAX_SALIDA}}


def costo_estimado(dur_s):
    dur_s = dur_s or 600
    return dur_s * resolucion(dur_s)[1] * PRECIO_ENTRADA_BATCH + 2000 * PRECIO_SALIDA_BATCH + 2500 * PRECIO_ENTRADA_BATCH


def costo_real(uso):
    entrada = uso.get("promptTokenCount", 0)
    salida = uso.get("candidatesTokenCount", 0) + uso.get("thoughtsTokenCount", 0)
    return entrada * PRECIO_ENTRADA_BATCH + salida * PRECIO_SALIDA_BATCH


# ---------- Sheet ----------
def _txt(v):
    return {"userEnteredValue": {"stringValue": v}} if v not in (None, "") else {"userEnteredValue": {"stringValue": ""}}


def _num(v):
    return {"userEnteredValue": {"numberValue": float(v)}} if v is not None and v != "" else {"userEnteredValue": {"stringValue": ""}}


def unir(lista):
    return " + ".join(dict.fromkeys(x for x in (lista or []) if x))


# Variantes que escribió Gemini en el primer lote → nombre del catálogo (se comparan en minúsculas, sin tildes ni paréntesis)
_PRODUCTOS = [
    (r"wandr", "Wandr"), (r"t7 \(?o tl7", "Pantalla interactiva OneScreen (modelo no identificable)"),
    (r"\btl7\b", "Pantalla interactiva OneScreen TL7"), (r"\bt7\b", "Pantalla interactiva OneScreen T7"),
    (r"titan", "Pantalla interactiva OneScreen Titan"), (r"\bcore\b", "Pantalla interactiva OneScreen Core"),
    (r"\baio\b", "Pantalla interactiva OneScreen AIO"), (r"modelo no identificable|^pantalla interactiva( onescreen)?$",
                                                         "Pantalla interactiva OneScreen (modelo no identificable)"),
    (r"\bled\b|videowall", "Pantalla LED / videowall"), (r"totem", "Tótem"), (r"\bvpa\b|proyector onescreen", "Proyector VPA"),
    (r"ms10", "Cámara MS10"), (r"snapcam", "Cámara SnapCam"), (r"\ba10\b", "Micrófono A10"), (r"mc200", "Soporte MC200"),
    (r"soporte", "Soporte con ruedas"), (r"\bops\b", "Computador OPS"), (r"marcador|lapiz", "Marcador o lápiz"),
    (r"control remoto", "Control remoto"), (r"ninguno", "Ninguno visible"),
]
_SOFTWARE = {"guru": "Gurú", "onescreen guru": "Gurú", "android": "Android / apps", "windows": "Windows / OPS"}


def _llave(v):
    v = unicodedata.normalize("NFD", v.lower())
    return "".join(c for c in v if unicodedata.category(c) != "Mn").strip()


def normalizar_producto(texto):
    """'cámara (MS10) + Marcador' → 'Cámara MS10 + Marcador o lápiz'. Lo que no está en el catálogo se deja tal cual."""
    out = []
    for parte in re.split(r"\s*\+\s*", str(texto or "")):
        k = _llave(parte)
        if not k:
            continue
        if "ms10" in k and "snapcam" in k:  # "cámara (MS10, SnapCam)"
            out += ["Cámara MS10", "Cámara SnapCam"]
            continue
        out.append(next((n for p, n in _PRODUCTOS if re.search(p, k)), parte.strip()))
    if len(out) > 1 and "Ninguno visible" in out:
        out.remove("Ninguno visible")
    return unir(out)


_SOFTWARE_CATALOGO = ["Write", "QuizWiz", "Scrybe", "Lessn", "SuprNotes", "Central", "Class", "LearningHub", "Attend", "Share",
                      "Account", "Google EDLA", "Android / apps", "Windows / OPS", "Gurú", "Ninguno"]


def normalizar_software(texto):
    out = []
    for parte in re.split(r"\s*\+\s*", str(texto or "")):
        p = parte.strip()
        if not p:
            continue
        k = _llave(p).replace("onescreen ", "")
        out.append(_SOFTWARE.get(k) or next((n for n in _SOFTWARE_CATALOGO if _llave(n) == k), p))
    if len(out) > 1 and "Ninguno" in out:
        out.remove("Ninguno")
    return unir(out)


def normalizar_permisos(texto):
    partes = [p.strip() for p in str(texto or "").split("+") if p.strip()]
    if len(partes) > 1 and "Libre" in partes:
        partes.remove("Libre")  # "Libre" contradice cualquier otra restricción
    return unir(partes) or "Libre"


def segundos(t, dur):
    """Gemini a veces escribe 1:15 como 115: si un tiempo pasa de la duración y leído como m:ss cabe, se convierte; si no, se recorta."""
    t = float(t or 0)
    if dur and t > dur + 1:
        mmss = int(t) // 100 * 60 + int(t) % 100 + (t - int(t))
        t = mmss if mmss <= dur + 1 and int(t) % 100 < 60 else dur
    return round(max(0.0, t), 1)


def celdas_directorio(fila0, ficha, plano, info_actual, dur):
    """updateCells para la fila (0-based) del Directorio. No toca O (Estado), S, AB, AC ni AK."""
    info = ficha["informacion_adicional"].strip()
    producto = normalizar_producto(ficha["producto"])
    if plano["origen"] in ("Stock", "Generado con IA"):  # sin logo no se sabe el modelo, aunque Gemini lo adivine
        producto = unir(re.sub(r"^Pantalla interactiva OneScreen (T7|TL7|Titan|Core|AIO)$", "Pantalla interactiva OneScreen (modelo no identificable)",
                               p) for p in producto.split(" + "))
    if "UCUENCA" in (info_actual or "") and "UCUENCA" not in info:
        info = "UCUENCA · " + info
    bloques = [
        (3, [_txt(producto), _txt(normalizar_software(ficha["software"])), _txt(ficha["categoria"]), _txt(ficha["valor_de_plano"]),
             _txt(ficha["movimiento"]), _txt(ficha["angulo"]), _txt(ficha["lugar"]), _txt(ficha["sector"]), _txt(unir(ficha["personas"])),
             _txt(ficha["cantidad_personas"]), _txt(ficha["acciones"])]),
        (15, [_txt(info), _txt(ficha["tipo_audio"]), _txt(ficha["idioma"])]),
        (19, [_num(max(1, min(5, int(ficha["calidad"])))), _txt(unir(ficha["motivo_descarte"]) or "Ninguno"),
              _num(segundos(ficha["mejor_momento_s"], dur)), _txt(ficha["posicion_sujeto"]), _txt(ficha["apto_vertical"])]),
        (34, [_txt(plano["origen"]), _txt(normalizar_permisos(unir(ficha["permisos"])))]),
    ]
    return [{"updateCells": {"rows": [{"values": v}], "fields": "userEnteredValue",
                             "start": {"sheetId": 0, "rowIndex": fila0, "columnIndex": c}}} for c, v in bloques]


def filas_segmentos(plano, ficha, dur):
    out = []
    for s in sorted(ficha.get("segmentos", []), key=lambda s: segundos(s["inicio_s"], dur)):
        inicio, fin = segundos(s["inicio_s"], dur), segundos(s["fin_s"], dur)
        if fin <= inicio:
            continue
        out.append({"id": int(plano["id"]), "inicio": inicio, "fin": fin,
                    "descripcion": s["descripcion"], "valor": s["valor_de_plano"], "movimiento": s["movimiento"], "angulo": s["angulo"],
                    "personas": unir(s["personas"]), "acciones": s["acciones"], "texto": s["texto_hablado"],
                    "calidad": max(1, min(5, int(s["calidad"]))), "usable": "Sí" if s["usable"] else "No"})
    return out


def celdas_segmentos(fila0, filas):
    """Escribe A, C:D y F:N desde la fila (0-based) fila0; B y E son fórmulas y no se tocan."""
    if not filas:
        return []
    a = [{"values": [_num(f["id"])]} for f in filas]
    cd = [{"values": [_num(f["inicio"]), _num(f["fin"])]} for f in filas]
    fn = [{"values": [_txt(f["descripcion"]), _txt(f["valor"]), _txt(f["movimiento"]), _txt(f["angulo"]), _txt(f["personas"]),
                      _txt(f["acciones"]), _txt(f["texto"]), _num(f["calidad"]), _txt(f["usable"])]} for f in filas]
    return [{"updateCells": {"rows": r, "fields": "userEnteredValue", "start": {"sheetId": 9007, "rowIndex": fila0, "columnIndex": c}}}
            for c, r in ((0, a), (2, cd), (5, fn))]


def a_wsl(ruta):
    """Ruta de Windows → /mnt/c/..., con nombres largos (WSL no entiende CRISTI~1)."""
    buf = ctypes.create_unicode_buffer(1024)
    larga = buf.value if ctypes.windll.kernel32.GetLongPathNameW(os.path.abspath(ruta), buf, 1024) else os.path.abspath(ruta)
    return f"/mnt/{larga[0].lower()}{larga[2:].replace(os.sep, '/')}"


def sheets(modo, arg):
    """Llama al ayudante de WSL (composio proxy → API de Sheets). modo: 'valores'/'crudos' (rango A1), 'meta' o 'batch' (JSON)."""
    if modo == "batch":
        arg = a_wsl(arg)
    for intento in range(4):  # Sheets a veces responde con error de cuota o Composio se cae: se reintenta
        p = subprocess.run(["wsl.exe", "-d", "Ubuntu", "--", "bash", a_wsl(os.path.join(BASE, "run_sheets.sh")), modo, arg],
                           capture_output=True, timeout=1000,
                           stdin=subprocess.DEVNULL)
        salida = p.stdout.decode("utf-8", "replace")
        try:
            r = json.loads(salida)
        except json.JSONDecodeError:
            r = {"error": salida[:300] + p.stderr.decode("utf-8", "replace")[:300]}
        if "error" not in r and (modo != "batch" or "replies" in r) and (modo not in ("valores", "crudos") or "range" in r):
            return r
        time.sleep(20 * (intento + 1))
    raise RuntimeError(f"Sheets {modo} falló: {str(r)[:500]}")


def ahora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
