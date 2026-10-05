export const boutique = {
  phone: '51930527248',
  url: 'https://xilianaboutique.comunidadfortaleza.com',
  provinceShipping: 15,
  address: 'Av. Horacio Urteaga 1438, Tienda 166 · C. C. El Rey · Jesús María, Lima',
  hours: 'Lunes a sábado, 11:00 a. m. a 8:00 p. m. · Domingo cerrado',
};

export const money = value => new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(value);

export function limaNow(now = new Date()) {
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Lima', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
  }).formatToParts(now).map(p => [p.type, p.value]));
  return { date: `${parts.year}-${parts.month}-${parts.day}`, time: `${parts.hour}:${parts.minute}` };
}

export function visitError(date, time, now = new Date()) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time)) return 'Elige una fecha y una hora para tu visita.';
  const day = new Date(`${date}T12:00:00Z`);
  if (Number.isNaN(day.getTime()) || day.toISOString().slice(0, 10) !== date) return 'Elige una fecha válida.';
  if (day.getUTCDay() === 0) return 'Los domingos estamos cerrados. Elige de lunes a sábado.';
  if (time < '11:00' || time >= '20:00') return 'Elige una hora desde las 11:00 a. m. y antes de las 8:00 p. m.';
  const current = limaNow(now);
  if (date < current.date || (date === current.date && time <= current.time)) return 'Elige una fecha y hora futuras (hora de Lima).';
  return '';
}

export function orderTotals(product, quantity, method) {
  const subtotal = Math.round(product.price * quantity * 100) / 100;
  const shipping = method === 'province' ? boutique.provinceShipping : method === 'lima' ? null : 0;
  return { subtotal, shipping, total: shipping === null ? null : subtotal + shipping };
}

export function orderMessage(product, data, path) {
  const totals = orderTotals(product, Number(data.quantity), data.method);
  const lines = [
    `Hola Xiliana Boutique, ${data.method === 'visit' ? 'quisiera ver este vestido en persona' : 'quisiera solicitar este pedido'}.`, '',
    `Vestido: ${product.name}`, `Referencia: XL-${String(product.id).padStart(3, '0')}`,
    `Colección: ${product.category}`, `Enlace: ${boutique.url}${path}`,
    `Precio unitario del catálogo: ${money(product.price)}`, `Cantidad: ${data.quantity}`,
    `Talla solicitada: ${data.size}`, `Subtotal: ${money(totals.subtotal)}`, '',
    `Nombre: ${data.name}`, `Celular: ${data.phone}`,
  ];
  if (data.method === 'visit') {
    lines.push('Modalidad: visita a la boutique', `Fecha solicitada: ${data.date.split('-').reverse().join('/')}`,
      `Hora solicitada: ${data.time} (hora de Lima)`, `Tienda: ${boutique.address}`, 'Por favor, confirmen la visita y la disponibilidad del vestido.');
  } else {
    lines.push(`Modalidad: envío a ${data.method === 'province' ? 'provincia' : 'Lima Metropolitana'}`);
    if (data.method === 'province') lines.push(`Departamento: ${data.department}`, `Provincia: ${data.province}`);
    lines.push(`Distrito: ${data.district}`, `Dirección de entrega: ${data.address}`, `Referencia: ${data.reference || 'No indicada'}`);
    if (data.method === 'province') lines.push(`Envío a provincia: ${money(totals.shipping)}`, `Total de referencia: ${money(totals.total)}`);
    else lines.push('Costo de envío en Lima: por confirmar con la boutique', `Importe de prendas: ${money(totals.subtotal)} + envío por confirmar`);
    lines.push('Por favor, confirmen stock, talla, entrega y forma de pago antes de realizar la compra.');
  }
  if (data.notes) lines.push('', `Comentarios: ${data.notes}`);
  return lines.join('\n');
}
