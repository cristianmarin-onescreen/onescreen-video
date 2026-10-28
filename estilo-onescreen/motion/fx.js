/* Flota de IA — ayudantes de movimiento compartidos.
   Todo es determinista: tweens en el timeline pausado de cada escena, sin relojes ni azar. */
(function () {
  var FX = {};

  // El render captura cada cuadro apenas se posiciona el timeline: nada puede quedar
  // pendiente de un "lazy render" de GSAP para el siguiente tick.
  gsap.defaults({ lazy: false });

  // Aparición/desaparición instantánea y segura al buscar hacia atrás o adelante.
  FX.show = function (tl, target, at) {
    tl.fromTo(target, { opacity: 0 }, { opacity: 1, duration: 0.01, ease: "none" }, at);
  };

  // Normaliza trazos: pathLength=1 permite dibujar cualquier forma con dashoffset 1 → 0
  // sin medir geometría en tiempo de render.
  FX.prep = function (root) {
    root.querySelectorAll("[data-draw]").forEach(function (el) {
      el.setAttribute("pathLength", "1");
    });
  };

  // Dibuja los trazos de un selector (ícono completo o partes).
  FX.draw = function (tl, target, at, dur, stagger) {
    tl.fromTo(
      target,
      { strokeDashoffset: 1 },
      { strokeDashoffset: 0, duration: dur || 0.9, ease: "power2.inOut", stagger: stagger || 0.08 },
      at
    );
  };

  // Entrada estándar: sube y aparece.
  FX.up = function (tl, target, at, opts) {
    opts = opts || {};
    tl.fromTo(
      target,
      { opacity: 0, y: opts.y == null ? 40 : opts.y, x: opts.x || 0, scale: opts.s || 1 },
      { opacity: 1, y: 0, x: 0, scale: 1, duration: opts.d || 0.6, ease: opts.ease || "power3.out", stagger: opts.stagger || 0 },
      at
    );
  };

  // Entrada con rebote contenido (íconos, sellos, nodos).
  FX.pop = function (tl, target, at, opts) {
    opts = opts || {};
    tl.fromTo(
      target,
      { opacity: 0, scale: opts.from || 0.6 },
      { opacity: 1, scale: 1, duration: opts.d || 0.55, ease: "back.out(1.7)", stagger: opts.stagger || 0 },
      at
    );
  };

  // Máscara: el texto sube desde detrás de su línea (el padre debe tener overflow:hidden).
  FX.rise = function (tl, target, at, opts) {
    opts = opts || {};
    tl.fromTo(
      target,
      { yPercent: 110, opacity: 0 },
      { yPercent: 0, opacity: 1, duration: opts.d || 0.7, ease: "power4.out", stagger: opts.stagger || 0.06 },
      at
    );
  };

  // Salida: se desvanece hacia un lado.
  FX.out = function (tl, target, at, opts) {
    opts = opts || {};
    tl.to(
      target,
      { opacity: 0, x: opts.x || 0, y: opts.y || 0, scale: opts.s || 1, duration: opts.d || 0.4, ease: "power2.in", stagger: opts.stagger || 0 },
      at
    );
  };

  // Barrido de color de sección: el fondo entra de izquierda a derecha.
  FX.wipe = function (tl, target, at, dur) {
    tl.fromTo(
      target,
      { clipPath: "inset(0% 100% 0% 0%)" },
      { clipPath: "inset(0% 0% 0% 0%)", duration: dur || 0.6, ease: "power3.inOut" },
      at
    );
  };

  // Un paquete de luz recorre una línea recta repetidamente (cuenta finita).
  FX.packet = function (tl, target, at, until, from, to, cycle) {
    cycle = cycle || 1.2;
    var n = Math.max(1, Math.floor((until - at) / cycle));
    tl.fromTo(target, { x: from[0], y: from[1] }, { x: to[0], y: to[1], duration: cycle, ease: "none", repeat: n - 1 }, at);
    FX.show(tl, target, at);
    tl.to(target, { opacity: 0, duration: 0.15 }, at + n * cycle);
  };

  window.FX = FX;
})();
