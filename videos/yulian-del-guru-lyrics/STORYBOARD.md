---
compositionId: yulian-del-guru
duration_s: 194.39
canvas: { w: 1920, h: 1080, fps: 30 }
style:
  font: "Inter 800-900 uppercase display / Space Grotesk label chrome"
  palette: ["#000000", "#FFFDF5", "#FE90E8", "#C0F7FE", "#2ad268", "#F7CB46"]
assets: false
build_notes: ["one paused timeline per frame", "no remote assets", "official lyrics from the artist (Yulian del Gurú, a OneScreen support-team jingle) mapped onto real ASR line boundaries; word anchors are evenly interpolated within each line span, not literal ASR word matches", "blockframe brand: 4px black borders, 8px hard offset shadows, square corners, candy pastel fills on black/cream ground", "shout groups (single word, e.g. ¡YULIAN!) should hit HARD: full-frame flash / chromatic-split / scale-punch, riding the hi-hat roll under them"]
avoid: ["generic slideshow", "tiny unreadable hero text", "rounded corners / soft shadows (off-brand for blockframe)", "flat karaoke with no hierarchy \u2014 always give the sung line a big readable treatment"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 22.67s
- span_sec: [0.0, 22.67]
- pacing: beat_cut
- mood: [hype, playful]
- feel: drum-roll build into the first vocal line, then a laugh/instrumental gap

### Groups

- **g1** — free_design
  - span_sec: [0.0, 6.68]
  - free_design: { dominant_system: "title card build on accelerating snare roll", primitives: ["chromatic-split", "hard-cut"], density_topology: "accelerate-into-downbeat" }
  - anchors: [0.766, 2.09, 3.5, 5.0, 6.4]
  - copy: ["YULIAN", "DEL", "GURÚ"]

- **g2** — free_design
  - span_sec: [6.68, 13.72]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [6.68, 7.413, 8.0, 8.587, 8.88, 9.613, 9.907, 10.64, 11.373, 11.667, 11.96, 12.107]
  - copy: ["Llegó", "otro", "caso", "al", "Gurú…", "¿Y", "ahora", "quién", "lo", "va", "a", "solucionar?"]

- **g3** — free_design
  - span_sec: [13.72, 22.67]
  - free_design: { dominant_system: "comic-beat visual gag (laugh reaction), no lyric", primitives: ["hard-cut", "chromatic-split"], density_topology: "single-hit-then-hold" }
  - anchors: []  # worker: ride the beat grid / audiomap onsets in this span
  - copy: ["😂"]

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 21.18s
- span_sec: [22.67, 43.85]
- pacing: beat_cut
- mood: [hype, playful]
- feel: dense verse 1 — Yulian works the guru queue, steady lyric lines back to back

### Groups

- **g1** — free_design
  - span_sec: [22.67, 25.53]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [22.67, 23.079, 23.351, 23.487, 23.623, 23.964, 24.577, 24.917]
  - copy: ["Yulian", "está", "en", "el", "Gurú,", "conectado", "desde", "temprano,"]

- **g2** — free_design
  - span_sec: [25.53, 28.25]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [25.53, 25.669, 26.088, 26.297, 26.925, 27.134, 27.413, 27.692, 27.762, 27.901]
  - copy: ["le", "llegan", "los", "problemas", "uno", "tras", "otro", "a", "la", "mano."]

- **g3** — free_design
  - span_sec: [28.25, 30.87]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [28.25, 28.541, 28.687, 29.487, 29.633, 30.142, 30.288, 30.433]
  - copy: ["Abre", "el", "computador,", "se", "acomoda", "en", "la", "silla,"]

- **g4** — free_design
  - span_sec: [30.87, 33.31]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [30.87, 31.134, 31.464, 31.661, 31.991, 32.057, 32.189, 32.321, 32.651, 32.782]
  - copy: ["mira", "todos", "los", "casos", "y", "se", "le", "borra", "la", "sonrisa."]

- **g5** — free_design
  - span_sec: [33.31, 36.05]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [33.31, 33.87, 34.057, 34.182, 34.805, 34.867, 35.116, 35.24, 35.427, 35.49]
  - copy: ["“¡Yulian,", "hay", "un", "problema!”", "—", "“Sí,", "ya", "voy", "a", "revisar”,"]

- **g6** — free_design
  - span_sec: [36.05, 38.45]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [36.05, 36.366, 36.745, 37.187, 37.25, 37.376, 37.755, 37.818]
  - copy: ["pasan", "veinte", "minutos", "y", "lo", "vuelve", "a", "consultar."]

- **g7** — free_design
  - span_sec: [38.45, 41.01]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [38.45, 38.625, 38.741, 39.032, 39.148, 39.672, 39.846, 39.963, 40.079, 40.428, 40.545]
  - copy: ["Que", "si", "falla", "la", "pantalla,", "que", "si", "no", "prende", "el", "sistema,"]

- **g8** — free_design
  - span_sec: [41.01, 43.85]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [41.01, 41.483, 41.799, 41.957, 42.272, 42.351, 42.509, 43.061, 43.219]
  - copy: ["Yulian", "mira", "el", "caso", "y", "le", "aumenta", "la", "condena."]

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 22.13s
- span_sec: [43.85, 65.98]
- pacing: beat_cut
- mood: [hype, tense]
- feel: chorus 1 — call-and-response hook with syncopated gaps, stress rising

### Groups

- **g1** — free_design
  - span_sec: [43.85, 48.59]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [43.85, 44.887, 45.924, 46.516, 47.109, 47.553, 47.849]
  - copy: ["Yulian,", "Yulian,", "¿qué", "pasó", "con", "el", "Gurú?"]

- **g2** — free_design
  - span_sec: [48.59, 53.74]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [48.59, 49.382, 49.911, 51.099, 51.231, 52.155, 53.344]
  - copy: ["Llegan", "diez", "problemas", "y", "ninguno", "resuelves", "tú."]

- **g3** — free_design
  - span_sec: [53.74, 59.32]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [53.74, 54.889, 56.038, 57.679, 58.828]
  - copy: ["Yulian,", "Yulian,", "tranquilo,", "respira", "ya,"]

- **g4** — free_design
  - span_sec: [59.32, 65.98]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [59.32, 59.875, 60.245, 61.17, 62.28, 62.835, 63.575, 63.945, 64.315, 64.5]
  - copy: ["que", "de", "tanto", "estrés", "ese", "Gurú", "te", "va", "a", "jubilar."]

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 21.28s
- span_sec: [65.98, 87.26]
- pacing: beat_cut
- mood: [playful, tense]
- feel: verse 2 — chat pings, calls, meetings, ticket still open

### Groups

- **g1** — free_design
  - span_sec: [65.98, 68.22]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [65.98, 66.084, 66.501, 66.657, 66.761, 67.022, 67.439, 67.855]
  - copy: ["Le", "escriben", "por", "el", "chat:", "“Yulian,", "necesito", "ayuda”,"]

- **g2** — free_design
  - span_sec: [68.22, 70.36]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [68.22, 68.324, 68.533, 68.638, 69.055, 69.107, 69.577, 69.89, 70.047]
  - copy: ["él", "mira", "la", "pantalla", "y", "responde:", "“Tengo", "una", "duda”."]

- **g3** — free_design
  - span_sec: [70.36, 73.18]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [70.36, 70.692, 70.941, 71.604, 72.185, 72.516]
  - copy: ["Hace", "una", "llamada,", "después", "otra", "reunión,"]

- **g4** — free_design
  - span_sec: [73.18, 76.12]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [73.18, 73.257, 73.412, 74.031, 74.418, 74.727, 75.424]
  - copy: ["y", "el", "problema", "sigue", "vivo", "esperando", "solución."]

- **g5** — free_design
  - span_sec: [76.12, 78.72]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [76.12, 76.387, 76.453, 76.92, 77.053, 77.453, 77.653, 77.987, 78.12]
  - copy: ["“Voy", "a", "escalar", "el", "caso”,", "esa", "frase", "es", "inmortal,"]

- **g6** — free_design
  - span_sec: [78.72, 81.2]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [78.72, 79.092, 79.464, 79.588, 80.146, 80.27, 80.704, 80.828]
  - copy: ["cuando", "Yulian", "la", "pronuncia", "ya", "sabemos", "el", "final."]

- **g7** — free_design
  - span_sec: [81.2, 83.74]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [81.2, 81.334, 81.735, 82.069, 82.604, 82.938, 83.205, 83.406]
  - copy: ["El", "ticket", "sigue", "abierto,", "nadie", "sabe", "qué", "pasó,"]

- **g8** — free_design
  - span_sec: [83.74, 87.26]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [83.74, 84.209, 84.6, 85.383, 85.774, 85.93, 86.556]
  - copy: ["Yulian", "sigue", "estresado…", "¡pero", "el", "problema", "continuó!"]

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 9.6s
- span_sec: [87.26, 96.86]
- pacing: beat_cut
- mood: [tense, hype]
- feel: chorus 2 opening lines, same hook pattern as chorus 1

### Groups

- **g1** — free_design
  - span_sec: [87.26, 91.62]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [87.26, 88.214, 89.168, 89.713, 90.258, 90.666, 90.939]
  - copy: ["Yulian,", "Yulian,", "¿qué", "pasó", "con", "el", "Gurú?"]

- **g2** — free_design
  - span_sec: [91.62, 96.86]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [91.62, 92.426, 92.964, 94.173, 94.307, 95.248, 96.457]
  - copy: ["Llegan", "diez", "problemas", "y", "ninguno", "resuelves", "tú."]

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 27.2s
- span_sec: [96.86, 124.06]
- pacing: beat_cut
- mood: [dark, hype]
- feel: chorus 2 close + spoken bridge/skit riding a long hi-hat roll break — punchy call-and-response

### Groups

- **g1** — free_design
  - span_sec: [96.86, 105.0]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [96.86, 98.536, 100.212, 102.606, 104.282]
  - copy: ["Yulian,", "Yulian,", "tranquilo,", "respira", "ya,"]

- **g2** — free_design
  - span_sec: [105.0, 113.0]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [105.0, 105.667, 106.111, 107.222, 108.556, 109.222, 110.111, 110.556, 111.0, 111.222]
  - copy: ["que", "de", "tanto", "estrés", "ese", "Gurú", "te", "va", "a", "jubilar."]

- **g3** — free_design
  - span_sec: [113.0, 115.5]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [113.0, 114.176, 114.618]
  - copy: ["Pantalla", "sin", "señal…"]

- **g4** — free_design
  - span_sec: [115.5, 116.5]
  - free_design: { dominant_system: "single-word shout hit, full-frame climax", primitives: ["flash-cut", "chromatic-split", "hard-cut"], density_topology: "single-hit-then-hold" }
  - anchors: [115.5]
  - copy: ["¡YULIAN!"]

- **g5** — free_design
  - span_sec: [116.5, 118.5]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [116.5, 117.643]
  - copy: ["Internet", "caído…"]

- **g6** — free_design
  - span_sec: [118.5, 119.5]
  - free_design: { dominant_system: "single-word shout hit, full-frame climax", primitives: ["flash-cut", "chromatic-split", "hard-cut"], density_topology: "single-hit-then-hold" }
  - anchors: [118.5]
  - copy: ["¡YULIAN!"]

- **g7** — free_design
  - span_sec: [119.5, 121.5]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [119.5, 119.682, 120.318, 120.682]
  - copy: ["El", "cliente", "está", "llamando…"]

- **g8** — free_design
  - span_sec: [121.5, 122.3]
  - free_design: { dominant_system: "single-word shout hit, full-frame climax", primitives: ["flash-cut", "chromatic-split", "hard-cut"], density_topology: "single-hit-then-hold" }
  - anchors: [121.5]
  - copy: ["¡YULIAN!"]

- **g9** — free_design
  - span_sec: [122.3, 124.06]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [122.3, 122.355, 122.465, 122.63, 122.85, 123.015, 123.235, 123.455]
  - copy: ["Y", "él", "con", "cara", "de:", "“Eso", "toca", "revisarlo…”"]

## Frame 7 — f7

- src: compositions/frames/07-f7.html
- duration: 23.25s
- span_sec: [124.06, 147.31]
- pacing: beat_cut
- mood: [playful, tense]
- feel: verse 3 — Yulian keeps grinding through the backlog, Friday interrupted

### Groups

- **g1** — free_design
  - span_sec: [124.06, 128.94]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [124.06, 124.504, 125.169, 125.613, 126.722, 127.276, 127.72, 127.942]
  - copy: ["Pero", "aunque", "esté", "estresado,", "nunca", "deja", "de", "intentar,"]

- **g2** — free_design
  - span_sec: [128.94, 131.24]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [128.94, 129.227, 129.515, 129.946, 130.018, 130.162, 130.593, 130.665]
  - copy: ["abre", "otro", "ticket", "y", "lo", "vuelve", "a", "revisar."]

- **g3** — free_design
  - span_sec: [131.24, 133.61]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [131.24, 131.529, 131.876, 132.454, 132.627, 132.743, 133.09, 133.205]
  - copy: ["Tiene", "tantos", "pendientes", "que", "ya", "perdió", "la", "cuenta,"]

- **g4** — free_design
  - span_sec: [133.61, 136.49]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [133.61, 133.891, 134.242, 134.874, 135.296, 135.436, 135.858]
  - copy: ["pero", "sigue", "conectado", "aunque", "la", "cabeza", "revienta."]

- **g5** — free_design
  - span_sec: [136.49, 138.93]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [136.49, 136.547, 136.887, 137.171, 137.284, 137.682, 137.965, 138.192, 138.363]
  - copy: ["Y", "cuando", "llega", "el", "viernes", "dice:", "“Por", "fin", "descansé”,"]

- **g6** — free_design
  - span_sec: [138.93, 141.17]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [138.93, 139.134, 139.388, 139.49, 139.897, 140.355, 140.457, 140.661]
  - copy: ["pero", "suena", "el", "celular:", "“¡Yulian,", "un", "caso", "encontré!”"]

- **g7** — free_design
  - span_sec: [141.17, 144.65]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [141.17, 141.344, 141.779, 142.388, 142.562, 142.997, 143.693, 143.867, 144.128]
  - copy: ["Se", "queda", "mirando", "al", "techo", "pensando", "en", "qué", "hacer,"]

- **g8** — free_design
  - span_sec: [144.65, 147.31]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [144.65, 145.013, 145.134, 145.375, 145.496, 145.98, 146.282, 146.705, 146.826, 147.008]
  - copy: ["porque", "el", "Gurú", "lo", "persigue", "hasta", "después", "de", "las", "seis."]

## Frame 8 — f8

- src: compositions/frames/08-f8.html
- duration: 47.08s
- span_sec: [147.31, 194.39]
- pacing: beat_cut
- mood: [hype]
- feel: final chorus + outro — problems keep coming, big closing chant on 'YULIAAAAN'

### Groups

- **g1** — free_design
  - span_sec: [147.31, 150.42]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [147.31, 148.181, 149.052, 149.425, 149.798]
  - copy: ["Yulian,", "Yulian,", "rey", "del", "Gurú,"]

- **g2** — free_design
  - span_sec: [150.42, 153.7]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [150.42, 150.66, 151.22, 151.38, 152.1, 152.18, 152.34, 152.82, 152.98]
  - copy: ["los", "tickets", "te", "persiguen", "y", "tú", "corres", "en", "círculos."]

- **g3** — free_design
  - span_sec: [153.7, 156.44]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [153.7, 154.281, 154.862, 155.028, 155.195, 155.61, 155.693]
  - copy: ["Yulian,", "Yulian,", "no", "te", "vayas", "a", "estresar,"]

- **g4** — free_design
  - span_sec: [156.44, 161.08]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [156.44, 156.73, 157.31, 157.6, 157.89, 158.76, 159.05, 159.727, 160.017]
  - copy: ["que", "mañana", "hay", "más", "problemas", "que", "tenemos", "que", "solucionar."]

- **g5** — free_design
  - span_sec: [161.08, 165.0]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [161.08, 162.06, 163.628]
  - copy: ["Yeah…", "Respira,", "Yulian…"]

- **g6** — free_design
  - span_sec: [165.0, 168.78]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [165.0, 166.745, 167.326]
  - copy: ["Cierra", "el", "Gurú…"]

- **g7** — free_design
  - span_sec: [168.78, 174.0]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [168.78, 169.747, 170.133, 171.487, 172.067, 173.613]
  - copy: ["¡Pero", "no", "cierres", "los", "tickets!", "😂🔥"]

- **g8** — free_design
  - span_sec: [174.0, 177.96]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [174.0, 174.72, 174.96, 175.32, 175.56, 176.52, 176.76]
  - copy: ["Porque", "si", "hay", "un", "problema", "en", "OneScreen,"]

- **g9** — free_design
  - span_sec: [177.96, 178.78]
  - free_design: { dominant_system: "karaoke word-by-word reveal, one lyric line", primitives: ["typewriter-reveal", "hard-cut"], density_topology: "per-word, character-length-weighted spacing" }
  - anchors: [177.96, 178.021, 178.233, 178.385, 178.446, 178.476]
  - copy: ["ya", "sabemos", "quién", "va", "a", "contestar…"]

- **g10** — free_design
  - span_sec: [178.78, 194.39]
  - free_design: { dominant_system: "single-word shout hit, full-frame climax", primitives: ["flash-cut", "chromatic-split", "hard-cut"], density_topology: "single-hit-then-hold" }
  - anchors: [178.78]
  - copy: ["¡YULIAAAAN!"]
