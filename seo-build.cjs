const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const config = require('./site-config.json');
const base = config.url.replace(/\/$/, '');
const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const json = value => JSON.stringify(value).replace(/</g, '\\u003c');
const money = value => new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(value);
const absolute = relative => new URL(relative.replace(/^\.\//, '/'), base).href;
const loadModule = file => import('data:text/javascript;base64,' + fs.readFileSync(path.join(__dirname, file)).toString('base64'));

module.exports = async function buildSEO(output) {
  if (new URL(base).protocol !== 'https:') throw new Error('El dominio público debe usar HTTPS.');
  const { products, categories } = await loadModule('products.js');
  const { displayImage, restoredImageIds, productPath, categoryPath } = await loadModule('catalog-utils.js');
  const dimensions = p => { const data = fs.readFileSync(path.join(__dirname, displayImage(p))); return data[0] === 137 ? `width="${data.readUInt32BE(16)}" height="${data.readUInt32BE(20)}"` : p.id >= 18 ? 'width="256" height="256"' : 'width="1122" height="1402"'; };
  const image = product => displayImage(product).replace(/^\.\//, '/');
  const business = {
    '@type': 'ClothingStore', '@id': `${base}/#boutique`, name: config.name, url: `${base}/`,
    telephone: config.telephone, email: config.email,
    openingHoursSpecification: [{ '@type': 'OpeningHoursSpecification', dayOfWeek: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], opens: '11:00', closes: '20:00' }],
    logo: absolute('./images/xiliana-logo-gold-black.png'), image: absolute('./images/dress-01.jpg'),
    address: { '@type': 'PostalAddress', streetAddress: 'Avenida Horacio Urteaga 1438, Tienda 166, Centro Comercial El Rey', addressLocality: 'Jesús María', addressRegion: 'Lima', postalCode: '15072', addressCountry: 'PE' },
    sameAs: ['https://www.instagram.com/xilianaboutiqueof/', 'https://www.tiktok.com/@xilianaboutique'],
    hasMap: 'https://www.google.com/maps/search/?api=1&query=Xiliana%20Boutique%20Horacio%20Urteaga%201438%20Jes%C3%BAs%20Mar%C3%ADa'
  };
  const website = { '@type': 'WebSite', '@id': `${base}/#website`, name: config.name, url: `${base}/`, inLanguage: 'es-PE', publisher: { '@id': business['@id'] } };
  const head = (title, description, urlPath, photo, data) => `
    <link rel="canonical" href="${escape(base + urlPath)}" />
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="es_PE" />
    <meta property="og:site_name" content="${escape(config.name)}" />
    <meta property="og:title" content="${escape(title)}" />
    <meta property="og:description" content="${escape(description)}" />
    <meta property="og:url" content="${escape(base + urlPath)}" />
    <meta property="og:image" content="${escape(absolute(photo))}" />
    <meta property="og:image:alt" content="${escape(title)}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${escape(title)}" />
    <meta name="twitter:description" content="${escape(description)}" />
    <meta name="twitter:image" content="${escape(absolute(photo))}" />
    <script type="application/ld+json">${json({ '@context': 'https://schema.org', '@graph': data })}</script>`;
  const write = (relative, text) => {
    const target = path.join(output, relative);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, text);
  };
  const categoryLinks = `<nav class="collection-links" aria-label="Colecciones de vestidos">${categories.filter(c => c !== 'Todos').map(c => `<a href="${categoryPath(c)}">Vestidos ${escape(c.toLowerCase())}</a>`).join('')}</nav>`;
  const cards = items => items.map(p => `<article class="product-card"><a class="product-open" href="${productPath(p)}" data-id="${p.id}" aria-label="Ver ${escape(p.name)}"><span class="product-image"><img src="${image(p)}" alt="${escape(p.name)}" ${dimensions(p)} loading="lazy" decoding="async" />${p.originalPrice ? '<span class="sale-tag">Oferta</span>' : ''}</span><span class="product-meta"><span class="category">${escape(p.category)}</span><span class="view-link">Ver vestido ↗</span></span><h2 class="product-name">${escape(p.name)}</h2><span class="price">${money(p.price)}${p.originalPrice ? `<del>${money(p.originalPrice)}</del>` : ''}</span></a></article>`).join('');
  const itemList = items => ({ '@type': 'ItemList', itemListElement: items.map((p, i) => ({ '@type': 'ListItem', position: i + 1, name: p.name, url: base + productPath(p) })) });
  const breadcrumbs = entries => ({ '@type': 'BreadcrumbList', itemListElement: entries.map(([name, url], i) => ({ '@type': 'ListItem', position: i + 1, name, item: base + url })) });
  const header = `<header class="site-header"><a class="brand-logo" href="/" aria-label="Xiliana Boutique, inicio"><img src="/images/xiliana-logo-gold-black.png" alt="Xiliana Boutique by Antonio Grau" width="188" height="68" /></a><nav aria-label="Navegación principal"><a href="/#coleccion">Colección</a><a href="/#visitanos">Visítanos</a><a href="https://wa.me/51930527248">WhatsApp ↗</a></nav></header>`;
  const footer = `<footer class="site-footer"><div class="footer-main"><a class="brand-logo" href="/"><img src="/images/xiliana-logo-gold-black.png" alt="Xiliana Boutique" loading="lazy" /></a><p>Solo una vida para lucirte.</p><a href="/#visitanos">Visita nuestra boutique ↗</a></div><p class="business-hours">Lunes a sábado: 11:00 a. m. – 8:00 p. m. · Domingo cerrado</p><address>Avenida Horacio Urteaga 1438, Tienda 166 · Centro Comercial El Rey · Jesús María, Lima</address><p><a href="tel:+51930527248">+51 930 527 248</a> · <a href="mailto:xilianaboutique@gmail.com">xilianaboutique@gmail.com</a></p><div class="footer-bottom"><small>Prendas únicas y personalizadas, sin talla definida por ahora. Medidas, precios y disponibilidad se coordinan con Xiliana Boutique.</small><div class="creator-credit"><span>Sitio creado por <strong>FLEXCOREOS</strong></span><a href="tel:+51992272521">¿Quieres un sitio así? Llámanos al <strong>992 272 521</strong> ↗</a></div></div></footer>`;
  const shell = (title, description, urlPath, photo, data, body) => `<!doctype html><html lang="es-PE"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="description" content="${escape(description)}" /><meta name="robots" content="index,follow,max-image-preview:large" /><meta name="theme-color" content="#111111" /><title>${escape(title)}</title><link rel="icon" type="image/png" href="/images/xiliana-logo-gold-black.png" /><link rel="stylesheet" href="/styles.css" /><link rel="stylesheet" href="/experience.css?v=orders-1" />${head(title, description, urlPath, photo, data)}</head><body>${header}<main class="seo-product">${body}</main>${footer}<script type="module" src="/order-ui.js?v=orders-1"></script></body></html>`;
  const ordered = [...products].sort((a, b) => categories.indexOf(a.category) - categories.indexOf(b.category) || a.id - b.id);
  let homepage = fs.readFileSync(path.join(output, 'index.html'), 'utf8');
  homepage = homepage.replace('<!-- SEO:HEAD -->', head(config.title, config.description, '/', './images/dress-01.jpg', [business, website, { '@type': 'CollectionPage', '@id': `${base}/#catalogo`, url: `${base}/`, name: config.title, inLanguage: 'es-PE', isPartOf: { '@id': website['@id'] }, mainEntity: itemList(ordered) }]));
  homepage = homepage.replace('<div class="product-grid" id="product-grid"></div>', categoryLinks + `<div class="product-grid" id="product-grid">${cards(ordered)}</div>`);
  const tileProducts = [1, 28, 47, 50, 27, 58];
  homepage = homepage.replace('<div class="category-showcase-grid" id="category-showcase-grid"></div>', `<div class="category-showcase-grid" id="category-showcase-grid">${categories.filter(c => c !== 'Todos').map((c, i) => `<a class="category-tile" href="${categoryPath(c)}"><img src="${image(products.find(p => p.id === tileProducts[i]))}" alt="Vestidos ${escape(c.toLowerCase())}" ${dimensions(products.find(p => p.id === tileProducts[i]))} loading="lazy" /><span>${escape(c)}</span><small>Explorar colección ↗</small></a>`).join('')}</div>`);
  write('index.html', homepage);
  const urls = [{ path: '/', images: [] }];
  for (const category of categories.filter(c => c !== 'Todos')) {
    const items = ordered.filter(p => p.category === category);
    const urlPath = categoryPath(category);
    const title = `Vestidos ${category.toLowerCase()} en Lima | Xiliana Boutique`;
    const description = `Explora ${items.length} vestidos de la colección ${category.toLowerCase()} de Xiliana Boutique en Jesús María, Lima. Prendas únicas y personalizadas, sin talla definida por ahora. Consulta medidas, precios y disponibilidad por WhatsApp.`;
    const data = [business, website, { '@type': 'CollectionPage', url: base + urlPath, name: title, inLanguage: 'es-PE', mainEntity: itemList(items) }, breadcrumbs([['Inicio', '/'], [category, urlPath]])];
    write(urlPath.slice(1) + 'index.html', shell(title, description, urlPath, displayImage(items[0]), data, `<nav class="breadcrumbs" aria-label="Ruta"><a href="/">Inicio</a> / ${escape(category)}</nav><h1>Vestidos ${escape(category.toLowerCase())}</h1><p>Encuentra tu vestido en Jesús María, Lima. Prendas únicas y personalizadas, sin talla definida por ahora. Coordina medidas y disponibilidad directamente con la boutique.</p>${categoryLinks}<div class="product-grid">${cards(items)}</div>`));
    urls.push({ path: urlPath, images: [] });
  }
  for (const p of products) {
    const urlPath = productPath(p);
    const title = `${p.name} | Xiliana Boutique, Lima`;
    const description = `${p.name} en Xiliana Boutique, Jesús María, Lima. Precio de referencia: ${money(p.price)}. Prenda única y personalizada, sin talla definida por ahora. Coordina medidas y entrega por WhatsApp.`;
    const aiNote = restoredImageIds.has(p.id) ? `<p class="product-note">Foto mejorada con IA a partir de una captura del catálogo. Los detalles finos pueden variar; confirma el diseño con la boutique. <a href="${escape(p.image.replace(/^\.\//, '/'))}" target="_blank" rel="noopener">Ver foto original ↗</a></p>` : p.id >= 18 ? '<p class="product-note">Foto original del catálogo de WhatsApp. Consulta una foto de mayor resolución con la boutique.</p>' : '';
    const product = { '@type': 'Product', '@id': base + urlPath + '#producto', url: base + urlPath, name: p.name, description, image: absolute(displayImage(p)), category: p.category, offers: { '@type': 'Offer', url: base + urlPath, priceCurrency: 'PEN', price: p.price.toFixed(2), seller: { '@id': business['@id'] } } };
    const data = [business, website, product, breadcrumbs([['Inicio', '/'], [p.category, categoryPath(p.category)], [p.name, urlPath]])];
    const query = encodeURIComponent(`Hola Xiliana Boutique, quiero consultar por ${p.name}. Entiendo que es una prenda única y personalizada, sin talla definida por ahora. Quisiera coordinar medidas y consultar disponibilidad.`);
    const body = `<nav class="breadcrumbs" aria-label="Ruta"><a href="/">Inicio</a> / <a href="${categoryPath(p.category)}">${escape(p.category)}</a> / ${escape(p.name)}</nav><article class="product-detail"><img src="${image(p)}" alt="${escape(p.name)}" ${dimensions(p)} fetchpriority="high" /><div><p class="eyebrow">Xiliana Boutique · ${escape(p.category)}</p><h1>${escape(p.name)}</h1><p class="price">${money(p.price)}${p.originalPrice ? `<del>${money(p.originalPrice)}</del>` : ''}</p><p>Prenda única y personalizada, sin talla definida por ahora. Medidas y ajustes se coordinan con la boutique. Precio de referencia del catálogo; confirma disponibilidad y entrega antes de comprar.</p>${p.note && !/talla/i.test(p.note) ? `<p>${escape(p.note)}</p>` : ''}${p.imageNote ? `<p class="image-warning">${escape(p.imageNote)}</p>` : ''}${aiNote}<div class="order-shortcuts"><button type="button" class="button button-dark" data-order-id="${p.id}">Solicitar pedido ↗</button><button type="button" class="button order-visit" data-order-id="${p.id}" data-order-visit>Ver en tienda ↗</button></div><noscript><a href="https://wa.me/51930527248?text=${query}">Consultar por WhatsApp ↗</a></noscript><p>Visítanos en Avenida Horacio Urteaga 1438, Tienda 166, Jesús María, Lima.</p><p class="business-hours">Lunes a sábado: 11:00 a. m. – 8:00 p. m.<br />Domingo: cerrado</p><a href="${categoryPath(p.category)}">Ver más vestidos ${escape(p.category.toLowerCase())} ↗</a></div></article>`;
    write(urlPath.slice(1) + 'index.html', shell(title, description, urlPath, displayImage(p), data, body));
    urls.push({ path: urlPath, images: [displayImage(p)] });
  }
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n${urls.map(u => `<url><loc>${escape(base + u.path)}</loc>${u.images.map(i => `<image:image><image:loc>${escape(absolute(i))}</image:loc></image:image>`).join('')}</url>`).join('\n')}\n</urlset>\n`;
  write('sitemap.xml', sitemap);
  write('robots.txt', `User-agent: *\nAllow: /\n\nSitemap: ${base}/sitemap.xml\n`);
  write('404.html', `<!doctype html><html lang="es-PE"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>Página no encontrada | Xiliana Boutique</title><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/experience.css"></head><body>${header}<main class="seo-product"><h1>No encontramos esta página.</h1><p>Explora nuestra colección de vestidos o consulta con la boutique.</p><a class="button button-dark" href="/">Volver al catálogo ↗</a></main>${footer}</body></html>`);
  console.log(`SEO preparado para ${base}: ${urls.length} páginas, sitemap de imágenes y robots.txt.`);
};
