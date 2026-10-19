"""Incorporar una prenda identificada en WhatsApp sin alterar las 139 existentes."""
from pathlib import Path
from collections import Counter
from PIL import Image
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'review/conciliacion-final-2026-10-15'
CAPTURES = AUDIT / 'whatsapp-actual'
BACKUP = CAPTURES / 'importacion-XL179'
SOURCE = ROOT / 'products.js'
MANIFEST = ROOT / 'review/categorias-confirmadas.json'
REVISION = 'conciliacion-catalogo-2026-10-15-con-XL179'

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

text = SOURCE.read_text(encoding='utf-8-sig')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])
manifest = read_json(MANIFEST)
assert manifest['revision'] == 'conciliacion-catalogo-2026-10-15', 'Revisar el catálogo actual antes de repetir esta importación.'
assert len(products) == 139 and len({p['id'] for p in products}) == 139
assert 179 not in {p['id'] for p in products}
assert sum(len(p['photos']) for p in products) == 225
assert read_json(ROOT / 'review/publicados-confirmados.json') == products
assert Counter(p['category'] for p in products) == {'Largos':25, 'Gala':32, 'Cortos':25, 'Cortos con brillo':35, 'Bandage':21, 'Liquidación':1}
assert {p['id']:p['category'] for p in products if p['id'] in (62,68,81,90,101,107)} == {62:'Gala',68:'Cortos',81:'Cortos',90:'Gala',101:'Gala',107:'Gala'}
before = json.loads(json.dumps(products))
BACKUP.mkdir(parents=True, exist_ok=True)
for path in [SOURCE, MANIFEST, ROOT/'review/publicados-confirmados.json', AUDIT/'resultado-aplicado.json', AUDIT/'CONCILIACION.md']:
    target = BACKUP / path.name
    assert not target.exists(), 'La copia previa ya existe; revisar antes de reimportar.'
    shutil.copy2(path, target)

photos = []
dest = ROOT / 'images/productos-reales/XL-179'
assert not dest.exists(), 'No sobrescribir una carpeta de producto ya existente.'
dest.mkdir()
for n, view in enumerate(('Frente','Espalda'), 1):
    name = view.lower()
    source = CAPTURES / f'brillo-azul329-{name}.png'
    target = dest / f'{n:02d}-WA182-{name}.png'
    shutil.copy2(source, target)
    assert target.read_bytes() == source.read_bytes()
    with Image.open(target) as img:
        width, height = img.size
    photos.append({
        'src':'./'+target.relative_to(ROOT).as_posix(), 'width':width, 'height':height,
        'view':view, 'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'sourceAttachment':source.relative_to(ROOT).as_posix(),
        'sourceType':'Captura de fotografía del catálogo WhatsApp Web',
        'captureSource':{
            'pantalla':(CAPTURES/f'brillo-azul329-{name}-pantalla.png').relative_to(ROOT).as_posix(),
            'encuadre':(CAPTURES/f'brillo-azul329-{name}-encuadre.json').relative_to(ROOT).as_posix(),
            'edicion':'Recorte al área de la fotografía; sin cambiar modelo, vestido, colores ni fondo de la fotografía.'
        }
    })
product = {
    'id':179, 'name':'Vestido corto azul', 'category':'Cortos con brillo', 'price':329,
    'photos':photos, 'image':photos[0]['src'], 'photoPending':False,
    'note':'Un toque de brillo para tu próxima noche especial. Combínalo a tu gusto y deja que tu sonrisa complete el look.',
    'catalogName':'Vestido corto azul', 'catalogCode':'182', 'catalogCategory':'Vestidos Cortos Brillos',
    'priceSource':{
        'tipo':'WhatsApp Web', 'telefono':'+51 930 527 248', 'fecha':'2026-10-15',
        'evidencia':(CAPTURES/'brillo-azul329-ficha-completa.png').relative_to(ROOT).as_posix()
    },
    'imageSource':{
        'tipo':'Capturas del catálogo WhatsApp Web', 'fecha':'2026-10-15',
        'codigo':'182', 'coleccion':'Vestidos Cortos Brillos',
        'comparacion':'Las 139 fotografías principales existentes, incluidas XL-051, XL-052 y XL-133, muestran modelos distintos. Frente y espalda de esta ficha corresponden al mismo vestido azul mini con satén, tul y lentejuelas.',
        'procedencia':'La interfaz no permitió descargar el blob. Se conservaron las capturas completas y los rectángulos de recorte como evidencia.'
    }
}
products.append(product)
assert products[:-1] == before
assert sum(len(p['photos']) for p in products) == 227
assert photos[0]['view'] == 'Frente' and photos[1]['view'] == 'Espalda'
assert len({p['sha256'] for p in photos}) == 2
assert not ({p['sha256'] for p in photos} & {f['sha256'] for p in before for f in p['photos']})
assert len(manifest['prendas']) == 139
manifest['prendas'].append({
    'id':179, 'nombre':product['name'], 'categoria':product['category'], 'fecha':'2026-10-15',
    'fuente':product['priceSource']['evidencia'], 'codigo_catalogo':'182',
    'motivo':'Mini azul con lentejuelas extendidas en falda y mangas; referencia exacta de Cortos con brillo. Nombre y precio S/329 verificados en la ficha actual. Distinto de las 139 prendas previamente publicadas.',
    'fotos':[{k:p[k] for k in ('src','view','sha256')} for p in photos]
})
manifest.update(revision=REVISION, fecha='2026-10-15')
replacement=json.dumps(products, ensure_ascii=False, indent=2)
SOURCE.write_text(text[:match.start(1)] + replacement + text[match.end(1):], encoding='utf-8')
write_json(ROOT/'review/publicados-confirmados.json', products)
write_json(MANIFEST, manifest)

