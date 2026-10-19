"""Verificar conservación, precios WhatsApp, galerías y páginas generadas."""
import json as _json, runpy as _runpy
from pathlib import Path as _Path
_root=_Path(__file__).resolve().parents[2]
if _json.loads((_root/'review/categorias-confirmadas.json').read_text(encoding='utf-8-sig')).get('revision')=='conciliacion-catalogo-2026-10-15-brillo-completo-2026-10-16':
    _runpy.run_path(str(_root/'review/revision-brillo-2026-10-16/verificar-generado.py'),run_name='__main__')
    raise SystemExit(0)
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
import json,re,hashlib,unicodedata

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def slug(s):return re.sub(r'[^a-z0-9]+','-',''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').lower()).strip('-')
products=read(ROOT/'review/publicados-confirmados.json')
raw=(ROOT/'products.js').read_text(encoding='utf-8')
assert products==json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',raw)[1])
before=read(HERE/'productos-antes.json')
assert len(before)==145 and len(products)==155
by_id={p['id']:p for p in products}
assert len(by_id)==155 and 187 not in by_id
for old,current in zip(before,products[:145]):
    expected=json.loads(json.dumps(old))
    if old['id']==69:
        expected.update(name='Vestido corto drapeado de mangas',price=379,catalogName='vestido corto drapeado de mangas',urlSlug='vestido-drapeado-azul-asimetrico',priceSource=current['priceSource'])
        assert current['priceSource']['evidencia'].endswith('F32-mangas379-ficha.png')
    elif old['id']==117:
        expected.update(price=379,priceSource=current['priceSource'])
        assert current['priceSource']['evidencia'].endswith('negro379-ficha.png')
    elif old['id']==64:expected['photos']=[old['photos'][i] for i in [0,2,1]]
    assert current==expected,old['id']
assert by_id[66]['price']==429 and by_id[131]['price']==389 and by_id[127]['price']==549
assert [ph['view'] for ph in by_id[64]['photos']]==['Frente','Espalda','Frente']
assert [ph['view'] for ph in by_id[185]['photos']]==['Frente','Espalda']
assert [ph['view'] for ph in by_id[186]['photos']]==['Frente','Espalda','Frente, otra pose','Frente, otra pose']
assert [ph['view'] for ph in by_id[189]['photos']]==['Frente','Espalda']
expected_prices={185:249,186:289,188:299,189:239,190:369,191:229,192:389,193:389,194:289,195:319}
assert {p['id'] for p in products[145:]}==set(expected_prices)
for ident,price in expected_prices.items():
    p=by_id[ident]
    assert p['price']==price and p['category']=='Cortos'
    assert p['photos'][0]['view']=='Frente' and p['image']==p['photos'][0]['src']
    assert (ROOT/p['priceSource']['evidencia']).exists()
    for ph in p['photos']:
        assert (ROOT/ph['src']).read_bytes()==(ROOT/ph['sourceAttachment']).read_bytes()
        assert hashlib.sha256((ROOT/ph['src']).read_bytes()).hexdigest()==ph['sha256']
        assert (ROOT/ph['captureSource']['pantalla']).exists() and (ROOT/ph['captureSource']['encuadre']).exists()
totals=dict(Counter(p['category'] for p in products))
assert totals=={'Gala':32,'Largos':25,'Cortos':37,'Bandage':22,'Cortos con brillo':38,'Liquidación':1}
assert sum(len(p['photos']) for p in products)==251
manifest=read(ROOT/'review/categorias-confirmadas.json')
assert manifest['revision']=='conciliacion-catalogo-2026-10-15-cortos-revisados-2026-10-16'
assert len(manifest['prendas'])==155
for row in manifest['prendas']:
    p=by_id[row['id']]
    assert row['categoria']==p['category'] and row['nombre']==p['name']
    assert row['fotos']==[{k:ph[k] for k in ['src','view','sha256']} for ph in p['photos']]
result=read(HERE/'CONCILIACION-33.json')
assert result['fichas_observadas']==33 and result['prendas_unicas_identificadas']==31
assert result['referencias_sin_identidad']==0 and result['prendas_fuente_publicadas']==30
assert result['precios_fichas_coincidentes']==30
assert result['matriz'][5]['id_reservado']==result['matriz'][9]['id_reservado']==187
assert result['matriz'][12]['id_web']==result['matriz'][14]['id_web']==66
pending=read(HERE/'XL-187-PENDIENTE.json')
assert pending['precios_catalogo']==[329,319] and pending['estado'].startswith('No publicado')
assert (ROOT/'public/products.js').read_bytes()==(ROOT/'products.js').read_bytes()
assert (ROOT/'public/catalog-utils.js').read_bytes()==(ROOT/'catalog-utils.js').read_bytes()
assert 'product.urlSlug || slug(product.name)' in (ROOT/'catalog-utils.js').read_text()
verified_photos=0
for p in products:
    urlslug=p.get('urlSlug') or slug(p['name'])
    path=ROOT/'public/vestidos'/f'{p["id"]}-{urlslug}'/'index.html'
    text=path.read_text(encoding='utf-8')
    graph=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',text)[1])['@graph']
    item=next(x for x in graph if x['@type']=='Product')
    assert item['name']==p['name'] and item['category']==p['category']
    assert float(item['offers']['price'])==p['price']
    assert [urlparse(u).path for u in item['image']]==[ph['src'].replace('./','/',1) for ph in p['photos']]
    assert f'<img class="gallery-main" src="{p["photos"][0]["src"].replace("./","/",1)}"' in text
    for ph in p['photos']:
        assert (ROOT/ph['src']).read_bytes()==(ROOT/'public'/ph['src']).read_bytes()
        verified_photos+=1
collections={}
for category in totals:
    text=(ROOT/'public/colecciones'/slug(category)/'index.html').read_text(encoding='utf-8')
    actual=[int(v) for v in re.findall(r'data-id="(\d+)"',text)]
    expected=[p['id'] for p in products if (p.get('originalPrice',0)>p['price'] if category=='Liquidación' else p['category']==category)]
    assert len(actual)==len(set(actual)) and set(actual)==set(expected)
    assert f'{len(actual)} modelos en esta colección' in text
    collections[category]=len(actual)
assert by_id[125]['category']=='Liquidación' and collections['Liquidación']==10
assert (ROOT/'public/vestidos/69-vestido-drapeado-azul-asimetrico/index.html').exists()
report={'fecha':'2026-10-16','revision':manifest['revision'],'prendas':155,'fotos':verified_photos,
        'fichas_verificadas':155,'colecciones_principales':totals,'colecciones_generadas':collections,
        'conservacion':'145 prendas previas conservadas salvo las correcciones exactas de nombre/precio/URL estable de XL-069, precio WhatsApp de XL-117 y orden de galería de XL-064. Ninguna foto previa ni categoría previa modificada.',
        'altas':10,'fotos_nuevas':15,'pendiente_sin_publicar':187,
        'comprobaciones':'Datos y manifiesto sincronizados, 33 referencias y dos duplicados, precios WhatsApp, fotos capturadas y publicadas iguales, orden frente/espalda, 155 fichas y JSON-LD, colecciones completas sin duplicados y URL histórica de XL-069 conservada.'}
(HERE/'verificacion-web.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'review/conciliacion-final-2026-10-15/verificacion-web.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))
