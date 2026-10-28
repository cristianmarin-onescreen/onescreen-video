"""Juez estricto de acento sobre las voces ya generadas: borra las que no pasan para que voz_inta las rehaga. uso: python -I juez.py [--borrar] INTA09 ..."""
import sys
from pathlib import Path
sys.argv, args = sys.argv[:1], sys.argv[1:]
borrar = "--borrar" in args
piezas = [a for a in args if a.startswith("INTA")]
sys.argv = ["voz_inta.py"] + ["__ninguna__"]
import importlib.util, os
spec = importlib.util.spec_from_file_location("vi", str(Path(__file__).parent / "voz_inta.py"))
src = Path(__file__).parent.joinpath("voz_inta.py").read_text(encoding="utf-8").split("for pz in PIEZAS:")[0]
ns = {"__name__": "vi", "__file__": str(Path(__file__).parent / "voz_inta.py")}
exec(compile(src, "voz_inta.py", "exec"), ns)
B = ns["BASE"]
for pz in piezas:
    h = B / pz / "Voz" / f"{pz}_hale.mp3"
    ok, r = ns["aprobada"](h)
    print(pz, "OK" if ok else "RECHAZADA", [(x.get("acento"), x.get("distincion_c_z"), x.get("entonacion_espana"), x.get("claridad")) for x in r], flush=True)
    if borrar and not ok:
        for f in (B / pz / "Voz").glob(f"{pz}_*"):
            if f.is_file():
                f.unlink()
