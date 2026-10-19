"""Aplicar la revisión por categoría y la regla comercial de abertura alta."""
from collections import Counter
from pathlib import Path
import copy
import json
import re

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'review/conciliacion-2026-10-15'
SOURCE = ROOT / 'products.js'
MANIFEST = ROOT / 'review/categorias-confirmadas.json'
HIGH_SLITS = [89, 101, 103, 137, 140, 154, 160, 161, 164]
DECISIONS = {
    ident: ('Cortos con brillo', 'Brillo y abertura alta que deja la pierna expuesta. El usuario confirmó que todos estos diseños pertenecen a Cortos con brillo, aunque tengan falda larga.')
    for ident in HIGH_SLITS
}
DECISIONS.update({
    83: ('Cortos', 'Vestido blanco midi de tela lisa, con un fleco de strass localizado en el nudo de cintura; pertenece también al listado oficial de Cortos.'),
    85: ('Cortos', 'El original ampliado muestra estampado marrón y blanco plano, sin lentejuelas ni pedrería. Coincide con el listado oficial de Cortos.'),
    86: ('Cortos', 'Vestido crema midi de gasa lisa con tres estrellas doradas como adorno localizado. Coincide con el listado oficial de Cortos.'),
    130: ('Cortos', 'Minifalda ploma lisa con caída lateral y lentejuelas limitadas a media copa del escote. El adorno localizado no convierte la base lisa en una prenda cubierta de brillo.'),
    141: ('Largos', 'Falda azul lisa hasta el suelo con cola; aplicación de encaje y pedrería limitada al panel alto del busto. Se aplica la regla del usuario sobre detalle localizado.'),
    174: ('Gala', 'Vestido hasta el suelo con apariencia metalizada uniforme en torso, mangas y falda, distinta de un pequeño adorno brillante. Clasificación visual; composición del tejido sin certificar.'),
})


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def immutable_fields(product):
    return {key: value for key, value in product.items() if key != 'category'}


if read_json(MANIFEST).get('revision') == 'fashion-2026-10-15' or read_json(MANIFEST).get('revision', '').startswith('conciliacion-catalogo-2026-10-15'):
    raise SystemExit('Hay una corrección posterior de criterios de moda; este script histórico no debe sobrescribirla.')
text = SOURCE.read_text(encoding='utf-8-sig')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])
baseline = read_json(AUDIT / 'productos-antes.json')
assert len(products) == len(baseline) == 139
assert [immutable_fields(p) for p in products] == [immutable_fields(p) for p in baseline]
by_before = {p['id']: p for p in baseline}
assert set(DECISIONS) <= set(by_before)
previous_manifest = AUDIT / 'categorias-antes.json'
if not previous_manifest.exists():
    previous_manifest.write_bytes(MANIFEST.read_bytes())
manifest = read_json(previous_manifest)
entries = {item['id']: item for item in manifest['prendas']}

for product in products:
    ident = product['id']
    if ident in DECISIONS:
        category, reason = DECISIONS[ident]
        product['category'] = category
        entries[ident].update(categoria=category, motivo=reason, fecha='2026-10-15',
            fuente='Conciliación con cinco revisiones independientes y criterios del usuario.')

totals = dict(Counter(p['category'] for p in products))
assert totals == {'Gala': 26, 'Largos': 25, 'Cortos': 18, 'Bandage': 21, 'Cortos con brillo': 48, 'Liquidación': 1}, totals
assert len({p['id'] for p in products}) == 139
assert sum(len(p['photos']) for p in products) == 225
assert [immutable_fields(p) for p in products] == [immutable_fields(p) for p in baseline]
assert all(next(p for p in products if p['id'] == ident)['category'] == 'Cortos con brillo' for ident in HIGH_SLITS)
assert next(p for p in products if p['id'] == 125)['category'] == 'Liquidación'

