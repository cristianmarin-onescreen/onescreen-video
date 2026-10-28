"""Validación estructural de un .prproj generado (no sustituye abrirlo en Premiere).
Revisa: gzip/XML que re-abre con prlib.load, ObjectID/ObjectUID únicos, ObjectRef/ObjectURef resueltos, huérfanos, pistas sin solapes y
cada clip de la secuencia con su cadena de componentes, SubClip y MasterClip.   Uso: python validate_prproj.py archivo.prproj"""
import collections, gzip, sys
from pathlib import Path
from lxml import etree
sys.path.insert(0, str(Path(__file__).parent))
from prlib import load, closure

p = sys.argv[1]
root, by = load(p)
errs, warns = [], []
ids, uids = collections.Counter(), collections.Counter()
projnested = set()
for pe in root:
    if pe.tag == "Project" and pe.get("ObjectID"):
        for x in pe.iter():
            if x is not pe and x.get("ObjectID"):
                projnested.add(x.get("ObjectID"))      # ids propios del Project (ámbito aparte, vienen así en la plantilla)
for e in root.iter():
    if e.get("ObjectID") and not (e.get("ObjectID") in projnested and e.tag != "Project" and any(a.tag == "Project" for a in e.iterancestors())):
        ids[e.get("ObjectID")] += 1
    if e.get("ObjectUID"):
        uids[e.get("ObjectUID")] += 1
for x in projnested:
    ids.setdefault(x, 1)
for k, n in ids.items():
    if n > 1:
        errs.append(f"ObjectID duplicado {k} x{n}")
for k, n in uids.items():
    if n > 1:
        errs.append(f"ObjectUID duplicado {k} x{n}")
for e in root.iter():
    r = e.get("ObjectRef")
    if r is not None and r not in ids:
        errs.append(f"ObjectRef sin resolver {r} en <{e.tag}> (padre {e.getparent().tag if e.getparent() is not None else ''})")
    r = e.get("ObjectURef")
    if r is not None and r not in uids:
        errs.append(f"ObjectURef sin resolver {r} en <{e.tag}>")
# huérfanos: todo objeto de primer nivel debe ser alcanzable desde el proyecto
reach = set(closure(by, ["1"]))
top = [e for e in root if e.get("ObjectID") or e.get("ObjectUID")]
for e in top:
    k = e.get("ObjectID") or e.get("ObjectUID")
    if k not in reach:
        warns.append(f"objeto no alcanzable desde Project: <{e.tag}> {k}")
# pistas
tr = {}
for e in root:
    if e.tag in ("VideoClipTrack", "AudioClipTrack"):
        items = []
        for ti in e.iter("TrackItem"):
            if ti.get("ObjectRef"):
                it = by[ti.get("ObjectRef")]
                s = int(it.findtext(".//TrackItem/Start") or 0); en = int(it.findtext(".//TrackItem/End"))
                items.append((s, en, ti.get("ObjectRef"), it))
        items.sort()
        for a, b in zip(items, items[1:]):
            if a[1] > b[0]:
                errs.append(f"solape en pista {e.get('ObjectUID')[:8]}: {a[2]} y {b[2]}")
        for s, en, oid, it in items:
            sc = by.get(it.find(".//SubClip").get("ObjectRef"))
            if sc is None:
                errs.append(f"item {oid} sin SubClip"); continue
            mc = sc.find("MasterClip").get("ObjectURef")
            if mc not in by:
                errs.append(f"item {oid}: MasterClip {mc} inexistente")
            ch = it.find(".//ComponentOwner/Components").get("ObjectRef")
            if ch not in by:
                errs.append(f"item {oid}: cadena {ch} inexistente")
        tr[e.get("ObjectUID")[:8]] = [(round(s / 10594584000), round(en / 10594584000), by[oid].tag) for s, en, oid, _ in items]
# componentes de cada cadena: ids únicos dentro de la cadena
for e in root:
    if e.tag == "VideoComponentChain":
        cids = []
        for c in e.iter("Component"):
            r = c.get("ObjectRef")
            if r in by:
                cids.append(by[r].findtext(".//ID"))
        if len(cids) != len(set(cids)):
            errs.append(f"IDs de componente repetidos en cadena {e.get('ObjectID')}: {cids}")
        dm, do = e.findtext("DefaultMotionComponentID"), e.findtext("DefaultOpacityComponentID")
        if dm and dm in cids:
            errs.append(f"cadena {e.get('ObjectID')}: ID de Movimiento por defecto {dm} choca con un componente")
        if do and do in cids:
            errs.append(f"cadena {e.get('ObjectID')}: ID de Opacidad por defecto {do} choca con un componente")
data = gzip.open(p).read()
print(Path(p).name, len(data) // 1024, "KB xml |", len(ids), "objetos con id |", len(uids), "con uid")
for k, v in tr.items():
    print("pista", k, len(v), "items", v[:3], "…", v[-1:] if v else "")
print("ERRORES:", len(errs)); [print("  ", x) for x in errs[:30]]
print("AVISOS:", len(warns)); [print("  ", x) for x in warns[:30]]
sys.exit(1 if errs else 0)
