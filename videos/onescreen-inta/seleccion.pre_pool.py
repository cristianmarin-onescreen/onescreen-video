"""Selección de planos del Directorio para los guiones INTA (preview, 26-oct-2026).
Parte la narración en tramos de ~1,2-2 s (REGLAS §5), puntúa los planos contra lo que dice cada tramo (apoyo literal) y el tema de la pieza,
y escribe <Pieza>\\Proyecto\\planos.json. Reglas duras: calidad >= 4, sin menores en cámara, vetados 103182 y 103512, existe en disco,
permisos Libre (o 'requiere aprobación' solo si la ruta es del caso de la pieza), no repetir plano dentro de la pieza ni dentro de la tanda (penaliza).
uso: python -I seleccion.py INTA09 [INTA15 ...]   (sin argumentos: las 12, en orden, para repartir planos)"""
import json, os, re, sys, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from specs import SPECS
import estable

BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
T = BASE / "_inta_trabajo"
rows = json.load(open(T / "directorio_rows.json", encoding="utf-8"))
VETADOS = {"103182", "103512", "102433"}
_ve = Path("D:/OneScreen/Contenido/2026/10. Octubre/_inta_trabajo/vetados_extra.json")      # planos donde sale la persona vetada (detectados con Gemini sobre los cuadros)
if _ve.exists():
    VETADOS |= set(json.load(open(_ve, encoding="utf-8")))
STOP = set("a al algo alguien ante antes aqui asi aun bien cada como con contigo cual cuando de del desde donde dos el ella ellos en entre era es esa ese eso esta este esto estos fue ha hace hacen hay hoy la las le les lo los mas me mi mientras muy ni no nos nuestra o para pero por porque que quien se si sin sobre solo son su sus tambien te tengan tiene todo todos tu tus un una uno unos va y ya yo".split())
SYN = {  # lo que se dice -> lo que describe la ficha
    "estudiante": "estudiantes alumnos aula clase", "estudiantes": "estudiantes alumnos aula clase", "aula": "aula salon clase estudiantes", "salon": "aula salon clase",
    "clase": "aula clase docente profesor estudiantes", "docente": "docente profesor profesora clase", "docentes": "docente profesor profesora",
    "pantalla": "pantalla interactiva", "pantallas": "pantalla interactiva", "tocando": "toca tocar tactil pantalla", "tocar": "toca tactil", "deslizar": "desliza dedo tactil", "escribir": "escribe escribiendo marcador pizarra",
    "escribe": "escribe pizarra marcador", "reunion": "reunion sala juntas equipo", "reuniones": "reunion sala juntas equipo", "sala": "sala reuniones juntas", "pizarra": "pizarra escribe dibuja marcador",
    "viajaba": "viaje carretera camioneta aeropuerto", "viaja": "viaje carretera", "plantacion": "plantacion palma cultivo aerea", "recorrerla": "carretera camino",
    "videollamada": "videollamada videoconferencia camara", "ingeniero": "soporte tecnico ingeniero atencion", "soporte": "soporte tecnico ingeniero atencion", "falla": "soporte tecnico problema",
    "procedimientos": "cirugia procedimiento clinica", "quirurgico": "cirugia procedimiento clinica", "estudiantes ven": "estudiantes ven pantalla",
    "traduce": "idioma traduccion", "idiomas": "idioma traduccion", "transcribe": "transcripcion texto reunion", "resumen": "resumen documento texto", "acta": "documento escribe computador",
    "cuota": "dinero pago calculadora", "flujo": "dinero pago calculadora", "caja": "dinero pago", "arrendar": "contrato firma", "fabrica": "fabrica produccion ensamblaje", "fabricamos": "fabrica produccion ensamblaje",
    "instala": "instalacion tecnico instala", "instalacion": "instalacion tecnico instala", "mantenimiento": "tecnico mantenimiento", "ia": "inteligencia artificial", "examen": "examen quiz preguntas estudiantes",
    "cables": "cables", "pdf": "documento pdf", "qr": "qr codigo celular", "celular": "celular movil", "universidad": "universidad estudiantes aula", "demostracion": "demostracion presentador pantalla",
}


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def toks(t):
    return [w for w in re.findall(r"[a-z0-9]+", norm(t)) if w not in STOP and len(w) > 2]


def stem(w):
    return w[:5]


