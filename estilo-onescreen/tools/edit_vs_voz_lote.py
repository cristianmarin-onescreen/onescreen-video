"""Corre edit_vs_voz carpeta por carpeta (lista en un .txt, una ruta por línea)."""
import sys, os, json, re, traceback
sys.path.insert(0, os.path.dirname(__file__))
from edit_vs_voz import analizar_carpeta
lista = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for k, c in enumerate(lista):
    nombre = f"{k:02d}_" + re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(c))[:36]
    try:
        r = analizar_carpeta(c)
        g = r.pop("_guion", [])
        json.dump(r, open(os.path.join(out, nombre + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        open(os.path.join(out, nombre + "_guion.txt"), "w", encoding="utf-8").write("\n".join(g))
        print("OK", nombre, r.get("prproj"), r.get("render"), r.get("duracion_seq"), flush=True)
    except Exception as e:
        print("ERROR", nombre, repr(e)[:120], flush=True)
print("DONE", flush=True)
