r"""Revisión OBLIGATORIA del reencuadre de cada plano en 9:16, 4:5 y 1:1 (Cris, 29-oct: «cuando reencuadra no está mirando qué
reencuadra; debe revisar»; y «no uses Gemini»). Todo local: ffmpeg + OpenCV para dibujar, sin APIs.

`enc` (en montaje_aprobado.json, por toma) = posición horizontal del sujeto en el plano 16:9, de 0 a 1. Antes se ponía a ciegas.

  1. python estudio-video/herramientas/revisar_encuadre.py PIEZA [9 45 1]
     Saca 3 fotogramas por toma (15 %, 50 % y 85 % del tramo) y hace una hoja de contacto por formato:
     <Pieza>\Proyecto\encuadre\encuadre_<fmt>.jpg = el plano 16:9 con una regla de 0 a 1 abajo, la ventana del recorte
     (verde = nominal; amarilla punteada = peor caso con el zoom del plano, el empuje x1,075 y el Camera Wiggle x1,052)
     y al lado cómo queda el recorte. Si ya hay notas, pinta el FOCO marcado (morado) y lo mide.
  2. Claude ABRE Y MIRA cada hoja (Read del .jpg) y escribe <Pieza>\Proyecto\encuadre\notas.json, una entrada por toma con plano:
        {"S04": {"foco": [0.33, 0.69], "ve": "cara del docente y su mano tocando los íconos"}, ...}
     foco = de dónde a dónde (fracción del ancho 16:9, leída en la regla) va lo que el plano tiene que mostrar: el rostro, la mano que
     toca o escribe, la pantalla en uso, el QR. Si no cabe todo, se decide qué es lo esencial y se dice en «ve». Corrige `enc` donde falle.
  3. python estudio-video/herramientas/revisar_encuadre.py PIEZA [9 45 1] --aprobar
     Se MIDE: ERROR si el foco de una toma no cabe en la ventana del peor caso de algún formato, si una toma con plano no tiene nota
     (foco + ve), o si `enc` contradice la posición del sujeto del Directorio (Izquierda/Derecha) sin explicarlo en «ve».
     Sin errores escribe encuadre\revisado.json con la huella de los `enc` y las notas.
build_inta_sb.py se niega a armar 9:16, 4:5 o 1:1 si revisado.json falta o no corresponde a los `enc` actuales (comprobar())."""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import cv2
import numpy as np

CONT = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
DIRECTORIO = CONT / "_inta_trabajo" / "directorio_rows.json"
VIS = {"9": 0.3164, "45": 0.45, "1": 0.5625}          # ancho visible del plano 16:9 en cada formato (object-fit: cover), igual que build_inta_sb.enc_pos
ZOOM = {"9": 1.15, "45": 1.18, "1": 1.18}               # zoom de los planos en posición impar (build_inta_sb.ZOOM)
EXTRA = 1.075 * 1.052                                   # empuje del plano y escala máxima del Camera Wiggle
NOMBRE = {"9": "9x16", "45": "4x5", "1": "1x1"}


def montaje(pz):
    return json.loads((CONT / pz / "Proyecto" / "montaje_aprobado.json").read_text(encoding="utf-8"))


def tomas_plano(pz):
    return [t for t in montaje(pz)["tomas"] if t["eleccion"]["tipo"] == "plano"]


def huella(pz, fmts, notas=None):
    encs = [(t["id"], t["eleccion"].get("plano"), t["eleccion"].get("enc")) for t in tomas_plano(pz)]
    return hashlib.sha1(json.dumps([encs, sorted(fmts), notas], sort_keys=True).encode()).hexdigest()[:16]


def comprobar(pz, fmt):
    """Para build_inta_sb.py: None si el reencuadre de este formato está revisado y vigente; si no, el motivo."""
    p = CONT / pz / "Proyecto" / "encuadre" / "revisado.json"
    if not p.exists():
        return f"el reencuadre de {pz} no está revisado: revisar_encuadre.py {pz} {fmt}, mirar las hojas, escribir notas.json y --aprobar"
    r = json.loads(p.read_text(encoding="utf-8"))
    if fmt not in r["formatos"]:
        return f"el reencuadre {NOMBRE.get(fmt, fmt)} de {pz} no está revisado"
    if r["huella"] != huella(pz, r["formatos"], r.get("notas")):
        return f"los enc de {pz} cambiaron después de la revisión del {r['fecha']}: vuelve a revisar"
    return None


