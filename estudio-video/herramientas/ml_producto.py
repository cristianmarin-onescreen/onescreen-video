"""Videos de producto 9:16 para Mercado Libre (nombrados con el SKU de la publicacion).
Producto en uso (clips Gemini Omni a partir del render oficial de la ficha) + specs de la ficha + voz con guion corto estilo Apple
(Cris, 28-oct: «¿por qué no tiene voz?»; el guion se aprueba antes de generar la voz).

  python ml_producto.py recortes [SKU...]   recorta los renders de las fichas (img/<SKU>_hero.png, _prod.png)
  python ml_producto.py clips [SKU...]      genera hasta 2 clips de 10 s por SKU (veo/<SKU>_a|b.mp4; un intento por clip, cuesta dinero real)
  python ml_producto.py guiones [SKU...]    guiones de voz (estilo producto Apple) + Guiones_voz.md para aprobar
  python ml_producto.py voz [SKU...]        voz con la receta unica (cuesta creditos: solo con guion aprobado)
  python ml_producto.py build [SKU...]      escribe el proyecto HyperFrames, mezcla voz y musica
  python ml_producto.py render [SKU...]     renderiza a Exports/<SKU>.mp4
Salida: D:/OneScreen/Contenido/2026/10. Octubre/Mercado Libre/<SKU>/ y Exports/<SKU>.mp4
Regla: cada cifra sale de la ficha tecnica (Drive > Fichas tecnicas, ID <SKU>.0001). Nada inventado."""
import concurrent.futures as cf, html, json, os, re, shutil, subprocess, sys, unicodedata
import numpy as np
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
BASE = Path("D:/OneScreen/Contenido/2026/10. Octubre/Mercado Libre")
FICHAS = BASE / "fichas"
MUSICA = Path("D:/OneScreen/Contenido/2026/10. Octubre/Mezcla de música/Masterizadas")
FUENTES = REPO / "videos/onescreen-flota-ia/assets/fonts"
LOGO = REPO / "estudio-carruseles/assets/logos/OneScreen White.svg"
sys.path.insert(0, str(Path(__file__).parent))
from veo_i2v import generar  # noqa: E402

ACC, SOP = "Accesorios - Fichas técnicas/", "Soportes - Fichas técnicas/"
NO_CAMBIAR = ("Keep the product exactly as in the reference image: same shape, size, colors and materials. "
              "No text, no logos added, no extra devices, no distortion. Steady camera, slow smooth motion, no cuts. "
              "Vertical composition with the upper third calm and uncluttered. No dialogue, soft room ambience only.")

