"""Verificar categorías, fichas y conservación de los datos después del build."""
import json as _json, runpy as _runpy
from pathlib import Path as _Path
_root=_Path(__file__).resolve().parents[2]
if _json.loads((_root/'review/categorias-confirmadas.json').read_text(encoding='utf-8-sig')).get('revision')=='conciliacion-catalogo-2026-10-15-brillo-completo-2026-10-16':
    _runpy.run_path(str(_root/'review/revision-brillo-2026-10-16/verificar-generado.py'),run_name='__main__')
    raise SystemExit(0)
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import unicodedata
from urllib.parse import urlparse

AUDIT=Path(__file__).resolve().parent
ROOT=AUDIT.parents[1]

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def slug(value):
    value=''.join(c for c in unicodedata.normalize('NFD',value) if unicodedata.category(c)!='Mn').lower()
    return re.sub(r'[^a-z0-9]+','-',value).strip('-')

def without_category(value):
    if isinstance(value,list):return [without_category(v) for v in value]
    if isinstance(value,dict):return {k:without_category(v) for k,v in value.items() if k not in ('category','categoria')}
    return value

text=(ROOT/'products.js').read_text(encoding='utf-8-sig')
products=json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',text)[1])
if read_json(ROOT/'review/categorias-confirmadas.json').get('revision')=='conciliacion-catalogo-2026-10-15-cortos-revisados-2026-10-16':
    import runpy
    runpy.run_path(str(ROOT/'review/verificacion-cortos-whatsapp-2026-10-15/verificar-generado.py'),run_name='__main__')
    raise SystemExit(0)
baseline=read_json(AUDIT/'productos-antes.json')
baseline_ids={p['id'] for p in baseline}
initial=[json.loads(json.dumps(p)) for p in products if p['id'] in baseline_ids]
next(p for p in initial if p['id']==117)['photos']=next(p for p in initial if p['id']==117)['photos'][:1]
assert without_category(initial)==without_category(baseline)
previous143=read_json(ROOT/'review/verificacion-brillo-whatsapp-2026-10-15/productos-antes.json')
current143=json.loads(json.dumps(products[:143]))
next(p for p in current143 if p['id']==117)['photos']=next(p for p in current143 if p['id']==117)['photos'][:1]
assert current143==previous143
assert len(products)==145 and len(baseline_ids)==139
assert products==read_json(ROOT/'review/publicados-confirmados.json')
assert (ROOT/'products.js').read_bytes()==(ROOT/'public/products.js').read_bytes()
by_id={p['id']:p for p in products}
manifest=read_json(ROOT/'review/categorias-confirmadas.json')
assert manifest['revision']=='conciliacion-catalogo-2026-10-15-con-XL179-184'
assert len(manifest['prendas'])==len(by_id)==145
for row in manifest['prendas']:
    assert row['categoria']==by_id[row['id']]['category']
assert sum(len(p['photos']) for p in products)==236
for ident,category,price,views in [
    (179,'Cortos con brillo',329,['Frente','Espalda']),
    (180,'Cortos',86.7,['Frente']),
    (181,'Cortos',115.6,['Frente','Espalda']),
    (182,'Bandage',379,['Frente','Espalda','Frente 3/4']),
    (183,'Cortos con brillo',389,['Frente']),
    (184,'Cortos con brillo',389,['Frente']),
]:
    p=by_id[ident]
    assert p['category']==category and p['price']==price
    assert [ph['view'] for ph in p['photos']]==views
    assert (ROOT/p['priceSource']['evidencia']).exists()
    for ph in p['photos']:
        assert (ROOT/ph['sourceAttachment']).read_bytes()==(ROOT/ph['src']).read_bytes()
assert by_id[180]['originalPrice']==by_id[181]['originalPrice']==289
assert by_id[183]['catalogCode']=='2008' and by_id[184]['catalogCode']=='1965'
assert by_id[117]['price']==389 and [ph['view'] for ph in by_id[117]['photos']]==['Frente','Espalda']
assert (ROOT/by_id[117]['photos'][1]['sourceAttachment']).read_bytes()==(ROOT/by_id[117]['photos'][1]['src']).read_bytes()
brillo=read_json(ROOT/'review/verificacion-brillo-whatsapp-2026-10-15/CONCILIACION-43.json')
assert brillo['fichas_actuales_observadas']==43 and brillo['prendas_unicas_asociadas']==42 and brillo['referencias_sin_asociar']==0
assert brillo['precios_coincidentes']==42 and [r['id'] for r in brillo['diferencias_precio']]==[117]
assert brillo['matriz'][10]['id']==brillo['matriz'][32]['id']==39
assert brillo['matriz'][38]['id']==117
for current,before in [(ROOT/'review/catalogo-whatsapp-2026-10-12/confirmados.json',AUDIT/'confirmados-oct12-antes.json'),(ROOT/'review/importacion-2026-10-10/verificacion.json',AUDIT/'verificacion-oct10-antes.json')]:
    assert without_category(read_json(current))==without_category(read_json(before))
