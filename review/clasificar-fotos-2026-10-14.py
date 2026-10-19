"""Clasificación tras revisar las 225 fotos y la aclaración del usuario.

Solo modifica categorías. Conserva precios, nombres, archivos y galerías.
La instantánea previa y las láminas permiten revisar las decisiones.
"""
from collections import Counter
from pathlib import Path
import copy
import json
import re

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'review/auditoria-visual-2026-10-14'
SOURCE = ROOT / 'products.js'
MANIFEST = ROOT / 'review/categorias-confirmadas.json'
RULES = {
    'Largos': 'Vestidos largos sin brillo extendido. Un detalle de pedrería en escote, cintura o puños permanece en Largos; el lustre del satén no equivale a lentejuelas.',
    'Gala': 'Vestidos largos con brillo extendido en la tela, el cuerpo o el corpiño; lentejuelas, perlas o pedrería repetidas.',
    'Cortos': 'Vestidos cortos o midi sin decoración brillante; las plumas por sí solas no cuentan como brillo.',
    'Cortos con brillo': 'Vestidos cortos o midi con lentejuelas, perlas, pedrería o decoración brillante. Una caída lateral larga no convierte una minifalda en vestido largo.',
    'Bandage': 'Modelos identificados como Bandage. No se deduce el tejido solo porque la silueta sea ajustada.',
    'Liquidación': 'XL-125 conserva su oferta y aparece únicamente en Liquidación, según la corrección solicitada.',
}

# Decisiones después de inspeccionar frente y vistas adicionales, cuando existen.
DECISIONS = {
    60: ('Largos', 'Gasa azul con cuerpo de encaje sin brillo extendido.'),
    91: ('Largos', 'Terciopelo verde liso; sin decoración brillante extendida.'),
    93: ('Largos', 'Tela fucsia lisa; sin lentejuelas ni pedrería extendidas.'),
    96: ('Largos', 'Terciopelo verde con brillo limitado al escote.'),
    100: ('Largos', 'Vestido rojo liso con strass localizado en el escote.'),
    106: ('Largos', 'Vestido negro liso con detalles brillantes en escote y puños.'),
    138: ('Largos', 'Vestido rosado de gasa sin brillo extendido.'),
    159: ('Largos', 'Vestido negro liso con detalles en cuello y puños.'),
    162: ('Largos', 'Vestido rojo liso con perlas únicamente en el borde de los hombros.'),
    163: ('Largos', 'Vestido rojo con encaje y detalle localizado en la cintura; falda lisa.'),
    174: ('Largos', 'Tela oscura satinada; el lustre de la tela no es decoración de lentejuelas.'),
    176: ('Largos', 'Vestido blanco con bordes decorados en escote y cintura; falda lisa.'),
    177: ('Largos', 'Vestido nude con volantes y aplicaciones florales localizadas.'),
    178: ('Largos', 'Vestido verde asimétrico de tela lisa con capa.'),
    173: ('Largos', 'Vestido rosado largo con estampado floral, sin brillo extendido.'),
    125: ('Liquidación', 'Vestido crema de encaje y tull asimétrico en oferta; retirar su aparición en Gala.'),
    61: ('Gala', 'Vestido largo morado cubierto de lentejuelas, con mangas de gasa.'),
    62: ('Gala', 'Vestido negro largo con perlas y pedrería repetidas por todo el corpiño.'),
    81: ('Gala', 'Vestido vino largo con filas repetidas de decoración metálica en todo el cuerpo superior.'),
    87: ('Gala', 'Vestido azul largo de lentejuelas.'),
    111: ('Gala', 'Vestido crema largo con perlas y pedrería por todo el cuerpo.'),
    141: ('Gala', 'Vestido azul largo con decoración brillante densa en el corpiño.'),
    114: ('Cortos con brillo', 'Largo midi, con capa y pedrería; no llega al suelo.'),
    22: ('Cortos', 'Vestido blanco floral de largo midi, sin brillo extendido.'),
    68: ('Gala', 'Vestido rosado hasta los tobillos con patrón vertical de perlas en frente y espalda.'),
    82: ('Cortos con brillo', 'Vestido negro a la rodilla con strass en el escote.'),
    83: ('Cortos con brillo', 'Vestido blanco corto con capa y strass en los hombros.'),
    85: ('Cortos con brillo', 'Vestido corto drapeado con patrón metálico brillante.'),
    86: ('Cortos con brillo', 'Vestido crema midi con estrellas metálicas en el cuerpo superior.'),
    127: ('Cortos con brillo', 'Minivestido vino con pedrería y caída lateral larga; distinto de XL-140.'),
    130: ('Cortos con brillo', 'Vestido plomo a la rodilla con corpiño de lentejuelas.'),
    121: ('Cortos', 'Minivestido negro liso de tiras y aberturas, sin decoración brillante.'),
    122: ('Cortos', 'Minivestido negro liso con plumas en el busto; sin decoración brillante.'),
    154: ('Gala', 'Vestido verde largo de lentejuelas con abertura y corsé.'),
}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def without_category(product):
    return {key: value for key, value in product.items() if key != 'category'}


