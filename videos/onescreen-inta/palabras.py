"""Imprime las palabras de Scribe de cada pieza (para escribir anclas en specs.py). uso: python -I palabras.py INTA09 ..."""
import json, sys
from pathlib import Path
B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
for pz in sys.argv[1:]:
    w = [x for x in json.load(open(B / pz / "Voz" / f"{pz}_scribe.json", encoding="utf-8"))["words"] if x.get("type") == "word"]
    print(pz, round(w[-1]["end"], 1), "s:", " ".join(f"{x['text']}@{x['start']:.1f}" for x in w))