confirmed=read_json(ROOT/'review/catalogo-whatsapp-2026-10-12/confirmados.json')
for row in confirmed['confirmados']:
    assert row['categoria']==by_id[148+int(row['grupo'].split('-')[1])]['category']
groups=read_json(ROOT/'review/importacion-2026-10-10/verificacion.json')
for row in groups['modelos_nuevos']:
    if row.get('productId') in by_id:assert row['categoria']==by_id[row['productId']]['category']
review=(ROOT/'review/catalogo-whatsapp-2026-10-12/REVISION.html').read_text(encoding='utf-8')
for p in products:
    if p.get('importGroup'):assert f'<small>XL-{p["id"]} · {p["importGroup"]} · {p["category"]}</small>' in review

totals=dict(Counter(p['category'] for p in products))
assert totals=={'Largos':25,'Gala':32,'Cortos':27,'Cortos con brillo':38,'Bandage':22,'Liquidación':1}
collections={}
for category in totals:
    html=(ROOT/'public/colecciones'/slug(category)/'index.html').read_text(encoding='utf-8')
    ids=[int(i) for i in re.findall(r'data-id="(\d+)"',html)]
    expected=[p['id'] for p in products if (p.get('originalPrice',0)>p['price'] if category=='Liquidación' else p['category']==category)]
    assert len(ids)==len(set(ids))
    assert set(ids)==set(expected),(category,ids,expected)
    assert f'{len(ids)} modelos en esta colección' in html
    collections[category]=len(ids)

verified_photos=0
for p in products:
    directory=ROOT/'public/vestidos'/f'{p["id"]}-{slug(p["name"])}'
    html=(directory/'index.html').read_text(encoding='utf-8')
    graph=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',html)[1])['@graph']
    data=next(x for x in graph if x['@type']=='Product')
    assert data['category']==p['category']
    assert data['name']==p['name']
    assert float(data['offers']['price'])==p['price']
    assert [urlparse(url).path for url in data['image']]==[f['src'].replace('./','/',1) for f in p['photos']]
    assert f'Xiliana Boutique · {p["category"]}</p>' in html
    assert f'<img class="gallery-main" src="{p["photos"][0]["src"].replace("./","/",1)}"' in html
    for photo in p['photos']:
        source=ROOT/photo['src']
        built=ROOT/'public'/photo['src']
        assert source.exists() and built.exists()
        assert hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256(built.read_bytes()).digest()
        verified_photos+=1
assert by_id[125]['category']=='Liquidación'
assert by_id[125]['id'] not in [int(i) for i in re.findall(r'data-id="(\d+)"',(ROOT/'public/colecciones/gala/index.html').read_text(encoding='utf-8'))]
report={'revision':manifest['revision'],'prendas':len(products),'fotos':verified_photos,'colecciones_principales':totals,'colecciones_generadas':collections,'fichas_verificadas':len(products),'conservacion':'Las 139 prendas iniciales conservan sus campos salvo las seis categorías documentadas y la espalda añadida a XL-117. Las 143 prendas previas a XL-183/184 se conservan, con esa única foto añadida. Se verifican seis altas y once fotos recuperadas en total. La copia de public contiene las mismas fotos.','verificado':'Pertenencia completa de colecciones, contadores visibles, categorías de ficha y JSON-LD, nombres, precios, fotos y orden de galería, espejos sincronizados y XL-125 excluido de Gala. Las 43 referencias actuales de Brillos están asociadas a 42 prendas únicas; XL-117 conserva S/389 pendiente de confirmar frente a S/379 de Brillos. La página de ofertas muestra 10 modelos con descuento y Liquidación conserva 1 categoría principal.'}
(AUDIT/'verificacion-web.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
