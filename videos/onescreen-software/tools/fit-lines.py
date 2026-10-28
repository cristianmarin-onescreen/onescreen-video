# -*- coding: utf-8 -*-
"""Mide cada línea con las fuentes REALES y calcula el font-size que cabe.

Por qué existe: el escalón tipográfico se elige por jerarquía, no por longitud, así que
una palabra larga en versalitas puede desbordar el cuadro. Pasó con "ACTUALIZACIONES,"
en la pieza de Rental: 16 caracteres a mega miden 3878 px en un área útil de 3302 y la
última letra se salía del lienzo. El `check` de HyperFrames no lo detectó porque muestrea
nueve instantes y ese cuadro no cayó en ninguno.

Una línea envuelve en los espacios, así que la restricción real es que la PALABRA MÁS
LARGA quepa. Si no cabe, se reduce el cuerpo de toda la línea hasta que quepa.

Salida: transcript/fit.json  →  { "f09": { "1": 8.63 } }  (índice de línea → cqw)
"""
import json, os, sys
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANVAS = 3840.0
CONTENT = 0.86 * CANVAS      # max-width de .inner
SAFETY = 0.985               # margen para redondeos del motor de texto

RUBIK = os.path.join(ROOT, "assets", "fonts", "Rubik-Variable.ttf")
NEVIS = os.path.join(ROOT, "assets", "fonts", "Nevis.ttf")

# cqw, peso, tracking en em — copiados del CSS del generador.
SCALE = {
    "sub":      (3.4, 500, -0.010),
    "phrase":   (5.2, 500, -0.018),
    "display":  (6.4, 600, -0.024),
    "mega":     (8.2, 800, -0.028),
    "colossal": (9.6, 800, -0.030),
}
CAPS_TRACK = {"sub": 0.16, "phrase": 0.02, "display": 0.0, "mega": -0.012, "colossal": -0.018}
CAPS_WEIGHT = {"sub": 600}
BRAND_CQW = {"sub": 3.81, "phrase": 5.82, "display": 7.17, "mega": 9.18, "colossal": 10.75}
BRAND_TRACK = -0.050

# --- Modo subtitulo (tercio inferior) ---
# Rango casi plano y medida mas corta: el bloque va sobre pantallazos del software.
LOWER_SCALE = {
    "sub":      (2.9, 500, -0.004),
    "phrase":   (3.3, 600, -0.006),
    "display":  (3.3, 600, -0.006),
    "mega":     (3.9, 700, -0.010),
    "colossal": (3.9, 800, -0.010),
}
LOWER_BRAND_CQW = {"sub": 3.25, "phrase": 3.70, "display": 3.70, "mega": 4.37, "colossal": 4.37}
LOWER_CONTENT = 0.80 * CANVAS
# El lockup de producto comparte fila con el icono (5.6cqw) y su separacion (1.5cqw),
# asi que al nombre le queda menos medida que a un subtitulo normal.
LOCK_CQW = 4.6
LOCK_CONTENT = (0.80 - 0.056 - 0.015) * CANVAS

MEASURE_PX = 200  # se mide a este cuerpo y se escala


def rubik(weight):
    f = ImageFont.truetype(RUBIK, MEASURE_PX)
    f.set_variation_by_axes([weight])
    return f


def width_em(text, font, tracking):
    """Ancho en em: avance de los glifos más el tracking de cada carácter."""
    return font.getlength(text) / MEASURE_PX + tracking * len(text)


def main():
    beats = json.load(open(os.path.join(ROOT, "transcript", "beats.json"), encoding="utf-8"))
    nevis = ImageFont.truetype(NEVIS, MEASURE_PX)
    cache = {}
    fits, report = {}, []

    for frame in beats["frames"]:
        for li, line in enumerate(frame["lines"]):
            scale = line["scale"]
            caps = line.get("caps", False)
            regular = line.get("regular", False)
            all_brand = all(w.get("brand") for w in line["words"])
            lower = frame.get("lower", False)
            # La ultima linea de un cuadro con icono en modo subtitulo es el lockup,
            # que va en su propia fila junto al icono.
            is_lock = lower and frame.get("icon") and li == len(frame["lines"]) - 1
            # En modo subtitulo las versalitas solo sobreviven en el escalon de remate.
            caps_render = caps and (not lower or scale == "colossal")

            if all_brand:
                cqw = (LOWER_BRAND_CQW if lower else BRAND_CQW)[scale]
                track = BRAND_TRACK
                font = nevis
            else:
                cqw, weight, track = (LOWER_SCALE if lower else SCALE)[scale]
                if caps:
                    if lower:
                        track, weight = (0.010, 800) if scale == "colossal" else (-0.008, 700)
                    else:
                        track = CAPS_TRACK[scale]
                        weight = CAPS_WEIGHT.get(scale, weight)
                if regular:
                    weight, track = 400, (-0.004 if lower else -0.018)
                if weight not in cache:
                    cache[weight] = rubik(weight)
                font = cache[weight]
            if is_lock and not all_brand:
                cqw = LOCK_CQW

            px = cqw / 100.0 * CANVAS
            widest, widest_word = 0.0, ""
            for w in line["words"]:
                t = w["text"].upper() if (caps_render and not w.get("brand")) else w["text"]
                # una palabra de marca dentro de una línea normal va 12% mayor y en Nevis
                if w.get("brand") and not all_brand:
                    wpx = width_em(t, nevis, BRAND_TRACK) * px * 1.12
                else:
                    wpx = width_em(t, font, track) * px
                if wpx > widest:
                    widest, widest_word = wpx, t

            area = LOCK_CONTENT if is_lock else (LOWER_CONTENT if lower else CONTENT)
            limit = area * SAFETY
            if widest > limit:
                new_cqw = round(cqw * limit / widest, 2)
                fits.setdefault(frame["id"], {})[str(li)] = new_cqw
                report.append((frame["id"], li, widest_word, round(widest), cqw, new_cqw))

    json.dump(fits, open(os.path.join(ROOT, "transcript", "fit.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    if report:
        print(f"{len(report)} linea(s) no caben; se reduce el cuerpo:")
        for fid, li, word, w, old, new in report:
            print(f"  {fid} linea {li}: '{word}' medía {w}px  ->  {old}cqw pasa a {new}cqw")
    else:
        print("todas las lineas caben; fit.json vacio")


main()
