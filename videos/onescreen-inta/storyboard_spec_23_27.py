"""SPEC del storyboard de INTA23.0003 e INTA27.0001 (28-oct-2026, proceso de 16 pasos, paso 9b).
Cada toma trae 3 opciones (planos de seleccion.py + al menos un motion de plantilla); la ★ es mi favorita. Los textos salen de lo que dice la voz.
INTA27: la voz no trae el extracto del caso; se inserta tras «no lo decimos nosotros» (extracto de Yolanda Velázquez, Areandina, clip 102494, 163,36-171,72 s) y los tiempos posteriores se corren.
uso: python -I storyboard_spec_23_27.py  -> SPEC en _inta_trabajo\\spec_sb_23_27.json
Luego:  python estudio-video/herramientas/storyboard.py SPEC SALIDA.html"""
import json
from pathlib import Path

B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
T = B / "_inta_trabajo"
alts = json.load(open(T / "alts_sb_23_27.json", encoding="utf-8"))
dirrows = {r["ID"]: r for r in json.load(open(T / "directorio_rows.json", encoding="utf-8"))}

EXT_ID, EXT_IN, EXT_OUT = "102494", 163.36, 171.72      # extracto Areandina (Yolanda)
GAP = 0.25
EXT_DUR = EXT_OUT - EXT_IN


LOTE = set()      # planos ya usados en otro video del lote (no se comparten)


def dur_clip(i):
    try:
        return float(str(dirrows[i]["Duración (s)"]).replace(",", "."))
    except Exception:
        return 0.0


# g = índices (base 1) de los tramos que se funden en la toma; m = motions [(plantilla, params)]; fav = "P1" | "P2" | "M1" | "M2"
P = {
"INTA23": dict(id="INTA23.0003", titulo="IA que responde desde lo que tú le diste (QuizWiz, SuprNotes y Gurú)", tomas=[
    dict(g=[1, 2], m=[("titular", dict(l1="Le pides a una IA", l2="que haga tu examen", tema="claro"))], fav="M1"),
    dict(g=[3], m=[("frase", dict(texto="Ella no estuvo en tu clase", clave="no estuvo", tema="claro"))], fav="M1"),
    dict(g=[4], m=[("titular", dict(l1="Saber lo que", l2="tú le enseñaste", tema="azul"))], fav="M1"),
    dict(g=[5], m=[("frase", dict(texto="Callada en lo demás", clave="callada", tema="azul"))], fav="M1"),
    dict(g=[6, 7], m=[("titular", dict(l1="Trabajan con las fuentes", l2="que tú les das", tema="azul"))], fav="M1"),
    dict(g=[8], m=[("frase", dict(texto="QuizWiz arma el examen", clave="QuizWiz", tema="azul"))], fav="M1"),
    dict(g=[9, 10], m=[("flujo", dict(nodos=["Tu PDF", "Tu enlace", "Foto de una página"], iconos=["doc", "globo", "pantalla"], titulo="A partir de", tema="claro"))], fav="M1"),
    dict(g=[11], m=[("frase", dict(texto="SuprNotes responde solo", clave="solo", tema="azul"))], fav="M1"),
    dict(g=[12], m=[("titular", dict(l1="Con lo que hay", l2="en tus fuentes", tema="claro"))], fav="M1"),
    dict(g=[13], m=[("tachado", dict(texto="Su tutor orienta sin revelar", tachado="las respuestas", tema="claro"))], fav="M1"),
    dict(g=[14], m=[("frase", dict(texto="Y Gurú", clave="Gurú", tema="verde"))], fav="P1",
         nota="Plano con la interfaz de Gurú (101066/101069); el verde del motion es solo para Gurú."),
    dict(g=[15], m=[("notificacion", dict(titulo="Gurú", texto="Te contesta con la fuente citada", hora="Respuesta", icono="chat", tema="verde"))], fav="M1"),
    dict(g=[16, 17], m=[("titular", dict(l1="Una IA que responde", l2="desde lo que le diste", tema="azul"))], fav="M1"),
], cta=dict(texto="Escríbenos", sub="y conversemos cómo se vería con los materiales de tu institución", tema="azul",
            nota="[REVISAR] «SuprNotes» sale escrito «SuperNotes» en Scribe; en pantalla va «SuprNotes». QuizWiz: la ficha dice 5 s y el guion de Cris «menos de un minuto»: no se muestra ninguna cifra.")),
"INTA27": dict(id="INTA27.0001", titulo="Quiénes somos: una pregunta de hace quince años (extracto Areandina)", tomas=[
    dict(g=[1, 2], m=[("titular", dict(l1="Una pregunta", l2="hace 15 años", tema="azul"))], fav="M1"),
    dict(g=[3, 4], m=[("titular", dict(l1="¿Y si una pantalla enseñara", l2="como una persona?", tema="claro"))], fav="M1"),
    dict(g=[5], m=[("frase", dict(texto="La seguimos respondiendo", clave="respondiendo", tema="azul"))], fav="M1"),
    dict(g=[6, 7], m=[("cifra", dict(valor="+50", etiqueta="países: colegios, universidades y empresas", tema="azul"))], fav="M1",
         nota="«más de 50 países»: la presentación interna dice «más de 70»; se dejó 50, por debajo de la real."),
    dict(g=[8], extra=GAP, m=[("frase", dict(texto="Esto no lo decimos nosotros", clave="nosotros", tema="claro"))], fav="M1"),
    "EXTRACTO",
    dict(g=[9], m=[("frase", dict(texto="Amamos contar historias", clave="historias", tema="azul"))], fav="M1"),
    dict(g=[10], m=[("titular", dict(l1="La de tu institución", l2="puede ser la siguiente", tema="azul"))], fav="M1"),
], cta=dict(texto="Escríbenos y armamos tu proyecto", sub="si tu institución es la siguiente historia", tema="azul",
            nota="[REVISAR: permiso y vigencia] del extracto de Areandina (el clip exige aprobación del cliente).")),
}


