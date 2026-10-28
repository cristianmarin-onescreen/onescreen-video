"""Montaje (HyperFrames) de las piezas INTA a partir de specs.py + planos.json + la voz con Scribe. Mismo sistema del corporativo:
texto directo sobre el plano (sin cajas), cada palabra sube con transparencia, corte promedio 1,2-2 s, escena de color, tarjeta final, subtítulos solo donde no hay texto.
uso: PIEZA=INTA09 FMT=16|9|45 python -I build_inta.py"""
import json, os, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from specs import SPECS
from gfx_inta import gfx

PZ = os.environ["PIEZA"]
FMT = os.environ.get("FMT", "16")
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[FMT]
BASE = Path(r"D:\OneScreen\Contenido\2026\10. Octubre") / PZ
PROJ = BASE / "Proyecto" / f"v_{FMT}"
CORP = Path(r"D:\OneScreen\Contenido\2026\10. Octubre\Corporativo salas de reuniones\Proyecto\v_16")
SPEC = SPECS[PZ]
PLAN = json.load(open(BASE / "Proyecto" / "planos.json", encoding="utf-8"))
FPS, D, LEAD = 24, 0.10, 0.10
ACC, INK = "#3976ff", "#1a1a1a"
SAFE = {"16": dict(l=270, r=270, t=150, b=170), "9": dict(l=150, r=150, t=340, b=550), "45": dict(l=150, r=150, t=210, b=310)}[FMT]
S1 = {"16": 150, "9": 118, "45": 112}[FMT]
S2 = round(S1 * 0.46)
MAXW = W - SAFE["l"] - SAFE["r"]
words = [w for w in json.load(open(BASE / "Voz" / f"{PZ}_voz_scribe.json", encoding="utf-8"))["words"] if w.get("type") == "word"]
FIX = {"gruplos": "Gurú Plus", "rentingo": "renting o", "supernotes": "SuprNotes", "serpnotes": "SuprNotes", "qizwiz": "QuizWiz", "quizwiz": "QuizWiz", "guru": "Gurú", "area": "Areandina", "ariandina": "Areandina", "arean": "Areandina", "areandina": "Areandina", "andina": "", "ygurú": "y Gurú", "ygur00fa": "y Gurú"}


def norm(t):
    return re.sub(r"[¿?¡!.,;:«»“”\"]", "", t).lower().translate(str.maketrans("áéíóú", "aeiou"))


def snap(t):
    return round(t * FPS) / FPS


def EV(a, usar_fin=False):
    word, n = a
    k = [w for w in words if norm(w["text"]) == norm(word)] or [w for w in words if norm(w["text"]).startswith(norm(word)[:5])]
    if len(k) <= n:
        raise SystemExit(f"{PZ}: no encuentro la palabra '{word}' #{n} en la voz")
    return snap(k[n]["start"] + D - LEAD)


END = snap(words[-1]["end"] + D + 1.5)
els, js, clips = [], [], []
cnt = [0]


def nid(p):
    cnt[0] += 1
    return f"{p}{cnt[0]:02d}"


def fit(text, base, bold):
    """tamaño que cabe en el ancho seguro (Rubik: ~0,56 em por carácter en negrita, 0,5 en ligera)"""
    return min(base, MAXW / ((0.56 if bold else 0.5) * max(len(text), 1)))


def vid(src, t, t1, scale=100):
    clips.append(dict(src=src, t=round(t, 4), dur=round(t1 - t, 4), scale=scale))
    i = nid("v")
    s0 = scale / 100
    dx = (18 if len(clips) % 2 else -18) * (W / 1920)
    js.append(f'tl.fromTo("#{i}",{{scale:{s0:.3f},x:0}},{{scale:{s0 * 1.075:.3f},x:{dx:.1f},duration:{t1 - t:.3f},ease:"none"}},{t:.4f});')     # empuje de cámara lento sobre cada plano
    els.append(f'<video id="{i}" class="clip" src="media/{src}.mp4" muted playsinline data-start="{t:.4f}" data-duration="{t1 - t:.4f}" data-media-start="0" data-track-index="1" '
               f'style="transform-origin:50% 50%;transform:scale({scale / 100:.3f})"></video>')


POS = {"16": dict(bl=f"left:{SAFE['l']}px;bottom:{SAFE['b'] + 40}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);text-align:center"),
       "9": dict(bl=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 30}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);text-align:center"),
       "45": dict(bl=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:{SAFE['t'] + 20}px;text-align:left", c=f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);text-align:center")}[FMT]


POS["l"] = f"left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);text-align:left"


