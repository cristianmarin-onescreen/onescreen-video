"""SPEC del storyboard de INTA20, INTA21 e INTA22 (28-oct-2026, proceso de 16 pasos, paso 9b).
Cada toma trae 3 opciones: planos (el que ya había + alternativas de seleccion.py, validados mirando el fotograma contra la frase) y al menos un motion de plantilla.
Los textos de los motion salen solo de lo que dice la voz. uso: python -I storyboard_spec_20_22.py  -> SPEC en _inta_trabajo\\spec_sb_20_22.json
Luego:  python estudio-video/herramientas/storyboard.py SPEC SALIDA.html"""
import json
from pathlib import Path

B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
T = B / "_inta_trabajo"
alts = json.load(open(T / "alts_sb_20_22.json", encoding="utf-8"))
dirrows = {r["ID"]: r for r in json.load(open(T / "directorio_rows.json", encoding="utf-8"))}


def dur_clip(i):
    try:
        return float(str(dirrows[i]["Duración (s)"]).replace(",", "."))
    except Exception:
        return 0.0


# --- por pieza: lista de tomas. g = índices (base 1) de los tramos de planos.json que se funden en la toma; quitar = planos descartados al mirar el fotograma;
# m = motions [(plantilla, params)]; fav = "P1" | "P2" | "M1" | "M2" (cuál lleva la ★). nota = aviso honesto para Cris.
def ic(*a):
    return list(a)


