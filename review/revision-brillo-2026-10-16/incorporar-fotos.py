from pathlib import Path
from PIL import Image
import json, re, hashlib, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
products=read(ROOT/'review/publicados-confirmados.json')
before=read(HERE/'productos-antes.json')
moved={54,118,121,122}
for old,p in zip(before,products):
    expected=dict(old)
    if old['id'] in moved:expected['category']='Cortos con brillo'
    assert p==expected,old['id']
assert len(products)==155
selection={38:[(10,1,'Frente, otra pose'),(10,2,'Frente, otra pose')],
40:[(12,2,'Frente, otra pose'),(12,3,'Espalda')],
149:[(16,2,'Frente, otra pose'),(16,3,'Frente, otra pose')],
51:[(23,1,'Frente, otra pose'),(23,2,'Espalda')],
150:[(25,3,'Prenda sin modelo')],
135:[(36,1,'Frente, otra pose'),(36,2,'Espalda, otra pose')],
132:[(41,2,'Espalda')],121:[(42,1,'Frente, otra pose')]}
added=[]
for p in products:
    for fila,n,view in selection.get(p['id'],[]):
        key=f'B{fila:02d}-{n}'
        source=HERE/f'{key}-foto.png'
        dest=ROOT/f'images/productos-reales/XL-{p["id"]:03d}/WA-Brillos-{key}.png'
        assert not dest.exists()
        shutil.copy2(source,dest)
        im=Image.open(dest)
        ph={'src':'./'+dest.relative_to(ROOT).as_posix(),'view':view,'width':im.width,'height':im.height,
            'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
            'sourceAttachment':source.relative_to(ROOT).as_posix(),
            'captureSource':{'pantalla':(HERE/f'{key}-pantalla.png').relative_to(ROOT).as_posix(),
                             'encuadre':(HERE/f'{key}-encuadre.json').relative_to(ROOT).as_posix()},
            'sourceCatalog':{'coleccion':'Vestidos Cortos Brillos','fila':fila,'fecha':'2026-10-16'}}
        p['photos'].append(ph); added.append({'id':p['id'],'foto':ph})
    if p['id'] in selection:
        p['photos']=[p['photos'][0]]+[ph for ph in p['photos'][1:] if ph['view'].startswith('Espalda')]+[ph for ph in p['photos'][1:] if not ph['view'].startswith('Espalda')]
assert len(added)==13
raw=(ROOT/'products.js').read_text(encoding='utf-8')
(ROOT/'products.js').write_text(re.sub(r'export const products = [\s\S]*?;(?=\s*export const categories)',lambda m:'export const products = '+json.dumps(products,ensure_ascii=False,indent=2)+';',raw,count=1),encoding='utf-8')
write(ROOT/'review/publicados-confirmados.json',products)
manifest=read(ROOT/'review/categorias-confirmadas.json')
manifest['revision']='conciliacion-catalogo-2026-10-15-brillo-completo-2026-10-16'
byid={p['id']:p for p in products}
for row in manifest['prendas']:
    p=byid[row['id']]
    row['fotos']=[{k:ph[k] for k in ['src','view','sha256']} for ph in p['photos']]
manifest['verificacion_brillo_actual']='43 fichas ampliadas y 68 imágenes de origen revisadas; 42 prendas únicas (XL-039 repetido). 13 fotos complementarias incorporadas a 8 modelos; 4 cruces trasladados exclusivamente a Cortos con brillo. Liquidación y precios conservados.'
write(ROOT/'review/categorias-confirmadas.json',manifest)
write(HERE/'fotos-incorporadas.json',added)
print('13 fotos incorporadas; 155 prendas, 264 fotos.')
