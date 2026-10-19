export const code = id => typeof id === 'number' ? `XL-${String(id).padStart(3, '0')}` : id;
export function normalize(product) {
  const photos = product.photos?.length ? product.photos : product.image ? [{src:product.image,view:'Frente'}] : [];
  return {id:code(product.id),name:product.name,category:product.category,price:product.price,photos:photos.map(p=>({src:p.src,view:p.view||'Foto'})),missing:!!product.photoPending,notes:'',status:'pending'};
}
export function differences(original, item) {
  if (!original) return ['Prenda nueva'];
  const changes = [];
  if(item.name!==original.name) changes.push(`Nombre: ${original.name} → ${item.name}`);
  if(item.category!==original.category) changes.push(`Categoría: ${original.category} → ${item.category}`);
  if(item.price!==original.price) changes.push(`Precio: S/ ${original.price} → S/ ${item.price}`);
  const removed=original.photos.filter(p=>!item.photos.some(n=>n.src===p.src));
  const added=item.photos.filter(p=>!original.photos.some(n=>n.src===p.src));
  removed.forEach(p=>changes.push(`Quitar foto: ${p.src}`));
  added.forEach(p=>changes.push(`Añadir foto: ${p.filename||p.src} (${p.view})`));
  if(original.photos[0]?.src!==item.photos[0]?.src && item.photos.length) changes.push(`Portada: ${item.photos[0].filename||item.photos[0].src}`);
  if(item.missing!==original.missing) changes.push(item.missing?'Faltan fotos por conseguir':'Fotos completas');
  return changes;
}
export function buildReport(originals, items, date=new Date()) {
  const reviewed=items.filter(p=>p.status!=='pending');
  const lines=['XILIANA BOUTIQUE · REVISIÓN DE COLECCIÓN',date.toLocaleString('es-PE',{timeZone:'America/Lima'}),`Revisadas: ${reviewed.length}/${items.length}. Pendientes: ${items.length-reviewed.length}.`,'Las siguientes son indicaciones del dueño para actualizar el catálogo.'];
  for(const item of reviewed) {
    const original=originals.find(p=>p.id===item.id);
    const changes=differences(original,item);
    const type=item.status==='deleted'?'ELIMINAR':!original?'AGREGAR':changes.length||item.notes?'CORREGIR':'CONFIRMADO';
    lines.push('',`[${type}] ${item.id} · ${item.name}`,`Categoría: ${item.category} · S/ ${item.price}`);
    if(type==='ELIMINAR') lines.push('Solicita retirar esta prenda del catálogo.');
    else if(!original) item.photos.forEach(p=>lines.push(`Foto: ${p.filename||p.src} (${p.view})`));
    else lines.push(...changes);
    if(item.missing) lines.push('PENDIENTE: faltan fotos por conseguir.');
    if(!item.photos.length) lines.push('SIN FOTOS: conseguir imágenes de esta prenda.');
    if(item.notes) lines.push(`Indicaciones: ${item.notes}`);
  }
  const attachments=reviewed.flatMap(p=>p.photos.filter(f=>f.src.startsWith('data:')).map(f=>`${p.id}: ${f.filename}`));
  if(attachments.length) lines.push('','FOTOS SUBIDAS (adjuntar el respaldo JSON en WhatsApp):',...attachments);
  if(!reviewed.length) lines.push('','Aún no hay decisiones registradas.');
  return lines.join('\n');
}
export function splitReport(report,max=2400) {
  const chunks=[];let buffer='';
  for(const line of report.split('\n')) {
    let remaining=line+'\n';
    if(buffer && buffer.length+remaining.length>max){chunks.push(buffer.trimEnd());buffer='';}
    while(remaining.length){
      const capacity=max-buffer.length;
      buffer+=remaining.slice(0,capacity);remaining=remaining.slice(capacity);
      if(buffer.length>=max){chunks.push(buffer.trimEnd());buffer='';}
    }
  }
  if(buffer.trim()) chunks.push(buffer.trimEnd());
  return chunks.map((text,i)=>`Xiliana · Parte ${i+1}/${chunks.length}\n${text}`);
}
export function validPhoto(src) {
  return typeof src==='string' && (/^\.\/images\/[a-zA-Z0-9_./%() áéíóúñÁÉÍÓÚÑ-]+$/u.test(src) && !src.includes('..') || /^data:image\/(jpeg|png|webp);base64,[a-zA-Z0-9+/=]+$/.test(src));
}
export function validateBackup(value,categories,originals) {
  if(value?.format!=='xiliana-review-v1'||!Array.isArray(value.items)||value.items.length>2000) throw Error('Este archivo no es un respaldo de Xiliana.');
  const seen=new Set();
  for(const p of value.items) {
    if(!p||typeof p.id!=='string'||!(/^(XL-\d{3,}|NUEVO-[A-Z0-9-]+)$/.test(p.id))||seen.has(p.id)||!p.name?.trim()||p.name.length>180||!categories.includes(p.category)||!Number.isFinite(p.price)||p.price<0||p.price>100000||!['pending','confirmed','edited','deleted'].includes(p.status)||typeof p.notes!=='string'||p.notes.length>2000||typeof p.missing!=='boolean'||!Array.isArray(p.photos)||p.photos.length>40) throw Error('El respaldo contiene una prenda inválida.');
    if(p.id.startsWith('XL-')&&!originals.some(o=>o.id===p.id)) throw Error(`El código ${p.id} no pertenece al catálogo actual.`);
    for(const f of p.photos) if(!validPhoto(f.src)||typeof f.view!=='string'||f.view.length>100||f.filename!==undefined&&typeof f.filename!=='string') throw Error('El respaldo contiene una foto inválida.');
    seen.add(p.id);
  }
  if(originals.some(p=>!seen.has(p.id))) throw Error('El respaldo está incompleto o pertenece a otra versión del catálogo.');
  return value.items;
}