manifest.update(fecha='2026-10-15',
    prioridad='La clasificación comercial y las confirmaciones actuales del usuario prevalecen sobre el nombre y la longitud de una cola.',
    regla_abertura_alta='Todos los vestidos con brillo y abertura alta que muestran la pierna van en Cortos con brillo, aunque tengan falda larga. Confirmado por el usuario el 15 de octubre de 2026.',
    revisiones_independientes=['Gala', 'Largos', 'Cortos', 'Cortos con brillo', 'Bandage'])
manifest['criterios']['Gala'] = 'Vestidos largos de brillo extendido sin abertura alta que exponga la pierna. Las aberturas altas se incluyen en Cortos con brillo por confirmación del usuario.'
manifest['criterios']['Cortos'] = 'Vestidos cortos o midi de base lisa o estampada, sin brillo extendido. Se incluyen los de adorno localizado; las plumas por sí solas no cuentan como brillo.'
manifest['criterios']['Cortos con brillo'] = 'Vestidos cortos o midi con brillo extendido, y todos los vestidos brillantes con abertura alta que muestran la pierna, aunque tengan falda larga.'
manifest['prendas'] = [entries[p['id']] for p in products]
write_json(MANIFEST, manifest)
serialized = json.dumps(products, ensure_ascii=False, indent=2)
SOURCE.write_text(text[:match.start(1)] + serialized + text[match.end(1):], encoding='utf-8')
write_json(ROOT / 'review/publicados-confirmados.json', products)

by_id = {p['id']: p for p in products}
confirmed_file = ROOT / 'review/catalogo-whatsapp-2026-10-12/confirmados.json'
confirmed = read_json(confirmed_file)
old_confirmed = copy.deepcopy(confirmed)
for item in confirmed['confirmados']:
    ident = 148 + int(item['grupo'].split('-')[1])
    item['categoria'] = by_id[ident]['category']
assert [{k: v for k, v in item.items() if k != 'categoria'} for item in confirmed['confirmados']] == [{k: v for k, v in item.items() if k != 'categoria'} for item in old_confirmed['confirmados']]
write_json(confirmed_file, confirmed)
groups_file = ROOT / 'review/importacion-2026-10-10/verificacion.json'
groups = read_json(groups_file)
for group in groups['modelos_nuevos']:
    if group.get('productId') in by_id:
        group['categoria'] = by_id[group['productId']]['category']
write_json(groups_file, groups)
report_file = ROOT / 'review/catalogo-whatsapp-2026-10-12/REVISION.html'
report = report_file.read_text(encoding='utf-8')
for product in products:
    if product.get('importGroup'):
        pattern = r'(<small>XL-' + str(product['id']) + r' · ' + re.escape(product['importGroup']) + r' · )[^<]+(</small>)'
        report = re.sub(pattern, lambda m: m[1] + product['category'] + m[2], report)
report_file.write_text(report, encoding='utf-8')

changes = [dict(id=p['id'], nombre=p['name'], antes=by_before[p['id']]['category'], ahora=p['category'], motivo=DECISIONS[p['id']][1]) for p in products if p['category'] != by_before[p['id']]['category']]
assert len(changes) == 15
summary = {
    'fecha': '2026-10-15', 'total_prendas': 139, 'total_fotos': 225,
    'totales': totals, 'cambios': changes, 'aberturas_altas_confirmadas': HIGH_SLITS,
    'referencia_encargado': {'Largos': 25, 'Cortos con brillo': 43, 'Cortos': '30 o 31, provisionalmente 31', 'Bandage': 22},
    'conciliacion_cerrada': False,
    'pendientes': [
        '16 entradas de la lista oficial de Cortos sin asociación segura con una ficha publicada; no equivalen a 16 prendas faltantes confirmadas.',
        'Dos entradas blancas de perlas usan la misma miniatura; confirmar si son modelos distintos o un registro duplicado.',
        'XL-069 y XL-131 comparten nombre de catálogo pero muestran diseños distintos; resolver identificación exacta.',
        'XL-127 y XL-140 tienen el mismo nombre y precio, pero muestran modelos distintos. Conservar los dos; conciliar nombre exacto de XL-127.',
        'Bandage: tres referencias adicionales con miniatura y precio requieren asociación a foto original; no hay evidencia para seleccionar únicamente una y cerrar 22.',
        'Con la regla nueva hay 48 Cortos con brillo frente a los 43 indicados; conciliar identidades y el inventario del encargado.',
        'Los materiales de XL-068, XL-107, XL-172 y XL-174 admiten dudas en una foto; no se certifica la composición textil.',
    ],
    'conservacion': 'Nombres, precios, identificadores, orden de registros, 225 fotos y orden de las galerías idénticos a la instantánea previa.',
}
write_json(AUDIT / 'resultado-aplicado.json', summary)

