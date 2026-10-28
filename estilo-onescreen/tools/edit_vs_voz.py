"""Edición vs. voz: cruza el montaje real de Cris (.prproj) con lo que dice la persona (SRT de Premiere o transcripción).

Para UNA carpeta de proyecto: elige el .prproj principal (solo en la raíz de la carpeta, nunca autoguardados), el render final y su SRT,
y produce un "guion de edición" (qué se ve, a qué escala, con qué efecto de sonido, mientras se dice qué) más métricas:
  - cortes respecto a las frases (adelanto/retraso, frontera de frase, saltos por silencios eliminados),
  - planos de apoyo: cuánto cubren, cuándo entran respecto al inicio de la frase, duración, qué se dice,
  - escala del plano principal: alternancia, zooms animados, y en qué parte de la frase empiezan,
  - sonido: efectos (whoosh/swoosh/hit) respecto a cortes, música (nivel, fades, ducking).
Uso: python -I edit_vs_voz.py "carpeta" [--render x.mp4] [--prproj y.prproj] [--srt z.srt] [--out salida]
"""
import argparse, glob, json, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from analiza_prproj import P, sec, num, resumen_clip, T

SFX_RE = re.compile(r"swoosh|whoosh|woosh|swish|swipe|hit|impact|riser|zoom|pop|click|tick|ding|bubble|clap|drum|boom|transition|stomp|snap", re.I)
APOYO_EXT = (".png", ".jpg", ".jpeg", ".ai", ".svg", ".psd")
VOZ_RE = re.compile(r"esv2|\.wav$|^C\d{4}\.MP4$|^IMG_|WhatsApp", re.I)


def dur(path):
    try:
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip())
    except Exception:
        return None


def leer_srt(path):
    txt = open(path, encoding="utf-8-sig", errors="ignore").read().replace("\r", "")
    cues = []
    for bloque in re.split(r"\n\s*\n", txt.strip()):
        l = bloque.split("\n")
        m = None
        for i, x in enumerate(l):
            m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", x)
            if m:
                break
        if not m:
            continue
        g = list(map(int, m.groups()))
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append((a, b, " ".join(l[i + 1:]).strip()))
    return cues


def frases(cues, pausa=0.35):
    """Agrupa subtítulos en frases: corta en puntuación final o pausa > 'pausa' s."""
    out, cur = [], None
    for a, b, t in cues:
        if cur and (a - cur[1] > pausa or re.search(r"[.?!…]\s*$", cur[2])):
            out.append(tuple(cur)); cur = None
        if cur is None:
            cur = [a, b, t]
        else:
            cur[1] = b; cur[2] += " " + t
    if cur:
        out.append(tuple(cur))
    return out


def texto_bloque(b64):
    import base64
    raw = base64.b64decode(b64)
    runs = re.findall(rb"(?:[\x20-\x7e]|[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2}){3,}", raw)
    out = []
    for r in runs:
        try:
            t = r.decode("utf-8")
        except Exception:
            continue
        if re.search(r"^(Rubik|Manrope|Arial|Quicksand|Product|Helvetica|Segoe)[\w .-]*$", t.strip()) or re.fullmatch(r"[A-Za-z]{1,3}", t.strip()):
            continue
        out.append(t.strip())
    return " ".join(out).strip()


def captions_proyecto(p, grupo_datos):
    cues = []
    if grupo_datos is None:
        return cues
    for pista in p.pistas(grupo_datos):
        for it in p.items(pista):
            tt = it.find(".//TrackItem")
            if tt is None or not tt.findtext("End"):
                continue
            txt = ""
            for bi in it.findall(".//BlockVector/BlockVectorItem"):
                blk = p.ref(bi)
                fd = blk.find(".//FormattedTextData") if blk is not None else None
                if fd is not None and fd.text:
                    txt += " " + texto_bloque(fd.text.strip())
            txt = txt.strip()
            if txt:
                cues.append((sec(tt.findtext("Start") or "0"), sec(tt.findtext("End")), txt))
    return sorted(cues)


