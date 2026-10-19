from pathlib import Path
from collections import Counter
import re, json, unicodedata, hashlib

ROOT=Path(__file__).resolve().parents[4]
AUDIT=ROOT/'review/conciliacion-final-2026-10-15'
HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
products=json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',(ROOT/'products.js').read_text(encoding='utf-8'))[1])
before=json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',(HERE/'products.js').read_text(encoding='utf-8'))[1])
assert products[:-1]==before and len(before)==139 and len(products)==140
assert products==read(ROOT/'review/publicados-confirmados.json')
manifest=read(ROOT/'review/categorias-confirmadas.json')
entries={p['id']:p for p in manifest['prendas']}
assert len(entries)==len(manifest['prendas'])==140
assert len({p['id'] for p in products})==140
slug=lambda s:re.sub(r'[^a-z0-9]+','-', ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').lower()).strip('-')
for p in products:
    assert entries[p['id']]['categoria']==p['category']
    assert entries[p['id']]['nombre']==p['name']
    assert p['price'] is not None and p['price']>0
    route=f"/vestidos/{p['id']}-{slug(p['name'])}/"
    html=(ROOT/'public'/route.strip('/')/'index.html').read_text(encoding='utf-8')
    graph=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',html)[1])['@graph']
    item=next(x for x in graph if x['@type']=='Product')
    assert item['name']==p['name'] and item['category']==p['category']
    assert float(item['offers']['price'])==p['price']
    assert item['size']=='Estándar'
    assert len(item['image'])==len(p['photos'])
    for f,img in zip(p['photos'],item['image']):
        assert img.endswith(f['src'].removeprefix('.'))
        src=ROOT/f['src'].removeprefix('./')
        public=ROOT/'public'/f['src'].removeprefix('./')
        assert hashlib.sha256(src.read_bytes()).hexdigest()==f['sha256']
        assert src.read_bytes()==public.read_bytes()
    assert p['photos'][0]['view'].startswith('Frente')
    assert p['image']==p['photos'][0]['src']

collections={}
for category in Counter(p['category'] for p in products):
    expected={p['id'] for p in products if (p.get('originalPrice',0)>p['price'] if category=='Liquidación' else p['category']==category)}
    html=(ROOT/'public/colecciones'/slug(category)/'index.html').read_text(encoding='utf-8')
    actual=[int(x) for x in re.findall(r'data-id="(\d+)"',html)]
    assert len(actual)==len(set(actual))
    assert set(actual)==expected, (category,set(actual)^expected)
    assert f'{len(actual)} modelos en esta colección' in html
    collections[category]=len(actual)
new=products[-1]
assert new['id']==179 and new['catalogCode']=='182' and new['price']==329
assert [p['view'] for p in new['photos']]==['Frente','Espalda']
assert {p['id']:p['category'] for p in products if p['id'] in (62,68,81,90,101,107)}=={62:'Gala',68:'Cortos',81:'Cortos',90:'Gala',101:'Gala',107:'Gala'}
result={'revision':manifest['revision'],'prendas':140,'fotos':sum(len(p['photos']) for p in products),'prendas_previas_sin_cambios':139,'fotos_previas_sin_cambios':225,'totales_principales':dict(Counter(p['category'] for p in products)),'colecciones_generadas':collections,'XL179':{'nombre':new['name'],'precio':329,'codigo':'182','categoria':new['category'],'orden_galeria':['Frente','Espalda'],'ruta':'/vestidos/179-vestido-corto-azul/'},'conciliacion_inventario_cerrada':False,'verificado':'140 fichas generadas con nombres, categorías, precios, fotos y orden correctos; manifiesto y espejo publicados sincronizados; activos copiados idénticos; seis correcciones conservadas.'}
(HERE/'verificacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(AUDIT/'verificacion-web.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
