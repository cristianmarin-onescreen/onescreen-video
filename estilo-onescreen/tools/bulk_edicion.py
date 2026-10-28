"""Corre analiza_prproj sobre todos los .prproj de una carpeta (sin render) y deja un CSV + JSON por proyecto."""
import os, sys, json, csv, glob, traceback
sys.path.insert(0, os.path.dirname(__file__))
from analiza_prproj import analizar
raiz = sys.argv[1]; salida = sys.argv[2]
os.makedirs(salida, exist_ok=True)
filas = []
for p in sorted(glob.glob(os.path.join(raiz, "**", "*.prproj"), recursive=True)):
    if "Auto-Save" in p:
        continue
    nombre = os.path.relpath(p, raiz)
    try:
        r = analizar(p, None)
    except Exception as e:
        filas.append(dict(proyecto=nombre, error=str(e)[:80])); continue
    json.dump(r, open(os.path.join(salida, nombre.replace("\\", "_").replace("/", "_")[:120] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
    pr = r["principal"]; ca = r.get("capa_ajuste") or {}
    h = r.get("habla") or {}
    filas.append(dict(proyecto=nombre, secuencia=r["secuencia"], dur_s=r["duracion"], clips=pr["clips"], dur_mediana=pr["dur_mediana"],
                      cortes_por_min=round(60 * pr["clips"] / max(r["duracion"], 1), 1), esc_n=r["escalas_fijas_stats"]["n"],
                      esc_min=r["escalas_fijas_stats"]["min"], esc_max=r["escalas_fijas_stats"]["max"], alternancia_pct=r["alternancia_pct"],
                      zooms_anim=len(r["zooms_animados"]), camara_flota=int(bool(ca.get("escala_min_max"))), aberracion=int(bool(ca.get("aberracion"))),
                      apoyo=len(r["apoyo"]), graficos=len(r["graficos"]), transiciones=r["transiciones_video"],
                      habla_bloques=h.get("bloques"), cortes_en_frase_pct=(h.get("cortes_en_frontera_principal") or {}).get("pct_a_2_cuadros"),
                      musica=";".join(sorted({n[:40] for a in r["audio"] for n in a["archivos"] if n.lower().endswith(".wav") and "esv2" not in n.lower() and not n.startswith("C")}))[:120]))
campos = sorted({k for f in filas for k in f}, key=lambda k: (k != "proyecto", k))
with open(os.path.join(salida, "resumen.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, campos); w.writeheader(); w.writerows(filas)
print(len(filas), "proyectos")
