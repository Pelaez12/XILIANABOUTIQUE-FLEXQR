"""Conciliar seis ubicaciones con nombres, fotos y colecciones del catálogo guardado."""
from collections import Counter
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'review/conciliacion-final-2026-10-15'
SOURCE = ROOT / 'products.js'
MANIFEST = ROOT / 'review/categorias-confirmadas.json'
REVISION = 'conciliacion-catalogo-2026-10-15'
DECISIONS = {
    62: ('Gala', 'Nombre y miniatura del vestido negro con lazo rosa en Gala Dresses, fila 19 del listado guardado. Se conserva su clasificación comercial de Gala.'),
    68: ('Cortos', 'La ficha de cuello cuadrado rosa, S/299, figura expresamente en la colección comercial Cortos, fila 17. Nombre, precio y fotografías se conservan.'),
    81: ('Cortos', 'La ficha marrón con aplicaciones plateadas, S/319, figura expresamente en la colección comercial Cortos, fila 28, aunque el nombre incluya largo.'),
    90: ('Gala', 'Nombre explícito de gala, miniatura guinda con perlas y S/589 en Gala Dresses, fila 25. Frente y espalda confirman el mismo vestido formal largo.'),
    101: ('Gala', 'Nombre explícito de gala, miniatura roja con bandas plateadas y S/349 en Gala Dresses, fila 39. La abertura alta no cambia la longitud principal.'),
    107: ('Gala', 'La referencia histórica GALA-CAPTURA-R112 vincula las fotos R112/R116, el nombre modelo plomo y S/529 a Gala. Se conserva separado de XL-175, un diseño distinto con nombre base genérico.'),
}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def fixed_fields(product):
    return {key: value for key, value in product.items() if key != 'category'}


AUDIT.mkdir(parents=True, exist_ok=True)
manifest = read_json(MANIFEST)
assert manifest.get('revision') in ('fashion-2026-10-15', REVISION), 'Una revisión posterior impide ejecutar esta conciliación histórica.'
text = SOURCE.read_text(encoding='utf-8-sig')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])
baseline_file = AUDIT / 'productos-antes.json'
if not baseline_file.exists():
    assert manifest.get('revision') == 'fashion-2026-10-15'
    write_json(baseline_file, products)
    for source, name in [
        (MANIFEST, 'categorias-antes.json'),
        (ROOT/'review/publicados-confirmados.json', 'publicados-antes.json'),
        (ROOT/'review/catalogo-whatsapp-2026-10-12/confirmados.json', 'confirmados-oct12-antes.json'),
        (ROOT/'review/importacion-2026-10-10/verificacion.json', 'verificacion-oct10-antes.json'),
        (ROOT/'review/catalogo-whatsapp-2026-10-12/REVISION.html', 'REVISION-antes.html'),
    ]:
        (AUDIT/name).write_bytes(source.read_bytes())
baseline = read_json(baseline_file)
assert len(products) == len(baseline) == 139
assert [fixed_fields(p) for p in products] == [fixed_fields(p) for p in baseline]
assert Counter(p['category'] for p in baseline) == {'Largos':31,'Gala':28,'Cortos':23,'Cortos con brillo':35,'Bandage':21,'Liquidación':1}
by_before = {p['id']: p for p in baseline}
entries = {item['id']: item for item in manifest['prendas']}
for product in products:
    ident = product['id']
    if ident in DECISIONS:
        category, reason = DECISIONS[ident]
        product['category'] = category
        entries[ident].update(categoria=category, motivo=reason, fecha='2026-10-15',
            fuente='Conciliación solicitada por el usuario: nombre + fotos originales + colección comercial guardada. Evidencia en conciliacion-final-2026-10-15/gala-largos/matriz.json.')

totals = dict(Counter(p['category'] for p in products))
assert totals == {'Largos':25,'Gala':32,'Cortos':25,'Cortos con brillo':35,'Bandage':21,'Liquidación':1}, totals
assert sum(len(p['photos']) for p in products) == 225
assert [fixed_fields(p) for p in products] == [fixed_fields(p) for p in baseline]
assert len({p['id'] for p in products}) == 139
by_id = {p['id']:p for p in products}
assert by_id[54]['category'] == 'Cortos' and by_id[89]['category'] == 'Gala'
assert by_id[154]['category'] == 'Cortos con brillo' and by_id[125]['category'] == 'Liquidación'

exceptions = {item['id']:item for item in manifest.get('excepciones_individuales',[])}
for ident in DECISIONS:
    category,reason = DECISIONS[ident]
    exceptions[ident] = {'id':ident,'categoria':category,'motivo':reason}
manifest.update(fecha='2026-10-15', revision=REVISION,
    prioridad='Primero las confirmaciones específicas del usuario. Cotejar después nombre completo, fotografías de frente y espalda y colección comercial del catálogo. Conservar las excepciones documentadas cuando nombre o longitud visual sean ambiguos; no usar solo una palabra ni solo una cuota.',
    criterios_documentados='conciliacion-final-2026-10-15/CONCILIACION.md',
    referencias_comerciales='catalogo-whatsapp-2026-10-12/cortos-completo.json y gala-completo.json; confirmaciones-usuario.json para GALA-CAPTURA-R112.',
    excepciones_individuales=list(exceptions.values()))
manifest['criterios']['Cortos'] += ' Las fichas comerciales XL-068 y XL-081 se conservan en Cortos por su ubicación explícita en el catálogo guardado.'
manifest['criterios']['Gala'] += ' Las referencias comerciales confirmadas XL-062, XL-090, XL-101 y XL-107 se conservan en Gala aunque su brillo sea localizado.'
# Evitar repetir las aclaraciones cuando se ejecute de nuevo la misma revisión.
for category,suffix in [('Cortos',' Las fichas comerciales XL-068 y XL-081 se conservan en Cortos por su ubicación explícita en el catálogo guardado.'),('Gala',' Las referencias comerciales confirmadas XL-062, XL-090, XL-101 y XL-107 se conservan en Gala aunque su brillo sea localizado.')]:
    base = manifest['criterios'][category].replace(suffix,'')
    manifest['criterios'][category] = base + suffix
