"""Elige el momento más estable de un clip (sin movimiento de cámara) para un plano de `need` s. 27-oct, Cris: "en el plano uno hay un movimiento de cámara, escoge un mejor momento".
Mide el desplazamiento global entre cuadros (correlación de fase sobre miniaturas a 8 fps) y busca la ventana con menos movimiento y sin picos; el contenido que se mueve
(alguien escribiendo) no cuenta como movimiento de cámara porque la correlación sigue al fondo dominante. Uso: mejor_ss(ruta, need, ini, dur, mm) -> segundos de inicio."""
import json, subprocess
from pathlib import Path
import numpy as np

CACHE = Path(r"D:/OneScreen/Contenido/2026/10. Octubre/_inta_trabajo/estable_cache.json")
_c = json.load(open(CACHE, encoding="utf-8")) if CACHE.exists() else {}
FPS, WW, HH = 8, 160, 90


def _mov(ruta):
    if ruta in _c:
        return _c[ruta]
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-t", "45", "-i", ruta, "-an", "-vf", f"fps={FPS},scale={WW}:{HH},format=gray", "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = len(a) // (WW * HH)
    if n < 4:
        _c[ruta] = []
        return []
    f = a[: n * WW * HH].reshape(n, HH, WW).astype(np.float32)
    win = np.outer(np.hanning(HH), np.hanning(WW))
    F = [np.fft.fft2((x - x.mean()) * win) for x in f]
    out = [0.0]
    for i in range(1, n):
        R = F[i] * np.conj(F[i - 1])
        R /= np.abs(R) + 1e-6
        c = np.fft.ifft2(R).real
        y, x = np.unravel_index(np.argmax(c), c.shape)
        dy = y if y < HH // 2 else y - HH
        dx = x if x < WW // 2 else x - WW
        out.append(float(np.hypot(dx, dy)))
    _c[ruta] = out
    json.dump(_c, open(CACHE, "w"))
    return out


def mejor_ss(ruta, need, ini=1.2, dur=None, mm=None):
    m = _mov(ruta)
    if not m:
        return None
    L = int(round((need + 0.3) * FPS))
    mejor = None
    for s in range(int(ini * FPS), max(int(ini * FPS) + 1, len(m) - L + 1)):
        w = m[s: s + L]
        if len(w) < L:
            break
        # movimiento medio + castigo a los picos (arranques, paneos, golpes) + leve preferencia por el "mejor momento" de la ficha
        sc = float(np.mean(w)) + 0.7 * float(np.max(w)) + (0.04 * abs(s / FPS - mm) if mm is not None else 0)
        if mejor is None or sc < mejor[0]:
            mejor = (sc, s / FPS)
    return mejor[1] if mejor else None
