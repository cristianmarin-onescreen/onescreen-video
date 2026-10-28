"""Resumen del lote: avance, costo real por video y por qué cuesta lo que cuesta. Escribe costos.csv."""
import collections
import csv
import json
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
planos = {p["id"]: p for p in json.load(open(os.path.join(BASE, "planos.json"), encoding="utf-8"))}
est = json.load(open(os.path.join(BASE, "estado.json"), encoding="utf-8"))
items = est["items"]
print("estados:", dict(collections.Counter(it.get("estado") for it in items.values())))
print(f"gastado USD {est['gastado']:.3f} | lotes en vuelo {len(est['lotes'])}")
con_costo = [(i, it) for i, it in items.items() if "costo" in it]
filas = []
for i, it in con_costo:
    dur = it.get("dur_s") or 1
    filas.append({"id": i, "clip": planos[i]["clip"], "color": planos[i]["color"], "dur_s": dur, "mb_copia": it.get("mb"),
                  "seg_copia": it.get("seg_copia"), "tok_entrada": it["tok_entrada"], "tok_salida": it["tok_salida"],
                  "tok_por_s": round(it["tok_entrada"] / dur, 1), "costo_usd": it["costo"], "estado": it["estado"]})
with open(os.path.join(BASE, "costos.csv"), "w", newline="", encoding="utf-8-sig") as f:
    if filas:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), delimiter=";")
        w.writeheader()
        w.writerows(filas)
if filas:
    dur = sum(f["dur_s"] for f in filas)
    costo = sum(f["costo_usd"] for f in filas)
    ent = sum(f["tok_entrada"] for f in filas)
    sal = sum(f["tok_salida"] for f in filas)
    print(f"{len(filas)} videos, {dur / 60:.1f} min | USD {costo:.4f} total, {costo / len(filas):.5f} por video, "
          f"{costo / (dur / 60):.5f} por minuto")
    print(f"entrada {ent:,} tok (USD {ent * 0.15e-6:.4f}) | salida {sal:,} tok (USD {sal * 1.25e-6:.4f}) | "
          f"salida media {sal // len(filas)} tok/video")
    for f in sorted(filas, key=lambda f: -f["costo_usd"])[:5]:
        print("  más caro:", f["id"], f["clip"], f["dur_s"], "s", f["costo_usd"])
errores = [(i, it.get("motivo")) for i, it in items.items() if it.get("estado") == "error"]
for i, m in errores[:20]:
    print("error", i, planos[i]["clip"], m)
