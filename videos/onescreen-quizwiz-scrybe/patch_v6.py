from pathlib import Path
f = Path(__file__).parent / "build_v2.py"
s = f.read_text(encoding="utf-8")
a = 'data-track-index="5">{txt}</div>\')'
assert a in s
s = s.replace(a, 'data-track-index="5">{("<span class=pl>" + txt + "</span>") if pill else txt}</div>\')', 1)
b = ".capd{{color:#1a1a1a;text-shadow:none}}\n"
assert b in s
s = s.replace(b, b + ".pl{{background:rgba(255,255,255,.9);padding:4px 18px;border-radius:12px;color:#1a1a1a;text-shadow:none}}\n", 1)
f.write_text(s, encoding="utf-8")
print("ok v6")