def pal(t0, t1, items):
    """Estilo del video de Beneficios en educación (Cris, 28-oct): palabras sueltas en negrita blanca, a media altura y al margen izquierdo, que entran una a una
    con su palabra de la voz y se quedan acumuladas en la misma línea hasta que termina la ventana; sin cajas. items = [(texto, tiempo de la palabra)]"""
    i = nid("p")
    tot = " ".join(t for t, _ in items)
    sz = min(S1 * 0.78, MAXW / (0.6 * len(tot)))
    sp = "".join(f'<span class="mk"><span class="lw pw">{t}</span></span> ' for t, _ in items)
    els.append(f'<div id="{i}" class="clip pal" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="3" style="font-size:{sz:.0f}px">{sp}</div>')
    for k, (_, tw) in enumerate(items):
        js.append(f'tl.fromTo("#{i} .mk:nth-child({k + 1}) .pw",{{yPercent:110,opacity:0}},{{yPercent:0,opacity:1,duration:1.0,ease:"power3.out"}},{max(tw, t0):.4f});')
    return i


def lines_html(lines, mask=True):
    out = ""
    for text, kind in lines:
        bold = kind == "b"
        sz = fit(text, S1 if bold else S2 * 1.25, bold)
        out += f'<div class="ln" style="font-size:{sz:.0f}px">' + " ".join((f'<span class="mk"><span class="lw {"b" if bold else "l"}">{w}</span></span>' if mask else f'<span class="lw {"b" if bold else "l"}" style="display:inline-block">{w}</span>') for w in text.split(" ")) + "</div>"
    return out


def tx(t0, t1, lines, pos="bl", cls="", track=3):
    """texto sobre plano con lettering 3D (Rental/Apple): la cámara entra desde atrás con giro suave y cada palabra se levanta con rotación; sin máscara para no aplanar el 3D"""
    i = nid("t")
    els.append(f'<div id="{i}" class="clip tx {cls}" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="{track}" style="{POS[pos]}"><div class="ti">{lines_html(lines, False)}</div></div>')
    js.append(f'tl.fromTo("#{i} .ti",{{transformPerspective:1100,z:-520,rotationX:12,rotationY:-13}},{{z:0,rotationX:0,rotationY:0,duration:1.15,ease:"power3.out"}},{t0:.4f});')
    js.append(f'tl.fromTo("#{i} .lw",{{opacity:0,scale:0.55,transformOrigin:"50% 60%"}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.7)",stagger:0.08}},{t0 + 0.05:.4f});')     # el texto aparece en pop; solo la cámara va en 3D
    return i


def bgs(t0, t1, color, track=2):
    i = nid("b")
    els.append(f'<div id="{i}" class="clip full" data-start="{t0:.4f}" data-duration="{t1 - t0:.4f}" data-track-index="{track}" style="background:{color}"></div>')
    js.append(f'tl.fromTo("#{i}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"power3.inOut"}},{t0:.4f});')
    return i


# ── ventanas con texto (no llevan subtítulo) ────────────────────────────────────────────────────
t_cierre = EV(SPEC["cierre"]["word"])
vent = []
for o in SPEC["ov"]:
    if "pal" in o:
        o = dict(o, pal=[(t, EV(w)) for t, w in o["pal"]])
    vent.append(["ov", EV(o["a"]), EV(o["b"]), o])
c = SPEC.get("color")
if c:
    vent.append(["color", EV(c["a"]), EV(c["b"]), c])
for g in SPEC.get("gfx", []):
    vent.append(["gfx", EV(g["a"]), EV(g["b"]), g])
vent.sort(key=lambda v: v[1])
for v, nx in zip(vent, vent[1:] + [["x", t_cierre, 0, 0]]):
    v[2] = min(v[2], nx[1] - (0.45 if nx[0] in ("color", "gfx") or v[0] in ("color", "gfx") else 0.12))     # el barrido de color necesita su tiempo
    v[2] = min(v[2], v[1] + {"color": 2.2, "gfx": 3.4}.get(v[0], 3.0))
    if v[0] == "gfx" and nx[0] == "gfx":          # escenas encadenadas: la siguiente barre encima, nunca se asoma un plano entre ellas
        v[2] = min(nx[1] - 0.35 + 0.5, v[1] + 3.4)
    if v[2] - v[1] < 0.9:
        print(f"AVISO {PZ}: ventana {v[0]} muy corta ({v[2] - v[1]:.2f}s) en {v[1]:.1f}s")

# ── montaje: planos por tramo; cada corte cae 2-3 cuadros antes de la palabra; zigzag 100 % / cerrado ─────
pl = [p for p in PLAN["planos"] if p["id"]]
starts = [0.0] + [snap(p["t0"] + D - LEAD) for p in pl[1:]]
ZOOM = {"16": 122, "9": 115, "45": 118}[FMT]
for k, p in enumerate(pl):
    t = starts[k]
    t1 = starts[k + 1] if k + 1 < len(pl) else t_cierre + 0.5
    vid(p.get("key", p["id"]), t, t1 + 0.04, 100 if k % 2 == 0 else ZOOM)

