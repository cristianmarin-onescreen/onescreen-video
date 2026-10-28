"""Video corporativo (25-oct-2026): planos del Directorio de video, SIN COLOREAR. Solo la conversión neutra S-Log3→Rec.709 para poder ver
(las tomas S-Log2 pasan por la misma LUT: es solo para ver, el color real va en Premiere). Stock e IA van tal cual.
python cortes.py  -> D:/OneScreen/Contenido/2026/10. Octubre/Corporativo salas de reuniones/Proyecto/v_<FMT>/media/<ID>.mp4 en 16:9, 9:16 y 4:5"""
import os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

B = "D:/OneScreen/"
R = Path("D:/OneScreen/Contenido/2026/10. Octubre/Corporativo salas de reuniones/Proyecto")
SRC = {  # ID del Directorio: (ruta, inicio, duración, punto focal x, log)
    "102648": (B + "Contenido/2026/7. Julio/CASO DE ÉXITO. Comfenalco/Apoyo/C1334.MP4", 0.5, 2.5, 0.50, 1),
    "101968": (B + "Contenido/2026/2. Febrero/10. Pantalla Interactiva vs otros/old-projector-lens-2025-12-17-12-08-45-utc.mov", 9.0, 2.5, 0.50, 0),
    "105957": (B + "Varios/Escritorio/Marketing/Copia de tera/Os/2024/4. Abril/Bucaramanga/Heyes English/B-Roll/C1300.MP4", 2.0, 2.0, 0.50, 1),
    "102227": (B + "Contenido/2026/6. Junio/Caso de éxito - Gimnasio Jireh/Apoyos/C1451.MP4", 0.3, 2.5, 0.55, 1),
    "102731": (B + "Contenido/2026/7. Julio/VIDEO. Regreso a clases/stack-of-electronic-sockets-close-up-isolated-4k-2025-12-17-19-18-38-utc.mp4", 10.0, 2.0, 0.55, 0),
    "101944": (B + "Contenido/2026/2. Febrero/07. Beneficios en salas de reuniones PUBLICADO/Slow_orbiting_4k_202602191541.mp4", 3.0, 2.0, 0.50, 0),
    "101421": (B + "Contenido/2025/9. Septiembre/Cablecom. Caso de éxito/Apoyo/C0611.MP4", 0.3, 2.0, 0.42, 1),
    "101939": (B + "Contenido/2026/2. Febrero/07. Beneficios en salas de reuniones PUBLICADO/C0924.MP4", 6.0, 2.5, 0.58, 1),
    "101927": (B + "Contenido/2026/2. Febrero/06. Beneficios en educación PUBLICADO/02_CEA_COR_PLANO DE MICROFONOS_T7_PP_505.MP4", 3.0, 2.0, 0.50, 1),
    "102604": (B + "Contenido/2026/6. Junio/Overview OneScreen AIO/C0530.MP4", 4.0, 2.0, 0.40, 1),
    "101831": (B + "Contenido/2026/10. Octubre/CASO DE ÉXITO. La Patria/Apoyo/C1136.MP4", 5.0, 2.5, 0.50, 1),
    "101875": (B + "Contenido/2026/10. Octubre/CASO DE ÉXITO. La Patria/Apoyo/C1182.MP4", 6.5, 2.5, 0.55, 1),
    "102711": (B + "Contenido/2026/7. Julio/VIDEO. Nativos digitales/C1569.MP4", 3.5, 2.0, 0.35, 1),
    "101042": (B + "Contenido/2025/7. Julio/Core Video/Apoyo/C0070.MP4", 0.5, 2.0, 0.40, 1),
    "106200": (B + "Varios/Escritorio/Marketing/Copia de tera/Os/2024/4. Abril/Video paisas/Source/close-up-portrait-of-woman-a-technical-customer-su-2023-11-27-05-15-17-utc.mov", 4.0, 2.5, 0.30, 0),
    "101799": (B + "Contenido/2026/10. Octubre/CASO DE ÉXITO. La Patria/Apoyo/C1105.MP4", 34.0, 4.0, 0.50, 1),
}
FORM = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}
LUT = R / "lut"; LUT.mkdir(parents=True, exist_ok=True)
shutil.copy("C:/Users/Cristian Marin/Desktop/Claudio/luts/festivalluts.com - Sony S-Log3 → Rec.709.cube", LUT / "sony.cube")


def uno(item):
    n, (src, ss, t, fx, log) = item
    for f, (w, h) in FORM.items():
        dst = R / f"v_{f}" / "media" / f"{n}.mp4"; dst.parent.mkdir(parents=True, exist_ok=True)
        # recorte al aspecto alrededor del punto focal (expresión de ffmpeg: funciona con fuentes 4K y 1080p)
        crop = f"crop='min(iw,ih*{w}/{h})':'min(ih,iw*{h}/{w})':'max(0,min(iw-min(iw,ih*{w}/{h}),{fx}*iw-min(iw,ih*{w}/{h})/2))':'(ih-min(ih,iw*{h}/{w}))/2'"
        vf = ("lut3d=sony.cube:interp=tetrahedral," if log else "") + f"fps=24,{crop},scale={w}:{h}:flags=lanczos,setsar=1"
        r = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(ss), "-i", src, "-t", str(t), "-an", "-vf", vf, "-c:v", "libx264", "-crf", "14",
                            "-g", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(dst)], capture_output=True, text=True, cwd=str(LUT))
        if r.returncode:
            return f"ERROR {n} {f} {r.stderr[-300:]}"
    return f"ok {n}"


SOLO = sys.argv[1:]
with ThreadPoolExecutor(3) as ex:
    for m in ex.map(uno, [kv for kv in SRC.items() if not SOLO or kv[0] in SOLO]):
        print(m, flush=True)
