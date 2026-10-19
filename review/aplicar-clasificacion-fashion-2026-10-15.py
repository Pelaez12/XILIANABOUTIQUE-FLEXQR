"""Aplicar las correcciones visuales ancladas en XL-054 y XL-089."""
from collections import Counter
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'review/clasificacion-fashion-2026-10-15'
SOURCE = ROOT / 'products.js'
MANIFEST = ROOT / 'review/categorias-confirmadas.json'
DECISIONS = {
    ident: ('Gala', 'La falda principal es larga y el brillo define el vestido. Una abertura alta no cambia la longitud principal, según la corrección del usuario y las definiciones consultadas.')
    for ident in [89, 103, 137, 140, 160, 161, 164]
}
DECISIONS.update({
    54: ('Cortos', 'Ejemplo explícito del usuario: minivestido de base negra lisa con bandas plateadas decorativas; el brillo no cubre la superficie predominante.'),
    82: ('Cortos', 'Base negra lisa; filas de strass localizadas en escote y torso, con falda y mangas lisas. Menor cobertura brillante que el ejemplo XL-054.'),
    114: ('Cortos', 'Vestido midi de cuerpo negro liso con perlas muy separadas y brillo concentrado en la pieza superior; no es un vestido de brillo predominante.'),
    118: ('Cortos', 'Vestido corto de base negra lisa con panel de lentejuelas localizado en el corpiño; falda lisa mayoritaria.'),
    172: ('Cortos', 'Vestido corto negro con bordado plateado localizado en mangas y parte de la pechera. La falda y la mayor parte del torso son lisos.'),
    62: ('Largos', 'Falda larga negra lisa, con perlas separadas en el corpiño y piezas satinadas rosas; brillo decorativo localizado, no predominante.'),
    68: ('Largos', 'Vestido rosado al tobillo de base lisa, con pequeños grupos de perlas separados por amplias zonas de tela lisa.'),
    81: ('Largos', 'Vestido marrón al tobillo con pequeñas aplicaciones plateadas espaciadas; la base lisa sigue definiendo el diseño.'),
    90: ('Largos', 'Vestido largo de terciopelo guinda con perlas localizadas en el busto; falda, mangas y espalda lisas.'),
    101: ('Largos', 'Falda principal larga y base roja lisa con bandas curvas plateadas decorativas, comparable al umbral confirmado con XL-054. La abertura no lo convierte en corto.'),
    107: ('Largos', 'Vestido largo plomo de base satinada lisa con aplicaciones florales localizadas en la falda; no se observa brillo predominante. No se certifica el material de las aplicaciones.'),
})


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def fixed_fields(product):
    return {key: value for key, value in product.items() if key != 'category'}


if read_json(MANIFEST).get('revision', '').startswith('conciliacion-catalogo-2026-10-15'):
    raise SystemExit('Existe una conciliación posterior con el catálogo comercial; este script histórico no debe sobrescribirla.')
text = SOURCE.read_text(encoding='utf-8-sig')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])
baseline = read_json(AUDIT / 'productos-antes.json')
assert len(products) == len(baseline) == 139
assert [fixed_fields(p) for p in products] == [fixed_fields(p) for p in baseline]
by_before = {p['id']: p for p in baseline}
manifest = read_json(AUDIT / 'categorias-antes.json')
entries = {item['id']: item for item in manifest['prendas']}
for product in products:
    ident = product['id']
    if ident in DECISIONS:
        category, reason = DECISIONS[ident]
        product['category'] = category
        entries[ident].update(categoria=category, motivo=reason, fecha='2026-10-15',
            fuente='Corrección del usuario con ejemplos XL-054 y XL-089, investigación de términos de moda y revisión independiente de fotografías.')

totals = dict(Counter(p['category'] for p in products))
assert totals == {'Gala': 28, 'Largos': 31, 'Cortos': 23, 'Bandage': 21, 'Cortos con brillo': 35, 'Liquidación': 1}, totals
assert sum(len(p['photos']) for p in products) == 225
assert len({p['id'] for p in products}) == 139
assert [fixed_fields(p) for p in products] == [fixed_fields(p) for p in baseline]
by_id = {p['id']: p for p in products}
assert by_id[54]['category'] == 'Cortos' and by_id[89]['category'] == 'Gala'
assert by_id[154]['category'] == 'Cortos con brillo' and by_id[125]['category'] == 'Liquidación'
assert all(by_id[p['id']]['category'] == 'Bandage' for p in baseline if p['category'] == 'Bandage')

