P="/d/OneScreen/Contenido/2026/10. Octubre/Rental DaaS/Proyecto"
export TMP=D:/hf-render/tmp TEMP=D:/hf-render/tmp
mkdir -p "$P/out_r3"
for f in 16 9 45; do
  cd "$P/v_$f"
  npx hyperframes render -o ../out_r3/raw_${f}.mp4 -q delivery --video-frame-format png --frames-cache-dir D:/hf-render/tmp/rfc${f}_r3 --quiet > ../out_r3/log_$f.txt 2>&1
  MIX="$P/mix_rental3.wav" python -I "C:/Users/Cristian Marin/Desktop/Claudio/videos/onescreen-quizwiz-scrybe/post_rental.py" $f "$P/out_r3/raw_${f}.mp4" "$P/out_r3/rental3_${f}.mp4" >> ../out_r3/log_$f.txt 2>&1
done
echo DONE > "$P/out_r3/alldone.txt"
