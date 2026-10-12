"""Incorporar solo coincidencias visuales verificadas en WhatsApp. Repetible."""
from pathlib import Path
import hashlib
import html
import json
import re
import shutil
import unicodedata
from PIL import Image
from categoria_producto import categoria_por_nombre

root = Path(__file__).resolve().parents[1]
audit_dir = root / 'review/catalogo-whatsapp-2026-10-12'
confirmed = json.loads((audit_dir / 'confirmados.json').read_text(encoding='utf-8'))
groups_file = root / 'review/importacion-2026-10-10/verificacion.json'
audit = json.loads(groups_file.read_text(encoding='utf-8'))
groups = {g['grupo']: g for g in audit['modelos_nuevos']}
source = root / 'products.js'
text = source.read_text(encoding='utf-8-sig')
products = json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)[1])
categories = json.loads(re.search(r'export const categories = ([\s\S]*?);', text)[1])
by_id = {p['id']: p for p in products}
backup = audit_dir / 'productos-antes.json'
if not backup.exists():
    backup.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding='utf-8')

for item in confirmed['confirmados']:
    group = groups[item['grupo']]
    ident = 148 + int(item['grupo'].split('-')[1])
    previous = by_id.get(ident)
    assert previous is None or previous.get('importGroup') == item['grupo'], f'ID ocupado: {ident}'
    assert item['precio'] > 0
    photos = []
    directory = root / f'images/productos-reales/XL-{ident:03}'
    directory.mkdir(parents=True, exist_ok=True)
    for position, shot in enumerate(group['fotos'], 1):
        original = root / shot['path'].removeprefix('./')
        target = directory / f'{position:02}-N{shot["n"]:03}.jpeg'
        shutil.copy2(original, target)
        with Image.open(target) as image:
            width, height = image.size
        photos.append(dict(src='./' + target.relative_to(root).as_posix(), width=width,
                           height=height, view=shot['vista'],
                           sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                           sourceAttachment=shot['path']))
    assert photos[0]['view'] == 'Frente'
    assert len({p['sha256'] for p in photos}) == len(photos)
    product = dict(id=ident, name=item['nombre'], category=categoria_por_nombre(item['nombre'], item['categoria']),
                   price=item['precio'], photos=photos, image=photos[0]['src'],
                   photoPending=False, importGroup=item['grupo'],
                   note='Elige tus accesorios favoritos y dale tu toque a este diseño. Podemos orientarte sobre medidas, ajustes y disponibilidad.',
                   catalogName=item.get('nombre_catalogo', item['nombre']),
                   priceSource=dict(tipo=item.get('fuente_tipo', 'WhatsApp Web'), telefono='+51 930 527 248',
                                    fecha=confirmed['fecha'], evidencia=item['evidencia']))
    if item.get('precio_regular'):
        product['originalPrice'] = item['precio_regular']
    if item.get('codigo_catalogo'):
        product['catalogCode'] = item['codigo_catalogo']
    if item.get('descripcion_catalogo'):
        product['catalogDescription'] = item['descripcion_catalogo']
    by_id[ident] = product
    group.update(nombre_catalogo=product['catalogName'], nombre_web=product['name'],
                 precio=product['price'], categoria=product['category'], productId=ident,
                 estado=('Confirmado por el usuario e incorporado a la tienda' if item.get('fuente_tipo') else 'Identificado en WhatsApp e incorporado a la tienda'))

products = list(by_id.values())
source.write_text('// Catálogo verificado con fotografías originales. Disponibilidad y medidas se coordinan con la boutique.\nexport const products = ' + json.dumps(products, ensure_ascii=False, indent=2) + ';\nexport const categories = ' + json.dumps(categories, ensure_ascii=False) + ';\n', encoding='utf-8')
(root / 'review/publicados-confirmados.json').write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding='utf-8')
groups_file.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')

def normalized(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if not unicodedata.combining(c)).strip(' .…�')