P = {
"INTA20": dict(titulo="Renta 3 · la tecnología de hace cinco años", tomas=[
    dict(g=[1], m=[("frase", dict(texto="La misma tecnología", clave="tecnología", tema="claro"))], fav="P1"),
    dict(g=[2], m=[("cifra", dict(valor="5 años", etiqueta="desde que compraste esa pantalla", tema="claro"))], fav="M1"),
    dict(g=[3], m=[("titular", dict(l1="Esa pantalla", l2="ya no es la de hoy", tema="azul"))], fav="M1"),
    dict(g=[4], m=[("frase", dict(texto="Renting o leasing", clave="leasing", tema="azul"))], fav="M1"),
    dict(g=[5, 6], m=[("notificacion", dict(titulo="Tus equipos", texto="Llegan actualizados", hora="Con renting o leasing", icono="pantalla", tema="azul"))], fav="P1"),
    dict(g=[7], m=[("flujo", dict(nodos=["Termina el contrato", "Se renueva la tecnología"], iconos=["doc", "pantalla"], titulo="Con leasing", tema="azul"))], fav="M1"),
    dict(g=[8], m=[("frase", dict(texto="Gurú Plus", clave="Gurú", tema="verde")), ("pantalla", dict(titulo="Gurú Plus", lineas=["Todo el contrato"], tema="verde"))], fav="P1",
         nota="Plano con la interfaz de Gurú (101069). Para el motion, el verde es solo Gurú."),
    dict(g=[9], m=[("notificacion", dict(titulo="Gurú Plus", texto="Actualizaciones de software", hora="Durante todo el contrato", icono="pantalla", tema="verde"))], fav="M1"),
    dict(g=[10], m=[("frase", dict(texto="Así, tu espacio", clave="espacio", tema="azul")), ("hub", dict(centro="Tu espacio", satelites=["Equipos actualizados", "Software", "Renovación"], tema="azul"))], fav="P1"),
    dict(g=[11], m=[("tachado", dict(texto="Tu espacio no se queda con", tachado="lo que alcanzaste a comprar", tema="azul"))], fav="M1"),
], cta=dict(texto="Pide información con un asesor", sub="Cómo sería la renovación de tus equipos con cada modelo", tema="azul",
            nota="Guion: «Gurú Plus» lo escribió Scribe como «Guru Plus»; renovación solo en leasing.")),
"INTA21": dict(titulo="Renta 4 · una sola cuota, todo incluido", tomas=[
    dict(g=[1], m=[("frase", dict(texto="Compras una pantalla", clave="pantalla", tema="claro"))], fav="P1"),
    dict(g=[2], quitar=["105957"], m=[("tarjetas", dict(titulo="¿Quién…?", items=[dict(icono="persona", titulo="Instala", texto=""), dict(icono="pantalla", titulo="Mantiene", texto=""), dict(icono="auriculares", titulo="Da soporte", texto="")], tema="claro")),
                                       ("frase", dict(texto="¿Quién te instala?", clave="instala", tema="claro"))], fav="P1",
         nota="102643: personal técnico en una sala de reuniones; el Directorio no tiene un plano de soporte más literal."),
    dict(g=[3], m=[("titular", dict(l1="¿Y quién", l2="da soporte?", tema="azul"))], fav="M1",
         nota="No hay plano literal de «soporte» en el Directorio; la ★ es el motion."),
    dict(g=[4], m=[("cifra", dict(valor="1", etiqueta="sola cuota mensual", tema="azul"))], fav="M1"),
    dict(g=[5], m=[("checklist", dict(titulo="Una sola cuota cubre", items=["La pantalla", "La instalación"], tema="claro"))], fav="M1"),
    dict(g=[6], m=[("flujo", dict(nodos=["El software", "El soporte Gurú Plus"], iconos=["pantalla", "auriculares"], titulo="También incluye", tema="verde"))], fav="P1"),
    dict(g=[7], m=[("frase", dict(texto="El mantenimiento", clave="mantenimiento", tema="azul"))], fav="M1",
         nota="Sin plano literal de mantenimiento."),
    dict(g=[8], m=[("titular", dict(l1="Llevamos los equipos", l2="hasta tu espacio", tema="azul"))], fav="M1",
         nota="101096 (dos personas sonriendo) no ilustra «llevamos»; no hay plano de entrega en el Directorio."),
    dict(g=[9], m=[("frase", dict(texto="Instalamos y capacitamos", clave="capacitamos", tema="claro")), ("flujo", dict(nodos=["Instalamos", "Capacitamos"], iconos=["pantalla", "grupo"], titulo="Y además", tema="azul"))], fav="P1"),
    dict(g=[10], m=[("titular", dict(l1="Tu equipo", l2="empieza a trabajar", tema="azul"))], fav="M1",
         nota="102898 (manos con marcadores) no tiene relación con la frase."),
    dict(g=[11], m=[("cifra", dict(valor="Día 1", etiqueta="desde el primer día", tema="claro"))], fav="M1"),
    dict(g=[12], m=[("frase", dict(texto="Si falla por dentro", clave="falla", tema="claro"))], fav="M1"),
    dict(g=[13], m=[("comparacion", dict(izq="La reparamos", der="La reemplazamos", tema="azul"))], fav="M1"),
    dict(g=[14, 15], m=[("titular", dict(l1="Sin costo adicional.", l2="Lo demás va por nuestra cuenta", tema="azul"))], fav="P1",
         nota="Toma fundida: «sin costo adicional» sola duraba 1,4 s (<1,5 s)."),
], cta=dict(texto="Pide tu cotización", sub="en menos de 24 horas, un especialista te dice tu cuota mensual y qué incluye", tema="azul",
            nota="[REVISAR] «menos de veinticuatro horas» es promesa de la web; confirmar con ventas.")),
"INTA22": dict(titulo="Empresas · la pizarra que no se borra (Write)", tomas=[
    dict(g=[1], m=[("frase", dict(texto="Al final de la reunión", clave="reunión", tema="claro"))], fav="P1"),
    dict(g=[2], m=[("pantalla", dict(titulo="Una foto a la pizarra", lineas=["para no perder lo escrito"], tema="claro"))], fav="P1",
         nota="106357: mujer con el celular en la mano frente a la pizarra."),
    dict(g=[3], m=[("tachado", dict(texto="Lo que se escribió", tachado="perderlo", tema="claro"))], fav="M1"),
    dict(g=[4], m=[("frase", dict(texto="Esto tiene arreglo", clave="arreglo", tema="azul"))], fav="M1"),
    dict(g=[5], m=[("frase", dict(texto="Una pantalla OneScreen", clave="OneScreen", tema="azul"))], fav="P1"),
    dict(g=[6], m=[("titular", dict(l1="La pizarra", l2="es infinita", tema="azul"))], fav="M1"),
    dict(g=[7], m=[("hub", dict(centro="Una pizarra", satelites=["Todo tu equipo", "Escribe a la vez", "En ella"], tema="azul"))], fav="P1"),
    dict(g=[8], quitar=["102931"], m=[("titular", dict(l1="Todos escriben", l2="a la vez", tema="azul"))], fav="M1",
         nota="Descartado 102931 (esqueleto/anatomía): no es la pizarra."),
    dict(g=[9], m=[("flujo", dict(nodos=["Pizarra", "PDF", "Imagen"], iconos=["pantalla", "doc", "doc"], titulo="La guardas en", tema="claro"))], fav="M1",
         nota="106397 (tienda de apps) no ilustra «guardar»."),
    dict(g=[10], quitar=["106005"], m=[("comparacion", dict(izq="Tu Drive", der="Tu OneDrive", tema="claro"))], fav="M1"),
    dict(g=[11], m=[("frase", dict(texto="Con un código QR", clave="QR", tema="claro"))], fav="P1"),
    dict(g=[12], m=[("frase", dict(texto="Nadie borra nada", clave="Nadie", tema="azul"))], fav="M1"),
    dict(g=[13], quitar=["104729"], m=[("titular", dict(l1="Nadie tiene", l2="que acordarse", tema="azul"))], fav="M1"),
], cta=dict(texto="Escríbenos por WhatsApp", sub="y te mostramos todo lo que trae la pizarra de la OneScreen T7 para empresas", tema="azul",
            nota="[FALTA DATO] URL de la ficha T7 Empresas.")),
}


