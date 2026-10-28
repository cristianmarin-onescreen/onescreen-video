#!/bin/bash
# Render del video corporativo en 16:9, 9:16 y 4:5 + post (aberración leve, intro de marca, audio mezclado). Cachés y TMP en D:.
P="/d/OneScreen/Contenido/2026/10. Octubre/Corporativo salas de reuniones/Proyecto"
export TMP=D:/hf-render/tmp TEMP=D:/hf-render/tmp
mkdir -p "$P/out"
for f in 16 9 45; do
  cd "$P/v_$f"
  npx hyperframes render -o ../out/raw_${f}.mp4 -q delivery --video-frame-format png --frames-cache-dir D:/hf-render/tmp/rfc${f}_corp --quiet > ../out/log_$f.txt 2>&1
  MIX="$P/mix_corp.wav" python -I "C:/Users/Cristian Marin/Desktop/Claudio/videos/onescreen-quizwiz-scrybe/post_rental.py" $f "$P/out/raw_${f}.mp4" "$P/out/corporativo_${f}.mp4" >> ../out/log_$f.txt 2>&1
done
echo DONE > "$P/out/alldone.txt"
