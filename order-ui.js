import { products } from './products.js';
import { displayImage, productPath } from './catalog-utils.js';
import { boutique, money, limaNow, visitError, visitDateError, visitDay, visitTime, orderTotals, orderMessage } from './order-data.js';

const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const orderDialog = document.createElement('dialog');
orderDialog.id = 'order-dialog';
orderDialog.className = 'order-dialog';
orderDialog.setAttribute('aria-labelledby', 'order-title');
orderDialog.innerHTML = `
  <button type="button" class="order-close" aria-label="Cerrar formulario">×</button>
  <div class="order-heading"><p class="eyebrow">Xiliana Boutique · Atención personal</p><h2 id="order-title">Tu vestido, a un mensaje.</h2><p>Prendas únicas y personalizadas, sin talla definida por ahora. Solicita tu pedido o una visita para coordinar medidas y detalles.</p></div>
  <form id="order-form">
    <div class="order-layout"><div class="order-fields">
      <fieldset><legend>01 · Tu vestido</legend>
        <label>Vestido<select name="product" required>${[...products].sort((a,b) => a.category.localeCompare(b.category) || a.id-b.id).map(p => `<option value="${p.id}">${escape(p.category)} · ${escape(p.name)}</option>`).join('')}</select></label>
        <div class="order-row"><label>Medidas o asesoría <span class="optional">(opcional)</span><input name="size" maxlength="180" placeholder="Indica tus medidas o pide asesoría" /></label><label>Cantidad<input type="number" name="quantity" min="1" max="10" step="1" value="1" required /></label></div>
      </fieldset>
      <fieldset><legend>02 · ¿Cómo lo quieres?</legend>
        <div class="order-methods"><label><input type="radio" name="method" value="lima" checked /><span>Envío a Lima</span></label><label><input type="radio" name="method" value="province" /><span>Provincia <small>+S/15</small></span></label><label><input type="radio" name="method" value="visit" /><span>Ver en tienda</span></label></div>
        <div data-delivery>
          <div class="order-row" data-province hidden><label>Departamento<input name="department" maxlength="70" autocomplete="address-level1" /></label><label>Provincia<input name="province" maxlength="70" /></label></div>
          <label>Distrito<input name="district" maxlength="70" autocomplete="address-level2" required /></label>
          <label>Dirección de entrega<input name="address" maxlength="180" autocomplete="street-address" placeholder="Calle, número, interior o departamento" required /></label>
          <label>Referencia para llegar <span class="optional">(opcional)</span><input name="reference" maxlength="180" placeholder="Ej. frente al parque, portón negro" /></label>
        </div>
        <div data-visit hidden>
          <p class="order-hours">${escape(boutique.address)}<br /><strong>Lunes a sábado · Apertura: 11:00 a. m.<br />Cierre: 8:00 p. m. · Domingo cerrado</strong></p>
          <div class="visit-date-row"><div class="visit-date-field"><label for="visit-date-display">Fecha de visita</label><button type="button" id="visit-date-display" aria-expanded="false" aria-controls="visit-calendar">Elegir fecha ▦</button><input type="hidden" name="date" />
          <div id="visit-calendar" class="visit-calendar" hidden><div class="calendar-heading"><button type="button" data-calendar-prev aria-label="Mes anterior">‹</button><strong id="calendar-month" aria-live="polite"></strong><button type="button" data-calendar-next aria-label="Mes siguiente">›</button></div><div class="calendar-week" aria-hidden="true"><span>L</span><span>M</span><span>M</span><span>J</span><span>V</span><span>S</span><span>D</span></div><div id="calendar-days" class="calendar-days"></div><p class="order-hint">Domingos cerrado. Las fechas deshabilitadas no se pueden seleccionar.</p></div></div>
          <label>Día<input id="visit-day" value="Se completa al elegir la fecha" readonly /></label>
          <label>Hora de visita<select name="time" aria-label="Hora de visita"><option value="">Elegir hora</option></select></label></div>
          <p id="visit-feedback" class="visit-feedback" role="status" hidden></p><p class="order-hint">Horario de Lima. Elige tu llegada antes del cierre; la boutique confirmará tu visita por WhatsApp.</p>
        </div>
      </fieldset>
      <fieldset><legend>03 · Tus datos</legend><div class="order-row"><label>Nombre y apellido<input name="name" maxlength="100" autocomplete="name" required /></label><label>Celular de contacto<input name="phone" type="tel" inputmode="tel" maxlength="20" autocomplete="tel" pattern="[+0-9 ()-]{9,20}" placeholder="Ej. 987 654 321" required /></label></div><label>Comentarios <span class="optional">(opcional)</span><textarea name="notes" maxlength="600" rows="3" placeholder="Color, personalización o indicaciones para el pedido"></textarea></label></fieldset>
    </div><aside class="order-summary"><img id="order-photo" alt="" /><p class="eyebrow" id="order-category"></p><h3 id="order-product-name"></h3><div id="order-totals" aria-live="polite"></div><p class="order-hint">Precio del catálogo. Medidas, personalización, disponibilidad y pago se coordinan con la boutique.</p><button class="button button-dark" type="submit">Revisar mensaje ↗</button><p class="order-hint">Tus datos se incluirán en el mensaje de WhatsApp que tú enviarás.</p><p id="order-error" role="alert" hidden></p></aside></div>
    <section class="order-preview" hidden aria-labelledby="preview-title"><h3 id="preview-title">Revisa tu solicitud</h3><pre id="order-message"></pre><a id="order-whatsapp" class="button button-dark" target="_blank" rel="noopener noreferrer">Continuar en WhatsApp ↗</a><p class="order-hint">Abre el chat del +51 930 527 248. El mensaje se envía cuando tú lo confirmes en WhatsApp.</p></section>
  </form>`;
