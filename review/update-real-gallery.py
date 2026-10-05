from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
file=root/'main.js'; s=file.read_text(encoding='utf-8')
s=s.replace('displayImage, aiImageIds, productPath','displayImage, productPath')
s=s.replace("import './order-ui.js';", "import './order-ui.js';\nimport { galleryMarkup } from './gallery.js';")
s=s.replace("product.id > 17 && !aiImageIds.has(product.id)", "product.id > 17 && !product.photos.length")
s=re.sub(r'dialogContent.innerHTML = `<div class="dialog-image[\s\S]*?</div><div class="dialog-info">', 'dialogContent.innerHTML = `${galleryMarkup(product)}<div class="dialog-info">',s,count=1)
s=re.sub(r'\$\{aiImageIds.has\(product.id\)[\s\S]*?: \'\'\}', '${!product.photos.length && product.id > 17 ? \'<p class="product-note">Captura original del catálogo. Consulta más fotos con la boutique.</p>\' : \'\'}',s,count=1)
# Portadas de las categorías con fotos reales identificadas y precio ya conocido.
s=s.replace('p.id === 28','p.id === 24').replace('p.id === 47','p.id === 39').replace('p.id === 50','p.id === 35').replace('p.id === 27','p.id === 14').replace('p.id === 58','p.id === 17')
file.write_text(s,encoding='utf-8')
file=root/'seo-build.cjs'; s=file.read_text(encoding='utf-8')
s=s.replace('displayImage, restoredImageIds, productPath','displayImage, productPath')
s=s.replace("  const dimensions = p => {", "  const { galleryMarkup } = await loadModule('gallery.js');\n  const dimensions = p => { if (p.photos.length) return `width=\"${p.photos[0].width}\" height=\"${p.photos[0].height}\"`; ")
s=s.replace('/order-ui.js?v=orders-1','/order-ui.js?v=real-photos-1').replace('experience.css?v=orders-1','experience.css?v=real-photos-1')
s=s.replace('<script type="module" src="/order-ui.js?v=real-photos-1"></script>', '<script type="module" src="/order-ui.js?v=real-photos-1"></script><script type="module" src="/gallery.js"></script>')
s=s.replace('const tileProducts = [1, 28, 47, 50, 27, 58]','const tileProducts = [1, 24, 39, 35, 14, 17]')
s=re.sub(r'    const aiNote = .*?;\n', '    const photoNote = !p.photos.length && p.id >= 18 ? \'<p class="product-note">Captura original del catálogo. Consulta más fotos con la boutique.</p>\' : \'\';\n',s,count=1)
s=s.replace('image: absolute(displayImage(p)), category:', 'image: (p.photos.length ? p.photos.map(photo => absolute(photo.src)) : [absolute(displayImage(p))]), category:')
s=s.replace('<article class="product-detail"><img src="${image(p)}" alt="${escape(p.name)}" ${dimensions(p)} fetchpriority="high" />', '<article class="product-detail">${galleryMarkup(p)}')
s=s.replace('${aiNote}', '${photoNote}')
s=s.replace('images: [displayImage(p)]', 'images: p.photos.length ? p.photos.map(photo => photo.src) : [displayImage(p)]')
file.write_text(s,encoding='utf-8')
file=root/'validate-seo.cjs'; s=file.read_text(encoding='utf-8')
s=s.replace('let schemas = 0;', 'let schemas = 0;\nlet galleryPhotos = 0;')
s=s.replace('(ai|model)', '(ai|model|faithful[^.]*)')
s=s.replace('    schemas++;', '''    schemas++;
    for (const product of data['@graph'].filter(item => item['@type'] === 'Product')) {
      assert(Array.isArray(product.image) && product.image.length > 0);
      galleryPhotos += product.image.length;
      for (const photo of product.image) {
        const target = path.join(output, decodeURIComponent(new URL(photo).pathname));
        assert(fs.existsSync(target), `Foto de galería ausente: ${photo}`);
      }
    }''')
s=s.replace("assert.equal((sitemap.match(/<image:loc>/g) || []).length, 58);", "assert.equal((sitemap.match(/<image:loc>/g) || []).length, galleryPhotos);")
s=s.replace("console.log('SEO validado: 65 páginas, 65 bloques JSON-LD, 58 imágenes de sitemap y todos los enlaces locales presentes.');", "console.log(`SEO validado: 65 páginas, 65 bloques JSON-LD, ${galleryPhotos} imágenes de sitemap y todos los enlaces locales presentes.`);")
file.write_text(s,encoding='utf-8')
file=root/'index.html'; s=file.read_text(encoding='utf-8')
s=re.sub(r'experience.css\?v=[^"\s]+','experience.css?v=real-photos-1',s)
s=re.sub(r'main.js\?v=[^"\s]+','main.js?v=real-photos-1',s)
file.write_text(s,encoding='utf-8')
file=root/'experience.css'; s=file.read_text(encoding='utf-8')
s+='''
/* Fotografías originales: mostrar el vestido completo y sus otras vistas. */
.product-gallery{min-width:0;background:#fff}
.gallery-main{display:block;width:100%;height:auto;aspect-ratio:3/4;object-fit:contain;background:#fff}
.gallery-thumbs{display:flex;gap:10px;overflow-x:auto;padding:14px 3px 5px;scrollbar-width:thin}
.gallery-thumbs button{flex:0 0 66px;padding:3px;border:1px solid #ddd;background:#fff}
.gallery-thumbs button[aria-pressed=true]{border:2px solid #97763d;padding:2px}
.gallery-thumbs button:focus-visible{outline:2px solid #97763d;outline-offset:2px}
.gallery-thumbs img{width:100%;height:82px;object-fit:contain}
.gallery-count{font-size:12px;color:#655f57;margin:7px 0 14px}
.product-image:has(img[src*="productos-reales/"]){aspect-ratio:3/4;background:#fff}
.product-image img[src*="productos-reales/"]{object-fit:contain;transform:none}
#dialog-content>.product-gallery{padding:16px;align-self:start}
@media(max-width:640px){#dialog-content .gallery-main{max-height:60dvh;aspect-ratio:3/4}.gallery-thumbs button{flex-basis:56px}.gallery-thumbs img{height:70px}}
'''
file.write_text(s,encoding='utf-8')
print('Galerías y publicación actualizadas')
