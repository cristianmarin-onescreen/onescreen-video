r"""Fusiona lo que Cris eligió en el storyboard (decisiones/<ID>.json) con el SPEC y escribe <Pieza>\Proyecto\montaje_aprobado.json:
una lista de tomas con t0, t1, voz y lo elegido (plano con ruta/in/out/log, o motion con plantilla/params). Es la entrada del ensamble (paso 10).
uso: python -I montaje_aprobado.py SPEC.json DECISIONES_DIR"""
import json, sys
from pathlib import Path
B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
spec = json.load(open(sys.argv[1], encoding="utf-8")); dec = Path(sys.argv[2])
for v in spec["videos"]:
    d = json.load(open(dec / f"{v['id']}.json", encoding="utf-8"))["tomas"]
    out, falta = [], []
    for t in v["tomas"]:
        r = d.get(t["id"])
        if not r or r.get("d") != "ok":
            falta.append(t["id"]); continue
        o = t["opciones"]["ABC".index(r["op"])]
        out.append(dict(id=t["id"], t0=t["t0"], t1=t["t1"], voz=t["voz"], eleccion=o, comentario=r.get("c", "")))
    pz = v["id"].split(".")[0]
    json.dump(dict(id=v["id"], tomas=out), open(B / pz / "Proyecto" / "montaje_aprobado.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pls = []
    for t in out:
        e = t["eleccion"]
        if e["tipo"] != "plano":
            continue
        dur = round(t["t1"] - t["t0"], 2)
        pls.append(dict(id=e["plano"], key=f"{e['plano']}_{int(round(e['plano_in'] * 100))}", ruta=e["ruta"], ss=e["plano_in"], need=round(dur + 0.6, 2), log=1 if e.get("log") else 0, fx=0.5, t0=t["t0"], t1=t["t1"], toma=t["id"]))
    json.dump(dict(planos=pls), open(B / pz / "Proyecto" / "planos_sb.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(v["id"], len(out), "tomas aprobadas; sin decisión/rechazadas:", falta,
          "| motion a construir:", sorted({(t["eleccion"]["plantilla"]) for t in out if t["eleccion"]["tipo"] == "motion"}))