document.body.append(orderDialog);
const form = orderDialog.querySelector('form');
const fields = form.elements;
const preview = orderDialog.querySelector('.order-preview');
const error = orderDialog.querySelector('#order-error');
const whatsapp = orderDialog.querySelector('#order-whatsapp');
let previousFocus;
const dateButton = orderDialog.querySelector('#visit-date-display');
const calendar = orderDialog.querySelector('#visit-calendar');
const feedback = orderDialog.querySelector('#visit-feedback');
const dayField = orderDialog.querySelector('#visit-day');
let calendarMonth = limaNow().date.slice(0, 7);
const slots = Array.from({ length: 36 }, (_, index) => {
  const minutes = 11 * 60 + index * 15;
  return `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;
});

function showVisitIssue(message) {
  feedback.textContent = message;
  feedback.hidden = !message;
}
function renderCalendar() {
  const [year, month] = calendarMonth.split('-').map(Number);
  const start = new Date(Date.UTC(year, month - 1, 1, 12));
  const days = new Date(Date.UTC(year, month, 0, 12)).getUTCDate();
  const offset = (start.getUTCDay() + 6) % 7;
  orderDialog.querySelector('#calendar-month').textContent = new Intl.DateTimeFormat('es-PE', { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(start);
  const today = limaNow();
  orderDialog.querySelector('[data-calendar-prev]').disabled = calendarMonth <= today.date.slice(0, 7);
  orderDialog.querySelector('#calendar-days').innerHTML = '<span></span>'.repeat(offset) + Array.from({length:days}, (_, index) => {
    const date = `${calendarMonth}-${String(index + 1).padStart(2, '0')}`;
    const issue = visitDateError(date) || (date === today.date && today.time >= slots.at(-1) ? 'Ya no hay horarios para hoy' : '');
    return `<button type="button" data-visit-date="${date}" ${issue ? 'disabled' : ''} aria-label="${escape(`${visitDay(date)}, ${date.split('-').reverse().join('/')}${issue ? '. ' + issue : ''}`)}" aria-pressed="${fields.date.value === date}">${index+1}</button>`;
  }).join('');
}
function updateVisit() {
  const date = fields.date.value;
  dateButton.textContent = date ? `${date.split('-').reverse().join('/')} ▦` : 'Elegir fecha ▦';
  dayField.value = date ? visitDay(date).replace(/^./, char => char.toUpperCase()) : 'Elige primero la fecha';
  const oldTime = fields.time.value;
  const today = limaNow();
  const validDate = date && !visitDateError(date);
  const available = validDate ? slots.filter(time => date !== today.date || time > today.time) : [];
  fields.time.innerHTML = '<option value="">Elegir hora</option>' + available.map(time => `<option value="${time}">${visitTime(time)}</option>`).join('');
  fields.time.value = available.includes(oldTime) ? oldTime : '';
  fields.time.disabled = method() !== 'visit' || !validDate;
  if (method() === 'visit' && date) {
    showVisitIssue(visitDateError(date) || (available.length ? '' : 'Ya no hay horarios para esta fecha. Elige otro día.'));
  } else showVisitIssue('');
}
dateButton.addEventListener('click', () => {
  calendar.hidden = !calendar.hidden;
  dateButton.setAttribute('aria-expanded', String(!calendar.hidden));
  if (!calendar.hidden) renderCalendar();
});
calendar.addEventListener('click', event => {
  const chosen = event.target.closest('[data-visit-date]');
  if (chosen && !chosen.disabled) {
    const issue = visitDateError(chosen.dataset.visitDate);
    if (issue) { showVisitIssue(issue); return; }
    fields.date.value = chosen.dataset.visitDate;
    fields.time.value = '';
    calendar.hidden = true;
    dateButton.setAttribute('aria-expanded', 'false');
    update();
    fields.time.focus();
    return;
  }
  const step = event.target.closest('[data-calendar-next]') ? 1 : event.target.closest('[data-calendar-prev]') ? -1 : 0;
  if (step) {
    const [year, month] = calendarMonth.split('-').map(Number);
    const target = new Date(Date.UTC(year, month-1+step, 1, 12)).toISOString().slice(0, 7);
    if (target >= limaNow().date.slice(0, 7)) { calendarMonth = target; renderCalendar(); }
  }
});

function currentProduct() { return products.find(p => p.id === Number(fields.product.value)); }
function method() { return fields.method.value; }
function showFields(selector, visible, requiredNames = []) {
  const container = orderDialog.querySelector(selector);
  container.hidden = !visible;
  container.querySelectorAll('input, select').forEach(input => {
    input.disabled = !visible;
    input.required = visible && requiredNames.includes(input.name);
  });
}
function clearPreview() {
  preview.hidden = true;
  whatsapp.removeAttribute('href');
  error.hidden = true;
}
function update() {
  clearPreview();
  const selected = currentProduct();
  const mode = method();
  showFields('[data-delivery]', mode !== 'visit', ['district', 'address']);
  showFields('[data-province]', mode === 'province', ['department', 'province']);
  showFields('[data-visit]', mode === 'visit');
  updateVisit();
  const photo = orderDialog.querySelector('#order-photo');
  const imagePath = displayImage(selected).replace(/^\.\//, '/');
  if (photo.getAttribute('src') !== imagePath) photo.src = imagePath;
  photo.alt = selected.name;
  orderDialog.querySelector('#order-category').textContent = selected.category;
  orderDialog.querySelector('#order-product-name').textContent = selected.name;
  const quantity = Number(fields.quantity.value);
  const validQuantity = Number.isInteger(quantity) && quantity >= 1 && quantity <= 10;
  const totals = orderTotals(selected, validQuantity ? quantity : 1, mode);
  orderDialog.querySelector('#order-totals').innerHTML = `<p><span>Precio por vestido</span><strong>${money(selected.price)}</strong></p><p><span>Prendas (${validQuantity ? quantity : '—'})</span><strong>${money(totals.subtotal)}</strong></p>${mode === 'visit' ? '<p><span>Modalidad</span><strong>Visita en tienda</strong></p>' : `<p><span>Envío ${mode === 'province' ? 'a provincia' : 'a Lima'}</span><strong>${totals.shipping === null ? 'Por confirmar' : money(totals.shipping)}</strong></p><p class="order-total"><span>${totals.total === null ? 'Prendas + envío' : 'Total de referencia'}</span><strong>${totals.total === null ? money(totals.subtotal) + ' + envío' : money(totals.total)}</strong></p>`}`;
}
export function openOrder(id, mode = 'lima') {
  previousFocus = document.activeElement;
  // Move from the product sheet to the order sheet without stacking dialogs.
  const productDialog = document.querySelector('#product-dialog[open]');
  if (productDialog) {
    previousFocus = document.querySelector(`#product-grid [data-id="${Number(id)}"]`) || previousFocus;
    productDialog.close();
  }
  form.reset();
  fields.date.value = '';
  calendar.hidden = true;
  calendarMonth = limaNow().date.slice(0, 7);
  dateButton.setAttribute('aria-expanded', 'false');
  fields.product.value = String(products.some(p => p.id === Number(id)) ? id : products[0].id);
  fields.method.value = mode;
  update();
  if (!orderDialog.open) orderDialog.showModal();
  orderDialog.scrollTop = 0;
}
document.addEventListener('click', event => {
  const trigger = event.target.closest('[data-order-id], [data-order-visit]');
  if (!trigger) return;
  event.preventDefault();
  openOrder(trigger.dataset.orderId, trigger.hasAttribute('data-order-visit') ? 'visit' : 'lima');
});
orderDialog.querySelector('.order-close').addEventListener('click', () => orderDialog.close());
orderDialog.addEventListener('click', event => { if (event.target === orderDialog) orderDialog.close(); });
orderDialog.addEventListener('close', () => { if (previousFocus?.isConnected) previousFocus.focus(); });
form.addEventListener('input', update);
form.addEventListener('submit', event => {
  event.preventDefault();
  if (method() === 'visit') {
    const issue = visitError(fields.date.value, fields.time.value);
    if (issue) { showVisitIssue(issue); dateButton.focus(); return; }
  }
  const data = Object.fromEntries(new FormData(form).entries());
  Object.keys(data).forEach(key => { data[key] = data[key].trim(); });
  if (['name', ...(method() === 'visit' ? [] : ['district', 'address']), ...(method() === 'province' ? ['department', 'province'] : [])].some(key => !data[key])) {
    error.textContent = 'Completa los datos solicitados; los campos no pueden contener solo espacios.'; error.hidden = false; return;
  }
  const phoneDigits = data.phone.replace(/\D/g, '');
  if (phoneDigits.length < 9 || phoneDigits.length > 15) { error.textContent = 'Revisa el número de celular de contacto.'; error.hidden = false; fields.phone.focus(); return; }
  const selected = currentProduct();
  const message = orderMessage(selected, data, productPath(selected));
  orderDialog.querySelector('#order-message').textContent = message;
  whatsapp.href = `https://wa.me/${boutique.phone}?text=${encodeURIComponent(message)}`;
  error.hidden = true; preview.hidden = false;
  preview.scrollIntoView({ behavior: 'smooth', block: 'start' });
  whatsapp.focus({ preventScroll: true });
});
