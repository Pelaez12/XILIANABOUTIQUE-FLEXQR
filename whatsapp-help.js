const widget = document.querySelector('.whatsapp-widget');
if (widget) {
  const trigger = widget.querySelector('.whatsapp-help');
  const panel = widget.querySelector('.whatsapp-panel');
  const message = widget.querySelector('textarea');
  const dress = document.querySelector('.product-detail h1')?.textContent.trim();
  const collection = document.querySelector('.collection-heading h1')?.textContent.trim();
  if (dress) message.value = `Hola Xiliana Boutique, me gustó el ${dress}. ¿Me ayudan con las medidas y la disponibilidad?`;
  else if (collection) message.value = `Hola Xiliana Boutique, estoy viendo la colección ${collection}. ¿Me ayudan a elegir un vestido?`;

  function closeHelp() {
    panel.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    trigger.focus();
  }
  trigger.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (!panel.hidden) { closeHelp(); return; }
    panel.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    message.focus();
  });
  widget.querySelector('.whatsapp-close').addEventListener('click', closeHelp);
  widget.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !panel.hidden) { event.preventDefault(); closeHelp(); }
  });
  widget.querySelector('form').addEventListener('submit', event => {
    message.value = message.value.trim();
    if (!message.value) { event.preventDefault(); message.reportValidity(); }
  });
}
