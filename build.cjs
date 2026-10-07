const fs = require('node:fs');
const path = require('node:path');
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
function media(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || entry.name === 'imagenes-reales' || /^catalog-\d+-(ai|model|faithful[^.]*)\.png$/i.test(entry.name)) continue;
    const source = path.join(directory, entry.name);
    if (entry.isDirectory()) media(source);
    else if (entry.isFile() && mediaTypes.has(path.extname(entry.name).toLowerCase())) {
      copy(source, path.relative(__dirname, source));
    }
  }
}
for (const file of ['index.html', 'styles.css', 'experience.css', 'main.js', 'products.js', 'catalog-utils.js', 'gallery.js', 'order-data.js', 'order-ui.js', 'video-audio.js', 'collection-search.js', 'whatsapp-help.js', 'recommendations-carousel.js', '_headers']) {
  copy(path.join(__dirname, file), file);
}
media(path.join(__dirname, 'images'));
fs.writeFileSync(path.join(output, '.assetsignore'), '.git/\nnode_modules/\n*.cjs\n*.json\n*.jsonc\n*.md\n');
require('./seo-build.cjs')(output).then(() => {
  require('./validate-seo.cjs');
  console.log(`Publicación preparada: ${count} archivos base; mayor archivo ${(largest / 1024 / 1024).toFixed(2)} MiB.`);
}).catch(error => { console.error(error); process.exitCode = 1; });