def num(s):
    try:
        return float(str(s).replace(",", "."))
    except Exception:
        return 0.0


def ruta(r):
    p = (r["Ruta en disco"] or "").split("\n")[0].strip()
    if not p:
        return None
    cand = [p] if re.match(r"^[A-Za-z]:", p) else [r"D:\OneScreen" + (p if p.startswith("\\") else "\\" + p), r"D:\OneScreen\Contenido" + (p if p.startswith("\\") else "\\" + p)]
    for c in cand:
        if os.path.exists(c):
            return c
    return None


KFECHA = next(k for k in rows[0] if k.startswith("Fecha"))
KORI = next(k for k in rows[0] if k.startswith("Origen"))
KAUD = next(k for k in rows[0] if k.startswith("Tipo de audio"))
KMOV = next(k for k in rows[0] if k.startswith("Movimiento"))
MOV_OK = ("Fijo", "Travelling / dolly", "Gimbal", "Dron")     # Cris 27-oct: errores de cámara (mano, zoom, tilt, combinado) sobre todo al inicio del clip
INI = 1.2                                                    # y nunca se arranca antes de 1,2 s del clip (el inicio trae sacudidas y enfoque)
RAW = re.compile(r"^C\d{4}\.mp4(\.mp4)?$", re.I)                      # solo clips crudos de cámara: nada de exportaciones ya editadas
HABLA = re.compile(r"explica|explicando|habla |hablando|dialog|conversa|entrevista|testimonio|expone|exponiendo|discurso|vocer|conferencista|dicta ", re.I)
INSTALA = re.compile(r"instal|desempaca|montaje|monta |montando|ensambl|arma la base|armando|soporte (con|wandr|de pared|rodante)|sobre un soporte|tubo|interruptor|enciende|encendiendo|c.mara web|webcam|camina|recorre|laboratorio t|herramienta de monta|cable|taladr|atornill|empaque|desempac", re.I)


def anio(r):
    m = re.match(r"\s*(\d{4})", r[KFECHA] or "")
    return int(m.group(1)) if m else 0


def base_ok(r, habla_ok=False, audio_ok=False):
    # Cris 27-oct: nada grabado antes de 2024 (excolaboradores que hoy trabajan en la competencia); nada generado con IA; nada ya editado
    # (exportaciones, anuncios, música/voz en off); ningún plano de gente hablando como apoyo (salvo piezas de caso donde hablan ellos).
    if r["ID"] in VETADOS or anio(r) < 2024 or r[KORI] != "Cámara propia" or not RAW.match(r["Clip"].strip()):
        return False
    if r[KMOV] not in MOV_OK:
        return False
    if r["Categoría"] in ("Comercial / pauta", "Unboxing") or r[KAUD] in ("Voz en off", "Música"):
        return False
    if not habla_ok and ((r[KAUD] == "Entrevista / voz a cámara" and not audio_ok) or HABLA.search(r["Información adicional"])):
        return False
    if "IA" in r["Información adicional"].split() or "generad" in norm(r["Información adicional"])[:80]:
        return False
    return (num(r["Calidad (1-5)"]) >= 4 and "Menores" not in r["Permisos"] and "No usar" not in r["Permisos"] and num(r["Duración (s)"]) >= 2.2)


FICHA = {}
for r in rows:
    FICHA[r["ID"]] = set(stem(w) for w in toks(" ".join([r["Acciones / palabras clave"], r["Información adicional"], r["Categoría"], r["Lugar"], r["Producto"], r["Personas"], r["Software en pantalla"]])))


def trozos(words, objetivo=1.0, maximo=1.7):
    """tramos de ~1,2-2 s cortando en pausa o signo de puntuación"""
    out, cur = [], []
    for w in words:
        cur.append(w)
        dur = w["end"] - cur[0]["start"]
        fin = bool(re.search(r"[.,;:?!»]$", w["text"].strip())) or w.get("gap", 0) > 0.25
        if (dur >= objetivo and fin) or dur >= maximo:
            out.append(cur); cur = []
    if cur:
        if out and cur[-1]["end"] - cur[0]["start"] < 0.8:
            out[-1].extend(cur)
        else:
            out.append(cur)
    return out