def medio(pz, e):
    key = f"{e['plano']}_{int(round(e['plano_in'] * 100))}"
    for sub in ("v_16c", "v_16"):
        f = CONT / pz / "Proyecto" / sub / "media" / f"{key}.mp4"
        if f.exists():
            return f, 0.0
    return Path(e["ruta"]), e["plano_in"]          # sin corte: el original (si es S-Log3 se ve plano, pero sirve para encuadrar)


def fotograma(ruta, t):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", str(ruta), "-frames:v", "1", "-vf", "scale=960:-2",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    return cv2.imdecode(np.frombuffer(r.stdout, np.uint8), cv2.IMREAD_COLOR) if r.stdout else None


def ventana(enc, fmt, escala):
    """(x0, x1) en fracción del ancho del plano 16:9 que se ve en el formato, con la escala total dada."""
    w = VIS[fmt]
    c = 0.5 if enc is None else enc
    p = min(1.0, max(0.0, (c - w / 2) / (1 - w)))
    centro = p * (1 - w) + w / 2
    ws = w / escala
    return centro - ws / 2, centro + ws / 2


def revisar(pz, fmts, aprobar=False):
    pos = {}
    if DIRECTORIO.exists():
        for r in json.loads(DIRECTORIO.read_text(encoding="utf-8")):
            pos[r["ID"]] = next((r[k] for k in r if k.startswith("Posici")), "")
    out = CONT / pz / "Proyecto" / "encuadre"
    out.mkdir(parents=True, exist_ok=True)
    pn = out / "notas.json"
    notas = json.loads(pn.read_text(encoding="utf-8")) if pn.exists() else {}
    errores, avisos, filas = [], [], {f: [] for f in fmts}
    for k, t in enumerate(tomas_plano(pz)):
        e = t["eleccion"]
        ruta, base = medio(pz, e)
        # el plano se MUEVE dentro de la toma y puede seguir en pantalla más allá de t1 (el CTA lo alarga): se mira todo lo que se ve
        dur = duracion(ruta) - base if base == 0 else t["t1"] - t["t0"]
        imgs = [i for i in (fotograma(ruta, base + dur * q) for q in (0.08, 0.5, 0.92)) if i is not None]
        if not imgs:
            errores.append(f"{t['id']} plano {e['plano']}: no se pudo leer {ruta}")
            continue
        enc = e.get("enc") if isinstance(e.get("enc"), (int, float)) else None
        n = notas.get(t["id"]) or {}
        foco = n.get("foco")
        if not (isinstance(foco, list) and len(foco) == 2 and 0 <= foco[0] < foco[1] <= 1 and n.get("ve")):
            (errores if aprobar else avisos).append(f"{t['id']} plano {e['plano']}: falta la nota (foco [x0, x1] y «ve») en notas.json")
            foco = None
        p = pos.get(str(e["plano"]), "")
        c = 0.5 if enc is None else enc
        if ((p == "Izquierda" and c > 0.55) or (p == "Derecha" and c < 0.45)) and "directorio" not in n.get("ve", "").lower():
            (errores if aprobar else avisos).append(f"{t['id']} plano {e['plano']}: el Directorio dice sujeto a la {p.lower()} y enc = {e.get('enc')} "
                                                    "(corrige enc o explica en «ve» por qué el Directorio no aplica)")
        escala = 1.03 if k % 2 == 0 else None
        for f in fmts:
            esc = escala or ZOOM[f]
            nom, peor = ventana(enc, f, esc), ventana(enc, f, esc * EXTRA)
            mal = bool(foco) and (foco[0] < peor[0] - 0.005 or foco[1] > peor[1] + 0.005)
            if mal:
                errores.append(f"{t['id']} plano {e['plano']} {NOMBRE[f]}: el foco [{foco[0]:.2f}, {foco[1]:.2f}] ({n.get('ve', '')}) no cabe en el "
                               f"recorte [{peor[0]:.2f}, {peor[1]:.2f}] con enc={e.get('enc')}")
            filas[f].append((t, e, imgs, nom, peor, foco, mal))
    for f in fmts:
        hoja(out / f"encuadre_{NOMBRE[f]}.jpg", pz, f, filas[f])
    for x in errores:
        print("ERROR:", x)
    for x in avisos:
        print("AVISO:", x)
    for f in fmts:
        print("hoja:", out / f"encuadre_{NOMBRE[f]}.jpg")
    if aprobar:
        if errores:
            raise SystemExit(f"No se aprueba: {len(errores)} error(es).")
        (out / "revisado.json").write_text(json.dumps({"pieza": pz, "formatos": fmts, "huella": huella(pz, fmts, notas), "notas": notas,
                                                       "fecha": time.strftime("%Y-%m-%d %H:%M")}, ensure_ascii=False, indent=1), encoding="utf-8")
        print("APROBADO:", out / "revisado.json")
    elif errores:
        sys.exit(1)