for kind, a, b, o in vent:
    if kind == "ov":
        if "pal" in o:
            pal(a, b, o["pal"])
        else:
            tx(a, b, o["lines"], o.get("pos", "bl"))
    elif kind == "gfx":
        cues = o.get("cues", [])
        h_, j_ = gfx(o["kind"], nid("g"), a - 0.35, b, lambda i, dflt: EV(cues[i]) if i < len(cues) else dflt, FMT, W, H, SAFE)
        els.append(h_); js.extend(j_)
    else:
        if o.get("blanca"):      # tarjeta blanca con texto azul alineado a la izquierda (referencia: Beneficios en educación)
            bgs(a - 0.35, b, "#fafafa")
            tx(a, b, [(t, k) for t, k in o["lines"]], "l", "blue", 3)
        else:
            bgs(a - 0.35, b, ACC)
            tx(a, b, [(t, k) for t, k in o["lines"]], "c", "", 3)

# ── tarjeta final (blanca): logo oficial + slogan o llamado a la acción ─────────────────────────────
LOGO = (CORP / "assets" / "onescreen-wordmark.svg").read_text(encoding="utf-8-sig")
LOGO = re.sub(r"<\?xml[^>]*\?>", "", LOGO)
LOGO = re.sub(r'\s(id|data-name)="[^"]*"', "", LOGO).replace("<svg ", '<svg class="logo" ', 1)
cz = SPEC["cierre"]
_cz = nid("b"); els.append(f'<div id="{_cz}" class="clip full" data-start="{t_cierre:.4f}" data-duration="{END - t_cierre:.4f}" data-track-index="2" style="background:#fafafa"></div>')
gid = nid("c")
if cz["slogan"]:
    inner = (f'<div class="lgbig">{LOGO}</div>'
             f'<div class="ln" style="font-size:{fit("Transforma el espacio.", S2 * 1.5, False):.0f}px"><span class="mk"><span class="lw l s1">Transforma</span></span> <span class="mk"><span class="lw l s1">el</span></span> <span class="mk"><span class="lw b s1">espacio.</span></span></div>'
             f'<div class="ln" style="font-size:{fit("Transforma el futuro.", S2 * 1.5, False):.0f}px"><span class="mk"><span class="lw l s2">Transforma</span></span> <span class="mk"><span class="lw l s2">el</span></span> <span class="mk"><span class="lw b s2">futuro.</span></span></div>')
else:
    CHAT = (f'<svg class="chat" viewBox="0 0 200 170" style="width:{round(MAXW * 0.13)}px;margin:0 0 {round(H * 0.025)}px;overflow:visible">'
            f'<path data-draw pathLength="1" class="cb" d="M30 20 H170 Q190 20 190 40 V105 Q190 125 170 125 H88 L50 155 V125 H30 Q10 125 10 105 V40 Q10 20 30 20 Z" fill="none" stroke="{ACC}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1 2"/>'
            + "".join(f'<circle class="cd" cx="{x}" cy="72" r="9" fill="{ACC}" style="transform-box:fill-box;transform-origin:center"/>' for x in (62, 100, 138)) + '</svg>')
    inner = f'<div class="lgsm">{LOGO}</div>' + CHAT + lines_html(cz["lines"], False)
els.append(f'<div id="{gid}" class="clip card ink" data-start="{t_cierre:.4f}" data-duration="{END - t_cierre:.4f}" data-track-index="3">{inner}</div>')
js.append(f'tl.fromTo("#{gid} .lw",{{opacity:0,scale:0.55,transformOrigin:"50% 60%"}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.7)",stagger:0.1}},{t_cierre + 0.45:.4f});')
js.append(f'tl.fromTo("#{gid} .logo",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.7)"}},{t_cierre:.4f});')
if not cz["slogan"]:     # la tarjeta de llamado a la acción nunca queda quieta: la burbuja se dibuja y los puntos "escriben"
    js.append(f'tl.fromTo("#{gid} .cb",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.inOut"}},{t_cierre + 0.15:.4f});')
    js.append(f'tl.fromTo("#{gid} .cd",{{opacity:0,scale:0.2}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",stagger:0.12}},{t_cierre + 0.6:.4f});')
    js.append(f'tl.to("#{gid} .cd",{{y:-12,duration:0.28,ease:"sine.inOut",yoyo:true,repeat:{max(2, int((END - t_cierre) / 0.56))},stagger:0.1}},{t_cierre + 1.1:.4f});')
