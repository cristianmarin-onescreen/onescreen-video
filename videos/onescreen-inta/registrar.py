"""Registra en el espejo local (registro.py nueva) la versión base .0001 de cada pieza INTA. La hoja de Producción se escribe aparte (conector de Sheets).
uso: python -I registrar.py"""
import subprocess, sys, os
NOM = {
"INTA15": ("Caso Palmas del Cesar (LinkedIn corporativo Colombia): de viajar a Bucaramanga a reunirse desde la plantación", "N4"),
"INTA16": ("Una reunión que se transcribe sola: nadie sale con una versión distinta de lo que se decidió (Scrybe; LinkedIn corporativo Colombia)", "N2"),
"INTA17": ("Antes de elegir pantalla para la sala de reuniones, la pregunta que casi nadie hace: quién responde cuando falla (Gurú)", "N3"),
"INTA18": ("Renta 1: comprar de una vez o pagar una cuota mensual, qué le hace cada camino al flujo de caja", "N3"),
"INTA19": ("Renta 2: directo de fábrica, sin intermediarios", "N4"),
"INTA20": ("Renta 3: la tecnología que compraste hace cinco años (nunca obsoleto)", "N2"),
"INTA21": ("Renta 4: una sola cuota con todo incluido (quien instala, mantiene y da soporte)", "N5"),
"INTA22": ("Empresas: las ideas de la reunión no deberían borrarse con la pizarra (Write)", "N2"),
"INTA23": ("IA: la que responde solo desde lo que tú le diste (QuizWiz, SuprNotes y Gurú)", "N3"),
"INTA24": ("Caso de éxito Areandina: la pantalla la eligieron los docentes", "N4"),
"INTA25": ("Caso de éxito Clínica Maxilofacial del Caribe: ver el procedimiento en vivo", "N4"),
}
env = dict(os.environ, PYTHONIOENCODING="utf-8")
for pz, (nom, nivel) in (NOM.items() if __name__ == "__main__" else []):
    r = subprocess.run([sys.executable, "herramientas/registro.py", "nueva", pz, "--nombre", nom, "--version", "v1", "--hook", "H1", "--contenido", "C1", "--cta", "A1", "--eje", "Base",
                        "--voz", "neutro", "--cambio", "Base (preview 26-oct-2026): planos con LUT neutra solo para ver", "--builder", "videos/onescreen-inta/build_inta.py",
                        "--formatos", "16x9, 9x16, 4x5", "--vertical", "INT", "--nivel", nivel],
                       capture_output=True, text=True, cwd=r"C:\Users\Cristian Marin\Desktop\Claudio\estudio-video", env=env)
    print(r.stdout.strip() or r.stderr.strip()[-300:])