def duracion(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ruta)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def hoja(salida, pz, f, filas):
    """Por toma, los 3 momentos (inicio, mitad, final de lo que se ve) del plano 16:9 con regla 0-1, la ventana del recorte, el peor caso
    y el foco marcado; a la derecha, los 3 recortes tal como saldrán. Así se ve si el sujeto se mueve y se sale."""
    TW, TH = 480, 270
    rw = int(TH / {"9": 16 / 9, "45": 5 / 4, "1": 1.0}[f])
    sep = lambda w: np.full((TH, w, 3), 30, np.uint8)
    bloques = []
    for t, e, imgs, (n0, n1), (p0, p1), foco, mal in filas:
        pl, rc = [], []
        for img in imgs:
            a = cv2.resize(img, (TW, TH))
            for i in range(11):                                     # regla 0..1 para leer el foco
                x = int(i / 10 * (TW - 1))
                cv2.line(a, (x, TH - 12), (x, TH - 1), (255, 255, 255), 2)
                cv2.putText(a, f"{i / 10:.1f}", (min(x + 2, TW - 26), TH - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
            if foco:
                cv2.rectangle(a, (int(foco[0] * TW), 34), (int(foco[1] * TW), TH - 26), (60, 60, 255) if mal else (255, 0, 200), 2)
            cv2.rectangle(a, (int(n0 * TW), 0), (int(n1 * TW), TH - 1), (80, 220, 80), 3)
            for yy in range(0, TH, 14):
                for xx in (int(p0 * TW), int(p1 * TW)):
                    cv2.line(a, (xx, yy), (xx, min(TH - 1, yy + 7)), (0, 220, 255), 2)
            W = img.shape[1]
            rec = img[:, max(0, int(n0 * W)):min(W, int(n1 * W))]
            rec = cv2.resize(rec, (rw, int(rec.shape[0] * rw / max(1, rec.shape[1]))))
            rec = rec[max(0, (rec.shape[0] - TH) // 2):][:TH]
            rc.append(cv2.copyMakeBorder(rec, 0, TH - rec.shape[0], 0, 0, cv2.BORDER_CONSTANT))
            pl += [a, sep(6)]
        while len(rc) < 3:
            rc.append(sep(rw))
            pl += [sep(TW), sep(6)]
        fila = np.hstack(pl + [sep(14)] + [x for r in rc for x in (r, sep(4))])
        txt = f"{t['id']}  plano {e['plano']}  enc={e.get('enc')}  {'FOCO FUERA' if mal else ('foco ok' if foco else 'sin nota')}"
        cv2.putText(fila, txt, (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
        cv2.putText(fila, txt, (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 255) if mal else (255, 255, 255), 2)
        bloques += [fila, np.full((10, fila.shape[1], 3), 30, np.uint8)]
    if bloques:
        cab = np.full((50, bloques[0].shape[1], 3), 30, np.uint8)
        cv2.putText(cab, f"{pz} {NOMBRE[f]}: verde = recorte; amarilla punteada = peor caso (zoom + wiggle); morado = foco marcado; rojo = foco fuera",
                    (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
        cv2.imwrite(str(salida), np.vstack([cab] + bloques), [cv2.IMWRITE_JPEG_QUALITY, 82])


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--aprobar"]
    if not a:
        raise SystemExit(__doc__)
    revisar(a[0], a[1:] or ["9", "45", "1"], "--aprobar" in sys.argv)
