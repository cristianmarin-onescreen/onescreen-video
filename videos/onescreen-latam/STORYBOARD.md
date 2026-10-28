---
format: 1920x1080
message: "OneScreen transforma espacios — de la educación y las empresas de hoy, a la educación y las empresas del futuro."
arc: Brand manifesto — contraste → revelación → significado → creencia → clímax → marca → CTA
audience: Instituciones educativas, empresas y entidades de gobierno en LATAM evaluando pantallas interactivas
mode: collaborative
music: cinematic emotional brand underscore, slow swelling build to a warm release
---

## Video direction

- **Palette system** (from `frame.md`, Blue Professional remix): warm cream ground (`colors.bg` #FAFAFA) on every frame — no dark backgrounds. Headlines in near-black (`colors.text` #293052), never cobalt. `colors.primary` cobalt (#3976FF) is the single accent — eyebrows, numerals, underline marks, the dot-grid/rings atmosphere, and the one solid CTA element per frame. Body/secondary lines in `colors.text-muted`.
- **The "espacio" motif**: the script's pun (espacio = room AND espacio = cosmos) is carried by the design system's own **atmosphere primitives** — the 3×3 cobalt dot-grid and concentric closing-rings already native to `frame.md` — never by a literal dark/starfield background (that would break the cream-ground rule). Frames 1–2 seed a faint cobalt dot-grid behind the type; it animates (drift → orbit → converge) across Frames 1→3, resolving into the logo reveal. Frames 7–8 reuse concentric rings as the closing atmosphere. Content Frames 4–6 stay in the restrained slide-header/quote register with no atmosphere layer (anti-monotony — atmosphere is scarce, bookends only).
- **Logo asset handling**: `assets/onescreen-logo.png` is the light/white wordmark variant (built for dark surfaces) — on this cream ground it must sit on a small **solid-cobalt rounded pill/card** (reusing the design system's one-permitted-solid-fill, the `cta-button` treatment) so it stays legible. Applies everywhere the wordmark appears (Frames 3, 7, 8).
- **Motion grammar + reveal model**: long-tail `power3` settles by default (no `back.out`/bounce); every frame reveals **paced to the voiceover** — at t=0 only what the VO is saying enters, each further piece (a line, a benefit, a pair) arrives on its spoken cue across the back ~50%. No mid-shot exits — the harness `transition_in` is each frame's exit.
- **Rhythm / held-frame allocation**: Frame 3 (the reveal) and Frame 6 (the climax line) are the deliberate held/breather beats — one fast move, then a still hold, no further development. Frames 4 and 5 carry the most sequential build (the benefit list; the two belief pairs). Frame 7 holds on the brand lockup; Frame 8 ends held on the completed click.
- **Negative list**: no cobalt headlines (cobalt marks/underlines/eyebrows only); no drop shadows on content; no second accent color; no lazy breathing loops; no back-half pan/push; no bouncy/overshoot entrances (the one exception: a single restrained spring-pop settle on the Frame 3 logo landing, still smooth power3-adjacent, not a hard `back.out`). **Revision note**: Frame 2 is a deliberate exception to the cream-ground rule — per direct user feedback it goes literally spacey (deep navy/cobalt gradient + a scattered starfield) to sell "un espacio que no se llena," with `blur-crossfade` in from Frame 1 to mask the light→dark shift; every other frame keeps the cream ground.
- **Logo asset handling (revised)**: `assets/onescreen-logo.png` is recolored solid cobalt via a CSS `mask-image` (masking a `background-color: #3976FF` box with the PNG's shape) rather than seated on a solid-cobalt pill/card — per direct user feedback, no boxed logo chip anywhere in the film; the wordmark itself reads as cobalt type on the cream ground. Applies to Frames 3, 7, and 8's resting mark. Frame 8's CTA *button* (a distinct element from the logo) keeps its own solid-cobalt pill fill — that's a button, not the logo.

## Frame 1 — Espacios que solo ocupan un lugar

- scene: Tipografía sola sobre fondo crema con un tenue dot-grid cobalto detrás; la primera frase aparece, luego un hard-cut da paso a la segunda
- voiceover: "Hay espacios que solo ocupan un lugar. Y hay espacios que cambian lo que pasa dentro de ellos."
- duration: 6.78s
- transition_in: crossfade
- status: animated
- src: compositions/frames/01-espacios-que-ocupan.html
- type: hook
- persuasion: Negative contrast
- beat: intrigue
- blueprint: kinetic-type-beats (Adapt)
- focal: (typography only)
- roles: dot-grid = background atmosphere (native CSS, ~8% opacity)
- asset_candidates:

narrativeRole: Abre con una contradicción filosófica — dos tipos de espacio — sin nombrar aún el producto.
keyMessage: No todos los espacios son iguales; algunos transforman lo que pasa dentro.

Adapt: keep the fixed-center flat-type signature; the "swap mechanism" becomes a hard-cut line replacement (sub-shape A) rather than a token swap, and the atmosphere layer (not in the base blueprint) seeds the espacio/cosmos motif that pays off in Frame 3.

Scene 1 (0.0–3.0s): cream ground; a near-invisible 3×3 cobalt dot-grid (`ambient-glow-bloom`-adjacent, static, ~8% opacity) sits behind a dead-center h1 line. "Hay espacios que solo ocupan un lugar." arrives via **per-word staggered reveal** (`dynamic-content-sequencing`) in near-black, smooth long-tail settle (`power3`). Camera static — Centered, ~45% of frame, dot-grid inert (no motion yet).
Scene 2 (3.0–6.78s): as the VO turns ("Y hay espacios que cambian..."), the line **hard-cuts** (`discrete-text-sequence`) to "Y hay espacios que cambian lo que pasa dentro de ellos." at the same center; simultaneously the dot-grid begins a slow **cluster→outward drift** (`center-outward-expansion`, low amplitude) — dots inch apart, a first sign of life behind the still-static type. Holds to end — Centered, dot-grid now ~15% opacity.

## Frame 2 — Lo que le falta al espacio

- scene: El dot-grid de Frame 1 continúa y ahora orbita lentamente sin resolverse, comunicando "algo falta" antes de que llegue la respuesta
- voiceover: "Hay espacios que no se llenan con cualquier cosa. Y hay espacios a los que solo les falta una cosa."
- duration: 7.895s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/02-lo-que-falta.html
- type: pain_point
- persuasion: Future pacing
- beat: curiosity
- blueprint: kinetic-type-beats (Adapt)
- focal: (typography only)
- roles: dot-grid = background atmosphere, continues from Frame 1 (visual continuity across the crossfade); ground = deep navy/cobalt space gradient + deterministic starfield (revised — see Video direction)
- asset_candidates:

narrativeRole: Sostiene la tensión — un espacio incompleto — preparando la revelación del producto como esa pieza faltante.
keyMessage: A un espacio le puede faltar exactamente una cosa.

Adapt: same fixed-center hard-cut engine as Frame 1; the dot-grid graduates from drift to orbit to hint the payoff is close, then begins to converge — seeding Frame 3's collapse.

Scene 1 (0.0–3.5s): cream ground; the dot-grid now drifts into a slow **orbit** (`orbit-3d-entry`, low amplitude, no entry flip — already in motion) around the empty center. Centered h2 line "Hay espacios que no se llenan con cualquier cosa." reveals via **per-word staggered reveal** (`dynamic-content-sequencing`). Camera static — Centered, ~45% of frame.
Scene 2 (3.5–7.895s): line **hard-cuts** (`discrete-text-sequence`) to "Y hay espacios a los que solo les falta una cosa."; the orbiting dots begin to **converge** toward center (`center-outward-expansion` run inward) — visibly tightening but not yet resolved, foreshadowing Frame 3. Holds on the unresolved tension — Centered, dot orbit radius shrinking through the hold.

## Frame 3 — La revelación

- scene: El dot-grid colapsa hacia el centro y se resuelve en el wordmark de OneScreen sobre una píldora cobalto sólida
- voiceover: "Esa cosa. Es una OneScreen."
- duration: 1.765s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/03-la-revelacion.html
- type: product_intro
- persuasion: Authority by association
- beat: clarity + confidence
- blueprint: logo-assemble-lockup (Adapt)
- focal: assets/onescreen-logo.png
- roles: onescreen-logo.png = cutout, recolored solid cobalt via CSS mask (no pill/box — see Video direction); converging dot-grid = background atmosphere, carried over from Frame 2
- asset_candidates: assets/onescreen-logo.png — wordmark oficial OneScreen, variante blanca

narrativeRole: Resuelve la tensión de los dos frames anteriores nombrando el producto como la pieza que faltaba.
keyMessage: OneScreen es esa cosa que completa el espacio.

Adapt: compress the Product_Intro "brand-reveal-assemble-zoom" shape into 1.765s — no room for its full context-then-focus arc, so it's a fast two-beat punch: the Frame 2 dot-convergence completes here (the shape's "assemble" half), then a same-center scale-swap lands the lockup (the shape's "resolve" half). Keeps the signature move: an assembling system resolving into a fixed centered mark.

Scene 1 (0.0–0.6s): the converging dots from Frame 2 (visual carry-over across the crossfade) snap into a final tight cluster at center as "Esa cosa." **hard-cuts** in (`discrete-text-sequence`) directly above the cluster — Centered, cluster now ~10% of frame.
Scene 2 (0.6–1.765s): the cluster **scale-swaps** (`scale-swap-transition`, shared `transform-origin`) into the solid-cobalt pill carrying the white OneScreen wordmark, landing with one restrained **spring-pop settle** (`spring-pop-entrance`, smooth long-tail, minimal overshoot — the doctrine's rare sanctioned exception); "Es una OneScreen." lands beneath it (`discrete-text-sequence`). Holds — Centered, pill ~35% of frame.

## Frame 4 — Lo que significa

- scene: Tres líneas de beneficio, cada una en su propia tarjeta cobalto-tintada, se apilan una a una en una lista vertical que crece sobre fondo crema (revisado: texto más grande, tarjetas con profundidad, más aire — la versión plana/pequeña/amontonada se corrigió tras feedback)
- voiceover: "Porque para nosotros, transformar un espacio es mucho más que solo tecnología. Es una clase que por fin se entiende. Es un equipo que toma mejores decisiones. Es una idea, que ahora se ve en grande."
- duration: 15.232s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-lo-que-significa.html
- type: benefit_highlight
- persuasion: Feature-to-benefit translation
- beat: aspiration
- blueprint: grid-card-assemble (Adapt — Benefits vertical-list, BUILD sub-mode)
- focal: (typography only)
- roles: (no image assets; pure list-line beats)
- asset_candidates:

narrativeRole: Traduce la promesa abstracta ("transformar un espacio") en tres resultados humanos concretos y reconocibles.
keyMessage: Transformar un espacio es entender mejor, decidir mejor, pensar en grande.

Adapt: keep the BUILD sub-mode signature (each line spring-pop + mask-wipe into a co-resident, accumulating slot); the intro clause gets its own eyebrow beat before the list starts, so the list itself carries exactly the 3 benefit lines (not 4).

Scene 1 (0.0–4.0s): cream ground; a cobalt `h4-eyebrow` reveals via **per-word staggered reveal** (`dynamic-content-sequencing`) as the VO says "Porque para nosotros, transformar un espacio es mucho más que solo tecnología." Camera static; the list region below sits empty, waiting — Left-aligned slide-header rhythm, eyebrow ~20% of frame.
Scene 2 (4.0–8.0s): as the VO says "Es una clase que por fin se entiende," the first benefit line enters the vertical list via **spring-overshoot marker pop + check-draw + pill mask-wipe** (`spring-pop-entrance` + `svg-path-draw` + clip-path reveal), landing in slot 1 — Left-aligned list, ~40% width.
Scene 3 (8.0–11.5s): as the VO says "Es un equipo que toma mejores decisiones," the second line enters the same way into slot 2, co-resident with line 1 (accumulating, not replacing) — list grows to 2 lines.
Scene 4 (11.5–15.232s): as the VO says "Es una idea, que ahora se ve en grande," the third line lands in slot 3. The completed 3-line list holds with a gentle **parallax/sine float** (`sine-wave-loop`, low amplitude, `/√3` per the concurrent-elements rule) — Left-aligned list, 3 lines co-resident, held read at the end.

## Frame 5 — En lo que creemos

- scene: Titular calmo se desliza hacia arriba; dos pares "hoy → futuro" se presentan uno tras otro con un leve cambio de tono cromático
- voiceover: "Creemos en eso. En transformar la educación normal, en educación del futuro. En transformar empresas, en empresas del futuro."
- duration: 12.492s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-en-lo-que-creemos.html
- type: benefit_highlight
- persuasion: Value stacking
- beat: conviction
- blueprint: titlecard-reveal (Adapt — Benefits two-line-crossfade, extended to 2 sequential pairs)
- focal: (typography only)
- roles: (no image assets)
- asset_candidates:

narrativeRole: Eleva de resultados individuales a una creencia de marca — posiciona a OneScreen como una causa, no solo un producto.
keyMessage: OneScreen cree en transformar la educación y las empresas hacia su versión futura.

Adapt: the base blueprint is ONE slide-up crossfade handoff; this beat's VO has two "hoy → futuro" pairs, so the signature move repeats twice (still calm, still ONE move per transition, never a chain of extra swaps).

Scene 1 (0.0–3.0s): cream ground, calm; centered `blockquote`-style line "Creemos en eso." fades in + scales slightly (~95%→100%, `scale-swap-transition`, smooth `power3` settle) — Centered, ~35% of frame.
Scene 2 (3.0–7.5s): as the VO says "En transformar la educación normal, en educación del futuro," the line **slide-up crossfades** (`discrete-text-sequence`) to a paired statement — "la educación normal" in `text-muted`, then "educación del futuro" in near-black with a cobalt underline mark (`css-marker-patterns`) drawing beneath it — one handoff, Centered.
Scene 3 (7.5–12.492s): as the VO says "En transformar empresas, en empresas del futuro," a second **slide-up crossfade** hands off to "empresas" → "empresas del futuro" (same cobalt-underline treatment on the future-state word). Holds to end on this final pair, settled — Centered, calm hold.

## Frame 6 — Cuando un espacio cambia

- scene: Corte seco a tipografía grande y centrada; dos frases cortas caen una tras otra con un peso creciente
- voiceover: "Porque cuando un espacio cambia. El futuro también."
- duration: 4.087s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/06-cuando-un-espacio-cambia.html
- type: branding
- persuasion: Future pacing
- beat: inevitability
- blueprint: kinetic-type-beats (Reproduce — Hook-escalation shape, compressed to 2 beats)
- focal: (typography only)
- roles: (no image assets)
- asset_candidates:

narrativeRole: El clímax emocional del video — conecta el cambio físico del espacio con un cambio de futuro.
keyMessage: Cambiar un espacio es cambiar lo que viene después.

Reproduce: the escalation shape's two-beat climax, landing on a held payoff — kept intact, just two lines instead of three.

Scene 1 (0.0–2.0s): hard cut to cream ground; bold centered h1 "Porque cuando un espacio cambia." **flash-in** (hard-cut, `discrete-text-sequence`, no fade/slide) in near-black — the largest type in the video. Camera static — Centered, ~55% of frame.
Scene 2 (2.0–4.087s): line **hard-cuts** (`discrete-text-sequence`) to "El futuro también." in near-black (headline stays near-black — never cobalt, per the design system), with a cobalt underline mark (`css-marker-patterns`) drawing left→right beneath it as the one accent touch. Settles and **holds** to end — no further motion, the deliberate climax stillness.

## Frame 7 — La marca

- scene: El wordmark de OneScreen se dibuja a sí mismo en el centro del frame sobre anillos concéntricos cobalto; el tagline aparece debajo, palabra por palabra
- voiceover: "OneScreen. Transforma el espacio. Transforma el futuro."
- duration: 3.669s
- transition_in: crossfade
- status: animated
- src: compositions/frames/07-la-marca.html
- type: brand_outro
- persuasion: Authority by association
- beat: pride + confidence
- blueprint: logo-assemble-lockup (Adapt — Brand_Outro shape, compressed)
- focal: assets/onescreen-logo.png
- roles: onescreen-logo.png = cutout, recolored solid cobalt via CSS mask, same treatment as Frame 3 (no pill/box); concentric rings = closing atmosphere (native, per Video direction)
- asset_candidates: assets/onescreen-logo.png — wordmark oficial OneScreen, variante blanca

narrativeRole: Cierra el arco narrativo con la marca y su tagline como resumen de todo lo dicho antes.
keyMessage: OneScreen = transformar el espacio, transformar el futuro.

Adapt: keep the Brand_Outro signature (a formerly-clear stage; the mark draws itself on and the wordmark completes the lockup) but compressed to 3.7s and opened directly on the atmosphere instead of a preceding element-clear (there's nothing on stage to clear coming out of Frame 6's typographic hold).

Scene 1 (0.0–1.2s): cream ground; faint cobalt **concentric rings** fade in behind center (`ambient-glow-bloom`); the OneScreen wordmark pill **draws itself on** stroke-by-stroke (`svg-path-draw`) at center as "OneScreen." lands (`discrete-text-sequence`) — Centered, one atmosphere layer.
Scene 2 (1.2–3.669s): as the VO delivers the tagline, "Transforma el espacio." reveals beneath the mark via **per-word staggered reveal** (`dynamic-content-sequencing`), then **hard-cuts** (`discrete-text-sequence`) to "Transforma el futuro." which lands and **holds** to end — Centered, rings continue at low, unchanging opacity (no further motion beyond the sanctioned subtle jitter).

## Frame 8 — Toca la pantalla

- scene: El wordmark se condensa hacia un único punto de contacto con un cursor táctil que "toca" el frame, revelando el CTA final
- voiceover: "Tu transformación puede comenzar ya, solo tienes que tocar la pantalla."
- duration: 5.155s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/08-toca-la-pantalla.html
- type: cta
- persuasion: Risk reversal
- beat: motivation
- blueprint: cta-morph-press (Reproduce)
- focal: assets/onescreen-logo.png
- roles: onescreen-logo.png = the resting hero mark (recolored solid cobalt via CSS mask, no pill/box) that morphs into the CTA pill (the CTA button itself keeps its own solid-cobalt fill — that's a button, not the logo); concentric rings continue from Frame 7 = background atmosphere
- asset_candidates: assets/onescreen-logo.png — wordmark oficial OneScreen, variante blanca

narrativeRole: Convierte la emoción del manifiesto en una acción física de un solo paso, coherente con el producto (pantalla táctil).
keyMessage: El siguiente paso es literalmente tocar la pantalla.

Reproduce: the full four-scene shape maps cleanly — the resting mark IS Frame 7's lockup carried over; the click payoff literalizes "tocar la pantalla" (touch the screen), which is the beat's whole point.

Scene 1 (0.0–1.4s): the Frame 7 lockup holds dead-center, alive but resting — only a faint rotational breath (`sine-wave-loop`, low amplitude, logo-scope only); concentric rings continue behind at unchanged opacity — Centered, presence beat.
Scene 2 (1.4–2.6s): as the VO reaches "comenzar ya," the mark **condenses** at the same center into the solid-cobalt `cta-button` pill reading "Toca para empezar" (`scale-swap-transition`, shared `transform-origin`) — Centered morph, the signature move.
Scene 3 (2.6–3.8s): as the VO says "solo tienes que," a touch-cursor glyph arrives from off-stage on a **decelerating path** (`gsap-effects`, `power2.out`), landing a few px off the CTA's geometric center so the aim reads human — Centered, cursor approach.
Scene 4 (3.8–5.155s): as the VO lands on "tocar la pantalla," the cursor presses the CTA — **lockstep compression + release ripple** (`physics-press-reaction` + `cursor-click-ripple`) — holds on the clicked/lit state to the end — Centered, final held click.
