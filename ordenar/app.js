import { products, categories as sourceCategories } from '../products.js';
import { normalize, differences, buildReport, splitReport, validateBackup } from './model.js';

const $=s=>document.querySelector(s);
const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const categories=sourceCategories.filter(c=>c!=='Todos');
const originals=products.map(normalize);
const byId=new Map(originals.map(p=>[p.id,p]));
let items=structuredClone(originals), selected='Todos', cursor=0, photoIndex=0, editing=null, isNew=false, history=[], db, busy=false, ready=false;
let toastTimer;
const money=n=>new Intl.NumberFormat('es-PE',{style:'currency',currency:'PEN'}).format(n);
const imageURL=p=>p.src.startsWith('data:')?p.src:'../'+p.src.replace(/^\.\//,'');
const photoLabel=p=>p.filename||p.src.split('/').pop();
function toast(message){$('#toast').textContent=message;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,4500);}
function openDB(){return new Promise((resolve,reject)=>{const r=indexedDB.open('xiliana-owner-review',1);r.onupgradeneeded=()=>r.result.createObjectStore('drafts');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});}
function readDraft(){return new Promise((resolve,reject)=>{const r=db.transaction('drafts').objectStore('drafts').get('active');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});}
function saveDraft(next){return new Promise((resolve,reject)=>{const t=db.transaction('drafts','readwrite');t.objectStore('drafts').put({format:'xiliana-review-v1',items:next,savedAt:new Date().toISOString()},'active');t.oncomplete=resolve;t.onerror=()=>reject(t.error);t.onabort=()=>reject(t.error);});}
async function commit(next,{undo=false}={}) {
  if(busy||!ready) return false;
  busy=true;$('#save-state').textContent='Guardando…';
  try{
    await saveDraft(next);
    if(!undo){history.push(items);if(history.length>25)history.shift();}
    items=next;photoIndex=0;render();return true;
  }catch(error){$('#save-state').textContent='No se pudo guardar';toast('No pudimos guardar. Libera espacio y vuelve a intentar. Tus decisiones anteriores siguen guardadas.');return false;}
  finally{busy=false;}
}
function filtered(){const q=$('#search').value.trim().toLocaleLowerCase('es');return items.filter(p=>{
  const status=$('#status').value;
  return (selected==='Todos'||p.category===selected)&&(p.name+' '+p.id).toLocaleLowerCase('es').includes(q)&&(status==='all'||status==='pending'&&p.status==='pending'||status==='reviewed'&&p.status!=='pending'||status==='changes'&&p.status!=='pending'&&(p.status==='deleted'||!byId.has(p.id)||differences(byId.get(p.id),p).length||p.notes));
});}
function render(){
  const reviewed=items.filter(p=>p.status!=='pending').length;
  $('#progress-text').textContent=`${reviewed} de ${items.length} prendas revisadas`;
  $('#progress').max=items.length||1;$('#progress').value=reviewed;
  $('#save-state').textContent='Avance guardado en este navegador';
  $('#finish').disabled=false;$('#add').disabled=false;$('#undo').disabled=!history.length;
  $('#categories').innerHTML=['Todos',...categories].map(c=>`<button class="category-tab" data-category="${escape(c)}" aria-pressed="${selected===c}">${escape(c)}<small>${items.filter(p=>(c==='Todos'||p.category===c)&&p.status==='pending').length}</small></button>`).join('');
  renderCard();
}
function renderCard(){
  const list=filtered();cursor=Math.max(0,Math.min(cursor,list.length-1));
  if(!list.length){const allDone=items.every(p=>p.status!=='pending');$('#game').innerHTML=`<div class="empty"><div class="checkmark" aria-hidden="true">✓</div><h2>${allDone?'¡Colección revisada!':'No quedan tarjetas en esta vista'}</h2><p>${allDone?'Ya puedes revisar tus decisiones y preparar el informe para WhatsApp.':'Elige otra colección o cambia los filtros para seguir ordenando.'}</p><button class="primary" data-action="${allDone?'summary':'show-all'}">${allDone?'Ver resumen final ↗':'Ver todas las pendientes'}</button></div>`;return;}
  const p=list[cursor];photoIndex=Math.min(photoIndex,Math.max(0,p.photos.length-1));const photo=p.photos[photoIndex];
  $('#game').innerHTML=`<article class="review-card" data-id="${escape(p.id)}"><div class="photo-stage">${photo?`<img class="hero-image" src="${escape(imageURL(photo))}" alt="${escape(p.name)}: ${escape(photo.view)}"><span class="photo-counter">${photoIndex+1} / ${p.photos.length} fotos</span><div class="photo-nav"><button data-action="prev-photo" aria-label="Foto anterior" ${p.photos.length<2?'disabled':''}>‹</button><span>${escape(photo.view)}</span><button data-action="next-photo" aria-label="Foto siguiente" ${p.photos.length<2?'disabled':''}>›</button></div>`:'<div class="placeholder">Esta prenda necesita una foto.<br>Usa «Corregir» para añadirla.</div>'}</div><div class="card-info"><div class="card-meta"><span class="code">${escape(p.id)}</span><span>${cursor+1} de ${list.length} en esta vista</span></div><h2>${escape(p.name)}</h2><p class="price">${money(p.price)}</p><p class="question">¿Pertenece a esta colección?</p><strong class="category-name">${escape(p.category)}</strong>${p.status!=='pending'?`<p class="pill ${p.status==='deleted'?'deleted':''}">${p.status==='deleted'?'Eliminación solicitada':p.status==='confirmed'?'Clasificación confirmada':'Corrección registrada'}</p>`:''}${p.missing?'<p class="card-note">Faltan fotos por conseguir.</p>':''}${p.notes?`<p class="card-note">${escape(p.notes)}</p>`:''}<div class="decision-actions"><span class="decision-context">¿Va en ${escape(p.category)}?</span><button class="wrong" data-action="edit"><b aria-hidden="true">×</b> Corregir</button><button class="correct" data-action="confirm"><b aria-hidden="true">✓</b> Sí, va aquí</button></div><div class="secondary-actions"><button class="text-button" data-action="previous" ${list.length<2?'disabled':''}>← Anterior</button><button class="text-button" data-action="skip" ${list.length<2?'disabled':''}>Ver después →</button></div></div></article>`;
  const img=$('.hero-image');if(img){img.addEventListener('click',()=>img.classList.toggle('zoomed'));img.addEventListener('error',()=>{img.alt='No se pudo cargar esta foto. Márcala como faltante desde Corregir.';toast('Hay una foto que no carga. Puedes reemplazarla o marcarla como faltante.');},{once:true});}
}
function current(){return filtered()[cursor];}
function showNextCard(){if(matchMedia('(max-width:760px)').matches)$('#game').scrollIntoView({block:'start'});}
function openEditor(p,newProduct=false){
  editing=structuredClone(p);isNew=newProduct;
  $('#edit-code').textContent=p.id;$('#editor-title').textContent=newProduct?'Añade una prenda':'Acomoda esta prenda';
  $('#edit-name').value=p.name;$('#edit-category').innerHTML=categories.map(c=>`<option ${c===p.category?'selected':''}>${escape(c)}</option>`).join('');
  $('#edit-price').value=p.price;$('#edit-notes').value=p.notes;$('#edit-missing').checked=p.missing;
  $('#delete-product').hidden=newProduct;$('#edit-error').textContent='';renderEditPhotos();$('#editor').showModal();
}
function renderEditPhotos(){
  $('#edit-photos').innerHTML=editing.photos.length?editing.photos.map((p,i)=>`<div class="edit-photo"><img src="${escape(imageURL(p))}" alt="${escape(p.view)}"><div><button type="button" data-cover="${i}" ${i===0?'disabled':''} aria-label="Usar foto ${i+1} como portada">${i===0?'Portada':'Portada ↑'}</button><button type="button" data-remove="${i}" aria-label="Quitar foto ${i+1}">Quitar</button></div></div>`).join(''):'<p class="card-note">Añade una foto del catálogo o sube una imagen real.</p>';
}
function captureEditor(){return {...editing,name:$('#edit-name').value.trim(),category:$('#edit-category').value,price:Number($('#edit-price').value),notes:$('#edit-notes').value.trim(),missing:$('#edit-missing').checked,status:'edited'};}
function renderPool(){
  const q=$('#photo-search').value.trim().toLowerCase();
  const pool=originals.filter(p=>(p.name+' '+p.id).toLowerCase().includes(q)).flatMap(p=>p.photos.map(f=>({...f,product:p})));
  $('#photo-pool').innerHTML=pool.length?pool.map((f,i)=>`<button type="button" class="pool-photo" data-pool="${i}" ${editing.photos.some(p=>p.src===f.src)?'disabled':''}><img loading="lazy" src="${escape(imageURL(f))}" alt="${escape(f.product.name)}: ${escape(f.view)}"><span><strong>${escape(f.product.id)}</strong> · ${escape(f.view)}<br>${escape(f.product.name)}</span></button>`).join(''):'<p>No se encontraron fotos. Busca otro nombre o código.</p>';
  $('#photo-pool').querySelectorAll('[data-pool]').forEach(button=>button.addEventListener('click',()=>{
    if(editing.photos.length>=40){toast('Máximo 40 fotos por prenda.');return;}
    const f=pool[Number(button.dataset.pool)];editing.photos.push({src:f.src,view:f.view});renderEditPhotos();$('#picker').close();toast(`Foto de ${f.product.id} añadida a la tarjeta.`);
  }));
}
function download(content,name,type){const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);}
function backup(){download(JSON.stringify({format:'xiliana-review-v1',savedAt:new Date().toISOString(),items},null,2),'xiliana-respaldo-con-fotos.json','application/json');}
function showSummary(){
  const report=buildReport(originals,items);$('#report').textContent=report;
  const pending=items.filter(p=>p.status==='pending').length;
  $('#summary-count').textContent=pending?`Quedan ${pending} prendas sin revisar. Puedes volver al juego o compartir el avance actual.`:'¡Revisaste todas las prendas! El informe incluye confirmaciones, cambios, eliminaciones y nuevas prendas.';
  const parts=splitReport(report);
  $('#whatsapp-parts').innerHTML=items.some(p=>p.status!=='pending')?parts.map((text,i)=>`<a class="primary" target="_blank" rel="noopener noreferrer" href="https://wa.me/51992272521?text=${encodeURIComponent(text)}">Abrir WhatsApp${parts.length>1?` · ${i+1}/${parts.length}`:''} ↗</a>`).join(''):'';
  $('#summary').showModal();
}
$('#categories').addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(!b)return;selected=b.dataset.category;cursor=0;photoIndex=0;render();});
for(const id of ['search','status'])$('#'+id).addEventListener(id==='search'?'input':'change',()=>{cursor=0;photoIndex=0;renderCard();});
$('#game').addEventListener('click',async e=>{
  const action=e.target.closest('[data-action]')?.dataset.action;if(!action||busy||!ready)return;
  if(action==='summary'){showSummary();return;}
  if(action==='show-all'){selected='Todos';$('#search').value='';$('#status').value='pending';cursor=0;render();return;}
  const p=current();if(!p)return;
  if(action==='edit')openEditor(p);
  if(action==='confirm'){
    if(p.missing||!p.photos.length){toast('Revisa las fotos pendientes con «Corregir» antes de confirmar.');openEditor(p);return;}
    const next=items.map(i=>i.id===p.id?{...i,status:differences(byId.get(i.id),i).length||i.notes?'edited':'confirmed'}:i);
    if(await commit(next)){toast(`${p.id} · clasificación confirmada`);showNextCard();}
  }
  if(action==='skip'||action==='previous'){cursor=(cursor+(action==='skip'?1:-1)+filtered().length)%filtered().length;photoIndex=0;renderCard();showNextCard();}
  if(action==='prev-photo'||action==='next-photo'){photoIndex=(photoIndex+(action==='next-photo'?1:-1)+p.photos.length)%p.photos.length;renderCard();}
});
$('#add').addEventListener('click',()=>openEditor({id:'NUEVO-'+crypto.randomUUID().slice(0,8).toUpperCase(),name:'',category:selected==='Todos'?categories[0]:selected,price:0,notes:'',photos:[],missing:false,status:'pending'},true));
$('#edit-photos').addEventListener('click',e=>{const remove=e.target.closest('[data-remove]'),cover=e.target.closest('[data-cover]');if(remove){editing.photos.splice(Number(remove.dataset.remove),1);renderEditPhotos();}if(cover){editing.photos.unshift(...editing.photos.splice(Number(cover.dataset.cover),1));renderEditPhotos();}});
$('#pick-photo').addEventListener('click',()=>{$('#photo-search').value='';renderPool();$('#picker').showModal();});
$('#photo-search').addEventListener('input',renderPool);
$('#upload').addEventListener('change',async e=>{
  const files=Array.from(e.target.files);
  if(files.length+editing.photos.length>40){toast('Máximo 40 fotos por prenda.');e.target.value='';return;}
  const submit=$('#edit-form button[type=submit]');submit.disabled=true;
  try{for(const file of files){
    if(!['image/jpeg','image/png','image/webp'].includes(file.type)||file.size>10*1024*1024)throw Error('Usa imágenes JPG, PNG o WebP de hasta 10 MB cada una.');
    const src=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=reject;r.readAsDataURL(file);});
    await new Promise((resolve,reject)=>{const img=new Image();img.onload=resolve;img.onerror=()=>reject(Error('El archivo no es una imagen válida.'));img.src=src;});
    editing.photos.push({src,filename:`${editing.id}-${editing.photos.length+1}-${file.name}`,view:'Foto subida'});
  }}catch(error){toast(error.message||'No se pudo leer la imagen.');}finally{submit.disabled=false;e.target.value='';renderEditPhotos();}
});
$('#edit-form').addEventListener('submit',async e=>{
  e.preventDefault();const p=captureEditor();
  if(!p.name){$('#edit-error').textContent='Escribe el nombre o una distinción para reconocer la prenda.';return;}
  if(!p.photos.length&&!p.missing){$('#edit-error').textContent='Añade una foto o marca «Faltan fotos por conseguir».';return;}
  if(!categories.includes(p.category)||!Number.isFinite(p.price)||p.price<0||p.price>100000)return;
  const submit=$('#edit-form button[type=submit]');submit.disabled=true;
  const next=isNew?[...items,p]:items.map(i=>i.id===p.id?p:i);
  if(await commit(next)){$('#editor').close();toast(`${p.id} · ${isNew?'prenda añadida':'corrección guardada'}`);showNextCard();}
  submit.disabled=false;
});
$('#delete-product').addEventListener('click',async()=>{
  const p=captureEditor();p.status='deleted';
  if(await commit(items.map(i=>i.id===p.id?p:i))){$('#editor').close();toast(`${p.id} · eliminación solicitada. Puedes deshacerla.`);}
});
$('#undo').addEventListener('click',async()=>{if(!history.length||busy)return;const previous=history.at(-1);if(await commit(previous,{undo:true})){history.pop();$('#undo').disabled=!history.length;toast('Última decisión deshecha.');}});
$('#finish').addEventListener('click',showSummary);
$('#backup').addEventListener('click',backup);$('#summary-backup').addEventListener('click',backup);
$('#download-report').addEventListener('click',()=>download(buildReport(originals,items),'xiliana-correcciones.txt','text/plain;charset=utf-8'));
$('#restore').addEventListener('change',async e=>{
  const file=e.target.files[0];if(!file)return;
  try{if(file.size>150*1024*1024)throw Error('El respaldo supera los 150 MB.');const data=JSON.parse(await file.text());const next=validateBackup(data,categories,originals);if(await commit(next))toast('Respaldo restaurado. Puedes deshacer esta restauración.');}catch(error){toast(error.message||'No se pudo restaurar el respaldo.');}finally{e.target.value='';}
});
document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',()=>$('#'+b.dataset.close).close()));
async function init(){
  try{db=await openDB();const draft=await readDraft();
    if(draft){try{items=validateBackup(draft,categories,originals);}catch(error){toast('El catálogo cambió. Descarga tu respaldo anterior antes de empezar de nuevo.');download(JSON.stringify(draft,null,2),'xiliana-respaldo-anterior.json','application/json');}}
    ready=true;render();
  }catch(error){$('#save-state').textContent='Almacenamiento no disponible';$('#game').innerHTML='<div class="empty"><h2>Activa el almacenamiento del navegador</h2><p>Necesitamos guardar tus decisiones y fotos. Abre esta página en una ventana normal y permite el almacenamiento del sitio. Después recarga la página.</p></div>';}
}
init();
