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
  { name: 'Liquidación', label: 'Ofertas · Liquidación', image: displayImage(products.find(p => p.id === 17)) },
];

const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);

categoryShowcase.innerHTML = featuredCategories.map(item => `<a class="category-tile" href="${categoryPath(item.name)}" aria-label="Explorar ${escapeHtml(item.label)}"><img src="${item.image}" alt="" loading="lazy" /><span>${escapeHtml(item.label)}</span><small>${products.filter(p => item.name === 'Liquidación' ? p.price != null && p.originalPrice > p.price : p.category === item.name).length} modelos · Ver colección ↗</small></a>`).join('');

document.querySelector('#opening')?.remove();
document.body.classList.remove('opening-active');
startVideo();

