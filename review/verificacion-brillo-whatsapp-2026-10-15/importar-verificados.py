"""Añadir dos modelos verificados y la espalda de XL-117 sin duplicar alias."""
from pathlib import Path
from collections import Counter
import json, re, hashlib, shutil
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

raw = (ROOT/'products.js').read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', raw)
before = json.loads(match[1])
assert len(before) == 143 and max(p['id'] for p in before) == 182
assert before == read(HERE/'productos-antes.json')
manifest = read(ROOT/'review/categorias-confirmadas.json')
assert manifest['revision'] == 'conciliacion-catalogo-2026-10-15-con-XL179-182'
backup = HERE/'respaldo-importacion'
assert not backup.exists()
backup.mkdir()
for name in ['products.js','review/publicados-confirmados.json','review/categorias-confirmadas.json']:
    shutil.copy2(ROOT/name, backup/Path(name).name)
save(backup/'productos-antes.json', before)
products = json.loads(json.dumps(before))
by_id = {p['id']:p for p in products}

def photo(ident, key, filename, view):
    source = HERE/(key+'-foto.png')
    target = ROOT/f'images/productos-reales/XL-{ident:03d}'/filename
    assert source.exists() and not target.exists()
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(source, target)
    with Image.open(source) as im:
        width, height = im.size
    return {'src':'./'+target.relative_to(ROOT).as_posix(), 'width':width, 'height':height,
            'view':view, 'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'sourceAttachment':source.relative_to(ROOT).as_posix(),
            'sourceType':'Captura de fotografía del catálogo WhatsApp Web',
            'captureSource':{'pantalla':(HERE/(key+'-pantalla.png')).relative_to(ROOT).as_posix(),
                             'encuadre':(HERE/(key+'-encuadre.json')).relative_to(ROOT).as_posix(),
                             'edicion':'Recorte de la interfaz; sin alterar vestido, modelo, color ni fondo.'}}

definitions = [
    (183, 'Vestido corto azul pedrería y strass', '2008', 'azul389',
     'Mini azul con cuello separado de pedrería, hombros con cadenas y strass extendido por cuerpo y falda. Distinto de XL-179 de satín y tul, XL-016 con plumas, XL-051/052 de lentejuelas, XL-133 de manga larga y los demás modelos guardados.'),
    (184, 'Vestido dorado corto asimétrico de flecos', '1965', 'dorado389',
     'Mini dorado de un hombro, con flecos rectos superpuestos y base brillante. Distinto de XL-129 Bandage código 2070, que tiene escote en V y flecos diagonales, y de XL-017 de una manga. Revisión contra las fotos de las 143 prendas anteriores.'),
]
for ident, name, code, key, comparison in definitions:
    ph = photo(ident, key, f'01-WA{code}-frente.png', 'Frente')
    p = {'id':ident, 'name':name, 'category':'Cortos con brillo', 'price':389,
         'photos':[ph], 'image':ph['src'], 'photoPending':False,
         'note':'Elige tus accesorios favoritos y dale tu toque a este diseño. Podemos orientarte sobre medidas, ajustes y disponibilidad.',
         'catalogName':name, 'catalogCode':code, 'catalogCategory':'Vestidos Cortos Brillos',
         'priceSource':{'tipo':'WhatsApp Web', 'telefono':'+51 930 527 248', 'fecha':'2026-10-15',
                        'evidencia':(HERE/(key+'-ficha.png')).relative_to(ROOT).as_posix()},
         'imageSource':{'tipo':'Captura del catálogo WhatsApp Web, misma pestaña del usuario',
                        'fecha':'2026-10-15', 'comparacion':comparison,
                        'procedencia':'Fotografía oficial ampliada y recortada al área de imagen, sin modificaciones visuales.'}}
    products.append(p)
    manifest['prendas'].append({'id':ident, 'nombre':name, 'categoria':p['category'],
                               'fecha':'2026-10-15', 'fuente':p['priceSource']['evidencia'],
                               'motivo':comparison+' Brillo predominante en vestido corto; ficha comercial en Brillos.',
                               'fotos':[{k:ph[k] for k in ['src','view','sha256']}]})

# Misma prenda que XL-117: conservar nombre, precio y frente originales, añadir solo la espalda.
assert by_id[117]['price'] == 389 and len(by_id[117]['photos']) == 1
back = photo(117, 'negro379-2', '02-WA2062-espalda.png', 'Espalda')
by_id[117]['photos'].append(back)
row117 = next(r for r in manifest['prendas'] if r['id']==117)
row117['fotos'].append({k:back[k] for k in ['src','view','sha256']})
row117['verificacion_adicional'] = 'Ficha Brillos código 2062: mismo diseño que XL-117. Se añade su espalda. El precio de Brillos S/379 difiere del precio guardado S/389: se registra para confirmar, conservando el precio existente.'

for old, current in zip(before, products[:143]):
    if old['id']==117:
        trimmed = json.loads(json.dumps(current))
        trimmed['photos'] = trimmed['photos'][:1]
        assert trimmed == old
    else:
        assert current == old
assert len(products)==145 and sum(len(p['photos']) for p in products)==236
totals = dict(Counter(p['category'] for p in products))
assert totals == {'Gala':32,'Largos':25,'Cortos':27,'Bandage':22,'Cortos con brillo':38,'Liquidación':1}
manifest['revision'] = 'conciliacion-catalogo-2026-10-15-con-XL179-184'
manifest['verificacion_brillo_actual'] = '43 fichas observadas en la misma sesión WhatsApp: dos altas XL-183/184, alias verde fila 33=XL-039 y negro fila 39=XL-117. La espalda de XL-117 se añade sin duplicar la prenda. Diferencia de precio de XL-117 pendiente de confirmar.'
(ROOT/'products.js').write_text(raw[:match.start(1)]+json.dumps(products,ensure_ascii=False,indent=2)+raw[match.end(1):],encoding='utf-8')
save(ROOT/'review/publicados-confirmados.json', products)
save(ROOT/'review/categorias-confirmadas.json', manifest)
save(HERE/'resultado-importacion.json', {'revision':manifest['revision'], 'total_prendas':145,
     'total_fotos':236, 'totales':totals, 'altas':[183,184], 'foto_adicional':{'id':117,'vista':'Espalda'},
     'alias_sin_duplicar':[{'fila':33,'id':39},{'fila':39,'id':117}],
     'precio_pendiente':{'id':117,'web':389,'ficha_brillos':379},
     'conservacion':'Las 143 prendas anteriores mantienen sus campos; XL-117 añade únicamente su fotografía de espalda.'})
print(json.dumps({'prendas':len(products),'fotos':236,'totales':totals},ensure_ascii=False))
