"""Genera la página de storyboards para que Cris revise video por video.

Uso:  python estudio-video/herramientas/storyboard.py SPEC.json SALIDA.html        (genera la página)
      python estudio-video/herramientas/storyboard.py servir SALIDA.html [PUERTO]    (la sirve en http://localhost:PUERTO/ y guarda lo que Cris envía)

SPEC.json = {"videos": [ {"id": "INTA36.0002", "titulo": "Gurú", "meta": "16:9 · voz Hale",
   "tomas": [ {"id": "S01", "t0": 0.0, "t1": 2.4, "voz": "Cuando todo falla...",
       "opciones": [   # SIEMPRE 5 por toma, en este orden: 3 PLANOS (A-C) + 2 MOTION DESIGNS (D-E); la capa es una sola (cada toma es un plano O un motion graphic); una lleva "fav": true
         {"tipo": "plano", "plano": "102385", "ruta": "D:/.../C0138.mp4", "plano_in": 12.0, "plano_out": 14.4, "fav": true,
          "frame_t": 13.0 (opcional; por defecto la mitad del tramo), "log": true (opcional: S-Log3 con conversión neutra para verlo), "nota": "..."},
         {"tipo": "plano", "plano": "105931", "ruta": "...", "plano_in": 2.0, "plano_out": 4.6},
         {"tipo": "plano", ...},
         {"tipo": "motion", "desc": "Nodos que se apagan y queda uno verde", "mov": "los nodos se apagan de izquierda a derecha",
          "plantilla": "cifra", "params": {"valor": "+20", "etiqueta": "idiomas"}   # PREFERIDO: biblioteca motion/plantillas.py (el boceto y el «mov» salen solos)
          "boceto": {"fondo": "#fff", "formas": [...]}  # alternativa a mano: PANTALLAZO estático del motion (no animado ni construido): ver boceto_svg(); flechas = indicaciones de movimiento
         } ]},
     ... más tomas ... ]},
   ... más videos ... ]}

Cris elige una opción por toma (la ★ favorita ya viene elegida) o «Ninguna sirve → traer 5 nuevas»; el envío trae por toma
{"d": "ok"|"no", "op": "B", "elegido": "plano 105931 2.0–4.6 s" | "MOTION: ...", "c": comentario}.
(Compatibilidad: una toma sin "opciones" se muestra como una sola opción favorita.)

Es determinista: no consulta nada, solo lee el JSON, saca un fotograma por toma con ffmpeg (si hay `ruta`) y
rellena `storyboard_plantilla.html`. Cris elige la opción de cada toma en la página;
con «Enviar» el servidor guarda `decisiones/<ID>.json` junto a la página (se sobrescribe en cada envío) y Claude lo lee de ahí.

Reglas que se COMPRUEBAN (si una falla no se escribe la página): hasta 3 planos + exactamente 2 motion por toma y una sola ★;
toma >= 1,5 s; el tramo del plano cubre la toma; plano grabado desde 2024 (si está la copia del Directorio); sin repetidos.
Rotación y veto (Cris, 29-oct; planos_rotacion.py): no se genera la página si un plano está VETADO (papelera) o ya se propuso en
alguno de los últimos 15 storyboards (cada video = un storyboard; regenerar la misma página no cuenta doble). `--sin-rotacion` salta
solo la regla de los 15 (no los vetados). Al generar, los planos de cada video quedan anotados en registro/planos_propuestos.json.
La papelera 🗑 de cada plano llama a POST /vetar del servidor y lo anota en registro/planos_vetados.json en el acto."""
import base64
import json
import subprocess
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "motion"))   # biblioteca de plantillas de motion (motion/plantillas.py)


LUT_DIR = Path("D:/OneScreen/Contenido/2026/10. Octubre/_inta_trabajo/lut")  # sony.cube: conversión neutra solo para ver S-Log3


from boceto import boceto_svg, revisar   # pantallazos y revisor de armado (textos que se pisan o salen, píldoras)
import planos_rotacion as R     # rotación de 15 storyboards y vetados (misma carpeta)

# filas del Directorio (copia local del selector) para comprobar la fecha de grabación (>= 2024, CLAUDE.md §4); si no está, no se comprueba
_DIR = Path("D:/OneScreen/Contenido/2026/10. Octubre/_inta_trabajo/directorio_rows.json")
FILAS = {r["ID"]: r for r in json.loads(_DIR.read_text(encoding="utf-8"))} if _DIR.exists() else {}


def frame(ruta, t, log=False):
    vf = ("lut3d=sony.cube:interp=tetrahedral," if log else "") + "scale=480:-2"
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", ruta, "-frames:v", "1", "-vf", vf,
                        "-q:v", "5", "-f", "image2pipe", "-vcodec", "mjpeg", "-"], capture_output=True, cwd=str(LUT_DIR) if log else None)
    return "data:image/jpeg;base64," + base64.b64encode(r.stdout).decode() if r.stdout else None


