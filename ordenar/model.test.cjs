const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const {pathToFileURL}=require('node:url');
const model=import(pathToFileURL(path.join(__dirname,'model.js')).href);
const catalog={};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../products.js'),'utf8').replaceAll('export const','var'),catalog);
test('El catálogo completo pasa la validación del respaldo y mantiene los códigos originales',async()=>{
  const m=await model;const originals=Array.from(catalog.products,p=>m.normalize(p));
  assert.equal(m.validateBackup({format:'xiliana-review-v1',items:originals},Array.from(catalog.categories),originals).length,catalog.products.length);
  assert.equal(originals[0].id,'XL-059');
  for(const p of originals)for(const photo of p.photos)assert(fs.existsSync(path.resolve(__dirname,'..',photo.src)),photo.src);
});
test('El informe distingue confirmaciones, cambios, eliminaciones, altas y fotos por conseguir',async()=>{
  const m=await model;const originals=Array.from(catalog.products.slice(0,4),p=>m.normalize(p));
  const items=structuredClone(originals);items[0].status='confirmed';items[1]={...items[1],status:'edited',category:'Bandage',price:500,notes:'Usar foto de frente',photos:[{src:'./images/otra.jpeg',view:'Frente'}]};items[2].status='deleted';
  items.push({id:'NUEVO-ABC123',name:'Vestido rojo nuevo',price:123,category:'Gala',photos:[{src:'data:image/png;base64,AAAA',filename:'NUEVO-ABC123-frente.png',view:'Frente'}],status:'edited',missing:true,notes:''});
  const report=m.buildReport(originals,items,new Date('2026-10-19T12:00:00Z'));
  for(const fragment of ['[CONFIRMADO] XL-059','[CORREGIR] XL-060','Gala → Bandage','649 → S/ 500','Quitar foto:','Añadir foto:','[ELIMINAR] XL-061','[AGREGAR] NUEVO-ABC123','Faltan','Pendientes: 1','adjuntar el respaldo JSON'])assert(report.toLowerCase().includes(fragment.toLowerCase()),fragment);
});
test('WhatsApp conserva todas las partes y usa tamaños acotados incluso con notas largas',async()=>{
  const m=await model;const source=Array.from({length:600},(_,i)=>`XL-${i} · corregir categoría y añadir foto`).join('\n')+'\n'+'a'.repeat(8000);
  const parts=m.splitReport(source);
  assert(parts.length>2);assert(parts.every(p=>p.length<2450));
  const restored=parts.map(p=>p.slice(p.indexOf('\n')+1)).join('\n');
  for(let i=0;i<600;i++)assert(restored.includes(`XL-${i} · corregir categoría y añadir foto`));
  assert.equal(restored.replace(/\n/g,'').split('a').length,source.replace(/\n/g,'').split('a').length);
});
test('Restaurar rechaza códigos duplicados, catálogo incompleto, precios inválidos y rutas inseguras',async()=>{
  const m=await model;const originals=Array.from(catalog.products.slice(0,2),p=>m.normalize(p));
  for(const mutate of [p=>p.push(p[0]),p=>p.pop(),p=>p[0].price=-1,p=>p[0].photos[0].src='javascript:alert(1)',p=>p[0].photos[0].src='./images/../../secret.png',p=>p[0].category='Inventada']){
    const items=structuredClone(originals);mutate(items);assert.throws(()=>m.validateBackup({format:'xiliana-review-v1',items},Array.from(catalog.categories),originals));
  }
});
