import { products } from './products.js';
import { displayImage, productPath, sizeLabel } from './catalog-utils.js';
import { boutique, money } from './order-data.js';
const intents={availability:['¿Está disponible?','Quisiera confirmar si este vestido está disponible.'],fit:['Asesoría de medidas','Quisiera asesoría para saber si este vestido se ajusta a mis medidas.'],visit:['Verlo en tienda','Quisiera ver este vestido en la boutique. ¿Podrían confirmar disponibilidad para una visita?'],lima:['Envío a Lima','Me interesa este vestido con envío a Lima. Quisiera confirmar disponibilidad y costo de envío.'],province:['Envío a provincia','Me interesa este vestido con envío a provincia. Quisiera confirmar disponibilidad, costo y plazo de entrega.']};
const dialog=document.createElement('dialog');
dialog.id='order-dialog';dialog.className='order-dialog quick-consult';dialog.setAttribute('aria-labelledby','order-title');
dialog.innerHTML=`<button type="button" class="order-close" aria-label="Cerrar consulta">×</button><header class="order-heading"><p class="eyebrow">Xiliana Boutique · Te asesoramos</p><h2 id="order-title">¿Te enamoró este vestido?</h2><p>Elige qué necesitas y te preparamos el mensaje. Puedes conversar con nosotras sin completar tus datos.</p></header><div class="consult-product"><img id="order-photo" alt=""/><div><p id="order-category" class="eyebrow"></p><h3 id="order-product-name"></h3><p class="consult-size">${sizeLabel}</p><strong id="consult-price"></strong><p class="order-hint">Disponibilidad y medidas por confirmar con la boutique.</p></div></div><form id="order-form"><fieldset><legend>¿Cómo te ayudamos?</legend><div class="consult-options">${Object.entries(intents).map(([key,[label]])=>`<label><input type="radio" name="intent" value="${key}" ${key==='availability'?'checked':''}/><span>${label}</span></label>`).join('')}</div></fieldset><div data-consult-city hidden><label>¿En qué distrito o ciudad estás? <span class="optional">(opcional)</span><input name="city" maxlength="100" autocomplete="address-level2" placeholder="Ej. Miraflores o Arequipa"/></label></div><div data-consult-visit hidden><p>${boutique.address}</p><p>${boutique.hours}</p><p class="order-hint">Consulta si el vestido está en tienda antes de ir. Coordinamos el día y la hora por WhatsApp.</p></div><p data-consult-fit hidden class="order-hint">Te ayudamos con las medidas y posibles ajustes. Puedes enviarlas directamente en el chat.</p><details class="consult-extra"><summary>Añadir una pregunta <span class="optional">(opcional)</span></summary><label>Tu pregunta<textarea name="notes" rows="2" maxlength="400" placeholder="Cuéntanos qué te gustaría saber"></textarea></label></details><details class="consult-message"><summary>Ver el mensaje preparado</summary><pre id="order-message" aria-live="polite"></pre></details><div class="consult-actions"><a id="order-whatsapp" class="button button-dark" target="_blank" rel="noopener noreferrer">Consultar por WhatsApp ↗</a><p class="order-hint">Se abrirá el chat del 930 527 248. Tú decides cuándo enviar el mensaje.</p></div></form>`;
document.body.append(dialog);
dialog.querySelector('[data-consult-visit]').insertAdjacentHTML('beforeend','<label>Día y horario que prefieres <span class="optional">(opcional)</span><input name="visitPreference" maxlength="120" placeholder="Ej. martes por la tarde"/></label>');
dialog.querySelector('[data-consult-city]').insertAdjacentHTML('beforeend',`<p data-province-price class="order-hint" hidden>Envío a provincia: ${money(boutique.provinceShipping)} de referencia. Confirma el plazo y el importe final con la boutique.</p>`);
const measurements=[
 ['bust','Busto','La parte más amplia del pecho.'],
 ['waist','Cintura','La parte más estrecha del torso.'],
 ['hips','Cadera','La parte más amplia de la cadera.']
];
// Estructura de la referencia visual; añadir centímetros solo tras confirmarlos con la boutique.
const sizeGuide={
 sizes:['Estándar'],
 rows:[
  {label:'Contorno de pecho',values:[null]},
  {label:'Contorno de cintura',values:[null]},
  {label:'Contorno de cadera',values:[null]}
 ]
};
dialog.querySelector('.consult-extra').insertAdjacentHTML('beforebegin',`
 <section class="consult-sizing" hidden>
  <h3 class="size-guide-title">Guía de tallas <span>(cm)</span></h3>
  <div class="size-chart-scroll" role="region" aria-label="Tabla de tallas, desliza para ver todas las columnas" tabindex="0">
   <table class="size-chart" aria-describedby="size-chart-note">
    <caption class="sr-only">Referencia de tallas. Medidas pendientes de confirmar.</caption>
    <thead><tr><th scope="col">Talla</th>${sizeGuide.sizes.map(size=>`<th scope="col">${size}</th>`).join('')}</tr></thead>
    <tbody>${sizeGuide.rows.map(row=>`<tr><th scope="row">${row.label}</th>${row.values.map(value=>`<td>${value===null?'<span aria-label="Por confirmar">—</span>':value}</td>`).join('')}</tr>`).join('')}</tbody>
   </table>
  </div>
  <p id="size-chart-note" class="order-hint">Medidas por confirmar con la boutique. Consulta la talla y los ajustes de tu vestido antes de comprar.</p>
  <details class="sizing-personal"><summary>Cómo tomar o compartir mis medidas</summary>
  <fieldset><legend>Sobre tus medidas</legend>
   <div class="sizing-options">
    <label><input type="radio" name="sizing" value="help" checked/><span>Necesito ayuda</span></label>
    <label><input type="radio" name="sizing" value="known"/><span>Ya tengo mis medidas</span></label>
   </div>
  </fieldset>
  <p id="sizing-instructions" class="sizing-instructions">Rodea cada zona con una cinta flexible, horizontal y sin apretar.</p>
  <table class="measurements-table" aria-describedby="sizing-instructions sizing-note">
   <caption class="sr-only">Cómo tomar tus medidas en centímetros</caption>
   <thead><tr><th scope="col">Zona</th><th scope="col">Dónde medir</th><th scope="col" class="measurement-value" data-known-sizing hidden>Tus cm</th></tr></thead>
   <tbody>${measurements.map(([key,label,instruction])=>`<tr><th scope="row">${label}</th><td>${instruction}</td><td class="measurement-value" data-known-sizing hidden><label class="sr-only" for="measure-${key}">${label} en centímetros</label><input id="measure-${key}" name="${key}" type="text" inputmode="decimal" maxlength="6" placeholder="cm"/></td></tr>`).join('')}</tbody>
  </table>
  <div class="sizing-reference" data-known-sizing hidden><label>Talla habitual <span class="optional">(opcional)</span><input name="usualSize" maxlength="40" placeholder="Ej. M o 38"/></label><p class="order-hint">Completa solo lo que sepas. También puedes compartirlo en el chat.</p></div>
  <p id="sizing-note" class="order-hint">Las medidas y los ajustes de cada vestido se confirman con la boutique.</p>
  </details>
 </section>
 <div data-general-consult hidden><label>Ocasión y fecha o visita que tienes en mente <span class="optional">(opcional)</span><input name="occasion" maxlength="180" placeholder="Ej. matrimonio en noviembre; quisiera una cita el martes"/></label><p class="order-hint">Consulta por asesoramiento de imagen o un diseño personalizado. La boutique confirmará el servicio y la cita; esta consulta no reserva un horario.</p></div>`);
