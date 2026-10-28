"""Lista los planos elegidos de una pieza para revisarlos. uso: python -I ver_planos.py INTA15"""
import json, sys
for pz in sys.argv[1:]:
    d = json.load(open(r"D:\OneScreen\Contenido\2026\10. Octubre\%s\Proyecto\planos.json" % pz, encoding="utf-8"))
    print("==", pz)
    for p in d["planos"]:
        print(round(p["t0"], 1), p["texto"][:34].ljust(34), p["id"], p.get("lugar"), "|", p.get("permisos", "")[:14], "|", p.get("desc", "")[:64])
