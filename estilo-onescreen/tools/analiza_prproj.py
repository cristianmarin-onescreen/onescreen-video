"""Analiza la EDICIÓN de un proyecto de Premiere (.prproj) y la cruza con el audio del render final.

Qué mide (para aprender el estilo de edición de Cris, no el color):
  - cortes y duración de planos (pista de video principal y capas de apoyo),
  - cambios de escala por clip (fijos y animados), movimiento de cámara (capa de ajuste / Transformar),
  - transiciones, capas gráficas (PNG/rótulos) y sus animaciones de opacidad/posición,
  - música/voz usadas por pista,
  - alineación de los cortes con el pulso y los golpes de la música (del audio del render final).

Uso:  python -I analiza_prproj.py "proyecto.prproj" "render_final.mp4" [--secuencia NOMBRE] [--json salida.json]
Los ticks de Premiere son 254016000000 por segundo; los keyframes llevan un desfase de 3600 s (clip de gráficos).
"""
import argparse, gzip, json, subprocess, sys, tempfile, os
from collections import Counter
import numpy as np
from lxml import etree

T = 254016000000


def cargar(path):
    xml = gzip.open(path, "rb").read()
    root = etree.fromstring(xml, parser=etree.XMLParser(huge_tree=True, recover=True))
    byid = {}
    for e in root.iter():
        for a in ("ObjectID", "ObjectUID"):
            v = e.get(a)
            if v:
                byid[v] = e
    return root, byid


def sec(t):
    return round(int(t) / T, 3)


class P:
    def __init__(self, path):
        self.root, self.byid = cargar(path)

    def ref(self, e):
        if e is None:
            return None
        r = e.get("ObjectRef") or e.get("ObjectURef")
        return self.byid.get(r) if r else None

    def secuencias(self):
        out = []
        for s in self.root.findall("Sequence"):
            tg = s.find("TrackGroups")
            if tg is None:
                continue
            grupos = [self.ref(g.find("Second")) for g in tg]
            vid = grupos[0] if grupos else None
            n = len(vid.findall(".//Tracks/Track")) if vid is not None else 0
            out.append((s, s.findtext("Name"), n))
        return out

    def pistas(self, grupo):
        return [self.byid[t.get("ObjectURef")] for t in grupo.findall(".//Tracks/Track")]

    def items(self, pista):
        res = []
        for i in pista.findall(".//TrackItems/TrackItem"):
            it = self.ref(i)
            if it is not None:
                res.append(it)
        return res

    def info_item(self, it):
        tt = it.find(".//TrackItem")
        st = sec(tt.findtext("Start") or "0")
        en = sec(tt.findtext("End"))
        sc = it.find(".//SubClip")
        nombre, ip, op = it.tag, None, None
        if sc is not None and sc.get("ObjectRef"):
            scx = self.ref(sc)
            nombre = scx.findtext("Name")
            cl = self.ref(scx.find("Clip"))
            if cl is not None:
                ip, op = cl.findtext(".//InPoint"), cl.findtext(".//OutPoint")
        efectos = []
        comps = it.find(".//Components")
        cadena = self.ref(comps) if comps is not None else None
        if cadena is not None:
            for cr in cadena.findall(".//Components/Component"):
                c = self.ref(cr)
                if c is None:
                    continue
                efectos.append(self.efecto(c))
        return dict(inicio=st, fin=en, dur=round(en - st, 3), nombre=nombre,
                    src_in=sec(ip) if ip else None, src_out=sec(op) if op else None, efectos=efectos)

    def efecto(self, c):
        mn = c.findtext("MatchName")
        disp = c.findtext(".//DisplayName")
        params = {}
        for pr in c.findall(".//Params/Param"):
            p = self.ref(pr)
            if p is None:
                continue
            nm = (p.findtext("Name") or "").strip()
            kf = p.findtext("Keyframes")
            st = p.findtext("StartKeyframe") or p.findtext("CurrentValue") or ""
            if kf and kf.strip():
                pts = []
                for k in kf.split(";"):
                    if k.strip():
                        q = k.split(",")
                        pts.append((int(q[0]), q[1]))
                t0 = pts[0][0]
                params[nm] = dict(kf=[(round((t - t0) / T, 3), v) for t, v in pts])
            elif "," in st:
                params[nm] = dict(v=st.split(",")[1])
        return dict(match=mn, nombre=disp, params=params)


