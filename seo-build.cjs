const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const config = require('./site-config.json');
const base = config.url.replace(/\/$/, '');
const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const json = value => JSON.stringify(value).replace(/</g, '\\u003c');
const money = value => value == null ? 'Precio por confirmar' : new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(value);
const absolute = relative => new URL(relative.replace(/^\.\//, '/'), base).href;
const loadModule = file => import('data:text/javascript;base64,' + fs.readFileSync(path.join(__dirname, file)).toString('base64'));

module.exports = async function buildSEO(output) {
  if (new URL(base).protocol !== 'https:') throw new Error('El dominio público debe usar HTTPS.');
  const { products, categories } = await loadModule('products.js');
  const { displayImage, productPath, categoryPath, featuredCategoryIds, slug } = await loadModule('catalog-utils.js');
  const { galleryMarkup } = await loadModule('gallery.js');
  const { recommendProducts } = await loadModule('recommendations.js');
  const dimensions = p => p.photos.length ? `width="${p.photos[0].width}" height="${p.photos[0].height}"` : 'width="900" height="1200"';
  const image = product => displayImage(product).replace(/^\.\//, '/');
  const business = {
    '@type': 'ClothingStore', '@id': `${base}/#boutique`, name: config.name, url: `${base}/`,
    telephone: config.telephone, email: config.email,
    openingHoursSpecification: [{ '@type': 'OpeningHoursSpecification', dayOfWeek: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], opens: '11:00', closes: '20:00' }],
    logo: absolute('./images/xiliana-logo-gold-black.png'), image: absolute('./images/xiliana-logo-gold-black.png'),
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
  const discount = p => p.originalPrice > p.price && p.price != null ? Math.round((1-p.price/p.originalPrice)*100) : 0;
  const isSale = p => p.category === 'Liquidación' || discount(p) > 0;
  const saleCategory = p => escape(p.category);
  const cards = items => items.map(p => `<article class="product-card${isSale(p) ? ' is-sale' : ''}" data-name="${escape(p.name)}"><a class="product-open" href="${productPath(p)}" data-id="${p.id}" aria-label="Ver ${escape(p.name)}"><span class="product-image"><img src="${image(p)}" alt="${escape(p.name)}" ${dimensions(p)} loading="lazy" decoding="async" /></span><span class="product-meta"><span class="category">${saleCategory(p)}</span><span class="view-link">Ver producto ↗</span></span><h2 class="product-name">${escape(p.name)}</h2><span class="price${isSale(p) ? ' price--sale' : ''}">${money(p.price)}${p.originalPrice ? `<del>${money(p.originalPrice)}</del>` : ''}</span></a></article>`).join('');
  const itemList = items => ({ '@type': 'ItemList', itemListElement: items.map((p, i) => ({ '@type': 'ListItem', position: i + 1, name: p.name, url: base + productPath(p) })) });
  const recommendations = current => {
    if (/^(Bralette|Falda|Top)\b/i.test(current.name)) return '';
    const suggestions = recommendProducts(current, products);
    if (!suggestions.length) return '';
    return `<section class="product-recommendations" aria-labelledby="recommendations-title"><div class="recommendations-heading"><div><h2 id="recommendations-title">Si te gustó este vestido…</h2><p>Estos también te pueden encantar. Encuentra otro look que vaya contigo.</p></div><a href="${categoryPath(current.category)}">Explorar ${escape(current.category.toLowerCase())} ↗</a></div><div class="recommendations-navigation"><p id="recommendations-hint">Desliza para descubrir más vestidos ↔</p><div class="recommendations-arrows" hidden><button type="button" data-recommendations-prev aria-label="Ver vestidos anteriores" aria-controls="recommendations-track">←</button><button type="button" data-recommendations-next aria-label="Ver más vestidos recomendados" aria-controls="recommendations-track">→</button></div></div><div class="recommendations-grid" id="recommendations-track" tabindex="0" role="region" aria-label="Vestidos recomendados, fila desplazable" aria-describedby="recommendations-hint">${suggestions.map(({product: p, reason}) => `<article class="product-card recommendation-card"><a class="product-open" href="${productPath(p)}" aria-label="Ver ${escape(p.name)}"><span class="product-image"><img src="${image(p)}" alt="${escape(p.name)}, vista de frente" ${dimensions(p)} loading="lazy" decoding="async" /></span><span class="recommendation-reason">${escape(reason)}</span><h3 class="product-name">${escape(p.name)}</h3><span class="price${isSale(p) ? ' price--sale' : ''}">${money(p.price)}${p.originalPrice ? `<del>${money(p.originalPrice)}</del>` : ''}</span><span class="recommendation-link">Descubrir vestido ↗</span></a></article>`).join('')}</div><script type="module" src="/recommendations-carousel.js"></script></section>`;
  };
  const breadcrumbs = entries => ({ '@type': 'BreadcrumbList', itemListElement: entries.map(([name, url], i) => ({ '@type': 'ListItem', position: i + 1, name, item: base + url })) });
  const header = `<header class="site-header"><a class="brand-logo" href="/" aria-label="Xiliana Boutique, inicio"><img src="/images/xiliana-logo-gold-black.png" alt="Xiliana Boutique by Antonio Grau" width="188" height="68" /></a><nav aria-label="Navegación principal"><a class="offers-nav" href="/colecciones/liquidacion/">Ofertas</a><a href="/#coleccion">Colección</a><a href="/colecciones/accesorios/">Accesorios</a><a href="/#asesoria">Asesoría</a><a href="/#visitanos">Visítanos</a><a href="https://wa.me/51930527248">WhatsApp ↗</a></nav></header>`;
  const footer = `<footer class="site-footer" id="contacto"><div class="footer-main"><a class="brand-logo" href="/"><img src="/images/xiliana-logo-gold-black.png" alt="Xiliana Boutique" loading="lazy" /></a><p>Solo una vida para lucirte.</p><a href="/#visitanos">Visita nuestra boutique ↗</a></div>${fs.readFileSync(path.join(__dirname, "contact-block.html"), "utf8")}<div class="footer-bottom"><small>Prendas únicas y personalizadas. Medidas, precios y disponibilidad se coordinan con Xiliana Boutique.</small><div class="creator-credit"><span>Sitio creado por <strong>FLEXCOREOS</strong></span><a href="tel:+51992272521">¿Quieres un sitio así? Llámanos al <strong>992 272 521</strong> ↗</a></div></div></footer>${fs.readFileSync(path.join(__dirname, "whatsapp-help.html"), "utf8")}`;
  const shell = (title, description, urlPath, photo, data, body) => `<!doctype html><html lang="es-PE"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="description" content="${escape(description)}" /><meta name="robots" content="index,follow,max-image-preview:large" /><meta name="theme-color" content="#111111" /><title>${escape(title)}</title><link rel="icon" type="image/png" href="/images/xiliana-logo-gold-black.png" /><link rel="stylesheet" href="/styles.css" /><link rel="stylesheet" href="/experience.css?v=sale-tile-darkred-20261022" />${head(title, description, urlPath, photo, data)}</head><body>${header}<main class="seo-product">${body}</main>${footer}<script type="module" src="/order-ui.js?v=sale-tile-20261022"></script><script type="module" src="/gallery.js"></script><script type="module" src="/brand-intro.js?v=sale-tile-20261022"></script><script type="module" src="/collection-search.js"></script></body></html>`;
  const ordered = products.filter(p => !p.photoPending).sort((a, b) => categories.indexOf(a.category) - categories.indexOf(b.category) || a.id - b.id);
  let homepage = fs.readFileSync(path.join(output, 'index.html'), 'utf8');
  homepage = homepage.replace('<!-- CONTACT:VISIT -->', fs.readFileSync(path.join(__dirname, 'contact-block.html'), 'utf8'));
  homepage = homepage.replace('<!-- SEO:HEAD -->', head(config.title, config.description, '/', './images/xiliana-logo-gold-black.png', [business, website, { '@type': 'CollectionPage', '@id': `${base}/#catalogo`, url: `${base}/`, name: config.title, inLanguage: 'es-PE', isPartOf: { '@id': website['@id'] }, mainEntity: itemList(ordered) }]));
  const pendientes = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/accessories.json'), 'utf8'));
  const showcaseCategories = categories.filter(c => c !== 'Todos' && c !== 'Liquidación');
  const labels = { Gala: 'Vestidos de gala', Largos: 'Vestidos largos', Cortos: 'Vestidos cortos' };
  const tiles = showcaseCategories.map(category => {
    const product = products.find(p => p.id === featuredCategoryIds[category]);
    return { label: labels[category] || category, href: categoryPath(category), photo: image(product), dimensions: dimensions(product), count: category === 'Cortos' ? 38 : products.filter(p => p.category === category).length };
  });
  tiles.push({ label: 'Accesorios', subtitle: 'De fantasía', href: '/colecciones/accesorios/', photo: pendientes[0].fotos_web[0].replace(/^\.\//, '/'), dimensions: 'width="497" height="1049"', count: pendientes.length, kind: 'accessories' });
  const saleCover = products.find(p => p.id === 125 && p.category === 'Liquidación') || products.find(p => p.category === 'Liquidación');
  tiles.push({ label: 'Vestidos en liquidación', saleTile: true, href: categoryPath('Liquidación'), photo: image(saleCover), dimensions: dimensions(saleCover), count: products.filter(p => p.category === 'Liquidación').length, kind: 'complement', action: 'Ver ofertas' });
  const tilesMarkup = tiles.map(tile => `<a class="category-tile${tile.kind ? ' category-tile--' + tile.kind : ''}" href="${tile.href}" aria-label="Explorar ${escape(tile.label)}, ${tile.count} modelos"><img src="${tile.photo}" alt="" ${tile.dimensions} loading="lazy" decoding="async" /><span>${tile.saleTile ? '<em class="liquidation-tile-lead">Vestidos en</em><i class="liquidation-tile-rule" aria-hidden="true"></i><strong class="liquidation-tile-word">LIQUIDACIÓN</strong>' : escape(tile.label)}${tile.subtitle ? `<em class="category-tile-subtitle">${escape(tile.subtitle)}</em>` : ''}</span><small>${tile.count} modelos · ${tile.action || 'Ver colección'} <b aria-hidden="true">↗</b></small></a>`).join('');
  homepage = homepage.replace('<div class="category-showcase-grid" id="category-showcase-grid"></div>', `<div class="category-showcase-grid" id="category-showcase-grid">${tilesMarkup}</div>`);
  write('index.html', homepage);
  const urls = [{ path: '/', images: [] }];
  for (const category of categories.filter(c => c !== 'Todos')) {
    const items = ordered.filter(p => p.category === category);
    const collectionNames = {Gala:'GALA DRESSES',Largos:'VESTIDOS LARGOS','Cortos con brillo':'CORTOS CON BRILLO',Cortos:'VESTIDOS CORTOS',Bandage:'BANDAGE',Liquidación:'OFERTAS · LIQUIDACIÓN'};
    const collectionCopy = {Gala:'Para noches que merecen una entrada inolvidable. Encuentra tu favorito y luce tu propia forma de brillar.',Largos:'Movimiento, encanto y un look muy tuyo. Descubre el vestido que te acompañará en tu próxima celebración.','Cortos con brillo':'Un toque de brillo y mucha actitud. Elige el look para disfrutar tu noche y sentirte preciosa.',Cortos:'Coquetos, con personalidad y listos para tu próximo plan. Encuentra el que va contigo.',Bandage:'Looks con actitud para salir sintiéndote fabulosa. Elige tu favorito y hazlo tuyo.',Liquidación:'Descubre vestidos con descuento. Compara el precio anterior con el actual y consulta disponibilidad con la boutique.'};
    const urlPath = categoryPath(category);
    const title = `Vestidos ${category.toLowerCase()} en Lima | Xiliana Boutique`;
    const description = `Explora ${items.length} vestidos de la colección ${category.toLowerCase()} de Xiliana Boutique en Jesús María, Lima. Prendas únicas y personalizadas. Consulta medidas, precios y disponibilidad por WhatsApp.`;
    const data = [business, website, { '@type': 'CollectionPage', url: base + urlPath, name: title, inLanguage: 'es-PE', mainEntity: itemList(items) }, breadcrumbs([['Inicio', '/'], [category, urlPath]])];
    write(urlPath.slice(1) + 'index.html', shell(title, description, urlPath, items.length ? displayImage(items[0]) : './images/xiliana-logo-gold-black.png', data, `<nav class="breadcrumbs" aria-label="Ruta"><a href="/">Inicio</a> / ${escape(category)}</nav><header class="collection-heading"><h1>${escape(collectionNames[category])}</h1><p>${escape(collectionCopy[category])}</p></header>${categoryLinks}<div class="collection-tools"><p class="collection-count" id="collection-count" role="status" aria-live="polite">${items.length} modelos en esta colección</p><div class="collection-search" hidden><label for="collection-query">Encuentra tu vestido</label><div class="collection-search-field"><input id="collection-query" type="search" placeholder="Buscar por nombre o color" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="collection-suggestions" /><span aria-hidden="true">⌕</span></div><ul id="collection-suggestions" class="collection-suggestions" role="listbox" aria-label="Vestidos sugeridos" hidden></ul></div></div><div class="product-grid collection-products" id="collection-products">${cards(items)}</div><div class="collection-empty" hidden><h2>No encontramos ese vestido.</h2><p>Prueba con otro nombre o color, o vuelve a ver la colección completa.</p><button type="button" class="button button-dark" id="clear-collection-search">Ver todos los modelos</button></div>`));
    urls.push({ path: urlPath, images: [] });
  }
  if (!pendientes.length || new Set(pendientes.map(p => p.numero_visible)).size !== pendientes.length || new Set(pendientes.map(p => `${p.nombre}\u0000${p.precio_pen}\u0000${p.numero_visible}`)).size !== pendientes.length) throw new Error('Inventario de accesorios vacío o con identificadores repetidos');
  const pendientesPath = '/colecciones/accesorios/';
  const accessoryPath = p => `/accesorios/${p.numero_visible}-${slug(p.nombre)}/`;
  const pendientesTitle = 'Accesorios en Lima | Xiliana Boutique';
  const pendientesDescription = `Explora ${pendientes.length} accesorios de Xiliana Boutique con sus fotos originales, nombres y precios verificados.`;
  const pendientesCards = pendientes.map((p, i) => {
    const photos = (Array.isArray(p.fotos_web) ? p.fotos_web : []).map(photo => `/${photo.replace(/^\.\//, '')}`);
    if (!photos.length) throw new Error(`El accesorio ${p.nombre} no tiene foto web`);
    return `<article class="product-card accessory-card" data-name="${escape(p.nombre)}"><a class="product-open" href="${accessoryPath(p)}" aria-label="Ver ${escape(p.nombre)}"><span class="product-image accessory-image"><img src="${photos[0]}" alt="${escape(p.nombre)}" loading="lazy" decoding="async" /></span><span class="product-meta"><span class="category">Accesorios</span><span class="view-link">Ver accesorio ↗</span></span><h2 class="product-name">${escape(p.nombre)}</h2><span class="price">${money(p.precio_pen)}</span></a></article>`;
  }).join('');
  const pendientesData = [business, website, { '@type': 'CollectionPage', url: base + pendientesPath, name: pendientesTitle, inLanguage: 'es-PE', mainEntity: { '@type': 'ItemList', itemListElement: pendientes.map((p, i) => ({ '@type': 'ListItem', position: i + 1, name: p.nombre })) } }, breadcrumbs([['Inicio', '/'], ['Accesorios', pendientesPath]])];
  const pendientesConFoto = pendientes.filter(p => Array.isArray(p.fotos_web) && p.fotos_web.length).length;
  write(pendientesPath.slice(1) + 'index.html', shell(pendientesTitle, pendientesDescription, pendientesPath, pendientesConFoto ? pendientes.find(p => Array.isArray(p.fotos_web) && p.fotos_web.length).fotos_web[0] : './images/xiliana-logo-gold-black.png', pendientesData, `<nav class="breadcrumbs" aria-label="Ruta"><a href="/">Inicio</a> / Accesorios</nav><header class="collection-heading"><h1>ACCESORIOS</h1><p>El detalle que completa tu look. Abre cualquier modelo para ver sus fotos y consultar disponibilidad.</p></header><div class="collection-tools"><p class="collection-count">${pendientes.length} modelos en esta colección</p></div><div class="product-grid collection-products accessories-products">${pendientesCards}</div>`));
  urls.push({ path: pendientesPath, images: [] });
  write('_redirects', '/colecciones/pendientes/ /colecciones/accesorios/ 301\n');
  for (const p of pendientes) {
    const urlPath = accessoryPath(p);
    const photos = p.fotos_web.map((src, i) => ({ src, view: `Foto ${i + 1}` }));
    const galleryProduct = { name: p.nombre, image: photos[0].src, photos };
    const title = `${p.nombre} | Accesorios Xiliana Boutique`;
    const description = `${p.nombre} en Xiliana Boutique, Jesús María, Lima. Precio de referencia: ${money(p.precio_pen)}. Consulta disponibilidad y entrega por WhatsApp.`;
    const product = { '@type': 'Product', '@id': base + urlPath + '#producto', url: base + urlPath, name: p.nombre, description, image: photos.map(photo => absolute(photo.src)), category: 'Accesorios', offers: { '@type': 'Offer', url: base + urlPath, priceCurrency: 'PEN', price: Number(p.precio_pen).toFixed(2), seller: { '@id': business['@id'] } } };
    const data = [business, website, product, breadcrumbs([['Inicio', '/'], ['Accesorios', pendientesPath], [p.nombre, urlPath]])];
    const query = encodeURIComponent(`Hola Xiliana Boutique, quiero consultar por el accesorio ${p.nombre} (código ${p.numero_visible}) a ${money(p.precio_pen)}. ¿Está disponible?`);
    const body = `<nav class="breadcrumbs" aria-label="Ruta"><a href="/">Inicio</a> / <a href="${pendientesPath}">Accesorios</a> / ${escape(p.nombre)}</nav><article class="product-detail accessory-detail">${galleryMarkup(galleryProduct)}<div><p class="eyebrow">Xiliana Boutique · Accesorios</p><h1>${escape(p.nombre)}</h1><p class="price">${money(p.precio_pen)}</p><div class="product-availability"><p><strong>Disponibilidad:</strong> consulta si este accesorio está disponible en tienda.</p><p><strong>Entrega:</strong> coordinamos recojo en boutique o envío a Lima y provincia por WhatsApp.</p></div><a class="button button-dark accessory-whatsapp" href="https://wa.me/51930527248?text=${query}" target="_blank" rel="noopener noreferrer">Consultar por WhatsApp ↗</a><p>Visítanos en Avenida Horacio Urteaga 1438, Tienda 166, Centro Comercial El Rey, Jesús María, Lima, Perú.</p><p class="business-hours">Lunes a sábado: 11:00 a. m. – 8:00 p. m.<br />Domingos: previa cita</p><a href="${pendientesPath}">Ver todos los accesorios ↗</a></div></article>`;
    write(urlPath.slice(1) + 'index.html', shell(title, description, urlPath, photos[0].src, data, body));
    urls.push({ path: urlPath, images: photos.map(photo => photo.src) });
  }
  for (const p of products) {
    const urlPath = productPath(p);
    const title = `${p.name} | Xiliana Boutique, Lima`;
    const description = `${p.name} en Xiliana Boutique, Jesús María, Lima. Precio de referencia: ${money(p.price)}. Prenda única y personalizada. Coordina medidas y entrega por WhatsApp.`;
    const photoNote = !p.photos.length && p.id >= 18 ? '<p class="product-note">Foto real pendiente. Consulta el modelo con la boutique.</p>' : '';
    const product = { '@type': 'Product', '@id': base + urlPath + '#producto', url: base + urlPath, name: p.name, description, ...(p.photos.length ? {image:p.photos.map(photo => absolute(photo.src))} : {}), category: p.category, ...(p.price != null ? {offers: { '@type': 'Offer', url: base + urlPath, priceCurrency: 'PEN', price: p.price.toFixed(2), seller: { '@id': business['@id'] } }} : {}) };
    const data = [business, website, product, breadcrumbs([['Inicio', '/'], [p.category, categoryPath(p.category)], [p.name, urlPath]])];
    const query = encodeURIComponent(`Hola Xiliana Boutique, quiero consultar por ${p.name}. Entiendo que es una prenda única y personalizada. Quisiera coordinar medidas y consultar disponibilidad.`);
    const body = `<nav class="breadcrumbs" aria-label="Ruta"><a href="/">Inicio</a> / <a href="${categoryPath(p.category)}">${escape(p.category)}</a> / ${escape(p.name)}</nav><article class="product-detail">${galleryMarkup(p)}<div><p class="eyebrow">Xiliana Boutique · ${saleCategory(p)}</p><h1>${escape(p.name)}</h1><p class="price${isSale(p) ? ' price--sale' : ''}">${money(p.price)}${p.originalPrice ? `<del>${money(p.originalPrice)}</del>` : ''}${discount(p) ? `<span class="discount-label">Ahorras ${discount(p)}%</span>` : ''}</p><div class="product-availability"><p><strong>Disponibilidad:</strong> consulta si este modelo está en tienda.</p><p><strong>Medidas y ajustes:</strong> te asesoramos antes de comprar. Confirma con la boutique las medidas disponibles y si admite ajustes.</p><p>Envíos a Lima y provincia. Entrega y costo se confirman por WhatsApp.</p></div>${p.note && !/talla/i.test(p.note) ? `<p>${escape(p.note)}</p>` : ''}${p.imageNote ? `<p class="image-warning">${escape(p.imageNote)}</p>` : ''}${photoNote}<div class="order-shortcuts"><button type="button" class="button button-dark" data-order-id="${p.id}">Consultar disponibilidad ↗</button><button type="button" class="button order-visit" data-order-id="${p.id}" data-order-visit>Ver en tienda ↗</button></div><noscript><a href="https://wa.me/51930527248?text=${query}">Consultar por WhatsApp ↗</a></noscript><p>Visítanos en Avenida Horacio Urteaga 1438, Tienda 166, Centro Comercial El Rey, Jesús María, Lima, Perú.</p><p class="business-hours">Lunes a sábado: 11:00 a. m. – 8:00 p. m.<br />Domingos: previa cita</p><a href="${categoryPath(p.category)}">Explorar ${escape(p.category.toLowerCase())} ↗</a></div></article>`;
    write(urlPath.slice(1) + 'index.html', shell(title, description, urlPath, displayImage(p), data, body + recommendations(p)));
    urls.push({ path: urlPath, images: p.photos.map(photo => photo.src) });
  }
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n${urls.map(u => `<url><loc>${escape(base + u.path)}</loc>${u.images.map(i => `<image:image><image:loc>${escape(absolute(i))}</image:loc></image:image>`).join('')}</url>`).join('\n')}\n</urlset>\n`;
  write('sitemap.xml', sitemap);
  write('robots.txt', `User-agent: *\nAllow: /\n\nSitemap: ${base}/sitemap.xml\n`);
  write('404.html', `<!doctype html><html lang="es-PE"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>Página no encontrada | Xiliana Boutique</title><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/experience.css"></head><body>${header}<main class="seo-product"><h1>No encontramos esta página.</h1><p>Explora nuestra colección de vestidos o consulta con la boutique.</p><a class="button button-dark" href="/">Volver al catálogo ↗</a></main>${footer}</body></html>`);
  console.log(`SEO preparado para ${base}: ${urls.length} páginas, sitemap de imágenes y robots.txt.`);
};
