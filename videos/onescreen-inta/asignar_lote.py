"""Reparto de planos para un LOTE de videos (storyboard, paso 9b) sin repetir ni un plano en todo el lote.
Antes cada video elegia por su cuenta (seleccion.elegir): todos veian el mismo pool diminuto, las alternativas se repetian entre tomas seguidas y entre videos.
Ahora: seleccion.pool() da TODOS los candidatos por tramo y aqui se reparten con la vista del lote entero:
  - un plano se usa UNA sola vez en todo el lote (ni como opcion, ni en tomas seguidas, ni en el CTA);
  - se reparte por rondas (1.er plano de cada toma, luego el 2.o, luego el 3.o), empezando por la toma con menos candidatos;
  - la toma que no alcanza plano bueno se queda con menos (el storyboard la completa con motion y lo dice), no se rellena con repetidos.
uso: python -I asignar_lote.py LOTE.json SALIDA.json     LOTE.json = {"INTA20": [[1],[2],[3,4]], ...}  (indices base 1 de los tramos que forman cada toma)
     o desde Python: asignar({"INTA20": [[1],[2],[3,4]]}, n=3)  ->  {"INTA20": {"tomas": [[ficha,...],...], "cta": [ficha,...]}}"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import seleccion as S

BYID = {r["ID"]: r for r in S.rows}


def _toma(pl, grupo, n):
    a, b = pl[grupo[0] - 1]["t0"], pl[grupo[-1] - 1]["t1"]
    c = {}
    for gi in grupo:
        for x in pl[gi - 1]["cands"]:
            if x["id"] not in c or x["rank"] > c[x["id"]]["rank"]:
                c[x["id"]] = x
    need_ok = max(1.8, b - a + 0.2)
    lista = []
    for x in sorted(c.values(), key=lambda x: -x["rank"]):
        dur = S.num(BYID[x["id"]]["Duración (s)"])
        if dur >= need_ok + S.INI + 0.2:
            lista.append(x)
    return dict(grupo=grupo, a=a, b=b, n=n, cands=lista, got=[], need=max(2.2, b - a + 0.7))


def asignar(lote, n=3, n_cta=2, dur_cta=None):
    """lote = {pieza: [grupo de tramos por toma]}; dur_cta = {pieza: segundos del CTA} (por defecto 4)."""
    tomas, ctas = [], []
    for pieza, grupos in lote.items():
        cierre_t, pl = S.pool(pieza)
        for g in grupos:
            t = _toma(pl, g, n)
            t["pieza"] = pieza
            tomas.append(t)
        # CTA: texto sobre plano; candidatos de toda la pieza, con duración propia
        dc = (dur_cta or {}).get(pieza, 4.0)
        c = {}
        for e in pl:
            for x in e["cands"]:
                if x["id"] not in c or x["rank"] > c[x["id"]]["rank"]:
                    c[x["id"]] = x
        lista = [x for x in sorted(c.values(), key=lambda x: -x["rank"]) if S.num(BYID[x["id"]]["Duración (s)"]) >= dc + 0.2 + S.INI + 0.2]
        ctas.append(dict(pieza=pieza, grupo=None, a=0, b=dc, n=n_cta, cands=lista, got=[], need=dc + 0.2))
    usados = set()
    todas = tomas + ctas
    for ronda in range(max(n, n_cta)):
        pend = [t for t in todas if len(t["got"]) == ronda and ronda < t["n"]]
        # la toma con menos candidatos libres elige primero
        pend.sort(key=lambda t: sum(1 for x in t["cands"] if x["id"] not in usados))
        for t in pend:
            for x in t["cands"]:
                if x["id"] in usados:
                    continue
                usados.add(x["id"])
                t["got"].append(x)
                break
    out = {}
    for t in todas:
        fichas = []
        for x in t["got"]:
            f = S.ficha_plano(BYID[x["id"]], t["need"])
            f["score"], f["relax"], f["coincide"] = x["score"], x["relax"], x["coincide"]
            fichas.append(f)
        o = out.setdefault(t["pieza"], dict(tomas=[], cta=[]))
        (o["cta"] if t["grupo"] is None else o["tomas"]).append(fichas)
        t["fichas"] = fichas
    return out, todas


def informe(todas):
    print("pieza  toma(tramos)  pedidos  asignados  candidatos")
    faltan = 0
    for t in todas:
        k = len(t["got"])
        faltan += max(0, t["n"] - k)
        marca = "" if k >= t["n"] else "   <-- faltan, se cubre con motion"
        print(f'{t["pieza"]:7s}{"CTA" if t["grupo"] is None else str(t["grupo"]):14s}{t["n"]:5d}{k:9d}{len(t["cands"]):12d}{marca}')
    ids = [x["id"] for t in todas for x in t["got"]]
    print(f"planos repartidos: {len(ids)} | distintos: {len(set(ids))} | huecos: {faltan}")


if __name__ == "__main__":
    lote = json.load(open(sys.argv[1], encoding="utf-8"))
    res, todas = asignar(lote)
    informe(todas)
    if len(sys.argv) > 2:
        json.dump(res, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("escrito", sys.argv[2])
