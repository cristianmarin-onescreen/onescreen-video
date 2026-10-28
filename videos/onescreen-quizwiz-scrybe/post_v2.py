"""Post de la v2: aberración cromática leve (R -/B +), cierre con la intro de marca del Brand kit y audio mezclado. Uso: python post_v2.py FMT raw.mp4 salida.mp4"""
import subprocess, sys
fmt, raw, out = sys.argv[1:4]
mix = r"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2work\mix_v3.wav"
intro = rf"D:\OneScreen\Contenido\2026\10. Octubre\QuizWiz y Scrybe\Proyecto\v2_{fmt}\media\intro.mp4"
W, H = {"16": (1920, 1080), "9": (1080, 1920), "45": (1080, 1350)}[fmt]
fc = f"[0:v]rgbashift=rh=-1:bh=1:edge=smear,format=yuv420p[a];[1:v]format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[v]"
cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", raw, "-i", intro, "-i", mix, "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
       "-r", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-600:] if r.returncode else "ok " + out)