# pagina de la ficha (render oficial), nombre en pantalla, specs (valor, etiqueta) tomadas de la ficha, escenas Omni
P = {
 "A10W": dict(
    pdf=ACC + "Micrófonos/Ficha técnica OneScreen A10W", nombre="A10W", sub="Speakerphone 360",
    lema="Tu sala de juntas, ahora más inteligente.", musica="MASTER_Fashion.wav",
    specs=[("360°", "Micrófonos digitales de alta precisión"), ("15 W", "Altavoz de doble frecuencia"),
           ("IA", "Elimina ruido y eco en tiempo real"), ("20 a 100 m²", "De cobertura, para 6 a 20 personas"),
           ("Plug & play", "Por USB o inalámbrico, sin drivers")],
    a="Slow cinematic push-in on the conference speakerphone and the two small expansion microphones on the wooden meeting table. Two people in the blurred background, one writing notes. The LED lights glow softly.",
    b="Slow gentle camera drift over the top of the grey speakerphone: flat dark grey fabric mesh surface with only a thin row of tiny LED indicator dots near the front edge. There is NO circular ring light and no ports on the top. Wooden table, soft blurred meeting room behind.",
    c="Wider slow sideways dolly showing the speakerphone in the center of the meeting table with the two small microphones, a person gesturing while speaking in the blurred background."),
 "CAST2": dict(
    pdf=ACC + "Periféricos/Ficha técnica OneScreen Cast2", nombre="Cast2", sub="Proyección inalámbrica",
    lema="Duplica tu pantalla en OneScreen, sin cables.", musica="MASTER_Cooking.wav",
    specs=[("4K", "Transmisión inalámbrica Ultra HD"), ("60 fps", "En Full HD, y 30 fps en 4K"),
           ("10 puntos", "De control táctil desde la pantalla"), ("Wi-Fi 6", "USB Tipo-C, conexión plug and play"),
           ("WPA2", "Autenticación Enterprise y contenido local")],
    a="Slow cinematic push-in: a hand plugs one small black wireless presentation dongle into the USB-C port of a laptop on a clean modern desk in a bright office, soft light, shallow depth of field.",
    b="Slow smooth orbit around the small black wireless presentation dongles standing on a clean surface, soft studio light, shallow depth of field.",
    c="Slow sideways dolly in the meeting room: the presenter points at the large screen with charts, people at the table watching, natural subtle movement."),
 "OCWL10C": dict(
    pdf=ACC + "Periféricos/Ficha técnica OneScreen Sensor Box", nombre="Sensor Box", sub="NFC + sensores de ambiente",
    lema="Tu acceso. Tu ambiente. Todo en un solo toque.", musica="MASTER_Food Menu.wav",
    specs=[("NFC", "Inicia sesión en OneScreen Account con una tarjeta"), ("4.9 m", "Detecta movimiento y enciende o apaga la pantalla"),
           ("Aire", "Mide calidad del aire, temperatura y humedad"), ("4 tarjetas", "NFC incluidas en la caja"),
           ("Core", "Se instala sin complicaciones en tu OneScreen Core")],
    a="Medium shot of the slim black sensor bar, small in the frame, exactly as in the reference: the small round element is a flat sensor window, NOT a camera lens, do not enlarge it or add glass. A hand gently taps a blank white card near the bar. Soft light.",
    b="Wide slow push-in on a bright classroom with a large interactive screen; the slim black sensor bar sits small under the bottom edge of the screen, unchanged and with no camera lens. Children at desks softly blurred.",
    c="Slow sideways dolly in the classroom: the teacher gestures toward the large interactive screen, children in the foreground, natural subtle movement."),
 "CAMSNAP2": dict(
    pdf=ACC + "Cámaras/Ficha técnica OneScreen SnapCam 2", nombre="SnapCam 2", sub="Cámara 4K con IA",
    lema="Ver mejor, es colaborar mejor.", musica="MASTER_For cooking fire.wav",
    specs=[("4K", "UHD a 30 fps con sensor CMOS de 1/2.8″"), ("IA", "Encuadre automático según las personas en la reunión"),
           ("Seguimiento", "Del presentador con IA mientras se mueve por la sala"), ("Privacidad", "Cubierta mecánica incorporada"),
           ("OneScreen T7", "Se inserta de forma nativa en la pantalla")],
    a="Slow cinematic push-in on the black compact camera on its tilting stand in a bright empty classroom with rows of desks, soft daylight, shallow depth of field.",
    b="Slow smooth orbit around the black camera with its large round lens, soft highlights on the glossy body, blurred classroom behind.",
    c="Slow sideways dolly past the black camera in the classroom, desks and blackboard blurred in the background, gentle light changes."),
 "CAMPTZ": dict(
    pdf=ACC + "Cámaras/Ficha técnica OneScreen PTZ 4K", nombre="PTZ 4K", sub="Cámara con seguimiento automático",
    lema="Ver mejor, es colaborar mejor.", musica="MASTER_Percussion Stomps Claps Energetic.wav",
    specs=[("4K", "Imagen real con sensor CMOS de 1/2.5″"), ("12×", "Zoom óptico, de planos amplios a primeros planos"),
           ("ReID", "Sigue al presentador automáticamente"), ("PoE", "Un solo cable: energía, control y red"),
           ("255", "Posiciones preestablecidas")],
    a="Slow cinematic push-in on the silver and black PTZ camera standing on a wooden conference table, a large screen with a video call blurred behind, soft office light.",
    b="Slow smooth close-up of the PTZ camera lens and body as the camera head slowly pans a little to the side, shallow depth of field.",
    c="Slow sideways dolly past the PTZ camera on the conference table toward the blurred large wall screen, gentle light, steady motion."),
 "OCMIC60": dict(
    pdf=ACC + "Micrófonos/OneScreen Amplifyr.pdf", nombre="Amplifyr", sub="Micrófono inalámbrico",
    lema="Tu voz, con amplificación cristalina.", musica="MASTER_stepanbel_percussion_main-01.wav",
    specs=[("100 m", "De alcance inalámbrico en espacio abierto"), ("Bluetooth 5.2", "LE Audio, latencia menor a 25 ms"),
           ("6 h+", "De batería; 10 min de carga dan más de 90 min"), ("95 dB", "De relación señal/ruido"),
           ("2 micrófonos", "Con estuche de carga y receptor incluidos")],
    a="Slow cinematic push-in on a hand holding the white charging case with a small wireless microphone beside it, bright clean background, soft light.",
    b="Slow smooth close-up of the white charging case with two compact microphones, a finger gently touching one, shallow depth of field.",
    c="Slow gentle orbit around the white charging case and the small wireless microphone held in an open hand, soft airy light."),
 "MC1500": dict(
    pdf=SOP + "Ficha técnica OneScreen Soporte móvil MC1500", nombre="MC1500", sub="Soporte móvil",
    lema="Tu pantalla, lista para moverse contigo.", musica="MASTER_upbeat-drum-energetic-percussion.wav", plano_desde=4,   # «Bandeja»: plano de cerca (Flow)
    specs=[("55″ y 65″", "Pantallas compatibles"), ("80 kg", "Peso máximo, VESA hasta 600 × 400 mm"),
           ("116 a 143 cm", "De altura ajustable"), ("Bandeja", "Incluida con el soporte"),
           ("Cámara", "Soporte para cámara incluido")],
    a="Slow cinematic push-in on the black mobile display stand holding a large flat screen with a video call, standing in a bright modern meeting room, soft daylight, steady camera.",
    b="Slow smooth tilt along the black metal mobile display stand with its mounting arms and lower shelf, shallow depth of field, office blurred behind.",
    c="Slow sideways dolly in the meeting room past the screen on its mobile stand, people at the table in the foreground, steady natural motion."),
 "MC1800": dict(
    pdf=SOP + "Ficha técnica OneScreen Soporte móvil MC1800", nombre="MC1800", sub="Soporte móvil",
    lema="Tu pantalla, lista para moverse contigo.", musica="MASTER_stepanbel_funk_main-01.wav",
    specs=[("55″ a 100″", "Pantallas compatibles"), ("100 kg", "Peso soportado, VESA 200 × 200 a 900 × 600 mm"),
           ("Ruedas", "Giratorias, con freno de bloqueo"), ("Altura", "Ajuste manual para cada espacio"),
           ("Bandeja", "Para teclados y otros accesorios, herrajes incluidos")],
    a="Slow cinematic push-in on the black mobile display stand with wheels holding a very large flat screen, standing in a bright classroom, soft daylight, steady camera.",
    b="Slow smooth tilt along the sturdy black mobile display stand with mounting arms, lower tray and wheels, shallow depth of field.",
    c="Slow sideways dolly in the classroom past the large screen on its mobile stand, students in the foreground, natural subtle movement."),
 "OSP-72": dict(
    pdf="Pantallas LED - Fichas técnicas/OneScreen-Poster_P1.9.pdf", nombre="Poster P1.9", sub="Póster LED digital 72″",
    lema="Grandes ideas necesitan grandes pantallas.", musica="MASTER_Phonk_Opener.wav",
    specs=[("72″", "Póster LED de 182.9 cm de diagonal"), ("800 nits", "De brillo, LED SMD con recubrimiento GOB"),
           ("1.9 mm", "De pixel pitch"), ("6 en cascada", "Une hasta 6 pósters en una sola pantalla"),
           ("Remoto", "Administra el contenido desde PC, smartphone o la nube")],
    a="Steady wide shot of a bright electronics store: two shoppers look at the tall slim vertical LED poster standing on its black base, exactly as in the reference image. The poster is only 62 cm wide and 173 cm tall, very thin (3.3 cm), black frame-less edges, black flat back, on a small black stand. Keep its proportions: it is taller than a person but NOT a wall-sized screen. Camera stays far, no zoom.",
    b="Slow orbit around the tall slim vertical LED poster seen in the reference image: front shows the colorful advertisement, the back is flat black with a small black stand base. Keep the poster very thin and narrow (62 x 173 cm), same proportions as the reference, never enlarge it. Camera stays at a distance, shoppers softly blurred.",
    c="Wide slow sideways dolly in the store past the tall slim vertical LED poster on its black base, shoppers blurred in the background, steady motion. The poster keeps the narrow proportions of the reference image."),
 "CAMWEB": dict(
    pdf=ACC + "Cámaras/Ficha técnica OneScreen WebCam 101", nombre="Camweb", sub="Cámara web Full HD",
    lema="Ver mejor, es trabajar mejor.", musica="MASTER_SierraAudio - Energetic Stomp Trap Percussion - Full - 190.wav",
    specs=[("1080p", "Video Full HD"), ("Micrófono", "Integrado en la cámara"),
           ("2D y 3D", "Reducción digital de ruido en poca luz"), ("USB", "Un solo cable, plug and play (UVC)"),
           ("Windows, macOS y Linux", "Compatible con tu computador")],
    a="Slow cinematic push-in on the black widescreen webcam sitting on a wooden table in a bright meeting room with large windows, soft daylight.",
    b="Slow smooth close-up of the webcam lens and its swivel stand on the wooden table, shallow depth of field, bright room blurred behind.",
    c="Slow sideways dolly past the webcam on the table, the bright meeting room and windows softly blurred behind, steady gentle motion."),
 "OPSL7I7": dict(
    pdf=ACC + "OPS/Catalogo OneScreen OPS i7 12th GEN.pdf", nombre="OPS i7", sub="Módulo OPS Intel® Core™ i7",
    lema="La computadora que cabe dentro de tu pantalla.", musica="MASTER_WAV_MusicHusky_Promo_Opener_Main_Version.wav",
    specs=[("Intel® Core™ i7", "Rendimiento de computadora en tu pantalla"), ("Windows", "Tu propio PC dentro de la pantalla interactiva"),
           ("OPS", "Se inserta en la ranura OPS de la pantalla"), ("Conectividad", "Wi-Fi, Bluetooth, Ethernet y USB")],
    a="Slow cinematic push-in on a slim black computer module with many ports lying on a dark wooden desk, warm soft light, shallow depth of field.",
    b="Slow smooth close-up gliding along the ports of the slim black computer module, HDMI and USB ports, shallow depth of field.",
    c="Slow gentle orbit around the slim black computer module on the wooden desk, soft highlights on the metal, steady motion."),
}
ORDEN = list(P)