def num(v):
    try:
        return float(str(v).split(":")[0])
    except Exception:
        return None


def resumen_clip(i):
    """Escala, movimiento y opacidad de un clip."""
    esc = None
    zoom = None
    pos = None
    opa = None
    otros = []
    for e in i["efectos"]:
        if e["match"] == "AE.ADBE Motion":
            for n, p in e["params"].items():
                if n.startswith("Escala") and "Anchura" not in n:
                    if "v" in p:
                        esc = num(p["v"])
                    if "kf" in p:
                        z = [(t, num(v)) for t, v in p["kf"]]
                        zoom = z
                if n.startswith("Posici") and "kf" in p:
                    pos = p["kf"]
        elif e["match"] == "AE.ADBE Opacity":
            for n, p in e["params"].items():
                if n.startswith("Opacidad") and "kf" in p:
                    opa = [(t, num(v)) for t, v in p["kf"]]
        elif e["match"] not in ("AE.ADBE Lumetri",):
            otros.append(e["nombre"])
    return esc, zoom, pos, opa, otros


def beats_audio(mp4, max_s=None):
    import librosa
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav")
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", mp4, "-vn", "-ac", "1", "-ar", "22050", wav], check=True)
        y, sr = librosa.load(wav, sr=22050)
    hop = 256
    # percusivo: separa la parte rítmica y busca pulso y golpes
    yp = librosa.effects.percussive(y, margin=2.0)
    oenv = librosa.onset.onset_strength(y=yp, sr=sr, hop_length=hop)
    tempo, b = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, hop_length=hop, units="time", trim=False)
    ons = librosa.onset.onset_detect(onset_envelope=oenv, sr=sr, hop_length=hop, units="time", backtrack=False)
    tempo = float(np.atleast_1d(tempo)[0])
    return tempo, np.array(b), np.array(ons)


def alineacion(cortes, beats, ons, rng=np.random.default_rng(0)):
    cortes = np.array(sorted(cortes))
    if len(cortes) == 0 or len(beats) < 4:
        return {}

    def d(a, ref):
        return np.min(np.abs(a[:, None] - ref[None, :]), axis=1)
    out = {}
    for nombre, ref in (("pulso", beats), ("golpes", ons)):
        dd = d(cortes, ref)
        T0, T1 = ref.min(), ref.max()
        base = []
        for _ in range(500):
            r = np.sort(rng.uniform(cortes.min(), cortes.max(), len(cortes)))
            base.append(np.mean(d(r, ref) <= 0.06))
        out[nombre] = dict(
            n=int(len(cortes)), mediana_ms=int(np.median(dd) * 1000),
            pct_a_2_cuadros=round(float(np.mean(dd <= 0.084)) * 100, 1),
            pct_a_1_cuadro=round(float(np.mean(dd <= 0.042)) * 100, 1),
            azar_pct_a_1_5_cuadros=round(float(np.mean(base)) * 100, 1),
            real_pct_a_1_5_cuadros=round(float(np.mean(dd <= 0.063)) * 100, 1),
            adelantados_ms=int(np.median([c - ref[np.argmin(np.abs(ref - c))] for c in cortes]) * 1000))
    return out


