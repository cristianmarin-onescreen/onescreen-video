"""Planos reales del Lápiz Interactivo (LAPIZP) para el video de Mercado Libre.
Material: D:\\OneScreen\\Varios\\Harrison Caballero\\...\\MARCADOR INFINITO\\videos\\C00xx.MP4 (crudos S-Log3 4K, 16-ene-2025, Sebastián usando el lápiz).
NO se usa el video exportado "Marcador Infinito_Titled" (Cris, 28-oct: solo planos crudos).
  python ml_lapiz.py recortar   recorta 10 s en 9:16 (1080x1920) de cada plano -> LAPIZP/planos/<k>_crudo.mp4
  python ml_lapiz.py instalar   copia el render del lápiz a img/LAPIZP_prod.png
  python ml_lapiz.py desde_color corta el export de Cris (LAPIZ_COLOR.mp4) en 3 planos 9:16 -> veo/LAPIZP_<k>.mp4 (sin tocar el color)
  python ml_lapiz.py prproj     .prproj con los 3 originales 4K SIN color para que Cris coloree en Premiere"""
import shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RAW = Path(r"D:\OneScreen\Varios\Harrison Caballero\HARRISON CABALLERO\MARCADOR INFINITO\videos")
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\Mercado Libre")
SALIDA = BASE / "LAPIZP" / "planos"
# k: (plano, segundo de inicio, posicion horizontal de la ventana 9:16: 0 = izquierda, 1 = derecha)
PLANOS = {"a": ("C0125", 2.0, 0.10),   # escribe un trazo verde con el lápiz (fijo, calidad 4)
          "b": ("C0123", 4.0, 0.55),   # señala las puntas y herramientas de Write con el lápiz (fijo)
          "c": ("C0127", 3.0, 0.50)}   # escribe "Lion" en la pizarra (fijo)


def recortar():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for k, (clip, t0, frac) in PLANOS.items():
        sal = SALIDA / f"{k}_crudo.mp4"
        # rango completo yuvj420p como sale de la A7III: el pipeline asume eso
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-t", "10", "-i", str(RAW / f"{clip}.MP4"), "-an", "-vf",
                        f"crop=ih*9/16:ih:(iw-ih*9/16)*{frac}:0,scale=1080:1920:flags=lanczos,format=yuvj420p",
                        "-c:v", "libx264", "-crf", "10", "-preset", "fast", str(sal)], check=True)
        print(sal)


def instalar():
    """Solo el render del lapiz para las escenas de color; los planos entran sin color y los colorea Cris."""
    shutil.copy(BASE / "LAPIZP/Material/Imágenes y videos/Lápiz Render_clean.png", BASE / "img/LAPIZP_prod.png")
    print("instalado")


def prproj():
    """.prproj con los 3 ORIGINALES 4K sin colorear (secuencia 4K 23,976 de la plantilla) para que Cris coloree en Premiere.
    El color NO se toca aqui (Cris, 28-oct: "no tienes autorizacion a colorear nada"). Tras su export en alta calidad
    se hacen los recortes 9:16 (flujo de CLAUDE.md, pasos 13-14). Reutiliza videos/onescreen-quizwiz-scrybe/build_prproj.py (modo PLANOS)."""
    import json, os
    destino = BASE / "LAPIZP" / "Premiere"
    destino.mkdir(parents=True, exist_ok=True)
    srcp, clips, t = {}, [], 0.0
    for k, (clip, t0, _frac) in PLANOS.items():
        ruta = RAW / f"{clip}.MP4"
        probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(ruta)],
                                          capture_output=True, text=True, encoding="utf-8").stdout)
        srcp[k] = {"path": str(ruta).replace("\\", "/"), "ss": 0.0, "probe": probe}
        clips.append({"src": k, "t": t, "dur": 10.0, "tin": t0, "scale": 100, "origin": "50% 50%"})
        t += 10.0
    (destino / "src_probe.json").write_text(json.dumps(srcp, ensure_ascii=False), encoding="utf-8")
    (destino / "plan.json").write_text(json.dumps({"END_SCENE": t, "clips": clips, "events": {}, "whites": []}), encoding="utf-8")
    env = dict(os.environ, PLANOS="1", PLAN_JSON=str(destino / "plan.json"), SRCP_JSON=str(destino / "src_probe.json"),
               SEQ="LAPIZP planos para colorear", PYTHONUTF8="1")
    salida = destino / "LAPIZP_planos_para_colorear.prproj"
    subprocess.run([sys.executable, "-I", str(REPO / "videos/onescreen-quizwiz-scrybe/build_prproj.py"), str(salida)], env=env, check=True)
    print(salida)


def desde_color():
    """Corta el export coloreado por Cris (LAPIZ_COLOR.mp4, 4K 16:9, secuencia de los 3 planos con 0,5 s de margen) y recorta a 9:16.
    NO toca el color. Deja veo/LAPIZP_<k>.mp4 (10 s, 1080x1920) que ml_producto.py usa como planos reales."""
    import json
    export = BASE / "LAPIZ_COLOR.mp4"
    mapa = json.loads((BASE / "LAPIZP/Premiere/LAPIZP_planos_para_colorear.planos.json").read_text(encoding="utf-8"))
    for m in mapa:
        k = m["src"]
        clip, t0, frac = PLANOS[k]
        inicio = m["secuencia_inicio_s"] + (t0 - m["origen_in_s"])      # segundo del export donde empieza mi corte de 10 s
        sal = BASE / "veo" / f"LAPIZP_{k}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{inicio:.3f}", "-t", "10", "-i", str(export), "-an", "-vf",
                        f"crop=ih*9/16:ih:(iw-ih*9/16)*{frac}:0,scale=1080:1920:flags=lanczos,format=yuv420p",
                        "-c:v", "libx264", "-crf", "12", "-preset", "fast", str(sal)], check=True)
        print(sal, f"(export {inicio:.2f}-{inicio + 10:.2f} s)")


if __name__ == "__main__":
    {"recortar": recortar, "instalar": instalar, "prproj": prproj, "desde_color": desde_color}[sys.argv[1]]()
