"""Proyecto de Premiere (.prproj) del video Rental/DaaS RENT.0005 (v3 aprobada, voz neutra v_rv_1).

Se parte de C1186.prproj (secuencia 4K a 23,976 con 3 pistas de video y 3 de audio) y se reemplazan sus clips por:
  V1  planos originales 4K SIN colorear (cortados según plan.json, zoom con Movimiento > Escala) + intro de marca al final
  V2  capa gráfica con alfa (MOV ProRes 4444, 4K)
  V3  planos dentro de las tarjetas de ventajas (Movimiento: posición/escala), mismos planos y color que en V1
  A1  mezcla de audio (WAV, incluye el sonido de la intro)
El Lumetri de cada plano se clona del proyecto fuente que dice el Sheet "Directorio" (col. AP); si ese plano no tiene Lumetri
en su proyecto (o no hay proyecto) queda sin color.
Uso: python build_prproj.py SALIDA.prproj [MOV] [WAV] [INTRO]
NO se ha podido abrir en Premiere desde aquí: se valida solo la estructura (ids únicos, refs resueltas, gzip re-abre)."""
import copy, gzip, json, os, re, subprocess, sys, uuid
from pathlib import Path
from lxml import etree

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from prlib import load, closure
from prser import serialize

TICK = 254016000000
FT = 10594584000                    # ticks por cuadro a 23,976
FPS = 24000 / 1001
TEMPLATE = "D:/OneScreen/Contenido/2026/10. Octubre/Pruebas prproj color/C1186.prproj"
AUDIO_PROTO = "D:/OneScreen/Contenido/2026/6. Junio/Caso de éxito - Gimnasio Los Cerezos/Caso de éxito - Gimnasio los Cerezos.prproj"
B = "D:/OneScreen/Contenido/2026/"
PLAN = json.load(open("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_16a/plan_alpha.json", encoding="utf-8"))
OUT = Path(sys.argv[1])
MOV = sys.argv[2] if len(sys.argv) > 2 else str(OUT.parent / "Rental-DaaS_graficos_alfa_4K.mov")
WAV = sys.argv[3] if len(sys.argv) > 3 else str(OUT.parent / "Rental-DaaS_mezcla.wav")
INTRO = sys.argv[4] if len(sys.argv) > 4 else str(OUT.parent / "intro_onescreen.mp4")
PLANOS = bool(os.environ.get("PLANOS"))     # prproj de planos sueltos para colorear (sin gráficos ni audio)
SEQ_NAME = "RENT.0005 planos para colorear" if PLANOS else "RENT.0005 H1C1A1 neutro"

# ── fuentes (misma tabla que trims_rental3.py) y de dónde sale el color de cada una ───────────────────────────
SRCP = json.load(open("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/premiere/src_probe.json", encoding="utf-8"))
COLOR = {   # src -> (proyecto fuente con Lumetri, id del VideoClipTrackItem de ese plano) o None
    "r1": None,
    "r2": None,
    "r3": ("D:/OneScreen/Contenido/2025/8. Agosto/Caso de éxito. UCuenca/UCuenca - CE.prproj", "2689"),
    "r4": ("D:/OneScreen/Contenido/2025/9. Septiembre/Itecsur - Ecuador/Itecsur.prproj", "3494"),
    "m1": ("D:/OneScreen/Contenido/2026/7. Julio/CASO DE ÉXITO. Comfenalco/Comfenalco.prproj", "1211"),
    "m2": None,
    "m3": None,
    "m4": ("D:/OneScreen/Contenido/2025/8. Agosto/Areandina. CASO DE ÉXITO/Areandina_Caso de éxito.prproj", "2689"),
    "m5": ("D:/OneScreen/Contenido/2025/8. Agosto/Caso de éxito. UCuenca/UCuenca - CE.prproj", "2685"),
}

HASHDATA = {}      # BinaryHash -> texto base64: Premiere lo escribe solo en la PRIMERA aparición; las demás van vacías y remiten al hash


def collect_hashes(r):
    for x in r.iter():
        h = x.get("BinaryHash")
        if h and x.text and x.text.strip():
            HASHDATA.setdefault(h, x.text)


