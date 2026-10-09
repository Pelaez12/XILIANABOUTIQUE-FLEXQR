from pathlib import Path
import re,json
r=Path(__file__).resolve().parents[1]
p=r/'seo-build.cjs'; t=p.read_text(encoding='utf-8')
t=t.replace("offers: { '@type': 'Offer', url: base + urlPath, priceCurrency: 'PEN', price: p.price.toFixed(2), seller: { '@id': business['@id'] } }", "...(p.price != null ? {offers: { '@type': 'Offer', url: base + urlPath, priceCurrency: 'PEN', price: p.price.toFixed(2), seller: { '@id': business['@id'] } }} : {})")
p.write_text(t,encoding='utf-8')
p=r/'validate-seo.cjs';t=p.read_text(encoding='utf-8')
declarations="const productSource = fs.readFileSync(path.join(__dirname, 'products.js'), 'utf8');\nconst products = JSON.parse(productSource.match(/export const products = ([\\s\\S]*?);\\s*export const categories/)[1]);\n"
t=t.replace(declarations,'')
t=t.replace('const expectedPages = 103; // Inicio, 6 categorías y 96 productos confirmados.',declarations+'const expectedPages = 7 + products.length;')
p.write_text(t,encoding='utf-8')
p=r/'review/publicar-confirmados.py';t=p.read_text(encoding='utf-8')
if 'actualizar-2026-10-08.py' not in t:
 t+="\n# Apply the subsequent owner corrections and attachment audit after rebuilding.\nimport runpy\nrunpy.run_path(str(r/'review/actualizar-2026-10-08.py'))\n"
p.write_text(t,encoding='utf-8')
print('Soporte de precios pendientes y regeneración actualizado.')
