"""Los 2 motion designs por toma de INTA41.0001 (D y E del storyboard), compuestos con el vocabulario de estudio-video/motion/elementos.py
o apoyados en una plantilla. Color por significado: solucion (azul) = OneScreen/arriendo; explicar (blanco) = exponer. La luz cambia entre tomas seguidas."""
import json
from pathlib import Path

SB = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\INTA41\Storyboard")


def tit(x, y, s, lineas, **kw):
    return dict(e="titulo", x=x, y=y, s=s, lineas=lineas, **kw)


def esc(tema, luz, elems, desc, mov, textura=None):
    f = {"luz": luz}
    if textura:
        f["textura"] = textura
    return dict(tipo="motion", escena={"tema": tema, "fondo": f, "elementos": elems}, desc=desc, mov=mov)


def pla(nombre, params, desc=None):
    o = dict(tipo="motion", plantilla=nombre, params=params)
    if desc:
        o["desc"] = desc
    return o


_IDEAS = {}


def idea(tid, k):
    """una idea de ideas.py (guion -> metáfora abstracta) tal cual la propuso"""
    if not _IDEAS:
        for t in json.load(open(SB / "ideas_spec.json", encoding="utf-8"))["videos"][0]["tomas"]:
            _IDEAS[t["id"]] = t["opciones"]
    o = dict(_IDEAS[tid][k]); o.pop("fav", None)
    return o