def opcion_plano(c, a, b, nota=""):
    o = dict(tipo="plano", plano=c["id"], ruta=c["ruta"], plano_in=round(c["ss"], 2), plano_out=round(c["ss"] + (b - a), 2), log=bool(c.get("log")))
    n = [x for x in (nota, "requiere aprobación del cliente" if "aprobaci" in (c.get("permisos") or "") else "", c.get("desc", "")[:90]) if x]
    o["nota"] = " · ".join(n)
    return o


def candidatos(plan, grupo, a, b):
    out, vistos = [], set(LOTE)
    for gi in grupo:
        e = plan[gi - 1]
        for x in ([e] if e.get("id") else []) + e.get("alts", []):
            if x["id"] in vistos:
                continue
            if dur_clip(x["id"]) and x["ss"] + (b - a) > dur_clip(x["id"]) - 0.2:
                continue
            vistos.add(x["id"])
            out.append(x)
    return out


def relleno(pr, usadas):
    tx = pr.get("texto") or (pr.get("l1", "") + " " + pr.get("l2", "")).strip() or " ".join(str(v) for k, v in pr.items() if k in ("valor", "etiqueta", "titulo") and v) or "OneScreen"
    w = tx.split()
    tema = pr.get("tema", "claro")
    if "frase" not in usadas and len(w) <= 4:
        return dict(tipo="motion", plantilla="frase", params=dict(texto=tx, clave=w[-1].strip(".,?!"), tema=tema))
    h = max(1, len(w) // 2)
    return dict(tipo="motion", plantilla="titular", params=dict(l1=" ".join(w[:h]), l2=" ".join(w[h:]) or tx, tema=tema))


def construir():
    videos = []
    for pieza, d in P.items():
        plan = alts[pieza]
        voz = B / pieza / "Voz"
        scribe = json.load(open(voz / f"{pieza}_voz_scribe.json", encoding="utf-8"))
        fin_voz = scribe.get("audio_duration_secs") or scribe["words"][-1]["end"]
        cierre_t = max(p["t1"] for p in plan)
        shift = 0.0
        tomas, usados = [], set()
        for tm in d["tomas"]:
            k = len(tomas) + 1
            if tm == "EXTRACTO":
                a = tomas[-1]["t1"]
                b = a + EXT_DUR
                shift += GAP + EXT_DUR + GAP - GAP       # el hueco antes del extracto ya está contado en la toma anterior (extra)
                r = dirrows[EXT_ID]
                ruta = r["Ruta en disco"].split("\n")[0].strip()
                ops = [dict(tipo="plano", plano=EXT_ID, ruta=ruta, plano_in=EXT_IN, plano_out=EXT_OUT, log=False, fav=True,
                            nota="Yolanda Velázquez (coordinadora de innovación tecnológica, Areandina), a cámara con su propia voz: «…One Screen tiene complementos de todo y son unas pantallas muy intuitivas y que a la gente le ha gustado.» · requiere aprobación del cliente"),
                       dict(tipo="plano", plano="102418", ruta=alts_ruta("102418", plan), plano_in=4.6, plano_out=round(4.6 + EXT_DUR, 2), log=True,
                            nota="Su voz se oye sobre un apoyo de aula de Areandina (sin verla en cámara) · requiere aprobación del cliente"),
                       dict(tipo="motion", plantilla="cita_tarjeta", params=dict(texto="One Screen tiene complementos de todo y son unas pantallas muy intuitivas.", autor="Coordinación de innovación tecnológica, Areandina", tema="explicar"))]
                tomas.append(dict(id=f"S{k:02d}", t0=round(a, 2), t1=round(b, 2), voz="(extracto del caso, su voz) «…No, One Screen tiene complementos de todo y es unas pantallas muy intuitivas y que a la gente le ha gustado.»", opciones=ops))
                shift += GAP   # pausa tras el extracto
                continue
            a = plan[tm["g"][0] - 1]["t0"] + shift
            b = plan[tm["g"][-1] - 1]["t1"] + shift + tm.get("extra", 0)
            texto = " ".join(plan[i - 1]["texto"] for i in tm["g"])
            ps = candidatos(plan, tm["g"], a - shift, b - shift - tm.get("extra", 0))
            n_m = len(tm["m"])
            ops = [opcion_plano(c, a, b) for c in ps[: 3 - n_m]]
            mot = [dict(tipo="motion", plantilla=pl, params=params) for pl, params in tm["m"]]
            while len(ops) + len(mot) < 3:
                mot.append(relleno(tm["m"][0][1], {m_["plantilla"] for m_ in mot}))
            todas = ops + mot
            idx = {"P1": 0, "P2": 1, "M1": len(ops), "M2": len(ops) + 1}[tm["fav"]]
            idx = min(idx, len(todas) - 1)
            todas[idx]["fav"] = True
            for p_ in ps[: 3 - n_m]:
                usados.add(p_["id"])
            if tm.get("nota"):
                todas[idx]["nota"] = (todas[idx].get("nota", "") + " · " if todas[idx].get("nota") else "") + tm["nota"]
            tomas.append(dict(id=f"S{k:02d}", t0=round(a, 2), t1=round(b, 2), voz=texto, opciones=todas))
        c = d["cta"]
        ct = cierre_t + shift
        fv = fin_voz + shift
        pool = [x for e in plan for x in e.get("alts", [])]
        cp = []
        for x in pool:
            if x["id"] in usados or x["id"] in LOTE or any(o["id"] == x["id"] for o in cp) or (dur_clip(x["id"]) and x["ss"] + (fv - ct) > dur_clip(x["id"]) - 0.2):
                continue
            cp.append(x)
        ops = [opcion_plano(x, ct, fv, "el texto del CTA va sobre este plano, con la intro de marca al final") for x in cp[:2]]
        ops.append(dict(tipo="motion", plantilla="cta", params=dict(texto=c["texto"], sub=c["sub"], tema=c["tema"])))
        while len(ops) < 3:
            ops.append(relleno(dict(texto=c["texto"], tema=c["tema"]), {o["plantilla"] for o in ops if o["tipo"] == "motion"}))
        ops[0]["fav"] = True
        ops[0]["nota"] = (ops[0].get("nota", "") + " · " + c["nota"]).strip(" ·")
        voz_cta = " ".join(w["text"] for w in scribe["words"] if w.get("type") == "word" and w["start"] >= cierre_t - 0.01)
        tomas.append(dict(id=f"S{len(tomas) + 1:02d}", t0=round(ct, 2), t1=round(fv, 2), voz=voz_cta, opciones=ops))
        for t_ in tomas:
            LOTE.update(o["plano"] for o in t_["opciones"] if o.get("tipo") == "plano" and o.get("plano") != EXT_ID)
        videos.append(dict(id=d["id"], titulo=d["titulo"], meta="16:9 · voz Hale (Cristian Sánchez → voz a voz) · storyboard v1", tomas=tomas))
    return dict(videos=videos)


def alts_ruta(i, plan):
    for e in plan:
        for x in [e] + e.get("alts", []):
            if x.get("id") == i:
                return x["ruta"]
    return dirrows[i]["Ruta en disco"].split("\n")[0].strip()


if __name__ == "__main__":
    spec = construir()
    out = T / "spec_sb_23_27.json"
    json.dump(spec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for v in spec["videos"]:
        print(v["id"], len(v["tomas"]), "tomas; <1,5 s:", [t["id"] for t in v["tomas"] if t["t1"] - t["t0"] < 1.5])
    print(out)
