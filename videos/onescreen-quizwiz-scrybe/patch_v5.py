"""Parche v5: altura de las interfaces 3D en 16:9, subtítulos con píldora sobre la escena de interfaces, toque más visible."""
from pathlib import Path
here = Path(__file__).parent
u = here / "ui3d.py"
t = u.read_text(encoding="utf-8")
t = t.replace('S_FIT = {"16": 0.9,', 'S_FIT = {"16": 0.84,', 1).replace('CYF = {"16": 0.55,', 'CYF = {"16": 0.49,', 1)
t = t.replace('width:76px;height:76px;margin:-38px 0 0 -38px;border-radius:50%;background:rgba(125,0,186,.2);border:3px solid rgba(125,0,186,.65)',
              'width:92px;height:92px;margin:-46px 0 0 -46px;border-radius:50%;background:rgba(125,0,186,.30);border:4px solid rgba(125,0,186,.85)', 1)
t = t.replace('width:76px;height:76px;margin:-38px 0 0 -38px;border-radius:50%;border:4px solid #7d00ba', 'width:92px;height:92px;margin:-46px 0 0 -46px;border-radius:50%;border:5px solid #7d00ba', 1)
u.write_text(t, encoding="utf-8")

f = here / "build_v2.py"
s = f.read_text(encoding="utf-8")
old = '''caps_html.append(f'<div class="clip cap{" capd" if blanco else ""}"'''
new = '''pill = any(sg["src"] == "ui" and sg["t"] - 0.05 <= tm < sg["t1"] for sg in SEG)
        caps_html.append(f'<div class="clip cap{" capd" if blanco else ""}{" capp" if pill else ""}"'''
assert old in s
s = s.replace(old, new, 1)
s = s.replace('.capd{{color:#1a1a1a;text-shadow:none}}\n', '.capd{{color:#1a1a1a;text-shadow:none}}\n.capp{{background:none}} .capp span{{}}\n', 1)
f.write_text(s, encoding="utf-8")
print("patch v5 ok")