# Lapiz Interactivo (LAPIZP): planos reales de Sebastian (ml_lapiz.py), no clips de IA. Ficha: STYG2-002.
P["LAPIZP"] = dict(
    pdf="", nombre="Touch Pen", sub="Lápiz Interactivo", real=True,
    lema="Precisión sin interrupciones.", musica="MASTER_Inspired and Uplifting Hip Hop.wav",
    specs=[("2 puntas", "Delgada y gruesa, cada una con su herramienta en Write"), ("Sin batería", "No requiere carga ni ninguna fuente de energía"),
           ("Antibacterial", "Superficie antibacteriana, para mayor higiene"), ("Imantado", "Se adhiere fácil a tu pantalla OneScreen"),
           ("Rechazo de palma", "Integrado: apoya la mano y escribe"), ("T7, Core y Titan", "Modelos OneScreen compatibles")])


def pagina(sku):
    import pymupdf
    pdf = FICHAS / P[sku]["pdf"]
    d = pymupdf.open(pdf)
    return d, pdf


def recortes(skus):
    import pymupdf
    img = BASE / "img"
    img.mkdir(exist_ok=True)
    for sku in skus:
        d, _ = pagina(sku)
        if sku == "OPSL7I7":
            # la ficha del OPS trae el render como imagenes sueltas
            for i, nombre in ((7, "hero"), (9, "prod")):
                px = pymupdf.Pixmap(d, i)
                if px.n >= 5: px = pymupdf.Pixmap(pymupdf.csRGB, px)
                px.save(img / f"{sku}_{nombre}.png")
            continue
        pg = d[0]
        pm = pg.get_pixmap(dpi=300)
        pm.save(img / f"_{sku}_p1.png")
        im = Image.open(img / f"_{sku}_p1.png").convert("RGB")
        w, h = im.size
        # el poster trae la insignia "P1.9" abajo a la derecha del render: se recorta fuera
        x1, y1 = (.86, .255) if sku == "OSP-72" else (.894, .31)
        im.crop((int(.066 * w), 0, int(x1 * w), int(y1 * h))).save(img / f"{sku}_hero.png")
        im.crop((int(.56 * w), int(.54 * h), int(.98 * w), int(.93 * h))).save(img / f"{sku}_prod.png")
        print(sku, "ok")


def clips(skus):
    (BASE / "veo").mkdir(exist_ok=True)

    def uno(args):
        sku, k, imagen = args
        sal = BASE / "veo" / f"{sku}_{k}.mp4"
        if sal.exists():
            return sal
        generar(str(BASE / "img" / f"{sku}_{imagen}.png"), str(sal), P[sku][k] + " " + NO_CAMBIAR)
        return sal
    # en estos SKU la foto de ambiente de la ficha no muestra el producto: la escena parte del render del producto
    prod_a = ("CAST2", "OCWL10C", "MC1500", "MC1800")
    prod_b = prod_a + ("OCMIC60", "OPSL7I7", "A10W")
    trabajos = []
    for sku in skus:
        # solo 2 clips nuevos por SKU (cada uno de 10 s cuesta ~US$1); el tercer tramo es el primero invertido
        faltan = 2 - sum((BASE / "veo" / f"{sku}_{k}.mp4").exists() for k in "abc")
        for k, img in (("a", "prod" if sku in prod_a else "hero"), ("b", "prod" if sku in prod_b else "hero")):
            if faltan > 0 and not (BASE / "veo" / f"{sku}_{k}.mp4").exists():
                trabajos.append((sku, k, img))
                faltan -= 1
    # de a uno: Tier 1 permite 4 peticiones por minuto y tiene tope por gasto
    for t in trabajos:
        try:
            print(uno(t), flush=True)
        except SystemExit as e:
            print("FALLO", t, e, flush=True)
            if "402" in str(e):
                break  # sin creditos: no seguir


def tam(texto, maximo, ancho=780, k=0.74):   # Rubik 800: ~0.70 em por caracter; con 0.60 se cortaba en el borde
    return max(50, min(maximo, int(ancho / (max(len(texto), 1) * k))))   # piso 50: con 70 «Windows, macOS y Linux» se salía del borde