manifest['prendas'] = [entries[p['id']] for p in products]
write_json(MANIFEST, manifest)
SOURCE.write_text(text[:match.start(1)] + json.dumps(products,ensure_ascii=False,indent=2) + text[match.end(1):],encoding='utf-8')
write_json(ROOT/'review/publicados-confirmados.json',products)

confirmed_file = ROOT/'review/catalogo-whatsapp-2026-10-12/confirmados.json'
confirmed = read_json(confirmed_file)
for item in confirmed['confirmados']:
    item['categoria'] = by_id[148+int(item['grupo'].split('-')[1])]['category']
write_json(confirmed_file,confirmed)
groups_file = ROOT/'review/importacion-2026-10-10/verificacion.json'
groups = read_json(groups_file)
for group in groups['modelos_nuevos']:
    if group.get('productId') in by_id:
        group['categoria'] = by_id[group['productId']]['category']
write_json(groups_file,groups)
report_file = ROOT/'review/catalogo-whatsapp-2026-10-12/REVISION.html'
report = report_file.read_text(encoding='utf-8')
for product in products:
    if product.get('importGroup'):
        pattern = r'(<small>XL-'+str(product['id'])+r' · '+re.escape(product['importGroup'])+r' · )[^<]+(</small>)'
        report = re.sub(pattern,lambda m:m[1]+product['category']+m[2],report)
report_file.write_text(report,encoding='utf-8')

changes = [dict(id=p['id'],nombre=p['name'],antes=by_before[p['id']]['category'],ahora=p['category'],motivo=DECISIONS[p['id']][1]) for p in products if p['category'] != by_before[p['id']]['category']]
assert len(changes) == 6
summary = dict(fecha='2026-10-15',revision=REVISION,total_prendas=139,total_fotos=225,totales=totals,cambios=changes,
    metas_usuario={'Largos':25,'Cortos con brillo':43,'Cortos':30},diferencias_pendientes={'Largos':0,'Cortos con brillo':8,'Cortos':5},
    conciliacion_inventario_cerrada=False,
    conservacion='Solo se modificaron seis categorías. Se conservan idénticos todos los nombres, precios, identificadores, fotografías, orden de galerías y orden de registros.',
    evidencia='gala-largos/REPORTE.md y gala-largos/matriz.json',
    pendientes=['Cortos con brillo: faltan conciliar ocho referencias frente al total indicado de 43.','Cortos: faltan conciliar cinco referencias frente al total indicado de 30.','Bandage conserva 21 modelos; el total histórico indicado fue 22.','XL-107 y XL-175 comparten nombre base y precio, pero sus fotos muestran modelos diferentes; no fusionarlos.'])
write_json(AUDIT/'resultado-aplicado.json',summary)
lines=['# Conciliación del catálogo por nombres, fotos y colección comercial','','15 de octubre de 2026. **Seis ubicaciones corregidas; 139 prendas y 225 fotos conservadas.**','','## Orden de referencia','','1. Confirmación específica más reciente del usuario.','2. Nombre completo y precio de la ficha para reconocer el modelo.','3. Fotos de frente y espalda para comprobar identidad, largo y brillo.','4. Colección comercial del catálogo guardado, con excepciones explícitas cuando el nombre o la longitud sean ambiguos.','','No decidir por una sola palabra ni trasladar modelos sin prueba para completar una cifra. Una abertura alta no hace corto a un maxi; XL-154 conserva la excepción individual ya confirmada.','','## Cantidades aplicadas','','| Colección principal | Modelos | Total indicado | Diferencia pendiente |','|---|---:|---:|---:|']
for category in ('Largos','Gala','Cortos con brillo','Cortos','Bandage','Liquidación'):
    target={'Largos':25,'Cortos con brillo':43,'Cortos':30,'Bandage':22}.get(category)
    lines.append(f'| {category} | {totals[category]} | {target if target is not None else "—"} | {target-totals[category] if target is not None else "—"} |')
lines += ['','**Largos ya coincide en 25.** Los demás desajustes indicados siguen en investigación; no equivalen automáticamente a prendas nuevas ni a stock físico faltante.','','## Seis correcciones respaldadas','','| Código | Nombre conservado | Antes | Ahora | Evidencia |','|---|---|---|---|---|']
for item in changes:
    lines.append(f'| XL-{item["id"]:03d} | {item["nombre"]} | {item["antes"]} | {item["ahora"]} | {item["motivo"]} |')
lines += ['','[Matriz de nombres, precios, fotografías y fuentes](gala-largos/matriz.json). [Revisión visual y comercial](gala-largos/REPORTE.md).','','## Excepciones y conservación','','XL-068 y XL-081 pertenecen comercialmente a Cortos según las filas 17 y 28 del listado guardado, aunque sus fotografías lleguen al tobillo y XL-081 incluya «largo» en el nombre. Los modelos XL-062, XL-090, XL-101 y XL-107 regresan a Gala por sus referencias identificadas.','','XL-125 conserva su precio de oferta y su categoría principal Liquidación. La página de ofertas puede mostrar otros modelos con descuento, sin duplicar sus registros.','',''+summary['conservacion'],'']
(AUDIT/'CONCILIACION.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'cambios':len(changes),'totales':totals,'prendas':139,'fotos':225},ensure_ascii=False))
