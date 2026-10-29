"""Storyboard de INTA41.0001 (Renta TOFU 1, educación; voz aprobada 29-oct, Voz\\aprobada\\).
Paso 1 (cand): por toma, candidatos del Directorio puntuados con seleccion._evalua contra palabras clave de la toma -> hojas de contacto para MIRARLOS.
Paso 2 (spec): con los planos ya vistos (ELEGIDOS) y los 2 motion por toma, escribe Storyboard\\SPEC_v1.json.
uso: python -I storyboard_inta41.py cand   |   python -I storyboard_inta41.py spec"""
import io, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import seleccion as S

B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre"); PZ = "INTA41"; VID = "INTA41.0001"
SB = B / PZ / "Storyboard"; LUT = B / "_inta_trabajo" / "lut"
BYID = {r["ID"]: r for r in S.rows}
from specs import EDU
TEMA = dict(EDU, kw=["aula", "colegio", "docente", "estudiantes", "pantalla"])

# (id, t0, t1, palabras clave para buscar el plano)  · cortes 2-3 cuadros antes de la palabra; ninguna toma < 1,5 s
TOMAS = [
 ("S01", 0.00, 1.78, "padre recorre colegio pasillo camina visita"),
 ("S02", 1.78, 4.64, "aula salon estudiantes clase colegio"),
 ("S03", 4.64, 6.80, "aula moderna salon clase pantalla"),
 ("S04", 6.80, 8.58, "pantalla interactiva toca tactil"),
 ("S05", 8.58, 11.08, "pizarra escribe proyecta video sonido pantalla"),
 ("S06", 11.08, 12.92, "docente escribe pizarra marcador pantalla"),
 ("S07", 12.92, 14.46, "docente explica muestra estudiantes pantalla"),
 ("S08", 14.46, 16.42, "docente prepara clase computador inteligencia artificial"),
 ("S09", 16.42, 18.00, "pantalla onescreen aula docente"),
 ("S10", 18.00, 19.88, "estudiantes clase pantalla interactua"),
 ("S11", 19.88, 21.68, "docente estudiantes pantalla clase"),
 ("S12", 21.68, 23.28, "aula pantalla estudiantes"),
 ("S13", 23.28, 24.92, "aula pantalla clase"),
 ("S14", 24.92, 27.14, "instalacion capacitacion formacion docentes taller"),
 ("S15", 27.14, 30.32, "aula moderna estudiantes pantalla colegio"),
 ("S16", 30.32, 32.04, "padres colegio estudiantes"),
 ("S17", 32.04, 35.28, "docente estudiantes pantalla clase"),
 ("S18", 35.28, 38.34, "aula pantalla estudiantes clase"),
]


def tg(t0, t1, kw):
    q = set()
    for t in S.toks(kw):
        q |= {S.stem(t)} | {S.stem(s) for s in S.SYN.get(t, "").split()}
    return dict(q=q, qtok=set(S.toks(kw)), texto_l=kw, t0=t0, t1=t1)


def cands(t0, t1, kw, n=12):
    g = tg(t0, t1, kw); dur = t1 - t0; need = max(1.8, dur + 0.2); out = {}
    for relax in (0, 1, 2, 3):
        for r in S.rows:
            s = S._evalua(r, g, TEMA, relax, need, set(), {}, {})
            if s is None or not S.ruta_id(r):
                continue
            rk = s - 2.0 * relax
            if r["ID"] not in out or rk > out[r["ID"]][0]:
                out[r["ID"]] = (rk, r)
    return [r for _, r in sorted(out.values(), key=lambda x: -x[0])][:n], need


def fr(p, t, log):
    vf = ("lut3d=sony.cube:interp=tetrahedral," if log else "") + "scale=256:-2"
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1", "-vf", vf, "-f", "image2pipe", "-vcodec", "mjpeg", "-"],
                       capture_output=True, cwd=str(LUT) if log else None)
    from PIL import Image
    return Image.open(io.BytesIO(r.stdout)) if r.stdout else Image.new("RGB", (256, 144), "#444")


def hoja_cand():
    from PIL import Image, ImageDraw
    SB.mkdir(exist_ok=True); usados = set(); todo = {}
    for tid, t0, t1, kw in TOMAS:
        lista, need = cands(t0, t1, kw, n=400)
        lista = [r for r in lista if r["ID"] not in usados][:9]
        usados |= {r["ID"] for r in lista}
        fichas = [S.ficha_plano(r, need) for r in lista]
        todo[tid] = fichas
        im = Image.new("RGB", (3 * 3 * 262 + 10, 3 * 172 + 30), "white"); d = ImageDraw.Draw(im)
        d.text((6, 4), f"{tid} {t0:.2f}-{t1:.2f}  [{kw}]", fill="black")
        for k, f in enumerate(fichas):
            col, row = k % 3, k // 3
            for j, fr_t in enumerate((f["ss"] + 0.1, f["ss"] + f["need"] / 2, f["ss"] + f["need"] - 0.1)):
                x = (col * 3 + j) * 262 + 5; y = 24 + row * 172
                im.paste(fr(f["ruta"], fr_t, f["log"]), (x, y))
            d.text((col * 3 * 262 + 8, 24 + row * 172 + 146), f"{f['id']} ss{f['ss']} | {f['desc'][:70]}", fill="red")
        im.save(SB / f"cand_{tid}.jpg", quality=78)
        print(tid, [f["id"] for f in fichas])
    json.dump(todo, open(SB / "cand_INTA41.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "cand":
        hoja_cand()
