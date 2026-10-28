"""Etapa 3: luz adaptativa por toma. Curva monótona (PCHIP) por canal, anclada en los percentiles de la toma."""
import numpy as np
from scipy.interpolate import PchipInterpolator

LUMA = np.array([0.2126, 0.7152, 0.0722])
Q = np.array([0.5, 5, 25, 50, 75, 95, 99.5])


def percentiles(img, mask=None):
    Y = img @ LUMA
    if mask is not None:
        Y = Y[mask]
    return np.percentile(Y, Q)


def objetivos(p, cfg_luz):
    """Percentiles base de la toma -> percentiles objetivo (p0.5 y p99.5 anclados, medios con S suave)."""
    lo, hi = cfg_luz["ancla_negros"], cfg_luz["ancla_blancos"]
    rango = p[-1] - p[0]
    s = (hi - lo) / rango
    smax = cfg_luz["max_estiramiento"]
    if s > smax:                                  # no estirar más de lo que aguantan 8 bits
        hi = lo + smax * rango
    u = (p - p[0]) / rango
    k, c = cfg_luz["s_k"], cfg_luz["s_c"]
    y = lo + (hi - lo) * (u + k * u * (1 - u) * (u - c))
    f = cfg_luz["fuerza"]
    return p + f * (y - p)


def curva(p, cfg_luz, n=4096):
    """Tabla 1D (n puntos en 0-1). Hombro suave: p99.5 -> objetivo y 1.0 -> 1.0."""
    y = objetivos(p, cfg_luz)
    xs = np.concatenate([[0.0], p, [1.0]])
    ys = np.concatenate([[0.0], y, [1.0]])
    keep = np.concatenate([[True], np.diff(xs) > 1e-4])          # x estrictamente creciente
    xs, ys = xs[keep], ys[keep]
    ys = np.maximum.accumulate(ys + np.arange(len(ys)) * 1e-6)    # monótona
    t = np.linspace(0, 1, n)
    return np.clip(PchipInterpolator(xs, ys, extrapolate=True)(t), 0, 1.5)


def aplicar_curva(img, tabla):
    n = len(tabla)
    return np.interp(np.clip(img, 0, 1), np.linspace(0, 1, n), tabla)


def exposicion(img, ev, rodilla=0.85):
    """Exposición en pasos sobre luz lineal (gamma 2.2) con hombro suave: el negro no se mueve y los blancos no se queman."""
    lin = np.power(np.clip(img, 0, 1), 2.2) * (2.0 ** ev)
    y = np.power(np.clip(lin, 0, None), 1 / 2.2)
    sobre = np.maximum(y - rodilla, 0)
    y = np.where(y > rodilla, rodilla + (1 - rodilla) * np.tanh(sobre / (1 - rodilla)), y)
    return np.clip(y, 0, 1).astype(np.float32)


def luma_cara(img, hsl):
    """Luma mediana de la piel de la cara: mayor mancha compacta de matiz piel (sin pelo/sombras: luma >= 0.25, sat 0.15-0.6),
    en la mitad superior-central del cuadro. None si no hay mancha fiable. (OpenCV 5 ya no trae Haar; sin modelos externos.)"""
    import cv2
    import etapa4
    h, w = img.shape[:2]
    x = np.clip(img, 0, 1).astype(np.float32)
    prot = etapa4.proteccion_piel(x, hsl)[..., 0]
    hsv = cv2.cvtColor(x, cv2.COLOR_RGB2HSV)
    l = x @ LUMA
    m = ((prot > 0.5) & (l >= 0.25) & (hsv[..., 1] >= 0.15) & (hsv[..., 1] <= 0.6)).astype(np.uint8)
    m[int(h * 0.75):] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n < 2:
        return None
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    if st[k, cv2.CC_STAT_AREA] < 0.004 * h * w:
        return None
    return float(np.median(l[lab == k]))
