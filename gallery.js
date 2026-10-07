const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
export function galleryMarkup(product) {
  const photos = product.photos?.length ? product.photos : [{src:product.image}];
  const name = escape(product.name);
  const caption = (photo, i) => escape(photo.view || `Foto ${i+1}`);
  const url = photo => escape(photo.src.replace(/^\.\//, '/'));
  const size = photo => photo.width ? `width="${photo.width}" height="${photo.height}"` : '';
  return `<div class="product-gallery" data-gallery><img class="gallery-main" src="${url(photos[0])}" alt="${name}, ${caption(photos[0],0)}" ${size(photos[0])} />${photos.length > 1 ? `<div class="gallery-thumbs" aria-label="Fotos de ${name}">${photos.map((photo,i) => `<button type="button" data-gallery-photo="${url(photo)}" data-photo-width="${photo.width || ''}" data-photo-height="${photo.height || ''}" data-photo-alt="${name}, ${caption(photo,i)}" data-photo-number="${i+1}" data-photo-view="${caption(photo,i)}" aria-label="Ver ${caption(photo,i).toLowerCase()}, foto ${i+1} de ${photos.length}" aria-pressed="${i===0}"><img src="${url(photo)}" alt="" loading="lazy" ${size(photo)} /><span>${caption(photo,i)}</span></button>`).join('')}</div><p class="gallery-count" aria-live="polite">${caption(photos[0],0)} · Foto 1 de ${photos.length}</p>` : ''}</div>`;
}
if (typeof document !== 'undefined') document.addEventListener('click', event => {
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