pending_file = root / 'review/gala-sin-foto-confirmada.json'
pending = json.loads(pending_file.read_text(encoding='utf-8-sig'))
known = {normalized(p['catalogName']) for p in products if p.get('importGroup')}
pending = [p for p in pending if not any(n == normalized(p['nombre']) or (len(normalized(p['nombre'])) > 40 and n.startswith(normalized(p['nombre']))) for n in known)]
pending_file.write_text(json.dumps(pending, ensure_ascii=False, indent=2), encoding='utf-8')

cards = []
for item in sorted(confirmed['confirmados'], key=lambda x: x['grupo']):
    group = groups[item['grupo']]
    product = by_id[group['productId']]
    pictures = ''.join(f'<figure><img src="../../{p["src"].removeprefix("./")}"><figcaption>{html.escape(p["view"])}</figcaption></figure>' for p in product['photos'])
    regular = f' <del>S/ {product["originalPrice"]:.2f}</del>' if product.get('originalPrice') else ''
    cards.append(f'<article><small>XL-{product["id"]} · {group["grupo"]} · {html.escape(product["category"])}</small><h2>{html.escape(product["name"])}</h2><p><strong>S/ {product["price"]:.2f}</strong>{regular}</p><div class="photos">{pictures}</div></article>')
remaining = [g for g in groups.values() if not g.get('productId')]
report = '<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Catálogo verificado · Xiliana</title><style>body{font:16px system-ui;color:#25221d;background:#faf8f4;margin:0;padding:28px}main{max-width:1200px;margin:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}article{background:white;border:1px solid #ded9cf;padding:18px}h1{font-size:32px}h2{font-size:19px;line-height:1.45}small,figcaption{color:#655e53}.photos{display:flex;gap:8px}figure{margin:0;min-width:0;flex:1}img{width:100%;height:320px;object-fit:contain}figcaption{font-size:13px}del{color:#777;font-size:14px}</style><main><h1>Prendas verificadas en tu WhatsApp</h1>'
report += f'<p>{len(cards)} modelos identificados · {sum(len(groups[i["grupo"]]["fotos"]) for i in confirmed["confirmados"])} fotos · frente primero. 29 modelos contrastados con el catálogo del +51 930 527 248. El rosado floral, XL-173, fue confirmado por el usuario a S/ 450.00 el 12 de octubre de 2026.</p>'
report += '<div class="grid">' + ''.join(cards) + '</div>'
report += '<h2>Fotos pendientes de asociar</h2><p>' + (', '.join(g['grupo'] for g in remaining) or 'Ninguna de las 30 prendas de esta entrega.') + '</p>'
report += '<h2>Prendas conocidas que todavía necesitan foto</h2><ul>' + ''.join(f'<li>{html.escape(p["nombre"])} · S/ {p["precio"]:.2f}</li>' for p in pending) + '</ul></main></html>'
(audit_dir / 'REVISION.html').write_text(report, encoding='utf-8')
old_pending = root / 'review/PENDIENTES-2026-10-08.html'
if old_pending.exists():
    old_report = old_pending.read_text(encoding='utf-8')
    updated_list = '<h2>Modelos del catálogo que todavía no tienen foto original identificada</h2><ul>' + ''.join(f'<li>{html.escape(p["nombre"])} · S/ {p["precio"]:.2f}</li>' for p in pending) + '</ul>'
    old_report = re.sub(r'<h2>Modelos del catálogo que todavía no tienen foto original identificada</h2><ul>[\s\S]*?</ul>', updated_list, old_report)
    old_pending.write_text(old_report, encoding='utf-8')
(audit_dir / 'resultado.json').write_text(json.dumps(dict(modelos_identificados=len(cards), fotos_incorporadas=sum(len(groups[i['grupo']]['fotos']) for i in confirmed['confirmados']), grupos_pendientes=[g['grupo'] for g in remaining], total_prendas=len(products), total_fotos=sum(len(p['photos']) for p in products), catalogo_sin_foto=pending), ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(cards)} modelos incorporados; {len(remaining)} pendientes. Tienda: {len(products)} prendas, {sum(len(p["photos"]) for p in products)} fotos.')
