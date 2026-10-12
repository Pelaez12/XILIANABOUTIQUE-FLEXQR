"""Aplicar la prioridad Gala > largo sin reconstruir fotos ni precios."""
from collections import Counter
from pathlib import Path
import copy
import json
import re

from categoria_producto import categoria_por_nombre

root = Path(__file__).resolve().parents[1]
audit_dir = root / 'review/categorias-2026-10-12'
audit_dir.mkdir(exist_ok=True)
source = root / 'products.js'
text = source.read_text(encoding='utf-8-sig')
pattern = r'export const products = ([\s\S]*?);\s*export const categories'
match = re.search(pattern, text)
products = json.loads(match[1])
before = copy.deepcopy(products)
backup = audit_dir / 'productos-antes.json'
if not backup.exists():
    backup.write_text(json.dumps(before, ensure_ascii=False, indent=2), encoding='utf-8')

for product in products:
    product['category'] = categoria_por_nombre(product['name'], product['category'])

# Verificar que la modificación se limita a la categoría.
assert len(before) == len(products)
for old, new in zip(before, products):
    assert {k:v for k,v in old.items() if k != 'category'} == {k:v for k,v in new.items() if k != 'category'}
assert not any(p['category'] == 'Largos' and re.search(r'\bgala\b', p['name'], re.I) for p in products)

serialized = json.dumps(products, ensure_ascii=False, indent=2)
source.write_text(text[:match.start(1)] + serialized + text[match.end(1):], encoding='utf-8')
(root / 'review/publicados-confirmados.json').write_text(serialized, encoding='utf-8')

confirmed_file = root / 'review/catalogo-whatsapp-2026-10-12/confirmados.json'
confirmed = json.loads(confirmed_file.read_text(encoding='utf-8'))
for item in confirmed['confirmados']:
    item['categoria'] = categoria_por_nombre(item['nombre'], item['categoria'])
confirmed_file.write_text(json.dumps(confirmed, ensure_ascii=False, indent=2), encoding='utf-8')

by_id = {p['id']:p for p in products}
groups_file = root / 'review/importacion-2026-10-10/verificacion.json'
groups = json.loads(groups_file.read_text(encoding='utf-8'))
for group in groups['modelos_nuevos']:
    if group.get('productId') in by_id:
        group['categoria'] = by_id[group['productId']]['category']
groups_file.write_text(json.dumps(groups, ensure_ascii=False, indent=2), encoding='utf-8')

report_file = root / 'review/catalogo-whatsapp-2026-10-12/REVISION.html'
report = report_file.read_text(encoding='utf-8')
for product in products:
    if product.get('importGroup'):
        report = re.sub(r'(<small>XL-' + str(product['id']) + r' · ' + re.escape(product['importGroup']) + r' · )[^<]+(</small>)', lambda m:m[1]+product['category']+m[2], report)
report_file.write_text(report, encoding='utf-8')

baseline = json.loads(backup.read_text(encoding='utf-8'))
initial_by_id = {p['id']:p for p in baseline}
changes = [dict(id=p['id'], nombre=p['name'], antes=initial_by_id[p['id']]['category'], ahora=p['category']) for p in products if p['id'] in initial_by_id and initial_by_id[p['id']]['category'] != p['category']]
summary = dict(fecha='2026-10-12', regla='La palabra gala tiene prioridad sobre largo. Se conservan Bandage y Liquidación.', cambios=changes, totales=dict(Counter(p['category'] for p in products)), total_prendas=len(products), total_fotos=sum(len(p['photos']) for p in products), verificacion='Solo cambió la categoría; nombres, precios, fotografías, orden de galerías e identificadores se conservaron.')
(audit_dir / 'resultado.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(cambios=len(changes), totales=summary['totales'], prendas=summary['total_prendas'], fotos=summary['total_fotos']), ensure_ascii=False))
