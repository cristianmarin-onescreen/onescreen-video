# Hoja maestra: "Directorio - Producción de video" (arquitectura v2, 26-oct-2026)

**Fuente de verdad del registro de videos.** Los CSV de esta carpeta son su espejo para sesiones sin acceso a la hoja y para git; si difieren, manda la hoja.

- Link: https://docs.google.com/spreadsheets/d/1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks/edit
- ID: `1a2SHROmw11oD-LZzvU8Qg45JV66Z_i_7DInVEr71Jks` (locale es_CO). Usa siempre `sheetId` en las llamadas de formato.
- Conectada con el **Directorio maestro de planos** (`1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w`, pestaña Directorio): al aprobar una versión se marcan los usos de sus planos.
- Pauta de Colombia (Meta y Google): la gestiona la agencia BigSEO. Aquí solo se dejan los creativos listos.

## Cuatro pestañas, cuatro dueños

| Pestaña | sheetId | Una fila = | Escribe | Espejo CSV |
|---|---|---|---|---|
| **Guiones** | 3001 | un ángulo (pieza) | Skill de estrategia. **Yo solo `Estado` y `Versiones generadas (IDs)`** (y `Estado = Cerrado` al cerrar todo) | `guiones.csv` |
| **Producción** | 2001 | una versión exportada (un ID, todos sus formatos) | Yo (todo menos amarillas) | `produccion.csv` |
| **Planner** | 3002 | una publicación (formato × plataforma) | Script del planner. **Yo no escribo** | `planner.csv` |
| **Histórico** | 3003 | una versión cerrada | Yo, al cerrar | `historico.csv` |

Archivadas y ocultas (solo consulta, no escribir): `ARCHIVO · Variaciones` 2002 · `ARCHIVO · Publicaciones` 1002 · `ARCHIVO · Resultados` 2003 · `ARCHIVO · Convenciones` 1003 · `ARCHIVO · README (para Claude)` 1004. Si algo viejo choca con este archivo, manda este archivo.

**Columnas amarillas = de Cris** (yo solo las leo): Guiones: Decisión de Cris, Hooks aprobados, Comentarios de Cris, Fecha de decisión · Producción: Decisión de Cris, Comentarios de Cris, Fecha de decisión · Planner: Qué vimos, Decisión, Próxima variación a probar · Histórico: Aprendizaje (Cris). Única excepción: si Cris aprueba **dentro de la sesión**, escribo por él Estado, Decisión de Cris, Comentarios ("aprobado en la sesión") y Fecha (permiso del 26-oct-2026) y releo la fila.

## Columnas

**Guiones** (A…X): A ID ángulo · B Vertical · C Pilar · D Nivel · E Rol · F Ángulo (la idea) · G Hook 1 · H Tipo H1 · I Hook 2 · J Tipo H2 · K Hook 3 · L Tipo H3 · M Cuerpo del guion (C1) · N CTA (A1) · O Formato / duración · P Otras variantes (C2, A2…) · **Q Estado** (Banco, Borrador, Aprobado, En producción, Cerrado, Descartado) · R Fecha propuesta · *S Decisión de Cris (Aprobado, Con cambios, Rechazado)* · *T Hooks aprobados* · *U Comentarios de Cris* · *V Fecha de decisión* · **W Versiones generadas (IDs)** · X Notas.

**Producción** (A…AD, 30 columnas): A ID único · B Pieza (código) · C Nombre de la pieza · D Versión · E Hook · F Contenido · G CTA · H Eje que cambia · I Basada en (ID) · J Voz / idioma · K Formatos · **L Estado** (Preview, Aprobada, Vigente, Reemplazada, Rechazada, Archivada) · M Preview (dónde verlo) · *N Decisión de Cris · O Comentarios de Cris · P Fecha de decisión* · Q Qué cambió · R Fecha de creación · S Planos usados (ID del Directorio) · **T Usos marcados en el Directorio (fecha)** · U Proyecto Premiere (.prproj) · V Ruta local · W Export en Drive (listo para subir) · X Usado · Y Usado en dónde · Z Fecha de uso (**X, Y, Z en desuso**: el uso real vive en Planner e Histórico) · AA Builder · AB Notas · **AC Vertical · AD Nivel**.

**Planner** (A…AM, 39): A ID publicación · B ID de versión · C Vertical · D Nivel · E Formato · F Plataforma · G Cuenta · H Mercado · I Uso · J Copy o título · K UTM campaign · L UTM content · M Fecha programada · N Estado (Pendiente, Programada, Publicada, En medición, Cerrada, Retirada, Error) · O Fecha publicada · P URL · Q Publicado por · R–W métricas 24 h (Alcance, Vistas, Retención %, Clics, Leads, Costo) · X–AC 48 h · AD–AI 72 h · *AJ Qué vimos · AK Decisión · AL Próxima variación a probar* · AM Notas.