def elegir(pieza, usados_tanda, usados, n_alt=0):
    """n_alt > 0: modo candidatos para el storyboard; no escribe planos.json y devuelve el plan con `alts` (los siguientes mejores) por tramo."""
    spec = SPECS[pieza]
    voz = BASE / pieza / "Voz"
    words = [w for w in json.load(open(voz / f"{pieza}_voz_scribe.json", encoding="utf-8"))["words"] if w.get("type") == "word"]
    for a, b in zip(words, words[1:]):
        a["gap"] = b["start"] - a["end"]
    # el cierre (tarjeta) empieza en su palabra ancla: los planos llegan hasta ahí
    cierre_t = None
    cw, cn = spec["cierre"]["word"]
    k = [w for w in words if norm(w["text"]).strip(".,¿?¡!«»:;") == norm(cw)]
    cierre_t = k[cn]["start"] if k else words[-1]["start"]
    ws = [w for w in words if w["start"] < cierre_t]
    tema = spec["tema"]
    plan = []
    fin = {}
    # candidatos extra por tramo (solo n_alt)
    for n, tr in enumerate(trozos(ws)):
        q = []
        for w in tr:
            for t in toks(w["text"]):
                q += [stem(t)] + [stem(s) for s in SYN.get(t, "").split()]
        qtok = {t for w in tr for t in toks(w["text"])}
        q = set(q)
        t0, t1 = tr[0]["start"], (ws[ws.index(tr[-1]) + 1]["start"] if ws.index(tr[-1]) + 1 < len(ws) else cierre_t)
        need0 = max(2.2, t1 - t0 + 0.7)
        need1 = max(1.8, t1 - t0 + 0.2)
        best = None
        cands = []
        need = need0
        for need, relax in ((need0, 0), (need0, 1), (need0, 2), (need0, 3), (need1, 3)):
            if best:
                break
            for r in rows:
                if not base_ok(r, tema.get("habla_ok", False), relax >= 3) or num(r["Duración (s)"]) < need + INI + 0.2 or (r["ID"] in usados and (relax < 3 or num(r["Duración (s)"]) - fin.get(r["ID"], 0) < need + 0.2)):
                    continue
                caso = tema.get("caso") and re.search(tema["caso"], r["Ruta en disco"] + r["Información adicional"], re.I)
                if "Requiere aprobación" in r["Permisos"] and not caso:
                    continue
                if tema.get("solo_caso") and not caso:
                    continue
                f = FICHA[r["ID"]]
                if INSTALA.search(r["Información adicional"] + r["Categoría"]) and not any(x.startswith("instal") for x in qtok):
                    continue
                m = len(q & f) + len(set(stem(x) for x in tema.get("kw", [])) & f)
                s = 3.0 * len(q & f) + (3.0 if caso else 0)
                if r["Lugar"] in tema.get("lugares", []):
                    s += 2.5
                if r["Sector"] in tema.get("sectores", []):
                    s += 1.5
                s += len(set(stem(x) for x in tema.get("kw", [])) & f) * 1.2
                if "OneScreen" in r["Producto"] and re.search(r"pantalla|clase|reuni|pizarra|escrib|toc|aula|salon|sala|examen|idioma|transcrib|resumen|docente|estudiante", " ".join(w["text"].lower() for w in tr)):
                    s += 2.0
                if r["Producto"].startswith("Ninguno") and tema.get("exige_pantalla"):
                    s -= 1.0
                if r["Categoría"] in ("Academy / tutorial", "Entrevista / testimonio", "Institucional / equipo") and not caso:
                    s -= 2.5
                if re.search(r"wandr|crm|leads|tutorial|onescreen account|lessn|scrybe", norm(r["Información adicional"] + " " + r["Producto"])) and not (q & set(stem(x) for x in ["wandr", "crm", "leads", "lessn", "scrybe"])):
                    s -= 3.0
                if r["Origen"] in ("Generado con IA",):
                    s -= 1.0
                info = norm(r["Información adicional"])
                if r["Valor de plano"] == "Plano detalle" and not caso:
                    s -= 2.0
                if r["Categoría"] == "Evento / feria" and not caso:
                    s -= 3.0
                if re.search(r"fachada|exterior|logotipo|vacia|vacio|cajas|puertos|camara web|monitor de control", info) and not caso:
                    s -= 3.0
                if re.search(r"estudio de television|interfaz de control|camara onescreen|snapcam|ms10|webcam|altavoz|microfono|aula vacia|sala vacia|vacio|vacia|configuracion|informacion del sistema|version de android|vista general de la oficina|columna vertebral|anatom|hueso|vertebr|cirug|dental|paciente", info) and not caso and not tema.get("salud"):
                    continue
                if 0 < relax < 3 and not re.search(r"interactua|escribe|escribiendo|toca|usando|trabaj|dibuja|usa ", info):
                    continue
                s += (num(r["Calidad (1-5)"]) - 4) * 0.8
                s -= 1.0 * usados_tanda.get(r["ID"], 0)
                s -= 0.4 * num(r["# de usos"] or 0) ** 0.5
                if usados_tanda.get(r["ID"], 0) >= 2 and relax < 3:
                    continue
                if ((m >= 1 and s >= 4.5) if not relax else (s >= (2.0 if relax < 3 else -1.5) and "OneScreen" in r["Producto"] and (relax >= 2 or r["Lugar"] in tema.get("lugares", []) or r["Sector"] in tema.get("sectores", [])))) or (caso and s >= 4.5):
                    if ruta(r):
                        cands.append((s, r))
                    if (best is None or s > best[0]) and ruta(r):
                        best = (s, r); bw = (relax, sorted(q & f)[:6])
        if not best:
            plan.append(dict(n=n, t0=t0, t1=t1, id=None, texto=" ".join(w["text"] for w in tr)))
            continue
        s, r = best
        usados.add(r["ID"]); usados_tanda[r["ID"]] = usados_tanda.get(r["ID"], 0) + 1
        mm = num(r["Mejor momento (s)"])
        dur = num(r["Duración (s)"])
        ss = max(INI, min(mm - 0.4, dur - need - 0.2))
        _e = estable.mejor_ss(ruta(r), need, INI, dur, mm)          # momento sin movimiento de cámara (Cris 27-oct)
        if _e is not None:
            ss = max(INI, min(_e, dur - need - 0.2))
        if r["ID"] in fin:
            ss = fin[r["ID"]] + 0.1
        fin[r["ID"]] = ss + need
        why = dict(relax=bw[0], coincide=bw[1]); perfil = r["Perfil de color"]
        p = ruta(r)
        log = 1 if (("S-Log" in perfil) and not re.search(r"graded|_color|cuatro_looks", p, re.I)) else 0
        plan.append(dict(n=n, t0=t0, t1=t1, id=r["ID"], key=f'{r["ID"]}_{int(round(ss * 100))}', ruta=p, ss=round(ss, 2), need=round(need, 2), log=log, fx=0.5, score=round(s, 1),
                         why=why, texto=" ".join(w["text"] for w in tr), desc=r["Información adicional"][:110], lugar=r["Lugar"], prod=r["Producto"][:40], permisos=r["Permisos"]))
        if n_alt:
            plan[-1]["alts"] = []
            for sa, ra in sorted(cands, key=lambda c: -c[0]):
                if ra["ID"] == r["ID"] or any(a["id"] == ra["ID"] for a in plan[-1]["alts"]) or len(plan[-1]["alts"]) >= n_alt:
                    continue
                da, ma = num(ra["Duración (s)"]), num(ra["Mejor momento (s)"])
                ssa = max(INI, min(ma - 0.4, da - need - 0.2))
                ea = estable.mejor_ss(ruta(ra), need, INI, da, ma)
                if ea is not None:
                    ssa = max(INI, min(ea, da - need - 0.2))
                pa = ruta(ra); perfa = ra["Perfil de color"]
                plan[-1]["alts"].append(dict(id=ra["ID"], ruta=pa, ss=round(ssa, 2), need=round(need, 2), score=round(sa, 1), log=1 if (("S-Log" in perfa) and not re.search(r"graded|_color|cuatro_looks", pa, re.I)) else 0,
                                              desc=ra["Información adicional"][:110], lugar=ra["Lugar"], permisos=ra["Permisos"]))
    if n_alt:
        return cierre_t, plan
    out = BASE / pieza / "Proyecto"
    out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(cierre_t=cierre_t, planos=plan), open(out / "planos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sin = sum(1 for p in plan if not p["id"])
    print(pieza, "tramos", len(plan), "sin plano", sin, "cierre en", round(cierre_t, 2))


if __name__ == "__main__":
    piezas = sys.argv[1:] or list(SPECS)
    tanda = {}
    for pz in piezas:
        elegir(pz, tanda, set())
