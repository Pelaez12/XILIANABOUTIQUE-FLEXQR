const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const output = path.join(__dirname, 'public');
const wrangler = JSON.parse(fs.readFileSync(path.join(__dirname, 'wrangler.jsonc'), 'utf8'));
assert.equal(path.resolve(__dirname, wrangler.assets.directory), output, 'Wrangler debe publicar solo public/');
assert.equal(wrangler.assets.not_found_handling, '404-page');
assert.equal(wrangler.assets.html_handling, 'auto-trailing-slash');
const origin = require('./site-config.json').url;
const files = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(file); else files.push(file);
  }
}
walk(output);
const pages = files.filter(file => file.endsWith('index.html'));
const expectedPages = 103; // Inicio, 6 categorías y 96 productos confirmados.
assert.equal(pages.length, expectedPages);
let schemas = 0;
let galleryPhotos = 0;
for (const file of files) {
  assert(fs.statSync(file).size <= 25 * 1024 * 1024, `Archivo grande: ${file}`);
  assert(!path.relative(output, file).split(path.sep).includes('.git'), 'Se incluyó .git');
  assert(!/\.(?:cjs|jsonc?|md|xlsx|pdf)$/i.test(file), `Archivo de trabajo en publicación: ${file}`);
  assert(!/^catalog-\d+-(ai|model|faithful[^.]*)\.png$/i.test(path.basename(file)), `Recreación retirada en publicación: ${file}`);
}
for (const file of pages) {
  const html = fs.readFileSync(file, 'utf8');
  assert.equal((html.match(/<h1\b/g) || []).length, 1, `H1: ${file}`);
  assert.equal((html.match(/rel="canonical"/g) || []).length, 1, `Canonical: ${file}`);
  const route = '/' + path.relative(output, path.dirname(file)).split(path.sep).filter(Boolean).join('/');
  const expected = origin + (route === '/' ? '/' : route + '/');
  assert(html.includes(`rel="canonical" href="${expected}"`), `Dominio/ruta: ${file}`);
  for (const match of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    const data = JSON.parse(match[1]);
    assert.equal(data['@context'], 'https://schema.org');
    schemas++;
    for (const product of data['@graph'].filter(item => item['@type'] === 'Product')) {
      if (!product.image) continue;
      assert(Array.isArray(product.image) && product.image.length > 0);
      galleryPhotos += product.image.length;
      for (const photo of product.image) {
        const target = path.join(output, decodeURIComponent(new URL(photo).pathname));
        assert(fs.existsSync(target), `Foto de galería ausente: ${photo}`);
      }
    }
  }
  for (const match of html.matchAll(/(?:src|href)="([^"#]+)"/g)) {
    const value = match[1].replace(/&amp;/g, '&');
    if (/^(https?:|tel:|mailto:)/.test(value)) continue;
    const url = new URL(value, expected);
    let target = path.join(output, decodeURIComponent(url.pathname));
    if (url.pathname.endsWith('/')) target = path.join(target, 'index.html');
    assert(fs.existsSync(target), `Enlace/imagen ausente: ${value} en ${file}`);
  }
}
const sitemap = fs.readFileSync(path.join(output, 'sitemap.xml'), 'utf8');
assert(fs.readFileSync(path.join(output, '404.html'), 'utf8').includes('noindex'), '404 debe excluirse de indexación');
assert(!fs.readFileSync(path.join(output, 'index.html'), 'utf8').includes('xilianaboutiqueoficial.com'), 'Dominio antiguo en portada');
assert.equal((sitemap.match(/<loc>/g) || []).length, expectedPages);
assert.equal((sitemap.match(/<image:loc>/g) || []).length, galleryPhotos);
assert(fs.readFileSync(path.join(output, 'robots.txt'), 'utf8').includes(origin + '/sitemap.xml'));
assert.equal(schemas, expectedPages);
const productSource = fs.readFileSync(path.join(__dirname, 'products.js'), 'utf8');
const products = JSON.parse(productSource.match(/export const products = ([\s\S]*?);\s*export const categories/)[1]);
for (const product of products) {
  assert(product.photos[0].view.startsWith('Frente'), `Portada de espalda: ${product.name}`);
  assert.equal(product.image, product.photos[0].src, `Portada distinta a foto 1: ${product.name}`);
  assert.equal(new Set(product.photos.map(photo => photo.sha256)).size, product.photos.length, `Fotos idénticas repetidas: ${product.name}`);
  const directory = fs.readdirSync(path.join(output, 'vestidos')).find(name => name.startsWith(product.id + '-'));
  const html = fs.readFileSync(path.join(output, 'vestidos', directory, 'index.html'), 'utf8');
  assert(html.includes(`<img class="gallery-main" src="${product.image.replace(/^\.\//, '/')}"`), `Primera foto incorrecta: ${product.name}`);
  assert.equal((html.match(/data-gallery-photo=/g) || []).length, product.photos.length > 1 ? product.photos.length : 0, `Miniaturas incorrectas: ${product.name}`);
  if (product.photos.length === 1) assert(!html.includes('class="gallery-count"'), `Contador innecesario: ${product.name}`);
}
assert(fs.readFileSync(path.join(output, 'colecciones/cortos-con-brillo/index.html'), 'utf8').includes('data-id="57"'));
assert(!fs.readFileSync(path.join(output, 'index.html'), 'utf8').includes('data-id="58"'));
console.log(`SEO validado: ${expectedPages} páginas, ${expectedPages} bloques JSON-LD, ${galleryPhotos} imágenes de sitemap y todos los enlaces locales presentes.`);
