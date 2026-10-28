"""Consulta rápida del Directorio local (directorio_rows.json, bajado de la hoja el 26-oct-2026). uso: python -I explorar.py REGEX [campo]"""
import json, re, sys, collections
T = r"D:\OneScreen\Contenido\2026\10. Octubre\_inta_trabajo"
rows = json.load(open(T + r"\directorio_rows.json", encoding="utf-8"))
pat = sys.argv[1]
x = [r for r in rows if re.search(pat, r["Ruta en disco"] + " " + r["Información adicional"] + " " + r["Clip"], re.I)]
print(len(x), collections.Counter(r["Permisos"] for r in x).most_common(4), collections.Counter(r["Ubicación"] for r in x).most_common(3))
for r in x[:int(sys.argv[2]) if len(sys.argv) > 2 else 6]:
    print(r["ID"], r["Clip"], "q", r["Calidad (1-5)"], "dur", r["Duración (s)"], "|", r["Lugar"], "|", r["Ruta en disco"][-90:], "|", r["Información adicional"][:140])
