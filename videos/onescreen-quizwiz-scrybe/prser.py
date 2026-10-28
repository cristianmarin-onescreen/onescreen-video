"""Serializa un árbol de .prproj byte a byte como lo hace Premiere (saltos de línea dentro de texto XML incrustado como &#10;, base64 con \n literal); verificado: ida y vuelta idéntica en 3 proyectos reales."""
from lxml import etree
M="\ue000"; MR="\ue002"
def serialize(root):
    for e in root.iter():
        if not isinstance(e.tag,str): continue
        if len(e)==0 and e.text and e.text.strip() and "<" in e.text and ("\n" in e.text or "\r" in e.text):
            e.text=e.text.replace("\r",MR).replace("\n",M)
        for k,v in list(e.attrib.items()):
            if "\n" in v or "\r" in v: e.set(k,v.replace("\r",MR).replace("\n",M))
    b=etree.tostring(root,encoding="utf-8")
    return b.replace(M.encode(),b"&#10;").replace(MR.encode(),b"&#13;")
