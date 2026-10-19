const dataNode = document.querySelector('#accessories-data');
const accessories = dataNode ? JSON.parse(dataNode.textContent) : [];

const escapeText = value => String(value ?? '');
let dialog;
let activeTrigger;
let activeAccessory;
let activePhoto = 0;

function ensureDialog() {
  if (dialog) return dialog;
  dialog = document.createElement('dialog');
  dialog.className = 'accessory-viewer';
  dialog.setAttribute('aria-labelledby', 'accessory-viewer-title');
  dialog.innerHTML = `
    <div class="accessory-viewer-layout">
      <div class="accessory-viewer-media">
        <button type="button" class="accessory-nav accessory-prev" aria-label="Ver foto anterior">←</button>
        <img class="accessory-viewer-image" alt="" />
        <button type="button" class="accessory-nav accessory-next" aria-label="Ver foto siguiente">→</button>
      </div>
      <div class="accessory-viewer-info">
        <button type="button" class="accessory-close" aria-label="Cerrar accesorio">×</button>
        <p class="category">Accesorios</p>
        <h2 id="accessory-viewer-title"></h2>
        <p class="accessory-viewer-price"></p>
        <p class="accessory-viewer-count" aria-live="polite"></p>
        <div class="accessory-thumbs" aria-label="Fotos del accesorio"></div>
      </div>
    </div>`;
  document.body.append(dialog);
  dialog.querySelector('.accessory-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.accessory-prev').addEventListener('click', () => showPhoto(activePhoto - 1));
  dialog.querySelector('.accessory-next').addEventListener('click', () => showPhoto(activePhoto + 1));
  dialog.addEventListener('click', event => {
    const box = dialog.querySelector('.accessory-viewer-layout').getBoundingClientRect();
    if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
  });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') showPhoto(activePhoto - 1);
    if (event.key === 'ArrowRight') showPhoto(activePhoto + 1);
  });
  dialog.addEventListener('close', () => activeTrigger?.focus({preventScroll:true}));
  return dialog;
}

function showPhoto(index) {
  if (!activeAccessory) return;
  const total = activeAccessory.photos.length;
  activePhoto = (index + total) % total;
  const image = dialog.querySelector('.accessory-viewer-image');
  image.src = activeAccessory.photos[activePhoto];
  image.alt = `${escapeText(activeAccessory.name)}, foto ${activePhoto + 1} de ${total}`;
  dialog.querySelector('.accessory-viewer-count').textContent = total > 1 ? `Foto ${activePhoto + 1} de ${total}` : 'Foto del accesorio';
  dialog.querySelectorAll('.accessory-thumbs button').forEach((button, i) => button.setAttribute('aria-pressed', String(i === activePhoto)));
}

function openAccessory(trigger) {
  const item = accessories[Number(trigger.dataset.accessoryIndex)];
  if (!item?.photos?.length) return;
  ensureDialog();
  activeTrigger = trigger;
  activeAccessory = item;
  dialog.querySelector('#accessory-viewer-title').textContent = item.name;
  dialog.querySelector('.accessory-viewer-price').textContent = `S/ ${Number(item.price).toFixed(2)}`;
  const thumbs = dialog.querySelector('.accessory-thumbs');
  thumbs.innerHTML = item.photos.map((photo, i) => `<button type="button" aria-label="Ver foto ${i + 1}" aria-pressed="${i === 0}"><img src="${photo}" alt="" /></button>`).join('');
  thumbs.hidden = item.photos.length < 2;
  thumbs.querySelectorAll('button').forEach((button, i) => button.addEventListener('click', () => showPhoto(i)));
  dialog.querySelector('.accessory-prev').hidden = item.photos.length < 2;
  dialog.querySelector('.accessory-next').hidden = item.photos.length < 2;
  showPhoto(0);
  dialog.showModal();
}

document.addEventListener('click', event => {
  const trigger = event.target.closest('.accessory-open');
  if (trigger) openAccessory(trigger);
});
