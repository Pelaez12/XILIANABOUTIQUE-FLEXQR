import { products } from './products.js';
import { displayImage, categoryPath } from './catalog-utils.js';
import './order-ui.js';
import { startVideo } from './video-audio.js';

const categoryShowcase = document.querySelector('#category-showcase-grid');
const featuredCategories = [
  { name: 'Gala', label: 'Vestidos de gala', image: displayImage(products.find(p => p.category === 'Gala')) },
  { name: 'Largos', label: 'Vestidos largos', image: displayImage(products.find(p => p.id === 24)) },
  { name: 'Cortos con brillo', label: 'Cortos con brillo', image: displayImage(products.find(p => p.id === 39)) },
  { name: 'Cortos', label: 'Vestidos cortos', image: displayImage(products.find(p => p.id === 10)) },
  { name: 'Bandage', label: 'Bandage', image: displayImage(products.find(p => p.id === 14)) },
  { name: 'Liquidación', label: 'En liquidación', image: displayImage(products.find(p => p.id === 17)) },
];

const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);

categoryShowcase.innerHTML = featuredCategories.map(item => `<a class="category-tile" href="${categoryPath(item.name)}" aria-label="Explorar ${escapeHtml(item.label)}"><img src="${item.image}" alt="" loading="lazy" /><span>${escapeHtml(item.label)}</span><small>${products.filter(p => p.category === item.name).length} modelos · Ver colección ↗</small></a>`).join('');

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
    startVideo();
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
  startVideo();
}
