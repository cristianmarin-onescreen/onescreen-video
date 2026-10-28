"""Registro de producción de video de OneScreen: ESPEJO local de la hoja maestra "Directorio - Producción de video"
(Sheet 1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks; ver estudio-video/registro/HOJA.md). Si la hoja y el espejo difieren, manda la hoja.
Arquitectura v2 (26-oct-2026): cuatro pestañas = cuatro CSV en estudio-video/registro/:
  guiones.csv (estrategia escribe; yo solo Estado y Versiones generadas), produccion.csv (mía), planner.csv (script del planner; solo lectura para mí),
  historico.csv (al cerrar versiones). Los CSV viejos (variaciones, publicaciones, resultados) están en registro/legacy/.

Comandos (desde la raíz del repo):
  registro.py guion INTA03                                          plan de producción desde un guion Aprobado (qué IDs crear, con qué datos); no escribe
  registro.py nueva INTA03 --nombre "..." --version v1 --hook H1 --eje Base --vertical INT --nivel N2 --cambio "..." [--basada ID] [--contenido C1] [--cta A1] [--voz neutro] [--planos 1,2] [--builder ruta]
  registro.py nombre RENT.0005 --formato 16x9 [--ext mp4]          nombre de archivo canónico
  registro.py preview RENT.0005 --link "chat + ruta local"          columna Preview (dónde verlo)
  registro.py decision RENT.0005 Aprobada [--comentarios "..."]    lo que Cris decidió (Aprobada | Con cambios | Rechazada); Aprobada => Estado Aprobada
  registro.py estado RENT.0005 Vigente [--nota "..."]
  registro.py ruta RENT.0005 [--local D:\\...] [--drive https://...] [--prproj D:\\...]
  registro.py usos RENT.0005                                        qué escribir en el Directorio maestro (# de usos y Usado en) al aprobar
  registro.py usos-hechos RENT.0005                                 marca la fecha en 'Usos marcados en el Directorio'
  registro.py cierres                                               versiones de Producción que ya deben moverse a Histórico (sección 6)
  registro.py cerrar RENT.0008 [--fecha 2026-10-26]                 arma la fila de Histórico (suma métricas 72 h del Planner) y la pasa en el ESPEJO; imprime la fila para la hoja
  registro.py importar guiones|produccion|planner|historico ARCHIVO.json   HOJA -> ESPEJO (JSON de get_values de la pestaña completa); lista las ACCIONES
  registro.py celdas RENT.0005 --fila 6 --campos estado,decision_cris,comentarios_cris,fecha_decision   ESPEJO -> HOJA, celda por celda
  registro.py pendientes | manifest | hoja | validar CARPETA
Convención de nombre: <PIEZA>.<NNNN>_<H#C#A#>_<voz>_<formato>[_preview].<ext>  p. ej. RENT.0005_H1C1A1_neutro_16x9_preview.mp4
Yo NUNCA escribo Planner ni columnas amarillas (decisión de Cris, hooks aprobados, comentarios, fecha de decisión, Qué vimos, Decisión, Próxima variación, Aprendizaje).
"""
import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

