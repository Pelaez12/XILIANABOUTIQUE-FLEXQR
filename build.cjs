const fs = require('node:fs');
const path = require('node:path');
const products = require('./validar-registro.cjs').validateRegistry();
const accessories = require('./data/accessories.json');
const output = path.join(__dirname, 'public');
// public es una salida regenerable; rechazar enlaces a otras carpetas.
if (output !== path.resolve(__dirname, 'public') || path.dirname(output) !== __dirname) throw new Error('Ruta de publicación no válida');
if (fs.existsSync(output)) {
  if (fs.realpathSync(output).toLowerCase() !== output.toLowerCase()) throw new Error('public no puede ser un enlace a otra carpeta');
  fs.rmSync(output, { recursive: true, force: true });
}
const mediaTypes = new Set(['.jpg', '.jpeg', '.png', '.webp', '.svg', '.mp4', '.woff', '.woff2']);
let count = 0;
let largest = 0;
function copy(source, relative) {
  const size = fs.statSync(source).size;
  if (size > 25 * 1024 * 1024) throw new Error(`Archivo superior a 25 MiB: ${relative}`);
  const target = path.join(output, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(source, target);
  largest = Math.max(largest, size);
  count++;
}
// Publicar solo las fotos activas y los recursos que usa la interfaz.
const assets = new Set([
  ...products.flatMap(product => product.photos.map(photo => photo.src)),
  ...accessories.flatMap(accessory => accessory.fotos_web),
  'images/xiliana-logo-gold-black.png', 'images/xiliana-video.mp4',
  'images/foto-pendiente.svg',
  ...['instagram', 'tiktok', 'googlemaps', 'whatsapp'].map(name => `images/social/${name}.svg`),
]);
for (const file of ['index.html', 'styles.css', 'experience.css', 'main.js', 'brand-intro.js', 'products.js', 'catalog-utils.js', 'gallery.js', 'order-data.js', 'order-ui.js', 'quick-consult.js', 'video-audio.js', 'collection-search.js', 'whatsapp-help.js', 'recommendations-carousel.js', '_headers']) {
  copy(path.join(__dirname, file), file);
}
for (const asset of assets) {
  const source = path.resolve(__dirname, asset);
  const relative = path.relative(__dirname, source);
  if (!relative.startsWith(`images${path.sep}`) || !mediaTypes.has(path.extname(source).toLowerCase())) throw new Error(`Recurso no permitido: ${asset}`);
  copy(source, relative);
}
// Herramienta de revisión del dueño: reutiliza el catálogo y sus fotos originales.
for (const file of ['index.html', 'style.css', 'app.js', 'model.js']) {
  copy(path.join(__dirname, 'ordenar', file), path.join('ordenar', file));
}
fs.writeFileSync(path.join(output, '.assetsignore'), '.git/\nnode_modules/\n*.cjs\n*.json\n*.jsonc\n*.md\n');
require('./seo-build.cjs')(output).then(() => {
  require('./validate-seo.cjs');
  console.log(`Publicación preparada: ${count} archivos base; mayor archivo ${(largest / 1024 / 1024).toFixed(2)} MiB.`);
}).catch(error => { console.error(error); process.exitCode = 1; });
