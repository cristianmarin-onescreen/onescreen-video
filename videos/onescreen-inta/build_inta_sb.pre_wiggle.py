r"""Montaje (HyperFrames) de una pieza INTA a partir del STORYBOARD APROBADO (<Pieza>\Proyecto\montaje_aprobado.json): una sola capa de tomas, cada toma = un plano o un motion graphic.
Los motion salen de las plantillas de estudio-video/motion (el mismo boceto del storyboard, animado): fondo vivo que deriva, formas que entran escalonadas, barrido de entrada.
Subtítulos solo en los tramos con plano. uso: PIEZA=INTA20 FMT=16|9|45 python -I build_inta_sb.py"""
import json, os, re, shutil, sys
from pathlib import Path

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI.parent.parent / "estudio-video" / "motion"))
import plantillas
from boceto import boceto_svg

PZ = os.environ["PIEZA"]
FMT = os.environ.get("FMT", "16")
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[FMT]
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre") / PZ
PROJ = BASE / "Proyecto" / f"v_{FMT}{os.environ.get('SUF', '')}"
CORP = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\Corporativo salas de reuniones\Proyecto\v_16")
_M = json.load(open(BASE / "Proyecto" / "montaje_aprobado.json", encoding="utf-8"))
MONT = _M["tomas"]
TERCIO = _M.get("tercio")      # {"nombre", "cargo", "t0", "t1"}: tercio inferior de quien habla (Cris 28-oct)
SUF = os.environ.get("SUF", "")   # carpeta de proyecto alterna (p. ej. el final con color)
FPS, D, LEAD = 24, 0.10, 0.10
ACC, INK = "#3976ff", "#1a1a1a"
SAFE = {"16": dict(l=270, r=270, t=150, b=170), "9": dict(l=150, r=150, t=340, b=550), "45": dict(l=150, r=150, t=210, b=310)}[FMT]
S1 = {"16": 150, "9": 118, "45": 112}[FMT]
words = [w for w in json.load(open(BASE / "Voz" / f"{PZ}_voz_scribe.json", encoding="utf-8"))["words"] if w.get("type") == "word"]
def _une_marca(ws):
    """Scribe separa «One Screen»: la marca siempre se escribe «OneScreen» junta (Cris, 28-oct)."""
    out, i = [], 0
    while i < len(ws):
        w = ws[i]
        if re.sub(r"\W", "", w["text"]).lower() == "one" and i + 1 < len(ws) and re.sub(r"\W", "", ws[i + 1]["text"]).lower() == "screen":
            out.append(dict(w, text="OneScreen" + re.sub(r"^\w+", "", ws[i + 1]["text"]).replace("Screen", ""), end=ws[i + 1]["end"])); i += 2
        else:
            out.append(w); i += 1
    return out


words = _une_marca(words)
FIX = {"gruplos": "Gurú Plus", "guru": "Gurú", "rentingo": "renting o"}


def norm(t):
    return re.sub(r"[¿?¡!.,;:«»“”\"]", "", t).lower().translate(str.maketrans("áéíóú", "aeiou"))


def snap(t):
    return round(t * FPS) / FPS


END = snap(words[-1]["end"] + D + 1.5)
els, js, clips = [], [], []
cnt = [0]


def nid(p):
    cnt[0] += 1
    return f"{p}{cnt[0]:02d}"


def vid(src, t, t1, scale=100):
    clips.append(dict(src=src, t=round(t, 4), dur=round(t1 - t, 4), scale=scale))
    i = nid("v")
    s0 = scale / 100
    dx = (18 if len(clips) % 2 else -18) * (W / 1920)
    js.append(f'tl.fromTo("#{i}",{{scale:{s0:.3f},x:0}},{{scale:{s0 * 1.075:.3f},x:{dx:.1f},duration:{t1 - t:.3f},ease:"none"}},{t:.4f});')
    els.append(f'<video id="{i}" class="clip" src="media/{src}.mp4" muted playsinline data-start="{t:.4f}" data-duration="{t1 - t:.4f}" data-media-start="0" data-track-index="1" '
               f'style="transform-origin:50% 50%;transform:scale({scale / 100:.3f})"></video>')


# área de contenido de un motion (los bocetos son de 1280x720; se recorta a x 80..1200 y se centra dentro de la zona segura)
CW = W - SAFE["l"] - SAFE["r"]
CH = CW * 720 / 1120
CY = (SAFE["t"] + (H - SAFE["b"])) / 2