totals = dict(Counter(p['category'] for p in products))
summary = read_json(AUDIT/'resultado-aplicado.json')
assert len(summary['cambios']) == 6
summary.update(revision=REVISION, total_prendas=140, total_fotos=227, totales=totals,
    altas=[{'id':179, 'nombre':product['name'], 'categoria':product['category'], 'precio':329, 'codigo_catalogo':'182', 'fotos':2, 'evidencia':product['priceSource']['evidencia']}],
    diferencias_pendientes={'Largos':0, 'Cortos con brillo':7, 'Cortos':5},
    conciliacion_inventario_cerrada=False,
    conservacion='Se mantienen las seis correcciones de categoría. Las 139 prendas anteriores conservan todos sus campos, precios, nombres, identificadores, fotos y orden. Se añade XL-179 con dos capturas de fotografías verificadas del catálogo actual, frente primero.',
    pendientes=['Cortos con brillo: faltan conciliar siete referencias frente al total indicado de 43.', 'Cortos: faltan conciliar cinco referencias frente al total indicado de 30.', 'Bandage conserva 21 modelos; el total histórico indicado fue 22.', 'XL-107 y XL-175 comparten nombre base y precio, pero sus fotos muestran modelos diferentes; no fusionarlos.'])
write_json(AUDIT/'resultado-aplicado.json', summary)
doc=(AUDIT/'CONCILIACION.md').read_text(encoding='utf-8')
doc=doc.replace('**Seis ubicaciones corregidas; 139 prendas y 225 fotos conservadas.**', '**Seis ubicaciones corregidas y una prenda recuperada del catálogo actual: 140 prendas y 227 fotos.**')
doc=doc.replace('| Cortos con brillo | 35 | 43 | 8 |', '| Cortos con brillo | 36 | 43 | 7 |')
doc=doc.replace('Solo se modificaron seis categorías. Se conservan idénticos todos los nombres, precios, identificadores, fotografías, orden de galerías y orden de registros.', summary['conservacion'])
doc+='\n## Prenda recuperada del catálogo actual\n\n**XL-179 · Vestido corto azul · S/ 329 · código de catálogo 182 · Cortos con brillo.** Frente y espalda identificados en la misma ficha actual. Se comparó con las 139 prendas anteriores; el diseño de satén azul en el escote, tul y lentejuelas en mangas y minifalda es distinto de XL-051, XL-052, XL-133 y los demás modelos.\n\nSe incorporaron dos capturas recortadas al área de la fotografía sin alterar vestido, modelo ni fondo. [Ficha completa](whatsapp-actual/brillo-azul329-ficha-completa.png), [frente](whatsapp-actual/brillo-azul329-frente.png) y [espalda](whatsapp-actual/brillo-azul329-espalda.png). Las capturas completas y los encuadres se conservan junto a esas imágenes. La portada es el frente y la segunda foto es la espalda.\n\nBrillo pasa de 35 a 36; la conciliación de 43 Brillo y 30 Cortos sigue abierta.\n'
(AUDIT/'CONCILIACION.md').write_text(doc, encoding='utf-8')
write_json(BACKUP/'resultado.json', {'revision':REVISION, 'alta':179, 'prendas_anteriores_intactas':139, 'fotos_anteriores_intactas':225, 'prendas':140, 'fotos':227, 'totales':totals, 'metas_completas':False})
print(json.dumps({'alta':179, 'prendas':len(products), 'fotos':227, 'totales':totals}, ensure_ascii=False))
