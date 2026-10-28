"""Escenas de EJEMPLO compuestas desde cero con el vocabulario de elementos.py (no son plantillas: cada una mezcla referencias distintas a la medida de su frase).
Sirven para ver cómo se compone: elegir el tema por significado, variar la luz entre escenas, 2-4 elementos de referencias distintas, jerarquía y aire.
Uso: from elementos import escena; spec, mov = escena(A)"""
A = {"tema": "solucion", "fondo": {"luz": "abajo"}, "elementos": [
    {"e": "titulo", "x": 100, "y": 250, "s": 92, "ancho": 560, "lineas": [["Un ingeniero real", 300], ["responde en", 700], ["minutos", 700, "grad"]]},
    {"e": "notificacion", "x": 640, "y": 330, "w": 560, "h": 170, "titulo": "Soporte", "t": "Ya estoy en línea, cuéntame qué pasa", "n": 24, "hora": "ahora", "icono": "auriculares"},
    {"e": "burbuja", "x": 1010, "y": 270, "t": "en línea"},
    {"e": "cursor", "x": 1080, "y": 560, "nombre": "Tú"},
    {"e": "destello", "x": 690, "y": 300, "s": 26, "fill": "#ffffff"}]}
B = {"tema": "explicar", "fondo": {"luz": "centro", "textura": "puntos"}, "elementos": [
    {"e": "anillos", "x": 640, "y": 380, "radios": [150, 250, 340, 430], "estilo": "suave"},
    {"e": "titulo", "x": 640, "y": 365, "s": 84, "a": "middle", "ancho": 700, "lineas": [["Capacitamos a", 300], ["todo tu equipo", 700, "grad"]]},
    {"e": "chip", "x": 90, "y": 110, "t": "Docentes", "icono": "persona", "w": 290}, {"e": "chip", "x": 900, "y": 95, "t": "Directivos", "icono": "grupo", "w": 290},
    {"e": "chip", "x": 60, "y": 520, "t": "Equipos de TI", "icono": "pantalla", "w": 310}, {"e": "chip", "x": 900, "y": 545, "t": "Certificado", "icono": "check", "w": 290},
    {"e": "progreso", "i": 1, "n": 4}]}
C = {"tema": "gurú", "fondo": {"luz": "arriba-der"}, "elementos": [
    {"e": "fantasma", "x": 80, "y": 600, "t": "24/5", "s": 520},
    {"e": "titulo", "x": 100, "y": 250, "s": 96, "ancho": 560, "lineas": [["Soporte vitalicio", 300]]},
    {"e": "marcador", "x": 90, "y": 282, "w": 470, "h": 108, "t": "sin costo"},
    {"e": "vidrio", "x": 720, "y": 200, "w": 480, "h": 340},
    {"e": "plano", "x": 860, "y": 110, "w": 300, "h": 520},
    {"e": "destello", "x": 700, "y": 140, "s": 34, "fill": "#ffffff"},
    {"e": "orbita", "x": 330, "y": 330, "rx": 430, "ry": 120, "rot": -6}]}
D = {"tema": "solucion", "fondo": {"luz": "abajo-der", "textura": "rejilla"}, "elementos": [
    {"e": "fantasma", "x": 600, "y": 520, "t": "80%", "s": 420, "op": 0.15},
    {"e": "titulo", "x": 100, "y": 230, "s": 74, "ancho": 600, "lineas": [["De cada 10 dudas", 300], ["8 se resuelven", 700], ["en una sesión", 700, "grad"]]},
    {"e": "curva", "puntos": [(100, 640), (300, 600), (500, 560), (700, 470), (900, 360), (1120, 250)], "neon": True, "final": True, "sw": 9, "base": 700},
    {"e": "burbuja", "x": 900, "y": 150, "t": "+80%"}]}

EJEMPLOS_ESCENAS = {
    "ingeniero_responde": A,   # solución (azul): titular light/bold con degradado + notificación con pila + burbuja + cursor + destello; luz desde abajo
    "capacitamos_equipo": B,   # explicar (blanco): anillos suaves + titular centrado + 4 chips satélite + indicador de progreso; luz al centro
    "soporte_sin_costo": C,    # Gurú (verde): número fantasma + marcador en la frase clave + vidrio con plano que lo rompe + órbita con destello; luz arriba-der
    "dudas_resueltas": D,      # solución (azul): número fantasma + titular + curva de neón con punto final + burbuja; luz abajo-der y rejilla
}
