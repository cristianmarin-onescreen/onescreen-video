"""SPEC del storyboard v1 de INTA41.0001 (29-oct). Planos vistos en las hojas de contacto (Storyboard\\col_*.jpg y pool_*.jpg):
material de colegios con OneScreen, sobre todo el caso Colegio San Mateo (Cris, 29-oct) y casos de colegios desde 2024. Motion: motion_inta41.py.
uso: python spec_inta41.py  -> Storyboard\\SPEC_v1.json"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import seleccion as S
from motion_inta41 import motion, SB

BYID = {r["ID"]: r for r in S.rows}
POOL = {**json.load(open(SB / "pool_INTA41.json", encoding="utf-8")), **json.load(open(SB / "pool_colegios.json", encoding="utf-8"))}
W = [w for w in json.load(open(SB.parent / "Voz" / "aprobada" / "INTA41_voz_scribe.json", encoding="utf-8"))["words"] if w.get("type") == "word"]

# id, t0, t1, [(plano, por qué sirve)], favorita (0-2 plano A-C, 3-4 motion D-E)
TOMAS = [
 ("S01", 0.00, 1.78, [("100923", "persona de traje recorre el pasillo de un colegio: el padre que recorre"), ("102364", "estudiantes y docente recorren el pasillo exterior del colegio"), ("104638", "travelling por un pasillo de colegio con carteles")], 0),
 ("S02", 1.78, 4.64, [("100922", "travelling que entra a un salón y termina en la pantalla: lo que ve en los salones"), ("104655", "recepción del Colegio San Mateo (caso de éxito)"), ("102344", "salón moderno con la OneScreen al fondo")], 0),
 ("S03", 4.64, 6.80, [("102369", "aula con la OneScreen al frente: salón moderno"), ("105903", "aula del Colegio Caldas con la pantalla mostrando gráficas"), ("104632", "salón del San Mateo con la OneScreen al fondo")], 0),
 ("S04", 6.80, 8.58, [("102387", "la pantalla interactiva encendida y alguien la usa"), ("102391", "OneScreen T7 sobre su soporte en un aula"), ("104630", "aula del San Mateo con la T7 montada")], 0),
 ("S05", 8.58, 11.08, [("102800", "estudiantes escriben en la pantalla: es pizarra"), ("104645", "alumnos ven un video en la pantalla: es proyector"), ("105908", "altavoz sobre la pantalla: es sonido")], 3),
 ("S06", 11.08, 12.92, [("104650", "docente del San Mateo escribe y explica sobre la pantalla"), ("102794", "docente y estudiante muestran un simulador en la pantalla"), ("102343", "docente muestra una plataforma en la pantalla")], 0),
 ("S07", 12.92, 14.46, [("104604", "docente explica tocando la pantalla frente a sus estudiantes"), ("102342", "docente explica una simulación en la pantalla"), ("104609", "docente da la clase con la pantalla a un grupo pequeño")], 0),
 ("S08", 14.46, 16.42, [("102721", "Lessn en pantalla («Enseña como quieras»): la IA que prepara la clase"), ("100372", "Lessn en pantalla grande: «Your next great Lessn»"), ("102723", "Lessn: el docente arma una clase en la pantalla")], 0),
 ("S09", 16.42, 18.00, [("104634", "logo OneScreen en la pantalla del San Mateo"), ("106410", "la pantalla arranca con el logo OneScreen"), ("101685", "detalle del logo OneScreen en el marco")], 0),
 ("S10", 18.00, 19.88, [("104611", "niños del San Mateo usan la T7"), ("104610", "niña interactúa con la pantalla en el aula"), ("102795", "estudiante y profesor trabajan en un circuito en la pantalla")], 3),
 ("S11", 19.88, 21.68, [("104608", "docente y estudiantes interactúan con la pantalla"), ("102796", "docentes interactúan con simulaciones"), ("104605", "docente explica frente a la pantalla, estudiantes de espaldas")], 3),
 ("S12", 21.68, 23.28, [("102799", "tres estudiantes dibujan en la pantalla"), ("105895", "estudiantes entran al aula con la pantalla encendida"), ("104606", "estudiante juega un juego educativo en la pantalla")], 3),
 ("S13", 23.28, 24.92, [("104643", "estudiantes ven contenido multimedia en la pantalla"), ("105904", "aula del Colegio Caldas con la pantalla encendida"), ("104628", "docente da la clase guiándose de la pantalla")], 3),
 ("S14", 24.92, 27.14, [("101026", "personal de OneScreen instala y desempaca la pantalla: la instalación"), ("101023", "técnico arma el soporte de la pantalla"), ("106158", "se configura la pantalla nueva")], 0),
 ("S15", 27.14, 30.32, [("105912", "fachada y patio del Colegio Caldas con estudiantes que entran"), ("104615", "fachada del San Mateo (St. Matthew)"), ("100938", "fachada de Eight Academy")], 0),
 ("S16", 30.32, 32.04, [("102379", "entrada de un colegio con niños caminando"), ("105918", "estudiantes en las escaleras del Colegio Caldas"), ("102363", "estudiantes caminan por el colegio")], 3),
 ("S17", 32.04, 35.28, [("104651", "docente del San Mateo explica con la pantalla y un libro: el CTA va en texto sobre este plano"), ("105896", "estudiante y profesor frente a la pantalla"), ("104633", "aula del San Mateo con la pantalla al fondo")], 0),
 ("S18", 35.28, 38.34, [("105905", "aula del Colegio Caldas con la pantalla al fondo"), ("102382", "pantalla OneScreen en una sala vacía")], 3),
]


def plano(i, dur, nota):
    f = POOL[i]
    d = S.num(BYID[i]["Duración (s)"])
    a = max(0.3, min(f["ss"], d - dur - 0.15))
    extra = " · caso de éxito San Mateo (2023, exento de la regla de 2024)" if 104603 <= int(i) <= 104660 else ""
    if "aprobaci" in (BYID[i]["Permisos"] or ""):
        extra += " · requiere aprobación del cliente"
    if "Menores" in (BYID[i]["Permisos"] or ""):
        extra += " · menores en cámara"
    return dict(tipo="plano", plano=i, ruta=f["ruta"], plano_in=round(a, 2), plano_out=round(a + dur, 2), log=bool(f.get("log")), nota=nota + extra)


M = motion()
tomas = []
for tid, t0, t1, pls, fav in TOMAS:
    dur = t1 - t0
    ops = [plano(i, dur, n) for i, n in pls] + M[tid]
    k = fav if fav < 3 else len(pls) + fav - 3
    ops[k]["fav"] = True
    voz = " ".join(w["text"] for w in W if t0 - 0.05 <= w["start"] < t1 - 0.05).replace("Onescreen", "OneScreen").replace("onescreenlatam", "onescreenlatam")
    tomas.append(dict(id=tid, t0=t0, t1=t1, voz=voz, opciones=ops))
spec = {"videos": [dict(id="INTA41.0001", titulo="Renta TOFU 1: lo que ven los padres en tus salones", meta="16:9 · voz Hale aprobada · 38,3 s · música MASTER_Inspired and Uplifting Hip Hop_1", tomas=tomas)]}
out = SB / "SPEC_v1.json"
json.dump(spec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, len(tomas), "tomas")