def fix_hashes(r):
    seen = set()
    for x in r.iter():
        h = x.get("BinaryHash")
        if not h:
            continue
        if h in seen:
            x.text = None
        else:
            assert h in HASHDATA, "BinaryHash sin datos: " + h
            x.text = HASHDATA[h]
            seen.add(h)


root, by = load(TEMPLATE)
collect_hashes(root)
nxt = [max(int(k) for k in by if k.isdigit()) + 1000]


def nid():
    nxt[0] += 1
    return str(nxt[0])


def newuid():
    return str(uuid.uuid4())


def X(s):
    return etree.fromstring(s)


def clone(src_by, starts, extra_map=None):
    """copia (con ids nuevos) todo lo alcanzable desde starts; devuelve (elementos, mapa viejo->nuevo)"""
    order = closure(src_by, starts)
    m = dict(extra_map or {})
    for k in order:
        e = src_by[k]
        m[k] = newuid() if e.get("ObjectUID") else nid()
        for x in e.iter():
            if x is not e and x.get("ObjectID") and x.get("ObjectID") not in m:
                m[x.get("ObjectID")] = nid()
    out = []
    for k in order:
        e = copy.deepcopy(src_by[k])
        for x in e.iter():
            for a in ("ObjectID", "ObjectUID"):
                v = x.get(a)
                if v is not None and v in m:
                    x.set(a, m[v])
            for a in ("ObjectRef", "ObjectURef"):
                v = x.get(a)
                if v is not None and v in m:
                    x.set(a, m[v])
        out.append(e)
    return out, m


def add(els):
    for e in els:
        root.append(e)


def set_text(e, tag, val):
    n = e.find(".//" + tag)
    assert n is not None, tag
    n.text = str(val)


def find1(els, tag):
    r = [e for e in els if e.tag == tag]
    return r


# ── prototipos (se copian ANTES de borrar nada) ───────────────────────────────────────────────────────────────
M_AV = "f5c0ca0f-f532-44e8-82a2-e2d45984ad95"          # C1186.MP4: video + audio (22 objetos)
M_V = "9d917820-ce15-4fbc-b3ac-2624276c4e04"           # still: solo video (8 objetos)
PROTO_AV = {k: copy.deepcopy(by[k]) for k in closure(by, [M_AV])}
PROTO_V = {k: copy.deepcopy(by[k]) for k in closure(by, [M_V])}
PROTO_MOTION = {k: copy.deepcopy(by[k]) for k in closure(by, ["273"])}
PROTO_VCLIP = copy.deepcopy(by["116"])
PROTO_AITEM = {k: copy.deepcopy(by[k]) for k in ("97",)}
rootA, byA = load(AUDIO_PROTO)
collect_hashes(rootA)
MA = [e.get("ObjectUID") for e in rootA if e.tag == "MasterClip" and (e.findtext("Name") or "").lower().endswith(".wav")][0]
PROTO_A = {k: copy.deepcopy(byA[k]) for k in closure(byA, [MA])}

# ── borrar lo que trae la plantilla: clips de la secuencia y sus elementos del proyecto ───────────────────────
proj_items = [e for e in root if e.tag == "ClipProjectItem"]
seq_item = [e for e in proj_items if (e.findtext(".//Name") or "") == "C1186"][0]
dele = set(closure(by, ["96", "97", "104", "89"]))
for e in proj_items:
    if e is not seq_item:
        dele |= set(closure(by, [e.get("ObjectUID")]))
for e in list(root):
    k = e.get("ObjectID") or e.get("ObjectUID")
    if k in dele and e is not seq_item:
        root.remove(e)
by = {(e.get("ObjectID") or e.get("ObjectUID")): e for e in root if (e.get("ObjectID") or e.get("ObjectUID"))}
rp = [e for e in root if e.tag == "RootProjectItem"][0]
for it in list(rp.iter("Item")):
    if it.get("ObjectURef") != seq_item.get("ObjectUID"):
        it.getparent().remove(it)


NL2 = bytes([10, 10])
STOP = os.environ.get("STOP", "")