def analizar(prproj, render=None, secuencia=None):
    p = P(prproj)
    secs = p.secuencias()
    cand = [(s, n, v) for s, n, v in secs if v >= 3]
    if secuencia:
        cand = [c for c in secs if c[1] == secuencia] or cand
    # la más larga con más pistas de video
    best, mejor = None, -1
    rd = None
    if render:
        rd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", render], capture_output=True, text=True).stdout.strip())
    for s, nombre, nv in cand:
        grupos = [p.ref(g.find("Second")) for g in s.find("TrackGroups")]
        dur = 0
        for pi in p.pistas(grupos[0]):
            for it in p.items(pi):
                dur = max(dur, sec(it.find(".//TrackItem").findtext("End")))
        ncl = sum(len(p.items(pi)) for pi in p.pistas(grupos[0]))
        punt = (-abs(dur - rd) * 100 + nv) if rd else ((nv * 1000 + ncl) if 8 <= dur <= 400 else -1)
        if best is None or punt > mejor:
            best, mejor = (s, nombre, grupos, dur), punt
    s, nombre, grupos, dur = best
    res = dict(proyecto=os.path.basename(prproj), secuencia=nombre, duracion=dur, pistas_video=[], audio=[], capa_ajuste=None)
    cortes = []
    todas = []
    for pi_idx, pista in enumerate(p.pistas(grupos[0])):
        lista = []
        for it in p.items(pista):
            if it.tag.endswith("TransitionItem") or "Transition" in it.tag:
                continue
            tt = it.find(".//TrackItem")
            if tt is None:
                continue
            if it.find(".//SubClip") is None or it.find(".//SubClip").get("ObjectRef") is None:
                continue
            i = p.info_item(it)
            lista.append(i)
        res["pistas_video"].append(dict(pista=pi_idx, clips=len(lista)))
        todas.append(lista)
    # capa de ajuste
    for lista in todas:
        for i in lista:
            if "ajuste" in (i["nombre"] or "").lower():
                cam = {}
                for e in i["efectos"]:
                    if e["match"] == "AE.ADBE Geometry":
                        pe = e["params"].get("Altura de escala", {}).get("kf")
                        po = e["params"].get("Posición", e["params"].get("Posición", {})).get("kf")
                        if pe:
                            vals = [num(v) for _, v in pe]
                            cam["escala_min_max"] = (min(vals), max(vals))
                            cam["intervalo_keyframes_s"] = (round(float(np.min(np.diff([t for t, _ in pe]))), 2), round(float(np.max(np.diff([t for t, _ in pe]))), 2))
                        if po:
                            xs = [float(v.split(":")[0]) for _, v in po]
                            ys = [float(v.split(":")[1]) for _, v in po if ":" in v]
                            cam["pos_x_rango"] = (round(min(xs), 3), round(max(xs), 3))
                            cam["pos_y_rango"] = (round(min(ys), 3), round(max(ys), 3)) if ys else None
                    elif e["match"] == "AE.Mettle SkyBox Chromatic Aberrations":
                        cam["aberracion"] = {k: v.get("v") for k, v in e["params"].items() if k.startswith("Aberraci")}
                res["capa_ajuste"] = cam
    # pista principal = la de mayor número de clips con fuente "C####"
    prin = max(todas, key=lambda l: len(l)) if todas else []
    prin = sorted(prin, key=lambda i: i["inicio"])
    dur_planos = [i["dur"] for i in prin]
    res["principal"] = dict(clips=len(prin), dur_mediana=round(float(np.median(dur_planos)), 2) if dur_planos else None,
                            dur_media=round(float(np.mean(dur_planos)), 2) if dur_planos else None,
                            dur_min=min(dur_planos) if dur_planos else None, dur_max=max(dur_planos) if dur_planos else None)
    escalas, zooms, secuencia_esc = [], [], []
    for i in prin:
        esc, zoom, pos, opa, otros = resumen_clip(i)
        secuencia_esc.append(esc if esc else 100.0 if not zoom else None)
        if esc:
            escalas.append(esc)
        if zoom:
            zooms.append(dict(inicio=i["inicio"], dur=i["dur"], de=zoom[0][1], a=zoom[-1][1]))
    res["escala_por_clip"] = secuencia_esc
    res["escalas_fijas_stats"] = dict(n=len(escalas), min=min(escalas) if escalas else None, max=max(escalas) if escalas else None,
                                      mediana=float(np.median(escalas)) if escalas else None)
    res["zooms_animados"] = zooms
    # alternancia: ¿clips consecutivos alternan 100 / zoom?
    alt = 0
    for a, b in zip(secuencia_esc, secuencia_esc[1:]):
        if a is not None and b is not None and (a <= 101) != (b <= 101):
            alt += 1
    res["alternancia_pct"] = round(100 * alt / max(1, len(secuencia_esc) - 1), 1)
    # capas de apoyo y gráficos
    apoyo, graficos = [], []
    for lista in todas:
        if lista is prin:
            continue
        for i in lista:
            if "ajuste" in (i["nombre"] or "").lower():
                continue
            esc, zoom, pos, opa, otros = resumen_clip(i)
            d = dict(inicio=i["inicio"], dur=i["dur"], nombre=i["nombre"], escala=esc, opacidad_kf=opa, pos_kf=[(t, v) for t, v in (pos or [])][:6], efectos=otros)
            (graficos if (i["nombre"] or "").lower().endswith((".png", ".jpg")) or "mate" in (i["nombre"] or "").lower() else apoyo).append(d)
    res["apoyo"] = apoyo
    res["graficos"] = graficos
    # transiciones
    tr = Counter()
    for t in grupos[0].iter():
        pass
    for pista in p.pistas(grupos[0]):
        for ti in pista.findall(".//TransitionItems/TrackItem"):
            it = p.ref(ti)
            if it is not None:
                tr["transicion"] += 1
    res["transiciones_video"] = tr["transicion"]
    # audio
    for pi_idx, pista in enumerate(p.pistas(grupos[1])):
        nombres = Counter()
        rango = [1e9, 0]
        for it in p.items(pista):
            tt = it.find(".//TrackItem")
            if tt is None:
                continue
            sc = it.find(".//SubClip")
            nm = p.ref(sc).findtext("Name") if sc is not None and sc.get("ObjectRef") else "?"
            nombres[nm] += 1
            rango[0] = min(rango[0], sec(tt.findtext("Start") or "0")); rango[1] = max(rango[1], sec(tt.findtext("End")))
        res["audio"].append(dict(pista=pi_idx, clips=sum(nombres.values()), archivos=dict(nombres), de=rango[0], a=rango[1]))
    # cortes: inicios de la pista principal (+ capas de apoyo)
    cortes = [i["inicio"] for i in prin[1:]] + [a["inicio"] for a in apoyo] + [a["inicio"] + a["dur"] for a in apoyo]
    res["cortes_total"] = len(cortes)
    res["cortes_principal_s"] = [i["inicio"] for i in prin[1:]]
    # ritmo del habla: bloques de subtítulos de Premiere (2-3 palabras) en la pista de datos
    caps = []
    if len(grupos) > 2 and grupos[2] is not None:
        for pista in p.pistas(grupos[2]):
            for it in p.items(pista):
                tt = it.find(".//TrackItem")
                if tt is not None and tt.findtext("End"):
                    caps.append((sec(tt.findtext("Start") or "0"), sec(tt.findtext("End"))))
    caps.sort()
    if caps:
        ini = np.array([c[0] for c in caps])
        pausas = [caps[k + 1][0] - caps[k][1] for k in range(len(caps) - 1)]
        res["habla"] = dict(bloques=len(caps), dur_bloque_mediana=round(float(np.median([c[1] - c[0] for c in caps])), 2),
                            pausas_mayores_0_3s=int(sum(1 for x in pausas if x > 0.3)))
        def dist(c):
            return float(np.min(np.abs(ini - c)))
        for nombre, cs in (("principal", res["cortes_principal_s"]), ("todos", cortes)):
            dd = np.array([dist(c) for c in cs]) if cs else np.array([])
            if len(dd):
                res["habla"]["cortes_en_frontera_" + nombre] = dict(
                    pct_a_2_cuadros=round(float(np.mean(dd <= 0.084)) * 100, 1), mediana_ms=int(np.median(dd) * 1000))
    if render:
        tempo, b, o = beats_audio(render)
        res["musica"] = dict(tempo_bpm=round(tempo, 1))
        res["alineacion_cortes_principal"] = alineacion(res["cortes_principal_s"], b, o)
        res["alineacion_todos_los_cortes"] = alineacion(cortes, b, o)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prproj"); ap.add_argument("render", nargs="?"); ap.add_argument("--secuencia"); ap.add_argument("--json")
    a = ap.parse_args()
    r = analizar(a.prproj, a.render, a.secuencia)
    s = json.dumps(r, ensure_ascii=False, indent=1, default=str)
    if a.json:
        open(a.json, "w", encoding="utf-8").write(s)
    print(s)
