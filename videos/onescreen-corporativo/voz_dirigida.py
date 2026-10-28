"""Locución dirigida (Cris, 26-oct-2026: la toma voz a voz "suena mejor, pero está muy plana, sin emoción, falta el director").
La voz a voz copia la interpretación de la fuente, así que la dirección va en la locución colombiana de origen:
  v3 -> Cristian Sánchez con eleven_v3 y etiquetas de interpretación por frase
  v2 -> Cristian Sánchez con eleven_multilingual_v2, menos estabilidad y más estilo
Después cada toma pasa a Hale (hale_co.py sts) y se mide su expresividad (rango de F0) contra la toma plana.
uso: python -I voz_dirigida.py v3|v2 PREFIJO N [VOZ_FUENTE]"""
import json, os, subprocess, sys, urllib.request
from pathlib import Path

OUT = Path(r"C:\Users\Cristian Marin\Desktop\Claudio\audio_elevenlabs\2026-10-25_corporativo")
FUENTE = "o2vbTbO3g4GrKUg7rehy"   # Cristian Sánchez, colombiano
KEY = os.environ["ELEVENLABS_API_KEY"]
DIRIGIDO = ("[serious, close, like talking to a manager] Si tu sala de reuniones depende de un proyector, "
            "[listing, slightly annoyed] una cámara web, micrófonos aparte... [ironic] y cables por todos lados, "
            "[short pause] [confident, leaning in] esto te interesa. "
            "[excited, proud] Una OneScreen... [emphatic] los reemplaza a todos. "
            "[energetic, upbeat] Compartes pantalla sin cables. [quick] Cámara y audio integrados. "
            "[pleased, smiling] Y cada reunión termina transcrita, con su resumen. "
            "[warm, reassuring] Si tu equipo necesita ayuda, el botón Gurú lo conecta en vivo con ingenieros de OneScreen. "
            "[inviting, energetic] Solicita tu demo.")
LIMPIO = ("Si tu sala de reuniones depende de un proyector, una cámara web, micrófonos aparte... ¡y cables por todos lados! Esto te interesa. "
          "Una OneScreen... ¡los reemplaza a todos! Compartes pantalla sin cables. Cámara y audio integrados. Y cada reunión termina transcrita, con su resumen. "
          "Si tu equipo necesita ayuda, el botón Gurú lo conecta en vivo con ingenieros de OneScreen. ¡Solicita tu demo!")
modo, pre, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
FUENTE = sys.argv[4] if len(sys.argv) > 4 else FUENTE
for i in range(n):
    if modo == "v3":
        body = {"text": DIRIGIDO, "model_id": "eleven_v3", "voice_settings": {"stability": 0.0}}          # 0 = "creative": más interpretación
    else:
        body = {"text": LIMPIO, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.3, "similarity_boost": 0.8, "style": 0.65, "use_speaker_boost": True}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{FUENTE}?output_format=mp3_44100_192", json.dumps(body).encode(), {"xi-api-key": KEY, "content-type": "application/json"})
    p = OUT / f"{pre}_{i}.mp3"
    p.write_bytes(urllib.request.urlopen(req).read())
    print("ok", p.name, flush=True)
