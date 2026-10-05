import { products } from './products.js';
import { displayImage, productPath } from './catalog-utils.js';
import { boutique, money, limaNow, visitError, orderTotals, orderMessage } from './order-data.js';

const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const orderDialog = document.createElement('dialog');
orderDialog.id = 'order-dialog';
orderDialog.className = 'order-dialog';
orderDialog.setAttribute('aria-labelledby', 'order-title');
orderDialog.innerHTML = `
  <button type="button" class="order-close" aria-label="Cerrar formulario">×</button>
  <div class="order-heading"><p class="eyebrow">Xiliana Boutique · Atención personal</p><h2 id="order-title">Tu vestido, a un mensaje.</h2><p>Solicita tu pedido o ven a probártelo. La boutique confirmará talla y disponibilidad contigo.</p></div>
  <form id="order-form">
    <div class="order-layout"><div class="order-fields">
      <fieldset><legend>01 · Tu vestido</legend>
        <label>Vestido<select name="product" required>${[...products].sort((a,b) => a.category.localeCompare(b.category) || a.id-b.id).map(p => `<option value="${p.id}">${escape(p.category)} · ${escape(p.name)}</option>`).join('')}</select></label>
        <div class="order-row"><label>Talla que buscas<input name="size" maxlength="35" placeholder="Ej. M, L o necesito asesoría" required /></label><label>Cantidad<input type="number" name="quantity" min="1" max="10" step="1" value="1" required /></label></div>
      </fieldset>
      <fieldset><legend>02 · ¿Cómo lo quieres?</legend>
        <div class="order-methods"><label><input type="radio" name="method" value="lima" checked /><span>Envío a Lima</span></label><label><input type="radio" name="method" value="province" /><span>Provincia <small>+S/15</small></span></label><label><input type="radio" name="method" value="visit" /><span>Ver en tienda</span></label></div>
        <div data-delivery>
          <div class="order-row" data-province hidden><label>Departamento<input name="department" maxlength="70" autocomplete="address-level1" /></label><label>Provincia<input name="province" maxlength="70" /></label></div>
          <label>Distrito<input name="district" maxlength="70" autocomplete="address-level2" required /></label>
          <label>Dirección de entrega<input name="address" maxlength="180" autocomplete="street-address" placeholder="Calle, número, interior o departamento" required /></label>
          <label>Referencia para llegar <span class="optional">(opcional)</span><input name="reference" maxlength="180" placeholder="Ej. frente al parque, portón negro" /></label>
        </div>
        <div data-visit hidden><p class="order-hours">${escape(boutique.address)}<br /><strong>${escape(boutique.hours)}</strong></p><div class="order-row"><label>Fecha de visita<input type="date" name="date" min="${limaNow().date}" /></label><label>Hora de llegada<input type="time" name="time" min="11:00" max="19:59" /></label></div><p class="order-hint">Hora de Lima. Tu visita se confirma por WhatsApp.</p></div>
      </fieldset>
      <fieldset><legend>03 · Tus datos</legend><div class="order-row"><label>Nombre y apellido<input name="name" maxlength="100" autocomplete="name" required /></label><label>Celular de contacto<input name="phone" type="tel" inputmode="tel" maxlength="20" autocomplete="tel" pattern="[+0-9 ()-]{9,20}" placeholder="Ej. 987 654 321" required /></label></div><label>Comentarios <span class="optional">(opcional)</span><textarea name="notes" maxlength="600" rows="3" placeholder="Color, dudas de talla o indicaciones para el pedido"></textarea></label></fieldset>
    </div><aside class="order-summary"><img id="order-photo" alt="" /><p class="eyebrow" id="order-category"></p><h3 id="order-product-name"></h3><div id="order-totals" aria-live="polite"></div><p class="order-hint">Precio del catálogo. Stock, talla y pago se coordinan con la boutique.</p><button class="button button-dark" type="submit">Revisar mensaje ↗</button><p class="order-hint">Tus datos se incluirán en el mensaje de WhatsApp que tú enviarás.</p><p id="order-error" role="alert" hidden></p></aside></div>
    <section class="order-preview" hidden aria-labelledby="preview-title"><h3 id="preview-title">Revisa tu solicitud</h3><pre id="order-message"></pre><a id="order-whatsapp" class="button button-dark" target="_blank" rel="noopener noreferrer">Continuar en WhatsApp ↗</a><p class="order-hint">Abre el chat del +51 930 527 248. El mensaje se envía cuando tú lo confirmes en WhatsApp.</p></section>
  </form>`;
document.body.append(orderDialog);
const form = orderDialog.querySelector('form');
const fields = form.elements;
const preview = orderDialog.querySelector('.order-preview');
const error = orderDialog.querySelector('#order-error');
const whatsapp = orderDialog.querySelector('#order-whatsapp');
let previousFocus;

function currentProduct() { return products.find(p => p.id === Number(fields.product.value)); }
function method() { return fields.method.value; }
function showFields(selector, visible, requiredNames = []) {
  const container = orderDialog.querySelector(selector);
  container.hidden = !visible;
  container.querySelectorAll('input').forEach(input => {
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
  showFields('[data-visit]', mode === 'visit', ['date', 'time']);
  fields.date.min = limaNow().date;
  fields.date.setCustomValidity(''); fields.time.setCustomValidity('');
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
    if (issue) { error.textContent = issue; error.hidden = false; fields.date.focus(); return; }
  }
  const data = Object.fromEntries(new FormData(form).entries());
  Object.keys(data).forEach(key => { data[key] = data[key].trim(); });
  if (['name', 'size', ...(method() === 'visit' ? [] : ['district', 'address']), ...(method() === 'province' ? ['department', 'province'] : [])].some(key => !data[key])) {
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
