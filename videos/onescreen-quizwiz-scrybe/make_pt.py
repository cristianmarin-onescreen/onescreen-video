"""Genera build_rental_pt.py (pt-BR) a partir de build_rental.py: textos en pantalla y mapa de eventos a las palabras de la narración portuguesa."""
from pathlib import Path
here = Path(__file__).parent
s = (here / "build_rental.py").read_text(encoding="utf-8")


def rep(a, b, cnt=1):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, cnt)


# eventos -> índice de palabra en la narración pt-BR (scribe_v_pt_a1.json)
ALIAS = {("tener", 0): 14, ("para", 0): 20, ("hay", 0): 27, ("daas", 0): 50, ("por", 0): 58, ("hay", 1): 72, ("primero", 1): 78, ("quieres", 0): 111,
         ("caminos", 0): 29, ("primero", 0): 30, ("o", 1): 43, ("contactarnos", 0): 39, ("arrendamiento", 0): 57, ("llenar", 0): 64, ("pantallas", 0): 70,
         ("toda", 0): 67, ("pagas", 0): 80, ("siempre", 0): 86, ("soporte", 0): 95, ("si", 0): 99, ("pregúntanos", 0): 116, ("explicamos", 0): 122,
         ("primera", 0): 7, ("onescreen", 0): 24}
rep('''def EV(word, n=0):
    k = [w for w in words if norm(w["text"]) == word]
    return snap(k[n]["start"] + D - LEAD)''', f'''ALIAS = {ALIAS!r}


def EV(word, n=0):
    return snap(words[ALIAS[(word, n)]]["start"] + D - LEAD)''')
rep('SCRIBE = os.environ.get("SCRIBE", r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-21_rental_daas/scribe_v_rv_1.json")',
    'SCRIBE = os.environ.get("SCRIBE", r"C:/Users/Cristian Marin/Desktop/Claudio/audio_elevenlabs/2026-10-23_rental_pt/scribe_v_pt_a1.json")')
rep('PROJ = Path(f"D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_{FMT}")', 'PROJ = Path(f"D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_{FMT}")')
# textos
rep("""'Dos <span class="ac">caminos</span>.'""", """'Dois <span class="ac">caminhos</span>.'""")
rep('"mon", "Tu OneScreen"', '"mon", "Sua OneScreen"')
rep('"cart", "Comprarla"', '"cart", "Comprar"')
rep('"cal", "Arrendarla"', '"cal", "Locação"')
rep("<span>Contáctanos</span>", "<span>Fale com a gente</span>")
rep("""'nuestro modelo de <span class="ac">arrendamiento.</span>'""", """'nosso modelo de <span class="ac">locação.</span>'""")
rep("""'Una cuota <span class="ac">mensual</span>, accesible.'""", """'Uma <span class="ac">mensalidade</span> acessível.'""")
rep('"cal", "Cada mes"', '"cal", "Todo mês"')
rep("""'Toda tu <span class="ac">institución</span>.'""", """'Toda a sua <span class="ac">instituição</span>.'""")
rep("""'Las <span class="ac">ventajas</span> de arrendar.'""", """'As <span class="ac">vantagens</span> da locação.'""")
rep('("coin", "Pagas por lo que usas", "Sin comprar de golpe"', '("coin", "Você paga pelo que usa", "Sem comprar tudo de uma vez"')
rep('("refresh", "Siempre actualizada", "Las últimas actualizaciones"', '("refresh", "Sempre atualizada", "As últimas atualizações"')
rep('("head", "Soporte técnico prioritario", "Atención primero"', '("head", "Suporte técnico prioritário", "Atendimento em primeiro lugar"')
rep('("shield", "Nosotros nos encargamos", "Si sufre algún daño"', '("shield", "A gente cuida de tudo", "Se a tela sofrer algum dano"')
rep("""'¿Quieres tu <span class="ac">pantalla</span>?'""", """'Quer a sua <span class="ac">tela</span>?'""")
rep("Pregúntanos {line_icon", "Fale com a gente {line_icon")
rep('Tu primera <span class="ac2">aula digital</span>', 'Sua primeira <span class="ac2">sala de aula</span>')
rep('x["text"].replace("DaaS", "DaaS")', '__import__("re").sub("(?i)daas", "DaaS", x["text"])')
rep('<html lang="es">', '<html lang="pt-BR">')
rep('data-composition-id="rental"', 'data-composition-id="rental"')
rep('BIG = {"16": 112, "9": 96, "45": 88}[FMT]', 'BIG = {"16": 112, "9": 72, "45": 68}[FMT]')
(here / "build_rental_pt.py").write_text(s, encoding="utf-8")
print("ok build_rental_pt.py")