def write_out():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fix_hashes(root)
    data = b'<?xml version="1.0" encoding="UTF-8" ?>\n' + serialize(root) + NL2
    with gzip.open(OUT, "wb") as f:
        f.write(data)
    print("escrito", OUT, len(data) // 1024, "KB (diagnóstico STOP=%s)" % STOP)


if STOP == "A":
    write_out(); sys.exit()

# ── masters de medios ────────────────────────────────────────────────────────────────────────────────────────
MASTERS = {}        # clave -> dict(uid, markers, vsrc, asrc, name)
item_order = [0]


def project_item(name, muid):
    item_order[0] += 1
    e = X(f'<ClipProjectItem ObjectUID="{newuid()}" ClassID="cb4e0ed7-aca1-4171-8525-e3658dec06dd" Version="1"><ProjectItem Version="1"><Node Version="1"><Properties Version="1">'
          f'<project.icon.view.grid.order>{item_order[0]}</project.icon.view.grid.order><Column.PropertyText.Label>BE.Prefs.LabelColors.1</Column.PropertyText.Label></Properties></Node><Name/></ProjectItem>'
          f'<MasterClip ObjectURef="{muid}"/></ClipProjectItem>')
    e.find(".//Name").text = name
    root.append(e)
    it = etree.SubElement(rp.find("ProjectItemContainer/Items"), "Item")
    it.set("Index", str(len(rp.findall(".//Item")) - 1)); it.set("ObjectURef", e.get("ObjectUID"))


def new_master(key, proto, protoroot, path, kind, name, tc_frames, vframes, audio_ticks, frect, extra=None):
    """kind: 'av' | 'v' | 'a'"""
    els, m = clone(proto, [protoroot])
    mc = els[0]
    assert mc.tag == "MasterClip"
    ids = {e.tag: e for e in els}
    mc.find("Name").text = name
    vticks = vframes * FT if vframes else 0
    start = tc_frames * FT
    for e in els:
        if e.tag == "ClipLoggingInfo":
            n = e.find("ClipName")
            if n is not None:
                n.text = name
            for t, v in (("MediaInPoint", start), ("MediaOutPoint", start + (vticks or audio_ticks))):
                if e.find(t) is not None:
                    e.find(t).text = str(v)
        if e.tag == "Media" and (e.find("VideoStream") is not None or e.find("AudioStream") is not None):
            win = path.replace("/", "\\")
            e.find("FilePath").text = win
            e.find("ActualMediaFilePath").text = win
            rel = e.find("RelativePath")
            if rel is not None:
                try:
                    rel.text = ".\\" + os.path.relpath(path, OUT.parent).replace("/", "\\") if os.path.splitdrive(path)[0] == os.path.splitdrive(str(OUT.parent))[0] else win
                except ValueError:
                    rel.text = win
            e.find("Title").text = name
            fk = e.find("FileKey")
            if fk is not None:
                fk.text = newuid()
            st = e.find("Start")
            if st is not None:
                st.text = str(start)
            inf = e.find("Infinite")
            if inf is not None:
                e.remove(inf)
        if e.tag == "VideoStream":
            e.find("Duration").text = str(vticks)
            e.find("FrameRect").text = frect
            if extra:
                extra(e)
        if e.tag == "AudioStream":
            e.find("Duration").text = str(audio_ticks)
            for t in ("ConformedAudioPath", "PeakFilePath"):
                n = e.find(t)
                if n is not None:
                    n.text = "C:\\Users\\Cristian Marin\\AppData\\Roaming\\Adobe\\Common\\Peak Files\\2026-10-23\\" + name + " 48000.pek"
        if e.tag == "VideoMediaSource":
            e.find("OriginalDuration").text = str(vticks)
        if e.tag == "AudioMediaSource":
            e.find("OriginalDuration").text = str(audio_ticks)
        if e.tag in ("VideoClip", "AudioClip", "TranscriptClip"):
            for c in e.iter("ClipID"):
                c.text = newuid()
            for t in ("OutPoint", "InPoint"):
                for n in e.iter(t):
                    n.getparent().remove(n)
    add(els)
    mk = [e for e in els if e.tag == "Markers"]
    vs = [e for e in els if e.tag == "VideoMediaSource"]
    asr = [e for e in els if e.tag == "AudioMediaSource"]
    MASTERS[key] = dict(uid=mc.get("ObjectUID"), markers=mk[0].get("ObjectID") if mk else None,
                        vsrc=vs[0].get("ObjectID") if vs else None, asrc=asr[0].get("ObjectID") if asr else None, name=name)
    project_item(name, mc.get("ObjectUID"))


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,nb_frames,duration,sample_rate", "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"]


def tc_to_frames(tc):
    h, m, s, f = [int(x) for x in re.split("[:;]", tc)]
    return (h * 3600 + m * 60 + s) * 24 + f


if PLANOS:
    _w = {}
    for _c in PLAN["clips"]:
        _a = SRCP[_c["src"]]["ss"] + _c["tin"]
        _lo, _hi = _w.get(_c["src"], (1e9, 0))
        _w[_c["src"]] = (min(_lo, _a), max(_hi, _a + _c["dur"]))
    _t, _cl, PLANOS_MAP = 0.0, [], []
    for _k, (_lo, _hi) in _w.items():
        _fd = float([x for x in SRCP[_k]["probe"]["streams"] if x["codec_type"] == "video"][0]["duration"])
        _lo = max(0.0, _lo - 0.5); _hi = min(_fd - 0.05, _hi + 0.5)
        _cl.append(dict(src=_k, t=_t, dur=_hi - _lo, tin=_lo - SRCP[_k]["ss"], scale=100))
        PLANOS_MAP.append(dict(src=_k, archivo=Path(SRCP[_k]["path"]).name, origen_in_s=round(_lo, 3), origen_out_s=round(_hi, 3), secuencia_inicio_s=round(_t, 3)))
        _t += _hi - _lo
    PLAN = dict(PLAN, clips=_cl)
NOMASTERS = bool(os.environ.get("NOMASTERS"))
NOCLIPS = bool(os.environ.get("NOCLIPS")) or NOMASTERS
for k, v in ([] if NOMASTERS else SRCP.items()):
    st = v["probe"]["streams"]
    vs = [s for s in st if s["codec_type"] == "video"][0]
    au = [s for s in st if s["codec_type"] == "audio"][0]
    tc = [s["tags"]["timecode"] for s in st if s.get("tags", {}).get("timecode")][0]
    nm = Path(v["path"]).name
    new_master(k, PROTO_AV, M_AV, v["path"], "av", nm, tc_to_frames(tc), int(vs["nb_frames"]),
               round(float(au["duration"]) * 48000) * 5292000 // 1, "0,0,3840,2160")


def ensure_media(path, what):
    if not os.path.exists(path):
        print("AVISO: no existe", what, path, "-> uso valores de plan")
        return None
    return probe(path)


# MOV con alfa (4K) e intro (1080p): solo video
mov_s = ensure_media(MOV, "MOV")
mov_frames = int(mov_s[0]["nb_frames"]) if mov_s else round(PLAN["END_SCENE"] * FPS)
mov_dim = (int(mov_s[0]["width"]), int(mov_s[0]["height"])) if mov_s else (3840, 2160)
intro_s = ensure_media(INTRO, "intro")
intro_frames = int(intro_s[0]["nb_frames"]) if intro_s else 194
intro_dim = (int(intro_s[0]["width"]), int(intro_s[0]["height"])) if intro_s else (1920, 1080)


def tweak_alpha(e):
    e.find("AlphaType").text = "1"
    for t in ("IgnoreAlpha", "IsStill", "OverriddenColorSpace", "IsColorSpacOverridden"):
        n = e.find(t)
        if n is not None:
            e.remove(n)
    cc = e.find("CodecType")
    cc.text = "1634755432"        # 'ap4h' ProRes 4444


def tweak_plain(e):
    n = e.find("IsStill")
    if n is not None:
        e.remove(n)
    e.find("CodecType").text = "1635148593"
    e.find("AlphaType").text = "3"


if not NOMASTERS and not PLANOS:
  new_master("mov", PROTO_V, M_V, MOV, "v", Path(MOV).name, 0, mov_frames, 0, f"0,0,{mov_dim[0]},{mov_dim[1]}", tweak_alpha)
  new_master("intro", PROTO_V, M_V, INTRO, "v", Path(INTRO).name, 0, intro_frames, 0, f"0,0,{intro_dim[0]},{intro_dim[1]}", tweak_plain)
wav_s = probe(WAV) if os.path.exists(WAV) else [{"duration": "45.175"}]
wav_dur = float(wav_s[0]["duration"])
wav_ticks = round(wav_dur * 48000) * 5292000
if not NOMASTERS and not PLANOS:
  new_master("wav", PROTO_A, MA, WAV, "a", Path(WAV).name, 0, 0, wav_ticks, "0,0,0,0")


if STOP == "B":
    write_out(); sys.exit()

# ── cadenas de componentes (Movimiento + Lumetri) ────────────────────────────────────────────────────────────
SRC_CACHE = {}


def src_project(path):
    if path not in SRC_CACHE:
        SRC_CACHE[path] = load(path)
        collect_hashes(SRC_CACHE[path][0])
    return SRC_CACHE[path]


def make_chain(src, scale=None, pos=None):
    """cadena de componentes del clip: Lumetri(s) clonados del proyecto fuente + Movimiento explícito si hay zoom/posición"""
    if src:
        sroot, sby = src_project(src[0])
        item = sby[src[1]]
        chid = item.find(".//ComponentOwner/Components").get("ObjectRef")
        els, m = clone(sby, [chid])
        chain = els[0]
        add(els)
        lum = [e for e in els if e.tag == "VideoFilterComponent"]
        for e in lum:
            assert "Lumetri" in (e.findtext(".//MatchName") or ""), e.findtext(".//MatchName")
        nlum = len(lum)
    else:
        chain = X(f'<VideoComponentChain ObjectID="{nid()}" ClassID="0970e08a-f58f-4108-b29a-1a717b8e12e2" Version="3"><DefaultMotion>true</DefaultMotion><DefaultOpacity>true</DefaultOpacity>'
                  '<DefaultMotionComponentID>1</DefaultMotionComponentID><DefaultOpacityComponentID>2</DefaultOpacityComponentID><ComponentChain Version="3"><Node Version="1"><Properties Version="1">'
                  '<MZ.ComponentChain.ActiveComponentID>2</MZ.ComponentChain.ActiveComponentID><MZ.ComponentChain.ActiveComponentParamIndex>4294967295</MZ.ComponentChain.ActiveComponentParamIndex>'
                  '</Properties></Node></ComponentChain></VideoComponentChain>')
        add([chain])
        nlum = 0
    if scale is not None or pos is not None:
        motion_id = chain.findtext("DefaultMotionComponentID")
        els, m = clone(PROTO_MOTION, ["273"])
        mot = els[0]
        add(els)
        mot.find(".//ID").text = motion_id
        for pe in els:
            nm = pe.findtext("Name")
            if pe.tag in ("PointComponentParam", "VideoComponentParam") and nm in ("Escala", "Anchura de escala", "Posici\u00f3n"):
                kf = pe.find("StartKeyframe")
                parts = kf.text.split(",")
                if nm == "Posici\u00f3n" and pos is not None:
                    parts[1] = f"{pos[0]:.6f}:{pos[1]:.6f}"
                elif nm in ("Escala", "Anchura de escala") and scale is not None:
                    parts[1] = f"{scale:.4f}"
                kf.text = ",".join(parts)
        for t in ("DefaultMotion", "DefaultMotionComponentID"):
            n = chain.find(t)
            if n is not None:
                chain.remove(n)
        cc = chain.find("ComponentChain")
        comps = cc.find("Components")
        if comps is None:
            comps = etree.SubElement(cc, "Components"); comps.set("Version", "1")
        for c in comps:
            c.set("Index", str(int(c.get("Index")) + 1))
        first = etree.Element("Component"); first.set("Index", "0"); first.set("ObjectRef", mot.get("ObjectID"))
        comps.insert(0, first)
    return chain.get("ObjectID"), nlum


# ── clips de la secuencia ─────────────────────────────────────────────────────────────────────────────────────
def vclip_item(master, name, in_f, dur_f, start_f, scale=None, pos=None, src_color=None):
    mk = MASTERS[master]
    if os.environ.get("NOCOLOR"):
        src_color = None
    if os.environ.get("COLORONLY") and master not in os.environ["COLORONLY"].split(","):
        src_color = None
    if os.environ.get("NOMOTION"):
        scale = pos = None
    chain_id, nlum = make_chain(src_color, scale, pos)
    vc = copy.deepcopy(PROTO_VCLIP)
    vc.set("ObjectID", nid())
    for t in ("OutPoint", "InPoint"):
        n = vc.find(".//" + t)
        if n is not None:
            n.getparent().remove(n)
    c = vc.find("Clip")
    c.find("MarkerOwner/Markers").set("ObjectRef", mk["markers"])
    c.find("Source").set("ObjectRef", mk["vsrc"])
    cid = c.find("ClipID")
    cid.text = newuid()
    outp = etree.Element("OutPoint"); outp.text = str((in_f + dur_f) * FT)
    inp = etree.Element("InPoint"); inp.text = str(in_f * FT)
    cid.addprevious(outp); cid.addprevious(inp)
    sub = X(f'<SubClip ObjectID="{nid()}" ClassID="e0c58dc9-dbdd-4166-aef7-5db7e3f22e84" Version="6"><Clip ObjectRef="{vc.get("ObjectID")}"/><MasterClip ObjectURef="{mk["uid"]}"/><Name/><OrigChGrp>0</OrigChGrp></SubClip>')
    sub.find("Name").text = name
    start_xml = f"<Start>{start_f * FT}</Start>" if start_f else ""
    it = X(f'<VideoClipTrackItem ObjectID="{nid()}" ClassID="368b0406-29e3-4923-9fcd-094fbf9a1089" Version="8"><ClipTrackItem Version="8"><ComponentOwner Version="1"><Components ObjectRef="{chain_id}"/></ComponentOwner>'
           f'<TrackItem Version="4">{start_xml}<End>{(start_f + dur_f) * FT}</End></TrackItem><SubClip ObjectRef="{sub.get("ObjectID")}"/></ClipTrackItem>'
           '<PixelAspectRatio>1,1</PixelAspectRatio><ToneMapSettings>{"peak":-1,"version":3}</ToneMapSettings><FrameRect>0,0,3840,2160</FrameRect></VideoClipTrackItem>')
    add([vc, sub, it])
    return it.get("ObjectID"), start_f


tracks = {t.get("ObjectUID"): t for t in root if t.tag in ("VideoClipTrack", "AudioClipTrack")}
V1, V2, V3 = "7bffe508-74f0-4293-922e-9b0391cf83de", "608682e1-1ed7-4be6-a95f-6d0dadc53d15", "7be2942a-4be5-4f4c-848d-ebb63245d878"
A1 = "11ac093e-89e7-491e-bea7-76f35bb4a23b"
placed = {V1: [], V2: [], V3: [], A1: []}
# las 4 tarjetas coinciden en el tiempo: una pista de video por plano (V3..V6) -> se clonan 3 pistas más de la plantilla
vtg = [e for e in root if e.tag == "VideoTrackGroup"][0]
tr_el = vtg.find("TrackGroup/Tracks")
cardtr = [V3]
BAKED = os.environ.get('BAKED', '1') == '1'     # las tarjetas con su plano ya vienen dentro del MOV de gráficos (3D igual que el preview)
for n in range(0 if (os.environ.get('NOTRACKS') or BAKED) else 3):
    t = copy.deepcopy(tracks[V3]); uid = newuid(); t.set("ObjectUID", uid)
    t.find(".//Track/ID").text = str(4 + n)
    for tag in ("Track", "ClipItems", "TransitionItems"):
        t.find(".//" + tag + "/Index").text = str(3 + n)
    root.append(t); tracks[uid] = t; placed[uid] = []; cardtr.append(uid)
    el = etree.SubElement(tr_el, "Track"); el.set("Index", str(3 + n)); el.set("ObjectURef", uid)
if not (os.environ.get("NOTRACKS") or BAKED):
    vtg.find("TrackGroup/NextTrackID").text = "7"
for lk in list(root.iter("Link")):
    if lk.get("ObjectRef") == "89":
        lk.getparent().remove(lk)
ncard = [0]
cmap = []                                   # tabla color
fr = lambda s: round(s * FPS)

for c in ([] if NOCLIPS else PLAN["clips"]):
    if BAKED and "card" in c:
        continue
    k = c["src"]
    ss = SRCP[k]["ss"]
    name = Path(SRCP[k]["path"]).name
    in_f = fr(ss + c["tin"])
    start_f = fr(c["t"]); end_f = fr(c["t"] + c["dur"] - (0.3 if "card" in c else 0))   # la tarjeta sale 0,3 s antes del final del plano
    dur_f = end_f - start_f
    src_color = COLOR[k]
    if "card" in c:
        card = c["card"]
        cx = (card["x"] + card["w"] / 2) / 1920; cy = (card["y"] + card["h"] / 2) / 1080
        scale = card["w"] / 1920 * 200.0 / 2.0 * 1.0       # 4K fuente en secuencia 4K: 100 % = ancho completo; la tarjeta ocupa card.w/1920 del ancho
        scale = card["w"] / 1920 * 100.0
        iid, sf = vclip_item(k, name, in_f, dur_f, start_f, scale=scale, pos=(cx, cy), src_color=src_color)
        placed[cardtr[ncard[0]]].append((sf, iid))
        row = (f"V{3 + ncard[0]} tarjeta", k, name, start_f, dur_f)
        ncard[0] += 1
    else:
        sc = c["scale"] if c["scale"] != 100 else None
        iid, sf = vclip_item(k, name, in_f, dur_f, start_f, scale=sc, src_color=src_color)
        placed[V1].append((sf, iid))
        row = ("V1", k, name, start_f, dur_f)
    cmap.append(dict(pista=row[0], clip=row[2], inicio_s=round(row[3] / FPS, 3), dur_s=round(row[4] / FPS, 3), zoom=c["scale"] if "card" not in c else "tarjeta",
                     color=(os.path.basename(src_color[0]) if src_color else "sin color")))

# V2: gráficos (MOV) de 0 a END; V1: intro al final
mov_start = 0
end_f = fr(PLAN["END_SCENE"])            # el MOV dura 1 cuadro más: se recorta a END (aquí entra la intro de marca con su sonido)
intro_start = fr(PLAN["END_SCENE"])
if not NOCLIPS and not PLANOS:
    iid, _ = vclip_item("mov", Path(MOV).name, 0, end_f, 0)
    placed[V2].append((0, iid))
    intro_start = end_f
    iid, _ = vclip_item("intro", Path(INTRO).name, 0, intro_frames, intro_start, scale=200.0 if intro_dim[0] == 1920 else None)
    placed[V1].append((intro_start, iid))
    cmap.append(dict(pista="V2", clip=Path(MOV).name, inicio_s=0, dur_s=round(end_f / FPS, 3), zoom="", color="n/a (gráficos)"))
    cmap.append(dict(pista="V1", clip=Path(INTRO).name, inicio_s=round(intro_start / FPS, 3), dur_s=round(intro_frames / FPS, 3), zoom=200, color="n/a (intro)"))

    # A1: mezcla
    wav = MASTERS["wav"]
    ach = X(f'<AudioComponentChain ObjectID="{nid()}" ClassID="3cb131d1-d3c0-47ae-a19a-bdf75ea11674" Version="4"><DefaultVol>true</DefaultVol><DefaultVolumeComponentID>1</DefaultVolumeComponentID><DefaultChannelVolumeComponentID>2</DefaultChannelVolumeComponentID>'
            '<ComponentChain Version="3"><Node Version="1"><Properties Version="1"><MZ.ComponentChain.ActiveComponentID>1</MZ.ComponentChain.ActiveComponentID><MZ.ComponentChain.ActiveComponentParamIndex>4294967295</MZ.ComponentChain.ActiveComponentParamIndex>'
            '</Properties></Node></ComponentChain><AudioChannelLayout>[{"channellabel":100},{"channellabel":101}]</AudioChannelLayout><ChannelType>1</ChannelType></AudioComponentChain>')
    sc0, sc1 = nid(), nid()
    sec = [X(f'<SecondaryContent ObjectID="{sc0}" ClassID="f9d004b5-cb04-4e2f-af6f-64fadc2c4be9" Version="1"><Content ObjectRef="{wav["asrc"]}"/><ChannelIndex>0</ChannelIndex></SecondaryContent>'),
           X(f'<SecondaryContent ObjectID="{sc1}" ClassID="f9d004b5-cb04-4e2f-af6f-64fadc2c4be9" Version="1"><Content ObjectRef="{wav["asrc"]}"/><ChannelIndex>1</ChannelIndex></SecondaryContent>')]
    aclip = X(f'<AudioClip ObjectID="{nid()}" ClassID="b8830d03-de02-41ee-84ec-fe566dc70cd9" Version="8"><Clip Version="18"><Node Version="1"><Properties Version="1"><asl.clip.label.color>6769408</asl.clip.label.color>'
              f'<asl.clip.label.name>BE.Prefs.LabelColors.1</asl.clip.label.name></Properties></Node><MarkerOwner Version="1"><Markers ObjectRef="{wav["markers"]}"/></MarkerOwner><Source ObjectRef="{wav["asrc"]}"/>'
              f'<OutPoint>{wav_ticks}</OutPoint><InPoint>0</InPoint><ClipID>{newuid()}</ClipID></Clip><SecondaryContents Version="1"><SecondaryContentItem Index="0" ObjectRef="{sc0}"/><SecondaryContentItem Index="1" ObjectRef="{sc1}"/></SecondaryContents>'
              '<AudioChannelLayout>[{"channellabel":100},{"channellabel":101}]</AudioChannelLayout></AudioClip>')
    asub = X(f'<SubClip ObjectID="{nid()}" ClassID="e0c58dc9-dbdd-4166-aef7-5db7e3f22e84" Version="6"><Clip ObjectRef="{aclip.get("ObjectID")}"/><MasterClip ObjectURef="{wav["uid"]}"/><Name/><OrigChGrp>0</OrigChGrp></SubClip>')
    asub.find("Name").text = Path(WAV).name
    aitem = copy.deepcopy(PROTO_AITEM["97"])
    aitem.set("ObjectID", nid())
    aitem.find(".//ComponentOwner/Components").set("ObjectRef", ach.get("ObjectID"))
    aitem.find(".//TrackItem/End").text = str(wav_ticks)
    aitem.find(".//SubClip").set("ObjectRef", asub.get("ObjectID"))
    aitem.find("ID").text = newuid()
    add([ach] + sec + [aclip, asub, aitem])
    placed[A1].append((0, aitem.get("ObjectID")))
    cmap.append(dict(pista="A1", clip=Path(WAV).name, inicio_s=0, dur_s=round(wav_dur, 3), zoom="", color="n/a (audio)"))

# ── enlazar las pistas ─────────────────────────────────────────────────────────────────────────────────────────
for tid, lst in placed.items():
    ti = tracks[tid].find(".//ClipItems/TrackItems")
    if ti is None:
        ci = tracks[tid].find(".//ClipItems")
        ti = etree.Element("TrackItems"); ti.set("Version", "1")
        ci.insert(0, ti)
    for c in list(ti):
        ti.remove(c)
    for i, (_, oid) in enumerate(sorted(lst)):
        e = etree.SubElement(ti, "TrackItem"); e.set("Index", str(i)); e.set("ObjectRef", oid)

# ── nombre y duraciones de la secuencia ───────────────────────────────────────────────────────────────────────
seq_end = (round(sum(c['dur'] for c in PLAN['clips']) * FPS) if PLANOS else max(intro_start + intro_frames, round(wav_dur * FPS))) * FT
for e in root:
    if e.tag in ("VideoSequenceSource", "AudioSequenceSource"):
        e.find("OriginalDuration").text = str(seq_end)
    if e.tag == "Sequence":
        for p in e.find("Node/Properties"):
            if p.tag.startswith("ExportSettings.Info.") and p.text:
                p.text = p.text.replace("1017080064000", str(seq_end)).replace("C1186", SEQ_NAME)
seq_item.find(".//ProjectItem/Name").text = SEQ_NAME
smc = by[seq_item.find("MasterClip").get("ObjectURef")]
smc.find("Name").text = SEQ_NAME
for e in root:
    if e.tag == "ClipLoggingInfo" and e.find("ClipName") is not None and e.findtext("ClipName") == "C1186":
        e.find("ClipName").text = SEQ_NAME

# ── escribir ───────────────────────────────────────────────────────────────────────────────────────────────────
OUT.parent.mkdir(parents=True, exist_ok=True)
fix_hashes(root)
data = b'<?xml version="1.0" encoding="UTF-8" ?>\n' + serialize(root) + NL2
with gzip.open(OUT, "wb") as f:
    f.write(data)
json.dump(cmap, open(OUT.with_suffix(".colormap.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if PLANOS:
    json.dump(PLANOS_MAP, open(OUT.with_suffix(".planos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito", OUT, len(data) // 1024, "KB (sin comprimir)", "| objetos nuevos hasta id", nxt[0])