def transcribir_scribe(render, cache="D:/hf-render/estilos/ed2/cache_stt"):
    """Transcripción por palabras (ElevenLabs Scribe) del render; se agrupa en bloques de ~3 palabras como los captions de Premiere."""
    import hashlib, tempfile
    os.makedirs(cache, exist_ok=True)
    key = os.path.join(cache, hashlib.md5(render.encode("utf-8")).hexdigest() + ".json")
    if os.path.exists(key):
        d = json.load(open(key, encoding="utf-8"))
    else:
        with tempfile.TemporaryDirectory() as t:
            wav = os.path.join(t, "a.mp3")
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", render, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k", wav], check=True)
            r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: " + os.environ["ELEVENLABS_API_KEY"],
                                "-F", "model_id=scribe_v1", "-F", "language_code=spa", "-F", "timestamps_granularity=word", "-F", "file=@" + wav], capture_output=True)
        d = json.loads(r.stdout.decode("utf-8"))
        json.dump(d, open(key, "w", encoding="utf-8"), ensure_ascii=False)
    pal = [w for w in d.get("words", []) if w.get("type") == "word"]
    cues, cur = [], []
    for w in pal:
        if cur and (w["start"] - cur[-1]["end"] > 0.3 or len(cur) >= 4):
            cues.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"] for x in cur))); cur = []
        cur.append(w)
    if cur:
        cues.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"] for x in cur)))
    return cues


def elegir(carpeta, render=None, prproj=None):
    pr = [prproj] if prproj else [f for f in glob.glob(os.path.join(carpeta, "*.prproj")) if not re.search(r"sin t[ií]tulo|untitled", os.path.basename(f), re.I)]
    cand = [f for f in glob.glob(os.path.join(carpeta, "*.mp4")) if not re.search(r"low|whatsapp|9x16|9\.16|1x1|^C\d{4}|test|prueba", os.path.basename(f), re.I)]
    cand = [f for f in cand if (dur(f) or 0) > 15]
    if render:
        cand = [render]
    return pr, cand


def sec_principal(p, objetivo):
    """Secuencia (de las de 2+ pistas de video) cuya duración más se parece a la del render."""
    mejor = None
    for s, nombre, nv in p.secuencias():
        if nv < 1:
            continue
        grupos = [p.ref(g.find("Second")) for g in s.find("TrackGroups")]
        d = 0
        for pi in p.pistas(grupos[0]):
            for it in p.items(pi):
                tt = it.find(".//TrackItem")
                if tt is not None and tt.findtext("End"):
                    d = max(d, sec(tt.findtext("End")))
        sc = abs(d - objetivo) if objetivo else -d
        if mejor is None or sc < mejor[0]:
            mejor = (sc, s, nombre, grupos, d)
    return mejor


def construir(p, grupos):
    video = []
    for ti, pista in enumerate(p.pistas(grupos[0])):
        for it in p.items(pista):
            tt = it.find(".//TrackItem")
            if tt is None or not tt.findtext("End"):
                continue
            sc = it.find(".//SubClip")
            if sc is None or sc.get("ObjectRef") is None:
                continue
            i = p.info_item(it)
            esc, zoom, pos, opa, otros = resumen_clip(i)
            nombre = i["nombre"] or ""
            video.append(dict(pista=ti, ini=i["inicio"], fin=i["fin"], nombre=nombre, src_in=i["src_in"], src_out=i["src_out"], escala=esc,
                              zoom=zoom, pos=pos, opa=opa, otros=otros,
                              ajuste="ajuste" in nombre.lower(), grafico=nombre.lower().endswith(APOYO_EXT) or "mate" in nombre.lower()))
    audio = []
    for ti, pista in enumerate(p.pistas(grupos[1])):
        for it in p.items(pista):
            tt = it.find(".//TrackItem")
            if tt is None or not tt.findtext("End"):
                continue
            sc = it.find(".//SubClip")
            nombre = p.ref(sc).findtext("Name") if sc is not None and sc.get("ObjectRef") else "?"
            vol = []
            comps = it.find(".//Components")
            ch = p.ref(comps) if comps is not None else None
            if ch is not None:
                for cr in ch.findall(".//Components/Component"):
                    c = p.ref(cr)
                    for pr in c.findall(".//Params/Param"):
                        pp = p.ref(pr)
                        if pp is not None and (pp.findtext("Name") or "").strip() in ("Nivel", "Volumen", "Level") and pp.findtext("Keyframes"):
                            ks = [k.split(",") for k in pp.findtext("Keyframes").split(";") if k.strip()]
                            t0 = int(ks[0][0])
                            vol = [(round((int(k[0]) - t0) / T, 2), float(k[1])) for k in ks]
            info = p.info_item(it)
            audio.append(dict(pista=ti, ini=sec(tt.findtext("Start") or "0"), fin=sec(tt.findtext("End")), nombre=nombre, src_in=info["src_in"], vol=vol))
    return video, audio


