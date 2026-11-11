(() => {
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const toggle = document.getElementById('motionToggle');
  const label = toggle.querySelector('span');
  let paused = preference.matches;

  const updateMotion = () => {
    document.body.dataset.motion = paused ? 'paused' : 'running';
    toggle.setAttribute('aria-pressed', String(paused));
    label.textContent = paused ? 'Reanudar animaciones' : 'Pausar animaciones';
  };
  toggle.hidden = false;
  toggle.addEventListener('click', () => { paused = !paused; updateMotion(); });
  preference.addEventListener('change', (event) => { paused = event.matches; updateMotion(); });
  updateMotion();

  const visuals = document.querySelectorAll('.visual, .option-visual');
  if (!('IntersectionObserver' in window)) {
    visuals.forEach((element) => element.classList.add('is-running'));
    return;
  }
  const animations = new IntersectionObserver((entries) => {
    entries.forEach((entry) => entry.target.classList.toggle('is-running', entry.isIntersecting));
  }, { threshold: 0.08 });
  visuals.forEach((element) => animations.observe(element));

  const reveal = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      reveal.unobserve(entry.target);
    });
  }, { threshold: 0.06 });
  document.querySelectorAll('section > h2, section > .intro, .option, .visual, .table-scroll, .api-grid, .callout, .flow, .decision, details, .sources').forEach((element) => {
    element.classList.add('reveal');
    if (element.classList.contains('option')) {
      element.style.setProperty('--delay', `${Array.from(element.parentNode.children).indexOf(element) * 80}ms`);
    }
    reveal.observe(element);
  });
  document.body.classList.add('motion-ready');
})();
