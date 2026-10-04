import { products, categories } from './products.js';
import { displayImage, aiImageIds, productPath } from './catalog-utils.js';

const grid = document.querySelector('#product-grid');
const filters = document.querySelector('#filters');
const search = document.querySelector('#search');
const count = document.querySelector('#product-count');
const empty = document.querySelector('#empty');
const dialog = document.querySelector('#product-dialog');
const dialogContent = document.querySelector('#dialog-content');
const categoryShowcase = document.querySelector('#category-showcase-grid');
let activeCategory = 'Todos';
const featuredCategories = [
  { name: 'Gala', label: 'Vestidos de gala', image: './images/dress-01.jpg' },
  { name: 'Largos', label: 'Vestidos largos', image: './images/catalog-28-ai.png' },
  { name: 'Cortos con brillo', label: 'Cortos con brillo', image: './images/catalog-47-ai.png' },
  { name: 'Cortos', label: 'Vestidos cortos', image: './images/catalog-50-ai.png' },
  { name: 'Bandage', label: 'Bandage', image: './images/catalog-27-ai.png' },
  { name: 'Liquidación', label: 'En liquidación', image: './images/catalog-58-ai.png' },
];

const money = value => new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(value);
const normalize = value => value.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const whatsappUrl = product => `https://wa.me/51930527248?text=${encodeURIComponent(`Hola Xiliana Boutique, quisiera consultar por ${product.name} (S/ ${product.price.toFixed(2)} en el catálogo). ¿Está disponible y qué tallas tienen?`)}`;

function renderFilters() {
  filters.innerHTML = categories.map(category => `<button type="button" data-category="${escapeHtml(category)}" class="filter${category === activeCategory ? ' active' : ''}" aria-pressed="${category === activeCategory}">${escapeHtml(category)}</button>`).join('');
  categoryShowcase.querySelectorAll('[data-category]').forEach(button => {
    button.setAttribute('aria-pressed', String(button.dataset.category === activeCategory));
  });
}

categoryShowcase.innerHTML = featuredCategories.map(item => `<button type="button" class="category-tile" data-category="${escapeHtml(item.name)}" aria-label="Ver ${escapeHtml(item.label)}" aria-pressed="false"><img src="${item.image}" alt="" loading="lazy" /><span>${escapeHtml(item.label)}</span><small>Explorar colección ↗</small></button>`).join('');

function renderProducts() {
  const term = normalize(search.value.trim());
  const shown = products
    .filter(product => (activeCategory === 'Todos' || product.category === activeCategory) && normalize(`${product.name} ${product.category}`).includes(term))
    .sort((a, b) => categories.indexOf(a.category) - categories.indexOf(b.category) || a.id - b.id);
  count.textContent = shown.length;
  empty.hidden = shown.length > 0;
  grid.innerHTML = shown.map(product => `<article class="product-card${product.id > 17 && !aiImageIds.has(product.id) ? ' is-thumbnail' : ''}"><a href="${productPath(product)}" class="product-open" data-id="${product.id}" aria-label="Ver ${escapeHtml(product.name)}"><span class="product-image"><img src="${displayImage(product)}" alt="${escapeHtml(product.name)}" loading="lazy" />${product.originalPrice ? '<span class="sale-tag">Oferta</span>' : ''}</span><span class="product-meta"><span class="category">${escapeHtml(product.category)}</span><span class="view-link">Ver vestido ↗</span></span><span class="product-name">${escapeHtml(product.name)}</span><span class="price">${money(product.price)}${product.originalPrice ? `<del>${money(product.originalPrice)}</del>` : ''}</span></a></article>`).join('');
}

function openProduct(id) {
  const product = products.find(item => item.id === id);
  if (!product) return;
  dialogContent.innerHTML = `<div class="dialog-image${product.id > 17 && !aiImageIds.has(product.id) ? ' is-thumbnail' : ''}"><img src="${displayImage(product)}" alt="${escapeHtml(product.name)}" /></div><div class="dialog-info"><p class="eyebrow">Xiliana Boutique / ${escapeHtml(product.category)}</p><h2 id="dialog-title">${escapeHtml(product.name)}</h2><p class="dialog-price">${money(product.price)}${product.originalPrice ? `<del>${money(product.originalPrice)}</del>` : ''}</p>${product.note ? `<p class="product-note">${escapeHtml(product.note)}</p>` : ''}${product.imageNote ? `<p class="image-warning">${escapeHtml(product.imageNote)}</p>` : ''}${product.id > 17 && !aiImageIds.has(product.id) ? '<p class="product-note">Foto extraída de una captura del catálogo. Pide una imagen de mayor tamaño a la boutique.</p>' : ''}<p class="availability">Consulta talla, disponibilidad y entrega con la boutique antes de comprar.</p><a class="button button-dark" href="${whatsappUrl(product)}" target="_blank" rel="noopener noreferrer">Consultar por WhatsApp <span aria-hidden="true">↗</span></a></div>`;
  dialog.showModal();
}

filters.addEventListener('click', event => {
  const button = event.target.closest('[data-category]');
  if (!button) return;
  activeCategory = button.dataset.category;
  renderFilters();
  renderProducts();
});
categoryShowcase.addEventListener('click', event => {
  const button = event.target.closest('[data-category]');
  if (!button) return;
  activeCategory = button.dataset.category;
  search.value = '';
  renderFilters();
  renderProducts();
  document.querySelector('#coleccion').scrollIntoView({ behavior: 'smooth', block: 'start' });
});
search.addEventListener('input', renderProducts);
grid.addEventListener('click', event => {
  const button = event.target.closest('[data-id]');
  if (button && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) { event.preventDefault(); openProduct(Number(button.dataset.id)); }
});
document.querySelector('#dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });

renderFilters();
renderProducts();

const opening = document.querySelector('#opening');
const heroVideo = document.querySelector('#hero-video');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let openingTimer;

function closeOpening(skip = false) {
  if (!opening || opening.classList.contains('is-exiting')) return;
  clearTimeout(openingTimer);
  opening.classList.add('is-exiting');
  const exitDuration = skip ? 0 : prefersReducedMotion ? 200 : 600;
  window.setTimeout(() => document.body.classList.remove('opening-active'), exitDuration);
  window.setTimeout(() => opening.remove(), exitDuration);
  if (heroVideo) {
    heroVideo.currentTime = 0;
    heroVideo.play().catch(() => {});
  }
}

if (opening) {
  document.body.classList.add('opening-active');
  window.scrollTo(0, 0);
  opening.querySelector('#opening-skip').addEventListener('click', () => closeOpening(true));
  window.addEventListener('keydown', event => { if (event.key === 'Escape') closeOpening(true); });
  requestAnimationFrame(() => {
    opening.classList.add('is-playing');
    openingTimer = window.setTimeout(() => closeOpening(), 3800);
  });
} else {
  heroVideo?.play().catch(() => {});
}
