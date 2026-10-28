from pathlib import Path
f = Path(__file__).parent / "build_rental.py"
s = f.read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# líneas del bifurcador: salen por debajo de la etiqueta, sin cruzarla
rep('p.append(conn(cid, 1, c0[0] - 30 if FMT == "16" else c0[0] - 20, c0[1] + 70, a[0] + 40, a[1] - nd // 2 - 12, ta - 0.2, 0.7))',
    'p.append(conn(cid, 1, c0[0] - 130, c0[1] + 82, a[0] + 30, a[1] - nd // 2 - 12, ta - 0.2, 0.7))')
rep('p.append(conn(cid, 2, c0[0] + 30 if FMT == "16" else c0[0] + 20, c0[1] + 70, b[0] - 40, b[1] - nd // 2 - 12, tb - 0.2, 0.7, PUR))',
    'p.append(conn(cid, 2, c0[0] + 130, c0[1] + 82, b[0] - 30, b[1] - nd // 2 - 12, tb - 0.2, 0.7, PUR))')
rep('CAPY = {"16": "89%", "9": "49%", "45": "80%"}[FMT]', 'CAPY = {"16": "89%", "9": "49%", "45": "84%"}[FMT]')
rep("""'Las <span class="ac">ventajas</span> de arrendar.', LAY["HY1"], t0 + 0.12""", """'Las <span class="ac">ventajas</span> de arrendar.', LAY["HY1"] - (60 if FMT == "9" else 0), t0 + 0.12""")
f.write_text(s, encoding="utf-8")
print("ok r5")
