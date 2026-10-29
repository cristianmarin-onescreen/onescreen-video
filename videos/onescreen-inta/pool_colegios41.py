"""Pool rápido de planos de colegios para INTA41: San Mateo (caso de éxito, exento de la regla de 2024) + casos de colegios desde 2024.
Sin análisis de estabilidad (lento): el tramo arranca en el «Mejor momento» del Directorio y se valida MIRANDO la hoja de contacto.
uso: python pool_colegios41.py  -> Storyboard\\col_N.jpg + pool_colegios.json"""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import seleccion as S
import storyboard_inta41 as X
from PIL import Image, ImageDraw

SM = {str(i) for i in range(104603, 104661)}
CASO = re.compile(r"colegio caldas|biffi|la salle|gimnasio del norte|cerezos|eight academy", re.I)
pool = []
for r in S.rows:
    if not (r["ID"] in SM or (CASO.search(r["Ruta en disco"] + " " + r["Información adicional"]) and S.anio(r) >= 2024)):
        continue
    if r["ID"] in S.VETADOS or r["ID"] in S.BLOQUEADOS or r[S.KMOV] not in ("Fijo", "Travelling / dolly", "Gimbal", "Dron"):
        continue
    if S.num(r["Calidad (1-5)"]) < 3 or S.num(r["Duración (s)"]) < 3.4 or not S.RAW.match(r["Clip"].strip()):
        continue
    if re.search(r"entrevista|testimonio", r["Información adicional"] + r["Categoría"], re.I) or S.FALSA.search(S.norm(r["Información adicional"] + " " + r["Acciones / palabras clave"])):
        continue
    p = S.ruta_id(r)
    if not p:
        continue
    dur, mm = S.num(r["Duración (s)"]), S.num(r["Mejor momento (s)"])
    ss = round(max(S.INI, min(mm - 0.4, dur - 3.2)), 2)
    log = 1 if ("S-Log" in r["Perfil de color"] and not re.search(r"graded|_color|cuatro_looks", p, re.I)) else 0
    pool.append(dict(id=r["ID"], ruta=p, ss=ss, need=3.0, log=log, dur=dur, desc=r["Información adicional"][:110], permisos=r["Permisos"]))
print(len(pool), "planos;", sum(f["id"] in SM for f in pool), "de San Mateo")
json.dump({f["id"]: f for f in pool}, open(X.SB / "pool_colegios.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

W, H, PER = 240, 135, 12


def tira(f):
    return [X.fr(f["ruta"], t, f["log"]).resize((W, H)) for t in (f["ss"] + 0.2, f["ss"] + 1.5, f["ss"] + 2.8)]


with ThreadPoolExecutor(8) as ex:
    tiras = list(ex.map(tira, pool))
for p in range(0, len(pool), PER):
    im = Image.new("RGB", (2 * (3 * W + 20), 6 * (H + 22)), "white"); d = ImageDraw.Draw(im)
    for k, (f, ts) in enumerate(zip(pool[p:p + PER], tiras[p:p + PER])):
        x0, y0 = (k % 2) * (3 * W + 20), (k // 2) * (H + 22)
        for j, imj in enumerate(ts):
            im.paste(imj, (x0 + j * W, y0))
        d.text((x0 + 2, y0 + H + 3), f"{f['id']} | {f['desc'][:95]}", fill="red")
    out = X.SB / f"col_{p // PER + 1}.jpg"; im.save(out, quality=80); print(out)
