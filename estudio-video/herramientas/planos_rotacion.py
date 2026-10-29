"""Rotación y veto de planos para los storyboards (Cris, 29-oct-2026).

«Siempre me trae los mismos 20 planos»: el ranking del selector es determinista y solo los usos APROBADOS (col. Y) penalizan,
así que lo propuesto y no elegido volvía a salir arriba. Dos reglas duras:
  1. ROTACIÓN: un plano propuesto (como cualquiera de las opciones A-C) en un storyboard no se vuelve a proponer
     hasta que pasen VENTANA (15) storyboards. Cada video de una página cuenta como un storyboard.
  2. VETO: la papelera del storyboard (o `vetar`) saca el plano para siempre (tomas falsas, gente riéndose, contenido inapropiado…).

Datos (en git, solo IDs de plano, sin datos de clientes):
  estudio-video/registro/planos_propuestos.json  = [{"sb": "storyboard_INTA20_v1.html#INTA20.0003", "fecha": "...", "planos": ["102385", ...]}, ...]
  estudio-video/registro/planos_vetados.json     = {"102385": {"fecha": "...", "motivo": "...", "origen": "INTA20.0003 S04"}}

Uso:  python estudio-video/herramientas/planos_rotacion.py estado            (cuántos bloqueados y vetados hay)
      python estudio-video/herramientas/planos_rotacion.py vetar ID [motivo]
      python estudio-video/herramientas/planos_rotacion.py desvetar ID
Desde Python: bloqueados(), vetados(), registrar(sb, planos), vetar(id, motivo, origen), desvetar(id)."""
import json
import sys
import time
from pathlib import Path

VENTANA = 15
REG = Path(__file__).resolve().parents[1] / "registro"
HIST = REG / "planos_propuestos.json"
VET = REG / "planos_vetados.json"


def _leer(p, defecto):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return defecto


def _escribir(p, datos):
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


CASOS = REG / "planos_casos.json"


def casos():
    """IDs de planos de casos de éxito: la regla de 2024 no les aplica (Cris, 29-oct)."""
    return {i for k, v in _leer(CASOS, {}).items() if not k.startswith("_") for i in v}


def vetados():
    return _leer(VET, {})


def vetar(plano, motivo="", origen=""):
    v = vetados()
    v[str(plano)] = {"fecha": time.strftime("%Y-%m-%d %H:%M"), "motivo": motivo, "origen": origen}
    _escribir(VET, v)


def desvetar(plano):
    v = vetados()
    if v.pop(str(plano), None) is not None:
        _escribir(VET, v)


def historial():
    return _leer(HIST, [])


def bloqueados(excluir=(), ventana=VENTANA):
    """{plano: storyboard} de los planos propuestos en los últimos `ventana` storyboards (sin contar los de `excluir`)."""
    h = [e for e in historial() if e["sb"] not in set(excluir)]
    out = {}
    for e in h[-ventana:]:
        for p in e["planos"]:
            out[str(p)] = e["sb"]
    return out


def registrar(sb, planos):
    """Anota (o reemplaza, si se regenera la misma página) los planos propuestos en el storyboard `sb`."""
    h = [e for e in historial() if e["sb"] != sb]
    h.append({"sb": sb, "fecha": time.strftime("%Y-%m-%d %H:%M"), "planos": sorted({str(p) for p in planos})})
    _escribir(HIST, h)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["vetar"] and len(a) >= 2:
        vetar(a[1], " ".join(a[2:]), "manual")
        print("vetado", a[1])
    elif a[:1] == ["desvetar"] and len(a) == 2:
        desvetar(a[1])
        print("desvetado", a[1])
    elif a[:1] == ["estado"]:
        h = historial()
        print(f"{len(h)} storyboards registrados; bloqueados por rotación (últimos {VENTANA}): {len(bloqueados())}; vetados: {len(vetados())}")
    else:
        raise SystemExit(__doc__)