manifest.update(fecha='2026-10-15', revision='fashion-2026-10-15',
    prioridad='La corrección actual del usuario y la revisión de largo principal y brillo predominante prevalecen sobre reglas anteriores, nombres y cantidades.',
    regla_abertura_alta='Sustituida: una abertura alta no convierte por sí sola una falda larga en vestido corto.',
    criterios_documentados='clasificacion-fashion-2026-10-15/CRITERIOS.md',
    excepciones_individuales=[{'id': 154, 'categoria': 'Cortos con brillo', 'motivo': 'Conservar la identificación individual explícita anterior del usuario sin extenderla a todos los maxis con abertura.'}])
manifest['criterios'].update({
    'Largos': 'Falda principal al tobillo o al suelo de base lisa o estampada; admite detalles brillantes localizados o dispersos sin brillo predominante.',
    'Gala': 'Vestido largo formal con brillo predominante, pedrería extensa o tejido brillante. Puede tener abertura alta; la abertura no cambia la longitud principal.',
    'Cortos': 'Vestido mini, a la rodilla o midi de base lisa o estampada; admite bandas, perlas dispersas y paneles decorativos localizados, como XL-054.',
    'Cortos con brillo': 'Vestido mini, a la rodilla o midi con brillo predominante y extendido en cuerpo o un bloque importante como toda la falda. Se conservan excepciones individuales expresamente confirmadas.',
})
manifest['prendas'] = [entries[p['id']] for p in products]
write_json(MANIFEST, manifest)
serialized = json.dumps(products, ensure_ascii=False, indent=2)
SOURCE.write_text(text[:match.start(1)] + serialized + text[match.end(1):], encoding='utf-8')
write_json(ROOT / 'review/publicados-confirmados.json', products)

confirmed_file = ROOT / 'review/catalogo-whatsapp-2026-10-12/confirmados.json'
confirmed = read_json(confirmed_file)
for item in confirmed['confirmados']:
    item['categoria'] = by_id[148 + int(item['grupo'].split('-')[1])]['category']
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
assert len(changes) == 18
summary = dict(fecha='2026-10-15', revision='fashion-2026-10-15', total_prendas=139, total_fotos=225,
    totales=totals, cambios=changes, conciliacion_inventario_cerrada=False,
    conservacion='Solo cambió la categoría: nombres, precios, identificadores, archivos de fotos, orden de galerías y orden de registros permanecen idénticos.',
    pendientes=['Las cantidades del encargado siguen pendientes de conciliación de identidades y stock.',
        'Se conservan las 16 entradas de Cortos sin asociación segura y las tres referencias Bandage pendientes del informe anterior; no se convierten en faltantes confirmados por aritmética.',
        'XL-127 mantiene categoría y precio; la resolución de sus fotos no certifica el material. Su nombre coincide con XL-140 aunque son diseños distintos.',
        'XL-107 y XL-174 se clasifican por apariencia visual; no se certifica la composición textil.'])
write_json(AUDIT / 'resultado-aplicado.json', summary)
lines = ['# Clasificación revisada con criterios de moda', '', '15 de octubre de 2026. **18 correcciones aplicadas; 139 prendas y 225 fotos conservadas.**', '',
    'La regla de abertura alta fue reemplazada por la corrección más reciente del usuario. XL-089 vuelve a Gala; XL-054 pasa a Cortos.', '',
    '## Reglas', '', '[Definiciones, referencias y orden de decisión](CRITERIOS.md).', '',
    '## Cantidades actuales', '', '| Colección principal | Prendas |', '|---|---:|']
for category in ('Largos', 'Gala', 'Cortos con brillo', 'Cortos', 'Bandage', 'Liquidación'):
    lines.append(f'| {category} | {totals[category]} |')
lines += ['', 'Estas cifras describen las fotografías guardadas con los criterios actuales. No equivalen a un conteo de stock confirmado ni se han forzado para alcanzar 25/43/30–31/22.', '',
    '## Cambios aplicados', '', '| Código | Nombre conservado | Antes | Ahora | Evidencia visual |', '|---|---|---|---|---|']
for item in changes:
    lines.append(f"| XL-{item['id']:03d} | {item['nombre']} | {item['antes']} | {item['ahora']} | {item['motivo']} |")
lines += ['', '## Excepción y pendientes', '',
    'XL-154 se conserva en Cortos con brillo por la confirmación individual previa del usuario. No se usa como regla para todos los vestidos largos con abertura.', '']
lines += ['- ' + item for item in summary['pendientes']]
lines += ['', '## Verificación', '', summary['conservacion'], '',
    'La revisión de brillo y Cortos coincide en retirar 54, 82, 114, 118 y 172 de Cortos con brillo. La revisión de Largos y la comprobación del coordinador retiran los largos de adorno localizado 62, 68, 81, 90, 101 y 107 de las colecciones de brillo predominante.', '']
(AUDIT / 'CLASIFICACION.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'cambios': len(changes), 'totales': totals, 'prendas': 139, 'fotos': 225}, ensure_ascii=False))
