"""Storyboard INTA41.0001 aprobado (envío de Cris del 29-oct 09:59): fusiona sus elecciones en el SPEC maestro y escribe Proyecto\\montaje_aprobado.json.
S03 llegó «ninguna sirve» con el comentario «usa acá el plano 102344»: se aplica tal cual (no hace falta otra ronda).
Textos sobre plano: CTA en S17 y slogan con logo en S18 (los lee build_inta_sb.py desde "sobre_plano")."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import seleccion as S
from spec_inta41 import plano, SB

PROY = SB.parent / "Proyecto"
spec = json.load(open(SB / "SPEC_v1.json", encoding="utf-8"))
dec = json.load(open(SB / "decisiones" / "INTA41.0001.json", encoding="utf-8"))
t03 = next(t for t in spec["videos"][0]["tomas"] if t["id"] == "S03")
t03["opciones"][0] = plano("102344", t03["t1"] - t03["t0"], "salón moderno con la OneScreen al fondo (lo pidió Cris en el storyboard)")
dec["tomas"]["S03"] = dict(d="ok", op="A", elegido="plano 102344", c="usa acá el plano 102344")
json.dump(spec, open(SB / "SPEC_maestro.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
(SB / "aprobado").mkdir(exist_ok=True)
json.dump(dec, open(SB / "aprobado" / "INTA41.0001.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, str(Path(__file__).parent / "montaje_aprobado.py"), str(SB / "SPEC_maestro.json"), str(SB / "aprobado")], check=True)
m = json.load(open(PROY / "montaje_aprobado.json", encoding="utf-8"))
m["sobre_plano"] = [dict(toma="S17", txt="Conoce cómo funciona en **onescreenlatam.com/rental**"),
                    dict(toma="S18", txt="Transforma **el espacio**. Transforma **el futuro**.", logo=True)]
for t in m["tomas"]:     # S16 usa la idea «personas que se encienden» que ideas.py generó para S01: el texto va con la voz de S16
    if t["id"] == "S16":
        for e in t["eleccion"]["escena"]["elementos"]:
            if e["e"] == "titulo":
                e["lineas"] = [["Y eso, los padres", 300], ["lo notan", 700, "grad"]]
json.dump(m, open(PROY / "montaje_aprobado.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(m["tomas"]), "tomas;", [(t["id"], t["eleccion"].get("plano") or "motion") for t in m["tomas"]])
