# Escena 'ui': interfaces de Scrybe (tableta) y QuizWiz recreadas en HTML y animadas por dentro con una cámara 3D (dolly / paneo / inclinación),
# al estilo de la cámara 3D de After Effects. Se ejecuta con exec() desde build_v2.py (usa els, js, EV, W, H, FMT, svg, SCR_ICO, QZ_ICO, wipe_in...).
import random as _rnd

P3 = 1600                                    # perspectiva
S_FIT = {"16": 0.84, "9": 0.83, "45": 0.83}[FMT]
CYF = {"16": 0.49, "9": 0.30, "45": 0.34}[FMT]
SHIFT = (H * CYF - H / 2) / S_FIT            # px de mundo para que el panel quede a la altura CYF
PX, PY = W / 2 - 600, H / 2 - 380            # esquina del panel 1200x760 con el origen del mundo en el centro de pantalla
QX = 1500                                    # panel QuizWiz a la derecha de la tableta


def out_left(sel, t, d=0.35):
    js.append(f'tl.to("{sel}",{{opacity:0,x:-60,duration:{d},ease:"power2.in"}},{t:.4f});')


def zf(m):
    """z de dolly para que lo que está en z=0 se vea a escala S_FIT*m"""
    return P3 * (1 - 1 / (S_FIT * m))


def U(cls, style, inner="", id_=None):
    return f'<div{(" id=" + chr(34) + id_ + chr(34)) if id_ else ""} class="{cls}" style="{style}">{inner}</div>'


def qr_svg(cid, size, name):
    r = _rnd.Random(7)
    n = 29
    m = [[r.random() < 0.46 for _ in range(n)] for _ in range(n)]

    def finder(ox, oy):
        for y in range(-1, 8):
            for x in range(-1, 8):
                if 0 <= ox + x < n and 0 <= oy + y < n:
                    on = (0 <= x <= 6 and 0 <= y <= 6) and (x in (0, 6) or y in (0, 6) or (2 <= x <= 4 and 2 <= y <= 4))
                    m[oy + y][ox + x] = on
    finder(0, 0); finder(n - 7, 0); finder(0, n - 7)
    rects = "".join(f'<rect class="qm_{name}" x="{x}" y="{y}" width="1.02" height="1.02"/>' for y in range(n) for x in range(n) if m[y][x])
    return f'<svg viewBox="0 0 {n} {n}" width="{size}" height="{size}" shape-rendering="crispEdges" fill="#111">{rects}</svg>'


def nav_ico():
    return '<span class="ni"></span>'


