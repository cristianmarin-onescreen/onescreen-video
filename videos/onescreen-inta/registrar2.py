"""Registra la versión .0002 (voz Hale directa con dirección) de cada pieza INTA en el espejo local, basada en .0001. uso: python -I registrar2.py"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from registrar import NOM
NOM = dict({"INTA09": ("Tus estudiantes ya viven en pantallas táctiles, ¿y su aula?", "N1")}, **NOM)
env = dict(os.environ, PYTHONIOENCODING="utf-8")
for pz, (nom, nivel) in NOM.items():
    r = subprocess.run([sys.executable, "herramientas/registro.py", "nueva", pz, "--nombre", nom, "--version", "v2", "--hook", "H1", "--contenido", "C1", "--cta", "A1", "--eje", "Idioma-voz",
                        "--basada", f"{pz}.0001", "--voz", "neutro", "--cambio", "Voz: Hale directo (eleven_v4, español neutro latino, guion dirigido) en lugar de locución colombiana pasada a Hale, que salió plana; mismo montaje y planos reseleccionados por tiempos",
                        "--builder", "videos/onescreen-inta/producir.py", "--formatos", "16x9, 9x16, 4x5", "--vertical", "INT", "--nivel", nivel],
                       capture_output=True, text=True, cwd=r"C:\Users\Cristian Marin\Desktop\Claudio\estudio-video", env=env)
    print(r.stdout.strip() or r.stderr.strip()[-300:])