def relleno(pr, usadas):
    """segundo motion con las mismas palabras de la voz, en otra plantilla (titular partido en 2 líneas o frase con la última palabra como clave)"""
    tx = pr.get("texto") or (pr.get("l1", "") + " " + pr.get("l2", "")).strip()
    w = tx.split()
    tema = pr.get("tema", "claro")
    if "frase" not in usadas and len(w) <= 4:
        return dict(tipo="motion", plantilla="frase", params=dict(texto=tx, clave=w[-1].strip(".,?!"), tema=tema))
    h = max(1, len(w) // 2)
    return dict(tipo="motion", plantilla="titular", params=dict(l1=" ".join(w[:h]), l2=" ".join(w[h:]) or tx, tema=tema))


def opcion_plano(c, a, b, nota=""):
    o = dict(tipo="plano", plano=c["id"], ruta=c["ruta"], plano_in=round(c["ss"], 2), plano_out=round(c["ss"] + (b - a), 2), log=bool(c.get("log")))
    n = [x for x in (nota, "requiere aprobación del cliente" if "aprobaci" in (c.get("permisos") or "") else "", c.get("desc", "")[:90]) if x]
    o["nota"] = " · ".join(n)
    return o


def candidatos(pieza, grupo, a, b, quitar):
    """planos de los tramos del grupo (el actual y sus alternativas), que alcancen para la duración de la toma"""
    cur = json.load(open(B / pieza / "Proyecto" / "planos.json", encoding="utf-8"))["planos"]
    out, vistos = [], set(quitar)
    for gi in grupo:
        i = gi - 1
        c = [cur[i]] if i < len(cur) and cur[i].get("id") else []
        for x in c + alts[pieza][i].get("alts", []):
            if x["id"] in vistos:
                continue
            if dur_clip(x["id"]) and x["ss"] + (b - a) > dur_clip(x["id"]) - 0.2:
                continue
            vistos.add(x["id"])
            out.append(x)
    return out


def cierre_planos(pieza, usados, a, b):
    """dos planos para el CTA (texto sobre plano): los alternativos que no se usan en la pieza y alcanzan para la duración"""
    pool = [x for al in alts[pieza] for x in al.get("alts", [])]
    out = []
    for x in pool:
        if x["id"] in usados or any(o["id"] == x["id"] for o in out):
            continue
        if dur_clip(x["id"]) and x["ss"] + (b - a) > dur_clip(x["id"]) - 0.2:
            continue
        out.append(x)
    return out[:2]


def construir():
    videos = []
    for pieza, d in P.items():
        scribe = json.load(open(B / pieza / "Voz" / f"{pieza}_voz_scribe.json", encoding="utf-8"))
        fin_voz = scribe.get("audio_duration_secs") or scribe["words"][-1]["end"]
        cur = json.load(open(B / pieza / "Proyecto" / "planos.json", encoding="utf-8"))
        tomas, usados = [], set()
        for k, tm in enumerate(d["tomas"], 1):
            a = alts[pieza][tm["g"][0] - 1]["t0"]
            b = alts[pieza][tm["g"][-1] - 1]["t1"]
            texto = " ".join(alts[pieza][i - 1]["texto"] for i in tm["g"])
            ps = candidatos(pieza, tm["g"], a, b, tm.get("quitar", []))
            n_m = len(tm["m"])
            ops = [opcion_plano(c, a, b) for c in ps[: 3 - n_m]]
            mot = []
            for pl, params in tm["m"]:
                mot.append(dict(tipo="motion", plantilla=pl, params=params))
            # si faltan planos, se completa con otro motion de OTRA plantilla (siempre 3 opciones)
            while len(ops) + len(mot) < 3:
                mot.append(relleno(tm["m"][0][1], {m_["plantilla"] for m_ in mot}))
            todas = ops + mot
            fav = tm["fav"]
            idx = {"P1": 0, "P2": 1, "M1": len(ops), "M2": len(ops) + 1}[fav]
            idx = min(idx, len(todas) - 1)
            todas[idx]["fav"] = True
            for p_ in ps[: 3 - n_m]:
                usados.add(p_["id"])
            if tm.get("nota"):
                todas[idx]["nota"] = (todas[idx].get("nota", "") + " · " if todas[idx].get("nota") else "") + tm["nota"]
            tomas.append(dict(id=f"S{k:02d}", t0=round(a, 2), t1=round(b, 2), voz=texto, opciones=todas))
        # CTA: texto sobre plano (dos opciones) o tarjeta de cierre (motion)
        cierre_t = cur["cierre_t"]
        cp = cierre_planos(pieza, usados, cierre_t, fin_voz)
        c = d["cta"]
        voz_cta = " ".join(w["text"] for w in scribe["words"] if w.get("type") == "word" and w["start"] >= cierre_t - 0.01)
        ops = [dict(opcion_plano(x, cierre_t, fin_voz, "el texto del CTA va sobre este plano, con la intro de marca al final")) for x in cp]
        ops.append(dict(tipo="motion", plantilla="cta", params=dict(texto=c["texto"], sub=c["sub"], tema=c["tema"])))
        while len(ops) < 3:
            ops.append(relleno(dict(texto=c["texto"], tema=c["tema"]), {o["plantilla"] for o in ops if o["tipo"] == "motion"}))
        ops[0]["fav"] = True
        ops[0]["nota"] = (ops[0].get("nota", "") + " · " + c["nota"]).strip(" ·")
        tomas.append(dict(id=f"S{len(tomas) + 1:02d}", t0=round(cierre_t, 2), t1=round(fin_voz, 2), voz=voz_cta, opciones=ops))
        videos.append(dict(id=f"{pieza}.0003", titulo=d["titulo"], meta="16:9 · voz Hale (aprobada) · storyboard v1", tomas=tomas))
    return dict(videos=videos)


if __name__ == "__main__":
    spec = construir()
    out = T / "spec_sb_20_22.json"
    json.dump(spec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for v in spec["videos"]:
        cortas = [t["id"] for t in v["tomas"] if t["t1"] - t["t0"] < 1.5]
        print(v["id"], len(v["tomas"]), "tomas; <1,5 s:", cortas, "| sin motion:", [t["id"] for t in v["tomas"] if not any(o["tipo"] == "motion" for o in t["opciones"])])
    print(out)
