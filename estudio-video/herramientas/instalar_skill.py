"""Instala el cargador de la skill video-onescreen en un entorno de Claude Code.
Uso:  python estudio-video/herramientas/instalar_skill.py            (en la raíz de un repo que contenga estudio-video/: crea .claude/skills/video-onescreen/SKILL.md)
      python estudio-video/herramientas/instalar_skill.py --usuario  (lo crea en ~/.claude/skills, apuntando a la ruta absoluta de esta carpeta)
La skill real vive en estudio-video/SKILL.md; el cargador solo la remite, así que nunca hay que actualizarlo."""
import re
import sys
from pathlib import Path

HUB = Path(__file__).resolve().parents[1]
real = (HUB / "SKILL.md").read_text(encoding="utf-8")
front = re.match(r"---\n.*?\n---\n", real, re.S).group(0)
if "--usuario" in sys.argv:
    destino = Path.home() / ".claude" / "skills" / "video-onescreen"
    ruta = str(HUB / "SKILL.md")
else:
    destino = HUB.parent / ".claude" / "skills" / "video-onescreen"
    ruta = "estudio-video/SKILL.md"
destino.mkdir(parents=True, exist_ok=True)
texto = (front + "\n# Video OneScreen (cargador)\n\nEste archivo solo carga la skill. **La skill real y todo su contenido están en `" + ruta
         + "`**: léela completa y síguela. No edites este archivo; las actualizaciones van en `estudio-video/`.\n")
(destino / "SKILL.md").write_text(texto, encoding="utf-8")
print("Cargador instalado en", destino / "SKILL.md")