# Guion de voz estilo producto Apple: una frase corta por escena (titulo, cada spec, cierre). Solo datos de la ficha.
# Cifras escritas como se pronuncian (REGLAS §6); "IA" -> "inteligencia artificial" / "i-a".
VOZ = {
 "A10W": ["Conoce el A10W.", "Trescientos sesenta grados. Escucha cada rincón de la sala.",
          "Un altavoz de doble frecuencia. Quince vatios de sonido.", "Y la inteligencia artificial hace el resto. Adiós al ruido. Adiós al eco.",
          "De seis a veinte personas. Una sola sala. Un solo equipo.", "Conéctalo por USB, o sin cables. Sin instalar nada.",
          "Tu sala de juntas, ahora más inteligente."],
 "CAST2": ["Conoce Cast dos.", "Cuatro ka. Ultra HD. Y sin un solo cable.", "Hasta sesenta cuadros por segundo, en Full HD.",
           "Toca tu pantalla. Diez puntos táctiles, a un clic.", "USB tipo C. Wi-Fi seis. Se conecta en segundos.",
           "Seguro por diseño. Autenticación WPA2 Enterprise, y todo se comparte de forma local.", "Duplica tu pantalla en OneScreen, sin cables."],
 "OCWL10C": ["Conoce el Sensor Box.", "Un toque. Y ya iniciaste sesión.", "Detecta el movimiento y enciende la pantalla. Cuando nadie está, la apaga.",
             "Mide el aire. La temperatura. La humedad.", "Cuatro tarjetas NFC, incluidas.", "Se instala sin complicaciones en tu OneScreen Core.",
             "Tu acceso. Tu ambiente. Todo en un solo toque."],
 "CAMSNAP2": ["Conoce la SnapCam dos.", "Cuatro ka UHD. Colores intensos. Cada detalle.", "Con inteligencia artificial, encuadra a todos los que están en la reunión.",
              "Y sigue a quien presenta, mientras se mueve por la sala.", "Tu privacidad, primero. Con cubierta mecánica incorporada.",
              "Se inserta en la OneScreen T siete. Nativa. Segura.", "Ver mejor, es colaborar mejor."],
 "CAMPTZ": ["Conoce la PTZ cuatro ka.", "Imagen cuatro ka real.", "Zoom óptico de doce aumentos. De planos amplios a primeros planos nítidos.",
            "Detecta a quien presenta. Lo sigue. Reencuadra en tiempo real.", "Un solo cable. Energía, control y red.",
            "Doscientas cincuenta y cinco posiciones preestablecidas.", "Ver mejor, es colaborar mejor."],
 "OCMIC60": ["Conoce el Amplifyr.", "Cien metros de alcance inalámbrico.", "Bluetooth cinco punto dos. LE Audio. Latencia menor a veinticinco milisegundos.",
             "Más de seis horas de batería. Diez minutos de carga, y noventa de uso.", "Noventa y cinco decibeles de relación señal ruido.",
             "Dos micrófonos, estuche de carga y receptor. Todo en la caja.", "Tu voz, con amplificación cristalina."],
 "MC1500": ["Conoce el MC mil quinientos.", "Para pantallas de cincuenta y cinco y sesenta y cinco pulgadas.", "Ochenta kilos de capacidad.",
            "Altura ajustable. De ciento dieciséis a ciento cuarenta y tres centímetros.", "Con bandeja incluida.", "Y soporte para tu cámara.",
            "Tu pantalla, lista para moverse contigo."],
 "MC1800": ["Conoce el MC mil ochocientos.", "De cincuenta y cinco a cien pulgadas.", "Hasta cien kilos. Construcción robusta.",
            "Ruedas giratorias, con freno.", "Ajusta la altura. A mano. Para cada espacio.", "Bandeja para teclados y accesorios. Herrajes incluidos.",
            "Tu pantalla, lista para moverse contigo."],
 "OSP-72": ["Conoce el OneScreen Poster.", "Setenta y dos pulgadas de pura presencia.", "Ochocientos nits de brillo.",
            "Pixel pitch de uno punto nueve milímetros. Cada detalle, nítido.", "Une hasta seis pósters. Y forma una sola pantalla gigante.",
            "Administra todo desde tu computador, tu celular o la nube.", "Grandes ideas necesitan grandes pantallas."],
 "CAMWEB": ["Conoce la Camweb.", "Full HD. Mil ochenta p.", "Con micrófono integrado.", "Reducción digital de ruido, dos D y tres D.",
            "Un solo cable USB. Conecta y listo.", "Funciona con Windows, macOS y Linux.", "Ver mejor, es trabajar mejor."],
 "OPSL7I7": ["Conoce el módulo OPS.", "Procesador Intel Core i siete.", "Con Windows. Tu propio PC, dentro de la pantalla.",
             "Se inserta en la ranura OPS. Y ya.", "Wi-Fi, Bluetooth, Ethernet y USB.", "La computadora que cabe dentro de tu pantalla."],
}


VOZ["LAPIZP"] = ["Conoce el Lápiz Interactivo.", "Doble punta. Delgada y gruesa. Cada una, con su herramienta.", "Sin batería. Nada que cargar.",
                 "Superficie antibacterial, para mayor higiene.", "Imantado. Se adhiere a tu pantalla.",
                 "Rechazo de palma integrado. Apoya la mano y escribe.", "Compatible con T7, Core y Titan.", "Precisión sin interrupciones."]


def guiones(skus):
    """Escribe Voz/guion_dirigido_v3.txt y guion_limpio.txt por SKU y un resumen Guiones_voz.md para aprobar."""
    md = ["# Guiones de voz — videos de producto para Mercado Libre", "",
          "Estilo producto Apple: una frase corta por escena, sin jerga, solo datos de la ficha. La pantalla muestra la cifra; la voz le da el sentido.", ""]
    for sku in skus:
        lineas = VOZ[sku]
        assert len(lineas) == len(P[sku]["specs"]) + 2, sku
        carpeta = BASE / sku / "Voz"
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / "guion_dirigido_v3.txt").write_text("\n".join("[confident] " + l for l in lineas), encoding="utf-8")
        (carpeta / "guion_limpio.txt").write_text("\n".join(lineas), encoding="utf-8")
        md += [f"## {sku} — OneScreen {P[sku]['nombre']}", "", "| Escena | En pantalla | Voz |", "|---|---|---|",
               f"| Título | {P[sku]['nombre']} · {P[sku]['sub']} | {lineas[0]} |"]
        md += [f"| Spec {i} | {v} — {e} | {lineas[i]} |" for i, (v, e) in enumerate(P[sku]["specs"], 1)]
        md += [f"| Cierre | OneScreen · {P[sku]['nombre']} | {lineas[-1]} |", ""]
    (BASE / "Guiones_voz.md").write_text("\n".join(md), encoding="utf-8")
    print("escrito", BASE / "Guiones_voz.md")


