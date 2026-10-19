import { products } from './products.js';
import { displayImage, categoryPath, featuredCategoryIds } from './catalog-utils.js';
import './order-ui.js';
import { startVideo } from './video-audio.js';
import { introFinished, playBrandIntro } from './brand-intro.js';

const categoryShowcase = document.querySelector('#category-showcase-grid');
const featuredCategories = [
  { name: 'Gala', label: 'Vestidos de gala', image: displayImage(products.find(p => p.category === 'Gala')) },
  { name: 'Largos', label: 'Vestidos largos', image: displayImage(products.find(p => p.id === 24)) },
  { name: 'Cortos con brillo', label: 'Cortos con brillo', image: displayImage(products.find(p => p.id === 39)) },
  { name: 'Cortos', label: 'Vestidos cortos', image: displayImage(products.find(p => p.id === featuredCategoryIds.Cortos)) },
  { name: 'Bandage', label: 'Bandage', image: displayImage(products.find(p => p.id === 14)) },
];
featuredCategories.forEach(item=>item.image=displayImage(products.find(p=>p.id===featuredCategoryIds[item.name])));

const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);

categoryShowcase.innerHTML = featuredCategories.map(item => `<a class="category-tile" href="${categoryPath(item.name)}" aria-label="Explorar ${escapeHtml(item.label)}"><img src="${item.image}" alt="" loading="lazy" /><span>${escapeHtml(item.label)}</span><small>${products.filter(p => p.category === item.name).length} modelos · Ver colección ↗</small></a>`).join('');

introFinished.then(startVideo);
document.querySelector('[data-replay-intro]')?.addEventListener('click',()=>playBrandIntro(true).then(startVideo));