if cz["slogan"]:   # las dos frases del slogan caen con la voz
    js.append(f'tl.fromTo("#{gid} .s1",{{yPercent:60,opacity:0}},{{yPercent:0,opacity:1,duration:1.0,ease:"power3.out",stagger:0.12}},{EV(("transforma", 0)):.4f});')
    js.append(f'tl.fromTo("#{gid} .s2",{{yPercent:60,opacity:0}},{{yPercent:0,opacity:1,duration:1.0,ease:"power3.out",stagger:0.12}},{EV(("transforma", 1)):.4f});')

# ── subtítulos solo fuera de las ventanas con texto y de la tarjeta ───────────────────────────────
caps = []
tapados = [(a - 0.35 if k in ("color", "gfx") else a, b) for k, a, b, _ in vent] + [(t_cierre - 0.35, END)]
per = {"16": 6, "9": 3, "45": 4}[FMT]
libres, cur = [], 0.0
for a, b in sorted(tapados):
    if a > cur:
        libres.append((cur, a))
    cur = max(cur, b)
for a, b in libres:
    ws = [w for w in words if a <= snap(w["start"] + D - LEAD) < b]
    ch = [ws[i:i + per] for i in range(0, len(ws), per)]
    for k, cc in enumerate(ch):
        t0 = max(a, snap(cc[0]["start"] + D - LEAD))
        t1 = min(b, snap(ch[k + 1][0]["start"] + D - LEAD)) if k + 1 < len(ch) else b
        if t1 - t0 > 0.2:
            txt = " ".join(FIX.get(norm(x["text"]), x["text"]).rstrip(",.") for x in cc).replace("  ", " ").strip()
            caps.append(f'<div class="clip cap" data-start="{t0:.4f}" data-duration="{t1 - t0 - 0.04:.4f}" data-track-index="5">{txt}</div>')

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
.full{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}
.tx{{position:absolute;color:#fff;font-family:'Rubik';line-height:1.0;letter-spacing:-0.035em;text-shadow:0 3px 26px rgba(0,0,0,.5),0 1px 3px rgba(0,0,0,.25)}}
.tx.ink{{color:{INK};text-shadow:none}} .tx.blue{{color:{ACC};text-shadow:none}}
.pal{{position:absolute;left:{SAFE['l']}px;right:{SAFE['r']}px;top:50%;transform:translateY(-50%);color:#fff;font-family:'Rubik';font-weight:800;line-height:1.05;letter-spacing:-0.035em;text-shadow:0 2px 18px rgba(0,0,0,.45),0 1px 2px rgba(0,0,0,.3)}}
.tx,.tx .ti,.ln{{transform-style:preserve-3d}} .ln{{display:block}} .mk{{display:inline-block;overflow:hidden;padding:0.06em 0.04em 0.14em;vertical-align:bottom}} .lw{{display:inline-block}} .b{{font-weight:700}} .l{{font-weight:300}}
.card{{position:absolute;left:{SAFE['l']}px;right:{SAFE['r']}px;top:0;height:{H}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{INK};font-family:'Rubik';letter-spacing:-0.035em;line-height:1.05}}
.card .logo{{width:100%;height:auto;display:block;color:{ACC}}}
.lgbig{{width:{round(MAXW * 0.62)}px;margin-bottom:{round(H * 0.045)}px}} .lgsm{{width:{round(MAXW * 0.34)}px;margin-bottom:{round(H * 0.05)}px}}
.gscene{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;perspective:1500px;perspective-origin:50% 50%;overflow:hidden;font-family:'Rubik'}}
.wd,.wd2{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-style:preserve-3d}}
.gscene svg .d{{stroke-dasharray:1 2}}
.gscene .nd,.gscene .pn,.gscene .bg1,.gscene .ac{{transform-box:fill-box;transform-origin:center}}
.big{{position:absolute;font-family:'Rubik';line-height:0.92;letter-spacing:-0.045em;white-space:nowrap;transform-style:preserve-3d}}
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
for sub in ("fonts", "vendor", "assets"):
    (PROJ / sub).mkdir(parents=True, exist_ok=True)
shutil.copy(CORP / "fonts" / "Rubik-variable-latin.woff2", PROJ / "fonts")
shutil.copy(CORP / "vendor" / "gsap.min.js", PROJ / "vendor")
shutil.copy(CORP / "hyperframes.json", PROJ / "hyperframes.json")
(PROJ / "index.html").write_text(html, encoding="utf-8")
cuts = starts
json.dump(dict(END_SCENE=END, clips=clips, events=dict(cierre=t_cierre, cuts=cuts, color=([v[1] for v in vent if v[0] in ("color", "gfx")] or [0])[0])), open(PROJ / "plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dur = [b - a for a, b in zip(starts, starts[1:] + [t_cierre])]
print("ok", PZ, FMT, "escena", END, "planos", len(pl), "promedio", round(sum(dur) / len(dur), 2), "min", round(min(dur), 2), "max", round(max(dur), 2))
