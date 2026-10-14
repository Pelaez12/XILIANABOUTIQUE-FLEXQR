"""Clasificación explícita por los dos álbumes del usuario. No modifica otras propiedades."""
from collections import Counter, defaultdict
from pathlib import Path
import copy
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]
audit_dir = root / 'review/clasificacion-2026-10-13'
source = root / 'products.js'
text = source.read_text(encoding='utf-8-sig')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])
before = copy.deepcopy(products)
by_id = {p['id']: p for p in products}
photos_file = audit_dir / 'coincidencias.json'
photos = json.loads(photos_file.read_text(encoding='utf-8'))

# Verificadas visualmente: mismo vestido, modelo, pose, pedrería y fondo.
# Los archivos del álbum tienen otra resolución o un encuadre distinto.
visual = {'brillo-03.jpeg': 16, 'brillo-14.jpeg': 17, 'brillo-26.jpeg': 122}
for shot in photos:
    path = root / shot['extraido']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == shot['sha256']
    if path.name in visual:
        product = by_id[visual[path.name]]
        shot['coincidencias'] = [dict(id=product['id'], nombre=product['name'],
            categoria=product['category'], foto=product['photos'][0]['src'],
            vista=product['photos'][0]['view'])]
        shot['metodo'] = 'Coincidencia visual verificada; resolución o encuadre diferente'
    else:
        shot['metodo'] = 'Archivo idéntico, SHA-256'
        assert shot['coincidencias'], f"Foto sin identificar: {shot['extraido']}"
        for item in shot['coincidencias']:
            original = root / item['foto'].removeprefix('./')
            assert hashlib.sha256(original.read_bytes()).hexdigest() == shot['sha256']
    assert len({p['id'] for p in shot['coincidencias']}) == 1

evidence = defaultdict(list)
for shot in photos:
    evidence[shot['coincidencias'][0]['id']].append(shot)
assert len(photos) == 49 and len(evidence) == 32

manifest_file = root / 'review/categorias-confirmadas.json'
manifest = json.loads(manifest_file.read_text(encoding='utf-8')) if manifest_file.exists() else {'prendas': []}
overrides = {p['id']: p for p in manifest['prendas']}
for ident, shots in evidence.items():
    categories = {s['categoria_indicada'] for s in shots}
    assert len(categories) == 1, f'Álbumes contradictorios: XL-{ident}'
    category = next(iter(categories))
    overrides[ident] = dict(id=ident, nombre=by_id[ident]['name'], categoria=category,
        fecha='2026-10-13', fuente='Clasificación explícita del usuario por álbum',
        album=shots[0]['album'], fotos=[dict(archivo=s['archivo'], sha256=s['sha256'],
            metodo=s['metodo']) for s in shots])
    by_id[ident]['category'] = category

backup = audit_dir / 'productos-antes.json'
if not backup.exists():
    backup.write_text(json.dumps(before, ensure_ascii=False, indent=2), encoding='utf-8')

assert len(before) == len(products) == 139
for old, new in zip(before, products):
    assert {k:v for k,v in old.items() if k != 'category'} == {k:v for k,v in new.items() if k != 'category'}
assert sum(len(p['photos']) for p in products) == 225

manifest_file.write_text(json.dumps(dict(prioridad='La categoría confirmada por el usuario prevalece sobre el nombre.',
    prendas=sorted(overrides.values(), key=lambda p:p['id'])), ensure_ascii=False, indent=2), encoding='utf-8')
serialized = json.dumps(products, ensure_ascii=False, indent=2)
source.write_text(text[:match.start(1)] + serialized + text[match.end(1):], encoding='utf-8')
(root / 'review/publicados-confirmados.json').write_text(serialized, encoding='utf-8')
photos_file.write_text(json.dumps(photos, ensure_ascii=False, indent=2), encoding='utf-8')

confirmed_file = root / 'review/catalogo-whatsapp-2026-10-12/confirmados.json'
confirmed = json.loads(confirmed_file.read_text(encoding='utf-8'))
for item in confirmed['confirmados']:
    ident = 148 + int(item['grupo'].split('-')[1])
    if ident in evidence:
        item['categoria'] = by_id[ident]['category']
confirmed_file.write_text(json.dumps(confirmed, ensure_ascii=False, indent=2), encoding='utf-8')

groups_file = root / 'review/importacion-2026-10-10/verificacion.json'
groups = json.loads(groups_file.read_text(encoding='utf-8'))
for group in groups['modelos_nuevos']:
    if group.get('productId') in evidence:
        group['categoria'] = by_id[group['productId']]['category']
groups_file.write_text(json.dumps(groups, ensure_ascii=False, indent=2), encoding='utf-8')

report_file = root / 'review/catalogo-whatsapp-2026-10-12/REVISION.html'
report = report_file.read_text(encoding='utf-8')
for ident in evidence:
    p = by_id[ident]
    if p.get('importGroup'):
        pattern = r'(<small>XL-' + str(ident) + r' · ' + re.escape(p['importGroup']) + r' · )[^<]+(</small>)'
        report = re.sub(pattern, lambda m:m[1]+p['category']+m[2], report)
report_file.write_text(report, encoding='utf-8')

baseline = {p['id']:p for p in json.loads(backup.read_text(encoding='utf-8'))}
changes = [dict(id=p['id'], nombre=p['name'], antes=baseline[p['id']]['category'], ahora=p['category'])
           for p in products if baseline[p['id']]['category'] != p['category']]
summary = dict(fecha='2026-10-13', fotos_revisadas=len(photos), coincidencias_exactas=46,
    coincidencias_visuales=3, modelos_revisados=len(evidence),
    modelos_por_album=dict(Counter(by_id[ident]['category'] for ident in evidence)), cambios=changes,
    totales=dict(Counter(p['category'] for p in products)), prendas=139, fotos_catalogo=225,
    verificacion='Solo cambió la categoría. Nombres, precios, descuentos, fotos, orden de galerías e identificadores se conservaron.')
(audit_dir / 'resultado.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
lines=['# Clasificación de los álbumes del 13 de octubre de 2026','',
       '49 fotos corresponden a 32 prendas ya existentes: 19 de Cortos con brillo y 13 de Gala.',
       '46 archivos idénticos y 3 coincidencias visuales verificadas. No se crearon prendas ni fotos duplicadas.',
       '', '| Código | Nombre | Categoría anterior | Categoría confirmada |', '| --- | --- | --- | --- |']
for ident in sorted(evidence):
    p=by_id[ident]
    lines.append(f"| XL-{ident:03} | {p['name']} | {baseline[ident]['category']} | {p['category']} |")
lines.extend(['', summary['verificacion'], '',
    'Se aplicó la clasificación explícita por álbum incluso cuando el nombre incluía largo. Los descuentos siguen apareciendo en Ofertas independientemente de la colección.'])
(audit_dir / 'REVISION.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False))
