# Directorio de video — análisis de planos con Gemini

Llena las columnas amarillas de la pestaña **Directorio** del Sheet "Directorio de video" y la pestaña **Segmentos**
con lo que Gemini 3.5 Flash-Lite ve y oye en cada plano (video completo a 1 cuadro/s más audio), vía Batch API (mitad de precio).

## Uso

```bash
python armar_cola.py              # datos/planos.json: planos sin Producto, con color primero y luego los más recientes
python lote.py --limite 15        # piloto: revisa la hoja antes de seguir
python lote.py --tope 30          # todo; reanudable (datos/estado.json): si se corta, se vuelve a correr igual
python lote.py --reintentar-errores --max-salida 12000   # pasada final para los que fallaron
python lote.py --drive --tope 10  # también los que solo están en Drive: los baja con rclone a D:\_lote_drive y los borra
python informe.py                 # avance y costo real por video (datos/costos.csv)

# re-análisis de planos con errores (IDs en un JSON): cola, estado y fichas aparte, imágenes de referencia de producto
python armar_cola.py --ids datos/ids_reanalisis.json
python lote.py --reanalisis --drive --max-salida 12000
```

Las imágenes de referencia viven en `datos/referencias` (Wandr real, render del T7 y contraejemplos: trituradora IDEAL,
impresora Pantum, parlante Clary Bass); `NOTAS_REFERENCIA` en lote.py dice qué es cada una. Al escribir, Producto, Software y
Permisos pasan por `comun.normalizar_*` (nombres del catálogo) y en stock o IA el modelo de pantalla baja a "modelo no identificable".

## Qué necesita

- `GEMINI_API_KEY` en el entorno (Google AI Studio, tier pagado).
- `ffmpeg`/`ffprobe` en el PATH.
- Composio CLI dentro de WSL Ubuntu con la cuenta `googledrive` conectada: `sheets_wsl.py` usa
  `composio proxy` contra la API de Sheets. El ayudante cierra stdin, si no Composio se queda esperando.
- Para `--drive`: rclone en `~\herramientas\rclone\rclone.exe` (o la variable `RCLONE`) con un remoto de solo lectura,
  `rclone config create gdrive drive scope=drive.readonly` (Cris aprueba el acceso en el navegador). Composio no sirve para
  bajar videos: su proxy solo devuelve JSON y la herramienta de descarga se vence. Opcional: `datos/tamanos_drive.json`
  (ID plano → bytes) para que el lote no baje más de lo que cabe en el disco a la vez.

## Qué escribe

- Directorio: D a N, P a R, T a X, AI y AJ. No toca Estado (O), Transcripción (S), Archivo graduado/LUT (AB, AC) ni Vigencia (AK).
  Si Información adicional decía UCUENCA, lo conserva.
- Segmentos: A, C, D y F a N. B y E son fórmulas. Antes de escribir valida los encabezados de ambas pestañas.

## Decisiones que no hay que deshacer

- Copia liviana con `-discard:v nokey` antes de `-i`: el demuxer lee solo los cuadros clave (~12 % del archivo).
  En el HDD D: fue 7 s en vez de 68 s para 3,2 GB. Va en 2 copias simultáneas por disco.
- Se decodifican enteros los archivos de menos de 200 MB, los clips de IA (traen un solo cuadro clave y la Files API
  los deja en FAILED) y las grabaciones de pantalla.
- Resolución alta hasta 40 min (~290 tokens/s); media para los más largos (~91 tokens/s). La baja da "invalid argument".
  Lo que pase de 2 h 30 min se corta y queda dicho en Información adicional.
- Gemini a veces escribe 1:15 como 115 en campos de segundos: `comun.segundos()` lo corrige.
- `datos/` queda fuera de git: las rutas y nombres de archivo traen nombres de clientes.

Corrida del 23-oct-2026: USD 16,45 por los 4.636 planos en disco (≈ USD 0,003 por minuto de video) y USD 2,34 por los
planos de Drive (380 GB bajados a ~65 GB/h).