**Histórico** (A…AD, 30): A ID único · B Pieza · C Nombre · D Vertical · E Nivel · F Versión · G Hook · H Contenido · I CTA · J Eje que cambia · K Basada en · L Voz / idioma · M Formatos · N **Estado final** (Reemplazada, Rechazada, Archivada, Cerrada) · O Fecha de creación · P Fecha de cierre · Q Qué cambió · R Planos usados · S Export en Drive · T Publicada en · U–Z métricas a 72 h (Alcance, Vistas, Retención %, Clics, Leads, Costo) · AA Decisión · *AB Aprendizaje (Cris)* · AC Builder · AD Notas.

**Códigos:** Vertical `INT` `LED` `WAN` `POS` · Pilar `P1` Atención y participación en el aula, `P2` Clase sin fricción, `P3` El aula que viene, `P4` Elegir bien · Nivel `N1` Inconsciente, `N2` Consciente del problema, `N3` Consciente de la solución, `N4` Consciente del producto, `N5` Totalmente consciente · ID de ángulo = código de pieza `<VERTICAL>A<NN>` (`INTA03` → versiones `INTA03.0001`…; 2 a 8 caracteres) · Decisión en Planner/Histórico: Escalar, Repetir, Iterar hook, Iterar contenido, Iterar CTA, Pausar, Sin conclusión.

## Flujo

```
GUIONES   estrategia escribe → Cris aprueba el guion
   │      yo copio lo aprobado (SKILL.md §5)
PRODUCCIÓN  Preview → Cris aprueba el video → Aprobada
   │      el planner lee solo Aprobada o Vigente
PLANNER   publica → mide 24/48/72 h → Cris decide a las 72 h
   │      yo muevo lo cerrado (SKILL.md §6)
HISTÓRICO  versión + resultado + decisión → la lee la skill de estrategia
```

Dos aprobaciones de Cris, independientes: la del guion (Guiones) y la del video (Producción). Un guion aprobado **no** habilita publicar nada.

## Reglas que se conservan
- **ID único** `<PIEZA>.<NNNN>`, secuencial por pieza. Un cambio = un ID nuevo. Nunca se reutiliza ni sobrescribe. Todos los formatos comparten ID. **Solo en el nombre del archivo**, nunca impreso en el video.
- **Nombre de archivo:** `<ID>_<H#C#A#>_<voz>_<formato>[_preview].<ext>`. Formatos 16x9 · 9x16 · 4x5 · 1x1. Voz: neutro · ec · mx · co · pt-br · en. Fechas aaaa-mm-dd.
- Una variable a la vez por prueba (`Eje que cambia`). Versión (v1, v2…) = iteración por correcciones de Cris.
- **Previews:** NO van a Drive; por el chat de la sesión y local en `Exports` con `_preview`.
- **Exports aprobados** (sin `_preview`): carpeta de Drive "Producción de video" (`1cda9LOGC2Yb_wli88bNpmJ0BRFqOnmDm`), subcarpeta por pieza; el link va en `Export en Drive (listo para subir)`. Sin link, el planner no publica y avisa.
- **Directorio de planos** (columna A = ID): al pasar a Aprobada, por cada ID de `Planos usados` sumar 1 a Y (# de usos), línea en AQ `<ID de versión> <nombre de la pieza> (video)`, fecha en T de Producción. Si T ya tiene fecha, no se vuelve a sumar; un ID nuevo con los mismos planos tampoco, salvo que Cris lo pida. El escaneo del Directorio recalcula Y desde los .prproj: si se re-escanea, reaplicar los usos desde Producción e Histórico.
- Carpeta local de exports: `D:\OneScreen\Contenido\<año>\<mes>\<Pieza>\Exports\`.
- **Honestidad:** la hoja dice lo que se anotó, no lo que se comprobó. Antes de afirmar que algo está hecho o publicado, decir qué verifiqué y qué no. Nunca `Publicada` sin la URL real.
- **Sincronización:** al empezar cada sesión leo la hoja y actúo sobre las decisiones de Cris. Si hay conflicto manda lo que Cris acaba de decidir; después releo la fila.
- Una sola lista larga con filtros y desplegables; sin pestañas ni columnas nuevas sin pedido de Cris (si hace falta una, al final y documentada aquí). Filas nuevas debajo de la última, copiando formato y listas. Tras cada escritura grande, verificar el número de filas.

## Inconsistencias conocidas (no corregir sin que Cris lo pida)
- Voz de RENT.0007 a 0010 como `ecuador`, `mexico`, `pt-BR` (convención: `ec`, `mx`, `pt-br`); los archivos ya llevan los nombres largos, no renombrar.
- En Producción las fechas de creación de RENT.0001 a RENT.0005 se leen como número de serie (46316, 46318); en Histórico están como 2026-10-21 / 2026-10-23.
- RENT.0001 a RENT.0004: archivos de entrega no localizados el 26-oct-2026 y publicación nunca verificada; Cris decide si se dan por perdidos.
- `Nivel = N3` para RENT es propuesto; Pilar y Rol sin asignar.
- Pendiente: .prproj final y MOV de gráficos de RENT.0006, 0007, 0009 y 0010.
