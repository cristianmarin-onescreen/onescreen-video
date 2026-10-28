"""Parche: v2 con la voz regenerada (notas de dirección v4), toque de Iniciar sincronizado con la palabra 'start' y subtítulos oscuros sobre pantallas claras."""
from pathlib import Path
f = Path(__file__).parent / "build_v2.py"
s = f.read_text(encoding="utf-8")

# voz nueva
s = s.replace('SCRIBE = r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-21_quizwiz_scrybe/scribe_e2.json"',
              'SCRIBE = r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-21_quizwiz_scrybe/scribe_v4_e.json"')

# seg() acepta velocidad
s = s.replace('def seg(t, kind, src=None, tin=0.0, scale=100, origin="50% 50%"):\n    SEG.append(dict(t=t, kind=kind, src=src, tin=tin, scale=scale, origin=origin))',
              'def seg(t, kind, src=None, tin=0.0, scale=100, origin="50% 50%", rate=1.0):\n    SEG.append(dict(t=t, kind=kind, src=src, tin=tin, scale=scale, origin=origin, rate=rate))')

# toque en Iniciar: la grabación tiene el toque en 27,4 s y la pantalla de grabación en 29,5 s; se acelera el giro para que "listo" caiga con la pantalla de grabación
old_a = '''seg(T_grabar, "vid", "scrA", 0.9, 100, "50% 52%")                       # el toque en Iniciar ocurre en 29,2 s de la grabación = palabra "start"
seg(T_con, "vid", "scrA", 0.9 + (T_con - T_grabar), 165, "50% 52%")
seg(T_start, "vid", "scrA", 0.9 + (T_start - T_grabar), 100, "50% 52%")'''
new_a = '''TAP, REC = 27.4 - 23.5, 29.5 - 23.5                                      # toque en "Iniciar" y pantalla de grabación, dentro del recorte scrA (empieza en 23,5 s de la grabación)
RATE = max(1.0, min(3.0, (REC - TAP) / ((EV("listo") - T_start) + 0.15)))   # el giro de 2 s se acelera para que la pantalla de grabación llegue con "listo"
seg(T_grabar, "vid", "scrA", TAP - (T_start - T_grabar), 100, "50% 52%")
seg(T_con, "vid", "scrA", TAP - (T_start - T_con), 165, "50% 52%")
seg(T_start, "vid", "scrA", TAP, 100, "50% 52%", rate=RATE)'''
assert old_a in s
s = s.replace(old_a, new_a)
s = s.replace('"scrA": 5.6,', '"scrA": 7.5,')

# aviso de fuente agotada considerando velocidad
s = s.replace('if s["src"] in CLIP_LEN and s["tin"] + s["dur"] > CLIP_LEN[s["src"]] + 0.01:', 'if s["src"] in CLIP_LEN and s["tin"] + s["dur"] * s.get("rate", 1.0) > CLIP_LEN[s["src"]] + 0.01:')

# video con data-playback-rate
s = s.replace('''f'data-media-start="{s["tin"]:.4f}" data-track-index="1" style=''', '''f'data-media-start="{s["tin"]:.4f}" data-playback-rate="{s["rate"]:.3f}" data-track-index="1" style=''')

# cámara que flota: extender el bucle hasta ~40 s
s = s.replace("(32.96, .4811, .4963), (34.48, .5217, .5213)]", "(32.96, .4811, .4963), (34.48, .5217, .5213), (37.04, .5, .5), (38.28, .5141, .5), (39.12, .4958, .487)]")
s = s.replace("(32.4, 105.2), (35.0, 104.9)]", "(32.4, 105.2), (35.0, 104.9), (37.04, 104.4), (39.12, 103.5)]")

# subtítulos oscuros sobre pantallas claras
old_c = '''        blanco = any(sg["kind"] == "white" and sg["t"] - 0.05 <= t0 < sg["t1"] for sg in SEG)'''
new_c = '''        tm = t0 + 0.3
        blanco = any((sg["kind"] == "white" or sg["src"] in ("scrA", "scrB", "qwzQR")) and sg["t"] - 0.05 <= tm < sg["t1"] for sg in SEG)'''
assert old_c in s
s = s.replace(old_c, new_c)
f.write_text(s, encoding="utf-8")
print("parche voz4 aplicado")