if read_json(MANIFEST).get('fecha', '') > '2026-10-14':
    raise SystemExit('Hay una clasificación posterior confirmada; este script histórico no debe sobrescribirla.')
source_text = SOURCE.read_text(encoding='utf-8-sig')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', source_text)
products = json.loads(match[1])
baseline = read_json(AUDIT / 'productos-antes.json')
assert len(products) == len(baseline) == 139
assert len({p['id'] for p in products}) == 139
assert [without_category(p) for p in products] == [without_category(p) for p in baseline], 'Se alteraron campos ajenos a la categoría.'
by_before = {p['id']: p for p in baseline}
assert set(DECISIONS) <= set(by_before)

previous_manifest = AUDIT / 'clasificacion-anterior.json'
if not previous_manifest.exists():
    previous_manifest.write_bytes(MANIFEST.read_bytes())

entries = []
for product in products:
    ident = product['id']
    category, reason = DECISIONS.get(ident, (by_before[ident]['category'], RULES[by_before[ident]['category']]))
    product['category'] = category
    entries.append({
        'id': ident, 'nombre': product['name'], 'categoria': category,
        'fecha': '2026-10-14',
        'fuente': 'Revisión visual de todas las fotos del producto y criterios del usuario.',
        'motivo': reason,
        'fotos': [{key: photo[key] for key in ('src', 'view', 'sha256') if key in photo} for photo in product['photos']],
    })

totals = dict(Counter(p['category'] for p in products))
assert totals == {'Gala': 35, 'Largos': 25, 'Cortos': 14, 'Cortos con brillo': 43, 'Bandage': 21, 'Liquidación': 1}, totals
assert sum(len(p['photos']) for p in products) == 225
assert [without_category(p) for p in products] == [without_category(p) for p in baseline]
assert next(p for p in products if p['id'] == 127)['price'] == 549
assert next(p for p in products if p['id'] == 125)['price'] == 194.5
assert next(p for p in products if p['id'] == 125)['category'] == 'Liquidación'

manifest = {
    'fecha': '2026-10-14',
    'prioridad': 'La revisión visual con los criterios actuales del usuario prevalece sobre palabras del nombre y álbumes anteriores.',
    'aclaracion_usuario': 'Largos, cuando el brillo sea solo un detalle.',
    'criterios': RULES,
    'evidencia_anterior': 'auditoria-visual-2026-10-14/clasificacion-anterior.json',
    'laminas_revisadas': 'auditoria-visual-2026-10-14/laminas.json',
    'prendas': entries,
}
write_json(MANIFEST, manifest)
serialized = json.dumps(products, ensure_ascii=False, indent=2)
SOURCE.write_text(source_text[:match.start(1)] + serialized + source_text[match.end(1):], encoding='utf-8')
write_json(ROOT / 'review/publicados-confirmados.json', products)

# Sincronizar registros de importación para que una reconstrucción conserve las categorías.
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
        report = re.sub(r'(<small>XL-' + str(product['id']) + r' · ' + re.escape(product['importGroup']) + r' · )[^<]+(</small>)', lambda m: m[1] + product['category'] + m[2], report)