def motion(t0, t1, plantilla, params):
    spec, _ = plantillas.boceto(plantilla, params)
    i = nid("m")
    fondo = spec["fondo"]
    bg = boceto_svg({"fondo": fondo, "formas": []}).replace("<svg ", f'<svg preserveAspectRatio="xMidYMid slice" style="width:{W}px;height:{H}px;display:block" ', 1)
    ct = boceto_svg({"fondo": "none", "formas": spec["formas"]}, anim=True).replace('viewBox="0 0 1280 720"', 'viewBox="80 0 1120 720"', 1)
    ct = ct.replace("<svg ", f'<svg style="position:absolute;left:{SAFE["l"]}px;top:{CY - CH / 2:.0f}px;width:{CW}px;height:{CH:.0f}px;overflow:visible" ', 1)
    els.append(f'<div id="{i}" class="clip mo" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="2"><div class="mbg">{bg}</div>{ct}</div>')
    n = max(1, ct.count('class="f"'))
    dur = t1 - t0
    st = min(0.13, max(0.04, dur * 0.45 / n))
    js.append(f'tl.fromTo("#{i} .mbg",{{scale:1.0,x:0}},{{scale:1.1,x:{-24 * W / 1920:.0f},duration:{dur:.3f},ease:"none"}},{t0:.4f});')          # fondo vivo: nunca estático
    js.append(f'tl.fromTo("#{i} .f",{{opacity:0,y:34}},{{opacity:1,y:0,duration:0.6,ease:"power3.out",stagger:{st:.3f}}},{t0 + 0.2:.4f});')
    return i


# ── tomas ───────────────────────────────────────────────────────────────────────────────────────
starts = [0.0] + [snap(t["t0"] + D - LEAD) for t in MONT[1:]]
ends = starts[1:] + [END]
ZOOM = {"16": 122, "9": 115, "45": 118}[FMT]
tapados = []
k_plano = 0
for t, a, b in zip(MONT, starts, ends):
    e = t["eleccion"]
    if e["tipo"] == "plano":
        key = f"{e['plano']}_{int(round(e['plano_in'] * 100))}"
        vid(key, a, b + 0.04, 100 if k_plano % 2 == 0 else ZOOM)
        k_plano += 1
    else:
        motion(a, b + 0.04, e["plantilla"], e["params"])
        tapados.append((a - 0.1, b))
# CTA sobre plano (si la última toma es un plano): llamado a la acción como gráfico tipo subtítulo
ult = MONT[-1]["eleccion"]
if ult["tipo"] == "plano":
    txt = os.environ.get("CTA_TXT", "")
    if txt:
        gid = nid("g")
        txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", txt)
        t_c = starts[-1]
        sid = nid("g")
        els.append(f'<div id="{sid}" class="clip scrim" data-start="{t_c - 0.2:.4f}" data-duration="{END - t_c + 0.2:.4f}" data-track-index="5"></div>')
        js.append(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:0.5,ease:"power2.out"}},{t_c - 0.2:.4f});')
        els.append(f'<div id="{gid}" class="clip cta" data-start="{t_c - 0.08:.4f}" data-duration="{END - t_c + 0.04:.4f}" data-track-index="4"><span class="mk"><span class="lw">{txt}</span></span></div>')
        js.append(f'tl.fromTo("#{gid} .lw",{{yPercent:115,opacity:0}},{{yPercent:0,opacity:1,duration:0.7,ease:"power3.out"}},{t_c - 0.08:.4f});')
        tapados.append((t_c - 0.35, END))

# ── subtítulos solo fuera de los motion y del CTA ──────────────────────────────────────────────
caps = []
per = {"16": 6, "9": 3, "45": 4}[FMT]
libres, cur = [], 0.0
for a, b in sorted(tapados):
    if a > cur:
        libres.append((cur, a))
    cur = max(cur, b)
if cur < END:
    libres.append((cur, END))
for a, b in libres:
    ws = [w for w in words if a <= snap(w["start"] + D - LEAD) < b]
    ch = [ws[i:i + per] for i in range(0, len(ws), per)]
    for k, cc in enumerate(ch):
        t0 = max(a, snap(cc[0]["start"] + D - LEAD))
        t1 = min(b, snap(ch[k + 1][0]["start"] + D - LEAD)) if k + 1 < len(ch) else min(b, cc[-1]["end"] + 0.5)
        if t1 - t0 > 0.2:
            txt = " ".join(FIX.get(norm(x["text"]), x["text"]).rstrip(",.") for x in cc).replace("  ", " ").strip()
            caps.append(f'<div class="clip cap" data-start="{t0:.4f}" data-duration="{t1 - t0 - 0.04:.4f}" data-track-index="5">{txt}</div>')

if TERCIO:
    _a, _b = TERCIO["t0"], TERCIO["t1"]
    caps.append(f'<div id="tercio" class="clip tercio" data-start="{_a:.4f}" data-duration="{_b - _a:.4f}" data-track-index="6"><span class="tn">{TERCIO["nombre"]}</span><span class="tc">{TERCIO["cargo"]}</span></div>')
    js.append(f'tl.fromTo("#tercio",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.6,ease:"power3.out"}},{_a:.4f});')
    js.append(f'tl.to("#tercio",{{opacity:0,duration:0.5,ease:"power2.in"}},{_b - 0.55:.4f});')