def build_ui3d(t0, t1, cid):
    wipe_in(cid, t0)
    T = dict(grab=EV("grabar"), start=EV("start"), listo=EV("listo"), el=EV("el"), qw=EV("quizwiz"), arma=EV("arma"), esa=EV("esa"), pal=EV("palabras"),
             ej=EV("ejemplos"), ent=EV("entregarlo"), qr=EV("qr"), est=EV("estudiante"), esc=EV("escanea"), cel=EV("celular"), scr=EV("scribe"))
    TRANS = "El Sol concentra el 99,86 % de la masa del sistema solar. Los cuatro planetas gigantes reúnen casi toda la masa restante."
    words = TRANS.split(" ")
    twd = "".join(f'<span class="tw">{w}</span> ' for w in words)

    # ── tableta Scrybe ──
    bars = "".join(f'<i style="height:{round(8 + 30 * abs(__import__("math").sin(i * 0.7) * __import__("math").cos(i * 0.31)))}px"></i>' for i in range(70))
    tab = f'''<div id="pT" class="pan" style="left:{PX}px;top:{PY}px">
  <div class="bez"><div class="scr">
    <div class="sbar"><span class="sbi">{SCR_ICO}</span><b>Scrybe</b></div>
    <div id="tHome" class="lay">
      <div class="t1">Presiona el botón de inicio para comenzar</div>
      <div id="ring"><div class="in">{SCR_ICO}<span>Iniciar</span></div><i class="tp"></i><i class="rp"></i></div>
      <div class="t2">Transcribir y traducir <b>Cambiar</b></div>
    </div>
    <div id="tRec" class="lay rec" style="opacity:0">
      <div class="rtop"><span>Transcribir &amp; Traducir</span><span class="rt"><em></em>00:07</span></div>
      <div class="lg"><span class="chk0">Español</span><span class="chk1">Inglés</span><u>Resumen</u></div>
      <div class="rtx">{twd}</div>
      <div class="wave">{bars}</div>
      <div class="rbt"><span class="b1"><i></i>Detener sesión</span><span class="b2">Pausar transcripción</span></div>
      <div id="toast">Habla en tu micrófono…</div>
    </div>
    <div class="snav"><span>Biblioteca</span><span class="act"><i></i>Inicio</span><span>Configuración</span></div>
    <div id="tSave" class="lay dim" style="opacity:0"><div class="dlg" id="dlgS"><h4>Guardar sesión <b>✕</b></h4><div class="inp">Transcripción_21102026_192822</div>
      <p>¡Siéntete libre de seleccionar una opción! (Opcional)</p><div id="mkq" class="mkq"><span class="dc"></span><em></em>Crear cuestionario</div>
      <div class="bts"><span id="bCont" class="bp">Continuar</span><span class="bd">Descartar</span></div></div></div>
  </div></div>
  <div id="chip" class="chip"><b></b>Transcripción · Sistema solar</div>
</div>'''

    # ── QuizWiz ──
    qs = [("¿Qué porcentaje de la masa del sistema solar se encuentra en el Sol?", ["Más del 99 % de la masa total", "Aproximadamente el 75 % de la masa total", "Cerca del 50 % de la masa total"], 0),
          ("¿Qué tipo de planetas son Júpiter y Saturno?", ["Gigantes gaseosos de hidrógeno y helio", "Planetas terrestres compuestos de roca", "Gigantes de hielo"], 0),
          ("¿Qué contienen los cuatro planetas gigantes?", ["Casi toda la masa restante", "Muy poca masa", "Solo agua"], 0)]
    qcards = ""
    for i, (q, opts, ok) in enumerate(qs):
        os_ = "".join(f'<div class="op{" ok" if k == ok else ""}"><span class="rd"></span>{o}</div>' for k, o in enumerate(opts))
        qcards += f'<div id="qc{i}" class="qc"><div class="qh"><span class="cb"></span><label>Pregunta:</label><div class="qt">{q}</div></div><div class="ops">{os_}</div></div>'
    qz = f'''<div id="pQ" class="pan qzw" style="left:{PX + QX}px;top:{PY}px">
  <div class="qtop"><span class="qlg">{QZ_ICO}</span><b>QuizWiz</b><nav><span>Mi biblioteca</span><span class="g">Generar un examen</span><span>Actualizar</span></nav><u>Unirse quiz</u><s></s><s></s></div>
  <div class="qcard">
    <div class="qL">
      <h3>Crear un nuevo cuestionario</h3><p>Elige tu material de origen para comenzar</p><u class="ex">Probar Ejemplo</u>
      <div class="ta" id="ta"><small>Texto</small><em>Limpiar</em><div class="tx">
        <span class="ln l1">El Sol concentra el 99,86 % de la masa del sistema solar.</span> <span class="ln l2">Los cuatro planetas gigantes reúnen casi toda la masa restante.</span>
        <span class="ln l3">Júpiter y Saturno son gigantes gaseosos de hidrógeno y helio.</span></div><i class="cnt">15 Frases | 339 Palabras</i></div>
      <div class="cfg"><b>Configuración del Quiz</b><div class="sel"><label>TIPO DE PREGUNTA</label><span>Opción múltiple</span></div><div class="sel"><label>DIFICULTAD</label><span>Intermedio</span></div><div class="sel"><label>CANTIDAD</label><span>Auto</span></div></div>
      <div class="bb"><span class="bo">Borrar Contenido</span><span id="bGen" class="bg">⚡ Generar Quiz<i class="tp"></i><i class="rp"></i></span></div>
    </div>
    <div class="qR">
      <h3>Vista Previa del Quiz <i>Respuesta correcta<s class="tg"></s></i></h3>
      <div id="empty" class="empty"><div class="cl"></div><b>Esperando contenido</b><span>Una vez que generes tu quiz, las preguntas aparecerán aquí para las revisas</span></div>
      <div id="spin" class="spin"><div></div><span>Generando preguntas…</span></div>
      <div id="qlist" class="qlist">{qcards}</div>
      <div class="pub"><span id="bPub" class="bg sm">Publicar Quiz<i class="tp"></i><i class="rp"></i></span><span class="bg sm">Comparte/Guardar ▾</span></div>
    </div>
  </div>
  <div class="qfoot"><b>presentado por</b> OneScreen</div>
  <div id="dPub" class="dpub" style="opacity:0"><div class="dd"><h4>Publicando cuestionario</h4><p>Un momento — esto suele tardar unos segundos.</p>
     <div class="st1" id="st1"><s></s>Preparando los datos del cuestionario</div><div class="st1" id="st2"><s></s>Publicando cuestionario</div><div class="st1" id="st3"><s></s>Finalizando</div></div></div>
  <div id="shr" class="shr" style="opacity:0"><h4>Compartir enlace del cuestionario <b>✕</b></h4>
    <div class="sg"><div class="sl"><label>Código QR</label><div class="qbox">{qr_svg(cid, 230, "q")}</div><p>Código de acceso: <b>EJDJI1</b></p><label>Subir CSV</label><div class="csv">Haz clic para subir</div></div>
      <div class="sr"><div class="bts2"><span class="bg">Copiar mensaje</span><span class="bo">Copiar enlace</span></div><label>Plantilla de mensaje</label>
      <div class="msg"><b>Sistema solar</b><p>Lee cada pregunta con atención y elige la mejor respuesta. Asegúrate de que tu internet sea estable.</p><small>03 preguntas</small><small class="lk2">https://quizwiz.onescreensolutions.com/form/EJDJI1</small></div>
      <label>Invitar a estudiantes anteriores</label><label>Cuestionarios anteriores</label></div></div></div>
</div>'''

    # ── celular ──
    ph = f'''<div id="pH" class="pan ph" style="left:{W / 2 - 180 + QX + 150}px;top:{H / 2 - 370 + 90}px">
  <div class="pb"><div class="ps">
    <div id="cam1" class="cam"><div class="vq">{qr_svg(cid, 220, "p")}</div><i class="br tl"></i><i class="br tr"></i><i class="br bl"></i><i class="br brr"></i><div id="scan" class="scan"></div><span class="hint">Escanea el código QR</span></div>
    <div id="qsc" class="qsc"><div class="qh2"><span class="qlg">{QZ_ICO}</span><b>Sistema solar</b></div>
      <div class="qq"><small>Pregunta 1 de 3</small><b>¿Qué porcentaje de la masa del sistema solar se encuentra en el Sol?</b>
      <div class="op ok2"><span class="rd"></span>Más del 99 % de la masa total</div><div class="op"><span class="rd"></span>Aproximadamente el 75 %</div><div class="op"><span class="rd"></span>Cerca del 50 %</div></div></div>
  </div></div></div>'''

    # ── fondo y adornos ──
    r = _rnd.Random(3)
    blobs = ""
    for k in range(7):
        bx, by, bz, bs = r.randint(-500, 2600), r.randint(-420, 420), r.randint(-700, -200), r.randint(260, 520)
        col = ["#cdb6ff", "#bcd0ff", "#e5d2ff"][k % 3]
        blobs += f'<div class="blob" style="left:{W / 2 + bx - bs / 2}px;top:{H / 2 + by - bs / 2}px;width:{bs}px;height:{bs}px;background:{col};transform:translateZ({bz}px)"></div>'
    dots = f'<div class="dgrid" style="left:{W / 2 - 3200}px;top:{H / 2 - 1400}px;transform:translateZ(-900px)"></div>'

    hud_top = {"16": 44, "9": round(H * 0.60), "45": round(H * 0.60)}[FMT]
    lock_dk = lambda name, sub, ico, k: (f'<div id="hl{k}" class="hl" style="top:{hud_top}px"><div class="lk dk"><span class="sq pop">{ico}</span><span class="tx"><span class="mk"><b class="rw">{name}</b></span>'
                                         f'<span class="mk"><i class="rw">{sub}</i></span><span class="ul"></span></span></div></div>')
    hud = lock_dk("Scrybe", "Graba y transcribe en tiempo real.", SCR_ICO, 1) + lock_dk("QuizWiz", "Genera exámenes con IA en segundos.", QZ_ICO, 2)

    world = f'<div id="u3"><div id="dolly"><div id="tilt"><div id="pan"><div id="look">{dots}{blobs}{tab}{qz}{ph}</div></div></div></div></div>'
    html_ = f'<div id="{cid}" class="clip white uiS" data-start="{t0:.4f}" data-duration="{(t1 - t0 + 0.6):.4f}" data-track-index="2">{world}{hud}</div>'

    # ── cámara (lenta, con respiro) ──
    def cam(t, x, y, m, ry, rx, d=1.0, ease="power2.inOut"):
        js.append(f'tl.to("#look",{{x:{-x:.1f},y:{-y + SHIFT:.1f},duration:{d:.3f},ease:"{ease}",overwrite:"auto"}},{t:.4f});')
        js.append(f'tl.to("#dolly",{{z:{zf(m):.1f},duration:{d:.3f},ease:"{ease}",overwrite:"auto"}},{t:.4f});')
        js.append(f'tl.to("#pan",{{rotationY:{ry},duration:{d:.3f},ease:"{ease}",overwrite:"auto"}},{t:.4f});')
        js.append(f'tl.to("#tilt",{{rotationX:{rx},duration:{d:.3f},ease:"{ease}",overwrite:"auto"}},{t:.4f});')

    def tap(sel, t):
        """toque con el dedo: aparece, presiona y suelta una onda (la app es táctil, no hay mouse)"""
        js.append(f'tl.fromTo("{sel} .tp",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{t - 0.55:.4f});')
        js.append(f'tl.to("{sel} .tp",{{scale:0.8,duration:0.14,ease:"power2.in"}},{t - 0.1:.4f});')
        js.append(f'tl.fromTo("{sel} .rp",{{opacity:0.75,scale:0.5}},{{opacity:0,scale:2.6,duration:0.8,ease:"power2.out"}},{t:.4f});')
        js.append(f'tl.to("{sel} .tp",{{scale:1,duration:0.2,ease:"power2.out"}},{t + 0.06:.4f});')
        js.append(f'tl.to("{sel} .tp",{{opacity:0,duration:0.35}},{t + 0.42:.4f});')

    js.append(f'gsap.set("#u3",{{perspective:{P3},perspectiveOrigin:"50% 50%"}});')
    js.append('gsap.set("#dolly,#tilt,#pan,#look",{transformStyle:"preserve-3d"});')
    js.append(f'gsap.set("#look",{{x:0,y:{SHIFT:.1f}}});gsap.set("#dolly",{{z:{zf(0.6):.1f}}});gsap.set("#pan",{{rotationY:-14}});gsap.set("#tilt",{{rotationX:6}});')
    js.append('gsap.set("#pQ .tx",{opacity:0});')
    cam(t0, 0, 0, 1.0, -6, 2, 2.2, "power3.out")                          # llegada: dolly-in lento
    cam(T["start"] - 0.2, 0, 10, 1.1, -3, 1, 1.6)                          # deriva suave hacia el botón
    cam(T["el"] - 0.2, QX, 0, 1.0, 8, -1, 1.4, "power3.inOut")             # paneo a QuizWiz
    cam(T["arma"] + 0.25, QX + 30, 30, 1.1, 2, 0, 1.0)
    cam(T["esa"] + 0.35, QX + 300, 40, 1.32, -7, 1, 1.1)                   # empuja al resultado
    cam(T["pal"] + 0.45, QX - 230, 20, 1.28, 7, -1, 1.3)                   # deriva al texto fuente
    cam(T["ent"] - 0.3, QX, 0, 1.05, 0, 0, 0.9)
    cam(T["qr"] + 0.15, QX - 250, 70, 1.4, -6, 1, 1.0)                     # QR
    PM = {"16": 1.0, "9": 0.72, "45": 0.78}[FMT]
    cam(T["est"] - 0.15, QX + 200, 90, 1.12 * PM, -8, 1, 1.2)                   # llega el celular
    cam(T["esc"] - 0.3, QX + 190, 90, 1.3 * PM, -4, 0, 1.0)                   # encima del celular

    # ── Scrybe por dentro ──
    js.append(f'tl.fromTo("#ring",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.7,ease:"back.out(1.7)"}},{t0 + 0.4:.4f});')
    js.append(f'tl.fromTo("#tHome .t1,#tHome .t2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.6,ease:"power3.out",stagger:0.14}},{t0 + 0.45:.4f});')
    tap("#ring", T["start"])
    js.append(f'tl.to("#ring",{{scale:0.95,duration:0.1,ease:"power2.in"}},{T["start"] - 0.1:.4f});tl.to("#ring",{{scale:1,duration:0.3,ease:"back.out(2)"}},{T["start"]:.4f});')
    js.append(f'tl.to("#tHome",{{opacity:0,duration:0.25}},{T["start"] + 0.2:.4f});')
    js.append(f'tl.fromTo("#tRec",{{opacity:0}},{{opacity:1,duration:0.25}},{T["start"] + 0.2:.4f});')
    js.append(f'tl.fromTo("#toast",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{T["start"] + 0.35:.4f});')
    js.append(f'tl.to("#toast",{{opacity:0,duration:0.3}},{T["start"] + 1.0:.4f});')
    nw = len(words)
    js.append(f'tl.fromTo("#tRec .tw",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.18,ease:"power2.out",stagger:{max(0.02, (T["el"] - T["start"] - 0.5) / nw):.4f}}},{T["start"] + 0.5:.4f});')
    js.append(f'tl.fromTo("#tRec .wave i",{{scaleY:0.2}},{{scaleY:1,duration:0.26,ease:"sine.inOut",repeat:{max(1, int((T["el"] - T["start"]) / 0.5))},yoyo:true,stagger:{{each:0.02,from:"random"}}}},{T["start"] + 0.2:.4f});')
    # la transcripción despega y viaja a QuizWiz
    js.append(f'tl.fromTo("#chip",{{opacity:0,x:0,y:0,scale:0.85}},{{opacity:1,x:30,y:-30,scale:1,duration:0.4,ease:"power3.out"}},{T["el"] - 0.1:.4f});')
    js.append(f'tl.to("#chip",{{x:{QX - 270},y:-70,scale:0.95,duration:1.0,ease:"power3.inOut"}},{T["el"] + 0.35:.4f});')
    js.append(f'tl.to("#chip",{{opacity:0,scale:0.9,duration:0.3}},{T["el"] + 1.3:.4f});')
    # ── QuizWiz por dentro ──
    js.append(f'tl.fromTo("#pQ .tx",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{T["el"] + 1.2:.4f});')
    tap("#bGen", T["arma"])
    js.append(f'tl.to("#bGen",{{scale:0.94,duration:0.1}},{T["arma"] - 0.1:.4f});tl.to("#bGen",{{scale:1,duration:0.3,ease:"back.out(2)"}},{T["arma"] + 0.02:.4f});')
    js.append(f'tl.to("#empty",{{opacity:0,duration:0.2}},{T["arma"] + 0.08:.4f});')
    js.append(f'tl.fromTo("#spin",{{opacity:0}},{{opacity:1,duration:0.15}},{T["arma"] + 0.12:.4f});tl.to("#spin",{{opacity:0,duration:0.15}},{T["esa"] - 0.05:.4f});')
    js.append(f'tl.fromTo("#spin div",{{rotation:0}},{{rotation:720,duration:{max(0.4, T["esa"] - T["arma"]):.3f},ease:"none"}},{T["arma"] + 0.12:.4f});')
    js.append(f'tl.fromTo("#qlist .qc",{{opacity:0,y:40,rotationX:-14}},{{opacity:1,y:0,rotationX:0,duration:0.6,ease:"power3.out",stagger:0.4}},{T["esa"] - 0.05:.4f});')
    js.append(f'tl.fromTo("#qlist .op.ok",{{borderColor:"#d6dbe4",background:"#fff"}},{{borderColor:"#7ed957",background:"#f3fff0",duration:0.35,stagger:0.4}},{T["esa"] + 0.4:.4f});')
    js.append(f'tl.fromTo("#qlist .op.ok .rd",{{scale:0}},{{scale:1,duration:0.35,ease:"back.out(2)",stagger:0.4}},{T["esa"] + 0.45:.4f});')
    js.append(f'tl.fromTo("#pQ .ln",{{backgroundSize:"0% 100%"}},{{backgroundSize:"100% 100%",duration:0.7,ease:"power2.inOut",stagger:0.55}},{T["pal"] + 0.4:.4f});')
    # publicar
    tap("#bPub", T["ent"] - 0.05)
    js.append(f'tl.to("#bPub",{{scale:0.94,duration:0.1}},{T["ent"] - 0.15:.4f});tl.to("#bPub",{{scale:1,duration:0.3,ease:"back.out(2)"}},{T["ent"] - 0.03:.4f});')
    js.append(f'tl.fromTo("#dPub",{{opacity:0}},{{opacity:1,duration:0.25}},{T["ent"] + 0.2:.4f});tl.fromTo("#dPub .dd",{{scale:0.9,y:30}},{{scale:1,y:0,duration:0.45,ease:"back.out(1.6)"}},{T["ent"] + 0.2:.4f});')
    for k in (1, 2, 3):
        js.append(f'tl.to("#st{k} s",{{backgroundColor:"#3bb54a",borderColor:"#3bb54a",duration:0.15}},{T["ent"] + 0.3 + 0.2 * k:.4f});tl.to("#st{k}",{{opacity:1,duration:0.15}},{T["ent"] + 0.3 + 0.2 * k:.4f});')
    js.append(f'tl.to("#dPub",{{opacity:0,duration:0.25}},{T["qr"] - 0.15:.4f});')
    js.append(f'tl.fromTo("#shr",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{T["qr"] - 0.2:.4f});')
    js.append(f'tl.fromTo(".qm_q",{{opacity:0,scale:0}},{{opacity:1,scale:1,transformOrigin:"center",duration:0.25,ease:"back.out(2)",stagger:{{each:0.0018,from:"random"}}}},{T["qr"] - 0.05:.4f});')
    # celular: la interfaz de atrás se desenfoca (cambio de foco) en vez de quedar encimada
    js.append(f'tl.to("#pQ",{{filter:"blur(7px)",opacity:0.5,duration:0.9,ease:"power2.inOut"}},{T["est"] - 0.25:.4f});')
    js.append(f'tl.fromTo("#pH",{{opacity:0,y:420,rotationX:18}},{{opacity:1,y:0,rotationX:0,duration:1.1,ease:"power3.out"}},{T["est"] - 0.25:.4f});')
    js.append(f'tl.fromTo(".qm_p",{{opacity:0}},{{opacity:1,duration:0.3,stagger:{{each:0.0008,from:"center"}}}},{T["est"] + 0.6:.4f});')
    js.append(f'tl.fromTo("#pH .br",{{scale:1.3,opacity:0.3}},{{scale:1,opacity:1,duration:0.5,ease:"power3.out",stagger:0.06}},{T["est"] + 0.7:.4f});')
    js.append(f'tl.fromTo("#scan",{{y:0,opacity:0}},{{y:222,opacity:1,duration:0.6,ease:"power1.inOut",repeat:1,yoyo:true}},{T["esc"] - 0.05:.4f});')
    js.append(f'tl.to("#cam1",{{opacity:0,duration:0.25}},{T["cel"] + 0.2:.4f});')
    js.append(f'tl.fromTo("#qsc",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{T["cel"] + 0.2:.4f});')
    js.append(f'tl.fromTo("#qsc .ok2 .rd",{{scale:0}},{{scale:1,duration:0.35,ease:"back.out(2)"}},{T["cel"] + 0.75:.4f});')
    # lockups
    for k, tt in ((1, T["scr"]), (2, T["qw"])):
        js.append(f'tl.fromTo("#hl{k} .pop",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.7)"}},{tt:.4f});')
        mask_rise(f"#hl{k} .rw", tt + 0.12, 0.7, 0.1)
        js.append(f'tl.fromTo("#hl{k} .ul",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},{tt + 0.35:.4f});')
        out_left(f"#hl{k} .rw,#hl{k} .pop,#hl{k} .ul", tt + (1.8 if k == 1 else 1.0))
    js.append(f'tl.to("#{cid} #u3",{{opacity:0,x:-80,duration:0.3,ease:"power2.in"}},{t1 - 0.3:.4f});')
    return html_


