# Regenera index.html a partir de la lista de escenas (inicio/fin globales).
import re
SC=[("01-apertura",0,15.8),("02-flota-odoo",15.8,42.2),("03-ivan",41.6,80.2),("04-isaac",79.6,127.6),
    ("05-isabel",127.0,159.9),("06-harby",159.3,183.4),("07-marco",182.8,196.1),("08-reglas",196.1,220.7),("09-cierre",220.7,243.72)]
import os
s=open('index.html',encoding='utf-8').read()
rows=''.join(f'      <div id="host-{n}" class="scene-host clip" data-composition-id="{n}" data-composition-src="compositions/frames/{n}.html" data-start="{a}" data-duration="{round(b-a,3)}" data-track-index="1" data-width="1920" data-height="1080"></div>\n' for n,a,b in SC if os.path.exists(f'compositions/frames/{n}.html'))
s=re.sub(r'(      <div id="host-.*\n)+', rows, s)
open('index.html','w',encoding='utf-8').write(s)
print(rows.count('host-'))