def voz(skus):
    """Voz con la receta unica (voz_exp_d.py + voz_post.py). Cuesta creditos de ElevenLabs: solo con guion aprobado."""
    env = dict(os.environ, CONTENIDO=str(BASE.parents[1]))   # ...\Contenido\2026 -> 10. Octubre\Mercado Libre\<SKU>\Voz
    ino = REPO / "videos/onescreen-inta"
    for sku in skus:
        subprocess.run([sys.executable, "-I", str(ino / "voz_exp_d.py"), sku], env=env, check=True)
        subprocess.run([sys.executable, "-I", str(ino / "voz_post.py"), sku], env=env, check=True)


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in t if unicodedata.category(c) != "Mn"))


def tiempos_de(specs, mg):
    """(inicio, duracion) de cada escena: titulo, specs, cierre. Misma cuenta que usa build()."""
    T_TIT, T_FIN, TOT = 3.2, 3.8, 30.0
    n = len(specs)
    dur = ((20.0 if mg else TOT - T_FIN) - T_TIT) / (n - 1 if mg else n)
    t = [(0.0, T_TIT)]
    for i in range(1, n + 1):
        ultima = mg and i == n
        t.append((20.0 if ultima else T_TIT + (i - 1) * dur, (TOT - T_FIN - 20.0) if ultima else dur))
    return t + [(TOT - T_FIN, T_FIN)]


def alinear_voz(sku):
    """Corte (inicio, fin) de cada frase del guion dentro de la toma unica, por palabras de Scribe. None si no hay voz."""
    tomas = sorted((BASE / sku / "Voz").glob(f"v[0-9][0-9][0-9][0-9]/{sku}_voz_scribe.json"))
    if not tomas:
        return None
    js = json.loads(tomas[-1].read_text(encoding="utf-8"))
    pal = [w for w in js["words"] if w.get("type") == "word"]
    nw = [norm(w["text"]) for w in pal]
    inicios, j = [], 0
    for linea in VOZ[sku]:
        primeras = [norm(x) for x in re.sub(r"(?i)cuatro ka", "4K", re.sub(r"\[.*?\]", "", linea)).split()[:2]]   # Scribe escribe "4K"
        k = next((k for k in range(j, len(pal)) if nw[k] == primeras[0] and (len(primeras) < 2 or k + 1 >= len(pal) or nw[k + 1] == primeras[1])), None)
        if k is None:
            k = next((k for k in range(j, len(pal)) if nw[k] == primeras[0]), None)
        if k is None:
            print(sku, "no encuentro la frase", linea); return None
        inicios.append(k); j = k + 1
    wav = tomas[-1].with_name(f"{sku}_voz.wav")
    # Los fines de palabra de Scribe pueden quedar antes de que acabe la voz (cortaba la cola de la frase): el corte entre dos
    # frases se pone en el punto mas silencioso entre el fin de una y el inicio de la otra.
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    sm = np.frombuffer(raw, np.float32)
    env = np.array([np.sqrt((sm[i:i + 160] ** 2).mean()) for i in range(0, len(sm) - 160, 160)])   # 10 ms

    def silencio(t0, t1):
        a, b = max(0, int(t0 * 100)), min(len(env) - 1, int(t1 * 100))
        return (a + int(np.argmin(env[a:b + 1])) + 0.5) / 100 if b > a else t0
    corte_ent = [silencio(pal[inicios[i + 1] - 1]["end"] - 0.05, pal[inicios[i + 1]]["start"] + 0.02) for i in range(len(inicios) - 1)]
    cortes = []
    for i, k in enumerate(inicios):
        ini = corte_ent[i - 1] if i else max(0.0, pal[k]["start"] - 0.05)
        fin = corte_ent[i] if i + 1 < len(inicios) else pal[-1]["end"] + 0.14
        cortes.append((ini, fin))
    return wav, cortes


def tiempos_de_voz(sku):
    """(tiempos, duracion total, cortes): cada escena dura lo que su frase + una respiracion; sin silencios muertos (Cris, 28-oct)."""
    al = alinear_voz(sku)
    if not al:
        return None
    _wav, cortes = al
    t, tiempos = 0.0, []
    for i, (a, b) in enumerate(cortes):
        ultima = i == len(cortes) - 1
        dd = (b - a) + 0.12 + (1.0 if ultima else 0.2)
        dd = max(dd, 2.4 if i == 0 else 2.0)
        tiempos.append((t, dd))
        t += dd
    return tiempos, t, cortes


def montar_voz(sku, proj, tiempos, tot):
    """Pone cada frase al inicio de su escena (las escenas ya siguen a la voz, asi que no se estira ni se acelera nada)."""
    wav, cortes = alinear_voz(sku)
    cadena, partes = [], []
    for i, (a, b) in enumerate(cortes):
        retraso = int((tiempos[i][0] + 0.12) * 1000)
        cadena.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0.0, b - a - 0.02):.3f}:d=0.02,adelay={retraso}|{retraso}[v{i}]")
        partes.append(f"[v{i}]")
    fc = ";".join(cadena) + ";" + "".join(partes) + f"amix=inputs={len(partes)}:normalize=0,apad=whole_dur={tot:.3f},loudnorm=I=-18:TP=-2[o]"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(wav), "-filter_complex", fc, "-map", "[o]", "-t", f"{tot:.3f}",
                    "-ar", "48000", str(proj / "assets/voz.wav")], check=True)
    return True


def partir(texto):
    """Palabras en spans: cada una entra sola, de abajo hacia arriba."""
    return " ".join(f'<span class="w">{html.escape(w)}</span>' for w in texto.split())


def numerico(v):
    """(valor, decimales, sufijo) si el dato empieza por una cifra que vale la pena contar; si no, None."""
    m = re.match(r"^(\d+(?:[.,]\d+)?)(.*)$", v)
    if not m or re.search(r"\d", m.group(2)):
        return None
    num = m.group(1).replace(",", ".")
    dec = len(num.split(".")[1]) if "." in num else 0
    val = float(num)
    return None if (val < 10 and dec == 0) else (val, dec, m.group(2))