UI_CSS = """
.uiS{background:linear-gradient(160deg,#fbfaff 0%,#eee9fb 100%)!important;display:block!important;padding:0!important;overflow:hidden}
#u3{position:absolute;left:0;top:0;width:100%;height:100%}
#dolly,#tilt,#pan,#look{position:absolute;left:0;top:0;width:100%;height:100%;transform-style:preserve-3d}
.dgrid{position:absolute;width:6400px;height:2800px;background-image:radial-gradient(#b9a8e6 3px,transparent 3.5px);background-size:70px 70px;opacity:.55}
.blob{position:absolute;border-radius:50%;filter:blur(40px);opacity:.55}
.pan{position:absolute;width:1200px;height:760px;transform-style:preserve-3d;font-family:Manrope,sans-serif}
.bez{position:absolute;inset:0;border-radius:44px;background:#17101f;padding:14px;box-shadow:0 60px 110px rgba(60,20,110,.28),0 8px 24px rgba(0,0,0,.2)}
.scr{position:relative;width:100%;height:100%;border-radius:30px;overflow:hidden;background:#ecdff2}
.sbar{position:absolute;left:0;top:0;width:100%;height:60px;background:#5a0b86;color:#fff;display:flex;align-items:center;gap:12px;padding:0 24px;font:700 22px Rubik}
.sbi .ico{height:26px;width:auto}.sbi .ico path{fill:#fff}
.lay{position:absolute;left:0;top:60px;width:100%;height:572px}
.dim{background:rgba(20,10,30,.55);top:0;height:100%}
.t1{position:absolute;left:0;width:100%;top:40px;text-align:center;color:#5a0b86;font:600 26px Manrope}
#ring{position:absolute;left:446px;top:100px;width:300px;height:300px;border-radius:50%;background:conic-gradient(from 200deg,#e0185a,#a31a8f,#5a0b86,#a31a8f,#e0185a);padding:18px;box-shadow:0 20px 50px rgba(110,20,150,.35)}
#ring .in{width:100%;height:100%;border-radius:50%;background:radial-gradient(circle at 40% 30%,#fff,#dfeaf6);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:#5a0b86;font:600 28px Manrope}
#ring .ico{height:92px;width:auto}#ring .ico path{fill:#6a1b9a}
.t2{position:absolute;left:0;width:100%;top:450px;text-align:center;color:#6e5b7b;font:500 22px Manrope}.t2 b{color:#7d00ba;margin-left:18px;font-weight:700}
.snav{position:absolute;left:0;bottom:0;width:100%;height:96px;background:#5a0b86;display:flex;justify-content:space-around;align-items:center;color:#d9c3ec;font:600 20px Manrope}
.snav .act{color:#fff;position:relative;display:flex;flex-direction:column;align-items:center;gap:6px}.snav .act i{width:28px;height:28px;border-radius:8px;border:3px solid #fff}
.rec{background:#fff}.rtop{display:flex;justify-content:space-between;padding:16px 28px;font:600 20px Manrope;color:#333}.rt em{display:inline-block;width:12px;height:12px;border-radius:50%;background:#e0245e;margin-right:8px}
.lg{display:flex;gap:18px;padding:0 28px;font:600 17px Manrope;align-items:center}.lg span{border:2px solid #ccc;padding:5px 12px;border-radius:8px}.lg .chk1{border-color:#5a0b86;color:#5a0b86}.lg u{margin-left:auto;text-decoration:none;background:#5a0b86;color:#fff;padding:9px 18px;border-radius:10px}
.rtx{padding:36px 40px;font:500 36px/1.4 Manrope;color:#222}.tw{display:inline-block}
.wave{position:absolute;left:28px;right:28px;bottom:84px;height:52px;background:#ececec;border-radius:8px;display:flex;align-items:center;gap:5px;padding:0 14px}.wave i{width:6px;border-radius:3px;background:#6fcf4f;transform-origin:50% 50%}
.rbt{position:absolute;left:0;width:100%;bottom:14px;display:flex;justify-content:center;gap:0;font:700 17px Manrope;color:#fff}.rbt span{background:#6a1b9a;padding:12px 26px}.rbt .b1 i{display:inline-block;width:14px;height:14px;background:#ff6b35;margin-right:10px}.rbt .b2{background:#7d00ba}
#toast{position:absolute;left:50%;margin-left:-130px;bottom:-4px;width:260px;text-align:center;background:#2a2a2a;color:#fff;padding:10px 0;border-radius:20px;font:600 17px Manrope}
.dlg{position:absolute;left:380px;top:70px;width:430px;background:#fff;border-radius:18px;padding:24px 26px;font-family:Manrope;box-shadow:0 30px 70px rgba(0,0,0,.4)}.dlg h4{margin:0 0 18px;font:700 22px Rubik;display:flex;justify-content:space-between}.dlg h4 b{font-weight:400}
.inp{border:2px solid #d8d8d8;border-radius:8px;padding:10px 12px;font:500 16px Manrope;color:#333}.dlg p{font:500 14px Manrope;color:#555;margin:16px 0 10px}
.mkq{display:flex;align-items:center;justify-content:center;gap:10px;width:180px;height:92px;margin:0 auto 18px;border:2px solid #cfcfcf;border-radius:12px;font:600 15px Manrope;flex-direction:column;position:relative}.mkq .dc{width:18px;height:18px;border:2px solid #bbb;border-radius:4px;position:absolute;left:10px;top:10px}
.bts{display:flex;gap:14px;justify-content:center}.bts span{padding:11px 28px;border-radius:8px;color:#fff;font:600 16px Manrope}.bp{background:#6a1b9a}.bd{background:#e5484d}
.tp{position:absolute;left:50%;top:50%;width:92px;height:92px;margin:-46px 0 0 -46px;border-radius:50%;background:rgba(125,0,186,.30);border:4px solid rgba(125,0,186,.85);box-shadow:0 6px 20px rgba(60,20,110,.3);opacity:0;pointer-events:none;z-index:30}
.rp{position:absolute;left:50%;top:50%;width:92px;height:92px;margin:-46px 0 0 -46px;border-radius:50%;border:5px solid #7d00ba;opacity:0;pointer-events:none;z-index:29}
.bg{position:relative}
.cur{position:absolute;left:0;top:0;width:36px;height:36px;z-index:20;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M4 2l16 9-7 2-3 7z' fill='white' stroke='black' stroke-width='1.5' stroke-linejoin='round'/></svg>") no-repeat;background-size:contain;filter:drop-shadow(0 4px 6px rgba(0,0,0,.4))}
.chip{position:absolute;left:520px;top:300px;padding:14px 22px;background:#fff;border-radius:14px;box-shadow:0 20px 50px rgba(80,20,140,.35);font:700 20px Manrope;color:#5a0b86;opacity:0;z-index:15;transform:translateZ(60px)}
.qzw{border-radius:26px;background:linear-gradient(160deg,#5b0f95,#7a1fbf);box-shadow:0 60px 110px rgba(60,20,110,.3);overflow:hidden;font-family:Manrope}
.qtop{position:absolute;left:0;top:0;width:100%;height:80px;display:flex;align-items:center;gap:14px;padding:0 30px;color:#fff;font:700 24px Rubik}.qlg{display:inline-flex;width:46px;height:46px;border-radius:50%;background:#fff;align-items:center;justify-content:center}.qlg .ico{height:26px}.qlg .ico path{fill:#6a1b9a}
.qtop nav{margin-left:60px;display:flex;gap:34px;font:600 17px Manrope}.qtop nav .g{color:#9eea78}.qtop u{margin-left:auto;text-decoration:none;background:#fff;color:#5a0b86;padding:9px 16px;border-radius:20px;font:700 14px Manrope}.qtop s{width:34px;height:34px;border-radius:50%;background:#9be15d;display:block}
.qcard{position:absolute;left:22px;top:92px;width:1156px;height:598px;background:#fff;border-radius:18px;display:flex;overflow:hidden}
.qL{width:46%;padding:22px 26px;position:relative;border-right:3px solid #8a35c8}.qL h3,.qR h3{margin:0;font:700 24px Rubik;color:#1a1a2e;display:flex;justify-content:space-between;align-items:center}.qL p{margin:4px 0 0;font:500 15px Manrope;color:#777}
.ex{position:absolute;right:26px;top:22px;text-decoration:none;border:2px solid #7d00ba;color:#7d00ba;padding:7px 14px;border-radius:8px;font:700 14px Manrope}
.ta{position:relative;margin-top:22px;height:230px;border:3px solid #7ed957;border-radius:14px;padding:24px 18px 10px}.ta small{position:absolute;left:14px;top:4px;font:600 12px Manrope;color:#888}.ta em{position:absolute;right:16px;top:-12px;background:#fff;border:1px solid #7ed957;border-radius:12px;padding:2px 12px;font:600 12px Manrope;font-style:normal;color:#7ed957}
.tx{font:500 17px/1.55 Manrope;color:#2a2a2a}.ln{background:linear-gradient(#e4d0f6,#e4d0f6) no-repeat 0 100%/0% 100%;border-radius:4px}.cnt{position:absolute;right:14px;bottom:8px;font:500 12px Manrope;color:#999;font-style:normal}
.cfg{margin-top:16px}.cfg b{font:700 16px Manrope;color:#333;display:block;margin-bottom:8px}.cfg{display:flex;flex-wrap:wrap;gap:12px}.cfg b{width:100%}.sel{flex:1;border:2px solid #e2e2e2;border-radius:10px;padding:8px 12px;font:600 15px Manrope;color:#333}.sel label{display:block;font:700 10px Manrope;color:#888;margin-bottom:4px}
.bb{position:absolute;left:26px;bottom:22px;display:flex;gap:16px}.bo{border:2px solid #cfcfcf;border-radius:10px;padding:13px 22px;font:700 15px Manrope;color:#444}.bg{background:#7ed957;border-radius:10px;padding:13px 28px;font:800 16px Manrope;color:#fff;display:inline-block}.bg.sm{padding:9px 18px;font-size:14px}
.qR{width:54%;padding:22px 26px;position:relative;background:#faf9fc}.qR h3 i{font:600 13px Manrope;color:#666;display:flex;align-items:center;gap:8px;font-style:normal}.tg{width:44px;height:22px;border-radius:12px;background:#7d00ba;display:inline-block}
.empty{position:absolute;left:0;top:150px;width:100%;text-align:center;font:500 14px Manrope;color:#888}.empty b{display:block;font:700 18px Manrope;color:#333;margin:14px 0 6px}.cl{width:56px;height:70px;border:4px solid #bbb;border-radius:10px;margin:0 auto}.empty span{display:block;padding:0 70px}
.spin{position:absolute;left:0;top:190px;width:100%;text-align:center;font:600 17px Manrope;color:#7d00ba;opacity:0}.spin div{width:54px;height:54px;border-radius:50%;border:6px solid #e4d0f6;border-top-color:#7d00ba;margin:0 auto 14px}
.qlist{position:absolute;left:26px;right:26px;top:72px;height:440px;overflow:hidden;perspective:900px}.qc{border:2px solid #ececf2;border-radius:14px;background:#fff;padding:12px 16px;margin-bottom:12px;opacity:0}.qh{display:flex;gap:10px;align-items:flex-start}.qh label{font:700 15px Manrope;color:#444;padding-top:6px}.qt{flex:1;border:2px solid #e2e2e8;border-radius:8px;padding:7px 10px;font:500 15px Manrope;color:#333}.cb{width:18px;height:18px;background:#7ed957;border-radius:4px;margin-top:6px}
.ops{margin:8px 0 0 100px}.op{display:flex;align-items:center;gap:10px;border:2px solid #d6dbe4;border-radius:8px;padding:6px 10px;margin-bottom:6px;font:500 14px Manrope;color:#333;background:#fff}.rd{width:14px;height:14px;border-radius:50%;border:2px solid #777;display:inline-block;flex:none}.op.ok .rd{background:radial-gradient(#3bb54a 45%,transparent 50%);border-color:#3bb54a}
.pub{position:absolute;right:26px;bottom:14px;display:flex;gap:10px}
.qfoot{position:absolute;left:30px;bottom:12px;color:#e7d3f7;font:500 14px Manrope}.qfoot b{font-weight:500;margin-right:6px}
.dpub{position:absolute;left:0;top:0;width:100%;height:100%;background:rgba(40,10,70,.55);display:flex;align-items:center;justify-content:center}.dd{width:470px;background:#fff;border-radius:16px;padding:26px 28px;box-shadow:0 30px 70px rgba(0,0,0,.4)}.dd h4{margin:0 0 4px;font:700 22px Rubik}.dd p{margin:0 0 16px;font:500 14px Manrope;color:#777}
.st1{display:flex;align-items:center;gap:12px;padding:10px 12px;border:2px solid #eee;border-radius:10px;margin-bottom:8px;font:600 15px Manrope;color:#444;opacity:.6}.st1 s{width:20px;height:20px;border-radius:50%;border:3px solid #cfcfcf;display:block}
.shr{position:absolute;left:22px;top:60px;width:1156px;height:640px;background:#fff;border-radius:16px;padding:20px 28px;font-family:Manrope}.shr h4{margin:0 0 16px;font:700 22px Rubik;display:flex;justify-content:space-between}.shr h4 b{font-weight:400}
.sg{display:flex;gap:30px}.sl{width:40%}.sr{flex:1}label{font:700 14px Manrope;color:#444;display:block;margin:8px 0}.qbox{border:2px solid #e8e8ee;border-radius:12px;padding:12px;display:flex;justify-content:center;background:#fff}.sl p{font:500 14px Manrope;margin:10px 0}.sl p b{color:#7d00ba}
.csv{border:3px dashed #d0d0d8;border-radius:12px;height:120px;display:flex;align-items:center;justify-content:center;font:600 15px Manrope;color:#777}.bts2{display:flex;gap:14px;margin-bottom:12px}
.msg{border:2px solid #e8e8ee;border-radius:12px;padding:14px 16px;font:500 14px Manrope;color:#555;margin-bottom:10px}.msg b{font:700 17px Manrope;color:#222}.msg p{margin:6px 0}.msg small{display:block;color:#777}.msg .lk2{color:#3bb54a}
.ph{width:360px;height:740px}.pb{position:absolute;inset:0;border-radius:56px;background:#101015;padding:14px;box-shadow:0 50px 90px rgba(40,10,90,.45);transform:translateZ(260px)}.ps{position:relative;width:100%;height:100%;border-radius:44px;overflow:hidden;background:#222}
.cam{position:absolute;inset:0;background:linear-gradient(180deg,#bcc9d4,#7f93a3)}.vq{position:absolute;left:46px;top:238px;background:#fff;padding:10px;border-radius:6px;width:240px;height:240px}
.br{position:absolute;width:56px;height:56px;border:6px solid #fff;border-radius:6px}.br.tl{left:36px;top:228px;border-right:0;border-bottom:0}.br.tr{right:36px;top:228px;border-left:0;border-bottom:0}.br.bl{left:36px;top:432px;border-right:0;border-top:0}.br.brr{right:36px;top:432px;border-left:0;border-top:0}
.scan{position:absolute;left:46px;right:46px;top:240px;height:6px;background:#7ed957;border-radius:3px;box-shadow:0 0 22px 8px rgba(126,217,87,.6);opacity:0}.hint{position:absolute;left:0;width:100%;top:120px;text-align:center;color:#fff;font:700 20px Manrope;text-shadow:0 2px 8px rgba(0,0,0,.5)}
.qsc{position:absolute;inset:0;background:#f4f1fa;opacity:0}.qh2{height:96px;background:#5b0f95;color:#fff;display:flex;align-items:flex-end;gap:12px;padding:0 20px 16px;font:700 22px Rubik}.qq{margin:22px 18px;background:#fff;border-radius:16px;padding:18px;box-shadow:0 8px 24px rgba(60,20,110,.12)}.qq small{color:#888;font:600 13px Manrope}.qq b{display:block;font:700 20px/1.25 Rubik;margin:8px 0 14px;color:#1a1a2e}.qq .op{font-size:15px;padding:10px}.qq .ok2{border-color:#3bb54a;background:#f3fff0}
.hl{position:absolute;left:0;width:100%;display:flex;justify-content:center;pointer-events:none;z-index:30}
.lk.dk{color:#0b0b14;text-shadow:none}.lk.dk .tx i{color:#4a4a5a}
"""
