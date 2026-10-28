"""Parche v7: puntos focales verticales, celular a menor escala en vertical, eventos nuevos para los efectos de sonido."""
from pathlib import Path
here = Path(__file__).parent

t = (here / "trims_v4.py").read_text(encoding="utf-8")
t = t.replace('"u1": 0.48', '"u1": 0.60').replace('"u4": 0.50', '"u4": 0.40')
(here / "trims_v4.py").write_text(t, encoding="utf-8")

u = here / "ui3d.py"
s = u.read_text(encoding="utf-8")
s = s.replace('    cam(T["est"] - 0.15, QX + 200, 90, 1.12, -8, 1, 1.2)', '    PM = {"16": 1.0, "9": 0.72, "45": 0.78}[FMT]\n    cam(T["est"] - 0.15, QX + 200, 90, 1.12 * PM, -8, 1, 1.2)', 1)
s = s.replace('    cam(T["esc"] - 0.3, QX + 190, 100, 1.32, -4, 0, 1.0)', '    cam(T["esc"] - 0.3, QX + 190, 90, 1.3 * PM, -4, 0, 1.0)', 1)
u.write_text(s, encoding="utf-8")

b = here / "build_v2.py"
s = b.read_text(encoding="utf-8")
old = 'events={k: EV(k) for k in ("scribe", "quizwiz", "qr", "segundos", "start", "el", "resultados", "implementarlo")}'
assert old in s
s = s.replace(old, 'events={k: EV(k) for k in ("scribe", "quizwiz", "qr", "segundos", "start", "el", "resultados", "implementarlo", "arma", "entregarlo", "estudiante", "escanea", "celular", "poner", "cuando", "pero", "nosotros")}', 1)
b.write_text(s, encoding="utf-8")

m = here / "mix_v2.py"
s = m.read_text(encoding="utf-8")
a = s.index("t_examen = ")
z = s.index("def lufs")
new = '''white = {sg["src"]: sg["t"] for sg in segs if sg["kind"] == "white"}
DROP_V = ev["el"] + 0.083          # la explosión cae 2 cuadros después del paneo a QuizWiz
DROP_M = 12.40
MOFF = DROP_M - DROP_V
EARLY = 0.075                      # los efectos van 60-85 ms antes del evento visual (medido en los proyectos de Cris)
SFX = [("pop", ev["scribe"]), ("tick", ev["start"]), ("hit", DROP_V + EARLY), ("pop", ev["quizwiz"]), ("tick", ev["arma"]), ("tick", ev["entregarlo"] + 0.1),
       ("scan", ev["qr"]), ("whoosh", ev["estudiante"] - 0.3), ("scan", ev["escanea"]), ("swipe", white["ia"]), ("ding", ev["resultados"]),
       ("swipe", white["res"]), ("whoosh", ev["pero"]), ("swipe", white["cta"])]


'''
s = s[:a] + new + s[z:]
m.write_text(s, encoding="utf-8")
print("patch v7 ok")