def motion():
    return {
 "S01": [esc("explicar", "abajo", [dict(e="fantasma", x=700, y=600, t="?", s=560, op=0.12), tit(100, 300, 92, [["Un padre recorre", 300], ["tu colegio", 700, "grad"]], ancho=620),
          dict(e="vidrio", x=760, y=170, w=420, h=300), dict(e="plano", x=820, y=120, w=300, h=400, t="pasillo del colegio"), dict(e="flecha", puntos=[(130, 520), (520, 520), (520, 600)])],
         "Recorrido del padre: titular a la izquierda y el pasillo del colegio rompiendo un vidrio a la derecha",
         "FONDO VIVO; el titular sube palabra a palabra; la flecha se dibuja como el camino del padre; el plano del pasillo avanza dentro del vidrio"),
         pla("titular", dict(l1="Antes de matricular,", l2="un padre recorre", tema="explicar"))],
 "S02": [esc("explicar", "arriba-der", [dict(e="fantasma", x=80, y=620, t="¿?", s=520, op=0.14), tit(640, 330, 100, [["¿Qué ve en", 300], ["tus salones?", 700, "grad"]], a="middle", ancho=900),
          dict(e="destello", x=1010, y=200, s=30, fill="#ffffff")], "La pregunta del hook, grande y centrada, con «¿?» fantasma detrás",
          "FONDO VIVO; «¿Qué ve en» entra light y «tus salones?» bold con degradado; el «¿?» late detrás"),
         pla("frase", dict(texto="¿Qué ve en los salones?", clave="salones", tema="solucion"))],
 "S03": [pla("comparacion", dict(izq="Un salón de siempre", der="Un salón moderno", tema="explicar")),
         esc("solucion", "izquierda", [tit(100, 260, 88, [["Hoy, un salón", 300], ["moderno", 700, "grad"], ["se resuelve con…", 300]], ancho=640),
          dict(e="vidrio", x=780, y=170, w=380, h=380), dict(e="icono", nombre="pantalla", x=970, y=360, s=150)], "Titular de tres líneas y una pantalla en vidrio a la derecha",
          "FONDO VIVO; las líneas entran una a una; el vidrio aparece con un barrido de luz y el ícono de pantalla se dibuja")],
 "S04": [esc("solucion", "abajo-der", [dict(e="fantasma", x=720, y=640, t="1", s=640, op=0.14), tit(100, 290, 92, [["Una sola", 300], ["pantalla", 700], ["interactiva", 700, "grad"]], ancho=600),
          dict(e="cursor", x=980, y=360, nombre="Toca")], "«Una sola pantalla interactiva» con un «1» fantasma gigante y un cursor que toca",
          "FONDO VIVO; el «1» se dibuja en contorno; las palabras suben una a una; el cursor entra y hace clic"),
         pla("cifra", dict(valor="1", etiqueta="sola pantalla interactiva", tema="solucion"))],
 "S05": [pla("tarjetas", dict(items=[dict(icono="toque", titulo="Pizarra", texto="escribe y dibuja"), dict(icono="pantalla", titulo="Proyector", texto="muestra en grande"),
          dict(icono="auriculares", titulo="Sonido", texto="audio integrado")], titulo="Todo en una", tema="explicar")),
         pla("chips", dict(centro=["Todo en", "una pantalla"], items=[dict(icono="toque", texto="Pizarra"), dict(icono="pantalla", texto="Proyector"), dict(icono="auriculares", texto="Sonido")], tema="solucion"))],
 "S06": [esc("explicar", "arriba", [tit(100, 260, 96, [["Escriben.", 700], ["Muestran.", 700, "grad"]], ancho=560), dict(e="vidrio", x=720, y=160, w=460, h=400),
          dict(e="curva", puntos=[(780, 470), (880, 380), (980, 420), (1100, 260)], sw=8, area=False), dict(e="cursor", x=1090, y=250, nombre="Docente")],
          "Dos verbos en bold y un trazo que se escribe solo sobre un vidrio", "FONDO VIVO; «Escriben.» entra y el trazo se dibuja; «Muestran.» entra con degradado; el cursor sigue el trazo"),
         pla("frase", dict(texto="Escriben, muestran", clave="muestran", tema="solucion"))],
 "S07": [pla("titular", dict(l1="Y explican", l2="sobre ella", tema="explicar")),
         esc("solucion", "centro", [dict(e="vidrio", x=140, y=150, w=560, h=420), dict(e="plano", x=190, y=110, w=460, h=380, t="docente explicando"),
          tit(780, 330, 84, [["Y explican", 300], ["sobre ella", 700, "grad"]], ancho=440)], "El plano del docente rompe un vidrio a la izquierda y el texto a la derecha",
          "FONDO VIVO; el vidrio entra con barrido de luz; el plano sobresale del borde; el texto sube palabra a palabra")],
 "S08": [idea("S08", 0), pla("notificacion", dict(titulo="Asistente con IA", texto="Te ayudo a preparar la clase", hora="ahora", icono="chat", tema="solucion"))],
 "S09": [esc("solucion", "abajo", [tit(640, 300, 80, [["Eso es una", 300]], a="middle", ancho=700), dict(e="marcador", x=390, y=340, w=500, h=120, t="OneScreen"),
          dict(e="orbita", x=640, y=380, rx=470, ry=120, rot=-6), dict(e="destello", x=1050, y=300, s=34, fill="#ffffff")],
          "«Eso es una» y el logo oficial de OneScreen en el centro, con órbita y destello",
          "FONDO VIVO; «Eso es una» sube; el marcador se dibuja y aparece el LOGO OFICIAL (4 colores, no texto); la órbita gira y el destello brilla"),
         pla("frase", dict(texto="Eso es una OneScreen", clave="OneScreen", tema="solucion"))],
 "S10": [esc("solucion", "arriba-der", [dict(e="fantasma", x=60, y=640, t="+", s=700, op=0.12), tit(640, 330, 104, [["Y aquí viene", 300], ["la mejor parte", 700, "grad"]], a="middle", ancho=980),
          dict(e="destello", x=1080, y=210, s=40, fill="#ffffff"), dict(e="destello", x=220, y=470, s=24, fill="#ffffff")], "La frase de giro centrada, grande, con destellos",
          "FONDO VIVO; «Y aquí viene» light; pausa corta; «la mejor parte» entra con degradado y los destellos brillan"),
         pla("titular", dict(l1="Y aquí viene", l2="la mejor parte", tema="explicar"))],
 "S11": [pla("tachado", dict(texto="No tienes que", tachado="comprarla", tema="solucion")),
         pla("comparacion", dict(izq="Comprarla", der="Arrendarla", tema="explicar"))],
 "S12": [pla("cifra", dict(valor="$0", etiqueta="de inversión inicial", tema="solucion")),
         esc("explicar", "izquierda", [dict(e="fantasma", x=640, y=620, t="$0", s=560, op=0.14, a="middle"), tit(640, 300, 96, [["Arrendar,", 700, "grad"], ["sin inversión inicial", 300]], a="middle", ancho=980)],
          "«$0» gigante en contorno detrás de «Arrendar, sin inversión inicial»", "FONDO VIVO; el «$0» se dibuja en contorno; «Arrendar,» entra bold con degradado y luego la línea light")],
 "S13": [esc("solucion", "abajo", [tit(100, 240, 76, [["Una cuota", 300], ["mensual", 700, "grad"], ["que ya incluye", 300]], ancho=520),
          dict(e="tarjeta_stat", x=780, y=170, w=360, h=320, valor="Cuota", sub="mensual", filas=[["Incluye", "Instalación"], ["Incluye", "Formación docente"]])],
          "Titular de la cuota y una tarjeta que la desglosa (sin cifras de precio)", "FONDO VIVO; el titular entra; la tarjeta blanca sube con halo y sus filas aparecen una a una"),
         pla("checklist", dict(items=["Pantalla", "Instalación", "Formación docente"], titulo="Una cuota mensual que incluye", tema="explicar"))],
 "S14": [idea("S14", 0), pla("flujo", dict(nodos=["Instalación", "Formación docente"], iconos=["pantalla", "grupo"], titulo="Incluido en la cuota", tema="solucion"))],
 "S15": [esc("explicar", "arriba", [dict(e="fantasma", x=80, y=640, t="hoy", s=460, op=0.14), tit(100, 260, 92, [["Moderno", 700, "grad"], ["este año,", 300]], ancho=600),
          dict(e="boton", x=760, y=470, t="no dentro de tres", estilo="contorno", s=40)], "«Moderno este año» y la etiqueta «no dentro de tres» que se tacha",
          "FONDO VIVO; «Moderno» entra con degradado; «este año,» light; la etiqueta aparece y una línea la tacha"),
         pla("linea", dict(puntos=["Este año", "+1", "+2", "+3"], titulo="Moderno desde ya", tema="solucion"))],
 "S16": [pla("titular", dict(l1="Y eso,", l2="los padres lo notan", tema="explicar")), idea("S01", 0)],
 "S17": [pla("cta", dict(texto="Conoce cómo funciona", sub="onescreenlatam.com/rental", tema="solucion")),
         esc("solucion", "izquierda", [tit(100, 270, 84, [["Conoce cómo", 300], ["funciona", 700, "grad"]], ancho=560), dict(e="boton", x=100, y=470, t="onescreenlatam.com/rental", estilo="blanca", s=34),
          dict(e="cursor", x=560, y=450, nombre="Tú")], "CTA con la URL en un botón blanco y un cursor que hace clic", "FONDO VIVO; el titular sube; el botón aparece con rebote; el cursor entra y hace clic")],
 "S18": [esc("solucion", "centro", [dict(e="marcador", x=470, y=170, w=340, h=90, t="OneScreen"), tit(640, 380, 76, [["Transforma el espacio.", 700]], a="middle", ancho=1000),
          tit(640, 480, 76, [["Transforma el futuro.", 700, "grad"]], a="middle", ancho=1000)], "Cierre de marca: logo oficial y slogan («el espacio» y «el futuro» en bold)",
          "FONDO VIVO; el LOGO OFICIAL entra; las dos líneas del slogan suben con la voz; intro de marca con su sonido"),
         pla("frase", dict(texto="Transforma el futuro", clave="el futuro", tema="solucion"))],
    }
