"""Arma datos/planos.json, la cola de lote.py, leyendo la pestaña Directorio del Sheet.

Prioridad de Cris: primero los planos con color, luego los más recientes (Fecha de grabación desc.), y a igual fecha por ID.
Por defecto solo entran los que aún no tienen Producto (los ya analizados se saltan). Con --ids (JSON con una lista o un dict de IDs)
se arma la cola de un re-análisis en datos/planos_reanalisis.json. Uso: python armar_cola.py [--todos] [--ids archivo.json]
"""
import argparse
import json
import os

import comun

# columna (letra) → campo; los números se leen sin formato para que es_CO no meta separadores de miles
COLUMNAS = {"A": "id", "B": "clip", "D": "producto", "P": "info", "Z": "color", "AD": "fecha", "AE": "dur_s", "AI": "origen",
            "AM": "rutas", "AN": "links"}
SIN_FORMATO = {"A", "AE"}


def leer():
    columnas = {}
    for letra, campo in COLUMNAS.items():
        modo = "crudos" if letra in SIN_FORMATO else "valores"
        valores = (comun.sheets(modo, f"'Directorio'!{letra}1:{letra}").get("values") or [[]])[0]
        columnas[campo] = valores[1:]  # sin encabezado
    filas = len(columnas["id"])
    return [{campo: (vals[n] if n < len(vals) else "") for campo, vals in columnas.items()} for n in range(filas)]


def plano(f):
    lineas = lambda v: [x.strip() for x in str(v).splitlines() if x.strip()]
    return {"id": str(f["id"]), "clip": f["clip"], "rutas": lineas(f["rutas"]), "links": lineas(f["links"]), "color": f["color"] == "Sí",
            "fecha": f["fecha"], "dur_s": int(f["dur_s"]) if f["dur_s"] != "" else None, "origen": f["origen"], "info": f["info"]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--todos", action="store_true", help="incluye también los que ya tienen Producto")
    ap.add_argument("--ids", help="JSON con los IDs a re-analizar (ya tengan Producto o no)")
    args = ap.parse_args()
    ids = {str(i) for i in json.load(open(args.ids, encoding="utf-8"))} if args.ids else None
    filas = [f for f in leer() if f["id"] != "" and (str(f["id"]) in ids if ids else (args.todos or not f["producto"]))]
    planos = [plano(f) for f in filas]
    planos.sort(key=lambda p: p["id"])
    planos.sort(key=lambda p: p["fecha"] or "", reverse=True)
    planos.sort(key=lambda p: not p["color"])
    os.makedirs(comun.DATOS, exist_ok=True)
    salida = "planos_reanalisis.json" if ids else "planos.json"
    json.dump(planos, open(os.path.join(comun.DATOS, salida), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    en_disco = sum(1 for p in planos if p["rutas"])
    print(f"{len(planos)} planos en la cola ({sum(p['color'] for p in planos)} con color, {en_disco} con archivo en disco, "
          f"{len(planos) - en_disco} solo en Drive)")