lines = ['# Conciliación del catálogo — 15 de octubre de 2026', '',
    'Cinco revisiones independientes: una para cada colección. **139 prendas y 225 fotos conservadas; 15 cambios de categoría aplicados.**', '',
    '## Criterio confirmado', '',
    '> Todos los vestidos con brillo y abertura alta que muestran la pierna pertenecen a Cortos con brillo, aunque tengan falda larga.', '',
    'Esta decisión comercial reemplaza la clasificación anterior de esos nueve modelos como Gala. Los largos de base lisa con un detalle localizado siguen en Largos. Se distingue también una base lisa con un adorno de un vestido cubierto de brillo.', '',
    '## Cantidades actuales', '',
    '| Colección principal | Prendas | Referencia del encargado |', '|---|---:|---:|']
references = summary['referencia_encargado']
for category in ('Largos', 'Gala', 'Cortos con brillo', 'Cortos', 'Bandage', 'Liquidación'):
    lines.append(f"| {category} | {totals[category]} | {references.get(category, '—')} |")
lines += ['', 'Liquidación es la categoría principal de XL-125. La página de Ofertas mantiene los ocho modelos con descuento, sin devolver XL-125 a Gala.', '',
    '**El inventario sigue pendiente de conciliación.** La diferencia numérica por sí sola no demuestra que falten prendas: hay asociaciones de nombres, miniaturas y modelos que resolver. Con la nueva regla comercial, Brillo suma 48 frente a la referencia de 43.', '',
    '## Cambios aplicados', '', '| Código | Nombre conservado | Antes | Ahora | Motivo |', '|---|---|---|---|---|']
for item in changes:
    lines.append(f"| XL-{item['id']:03d} | {item['nombre']} | {item['antes']} | {item['ahora']} | {item['motivo']} |")
lines += ['', '## Asociaciones pendientes', '']
lines += ['- ' + value for value in summary['pendientes']]
lines += ['', '## Revisiones por colección', '',
    '- [Gala](revision-gala/REVISION-GALA.md) · [Aberturas altas confirmadas](revision-gala/ALCANCE-ABERTURAS-CONFIRMADO.md)',
    '- [Largos](revision-largos/REVISION-LARGOS.md)',
    '- [Cortos: matriz de las 33 entradas oficiales](revision-cortos/REPORTE-CORTOS.md)',
    '- [Cortos con brillo](revision-brillo/REPORTE-BRILLO.md)',
    '- [Bandage: tres referencias con nombre, precio y miniatura](revision-bandage/REVISION-BANDAGE.md)', '',
    'Los informes individuales contienen propuestas anteriores a la decisión final; la tabla de cambios aplicada y products.js son la clasificación vigente.', '',
    '## Verificación', '', summary['conservacion'], '']
(AUDIT / 'CONCILIACION.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'cambios': len(changes), 'totales': totals, 'prendas': 139, 'fotos': 225, 'conciliacion_inventario_cerrada': False}, ensure_ascii=False))
