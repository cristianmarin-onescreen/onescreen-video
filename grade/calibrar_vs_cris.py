"""Calibra el look contra el render final de Cris (sin renderizar video): usa los mismos fotogramas del plano crudo
y del render de Cris (16:9 final) y compara estadísticos de color/luz.

Uso: python -I grade/calibrar_vs_cris.py [clave=valor ...]     p.ej.  luz.ancla_negros=0.03 look.hsl_inverso.saturacion=1.0
Pares (plano crudo recortado -> render de Cris) en PARES; los recortes están en D:\\hf-render\\estilos\\cal.
"""
import os, sys, subprocess
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
import pipeline as pl
from etapa1 import cargar_config, sondear, decodificar_frame
import etapa4

CAL = r"D:/hf-render/estilos/cal/"
J = r"D:/OneScreen/Contenido/2026/7. Julio/"
RGR = J + "VIDEO. Regreso a clases/Regreso a clases_16x9_Subs.mp4"
COL = J + "VIDEO. Colaboradores que colaboran/Colaboradores que colaboran_16x9_Subs.mp4"
NAT = J + "VIDEO. Nativos digitales/Nativos digitales_16x9_Clean.mp4"
PARES = [("colab", "colab_c1573", COL, [(0.2, 0.2), (0.6, 0.6), (1.0, 1.0)]), ("nat", "nat_c1565", NAT, [(0.15, 0.15), (0.35, 0.35)]),
         ("reg0", "reg_c1577", RGR, [(0.1, 0.1), (0.25, 0.25)]), ("r1", "reg_r1", RGR, [(0.3, 18.0), (0.8, 18.5)]),
         ("r2", "reg_r2", RGR, [(0.3, 24.3), (0.8, 24.8)]), ("r3", "reg_r3", RGR, [(0.3, 29.4), (0.8, 29.9)]),
         ("r4", "reg_r4", RGR, [(0.3, 30.8), (0.8, 31.3)])]
LUMA = np.array([.2126, .7152, .0722], np.float32)
PCT = [1, 5, 25, 50, 75, 95, 99]


def fr(path, t):
    out = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-vf", "scale=960:540:flags=area",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(out, np.uint8), cv2.IMREAD_COLOR)[:, :, ::-1].astype(np.float32) / 255


def region(x):
    h, w = x.shape[:2]
    return x[int(.08 * h):int(.62 * h), int(.15 * w):int(.85 * w)]


def estad(x, hsl):
    r = region(x).reshape(-1, 3)
    l = r @ LUMA
    m = etapa4.proteccion_piel(region(x), hsl)[..., 0].reshape(-1) > 0.5
    hsv = cv2.cvtColor(np.ascontiguousarray(region(x)), cv2.COLOR_RGB2HSV).reshape(-1, 3)
    d = dict(p=np.percentile(l, PCT), media=r.mean(0), piel_l=np.median(l[m]) if m.sum() > 300 else np.nan,
             piel_rgb=r[m].mean(0) if m.sum() > 300 else np.full(3, np.nan), sat_fondo=hsv[~m, 1].mean())
    return d


def poner(cfg, clave, valor):
    d = cfg
    ks = clave.split(".")
    for k in ks[:-1]:
        d = d[k]
    d[ks[-1]] = float(valor)


def correr(ajustes=(), verbose=True):
    cfg = cargar_config()
    for a in ajustes:
        k, v = a.split("=")
        poner(cfg, k, v)
    lut1, lut2 = pl.cargar_luts()
    filas = []
    for n, clip, his, ts in PARES:
        video = CAL + clip + ".mp4"
        P, rep, _ = pl.analizar(video, cfg, lut1)
        info = sondear(video)
        for ta, tb in ts:
            src, _ = decodificar_frame(video, ta, cfg["entrada"]["rango"], cfg["entrada"]["matriz"], info)
            src = cv2.resize(src, (960, 540), interpolation=cv2.INTER_AREA)
            mia = np.clip(pl.frame_python(src, P, cfg, lut1, lut2), 0, 1)
            suya = fr(his, tb)
            filas.append((n, estad(mia, cfg["look"]["hsl_inverso"]), estad(suya, cfg["look"]["hsl_inverso"])))
    dp = np.array([b["p"] - a["p"] for _, a, b in filas])
    res = dict(
        luma_p=dict(zip(PCT, dp.mean(0).round(3))), luma_p_sd=dict(zip(PCT, dp.std(0).round(3))),
        piel_l=float(np.nanmean([b["piel_l"] - a["piel_l"] for _, a, b in filas])),
        sat_fondo_razon=float(np.mean([b["sat_fondo"] / a["sat_fondo"] for _, a, b in filas])),
        cromatico_rms=float(np.sqrt(np.mean([[np.log(b["media"][0] / b["media"][1]) - np.log(a["media"][0] / a["media"][1]),
                                              np.log(b["media"][2] / b["media"][1]) - np.log(a["media"][2] / a["media"][1])] for _, a, b in filas]) ** 2)),
        piel_rgb_razon=np.nanmean([b["piel_rgb"] / a["piel_rgb"] for _, a, b in filas], axis=0).round(3).tolist())
    # error global (menor = mejor): percentiles de luma + piel + saturación + cromático
    res["error"] = float(np.sqrt(np.mean(dp ** 2)) + abs(res["piel_l"]) + abs(res["sat_fondo_razon"] - 1) * 0.5 + res["cromatico_rms"])
    if verbose:
        print("luma suya-mia por percentil (media):", res["luma_p"])
        print("  sd entre fotogramas:", res["luma_p_sd"])
        print(f"luma de la piel suya-mia {res['piel_l']:+.3f} | sat fondo razon {res['sat_fondo_razon']:.3f} | cromático RMS {res['cromatico_rms']:.3f} | razón RGB piel {res['piel_rgb_razon']}")
        print(f"ERROR global {res['error']:.4f}")
    return res


if __name__ == "__main__":
    correr(sys.argv[1:])