REG = Path(__file__).resolve().parents[1] / "registro"
GUIO, PROD, PLAN, HIST = (REG / "guiones.csv", REG / "produccion.csv", REG / "planner.csv", REG / "historico.csv")
_MET = ["alcance", "vistas", "retencion", "clics", "leads", "costo"]
CAMPOS = {
    GUIO: ["id_angulo", "vertical", "pilar", "nivel", "rol", "angulo", "hook1", "tipo_h1", "hook2", "tipo_h2", "hook3", "tipo_h3", "cuerpo_c1", "cta_a1", "formato_duracion",
           "otras_variantes", "estado", "fecha_propuesta", "decision_cris", "hooks_aprobados", "comentarios_cris", "fecha_decision", "versiones_generadas", "notas"],
    PROD: ["id", "pieza", "nombre_pieza", "version", "hook", "contenido", "cta", "eje_que_cambia", "basada_en", "voz_idioma", "formatos", "estado", "link_preview",
           "decision_cris", "comentarios_cris", "fecha_decision", "que_cambio", "fecha_creacion", "planos_usados_directorio", "usos_marcados_directorio", "prproj",
           "ruta_local", "link_drive_final", "usado", "usado_donde", "fecha_uso", "builder", "notas", "vertical", "nivel"],
    PLAN: ["id_pub", "id_version", "vertical", "nivel", "formato", "plataforma", "cuenta", "mercado", "uso", "copy_o_titulo", "utm_campaign", "utm_content", "fecha_programada",
           "estado", "fecha_publicada", "url", "publicado_por"] + [f"h{h}_{m}" for h in (24, 48, 72) for m in _MET] + ["que_vimos", "decision", "proxima_variacion", "notas"],
    HIST: ["id", "pieza", "nombre_pieza", "vertical", "nivel", "version", "hook", "contenido", "cta", "eje_que_cambia", "basada_en", "voz_idioma", "formatos", "estado_final",
           "fecha_creacion", "fecha_cierre", "que_cambio", "planos_usados", "export_drive", "publicada_en"] + [f"h72_{m}" for m in _MET] + ["decision", "aprendizaje", "builder", "notas"],
}
ESTADOS = ("Preview", "Aprobada", "Vigente", "Reemplazada", "Rechazada", "Archivada")
SALEN = ("Reemplazada", "Rechazada", "Archivada")
DECISIONES = ("Pendiente", "Aprobada", "Con cambios", "Rechazada")
FORMATOS = ("16x9", "9x16", "4x5", "1x1")
NOMBRE = re.compile(r"^(?P<id>[A-Z0-9]{2,8}\.\d{4})_(?P<var>H\d+C\d+A\d+)_(?P<voz>[a-z\-A-Z]+)_(?P<fmt>\d+x\d+)(?:_(?P<tipo>[a-z]+))?\.[A-Za-z0-9]+$")


def leer(p):
    if not p.exists():
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def escribir(p, filas):
    REG.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS[p], extrasaction="ignore")
        w.writeheader()
        for r in filas:
            w.writerow({k: r.get(k, "") for k in CAMPOS[p]})


def buscar(filas, vid, clave="id"):
    for r in filas:
        if r[clave] == vid:
            return r
    sys.exit(f"No existe {vid}")


def variacion_de(r):
    return f"{r['hook']}{r['contenido']}{r['cta']}"


def nombre_base(r):
    return f"{r['id']}_{variacion_de(r)}_{r['voz_idioma']}"


