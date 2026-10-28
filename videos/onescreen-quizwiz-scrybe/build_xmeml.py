"""FCP XML (xmeml v4) de respaldo del video Rental/DaaS v3: mismos cortes, zoom, tarjetas, gráficos con alfa y audio que el .prproj,
pero SIN Lumetri (el XML de FCP7 no lo transporta). Se importa en Premiere con Archivo > Importar.
Uso: python build_xmeml.py SALIDA.xml [MOV] [WAV] [INTRO]"""
import json, os, sys
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

PLAN = json.load(open("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_16a/plan_alpha.json", encoding="utf-8"))
SRCP = json.load(open("D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/premiere/src_probe.json", encoding="utf-8"))
OUT = Path(sys.argv[1])
MOV = sys.argv[2] if len(sys.argv) > 2 else str(OUT.parent / "Rental-DaaS_graficos_alfa_4K.mov")
WAV = sys.argv[3] if len(sys.argv) > 3 else str(OUT.parent / "Rental-DaaS_mezcla.wav")
INTRO = sys.argv[4] if len(sys.argv) > 4 else str(OUT.parent / "intro_onescreen.mp4")
FPS = 24000 / 1001
fr = lambda s: round(s * FPS)
RATE = "<rate><timebase>24</timebase><ntsc>TRUE</ntsc></rate>"


def url(p):
    return "file://localhost/" + quote(p.replace("\\", "/"), safe="/:")


def tcf(tc):
    h, m, s, f = [int(x) for x in tc.replace(";", ":").split(":")]
    return (h * 3600 + m * 60 + s) * 24 + f


files = {}


def file_el(key, path, name, dur, w, h, tc=0, audio=False, ch=2):
    if key in files:
        return f'<file id="file-{key}"/>'
    files[key] = 1
    a = f'<audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>{ch}</channelcount></audio>' if audio else ""
    v = f'<video><samplecharacteristics>{RATE}<width>{w}</width><height>{h}</height><anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></video>' if w else ""
    return (f'<file id="file-{key}"><name>{escape(name)}</name><pathurl>{escape(url(path))}</pathurl>{RATE}<duration>{dur}</duration>'
            f'<timecode>{RATE}<string>00:00:00:00</string><frame>{tc}</frame><displayformat>NDF</displayformat></timecode><media>{v}{a}</media></file>')


def motion(scale, cx=0.0, cy=0.0):
    if scale is None and not cx and not cy:
        return ""
    sv = 100 if scale is None else scale
    return ('<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype>'
            f'<parameter authoringApp="PremierePro"><parameterid>scale</parameterid><name>Scale</name><valuemin>0</valuemin><valuemax>1000</valuemax><value>{sv}</value></parameter>'
            f'<parameter authoringApp="PremierePro"><parameterid>center</parameterid><name>Center</name><value><horiz>{cx:.6f}</horiz><vert>{cy:.6f}</vert></value></parameter></effect></filter>')


cid = [0]


def vitem(key, name, path, start, end, in_f, w, h, dur, tc=0, scale=None, cx=0.0, cy=0.0):
    cid[0] += 1
    return (f'<clipitem id="clipitem-{cid[0]}"><name>{escape(name)}</name><enabled>TRUE</enabled><duration>{dur}</duration>{RATE}<start>{start}</start><end>{end}</end>'
            f'<in>{in_f}</in><out>{in_f + end - start}</out>{file_el(key, path, name, dur, w, h, tc)}{motion(scale, cx, cy)}</clipitem>')


v1, v2 = [], []
cards = []
for c in PLAN["clips"]:
    k = c["src"]; v = SRCP[k]
    st = [s for s in v["probe"]["streams"] if s["codec_type"] == "video"][0]
    tc = [s["tags"]["timecode"] for s in v["probe"]["streams"] if s.get("tags", {}).get("timecode")][0]
    in_f = fr(v["ss"] + c["tin"]); s_f = fr(c["t"]); e_f = fr(c["t"] + c["dur"] - (0.3 if "card" in c else 0))
    nm = Path(v["path"]).name
    if "card" in c:
        cd = c["card"]
        cards.append(vitem(k, nm, v["path"], s_f, e_f, in_f, 3840, 2160, int(st["nb_frames"]), tcf(tc), cd["w"] / 1920 * 100.0, (cd["x"] + cd["w"] / 2) / 1920 - 0.5, (cd["y"] + cd["h"] / 2) / 1080 - 0.5))
    else:
        v1.append((s_f, vitem(k, nm, v["path"], s_f, e_f, in_f, 3840, 2160, int(st["nb_frames"]), tcf(tc), c["scale"] if c["scale"] != 100 else None)))
mov_frames = round(PLAN["END_SCENE"] * FPS)
intro_frames = 194
v2.append(vitem("mov", Path(MOV).name, MOV, 0, mov_frames, 0, 3840, 2160, mov_frames))
v1.append((mov_frames, vitem("intro", Path(INTRO).name, INTRO, mov_frames, mov_frames + intro_frames, 0, 1920, 1080, intro_frames, 0, 200.0)))
wav_dur = 45.175
wav_frames = fr(wav_dur)
total = max(mov_frames + intro_frames, wav_frames)
afile = file_el("wav", WAV, Path(WAV).name, round(wav_dur * 48000), 0, 0, 0, True)
vtracks = [''.join(x for _, x in sorted(v1)), ''.join(v2)] + cards
a_tracks = []
for ch in (1, 2):
    cid[0] += 1
    a_tracks.append(f'<track><clipitem id="clipitem-{cid[0]}"><name>{escape(Path(WAV).name)}</name><enabled>TRUE</enabled><duration>{round(wav_dur * 48000)}</duration>{RATE}<start>0</start><end>{wav_frames}</end><in>0</in><out>{wav_frames}</out>'
                    f'{afile if ch == 1 else "<file id=\"file-wav\"/>"}<sourcetrack><mediatype>audio</mediatype><trackindex>{ch}</trackindex></sourcetrack></clipitem></track>')
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><sequence id="sequence-1"><name>Rental DaaS v3</name>'
       f'<duration>{total}</duration>{RATE}<timecode>{RATE}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>'
       '<media><video><format><samplecharacteristics>' + RATE + '<width>3840</width><height>2160</height><anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>'
       + "".join(f"<track>{t}</track>" for t in vtracks) + "</video><audio>" + "".join(a_tracks) + "</audio></media></sequence></xmeml>")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(xml, encoding="utf-8")
print("escrito", OUT, len(xml) // 1024, "KB")
