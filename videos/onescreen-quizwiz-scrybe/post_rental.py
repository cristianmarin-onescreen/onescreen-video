"""Post del video Rental: aberración cromática leve, cierre con la intro de marca (con su sonido) y audio mezclado. Uso: python post_rental.py FMT raw.mp4 salida.mp4"""
import os, subprocess, sys
fmt, raw, out = sys.argv[1:4]
mix = os.environ.get("MIX", r"D:\OneScreen\Contenido\2026\10. Octubre\Rental DaaS\Proyecto\mix_rental.wav")
intro = os.environ.get("INTRO") or rf"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2_{fmt}\media\intro.mp4"
fc = "[0:v]rgbashift=rh=-1:bh=1:edge=smear,format=yuv420p[a];[1:v]setsar=1,format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[v]"
cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", raw, "-i", intro, "-i", mix, "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
       "-r", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-600:] if r.returncode else "ok " + out)
