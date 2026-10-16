const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
export function galleryMarkup(product) {
  const photos = product.photos?.length ? product.photos : [{src:product.image}];
  const name = escape(product.name);
  const caption = (photo, i) => escape(photo.view || `Foto ${i+1}`);
  const url = photo => escape(photo.src.replace(/^\.\//, '/'));
  const size = photo => photo.width ? `width="${photo.width}" height="${photo.height}"` : '';
  return `<div class="product-gallery" data-gallery><button type="button" class="gallery-zoom" aria-label="Ampliar foto de ${name}"><img class="gallery-main" src="${url(photos[0])}" alt="${name}, ${caption(photos[0],0)}" ${size(photos[0])} /><span class="gallery-zoom-hint">Ampliar ⤢</span></button>${photos.length > 1 ? `<div class="gallery-thumbs" aria-label="Fotos de ${name}">${photos.map((photo,i) => `<button type="button" data-gallery-photo="${url(photo)}" data-photo-width="${photo.width || ''}" data-photo-height="${photo.height || ''}" data-photo-alt="${name}, ${caption(photo,i)}" data-photo-number="${i+1}" data-photo-view="${caption(photo,i)}" aria-label="Ver ${caption(photo,i).toLowerCase()}, foto ${i+1} de ${photos.length}" aria-pressed="${i===0}"><img src="${url(photo)}" alt="" loading="lazy" ${size(photo)} /><span>${caption(photo,i)}</span></button>`).join('')}</div><p class="gallery-count" aria-live="polite">${caption(photos[0],0)} · Foto 1 de ${photos.length}</p>` : ''}</div>`;
}
let viewer, viewerTrigger;
function openPhoto(trigger){
 if(!viewer){
  viewer=document.createElement('dialog');viewer.className='photo-viewer';viewer.setAttribute('aria-labelledby','photo-viewer-title');
  viewer.innerHTML='<header><p id="photo-viewer-title">Foto del vestido</p><button type="button" data-photo-zoom aria-pressed="false">Acercar +</button><button type="button" data-photo-close aria-label="Cerrar foto ampliada">×</button></header><div class="photo-viewer-stage" tabindex="0" role="region" aria-label="Fotografía ampliada, desplazable al acercar"><img alt=""/></div><p class="photo-viewer-note">Acerca la foto y desliza para ver los detalles.</p>';
  document.body.append(viewer);
  viewer.querySelector('[data-photo-close]').addEventListener('click',()=>viewer.close());
  viewer.querySelector('[data-photo-zoom]').addEventListener('click',event=>{
   const zoomed=viewer.classList.toggle('is-zoomed');event.currentTarget.setAttribute('aria-pressed',String(zoomed));event.currentTarget.textContent=zoomed?'Alejar −':'Acercar +';
  });
  viewer.addEventListener('click',event=>{if(event.target!==viewer)return;const r=viewer.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)viewer.close();});
  viewer.addEventListener('close',()=>viewerTrigger?.focus({preventScroll:true}));
 }
 viewerTrigger=trigger;const source=trigger.querySelector('.gallery-main'),image=viewer.querySelector('img');image.src=source.src;image.alt=source.alt;
 viewer.classList.remove('is-zoomed');const zoom=viewer.querySelector('[data-photo-zoom]');zoom.setAttribute('aria-pressed','false');zoom.textContent='Acercar +';
 const stage=viewer.querySelector('.photo-viewer-stage');stage.scrollTop=0;stage.scrollLeft=0;viewer.showModal();
}
if (typeof document !== 'undefined') document.addEventListener('click', event => {
  const zoom=event.target.closest('.gallery-zoom');if(zoom){openPhoto(zoom);return;}
  const button = event.target.closest('[data-gallery-photo]');
  if (!button) return;
  const gallery = button.closest('[data-gallery]');
  const photo = gallery.querySelector('.gallery-main');
  photo.src = button.dataset.galleryPhoto;
  photo.alt = button.dataset.photoAlt;
  if (button.dataset.photoWidth) {
    photo.width = Number(button.dataset.photoWidth);
    photo.height = Number(button.dataset.photoHeight);
  }
  const buttons = gallery.querySelectorAll('[data-gallery-photo]');
  buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  gallery.querySelector('.gallery-count').textContent = `${button.dataset.photoView} · Foto ${button.dataset.photoNumber} de ${buttons.length}`;
});
