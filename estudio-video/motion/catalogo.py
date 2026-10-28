"""Catálogo COMPLETO de referencias y plantillas de motion.
Parte 1: TODAS las referencias que Cris ha mandado (cada imagen/video guardado), numeradas, con la(s) plantilla(s) que salen de ella.
Parte 2: cada plantilla con SU referencia (izquierda) y nuestro pantallazo (derecha), con su indicación de movimiento y avisos del revisor de armado.
Uso: python estudio-video/motion/catalogo.py [SALIDA.html]   (por defecto: D:\\OneScreen\\Contenido\\2026\\10. Octubre\\_referencias_motion\\catalogo.html)
Sirve para escoger: «quiero la de la referencia 14» = `pregunta`. Cada referencia nueva se agrega a plantillas_ref.py (REFERENCIAS, EJEMPLOS) y vuelve a salir aquí."""
import base64
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "herramientas"))
import plantillas      # noqa: E402
import plantillas_ref  # noqa: E402
from boceto import boceto_svg, revisar  # noqa: E402

REF_DIR = Path("D:/OneScreen/Contenido/2026/10. Octubre/_referencias_motion")
NOTAS_IMG = {"ideas/17.webp": "repetida: es la misma de la 1 (Imagine)"}


def miniatura(rel, ancho=520):
    if not rel:
        return None
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(REF_DIR / rel), "-frames:v", "1", "-vf", f"scale={ancho}:-2", "-q:v", "5", "-f", "image2pipe", "-vcodec", "mjpeg", "-"], capture_output=True)
    return "data:image/jpeg;base64," + base64.b64encode(r.stdout).decode() if r.stdout else None


def todas_las_referencias():
    """lista (ruta relativa, título) de cada imagen guardada, en orden numérico"""
    imgs = sorted((REF_DIR / "ideas").glob("*.*"), key=lambda p: int(re.match(r"\d+", p.stem).group()) if re.match(r"\d+", p.stem) else 999)
    out = [(f"ideas/{p.name}", f"Referencia {p.stem}") for p in imgs]
    out += [(f"apple/sheets/{p.name}", "Apple: " + p.stem) for p in sorted((REF_DIR / "apple" / "sheets").glob("*.jpg"))]
    return out


def main(salida):
    por_img = {}
    for nombre, (img, _nota) in plantillas_ref.REFERENCIAS.items():
        if img:
            por_img.setdefault(img, []).append(nombre)
    galeria = []
    for rel, titulo in todas_las_referencias():
        pl = por_img.get(rel) or []
        if not pl and rel == "ideas/17.webp":
            pl = por_img.get("ideas/1.webp", [])
        estado = ", ".join(f"<b>{x}</b>" for x in pl) if pl else '<span style="color:#ff9a9a">sin plantilla todavía</span>'
        extra = f"<br><small>{NOTAS_IMG[rel]}</small>" if rel in NOTAS_IMG else ""
        m = miniatura(rel, 360)
        galeria.append(f'<figure><img src="{m}"><figcaption><b>{titulo}</b><br>→ {estado}{extra}</figcaption></figure>')
    sin_img = [(n, nota) for n, (img, nota) in plantillas_ref.REFERENCIAS.items() if not img]
    cards, avisos = [], []
    for nombre, (img, nota) in plantillas_ref.REFERENCIAS.items():
        ej = plantillas_ref.EJEMPLOS.get(nombre)
        if not ej:
            continue
        spec, mov = plantillas.boceto(nombre, ej)
        av = revisar(spec)
        if av:
            avisos.append(f"{nombre}: " + "; ".join(av))
        m = miniatura(img)
        izq = f'<img src="{m}">' if m else f'<div class="sin">sin imagen guardada<br><small>{nota}</small></div>'
        svg = boceto_svg(spec).replace("<svg ", "<svg style='width:100%;display:block;border-radius:8px' ")
        cards.append(f'<section id="{nombre}"><h3>{nombre}</h3><div class="par"><div>{izq}<p>{nota}</p></div><div>{svg}<p><b>Movimiento:</b> {mov}</p></div></div></section>')
    html = ('<!doctype html><meta charset="utf-8"><title>Catálogo de referencias y plantillas de motion</title><style>body{font:15px/1.4 Manrope,system-ui,sans-serif;background:#12151b;color:#eceff6;margin:0;padding:24px}'
            'h1,h2{margin:0 0 6px}h2{margin-top:30px}section{background:#1b2029;border:1px solid #2c313d;border-radius:14px;padding:14px;margin:16px 0}h3{margin:0 0 10px;color:#8fb4ff}'
            '.par{display:grid;grid-template-columns:1fr 1.4fr;gap:16px}img{width:100%;border-radius:8px;display:block}p{color:#9aa3b5;font-size:13px;margin:8px 0 0}'
            '.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}figure{margin:0;background:#1b2029;border:1px solid #2c313d;border-radius:12px;padding:10px}figcaption{font-size:13px;color:#c9d0de;margin-top:8px}'
            '.sin{border:1px dashed #44505f;border-radius:8px;padding:30px;color:#9aa3b5;min-height:120px}@media(max-width:900px){.par{grid-template-columns:1fr}}</style>'
            f'<h1>Referencias y plantillas de motion</h1><p>{len(galeria)} referencias guardadas · {len(cards)} plantillas con ejemplo.</p>'
            f'<h2>1. Todas las referencias</h2><div class="gal">{"".join(galeria)}</div>'
            + ('<h2>Referencias sin imagen guardada</h2><ul>' + "".join(f"<li><b>{n}</b>: {nota}</li>" for n, nota in sin_img) + "</ul>" if sin_img else "")
            + f'<h2>2. Cada plantilla con su referencia</h2>{"".join(cards)}')
    Path(salida).write_text(html, encoding="utf-8")
    print("catálogo:", salida, "|", len(galeria), "referencias,", len(cards), "plantillas")
    for a in avisos:
        print("AVISO", a)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(REF_DIR / "catalogo.html"))