def main(spec_p, out_p):
    spec = json.loads(Path(spec_p).read_text(encoding="utf-8"))
    revisor = []    # avisos de boceto.revisar sobre cada motion design (nada se sobrepone, nada fuera del lienzo, sin píldoras)
    for v in spec["videos"]:
        for t in v["tomas"]:
            for x in [t] + t.get("opciones", []):
                if x.get("escena"):       # escena COMPUESTA libremente con el vocabulario de motion/elementos.py (no es una plantilla)
                    import elementos
                    spec_b, mov = elementos.escena(x["escena"])
                    x["boceto"] = spec_b
                    x.setdefault("mov", mov)
                    x.setdefault("desc", "escena compuesta")
                if x.get("plantilla"):    # motion desde plantilla: el pantallazo y la indicación de movimiento salen de la biblioteca
                    import plantillas
                    if x["plantilla"] not in plantillas.PLANTILLAS:
                        raise SystemExit(f"ERROR: {v['id']} {t['id']}: la plantilla «{x['plantilla']}» no existe (¿retirada? hub y palabras están prohibidas)")
                    spec_b, mov = plantillas.boceto(x["plantilla"], x.get("params", {}))
                    x["boceto"] = spec_b
                    x.setdefault("mov", mov)
                    x.setdefault("desc", "plantilla «" + x["plantilla"] + "»")
                if isinstance(x.get("boceto"), dict):
                    revisor += [f"{v['id']} {t['id']} (motion «{x.get('desc', '')[:30]}»): {a}" for a in revisar(x["boceto"])]
                    x["svg"] = boceto_svg(x["boceto"])
                    x.pop("boceto")
                if x.get("img") or not x.get("ruta"):
                    continue
                ft = x.get("frame_t")
                if ft is None:
                    a, b = x.get("plano_in"), x.get("plano_out")
                    ft = (a + b) / 2 if a is not None and b is not None else (a or 0)
                x["img"] = frame(x["ruta"], ft, x.get("log"))
                if not x["img"]:
                    print("sin fotograma:", v["id"], t["id"], x["ruta"])
                x.pop("ruta", None)
    # ---- revisión de reglas (CLAUDE.md §4 y paso 9b): 3 planos + 2 motion por toma y NINGÚN plano repetido entre videos del lote ni dentro de un video ----
    usados, estructura = {}, list(revisor)
    for v in spec["videos"]:
        for t in v["tomas"]:
            ops = t.get("opciones", [])
            npl = sum(1 for o in ops if o.get("tipo") != "motion")
            nmo = len(ops) - npl
            if npl > 3 or nmo != 2:     # menos de 3 planos se permite (no alcanzan planos buenos: se dice y se cubre con motion)
                estructura.append(f"{v['id']} {t['id']}: trae {npl} planos y {nmo} motion (deben ser hasta 3 planos + 2 motion designs)")
            elif npl < 3:
                print(f"AVISO: {v['id']} {t['id']} trae solo {npl} planos (no alcanzaron planos buenos; decirlo a Cris)")
            if sum(1 for o in ops if o.get("fav")) != 1:
                estructura.append(f"{v['id']} {t['id']}: debe tener exactamente una favorita ★")
            if t["t1"] - t["t0"] < 1.5 - 1e-3:
                estructura.append(f"{v['id']} {t['id']}: la toma dura {t['t1'] - t['t0']:.2f} s (< 1,5 s)")
            for o in ops:
                if o.get("tipo") != "motion" and o.get("plano_in") is not None and o.get("plano_out") is not None and o["plano_out"] - o["plano_in"] < t["t1"] - t["t0"] - 1e-3:
                    estructura.append(f"{v['id']} {t['id']}: el tramo del plano {o.get('plano')} ({o['plano_out'] - o['plano_in']:.2f} s) es más corto que la toma")
                if o.get("tipo") != "motion" and FILAS and str(o.get("plano")) in FILAS:
                    r = FILAS[str(o["plano"])]
                    anio = next((r[k][:4] for k in r if k.startswith("Fecha de grab") and r[k]), "")
                    if (not anio.isdigit() or int(anio) < 2024) and str(o['plano']) not in R.casos():   # casos de éxito exentos (Cris, 29-oct)
                        estructura.append(f"{v['id']} {t['id']}: el plano {o['plano']} no es de 2024 en adelante (fecha «{anio or 'sin fecha'}»)")
            for o in ops:
                if o.get("tipo") != "motion" and o.get("plano"):
                    usados.setdefault(str(o["plano"]), set()).add(v["id"])
    for pl, vs in sorted(usados.items()):
        if len(vs) > 1:
            print(f"AVISO: el plano {pl} se repite entre videos del lote: {', '.join(sorted(vs))} (no se comparten planos)")
    # repetidos: cualquier opcion (no solo la favorita) dentro de un video y entre tomas seguidas; el extracto de un caso (EXTRACTO) puede repetirse
    errores = estructura + [f"el plano {pl} se repite entre videos del lote: {', '.join(sorted(vs))}" for pl, vs in sorted(usados.items()) if len(vs) > 1]
    for v in spec["videos"]:
        cuenta = {}
        prev = set()
        for t in v["tomas"]:
            ids = [str(o["plano"]) for o in t.get("opciones", []) if o.get("tipo") != "motion" and o.get("plano")]
            for i in ids:
                cuenta.setdefault(i, []).append(t["id"])
            if prev & set(ids):
                errores.append(f"{v['id']}: {t['id']} repite con la toma anterior el plano {', '.join(sorted(prev & set(ids)))}")
            prev = set(ids)
        for i, ts in sorted(cuenta.items()):
            if len(ts) > 1:
                errores.append(f"{v['id']}: el plano {i} aparece en varias tomas ({', '.join(ts)})")
    # rotación (un plano 1 vez cada 15 storyboards) y vetados (papelera): reglas de Cris del 29-oct
    claves = {v["id"]: f"{Path(out_p).name}#{v['id']}" for v in spec["videos"]}
    vet, bloq = R.vetados(), R.bloqueados(excluir=claves.values())
    for v in spec["videos"]:
        for t in v["tomas"]:
            for o in t.get("opciones", []):
                pl = str(o.get("plano") or "")
                if o.get("tipo") == "motion" or not pl:
                    continue
                if pl in vet:
                    errores.append(f"{v['id']} {t['id']}: el plano {pl} está VETADO ({vet[pl].get('motivo') or 'papelera'})")
                elif pl in bloq and "--sin-rotacion" not in sys.argv:
                    errores.append(f"{v['id']} {t['id']}: el plano {pl} ya se propuso en {bloq[pl]} (un plano 1 vez cada {R.VENTANA} storyboards)")
    if errores:
        for e in errores:
            print("ERROR:", e)
        if "--permitir-repetidos" not in sys.argv or any("VETADO" in e or "ya se propuso" in e for e in errores) or estructura:
            print(f"{len(errores)} problema(s): no se genera el storyboard (los planos no se repiten, los vetados no vuelven y un plano sale 1 vez cada {R.VENTANA} storyboards; si no alcanzan, la toma se cubre con motion). Reparte con asignar_lote.py.")
            sys.exit(1)
    html = (AQUI / "storyboard_plantilla.html").read_text(encoding="utf-8")
    datos = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    Path(out_p).write_text(html.replace("__DATA__", datos), encoding="utf-8")
    for v in spec["videos"]:
        R.registrar(claves[v["id"]], [o["plano"] for t in v["tomas"] for o in t.get("opciones", []) if o.get("tipo") != "motion" and o.get("plano")])
    print("listo:", out_p, "|", len(spec["videos"]), "video(s),", sum(len(v["tomas"]) for v in spec["videos"]), "tomas")