def build(skus):
    for sku in skus:
        d = P[sku]
        proj = BASE / sku / "Proyecto"
        (proj / "assets/fonts").mkdir(parents=True, exist_ok=True)
        for f in ("Rubik-Variable.ttf", "Manrope-variable-latin.woff2"):
            shutil.copy(FUENTES / f, proj / "assets/fonts" / f)
        shutil.copy(LOGO, proj / "assets/logo.svg")
        shutil.copy(REPO / "estudio-carruseles/assets/logos/OneScreen_Azul.svg", proj / "assets/logo_azul.svg")
        shutil.copy(BASE / "img" / f"{sku}_prod.png", proj / "assets/prod.png")
        # Tramos de 10 s: con 3 clips, todo en plano; con 2, tramo final 20-30 s en motion graphic del render oficial.
        # Con menos de 2 clips no se arma: un video no puede quedar sin planos.
        disp = [BASE / "veo" / f"{sku}_{k}.mp4" for k in "abc" if (BASE / "veo" / f"{sku}_{k}.mp4").exists()]
        if len(disp) < 2:
            print(sku, "SIN CLIPS SUFICIENTES (", len(disp), "): no se arma"); continue
        mg = len(disp) == 2
        pd = d.get("plano_desde")   # con 3 clips: el tercero (plano de apoyo) entra al empezar la escena pd, y de ahi al cierre todo es plano
        for i, k in enumerate("abc"[:len(disp)]):
            # Omni arranca cada clip con la imagen de referencia estatica: se recortan los primeros 0.4 s y se
            # estira 4 % para volver a 10 s. Fotogramas clave cada 1 s (si no, HyperFrames puede congelar el cuadro).
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0" if d.get("real") else "0.4", "-i", str(disp[i]), "-an", "-vf",
                            "fps=30" if d.get("real") else "setpts=PTS*1.04167,fps=30", "-t", "10", "-c:v", "libx264", "-g", "30", "-keyint_min", "30",
                            "-movflags", "+faststart", str(proj / "assets" / f"{k}.mp4")], check=True)
        vt = tiempos_de_voz(sku)
        if vt:
            tiempos_s, TOT, _cortes = vt
            tiene_voz = montar_voz(sku, proj, tiempos_s, TOT)
        else:
            tiempos_s, TOT, tiene_voz = tiempos_de(d["specs"], mg), 30.0, False
        # voz ~ -18 LUFS; musica ~6 LU por debajo (-24) cuando hay voz
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(MUSICA / d["musica"]), "-t", f"{TOT:.3f}", "-af",
                        f"loudnorm=I={-24 if tiene_voz else -16}:TP=-2,afade=t=in:d=0.4,afade=t=out:st={TOT - 1.8:.2f}:d=1.8", "-ar", "48000",
                        str(proj / "assets/musica.wav")], check=True)
        shutil.copy(REPO / "videos/onescreen-flota-ia/hyperframes.json", proj / "hyperframes.json")
        (proj / "package.json").write_text(json.dumps({"name": f"ml-{sku.lower()}", "private": True, "type": "module",
            "scripts": {"render": "npx --yes hyperframes@0.8.112 render"}}, indent=2))

        specs = d["specs"]
        n = len(specs)
        T_TIT, T_FIN = tiempos_s[0][1], tiempos_s[n + 1][1]
        T_MG = tiempos_s[n][0] if mg else TOT          # inicio del motion graphic final (solo con 2 clips)
        T_C = tiempos_s[pd][0] if (pd and not mg) else None   # inicio del tercer clip
        W = (T_MG / 2) if mg else ((T_C / 2) if T_C else (TOT / 3))   # cada plano cubre un tercio (o la mitad antes del motion)
        esc = html.escape
        escenas, js, tiempos = [], [], [(0.0, T_TIT)]

        def anillos(pref, color="pr"):
            return "".join(f'<div id="{pref}-r{r}" class="{color}"></div>' for r in range(3))

        def js_anillos(pref, t0, dd):
            return (f'for(let r=0;r<3;r++){{tl.fromTo("#{pref}-r"+r,{{scale:.35,opacity:.7}},'
                    f'{{scale:1.9,opacity:0,duration:2.4,ease:"power1.out",repeat:{max(0, int(dd // 2.4) - 1)}}},{t0 + .1:.2f}+r*.8);}}')

        # --- titulo sobre el plano A
        escenas.append(f'''<section id="s0" class="clip esc" data-start="0" data-duration="{T_TIT}">
  {anillos("s0")}
  <div class="mt">
    <img id="s0-logo" class="logo" src="assets/logo.svg" alt="OneScreen">
    <div id="s0-nom" class="val" style="font-size:{tam(d["nombre"], 250)}px">{esc(d["nombre"])}</div>
    <div id="s0-bar" class="bar"></div>
    <div id="s0-sub" class="eti ligera">{esc(d["sub"])}</div>
    <div id="s0-lema" class="eti peq">{partir(d["lema"])}</div></div></section>''')
        js.append('tl.from("#s0-logo",{y:50,opacity:0,duration:.9,ease:"power3.out"},0.1);'
                  'tl.from("#s0-nom",{y:80,opacity:0,duration:1,ease:"power3.out"},0.3);'
                  'tl.from("#s0-bar",{scaleX:0,duration:.9,ease:"power3.out",transformOrigin:"left center"},0.7);'
                  'tl.from("#s0-sub",{y:50,opacity:0,duration:.9,ease:"power3.out"},0.8);'
                  'tl.from("#s0-lema .w",{y:46,opacity:0,duration:.9,stagger:.07,ease:"power3.out"},1.0);'
                  + js_anillos("s0", 0, T_TIT) + f'tl.to("#s0",{{opacity:0,duration:.3}},{T_TIT - .3});')

        # --- especificaciones: alternan plano con graficos (P) y escena de color con el producto flotando (M)
        for i, (v, e) in enumerate(specs, 1):
            ultima = mg and i == n
            t0, dd = tiempos_s[i]
            es_m = (i % 2 == 0) and not ultima and not (T_C and i >= pd)
            tiempos.append((t0, dd))
            num = numerico(v)
            val_html = esc(v)
            tam_v = tam(v, 250)
            texto = f'''<div class="mt{" claro" if (es_m or ultima) else ""}">
    <div id="s{i}-v" class="val" style="font-size:{tam_v}px">{val_html}</div>
    <div id="s{i}-b" class="bar"></div>
    <div id="s{i}-e" class="eti">{partir(e)}</div></div>'''
            if es_m:
                motivo = ""
                if (i // 2) % 2 == 1:   # barras de audio que laten
                    barras = "".join(f'<rect class="eq" x="{k * 56}" y="0" width="22" height="90" fill="url(#g{i})"/>' for k in range(14))
                    motivo = (f'<svg class="motivo" viewBox="0 0 780 90" width="780" height="90"><defs><linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1">'
                              f'<stop offset="0" stop-color="#3976ff"/><stop offset="1" stop-color="#9fc0ff"/></linearGradient></defs>{barras}</svg>')
                    js_m = ('document.querySelectorAll("#s%d .eq").forEach((el,k)=>{tl.fromTo(el,{scaleY:.12},{scaleY:.25+((k*37)%%10)/12,'
                            'duration:.45+(k%%5)*.08,ease:"sine.inOut",yoyo:true,repeat:%d},%.2f+k*.04);});' % (i, max(1, int(dd / 0.6)), t0 + .3))
                else:                   # arco que se dibuja alrededor del producto
                    motivo = (f'<svg class="arco" viewBox="0 0 1080 1920" width="1080" height="1920">'
                              f'<circle id="s{i}-arc" cx="540" cy="1330" r="360" fill="none" stroke="#3976ff" stroke-width="7" '
                              f'stroke-dasharray="2262" stroke-dashoffset="2262" transform="rotate(-90 540 1330)"/>'
                              f'<circle id="s{i}-dot" cx="540" cy="970" r="14" fill="#3976ff"/></svg>')
                    js_m = ('tl.to("#s%d-arc",{strokeDashoffset:566,duration:1.8,ease:"power2.inOut"},%.2f);'
                            'tl.to("#s%d-dot",{rotation:270,svgOrigin:"540 1330",duration:1.8,ease:"power2.inOut"},%.2f);' % (i, t0 + .3, i, t0 + .3))
                escenas.append(f'''<section id="s{i}" class="clip esc m" data-start="{t0:.2f}" data-duration="{dd:.2f}">
  <div class="mbg"></div><div id="s{i}-b1" class="blob b1"></div><div id="s{i}-b2" class="blob b2"></div>
  {anillos(f"s{i}", "ring")}
  {motivo}
  <img id="s{i}-p" class="prod" src="assets/prod.png" alt="">
  {texto}</section>''')
                js.append(f'tl.fromTo("#s{i}-b1",{{x:-120,y:-40}},{{x:160,y:90,duration:{dd:.2f},ease:"sine.inOut"}},{t0:.2f});'
                          f'tl.fromTo("#s{i}-b2",{{x:140,y:60}},{{x:-130,y:-70,duration:{dd:.2f},ease:"sine.inOut"}},{t0:.2f});'
                          f'tl.from("#s{i}-p",{{y:110,opacity:0,scale:.9,duration:1.3,ease:"power3.out"}},{t0 + .15:.2f});'
                          f'tl.to("#s{i}-p",{{y:-16,duration:2.2,ease:"sine.inOut",yoyo:true,repeat:{max(1, int(dd / 2.2))}}},{t0 + 1.5:.2f});'
                          f'for(let r=0;r<3;r++){{tl.fromTo("#s{i}-r"+r,{{scale:.45,opacity:.55}},{{scale:1.7,opacity:0,duration:3.3,ease:"power1.out"}},{t0 + .3:.2f}+r*1.1);}}'
                          + js_m)
            else:
                escenas.append(f'''<section id="s{i}" class="clip esc{" claro" if ultima else ""}" data-start="{t0:.2f}" data-duration="{dd:.2f}">
  {"" if ultima else anillos(f"s{i}")}
  {texto}</section>''')
                if not ultima:
                    js.append(js_anillos(f"s{i}", t0, dd))
            # texto comun: valor (con cuenta si es cifra), barra que se dibuja y etiqueta palabra por palabra
            if num:
                val, dec, suf = num
                js.append('{const o={v:0};tl.fromTo(o,{v:0},{v:%s,duration:1.4,ease:"power2.out",onUpdate:()=>{document.getElementById("s%d-v").textContent=o.v.toFixed(%d)+%s;}},%.2f);}'
                          % (val, i, dec, json.dumps(suf), t0 + .05))
            js.append(f'tl.from("#s{i}-v",{{y:70,opacity:0,duration:1,ease:"power3.out"}},{t0 + .05:.2f});'
                      f'tl.from("#s{i}-b",{{scaleX:0,duration:.9,ease:"power3.out",transformOrigin:"left center"}},{t0 + .5:.2f});'
                      f'tl.from("#s{i}-e .w",{{y:46,opacity:0,duration:.9,stagger:.07,ease:"power3.out"}},{t0 + .35:.2f});'
                      # escenas de fondo opaco (M / ultima): sin fundido de salida, o dejan ver el plano de abajo («flash»)
                      + ("" if (es_m or ultima) else f'tl.to("#s{i}",{{opacity:0,duration:.3}},{t0 + dd - .3:.2f});'))

        # --- cierre
        t0 = tiempos_s[n + 1][0]
        tiempos.append((t0, T_FIN))
        escenas.append(f'''<section id="sf" class="clip esc fin{" claro" if mg else ""}" data-start="{t0}" data-duration="{T_FIN}">
  <img id="sf-logo" class="logo grande" src="assets/{"logo_azul" if mg else "logo"}.svg" alt="OneScreen">
  <div id="sf-nom" class="eti ligera">{esc(d["nombre"])} · {esc(d["sub"])}</div></section>''')
        js.append(f'tl.from("#sf-logo",{{y:50,opacity:0,duration:1,ease:"power3.out"}},{t0 + .1});'
                  f'tl.from("#sf-nom",{{y:40,opacity:0,duration:.9,ease:"power3.out"}},{t0 + .5});')
        if mg:
            DMG = TOT - T_MG
            escenas.insert(0, f'''<section id="mg" class="clip" data-start="{T_MG:.2f}" data-duration="{DMG:.2f}">
  <div id="mg-b1" class="blob b1"></div><div id="mg-b2" class="blob b2"></div>
  <div id="mg-r0" class="ring"></div><div id="mg-r1" class="ring"></div><div id="mg-r2" class="ring"></div>
  <img id="mg-prod" src="assets/prod.png" alt=""></section>''')
            js.append(f'tl.fromTo("#mg-b1",{{x:-120,y:-40}},{{x:160,y:90,duration:{DMG:.2f},ease:"sine.inOut"}},{T_MG:.2f});'
                      f'tl.fromTo("#mg-b2",{{x:140,y:60}},{{x:-130,y:-70,duration:{DMG:.2f},ease:"sine.inOut"}},{T_MG:.2f});'
                      f'for(let r=0;r<3;r++){{tl.fromTo("#mg-r"+r,{{scale:.45,opacity:.55}},{{scale:1.7,opacity:0,duration:3.3,ease:"power1.out",repeat:{max(0, int(DMG / 3.3) - 1)}}},{T_MG + .2:.2f}+r*1.1);}}'
                      f'tl.from("#mg-prod",{{y:90,opacity:0,scale:.9,duration:1.3,ease:"power3.out"}},{T_MG + .2:.2f});'
                      f'tl.to("#mg-prod",{{y:-16,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:{max(1, int(DMG / 2.4))}}},{T_MG + 1.6:.2f});')

        css = '''
@font-face{font-family:"Rubik";src:url("assets/fonts/Rubik-Variable.ttf") format("truetype");font-weight:300 900;font-display:block}
@font-face{font-family:"Manrope";src:url("assets/fonts/Manrope-variable-latin.woff2") format("woff2");font-weight:200 800;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0b1224}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#0b1224}
video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.sombra{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,12,28,.86) 0%,rgba(7,12,28,.74) 30%,rgba(7,12,28,.38) 46%,rgba(7,12,28,0) 62%,rgba(7,12,28,.30) 100%)}
.esc{position:absolute;inset:0;overflow:hidden}
.mt{position:absolute;left:150px;top:340px;width:780px}
.fin{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;background:rgba(7,12,28,.55)}
.logo{display:block;height:64px;width:auto;margin-bottom:34px}
.logo.grande{height:120px;margin:0}
.val{font-family:"Rubik",sans-serif;font-weight:800;color:#fff;line-height:1.02;letter-spacing:-.02em;white-space:nowrap;
 background:linear-gradient(180deg,#fff 30%,#9fc0ff 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
 filter:drop-shadow(0 4px 18px rgba(0,0,0,.35))}
.eti{font-family:"Manrope",sans-serif;font-weight:600;font-size:56px;line-height:1.22;color:#fff;margin-top:26px;text-shadow:0 2px 14px rgba(0,0,0,.55);text-wrap:balance}
.eti.ligera{font-family:"Rubik",sans-serif;font-weight:300;font-size:56px;margin-top:8px}
.eti.peq{font-weight:500;font-size:42px;margin-top:34px;opacity:.92}
.fin .eti{text-align:center;margin:0;max-width:780px}
.w{display:inline-block}
.bar{width:260px;height:7px;margin-top:22px;background:linear-gradient(90deg,#3976ff,#9fc0ff)}
.pr{position:absolute;left:240px;top:960px;width:600px;height:600px;border-radius:50%;border:3px solid rgba(255,255,255,.6)}
.m .mbg{position:absolute;inset:0;background:linear-gradient(165deg,#ffffff 0%,#eef4ff 50%,#d6e4ff 100%)}
#mg{position:absolute;inset:0;background:linear-gradient(165deg,#ffffff 0%,#eef4ff 50%,#d6e4ff 100%);overflow:hidden}
.blob{position:absolute;width:900px;height:900px;border-radius:50%;filter:blur(90px)}
.b1{left:-300px;top:900px;background:radial-gradient(circle,rgba(57,118,255,.38),rgba(57,118,255,0) 65%)}
.b2{left:480px;top:1250px;background:radial-gradient(circle,rgba(125,0,186,.18),rgba(125,0,186,0) 65%)}
.ring{position:absolute;left:190px;top:960px;width:700px;height:700px;border-radius:50%;border:3px solid rgba(57,118,255,.45)}
.prod,#mg-prod{position:absolute;left:130px;top:1000px;width:820px;mix-blend-mode:multiply;
 -webkit-mask-image:radial-gradient(ellipse at center,#000 52%,transparent 74%);mask-image:radial-gradient(ellipse at center,#000 52%,transparent 74%)}
.ghost{position:absolute;right:-60px;top:930px;font-family:"Rubik",sans-serif;font-weight:800;font-size:520px;line-height:1;color:rgba(57,118,255,.07);-webkit-text-fill-color:rgba(57,118,255,.07);-webkit-text-stroke:3px rgba(57,118,255,.22)}
.motivo{position:absolute;left:150px;top:880px}
.eq{transform-box:fill-box;transform-origin:50% 100%}
.arco{position:absolute;left:0;top:0}
.claro .val{color:#2f6bff;background:linear-gradient(180deg,#2f6bff 20%,#0f3fb8 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;filter:none}
.claro .eti{color:#14213d;text-shadow:none}
.fin.claro{background:transparent;justify-content:flex-start;padding-top:340px}
'''
        pagina_html = f'''<!doctype html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<title>{sku}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{TOT:.2f}">
<video id="va" class="clip" src="assets/a.mp4" muted playsinline data-start="0" data-duration="{W:.2f}" data-track-index="0"></video>
<video id="vb" class="clip" src="assets/b.mp4" muted playsinline data-start="{W:.2f}" data-duration="{W:.2f}" data-track-index="0"></video>
{'' if mg else f'<video id="vc" class="clip" src="assets/c.mp4" muted playsinline data-start="{2 * W:.2f}" data-duration="{TOT - 2 * W:.2f}" data-track-index="0"></video>'}
<div class="sombra clip" data-start="0" data-duration="{T_MG if mg else TOT:.2f}"></div>
{chr(10).join(escenas)}
<audio id="musica" src="assets/musica.wav" data-start="0" data-duration="{TOT:.2f}" data-track-index="5" data-volume="1"></audio>
{'<audio id="voz" src="assets/voz.wav" data-start="0" data-duration="{TOT:.2f}" data-track-index="6" data-volume="1"></audio>' if tiene_voz else ''}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script></body></html>'''
        (proj / "index.html").write_text(pagina_html, encoding="utf-8")
        print(sku, "proyecto escrito (v2)", "con motion final" if mg else "3 planos")


def render(skus):
    env = dict(os.environ, TMP="D:/hf-render/tmp", TEMP="D:/hf-render/tmp")
    (BASE / "Exports").mkdir(exist_ok=True)
    for sku in skus:
        proj = BASE / sku / "Proyecto"
        out = BASE / "Exports" / f"{sku}.mp4"
        r = subprocess.run(["npx", "--yes", "hyperframes@0.8.112", "render", "-o", str(out), "-q", "delivery",
                            "--video-frame-format", "png", "--frames-cache-dir", f"D:/hf-render/tmp/ml_{sku}", "--quiet"],
                           cwd=proj, env=env, shell=True, capture_output=True, text=True)
        print(sku, "render", r.returncode, (r.stdout + r.stderr)[-400:])


if __name__ == "__main__":
    cmd = sys.argv[1]
    skus = sys.argv[2:] or ORDEN
    {"recortes": recortes, "clips": clips, "guiones": guiones, "voz": voz, "build": build, "render": render}[cmd](skus)