const form=dialog.querySelector('form');let selected=products[0];let previousFocus;
function update(){
 const intent=form.elements.intent.value,city=form.elements.city.value.trim(),notes=form.elements.notes.value.trim();
 dialog.querySelector('[data-consult-city]').hidden=!['lima','province'].includes(intent);
 dialog.querySelector('[data-province-price]').hidden=intent!=='province';
 dialog.querySelector('[data-consult-visit]').hidden=intent!=='visit';dialog.querySelector('[data-consult-fit]').hidden=intent!=='fit';
 const sizingVisible=!!selected&&['fit','lima','province'].includes(intent);
 dialog.querySelector('.consult-sizing').hidden=!sizingVisible;
 dialog.querySelectorAll('[data-known-sizing]').forEach(el=>el.hidden=form.elements.sizing.value!=='known');
 dialog.querySelector('[data-consult-fit]').hidden=!selected||intent!=='fit';
 const lines=['Hola Xiliana Boutique 💛',selected?intents[intent][1]:intent==='visit'?'Quisiera coordinar una cita de asesoría en la boutique.':'Quisiera asesoramiento de imagen para elegir mi vestido, combinar accesorios y consultar opciones de diseño personalizado.'];
 if(selected)lines.push('',`Vestido: ${selected.name}`,`Referencia: XL-${String(selected.id).padStart(3,'0')}`,`Precio del catálogo: ${money(selected.price)}`,`Talla: estándar`,`Enlace: ${boutique.url}${productPath(selected)}`);
 if(sizingVisible){
  const known=measurements.flatMap(([key,label])=>{const value=form.elements[key].value.trim();return value?[`${label}: ${value} cm`]:[];});
  const usualSize=form.elements.usualSize.value.trim();
  if(usualSize)known.unshift(`Talla habitual: ${usualSize}`);
  lines.push(form.elements.sizing.value==='help'?'Medidas: necesito ayuda para medirme.':known.length?`Mis referencias: ${known.join('; ')}.`:'Medidas: las compartiré en el chat.','Quisiera confirmar las medidas y posibles ajustes antes de comprar.');
 }
 if(!selected&&form.elements.occasion.value.trim())lines.push(`Mi ocasión o visita: ${form.elements.occasion.value.trim()}`);
 if(intent==='visit'&&form.elements.visitPreference.value.trim())lines.push(`Día y horario preferido: ${form.elements.visitPreference.value.trim()}`,'Por favor, confirmen la cita antes de mi visita.');
 if(intent==='province')lines.push(`Envío a provincia de referencia: ${money(boutique.provinceShipping)}. Por favor, confirmen el importe final.`);
 if(city&&['lima','province'].includes(intent))lines.push(`Mi distrito o ciudad: ${city}`);
 if(notes)lines.push('',`Mi pregunta: ${notes}`);
 const message=lines.join('\n');dialog.querySelector('#order-message').textContent=message;dialog.querySelector('#order-whatsapp').href=`https://wa.me/${boutique.phone}?text=${encodeURIComponent(message)}`;
}
export function openOrder(id,mode='availability'){
 previousFocus=document.activeElement;document.querySelector('#product-dialog[open]')?.close();selected=products.find(p=>p.id===Number(id))||null;form.reset();form.elements.intent.value=Object.hasOwn(intents,mode)?mode:'availability';if(!selected&&mode!=='visit')form.elements.intent.value='fit';dialog.querySelectorAll('details').forEach(el=>el.open=false);
 dialog.querySelector('.consult-product').hidden=!selected;dialog.querySelector('[data-general-consult]').hidden=!!selected;
 dialog.querySelector('#order-title').textContent=selected?'¿Te enamoró este vestido?':'Encuentra tu próximo look.';
 for(const input of form.querySelectorAll('[name="intent"]'))input.closest('label').hidden=!selected&&!['fit','visit'].includes(input.value);
 form.querySelector('[name="intent"][value="fit"]').nextElementSibling.textContent=selected?'Asesoría de medidas':'Elegir mi vestido';
 form.querySelector('[name="intent"][value="visit"]').nextElementSibling.textContent=selected?'Verlo en tienda':'Coordinar una cita';
 if(selected){
 const photo=dialog.querySelector('#order-photo');photo.src=displayImage(selected).replace(/^\.\//,'/');photo.alt=selected.name;
 dialog.querySelector('#order-category').textContent=selected.category;dialog.querySelector('#order-product-name').textContent=selected.name;dialog.querySelector('#consult-price').textContent=money(selected.price);}
 update();if(!dialog.open)dialog.showModal();dialog.scrollTop=0;
}
document.addEventListener('click',event=>{const trigger=event.target.closest('[data-order-id], [data-order-visit], [data-advice]');if(!trigger)return;event.preventDefault();openOrder(trigger.dataset.orderId,trigger.hasAttribute('data-order-visit')?'visit':trigger.hasAttribute('data-advice')?'fit':'availability');});
dialog.querySelector('.order-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});
dialog.addEventListener('close',()=>{if(previousFocus?.isConnected)previousFocus.focus();});
form.addEventListener('input',update);form.addEventListener('change',update);form.addEventListener('submit',event=>event.preventDefault());
