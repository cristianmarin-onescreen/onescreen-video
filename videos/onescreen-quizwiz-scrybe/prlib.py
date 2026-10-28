"""Utilidades para leer/clonar objetos de un .prproj de Premiere (XML gzip con ObjectID/ObjectUID/ObjectRef)."""
import gzip, copy, uuid
from lxml import etree

TICKS = 254016000000


def load(path):
    root = etree.fromstring(gzip.open(path).read(), parser=etree.XMLParser(huge_tree=True))
    byid = {}
    for e in root:
        k = e.get("ObjectID") or e.get("ObjectUID")
        if k:
            byid[k] = e
    return root, byid


def refs_of(e):
    out = []
    for c in e.iter():
        r = c.get("ObjectRef") or c.get("ObjectURef")
        if r:
            out.append(r)
    return out


def closure(byid, start_ids, stop_tags=(), stop_ids=()):
    """objetos alcanzables desde start_ids (sin cruzar stop_tags/stop_ids)"""
    seen, order, stack = set(), [], list(start_ids)
    while stack:
        i = stack.pop()
        if i in seen or i not in byid or i in stop_ids:
            continue
        e = byid[i]
        if e.tag in stop_tags:
            continue
        seen.add(i); order.append(i)
        stack.extend(refs_of(e))
    return order


def short(e, n=60):
    return etree.tostring(e).decode("utf-8", "replace")[:n]
