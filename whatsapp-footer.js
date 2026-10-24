// Conserva el botón de opiniones y evita que su aviso cubra el contacto.
(() => {
const contact = document.querySelector('[data-eia-whatsapp="footer"]');
const hints = document.querySelectorAll('#floating-copilot .copilot-label, .ai-widget-tooltip');
if (contact && hints.length && 'IntersectionObserver' in window) {
  const original = new Map([...hints].map(hint => [hint, [hint.style.getPropertyValue('display'), hint.style.getPropertyPriority('display')]]));
  new IntersectionObserver(([entry]) => {
    for (const hint of hints) {
      const [value, priority] = original.get(hint);
      hint.style.setProperty('display', entry.isIntersecting ? 'none' : value, entry.isIntersecting ? 'important' : priority);
    }
  }).observe(contact);
}
})();
