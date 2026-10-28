"""INTA25 sin narrador (Cris, 27-oct: "si vas a usar casos de éxito, evita al narrador y deja que las mismas personas hablen").
Arma la 'voz' con frases reales de los entrevistados del caso (Clínica Maxilofacial del Caribe / Instituto Bucofacial de las Américas), sus tiempos, los planos
(el entrevistado mientras habla + apoyos del mismo caso) y la spec. Los entrevistados autorizaron grabación y uso de imagen en cámara; el permiso del cliente sigue abierto en la hoja.
uso: python -I armar_caso25.py"""
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.argv = ["x"]
from seleccion import rows, ruta, num

BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\INTA25")
CASO = BASE / "Caso"
D = 0.10
GAP = 0.25
TAIL = 2.6        # silencio final para la tarjeta de llamado a la acción
R = {r["ID"]: r for r in rows}
# (clip, desde, hasta, etiqueta). Las frases son exactas de la transcripción (Scribe); sin nombres, cédulas ni charla previa.
SEGS = [
    ("105163", 139.42, 144.32, "gancho"),     # José Luis: proyección en vivo del procedimiento
    ("105163", 124.20, 128.98, "dibuja"),     # el conferencista puede dibujar, borrar... intuitiva
    ("105165", 124.98, 127.84, "vanessa1"),   # muy innovador y muy dinámico
    ("105165", 133.34, 137.32, "vanessa2"),   # la explicación mucho más fácil y entendible
    ("105164", 358.02, 365.28, "elion"),      # sin tablero, proyector ni televisor: todo en una pantalla
    ("105163", 237.78, 239.40, "facil"),      # muy fácil, muy fácil de usar
    ("105164", 443.08, 445.16, "recomiendo"), # la recomiendo al cien por ciento
]
APOYOS = ["105174", "105173", "107119", "107123", "105166", "105168", "105170", "105172"]   # apoyos del mismo caso (planos sin la voz del entrevistado)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-400:])


voz = BASE / "Voz"
voz.mkdir(exist_ok=True)
tmp = BASE / "Proyecto" / "caso_tmp"
tmp.mkdir(parents=True, exist_ok=True)
words, t, partes = [], 0.0, []
fuente = {}
for n, (cid, a, b, tag) in enumerate(SEGS):
    j = json.load(open(CASO / f"{cid}.json", encoding="utf-8"))
    fuente[cid] = j["ruta"]
    a0, b0 = a - 0.06, b + 0.12
    wav = tmp / f"seg{n}.wav"
    run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(a0), "-i", j["ruta"], "-t", str(b0 - a0), "-vn", "-ac", "1", "-ar", "48000",
         "-af", "highpass=f=70,loudnorm=I=-18:TP=-1.5:LRA=9", str(wav)])
    ws = [w for w in j["words"] if w.get("type") == "word" and w["start"] >= a - 0.02 and w["end"] <= b + 0.05]
    for k, w in enumerate(ws):
        txt = re.sub(r"[¿¡]", "", w["text"])
        words.append(dict(text=txt, start=round(t + (w["start"] - a0), 3), end=round(t + (w["end"] - a0), 3), type="word"))
    if not re.search(r"[.:?!]$", words[-1]["text"]):
        words[-1]["text"] = re.sub(r"[,;]$", "", words[-1]["text"]) + "."
    partes.append(dict(tag=tag, clip=cid, src=a0, t0=t, dur=b0 - a0, wav=str(wav), i0=len(words) - len(ws), i1=len(words)))
    t += (b0 - a0) + GAP
# voz concatenada + silencio final
lst = tmp / "lista.txt"
sil = tmp / "sil.wav"
run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=mono", "-t", str(GAP), str(sil)])
cola = tmp / "cola.wav"
run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(TAIL), str(cola)])
lst.write_text("\n".join(f"file '{p['wav'].replace(chr(92), '/')}'\nfile '{str(sil).replace(chr(92), '/')}'" for p in partes) + f"\nfile '{str(cola).replace(chr(92), '/')}'\n", encoding="utf-8")
run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "pcm_s16le", str(voz / "INTA25_voz.wav")])
# palabra-ancla del cierre (tarjeta de texto sin voz)
t_fin = words[-1]["end"]
words.append(dict(text="Escríbenos", start=round(t_fin + 0.35, 3), end=round(t_fin + 1.45, 3), type="word"))
(voz / "INTA25_voz_scribe.json").write_text(json.dumps(dict(words=words), ensure_ascii=False), encoding="utf-8")
(voz / "guion_limpio.txt").write_text(" ".join(w["text"] for w in words[:-1]), encoding="utf-8")
(voz / "guion_dirigido.txt").write_text("(sin narrador: frases reales de los entrevistados del caso)", encoding="utf-8")