def servir(html_p, puerto=8765):
    carpeta = Path(html_p).resolve().parent
    (carpeta / "decisiones").mkdir(exist_ok=True)

    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(carpeta), **k)

        def do_POST(self):
            if self.path == "/vetar":     # papelera: {"plano", "motivo", "origen", "deshacer": bool}
                d = json.loads(self.rfile.read(int(self.headers["content-length"])))
                if d.get("deshacer"):
                    R.desvetar(d["plano"])
                else:
                    R.vetar(d["plano"], d.get("motivo", ""), d.get("origen", ""))
                print(("desvetado: " if d.get("deshacer") else "VETADO: ") + str(d["plano"]), d.get("origen", ""), d.get("motivo", ""), flush=True)
                self.send_response(200)
                self.end_headers()
                return self.wfile.write(b"ok")
            if self.path != "/enviar":
                return self.send_error(404)
            d = json.loads(self.rfile.read(int(self.headers["content-length"])))
            d["enviado_en"] = time.strftime("%Y-%m-%d %H:%M:%S")
            nombre = "".join(c for c in d["id"] if c.isalnum() or c in "._-")
            (carpeta / "decisiones" / f"{nombre}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            print("recibido:", nombre, d["enviado_en"], flush=True)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *a):
            pass

    print(f"Storyboard en http://localhost:{puerto}/{Path(html_p).name}  (decisiones -> {carpeta / 'decisiones'})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", puerto), H).serve_forever()


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "servir":
        servir(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8765)
        raise SystemExit
    args = [a for a in sys.argv[1:] if a not in ("--permitir-repetidos", "--sin-rotacion")]
    if len(args) != 2:
        raise SystemExit(__doc__)
    main(args[0], args[1])
