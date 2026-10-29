"""SPEC del storyboard v2 de INTA23.0004 e INTA27.0002 (28-oct-2026, voz regenerada y aprobada por Cris: INTA23 v0005, INTA27 v0001).
5 opciones por toma: 3 planos (A-C, vistos en hoja de contacto y repartidos sin repetir en el lote con asignar_lote.py) + 2 motion designs (D-E). Favorita = fav.
Planos: lote_v2.json (asignar_lote); tomas por frase (tiempos de la voz nueva). INTA27: extracto Areandina tras «nosotros» (voz_compuesta_27.py, T1=16,35).
uso: python -I storyboard_spec_23_27_v2.py -> _inta_trabajo\\spec_sb_23_27_v2.json"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import seleccion as S

B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre"); T = B / "_inta_trabajo"
BYID = {r["ID"]: r for r in S.rows}
lote = json.load(open(T / "lote_v2.json", encoding="utf-8"))
FICHA = {f["id"]: f for o in lote.values() for fs in o["tomas"] + o["cta"] for f in fs}
EXT = dict(id="102494", a=163.36, b=171.72); GAP = 0.25; EXT_DUR = EXT["b"] - EXT["a"]; T1 = 16.35


def ficha(i, dur):
    f = FICHA.get(i)
    d = S.num(BYID[i]["Duración (s)"])
    if not f or f["ss"] + dur > d - 0.2:
        f = S.ficha_plano(BYID[i], dur + 0.2)
    return f


def plano(i, dur, nota=""):
    f = ficha(i, dur)
    n = " · ".join(x for x in (nota, "requiere aprobación del cliente" if "aprobaci" in (BYID[i]["Permisos"] or "") else "", BYID[i]["Información adicional"][:90]) if x)
    return dict(tipo="plano", plano=i, ruta=f["ruta"], plano_in=round(f["ss"], 2), plano_out=round(f["ss"] + dur, 2), log=bool(f.get("log")), nota=n)


# (t0, t1, planos [ids], motions [(plantilla, params)], índice de la favorita (0-2 planos, 3-4 motion), nota)
V23 = [
 (0.0, 3.36, ["102710", "106294", "100373"], [("titular", dict(l1="Le pides a una IA", l2="que haga tu examen", tema="claro")), ("frase", dict(texto="¿Y el examen?", clave="examen", tema="azul"))], 0, ""),
 (3.36, 5.14, ["101049", "105906", "101197"], [("frase", dict(texto="Ella no estuvo en tu clase", clave="no estuvo", tema="claro")), ("tachado", dict(texto="Una IA que", tachado="no estuvo en tu clase", tema="claro"))], 3, ""),
 (5.14, 7.64, ["105902", "100883", "106034"], [("titular", dict(l1="Que sepa lo que", l2="tú le enseñaste", tema="azul")), ("flujo", dict(nodos=["Tu clase", "Tus fuentes", "La IA"], iconos=["persona", "doc", "chat"], titulo="Lo que le enseñaste", tema="claro"))], 0, ""),
 (7.64, 9.44, ["100763", "101196", "102607"], [("frase", dict(texto="Callada en lo demás", clave="callada", tema="azul")), ("tachado", dict(texto="Lo demás", tachado="se queda callada", tema="claro"))], 3, ""),
 (9.44, 12.9, ["106423", "101881", "102605"], [("chips", dict(centro=["Tus", "fuentes"], items=[dict(icono="doc", texto="Tu PDF"), dict(icono="globo", texto="Tu enlace"), dict(icono="pantalla", texto="Tu foto")], tema="azul")), ("titular", dict(l1="Trabajan con las fuentes", l2="que tú les das", tema="azul"))], 4, ""),
 (12.9, 14.8, ["100375", "101249", "101571"], [("frase", dict(texto="QuizWiz arma el examen", clave="QuizWiz", tema="azul")), ("notificacion", dict(titulo="QuizWiz", texto="Tu examen está listo", hora="Ahora", icono="check", tema="azul"))], 0, "Único plano del Directorio con QuizWiz en pantalla."),
 (14.8, 17.52, ["104729", "100876", "106396"], [("flujo", dict(nodos=["Tu PDF", "Tu enlace", "Foto de una página"], iconos=["doc", "globo", "pantalla"], titulo="A partir de", tema="claro")), ("checklist", dict(items=["Tu PDF", "Tu enlace", "La foto de una página"], titulo="Tus fuentes", tema="claro"))], 3, "Los planos solo ilustran navegar/enlace; PDF y foto no se filmaron: por eso la favorita es el motion."),
 (17.52, 20.28, ["106289", "101581", "102690"], [("frase", dict(texto="SuprNotes responde solo", clave="solo", tema="azul")), ("titular", dict(l1="Con lo que hay", l2="en tus fuentes", tema="claro"))], 4, "[REVISAR] en pantalla va «SuprNotes»; la voz dice «Supr Nouts»."),
 (20.28, 22.94, ["106357", "106425", "101941"], [("tachado", dict(texto="Su tutor orienta sin revelar", tachado="las respuestas", tema="claro")), ("notificacion", dict(titulo="Tutor", texto="¿Qué dice tu fuente?", hora="Pista", icono="chat", tema="azul"))], 3, ""),
 (22.94, 25.08, ["101070", "101940", "102599"], [("notificacion", dict(titulo="Gurú", texto="Te contesta con la fuente citada", hora="Respuesta", icono="chat", tema="verde")), ("frase", dict(texto="Y Gurú te contesta", clave="Gurú", tema="verde"))], 0, "Plano con la plataforma Gurú en pantalla; el verde del motion es solo para Gurú."),
 (25.08, 27.78, ["100394", "106298", "101200"], [("titular", dict(l1="Una IA que responde", l2="desde lo que le diste", tema="azul")), ("frase", dict(texto="Desde lo que le diste", clave="diste", tema="claro"))], 3, ""),
]
CTA23 = (27.78, None, ["100861", "102927", "101269"], [("cta", dict(texto="Escríbenos", sub="y conversemos cómo se vería con los materiales de tu institución", tema="azul")), ("frase", dict(texto="Conversemos", clave="Conversemos", tema="azul"))], 0, "El texto del CTA va sobre este plano, con la intro de marca al final.")

SH = GAP + EXT_DUR + GAP     # corrimiento de la voz tras el extracto (voz_compuesta_27.py)
V27 = [
 (0.0, 2.68, ["102926", "100873", "106479"], [("titular", dict(l1="Una pregunta", l2="hace 15 años", tema="azul")), ("cifra", dict(valor="15", etiqueta="años con una sola pregunta", tema="azul"))], 0, ""),
 (2.68, 4.42, ["106005", "106411", "101870"], [("frase", dict(texto="Todavía la respondemos", clave="respondemos", tema="azul")), ("titular", dict(l1="Seguimos", l2="respondiendo", tema="claro"))], 0, ""),
 (4.42, 6.68, ["106397", "100341", "104761"], [("titular", dict(l1="¿Y si una pantalla", l2="pudiera enseñar?", tema="claro")), ("frase", dict(texto="La pregunta era simple", clave="simple", tema="claro"))], 3, ""),
 (6.68, 9.06, ["100635", "106478", "102895"], [("comparacion", dict(izq="Una pantalla", der="Una persona que enseña", tema="claro")), ("frase", dict(texto="Enseñar como una persona", clave="persona", tema="azul"))], 0, ""),
 (9.06, 11.58, ["102929", "101062", "101939"], [("frase", dict(texto="Hasta hoy la seguimos respondiendo", clave="respondiendo", tema="azul")), ("linea", dict(puntos=["Colegios", "Universidades", "Empresas"], titulo="Hasta hoy", tema="claro"))], 0, ""),
 (11.58, 14.72, ["101029", "106306", "106438"], [("cifra", dict(valor="+50", etiqueta="países: colegios, universidades y empresas", tema="azul")), ("orbitas", dict(lineas=["Más de", "50 países"], iconos=["globo", "grupo", "pantalla"], tema="azul"))], 3, "«más de 50 países»: la presentación interna dice «más de 70»; se dejó 50, por debajo de la real."),
 (14.72, T1 + GAP, ["104995", "102924", "104730"], [("frase", dict(texto="Esto no lo decimos nosotros", clave="nosotros", tema="claro")), ("titular", dict(l1="Y esto no lo", l2="decimos nosotros", tema="claro"))], 3, ""),
 "EXTRACTO",
 (T1 + GAP + EXT_DUR, 18.82 + SH, ["101034", "102941", "100730"], [("frase", dict(texto="Amamos contar historias", clave="historias", tema="azul")), ("titular", dict(l1="Amamos contar", l2="historias", tema="azul"))], 3, ""),
 (18.82 + SH, 20.94 + SH, ["106169", "104731", "102942"], [("titular", dict(l1="La de tu institución", l2="puede ser la siguiente", tema="azul")), ("frase", dict(texto="La siguiente historia", clave="siguiente", tema="azul"))], 3, ""),
]
CTA27 = (20.94 + SH, None, ["106387", "101667", "105014"], [("cta", dict(texto="Escríbenos y armamos tu proyecto", sub="si tu institución es la siguiente historia", tema="azul")), ("frase", dict(texto="Armamos tu proyecto", clave="proyecto", tema="azul"))], 0, "[REVISAR: permiso y vigencia] del extracto de Areandina.")


def words(pz):
    f = B / pz / "Voz" / f"{pz}_voz_scribe.json"
    sc = json.load(open(f, encoding="utf-8"))
    return [w for w in sc["words"] if w.get("type") == "word"], sc.get("audio_duration_secs") or sc["words"][-1]["end"]


def toma(k, t0, t1, ws, planos, mots, fav, nota):
    dur = t1 - t0
    ops = [plano(i, dur) for i in planos] + [dict(tipo="motion", plantilla=p, params=pr) for p, pr in mots]
    ops[fav]["fav"] = True
    if nota:
        ops[fav]["nota"] = (ops[fav].get("nota", "") + " · " if ops[fav].get("nota") else "") + nota
    voz = " ".join(w["text"] for w in ws if t0 - 0.01 <= w["start"] < t1 - 0.01)
    return dict(id=f"S{k:02d}", t0=round(t0, 2), t1=round(t1, 2), voz=voz, opciones=ops)


def video(pz, vid, titulo, rows, cta):
    ws, fin = words(pz)
    tomas = []
    for r in rows:
        if r == "EXTRACTO":
            a = tomas[-1]["t1"]; b = a + EXT_DUR
            ruta = BYID[EXT["id"]]["Ruta en disco"].split("\n")[0].strip()
            ops = [dict(tipo="plano", plano=EXT["id"], ruta=ruta, plano_in=EXT["a"], plano_out=EXT["b"], log=False, fav=True,
                        nota="Yolanda Velázquez (coordinadora de innovación tecnológica, Areandina), a cámara con su propia voz: «…One Screen tiene complementos de todo y son unas pantallas muy intuitivas y que a la gente le ha gustado.» · requiere aprobación del cliente"),
                   plano("101119", EXT_DUR, "Su voz se oye sobre un apoyo de aula (sin verla en cámara)"), plano("102421", EXT_DUR, "Su voz se oye sobre un apoyo de aula (sin verla en cámara)"),
                   dict(tipo="motion", plantilla="cita_tarjeta", params=dict(texto="One Screen tiene complementos de todo y son unas pantallas muy intuitivas.", autor="Coordinación de innovación tecnológica, Areandina", tema="explicar")),
                   dict(tipo="motion", plantilla="frase", params=dict(texto="Unas pantallas muy intuitivas", clave="intuitivas", tema="azul"))]
            tomas.append(dict(id=f"S{len(tomas) + 1:02d}", t0=round(a, 2), t1=round(b, 2), voz="(extracto del caso, su voz) «…No, One Screen tiene complementos de todo y es unas pantallas muy intuitivas y que a la gente le ha gustado.»", opciones=ops))
            continue
        tomas.append(toma(len(tomas) + 1, r[0], r[1], ws, r[2], r[3], r[4], r[5]))
    tomas.append(toma(len(tomas) + 1, cta[0], fin, ws, cta[2], cta[3], cta[4], cta[5]))
    return dict(id=vid, titulo=titulo, meta="16:9 · voz regenerada (Cristian Sánchez → Hale) · storyboard v2", tomas=tomas)


if __name__ == "__main__":
    spec = dict(videos=[video("INTA23", "INTA23.0004", "IA que responde desde lo que tú le diste (QuizWiz, SuprNotes y Gurú)", V23, CTA23),
                        video("INTA27", "INTA27.0002", "Quiénes somos: una pregunta de hace quince años (extracto Areandina)", V27, CTA27)])
    usados = {}
    for v in spec["videos"]:
        for t in v["tomas"]:
            for o in t["opciones"]:
                if o["tipo"] == "plano" and o["plano"] != EXT["id"]:
                    usados.setdefault(o["plano"], []).append((v["id"], t["id"]))
        print(v["id"], len(v["tomas"]), "tomas; <1,5 s:", [t["id"] for t in v["tomas"] if t["t1"] - t["t0"] < 1.5])
    print("repetidos en el lote:", {k: x for k, x in usados.items() if len(x) > 1})
    json.dump(spec, open(T / "spec_sb_23_27_v2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