# ── planos: el entrevistado mientras habla; a mitad de cada frase larga, un apoyo del mismo caso ─────────
plan, ap = [], 0
for p in partes:
    ws = words[p["i0"]:p["i1"]]
    # tramos de 2-3 s cortando en palabra
    cortes, ini = [], ws[0]["start"] - 0.0
    for w in ws:
        if w["end"] - ini >= 2.1:
            cortes.append((ini, w["end"])); ini = w["end"] + 0.0
    if ws[-1]["end"] - ini > 0.5 or not cortes:
        cortes.append((ini, ws[-1]["end"] + GAP * 0.9))
    elif cortes:
        cortes[-1] = (cortes[-1][0], ws[-1]["end"] + GAP * 0.9)
    cortes[0] = (p["t0"], cortes[0][1])
    while len(cortes) > 1 and cortes[-1][1] - cortes[-1][0] < 1.4:       # sin tramos de menos de 1,4 s
        cortes[-2] = (cortes[-2][0], cortes[-1][1]); cortes.pop()
    for q, (a, b) in enumerate(cortes):
        need = max(2.2, b - a + 0.7)
        hablando = not (len(cortes) > 1 and q == len(cortes) - 1 and p["tag"] != "gancho") or p["dur"] < 3.6
        if p["tag"] == "gancho" and q == 1:
            hablando = False
        if hablando:
            cid = p["clip"]
            ss = max(0.0, p["src"] + (a - p["t0"]) - D)          # el video lleva el audio con retraso D: se compensa para que los labios coincidan
            r = R[cid]
        else:
            r = None
            while r is None:
                cand = R[APOYOS[ap % len(APOYOS)]]; ap += 1
                if num(cand["Duración (s)"]) >= need + 0.3 and ruta(cand):
                    r = cand
            cid = r["ID"]
            ss = max(0.0, min(num(r["Mejor momento (s)"]) - 0.4, num(r["Duración (s)"]) - need - 0.1))
        perfil = r["Perfil de color"]
        pr = ruta(r)
        plan.append(dict(n=len(plan), t0=round(a, 3), t1=round(b, 3), id=cid, key=f"{cid}_{int(round(ss * 100))}", ruta=pr, ss=round(ss, 2), need=round(need, 2),
                         log=1 if ("S-Log" in perfil and not re.search(r"graded|_color|cuatro_looks", pr, re.I)) else 0, fx=0.5, habla=bool(hablando),
                         texto=" ".join(w["text"] for w in ws if a - 0.01 <= w["start"] < b), desc=r["Información adicional"][:90], lugar=r["Lugar"], prod=r["Producto"][:40], permisos=r["Permisos"]))
cierre_t = words[-1]["start"]
json.dump(dict(cierre_t=cierre_t, planos=plan), open(BASE / "Proyecto" / "planos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ── spec: sobreimpresos (nombre y cargo), escena azul con la idea, tarjeta final de texto ────────────
def ancla(i):
    w = words[i]
    n = sum(1 for x in words[:i] if re.sub(r"[^\wáéíóúñ]", "", x["text"].lower()) == re.sub(r"[^\wáéíóúñ]", "", w["text"].lower()))
    return [re.sub(r"[¿?¡!.,;:«»“”\"]", "", w["text"]).lower(), n]


pa = {p["tag"]: p for p in partes}
spec = dict(
    ov=[dict(a=ancla(pa["gancho"]["i0"]), b=ancla(pa["gancho"]["i0"] + 8), lines=[["José Luis Claro", "b"], ["Representante legal, Clínica Maxilofacial del Caribe", "l"]], pos="bl"),
        dict(a=ancla(pa["vanessa1"]["i0"]), b=ancla(pa["vanessa1"]["i0"] + 6), lines=[["Vanessa Rubio", "b"], ["Estudiante, Instituto Bucofacial de las Américas", "l"]], pos="bl"),
        dict(a=ancla(pa["recomiendo"]["i0"]), b=ancla(pa["recomiendo"]["i1"] - 1), lines=[["Elión Corro", "b"], ["Especialista de contenido digital, Clínica Maxilofacial", "l"]], pos="bl")],
    color=dict(a=ancla(pa["elion"]["i0"] + 8), b=ancla(pa["elion"]["i1"] - 1), lines=[["Pizarra, proyector", "l"], ["y tablero en uno", "b"]]),
    cierre=dict(word=["escríbenos", 0], slogan=False, lines=[["Si tu institución es la siguiente,", "l"], ["escríbenos y armamos tu proyecto", "b"]]),
)
(BASE / "Proyecto" / "spec_caso.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
print("INTA25 voz", round(t_fin, 1), "s | planos", len(plan), "| hablando", sum(1 for p in plan if p["habla"]), "| apoyos", sum(1 for p in plan if not p["habla"]))
for p in plan:
    print(p["t0"], p["t1"], "HABLA" if p["habla"] else "apoyo", p["id"], p["texto"][:50])
