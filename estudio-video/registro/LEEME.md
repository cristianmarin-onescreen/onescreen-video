# Registro de videos (para Claude y para el planner)

**Fuente de verdad: la hoja de Google "Directorio - Producción de video"** (`1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks`). Pestañas, columnas, dueños y flujo: [HOJA.md](HOJA.md). Los CSV de esta carpeta (`guiones`, `produccion`, `planner`, `historico`) son su **espejo** para sesiones sin acceso a la hoja y para git; `manifest.json` es lo mismo en un solo JSON. Se editan con `herramientas/registro.py` (no a mano, para no romper IDs) y cada cambio se escribe también en la hoja. Si hay diferencias, manda la hoja. Los CSV anteriores a la arquitectura v2 están en `legacy/` (no se borran).

## Cuatro pestañas, cuatro dueños
1. **Guiones**: la skill de estrategia los escribe y Cris los aprueba **antes** de producir. Yo solo escribo `Estado` y `Versiones generadas (IDs)`.
2. **Producción**: la cola de versiones activas; la manejo yo.
3. **Planner**: un script local en el PC de Cris publica y mide a 24/48/72 h. Yo no escribo ahí.
4. **Histórico**: archivo de versiones cerradas, con resultado y decisión; lo lee la skill de estrategia.

## IDs y nombres
- **ID de versión** `<PIEZA>.<NNNN>` (p. ej. `RENT.0006`, `INTA03.0001`); la pieza es el ID de ángulo del guion. Un cambio = un ID nuevo; nunca se reutiliza. Todos los formatos de una versión comparten ID.
- **Nombre de archivo** `<ID>_<H#C#A#>_<voz>_<formato>[_preview].<ext>` (`registro.py nombre`, `registro.py validar CARPETA`). H = hook (primeros ~3 s), C = contenido, A = CTA; qué es cada uno se lee en la fila de Guiones (Hook 1/2/3, Cuerpo, CTA, Otras variantes).
- Voz/idioma es otra columna; un acento o idioma nuevo es otra versión con su ID (`Eje que cambia = Idioma-voz`).

## Estados y aprobación
- **Producción:** Preview → Aprobada → Vigente (Reemplazada, Rechazada, Archivada). **Solo se publica Aprobada o Vigente**; el planner lee solo esas.
- **Decisión de Cris** (amarilla): Aprobada / Con cambios / Rechazada. Con Aprobada: Estado Aprobada, marcar usos en el Directorio de planos, crear el `.prproj`. **No se crean filas de publicación**: el planner las crea solo.
- Previews no van a Drive (chat de la sesión + `Exports` local). Exports aprobados sin `_preview` van a la carpeta de Drive "Producción de video" (https://drive.google.com/drive/folders/1cda9LOGC2Yb_wli88bNpmJ0BRFqOnmDm), una subcarpeta por pieza, y su link a `Export en Drive (listo para subir)`.

## Cierre
Una versión sale de Producción a Histórico cuando su Estado es Reemplazada/Rechazada/Archivada, o cuando todas sus filas del Planner están Cerrada o Retirada (`registro.py cierres` y `registro.py cerrar ID`). Copiar, verificar, recién entonces borrar. RENT.0001 a RENT.0005 esperan la confirmación de Cris.
