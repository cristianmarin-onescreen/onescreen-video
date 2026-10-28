import sys, os, json, glob
sys.path.insert(0, os.path.dirname(__file__))
import edit_vs_voz as e
lote = sys.argv[1]
for f in sorted(glob.glob(os.path.join(lote, "*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    r = d.get("render"); c = d.get("carpeta")
    if not r:
        continue
    # localizar el render por nombre dentro de la lista de carpetas
    carp = [l.strip() for l in open(sys.argv[2], encoding="utf-8") if os.path.basename(l.strip()).startswith(c[:20])]
    if not carp:
        continue
    p = os.path.join(carp[0], r)
    if not os.path.exists(p):
        continue
    try:
        e.transcribir_scribe(p)
        print("OK", os.path.basename(f)[:30], flush=True)
    except Exception as ex:
        print("ERROR", f[-30:], str(ex)[:80], flush=True)
print("DONE", flush=True)
