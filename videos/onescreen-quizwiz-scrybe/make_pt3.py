"""Genera build_rental3_pt.py (pt-BR) a partir de build_rental3.py: textos en pantalla en portugués y eventos atados a las palabras de la narración pt-BR.
Uso: python make_pt3.py   ->   FMT=16 PROJ=... SCRIBE=<scribe_v_pt_a1.json> python build_rental3_pt.py"""
from pathlib import Path
here = Path(__file__).parent
s = (here / "build_rental3.py").read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


# eventos -> índice de palabra en scribe_v_pt_a1.json (0-based, solo palabras)
ALIAS = {("primera", 0): 7, ("tener", 0): 14, ("para", 0): 20, ("onescreen", 0): 24, ("hay", 0): 27, ("dos", 0): 28, ("caminos", 0): 29, ("primero", 0): 30,
         ("contactarnos", 0): 39, ("o", 1): 43, ("daas", 0): 50, ("arrendamiento", 0): 57, ("por", 0): 58, ("cuota", 0): 60, ("llenar", 0): 64, ("toda", 0): 67,
         ("interactivas", 0): 71, ("hay", 1): 72, ("primero", 1): 78, ("pagas", 0): 80, ("siempre", 0): 86, ("soporte", 0): 95, ("prioritario", 0): 97,
         ("si", 0): 99, ("sufre", 0): 103, ("encargamos", 0): 108, ("nosotros", 0): 107, ("quieres", 0): 111, ("pregúntanos", 0): 116, ("explicamos", 0): 122}
rep('''def EV(word, n=0):
    k = [w for w in words if norm(w["text"]) == word]
    return snap(k[n]["start"] + D - LEAD)''', f'''ALIAS = {ALIAS!r}


def EV(word, n=0):
    return snap(words[ALIAS[(word, n)]]["start"] + D - LEAD)''')
rep('2026-10-21_rental_daas/scribe_v_rv_1.json', '2026-10-23_rental_pt/scribe_v_pt_a1.json')
# textos
rep('<span class="l">Tu primera</span>', '<span class="l">Sua primeira</span>')
rep('<span class="b">aula digital</span>', '<span class="b">aula digital</span>')
rep('Toda tu</span>', 'Toda a sua</span>')
rep('<span class="b">institución</span>', '<span class="b">instituição</span>')
rep('<span class="l">¿Quieres adquirir tu</span> <span class="b">pantalla</span>?', '<span class="l">Quer adquirir a sua</span> <span class="b">tela</span>?')
rep('<span class="b">Pregúntanos</span>', '<span class="b">Pergunte</span>')
rep('lets("Dos", "l")', 'lets("Dois", "l")')
rep('lets("caminos.", "b")', 'lets("caminhos.", "b")')
rep('>Comprarla</text>', '>Comprá-la</text>')
rep('>Arrendarla</text>', '>Alugá-la</text>')
rep('>Contáctanos</text>', '>Fale conosco</text>')
rep('lets("Una cuota", "l")', 'lets("Pagamento", "l")')
rep('lets("mensual", "b")', 'lets("mensal", "b")')
rep('lets("Muchas ", "l") + lets("ventajas.", "b")', 'lets("Muitas ", "l") + lets("vantagens.", "b")')
rep('("coin", "Pagas por lo que usas", "Sin comprar de golpe"', '("coin", "Paga só pelo que usa", "Sem comprar de uma vez"')
rep('("refresh", "Siempre actualizada", "Las últimas actualizaciones"', '("refresh", "Sempre atualizada", "As últimas atualizações"')
rep('("head", "Soporte técnico prioritario", "Atención primero"', '("head", "Suporte técnico prioritário", "Atendimento primeiro"')
rep('("shield", "Nosotros nos encargamos", "Si sufre algún daño"', '("shield", "A gente cuida de tudo", "Se sofrer algum dano"')
rep('rv_1', 'rv_1') if False else None
(here / "build_rental3_pt.py").write_text(s, encoding="utf-8")
print("ok build_rental3_pt.py")
