"""Aplica la confirmación específica más reciente: XL-117 en Brillos a S/379."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TEMP = Path(r'C:/Users/USER/AppData/Local/Temp')
SOURCE = ROOT / 'products.js'
text = SOURCE.read_text(encoding='utf-8')
products = json.loads(text.split('export const products = ', 1)[1].split('];', 1)[0] + ']')
product = next(p for p in products if p['id'] == 117)
before = json.loads(json.dumps(product))
assert len(products) == 177 and product['category'] == 'Gala' and product['price'] == 389
liquidacion = [p for p in products if p['category'] == 'Liquidación']
assert len(liquidacion) == 11
photos = []
for attachment, filename, view in [
    ('codex-clipboard-766c8f00-baae-4be3-8601-2399e4f86a97.png', '03-propietario-frente.png', 'Frente'),
    ('codex-clipboard-6fd194c0-72b2-441c-a77c-5e72aa699adb.png', '04-propietario-espalda.png', 'Espalda'),
]:
    source = TEMP / attachment
    with Image.open(source) as image:
        image.verify()
    with Image.open(source) as image:
        width, height = image.size
    dest = ROOT / 'images/productos-reales/XL-117' / filename
    shutil.copyfile(source, dest)
    photos.append({'src': f'./images/productos-reales/XL-117/{filename}', 'width': width, 'height': height,
                   'view': view, 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
                   'sourceAttachment': attachment, 'sourceType': 'Foto original entregada por el propietario el 20/10/2026'})

product.update({
    'name': 'Vestido elegante estraple negro con plateado',
    'urlSlug': 'vestido-negro-brillante',
    'category': 'Cortos con brillo', 'price': 379,
    'catalogName': 'Vestido elegante estraple negro con plateado',
    'catalogCategory': 'Vestidos Cortos Brillos', 'catalogCode': '2062',
    'photos': photos + product['photos'], 'image': photos[0]['src'],
    'priceSource': {'tipo': 'Confirmación específica del propietario', 'fecha': '2026-10-20', 'codigoCatalogo': '2062',
                    'evidencia': 'review/revision-brillos-2026-10-20/confirmacion-xl117.json'},
    'ownerConfirmation': {'fecha': '2026-10-20', 'categoria': 'Cortos con brillo', 'precio_pen': 379,
                           'codigo_whatsapp': '2062', 'evidencia': 'review/revision-brillos-2026-10-20/confirmacion-xl117.json',
                           'prioridad': 'Confirmación posterior que sustituye Gala a S/389 del 16/10.'},
})
start = text.index('  {\n    "id": 117,')
end = text.index('  {\n    "id": 118,', start)
block = '  ' + json.dumps(product, ensure_ascii=False, indent=2).replace('\n', '\n  ') + ',\n'
SOURCE.write_text(text[:start] + block + text[end:], encoding='utf-8')
(ROOT / 'review/publicados-confirmados.json').write_text(json.dumps(products, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert [p for p in products if p['category'] == 'Liquidación'] == liquidacion
confirmation = {'fecha': '2026-10-20', 'id_web': 'XL-117',
    'instruccion_previa': 'Las fotos siguientes son de Cortos con brillo; mover inmediatamente la ficha si aparece en otra categoría. Liquidación queda excluida de cualquier traslado.',
    'mensaje_propietario': 'Vestido elegante estraple negro con plateado; PEN 379.00; Prendas Importadas; 2062',
    'decision': 'Misma prenda que XL-117 por frente y espalda; cambiar Gala por Cortos con brillo y S/389 por S/379; conservar ID y URL.',
    'antes': before, 'despues': product, 'liquidacion_sin_cambios': True,
    'fotos_anteriores_conservadas': True, 'nuevo_producto_creado': False}
(OUT / 'confirmacion-xl117.json').write_text(json.dumps(confirmation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('XL-117 actualizado: Cortos con brillo, S/379, código2062, cuatro fotos; Liquidación intacta.')
