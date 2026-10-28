"""Verifica los previews INTA: existe, abre, duración, resolución, audio y sonoridad. uso: python -I verificar.py INTA09 ..."""
import json, re, subprocess, sys
from pathlib import Path
B = Path(r"D:\OneScreen\Contenido\2026\10. Octubre")
for pz in sys.argv[1:]:
    for f, (w, h) in {"16x9": (1920, 1080), "9x16": (1080, 1920), "4x5": (1080, 1350)}.items():
        p = B / pz / "Exports" / f"{pz}.0002_H1C1A1_neutro_{f}_preview.mp4"
        if not p.exists():
            print(pz, f, "NO EXISTE"); continue
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height", "-of", "json", str(p)], capture_output=True, text=True)
        try:
            j = json.loads(r.stdout)
        except Exception:
            print(pz, f, "ILEGIBLE"); continue
        v = [s for s in j["streams"] if s["codec_type"] == "video"]
        a = [s for s in j["streams"] if s["codec_type"] == "audio"]
        ok = bool(v) and (v[0]["width"], v[0]["height"]) == (w, h) and bool(a)
        lu = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(p), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        i = re.findall(r"I:\s+(-?\d+\.\d+) LUFS", lu)
        print(pz, f, "OK" if ok else "REVISAR", round(float(j["format"]["duration"]), 1), "s", i[-1] if i else "?", "LUFS", round(p.stat().st_size / 1e6, 1), "MB")
