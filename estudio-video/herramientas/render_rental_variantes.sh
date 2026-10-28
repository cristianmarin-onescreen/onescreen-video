#!/bin/bash
# Rental DaaS v3-color: construye y renderiza una variante de voz en los formatos pedidos.
# Uso: render_rental_variantes.sh ID ACC SCRIBE.json VOZ.wav "16 9 45"
#   ID = RENT.0007 ; ACC = ec|mx ; el neutro (RENT.0006) usa los v_<fmt> tal cual (ACC=neutro, SCRIBE y VOZ ignorados)
# Deja los MP4 en ...\Rental DaaS\Exports\<ID>_H1C1A1_<voz>_<formato>_preview.mp4 (nombre canónico de registro.py)
ID=$1; ACC=$2; SCRIBE=$3; VOZ=$4; FMTS=${5:-"16 9 45"}
BUILDER=${BUILDER:-build_rental3.py}     # pt-BR: BUILDER=build_rental3_pt.py INTRO_TPL=".../intro_pt_@F@.mp4" INTRO_AUD=.../intro_aud_pt.wav
ROOT="C:/Users/Cristian Marin/Desktop/Claudio"
P="/d/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto"
EXP="/d/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Exports"
SC="$ROOT/videos/onescreen-quizwiz-scrybe"
export TMP=D:/hf-render/tmp TEMP=D:/hf-render/tmp
mkdir -p "$P/out_$ID" "$TMP"
if [ "$ACC" != "neutro" ]; then
  for f in $FMTS; do
    rm -rf "$P/v_${f}_$ACC"; cp -r "$P/v_$f" "$P/v_${f}_$ACC"; rm -rf "$P/v_${f}_$ACC/media_neutro"
    (cd "$SC" && FMT=$f PROJ="D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_${f}_$ACC" SCRIBE="$SCRIBE" python $BUILDER) || exit 1
  done
  f1=$(echo $FMTS | cut -d' ' -f1)
  PLAN_JSON="D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/v_${f1}_$ACC/plan.json" python -I "$SC/mix_rental.py" "D:/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto/mix_$ID.wav" "$VOZ" || exit 1
  MIX="$P/mix_$ID.wav"
else
  MIX="$P/mix_rental3.wav"
fi
for f in $FMTS; do
  if [ "$ACC" = "neutro" ]; then D="$P/v_$f"; else D="$P/v_${f}_$ACC"; fi
  (cd "$D" && npx hyperframes render -o "$P/out_$ID/raw_$f.mp4" -q delivery --video-frame-format png --frames-cache-dir D:/hf-render/tmp/rfc${f}_$ID --quiet > "$P/out_$ID/log_$f.txt" 2>&1)
  if [ -n "$INTRO_TPL" ]; then export INTRO="${INTRO_TPL//@F@/$f}"; fi
  MIX="$MIX" python -I "$SC/post_rental.py" $f "$P/out_$ID/raw_$f.mp4" "$P/out_$ID/final_$f.mp4" >> "$P/out_$ID/log_$f.txt" 2>&1
  case $f in 16) F=16x9;; 9) F=9x16;; 45) F=4x5;; esac
  N=$(cd "$ROOT" && python estudio-video/herramientas/registro.py nombre $ID --formato $F | tail -1)
  cp "$P/out_$ID/final_$f.mp4" "$EXP/$N"
  echo "listo $N" >> "$P/out_$ID/alldone.txt"
done
echo DONE >> "$P/out_$ID/alldone.txt"
