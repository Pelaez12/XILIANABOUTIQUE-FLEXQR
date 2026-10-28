// Disponibilidad pública, sin precios ni códigos internos.
const endpoint = 'https://stock.comunidadfortaleza.com/public/catalog-availability';
function identity(path) {
  const dress = path.match(/^\/vestidos\/(\d+)-/i);
  if (dress) return `XL-${dress[1].padStart(3,'0')}`;
  const accessory = path.match(/^\/accesorios\/((?:acc-)?\d+)-/i);
  return accessory ? `ACC:${accessory[1].toUpperCase()}` : null;
}
try {
  const response=await fetch(endpoint,{credentials:'omit',cache:'no-store'});
  if(!response.ok) throw new Error('Disponibilidad no disponible');
  const payload=await response.json();
  const states=new Map(payload.products.map(p=>[p.catalog_id,p.status]));
  for(const card of document.querySelectorAll('.product-card')) {
    const link=card.querySelector('a.product-open');
    if(!link) continue;
    const status=states.get(identity(new URL(link.href,location.href).pathname));
    if(status==='archived') {card.dataset.stockArchived='true';card.hidden=true;}
    if(status==='sold_out') {
      const note=document.createElement('span'); note.className='stock-note';note.textContent='Agotado';link.append(note);
    }
  }
  document.dispatchEvent(new Event('stock-availability-updated'));
  const status=states.get(identity(location.pathname));
  const target=document.querySelector('.product-detail .product-availability p');
  if(target && status && status!=='unknown') {
    target.replaceChildren(); const label=document.createElement('strong'); label.textContent='Disponibilidad: '; target.append(label, status==='available'?'disponible en tienda.':status==='sold_out'?'agotado.':'modelo archivado.');
    if(status==='archived') document.querySelectorAll('.product-detail [data-order-id],.product-detail a.accessory-whatsapp').forEach(el=>{el.hidden=true;});
  }
} catch { /* Conserva la indicación existente de consultar con la boutique. */ }
