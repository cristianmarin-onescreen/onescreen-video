r"""Voz con la receta que Cris aprobó en INTA37 ("exp_d", 28-oct): fuente colombiana (Cristian Sánchez) con eleven_v4, es, speed 1,12, style 0,6, stability 0,45,
guion dirigido ENÉRGICO (etiquetas en inglés, MAYÚSCULA en el énfasis) -> voz a voz a Hale (stability 0,2, similarity 0,7, style 0,7). Sin acelerar en el post (TEMPO=1.0).
La carpeta de la pieza se busca en D:\OneScreen\Contenido\AAAA\MM. Mes\<Pieza>\Voz (o con la variable CONTENIDO). Escribe en Voz\vNNNN\ (siguiente número libre: nunca pisa una toma anterior)
y se niega si existe Voz\aprobada\ (la voz aprobada no se regenera) salvo FORZAR=1 con permiso de Cris.
Después: python -I voz_post.py <Pieza> (recorta silencios + Scribe). uso: python -I voz_exp_d.py INTA20 [INTA21 ...]"""
import json, os, re, subprocess, sys, urllib.request
from pathlib import Path
KEY = os.environ["ELEVENLABS_API_KEY"]; HALE = "wWWn96OtTHu1sn8SRGEr"; COL = "o2vbTbO3g4GrKUg7rehy"
CONTENIDO = Path(os.environ.get("CONTENIDO", r"D:\OneScreen\Contenido"))


def carpeta_voz(pz):
    c = sorted(CONTENIDO.glob(f"*/*/{pz}/Voz"))
    if not c:
        raise SystemExit(f"No encuentro {CONTENIDO}\\AAAA\\MM. Mes\\{pz}\\Voz")
    return c[-1]   # el mes más reciente


def siguiente_version(voz):
    n = [int(m.group(1)) for p in voz.glob("v[0-9][0-9][0-9][0-9]") if (m := re.fullmatch(r"v(\d{4})", p.name))]
    return voz / f"v{(max(n) + 1) if n else 1:04d}"


if __name__ == "__main__":
    for pz in sys.argv[1:]:
        voz = carpeta_voz(pz)
        if (voz / "aprobada").exists() and os.environ.get("FORZAR") != "1":
            raise SystemExit(f"{pz}: hay Voz\\aprobada\\; no se regenera sin permiso de Cris (FORZAR=1).")
        out = siguiente_version(voz); out.mkdir()
        txt = (voz / "guion_dirigido_v3.txt").read_text(encoding="utf-8")
        body = {"text": txt, "model_id": "eleven_v4", "language_code": "es", "voice_settings": {"stability": 0.45, "style": 0.6, "speed": 1.12, "use_speaker_boost": True}}
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{COL}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
        fu = out / f"{pz}_fuente_col.mp3"; fu.write_bytes(urllib.request.urlopen(req).read())
        r = subprocess.run(["curl", "-s", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{HALE}?output_format=mp3_44100_192", "-H", "xi-api-key: " + KEY,
            "-F", "model_id=eleven_multilingual_sts_v2", "-F", "voice_settings=" + json.dumps({"stability": 0.2, "similarity_boost": 0.7, "style": 0.7}), "-F", f"audio=@{fu}"], capture_output=True)
        if r.stdout[:1] == b"{":
            raise SystemExit(r.stdout[:300])
        o = out / f"{pz}_hale.mp3"; o.write_bytes(r.stdout)
        d = lambda f: round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout), 1)
        print(pz, out.name, "fuente", d(fu), "s | hale", d(o), "s", flush=True)