def analizar_carpeta(carpeta, render=None, prproj=None, srt=None):
    pr, cand = elegir(carpeta, render, prproj)
    mejor = None
    for f in pr:
        p = P(f)
        for r in (cand or [None]):
            d = dur(r) if r else None
            m = sec_principal(p, d)
            if m and (mejor is None or m[0] < mejor[0]):
                mejor = (m[0], f, r, p, m)
    if mejor is None:
        return dict(error="sin proyecto")
    _, fpr, frender, p, m = mejor
    _, s, nombre_seq, grupos, dseq = m
    video, audio = construir(p, grupos)
    res = dict(carpeta=os.path.basename(carpeta), prproj=os.path.basename(fpr), secuencia=nombre_seq, duracion_seq=dseq, render=os.path.basename(frender) if frender else None,
               duracion_render=dur(frender) if frender else None)
    # voz
    cues = []
    cues = captions_proyecto(p, grupos[2] if len(grupos) > 2 else None)
    res["transcripcion"] = "captions del proyecto" if cues else None
    if not cues:
        srt = srt or (glob.glob(frender + ".srt") + glob.glob(os.path.splitext(frender or "")[0] + ".srt") + glob.glob(os.path.join(carpeta, "*.srt")) or [None])[0]
        if srt and os.path.exists(srt):
            cues = leer_srt(srt)
            res["transcripcion"] = "SRT " + os.path.basename(srt)
    if not cues and frender:
        try:
            cues = transcribir_scribe(frender)
            res["transcripcion"] = "STT Scribe (el proyecto no tiene captions ni SRT)"
        except Exception as e:
            res["transcripcion"] = "sin transcripción: " + str(e)[:60]
    fr = frases(cues) if cues else []
    res["frases"] = len(fr)
    res["palabras"] = sum(len(t.split()) for _, _, t in cues)
    # capas
    pistas_video = sorted({v["pista"] for v in video})
    aroll_pista = None
    # A-roll = la pista con más clips de cámara (C####/IMG) que sostiene la voz
    cuenta = {}
    for v in video:
        if re.match(r"^(C\d{4}|IMG_|WhatsApp)", v["nombre"], re.I) and not v["ajuste"]:
            cuenta[v["pista"]] = cuenta.get(v["pista"], 0) + 1
    aroll_pista = max(cuenta, key=cuenta.get) if cuenta else (min(pistas_video) if pistas_video else 0)
    aroll = sorted([v for v in video if v["pista"] == aroll_pista and not v["ajuste"]], key=lambda v: v["ini"])
    nombres_voz = {re.sub(r"[-_]esv2.*|\.wav$|\.MP4$|\.mov$", "", a["nombre"], flags=re.I) for a in audio if re.search(r"esv2|^C\d{4}|^IMG_", a["nombre"], re.I)}
    apoyo = [v for v in video if v["pista"] != aroll_pista and not v["ajuste"] and not v["grafico"]]
    graficos = [v for v in video if v["grafico"]]
    res["aroll_pista"] = aroll_pista
    res["aroll_clips"] = len(aroll)
    res["apoyo_clips"] = len(apoyo)
    res["graficos"] = len(graficos)
    res["ajuste"] = [v["nombre"] for v in video if v["ajuste"]]
    # --- cortes en A-roll y su relación con frases ---
    cortes = [v["ini"] for v in aroll[1:]]
    ini_f = np.array([a for a, _, _ in fr]) if fr else np.array([])
    fin_f = np.array([b for _, b, _ in fr]) if fr else np.array([])
    ini_c = np.array([a for a, _, _ in cues]) if cues else np.array([])
    if len(cortes) and len(ini_f):
        d_ini = np.array([c - ini_f[np.argmin(np.abs(ini_f - c))] for c in cortes])
        d_fin = np.array([c - fin_f[np.argmin(np.abs(fin_f - c))] for c in cortes])
        d_cue = np.array([c - ini_c[np.argmin(np.abs(ini_c - c))] for c in cortes])
        en_pausa = np.mean([any(b < c < a2 for (a, b, _), (a2, b2, _) in zip(fr, fr[1:])) for c in cortes])
        interior = np.mean([any(a + 0.2 < c < b - 0.2 for a, b, _ in fr) for c in cortes])
        res["cortes_aroll"] = dict(
            n=len(cortes),
            pct_en_inicio_de_frase_2f=round(float(np.mean(np.abs(d_ini) <= 0.084)) * 100, 1),
            pct_en_fin_de_frase_2f=round(float(np.mean(np.abs(d_fin) <= 0.084)) * 100, 1),
            pct_en_inicio_de_subtitulo_2f=round(float(np.mean(np.abs(d_cue) <= 0.084)) * 100, 1),
            pct_entre_frases_pausa=round(float(en_pausa) * 100, 1), pct_dentro_de_una_frase=round(float(interior) * 100, 1),
            adelanto_mediano_vs_subtitulo_ms=int(np.median(d_cue) * 1000))
    # --- saltos de material (silencios o repeticiones eliminados) ---
    saltos = []
    for a, b in zip(aroll, aroll[1:]):
        if a["nombre"] == b["nombre"] and a["src_out"] is not None and b["src_in"] is not None:
            saltos.append(round(b["src_in"] - a["src_out"], 2))
    if saltos:
        res["saltos_material_s"] = dict(n=len(saltos), mediana=float(np.median(saltos)), p25=float(np.percentile(saltos, 25)), p75=float(np.percentile(saltos, 75)),
                                       pct_continuos=round(float(np.mean(np.abs(saltos) < 0.05)) * 100, 1), max=max(saltos))
    # --- escala del A-roll ---
    esc_seq = [(v["ini"], v["fin"], v["escala"] if v["escala"] else 100.0, v["zoom"]) for v in aroll]
    res["escala_aroll"] = [round(e[2], 1) for e in esc_seq]
    zoomed = [e for e in esc_seq if e[2] > 101]
    res["escala_stats"] = dict(pct_clips_con_zoom=round(100 * len(zoomed) / max(1, len(esc_seq)), 1),
                               mediana_zoom=float(np.median([e[2] for e in zoomed])) if zoomed else None,
                               rango=(min(e[2] for e in esc_seq), max(e[2] for e in esc_seq)) if esc_seq else None,
                               animados=[(round(e[0], 2), e[3][0][1], e[3][-1][1], round(e[1] - e[0], 2)) for e in esc_seq if e[3]])
    runs = []
    cur, n = None, 0
    for e in esc_seq:
        t = e[2] > 101
        if t == cur:
            n += 1
        else:
            if cur is not None:
                runs.append(n)
            cur, n = t, 1
    runs.append(n)
    res["escala_stats"]["largo_de_rachas_mediana"] = float(np.median(runs)) if runs else None
    # posición del inicio de cada clip con zoom respecto a la frase
    if len(fr):
        pos = []
        for e in zoomed:
            for a, b, t in fr:
                if a - 0.05 <= e[0] <= b:
                    pos.append(round((e[0] - a) / max(b - a, 0.1), 2)); break
        res["escala_stats"]["inicio_zoom_posicion_en_frase_mediana"] = float(np.median(pos)) if pos else None
        pos2 = []
        for e in esc_seq:
            if e[2] <= 101:
                for a, b, t in fr:
                    if a - 0.05 <= e[0] <= b:
                        pos2.append(round((e[0] - a) / max(b - a, 0.1), 2)); break
        res["escala_stats"]["inicio_plano_ancho_posicion_en_frase_mediana"] = float(np.median(pos2)) if pos2 else None
    # --- planos de apoyo vs voz ---
    ap = []
    for v in sorted(apoyo, key=lambda v: v["ini"]):
        habla = " ".join(t for a, b, t in cues if b > v["ini"] and a < v["fin"])
        f_idx = next((k for k, (a, b, t) in enumerate(fr) if a - 0.05 <= v["ini"] <= b), None)
        off = round(v["ini"] - fr[f_idx][0], 2) if f_idx is not None else None
        rel = round((v["ini"] - fr[f_idx][0]) / max(fr[f_idx][1] - fr[f_idx][0], 0.1), 2) if f_idx is not None else None
        ap.append(dict(ini=round(v["ini"], 2), fin=round(v["fin"], 2), dur=round(v["fin"] - v["ini"], 2), pista=v["pista"], nombre=v["nombre"][:50], escala=v["escala"],
                       opa_kf=v["opa"], frase=(fr[f_idx][2][:70] if f_idx is not None else None), offset_en_frase_s=off, pos_rel=rel, habla=habla[:110]))
    res["apoyo"] = ap
    if ap:
        dm = [a["dur"] for a in ap]
        cubre = sum(a["dur"] for a in ap)
        res["apoyo_stats"] = dict(n=len(ap), dur_mediana=float(np.median(dm)), dur_p25=float(np.percentile(dm, 25)), dur_p75=float(np.percentile(dm, 75)),
                                  cobertura_pct_del_video=round(100 * cubre / max(res["duracion_seq"], 1), 1),
                                  pos_rel_mediana=float(np.median([a["pos_rel"] for a in ap if a["pos_rel"] is not None])) if any(a["pos_rel"] is not None for a in ap) else None,
                                  offset_mediano_s=float(np.median([a["offset_en_frase_s"] for a in ap if a["offset_en_frase_s"] is not None])) if any(a["offset_en_frase_s"] is not None for a in ap) else None)
        if fr:
            res["apoyo_stats"]["pct_frases_con_apoyo"] = round(100 * len({id(next((f for f in fr if f[0] - 0.05 <= a["ini"] <= f[1]), None)) for a in ap}) / max(1, len(fr)), 1)
    # --- gráficos ---
    gr = []
    for v in sorted(graficos, key=lambda v: v["ini"]):
        habla = " ".join(t for a, b, t in cues if b > v["ini"] and a < v["fin"])
        gr.append(dict(ini=round(v["ini"], 2), dur=round(v["fin"] - v["ini"], 2), nombre=v["nombre"][:40], opa_kf=v["opa"], pos_kf=(v["pos"] or [])[:4], escala=v["escala"], habla=habla[:90]))
    res["graficos_lista"] = gr
    # --- sonido: SFX vs cortes y entradas ---
    eventos = sorted(set([round(v["ini"], 2) for v in aroll[1:]] + [round(v["ini"], 2) for v in apoyo] + [round(v["ini"], 2) for v in graficos]))
    sfx = [a for a in audio if SFX_RE.search(a["nombre"]) and not re.search(r"esv2", a["nombre"])]
    musica = [a for a in audio if not SFX_RE.search(a["nombre"]) and not re.search(r"esv2|\.mp4$|\.mov$", a["nombre"], re.I) and a["nombre"].lower().endswith((".wav", ".mp3", ".aif", ".aiff"))]
    res["sfx"] = []
    for a in sorted(sfx, key=lambda a: a["ini"]):
        if eventos:
            e = min(eventos, key=lambda e: abs(e - a["ini"])); res["sfx"].append(dict(t=round(a["ini"], 2), nombre=a["nombre"][:30], vs_evento_cercano_ms=int((a["ini"] - e) * 1000), dur=round(a["fin"] - a["ini"], 2)))
    if res["sfx"]:
        d = np.array([x["vs_evento_cercano_ms"] for x in res["sfx"]])
        res["sfx_stats"] = dict(n=len(d), mediana_ms=int(np.median(d)), p25=int(np.percentile(d, 25)), p75=int(np.percentile(d, 75)),
                                pct_antes_del_evento=round(float(np.mean(d < -20)) * 100, 1), nombres=sorted({x["nombre"] for x in res["sfx"]})[:8])
    res["musica"] = [dict(nombre=a["nombre"][:60], ini=round(a["ini"], 2), fin=round(a["fin"], 2), vol_kf=a["vol"][:14]) for a in musica]
    # música/voz: del render, tempo
    if frender:
        try:
            from analiza_prproj import beats_audio, alineacion
            tempo, b, o = beats_audio(frender)
            res["tempo_bpm"] = round(tempo, 1)
            res["alineacion_cortes_aroll"] = alineacion(cortes, b, o)
        except Exception as e:
            res["tempo_bpm"] = f"error {str(e)[:40]}"
    def sync(ev, ref, ventana=0.084, n=400):
        ev = np.array(sorted(ev)); ref = np.array(sorted(ref))
        if len(ev) < 3 or len(ref) < 3:
            return None
        d = np.array([e - ref[np.argmin(np.abs(ref - e))] for e in ev])
        rng = np.random.default_rng(1)
        base = np.mean([np.mean([abs(r - ref[np.argmin(np.abs(ref - r))]) <= ventana for r in rng.uniform(ev.min(), ev.max(), len(ev))]) for _ in range(n // 8)])
        return dict(n=len(ev), real_pct=round(float(np.mean(np.abs(d) <= ventana)) * 100, 1), azar_pct=round(float(base) * 100, 1),
                    mediana_ms=int(np.median(d) * 1000), p25_ms=int(np.percentile(d, 25) * 1000), p75_ms=int(np.percentile(d, 75) * 1000))
    ini_sub = [a for a, _, _ in cues]
    fin_sub = [b for _, b, _ in cues]
    res["sync"] = dict(
        cortes_aroll_vs_inicio_subtitulo=sync(cortes, ini_sub), cortes_aroll_vs_fin_subtitulo=sync(cortes, fin_sub),
        entrada_apoyo_vs_inicio_subtitulo=sync([a["ini"] for a in ap], ini_sub), salida_apoyo_vs_fin_subtitulo=sync([a["fin"] for a in ap], fin_sub),
        entrada_grafico_vs_inicio_subtitulo=sync([g["ini"] for g in gr], ini_sub),
        inicio_zoom_vs_inicio_subtitulo=sync([e[0] for e in zoomed], ini_sub))
    res["crudo"] = dict(cortes=[round(c, 2) for c in cortes], zoom_ini=[round(e[0], 2) for e in zoomed], ancho_ini=[round(e[0], 2) for e in esc_seq if e[2] <= 101],
                        apoyo=[(a["ini"], a["fin"]) for a in ap], graficos=[(g["ini"], g["dur"]) for g in gr], cues=[(round(a, 2), round(b, 2), t) for a, b, t in cues])
    if cues:
        pal = sum(len(t.split()) for _, _, t in cues)
        res["voz"] = dict(palabras=pal, palabras_por_s=round(pal / max(res["duracion_seq"], 1), 2), cobertura_habla_pct=round(100 * sum(b - a for a, b, _ in cues) / max(res["duracion_seq"], 1), 1),
                          pausas_mayores_0_5s=int(sum(1 for (a, b, _), (a2, b2, _) in zip(cues, cues[1:]) if a2 - b > 0.5)))
    # --- guion de edición legible ---
    L = []
    marks = sorted(set([0.0] + [round(v["ini"], 2) for v in video if not v["ajuste"]]))
    for k, t0 in enumerate(marks):
        t1 = marks[k + 1] if k + 1 < len(marks) else res["duracion_seq"]
        if t1 - t0 < 0.08:
            continue
        mid = (t0 + t1) / 2
        act = [v for v in video if v["ini"] <= mid < v["fin"] and not v["ajuste"]]
        a = next((v for v in act if v["pista"] == aroll_pista), None)
        partes = []
        if a:
            e = a["escala"] if a["escala"] else 100
            z = f" zoom {a['zoom'][0][1]:.0f}->{a['zoom'][-1][1]:.0f}" if a["zoom"] else ""
            partes.append(f"A:{a['nombre'][:12]} {e:.0f}%{z}")
        for v in act:
            if v is a:
                continue
            tag = "G" if v["grafico"] else "B"
            partes.append(f"{tag}:{v['nombre'][:34]}" + (f" {v['escala']:.0f}%" if v["escala"] else ""))
        habla = " ".join(t for aa, bb, t in cues if bb > t0 + 0.05 and aa < t1 - 0.05)
        L.append(f"{t0:7.2f}-{t1:7.2f} ({t1 - t0:4.2f}s) | {' | '.join(partes):<70.70} | {habla[:90]}")
    res["_guion"] = L
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta"); ap.add_argument("--render"); ap.add_argument("--prproj"); ap.add_argument("--srt"); ap.add_argument("--out")
    a = ap.parse_args()
    r = analizar_carpeta(a.carpeta, a.render, a.prproj, a.srt)
    guion = r.pop("_guion", [])
    nombre = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(a.carpeta))[:40]
    out = a.out or "."
    os.makedirs(out, exist_ok=True)
    json.dump(r, open(os.path.join(out, nombre + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    open(os.path.join(out, nombre + "_guion.txt"), "w", encoding="utf-8").write("\n".join(guion))
    print(json.dumps({k: v for k, v in r.items() if k not in ("apoyo", "graficos_lista", "sfx", "musica", "escala_aroll")}, ensure_ascii=False, indent=1, default=str))