report_file.write_text(report, encoding='utf-8')

changes = [dict(id=p['id'], nombre=p['name'], antes=by_before[p['id']]['category'], ahora=p['category'], motivo=DECISIONS[p['id']][1]) for p in products if p['category'] != by_before[p['id']]['category']]
targets = {'Largos': 25, 'Cortos con brillo': 43, 'Cortos': 31, 'Bandage': 22}
comparison = {category: {'indicados': target, 'clasificados': totals[category], 'diferencia': target - totals[category]} for category, target in targets.items()}
summary = {
    'fecha': '2026-10-14', 'total_prendas': len(products), 'total_fotos_revisadas': 225,
    'totales': totals, 'comparacion_cantidades': comparison, 'cambios': changes,
    'modelos_en_ofertas': sum(p.get('originalPrice', 0) > p['price'] for p in products),
    'verificacion': 'Solo cambió la categoría. Identificadores, nombres, precios, fotos, orden de galerías y orden de registros permanecen idénticos a la instantánea previa.',
    'pendiente': 'Las cantidades indicadas superan en 17 los cortos y en 1 los Bandage guardados con foto. La diferencia no identifica por sí sola prendas faltantes ni autoriza duplicarlas o reclasificarlas sin evidencia.',
}
write_json(AUDIT / 'resultado.json', summary)

lines = ['# Clasificación visual del catálogo — 14 de octubre de 2026', '',
    'Revisadas **139 prendas y sus 225 fotografías**, incluidas las vistas adicionales. Se aplica la aclaración: **un largo con brillo solo en un detalle permanece en Largos**.', '',
    '## Resultado', '', '| Colección | Prendas clasificadas | Cantidad indicada | Diferencia |', '|---|---:|---:|---:|']
for category in ('Largos', 'Gala', 'Cortos con brillo', 'Cortos', 'Bandage', 'Liquidación'):
    target = targets.get(category)
    lines.append(f"| {category} | {totals[category]} | {target if target is not None else '—'} | {target - totals[category] if target is not None else '—'} |")
lines += ['', 'La tabla cuenta la categoría principal de cada prenda. La página de Ofertas reúne los 8 modelos con descuento, incluida XL-125, que es la única con Liquidación como categoría principal.', '',
    f'**{len(changes)} prendas cambiaron de colección.** XL-125 conserva S/ 194.50 y queda en Liquidación, fuera de Gala. XL-127 conserva S/ 549.00.', '',
    '**Pendiente de conciliación:** hay 14 Cortos frente a los 31 indicados y 21 Bandage frente a los 22 indicados. Estas diferencias corresponden al catálogo guardado; no se añadieron ni se duplicaron modelos para completar cifras.', '',
    '## Criterios', '']
lines += [f'- **{category}:** {rule}' for category, rule in RULES.items()]
lines += ['', '## Registro de todas las prendas', '', '| Código | Nombre | Colección anterior | Colección revisada | Precio | Motivo |', '|---|---|---|---|---:|---|']
for product, entry in zip(products, entries):
    name = product['name'].replace('|', '\\|')
    reason = entry['motivo'].replace('|', '\\|')
    lines.append(f"| XL-{product['id']:03d} | {name} | {by_before[product['id']]['category']} | {product['category']} | S/ {product['price']:.2f} | {reason} |")
lines += ['', '## Evidencia y conservación', '',
    '- `productos-antes.json`: instantánea previa de las 139 prendas.',
    '- `laminas.json` y las láminas JPG: cobertura de las 225 fotografías revisadas.',
    '- `clasificacion-anterior.json`: clasificación anterior por álbum, conservada para trazabilidad.',
    '- `resultado.json`: cambios y conteos estructurados.',
    '- Se conservaron nombres, precios, fotos, orden de galerías, identificadores y orden de registros.', '']
(AUDIT / 'CLASIFICACION.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'cambios': len(changes), 'totales': totals, 'prendas': len(products), 'fotos': 225, 'comparacion': comparison}, ensure_ascii=False))