js.append('gsap.set("#cam",{transformOrigin:"50% 50%"});')
pts = [(0, 0, 0, 1.03), (END * .33, -0.012, 0.008, 1.045), (END * .66, 0.01, -0.01, 1.035), (END, 0.006, -0.004, 1.04)]
js.append(f'tl.set("#cam",{{x:0,y:0,scale:{pts[0][3]}}},0);')
for (t, x, y, s), (t2, x2, y2, s2) in zip(pts, pts[1:]):
    js.append(f'tl.to("#cam",{{x:{x2 * W:.1f},y:{y2 * H:.1f},scale:{s2},duration:{t2 - t:.3f},ease:"sine.inOut"}},{t:.3f});')

CAP_FS = {"16": 42, "9": 50, "45": 44}[FMT]
CAP_POS = {"16": f"left:{SAFE['l']}px;right:{SAFE['r']}px;bottom:{SAFE['b']}px", "9": f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:49%", "45": f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:63%"}[FMT]
CSS = f"""
@font-face {{ font-family:'Rubik'; src:url('fonts/Rubik-variable-latin.woff2') format('woff2'); font-weight:300 900; font-display:block; }}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10;font-family:'Rubik',sans-serif}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b10}}
#cam{{position:absolute;inset:0;width:{W}px;height:{H}px}}
video{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover}}
.mo{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;overflow:hidden}} .mbg{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:50% 50%}}
.mo svg{{font-family:'Rubik',sans-serif}}
.tercio{{position:absolute;left:{SAFE['l']}px;bottom:{SAFE['b'] + 130}px;border-left:7px solid {ACC};padding-left:22px;color:#fff;font-family:'Rubik';text-shadow:0 2px 14px rgba(0,0,0,.55)}} .tercio .tn{{display:block;font-weight:700;font-size:{round(S1 * 0.36)}px;line-height:1.1}} .tercio .tc{{display:block;font-weight:400;font-size:{round(S1 * 0.23)}px;margin-top:6px}}
.cta{{position:absolute;left:{SAFE['l']}px;right:{SAFE['r']}px;bottom:{SAFE['b'] + 20}px;color:#fff;font-family:'Rubik';text-align:center;font-weight:300;font-size:{round(S1 * 0.46)}px;letter-spacing:-0.025em;line-height:1.1;text-shadow:0 2px 16px rgba(0,0,0,.5),0 1px 3px rgba(0,0,0,.35)}}
.scrim{{position:absolute;left:0;right:0;bottom:0;height:46%;background:linear-gradient(to top,rgba(10,16,40,.62),rgba(10,16,40,0))}} .cta b{{font-weight:700}} .mk{{display:inline-block;overflow:hidden;padding:0.06em 0.04em 0.14em;vertical-align:bottom}} .lw{{display:inline-block}}
.cap{{position:absolute;{CAP_POS};text-align:center;font-family:'Rubik';font-weight:500;font-size:{CAP_FS}px;line-height:1.15;color:#fff;-webkit-text-stroke:{max(3, round(CAP_FS * 0.11))}px #000;paint-order:stroke fill;text-shadow:none;pointer-events:none}}
"""
body = chr(10).join("    " + e for e in els)
html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8" /><style>{CSS}</style></head>
<body>
<div id="stage" data-composition-id="inta" data-start="0" data-duration="{END:.4f}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
  <div id="cam">
{body}
  </div>
  {chr(10).join('  ' + c for c in caps)}
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    window.gsap.defaults({{ lazy: false }});
    const tl = window.gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in js)}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["inta"] = tl;
  }})();
  </script>
</div>
</body></html>
"""
if os.environ.get("UHD") and FMT == "16":
    html = html.replace(f'data-width="{W}" data-height="{H}"', f'data-width="{W * 2}" data-height="{H * 2}"')
    html = html.replace("</style>", f"html,body,#stage{{width:{W * 2}px!important;height:{H * 2}px!important}} #u{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform:scale(2);transform-origin:0 0;overflow:hidden}}</style>", 1)
    html = html.replace('<div id="cam">', '<div id="u"><div id="cam">', 1)
    html = html.replace('  <script src="vendor/gsap.min.js"></script>', '  </div>' + chr(10) + '  <script src="vendor/gsap.min.js"></script>', 1)
for sub in ("fonts", "vendor", "assets"):
    (PROJ / sub).mkdir(parents=True, exist_ok=True)
shutil.copy(CORP / "fonts" / "Rubik-variable-latin.woff2", PROJ / "fonts")
shutil.copy(CORP / "vendor" / "gsap.min.js", PROJ / "vendor")
shutil.copy(CORP / "hyperframes.json", PROJ / "hyperframes.json")
(PROJ / "index.html").write_text(html, encoding="utf-8")
json.dump(dict(END_SCENE=END, clips=clips, events=dict(cierre=starts[-1], cuts=starts, color=0)), open(PROJ / "plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dur = [b - a for a, b in zip(starts, ends)]
print("ok", PZ, FMT, "escena", END, "tomas", len(MONT), "planos", k_plano, "min", round(min(dur), 2), "max", round(max(dur), 2))
