"""Sincroniza las notas de video entre la memoria de Claude Code y estudio-video/memoria/ (gana la más nueva) y regenera INDEX.md.
Uso: python estudio-video/herramientas/sync_memoria.py [--solo-ver]
Copia los archivos que ya existen en estudio-video/memoria/ y los nuevos de la memoria cuyo nombre empiece por un prefijo de video (PREFIJOS)."""
import re
import shutil
import sys
from pathlib import Path

HUB = Path(__file__).resolve().parents[1] / "memoria"
MEM = Path.home() / ".claude" / "projects" / "C--Users-Cristian-Marin-Desktop-Claudio" / "memory"
PREFIJOS = ("video_", "videos_", "estilo_", "mezcla_", "musica_", "paleta_", "zonas_", "color_desde", "directorio_video_onescreen",
            "pipeline_color", "hyperframes_", "marca_tipografia", "marca_onescreen", "pronunciacion_", "proceso_video",
            "short_", "edicion_", "voz_", "feedback_pasar_link")
solo_ver = "--solo-ver" in sys.argv

if not MEM.exists():
    print("No hay memoria de Claude Code en este equipo (sesión en la nube): se usa solo estudio-video/memoria/.")
else:
    nombres = {f.name for f in HUB.glob("*.md") if f.name != "INDEX.md"} | {f.name for f in MEM.glob("*.md") if f.name.startswith(PREFIJOS)}
    for n in sorted(nombres):
        a, b = HUB / n, MEM / n
        if a.exists() and b.exists():
            if a.read_bytes() == b.read_bytes():
                continue
            src, dst = (a, b) if a.stat().st_mtime > b.stat().st_mtime else (b, a)
        elif a.exists():
            src, dst = a, b
        else:
            src, dst = b, a
        print(("[ver] " if solo_ver else "") + f"{src.parent.name}/{n} -> {dst.parent.name}/")
        if not solo_ver:
            shutil.copy2(src, dst)

if not solo_ver:
    filas = []
    for f in sorted(HUB.glob("*.md")):
        if f.name == "INDEX.md":
            continue
        m = re.search(r"^description:\s*(.+)$", f.read_text(encoding="utf-8"), re.M)
        filas.append(f"- [{f.stem.replace('_', ' ')}]({f.name}) — {m.group(1).strip() if m else ''}")
    (HUB / "INDEX.md").write_text(
        "# Memoria de video\n\nCopias de las notas de la memoria de Claude Code que tocan video (se sincronizan con `herramientas/sync_memoria.py`). "
        "Resumen de reglas: [../CLAUDE.md](../CLAUDE.md).\n\n" + "\n".join(filas) + "\n", encoding="utf-8")
    print("INDEX.md regenerado:", len(filas), "notas")