def num(s):
    try:
        return float(str(s).replace(".", "").replace(",", ".")) if s not in ("", None) else 0.0
    except ValueError:
        return 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("guion"); a.add_argument("id_angulo")
    a = sp.add_parser("nueva"); a.add_argument("pieza"); a.add_argument("--nombre", default=""); a.add_argument("--version", required=True)
    a.add_argument("--hook", default="H1"); a.add_argument("--contenido", default="C1"); a.add_argument("--cta", default="A1"); a.add_argument("--eje", default="Base")
    a.add_argument("--voz", default="neutro"); a.add_argument("--cambio", required=True); a.add_argument("--basada", default=""); a.add_argument("--planos", default="")
    a.add_argument("--builder", default=""); a.add_argument("--formatos", default="16x9, 9x16, 4x5"); a.add_argument("--vertical", default=""); a.add_argument("--nivel", default="")
    a = sp.add_parser("nombre"); a.add_argument("id"); a.add_argument("--formato", required=True, choices=FORMATOS); a.add_argument("--tipo", default=""); a.add_argument("--ext", default="mp4")
    a = sp.add_parser("preview"); a.add_argument("id"); a.add_argument("--link", required=True)
    a = sp.add_parser("decision"); a.add_argument("id"); a.add_argument("decision", choices=DECISIONES); a.add_argument("--comentarios", default=""); a.add_argument("--fecha", default=str(date.today()))
    a = sp.add_parser("estado"); a.add_argument("id"); a.add_argument("estado", choices=ESTADOS); a.add_argument("--nota", default="")
    a = sp.add_parser("ruta"); a.add_argument("id"); a.add_argument("--local", default=""); a.add_argument("--drive", default=""); a.add_argument("--prproj", default="")
    a = sp.add_parser("usos"); a.add_argument("id")
    a = sp.add_parser("usos-hechos"); a.add_argument("id"); a.add_argument("--fecha", default=str(date.today()))
    sp.add_parser("cierres")
    a = sp.add_parser("cerrar"); a.add_argument("id"); a.add_argument("--fecha", default=str(date.today()))
    a = sp.add_parser("importar"); a.add_argument("pestana", choices=("guiones", "produccion", "planner", "historico")); a.add_argument("archivo")
    a = sp.add_parser("celdas"); a.add_argument("id"); a.add_argument("--fila", type=int, required=True, help="fila de la hoja (busca el ID en la columna A de Producción)"); a.add_argument("--campos", required=True, help="p. ej. estado,decision_cris,comentarios_cris,fecha_decision")
    sp.add_parser("pendientes"); sp.add_parser("manifest"); sp.add_parser("hoja")
    a = sp.add_parser("validar"); a.add_argument("carpeta")
    x = ap.parse_args()
    guio, prod, plan, hist = leer(GUIO), leer(PROD), leer(PLAN), leer(HIST)

    if x.cmd == "guion":
        g = buscar(guio, x.id_angulo, "id_angulo")
        if g["estado"] != "Aprobado" or g["decision_cris"] != "Aprobado":
            sys.exit(f"{x.id_angulo}: Estado={g['estado']!r}, Decisión de Cris={g['decision_cris']!r}. Solo se produce con Estado=Aprobado y Decisión=Aprobado")
        hooks = [h.strip() for h in g["hooks_aprobados"].split(",") if h.strip()] or [f"H{i}" for i in (1, 2, 3) if g[f"hook{i}"].strip()]
        faltan = [h for h in hooks if not g.get(f"hook{h[1:]}", "").strip()]
        if faltan or not g["cuerpo_c1"].strip() or not g["cta_a1"].strip():
            sys.exit(f"Falta texto en el guion (hooks sin texto: {faltan or 'ninguno'}; cuerpo: {'ok' if g['cuerpo_c1'].strip() else 'VACÍO'}; CTA: {'ok' if g['cta_a1'].strip() else 'VACÍA'}). No inventar: avisar a Cris")
        for h in hooks:
            if g.get(f"tipo_h{h[1:]}") == "Dato":
                print(f"AVISO: {h} es de tipo Dato: si trae una cifra sin fuente, NO producir y avisar")
        n = max([int(r["id"].split(".")[1]) for r in prod + hist if r["id"].startswith(x.id_angulo + ".")] or [0])
        print(f"Pieza {x.id_angulo} | nombre: {g['angulo']} | vertical {g['vertical']} nivel {g['nivel']} | voz neutro | formatos 16x9, 9x16, 4x5 | estado inicial Preview, versión v1")
        base = None
        for i, h in enumerate(hooks):
            vid = f"{x.id_angulo}.{n + 1 + i:04d}"
            base = base or vid
            print(f"  {vid}: Hook {h} C1 A1 | eje {'Base' if i == 0 else 'Hook'} | basada en {'' if i == 0 else base}")
        print("Luego: en Guiones solo Estado='En producción' y 'Versiones generadas (IDs)'.")
    elif x.cmd == "nueva":
        n = [int(r["id"].split(".")[1]) for r in prod + hist if r["id"].startswith(x.pieza + ".")]
        nombre = x.nombre or next((r["nombre_pieza"] for r in prod if r["pieza"] == x.pieza), "")
        if not nombre:
            sys.exit("Pieza nueva: pasa --nombre")
        vid = f"{x.pieza}.{(max(n) + 1) if n else 1:04d}"
        prod.append(dict(id=vid, pieza=x.pieza, nombre_pieza=nombre, version=x.version, hook=x.hook, contenido=x.contenido, cta=x.cta, eje_que_cambia=x.eje, basada_en=x.basada,
                         voz_idioma=x.voz, formatos=x.formatos, estado="Preview", decision_cris="Pendiente", que_cambio=x.cambio, fecha_creacion=str(date.today()),
                         planos_usados_directorio=x.planos, builder=x.builder, usado="", vertical=x.vertical, nivel=x.nivel))
        escribir(PROD, prod)
        print(vid, "->", nombre_base(prod[-1]) + "_<formato>[_preview].<ext>")
    elif x.cmd == "nombre":
        r = buscar(prod, x.id)
        t = x.tipo or ("preview" if r["estado"] == "Preview" else "")
        print(nombre_base(r) + f"_{x.formato}" + (f"_{t}" if t else "") + f".{x.ext}")
    elif x.cmd == "preview":
        buscar(prod, x.id)["link_preview"] = x.link; escribir(PROD, prod); print("ok")
    elif x.cmd == "decision":
        r = buscar(prod, x.id)
        r.update(decision_cris=x.decision, fecha_decision=x.fecha)
        if x.comentarios:
            r["comentarios_cris"] = x.comentarios
        if x.decision == "Aprobada":
            r["estado"] = "Aprobada"
        elif x.decision == "Rechazada":
            r["estado"] = "Rechazada"
        escribir(PROD, prod); print(x.id, "decisión:", x.decision, "| estado:", r["estado"])
    elif x.cmd == "estado":
        r = buscar(prod, x.id)
        r["estado"] = x.estado
        if x.nota:
            r["notas"] = (r["notas"] + " | " if r["notas"] else "") + f"{date.today()}: {x.nota}"
        if x.estado == "Vigente":
            for o in prod:
                if o["pieza"] == r["pieza"] and variacion_de(o) == variacion_de(r) and o["voz_idioma"] == r["voz_idioma"] and o["id"] != r["id"] and o["estado"] in ("Vigente", "Aprobada"):
                    o["estado"] = "Reemplazada"
        escribir(PROD, prod); print(x.id, "->", x.estado)
    elif x.cmd == "ruta":
        r = buscar(prod, x.id)
        for k, v in (("ruta_local", x.local), ("link_drive_final", x.drive), ("prproj", x.prproj)):
            if v:
                r[k] = v
        escribir(PROD, prod); print("ok")
    elif x.cmd == "usos":
        r = buscar(prod, x.id)
        if r["estado"] not in ("Aprobada", "Vigente"):
            sys.exit(f"{x.id} está en {r['estado']}: los usos se marcan al aprobar")
        if r["usos_marcados_directorio"]:
            sys.exit(f"Ya marcados el {r['usos_marcados_directorio']}: no sumar dos veces")
        ids = [i.strip() for i in r["planos_usados_directorio"].split(",") if i.strip()]
        print("En el Directorio maestro (Sheet 1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w, pestaña Directorio), para cada ID de la columna A:")
        print(f"  columna Y (# de usos) += 1 ; columna AQ (Usado en) += línea '{r['id']} {r['nombre_pieza']} (video)'")
        print("  IDs:", ", ".join(ids))
        print("Luego: registro.py usos-hechos", r["id"])
    elif x.cmd == "usos-hechos":
        buscar(prod, x.id)["usos_marcados_directorio"] = x.fecha; escribir(PROD, prod); print("ok")
    elif x.cmd in ("cierres", "cerrar"):
        def pubs_de(vid):
            return [p for p in plan if p["id_version"] == vid]
        def sale(r):
            ps = pubs_de(r["id"])
            return r["estado"] in SALEN or (ps and all(p["estado"] in ("Cerrada", "Retirada") for p in ps))
        if x.cmd == "cierres":
            hay = False
            for r in prod:
                if sale(r):
                    hay = True
                    en_h = any(h["id"] == r["id"] for h in hist)
                    print(f"  {r['id']} ({r['estado']}) | en Histórico: {'sí' if en_h else 'NO'}")
            print("" if hay else "Nada para mover.")
        else:
            r = buscar(prod, x.id)
            if not sale(r):
                sys.exit(f"{x.id} no cumple la regla de cierre (Estado {r['estado']}; publicaciones en Planner abiertas o sin ninguna)")
            ps = pubs_de(x.id)
            tot = {m: sum(num(p[f"h72_{m}"]) for p in ps) for m in ("alcance", "vistas", "clics", "leads", "costo")}
            vistas = sum(num(p["h72_vistas"]) for p in ps)
            tot["retencion"] = (sum(num(p["h72_retencion"]) * num(p["h72_vistas"]) for p in ps) / vistas) if vistas else 0
            decs = sorted({p["decision"] for p in ps if p["decision"]})
            fila = dict(id=r["id"], pieza=r["pieza"], nombre_pieza=r["nombre_pieza"], vertical=r["vertical"], nivel=r["nivel"], version=r["version"], hook=r["hook"], contenido=r["contenido"],
                        cta=r["cta"], eje_que_cambia=r["eje_que_cambia"], basada_en=r["basada_en"], voz_idioma=r["voz_idioma"], formatos=r["formatos"],
                        estado_final=r["estado"] if r["estado"] in SALEN else "Cerrada", fecha_creacion=r["fecha_creacion"], fecha_cierre=x.fecha, que_cambio=r["que_cambio"],
                        planos_usados=r["planos_usados_directorio"], export_drive=r["link_drive_final"],
                        publicada_en="; ".join(f"{p['plataforma']} {p['url']}".strip() for p in ps if p["url"]), decision="; ".join(decs), builder=r["builder"], notas=r["notas"])
            if ps:
                fila.update({f"h72_{m}": (f"{v:g}" if v else "") for m, v in tot.items()})
            if len(decs) > 1:
                fila["notas"] += " | Publicaciones con decisiones distintas: revisar y detallar"
            if not any(h["id"] == r["id"] for h in hist):
                hist.append(fila); escribir(HIST, hist)
            print("Fila de Histórico (agregar al final de la hoja y verificar ANTES de borrar la de Producción):")
            print(json.dumps([[fila.get(c, "") for c in CAMPOS[HIST]]], ensure_ascii=False))
            print("Borrar de Producción solo tras verificar; RENT.0001 a RENT.0005 esperan confirmación de Cris. Luego espejo: quitar la fila de produccion.csv (ya está en historico.csv).")
    elif x.cmd == "importar":
        # HOJA -> ESPEJO. archivo = JSON de get_values de la pestaña completa (fila 1 = encabezados). La hoja manda.
        destino = {"guiones": (GUIO, guio, "id_angulo"), "produccion": (PROD, prod, "id"), "planner": (PLAN, plan, "id_pub"), "historico": (HIST, hist, "id")}[x.pestana]
        p, filas, clave = destino
        datos = json.load(open(x.archivo, encoding="utf-8"))
        vals = datos["values"] if isinstance(datos, dict) else datos
        campos = CAMPOS[p]
        acciones, cambios, vistos = [], 0, set()
        for n, fila in enumerate(vals[1:], start=2):
            fila = list(fila) + [""] * (len(campos) - len(fila))
            reg = {c: str(fila[i]).strip() for i, c in enumerate(campos)}
            if not any(reg.values()):
                continue
            vistos.add(reg[clave])
            ex = next((r for r in filas if r[clave] == reg[clave]), None)
            if ex is None:
                filas.append(reg); cambios += 1; print(f"NUEVA en la hoja (fila {n}): {reg[clave]}"); ex = reg
            else:
                dif = [c for c in campos if (ex.get(c, "") or "") != reg[c]]
                for c in dif:
                    print(f"  {reg[clave]}.{c}: '{ex.get(c, '')}' -> '{reg[c]}'")
                    ex[c] = reg[c]
                cambios += bool(dif)
            if x.pestana == "guiones" and ex["estado"] == "Aprobado" and ex["decision_cris"] == "Aprobado" and not ex["versiones_generadas"]:
                acciones.append(f"{ex['id_angulo']} (fila {n}): guion APROBADO sin versiones -> registro.py guion {ex['id_angulo']} y producir (sección 5)")
            if x.pestana == "guiones" and ex["decision_cris"] in ("Con cambios", "Rechazado"):
                acciones.append(f"{ex['id_angulo']} (fila {n}): decisión {ex['decision_cris']} -> NO producir")
            if x.pestana == "produccion":
                if ex["decision_cris"] == "Aprobada" and ex["estado"] == "Preview":
                    ex["estado"] = "Aprobada"
                    acciones.append(f"{ex['id']} (fila {n}): Cris APROBÓ en la hoja -> escribir Estado=Aprobada en L{n}; marcar usos en el Directorio (registro.py usos {ex['id']}); crear .prproj. NO crear filas en el Planner (se crean solas)")
                elif ex["decision_cris"] == "Con cambios" and ex["estado"] == "Preview":
                    acciones.append(f"{ex['id']} (fila {n}): Cris pidió CAMBIOS -> leer comentarios_cris y crear versión nueva (ID nuevo)")
                elif ex["decision_cris"] == "Rechazada" and ex["estado"] not in ("Rechazada", "Archivada"):
                    ex["estado"] = "Rechazada"
                    acciones.append(f"{ex['id']} (fila {n}): Cris RECHAZÓ -> escribir Estado=Rechazada en L{n}")
                if ex["estado"] in ("Aprobada", "Vigente") and not ex["usos_marcados_directorio"] and ex["planos_usados_directorio"]:
                    acciones.append(f"{ex['id']}: aprobada y con usos SIN marcar en el Directorio de planos (registro.py usos {ex['id']})")
            if x.pestana == "planner":
                if ex["estado"] == "Publicada" and not ex["url"]:
                    acciones.append(f"{ex['id_pub']}: Publicada sin URL -> avisar a Cris (no dar por publicada)")
                if ex["estado"] in ("Cerrada", "Retirada"):
                    acciones.append(f"{ex['id_pub']}: {ex['estado']} -> mirar si la versión {ex['id_version']} ya puede cerrarse (registro.py cierres)")
        escribir(p, filas)
        print(f"{x.pestana}: {cambios} fila(s) con cambios traídas de la hoja")
        for ac in acciones:
            print("ACCIÓN:", ac)
    elif x.cmd == "celdas":
        # ESPEJO -> HOJA, celda por celda (para no pisar el resto de la fila): imprime rango y valor listos para update_values
        r = buscar(prod, x.id)
        cols = CAMPOS[PROD]
        def letra(i):
            return (chr(65 + i // 26 - 1) if i >= 26 else "") + chr(65 + i % 26)
        for c in x.campos.split(","):
            c = c.strip()
            print(f"Producción!{letra(cols.index(c))}{x.fila}  ({c}) = {json.dumps(r[c], ensure_ascii=False)}")
    elif x.cmd == "pendientes":
        print("Guiones aprobados por Cris sin producir:")
        for g in guio:
            if g["estado"] == "Aprobado" and g["decision_cris"] == "Aprobado":
                print(f"  {g['id_angulo']} {g['angulo']} | hooks: {g['hooks_aprobados'] or '(todos los que tengan texto)'}")
        print("Versiones en Preview esperando decisión de Cris:")
        for r in prod:
            if r["estado"] == "Preview":
                print(f"  {r['id']} {variacion_de(r)} {r['voz_idioma']} | decisión: {r['decision_cris'] or 'Pendiente'} | preview: {r['link_preview'] or '(sin link: enviar por chat)'}")
        print("Aprobadas/vigentes sin export en Drive (el planner no publica sin link):")
        for r in prod:
            if r["estado"] in ("Aprobada", "Vigente") and not r["link_drive_final"].strip():
                print(f"  {r['id']} {variacion_de(r)} {r['voz_idioma']}")
        print("Planner: filas Cerradas/Retiradas por revisar para cierre: registro.py cierres")
    elif x.cmd == "manifest":
        out = dict(generado=str(date.today()), hoja="1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks", guiones=guio, produccion=prod, planner=plan, historico=hist)
        (REG / "manifest.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print("manifest.json:", len(guio), "guiones,", len(prod), "producción,", len(plan), "planner,", len(hist), "histórico")
    elif x.cmd == "hoja":
        # valores del espejo en el orden de las columnas de la hoja maestra, listos para update_values (ver registro/HOJA.md)
        for nombre, filas, p in (("Guiones", guio, GUIO), ("Producción", prod, PROD), ("Planner", plan, PLAN), ("Histórico", hist, HIST)):
            vals = [[r.get(c, "") or "" for c in CAMPOS[p]] for r in filas]
            print(f"--- {nombre}!A2 ({len(vals)} filas x {len(CAMPOS[p])} columnas)")
            print(json.dumps(vals, ensure_ascii=False))
    elif x.cmd == "validar":
        ids = {r["id"] for r in prod} | {r["id"] for r in hist}
        malos = 0
        for f in sorted(Path(x.carpeta).rglob("*")):
            if f.is_file() and f.suffix.lower() in (".mp4", ".mov", ".prproj", ".wav"):
                m = NOMBRE.match(f.name)
                if not m:
                    print("NOMBRE FUERA DE CONVENCIÓN:", f.name); malos += 1
                elif m["id"] not in ids:
                    print("SIN REGISTRO:", f.name); malos += 1
        print("ok" if not malos else f"{malos} archivo(s) por corregir")


if __name__ == "__main__":
    main()
