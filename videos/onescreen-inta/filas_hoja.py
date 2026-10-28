"""Genera las 12 filas de Producción (A..AD) de los previews INTA en JSON, para pegarlas en la hoja con el conector. uso: python -I filas_hoja.py"""
import json, sys
sys.path.insert(0, r"C:\Users\Cristian Marin\Desktop\Claudio\videos\onescreen-inta")
from registrar import NOM
B = r"D:\OneScreen\Contenido\2026\10. Octubre"
NOM = dict({"INTA09": ("Tus estudiantes ya viven en pantallas táctiles, ¿y su aula?", "N1")}, **NOM)
BANDERA = {
 "INTA15": "[REVISAR: permiso y vigencia] del caso Palmas del Cesar y de su cita; planos de entrevistas con clientes requieren aprobación.",
 "INTA16": "[FALTA DATO: URL de la ficha T7 Empresas]. La voz dice 'más de veinte idiomas'.",
 "INTA17": "[REVISAR: soporte 'gratis y de por vida' tal como lo promete la ficha vigente].",
 "INTA18": "La voz leyó 'Gurú Plus' rápido (Scribe: 'Gruplos'); revisar. Planos genéricos: el Directorio casi no tiene planos de dinero/cuota.",
 "INTA19": "[REVISAR: garantía] tiempos de reparación dependen de disponibilidad y hay exclusiones por mal uso.",
 "INTA20": "'Gurú Plus' sonó como 'Guru Plus' en Scribe; revisar. Renovación solo en leasing.",
 "INTA21": "[REVISAR: 'en menos de veinticuatro horas' es promesa de la web; confirmar con ventas].",
 "INTA22": "[FALTA DATO: URL de la ficha T7 Empresas].",
 "INTA23": "La voz leyó 'SuprNotes' como 'SuperNotes'; revisar pronunciación. Sin 'en menos de 5 segundos' de QuizWiz.",
 "INTA24": "[REVISAR: permiso y vigencia] del caso Areandina y de la cita (sale del testimonial de la home).",
 "INTA25": "[REVISAR: permiso y vigencia] del caso, de la cita y de mostrar procedimientos quirúrgicos (privacidad de pacientes). Sin planos de cirugía en el Directorio: se usó clase/clínica.",
}
filas = []
for pz, (nom, nivel) in NOM.items():
    d = json.load(open(rf"{B}\{pz}\Proyecto\planos.json", encoding="utf-8"))
    ids = []
    for p in d["planos"]:
        if p["id"] and p["id"] not in ids:
            ids.append(p["id"])
    filas.append([f"{pz}.0001", pz, nom, "v1", "H1", "C1", "A1", "Base", "", "neutro", "16x9, 9x16, 4x5", "Preview",
                  "Enviado por el chat de la sesión; copia local en ...\\" + pz + "\\Exports (archivos _preview)", "Pendiente", "", "",
                  "Base: preview del guion aprobado en sesión el 26-oct-2026 (solo H1). Planos con conversión neutra S-Log3 solo para ver (sin color de Cris); render draft",
                  "2026-10-26", ", ".join(ids), "", "", rf"{B}\{pz}\Exports", "", "No", "", "", "videos/onescreen-inta/producir.py",
                  "Guion aprobado en la sesión (orden de Cris). Voz: Hale colombiano (voz a voz). " + BANDERA.get(pz, ""), "INT", nivel])
open(B + "/_inta_trabajo/filas.json", "w", encoding="utf-8").write(json.dumps(filas, ensure_ascii=False))
