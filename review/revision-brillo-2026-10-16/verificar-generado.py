from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
import json,re,hashlib,unicodedata
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def slug(s):return re.sub(r'[^a-z0-9]+','-',''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').lower()).strip('-')
products=read(ROOT/'review/publicados-confirmados.json')
assert products==json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',(ROOT/'products.js').read_text(encoding='utf-8'))[1])
before=read(HERE/'productos-antes.json'); additions=read(HERE/'fotos-incorporadas.json')
assert len(products)==len(before)==155 and len(additions)==13
byid={p['id']:p for p in products}; assert len(byid)==155
for old in before:
    p=byid[old['id']]; expected=json.loads(json.dumps(old))
    if old['id'] in {54,118,121,122,172}:expected['category']='Cortos con brillo'
    extra=[a['foto'] for a in additions if a['id']==old['id']]
    if extra:
        photos=expected['photos']+extra
        expected['photos']=[photos[0]]+[ph for ph in photos[1:] if ph['view'].startswith('Espalda')]+[ph for ph in photos[1:] if not ph['view'].startswith('Espalda')]
    assert p==expected,old['id']
    assert p['photos'][0]['src']==old['photos'][0]['src'] and p['image']==old['image']
    if old.get('originalPrice',0)>old['price']:assert {k:v for k,v in p.items() if k!='category'}=={k:v for k,v in old.items() if k!='category'}
totals=dict(Counter(p['category'] for p in products))
assert totals=={'Gala':32,'Largos':25,'Cortos':32,'Bandage':22,'Cortos con brillo':43,'Liquidación':1}
assert sum(len(p['photos']) for p in products)==264
manifest=read(ROOT/'review/categorias-confirmadas.json')
for row in manifest['prendas']:
    p=byid[row['id']];assert row['categoria']==p['category'] and row['nombre']==p['name']
    assert row['fotos']==[{k:ph[k] for k in ['src','view','sha256']} for ph in p['photos']]
prices=read(HERE/'precios-verificados.json');assert len(prices)==43
assert all(byid[x['id']]['price']==x['price'] for x in prices)
assert len({x['id'] for x in prices})==42
assert len(list(HERE.glob('B*-resultado.json')))==43
for a in additions:
    ph=a['foto'];assert (ROOT/ph['src']).read_bytes()==(ROOT/ph['sourceAttachment']).read_bytes()
    assert hashlib.sha256((ROOT/ph['src']).read_bytes()).hexdigest()==ph['sha256']
for f in ['products.js','catalog-utils.js']:assert (ROOT/f).read_bytes()==(ROOT/'public'/f).read_bytes()
for p in products:
    text=(ROOT/'public/vestidos'/f'{p["id"]}-{p.get("urlSlug") or slug(p["name"])}'/'index.html').read_text(encoding='utf-8')
    graph=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',text)[1])['@graph']
    item=next(x for x in graph if x['@type']=='Product')
    assert item['name']==p['name'] and item['category']==p['category'] and float(item['offers']['price'])==p['price']
    assert [urlparse(u).path for u in item['image']]==[ph['src'].replace('./','/',1) for ph in p['photos']]
    for ph in p['photos']:assert (ROOT/ph['src']).read_bytes()==(ROOT/'public'/ph['src']).read_bytes()
collections={}
for category in totals:
    text=(ROOT/'public/colecciones'/slug(category)/'index.html').read_text(encoding='utf-8')
    actual=[int(v) for v in re.findall(r'data-id="(\d+)"',text)]
    expected=[p['id'] for p in products if (p.get('originalPrice',0)>p['price'] if category=='Liquidación' else p['category']==category)]
    assert len(actual)==len(set(actual)) and set(actual)==set(expected)
    assert f'{len(actual)} modelos en esta colección' in text
    collections[category]=len(actual)
assert collections['Liquidación']==10 and byid[172]['category']=='Cortos con brillo'
report={'fecha':'2026-10-16','revision':manifest['revision'],'prendas':155,'fotos':264,'fichas_whatsapp':43,'prendas_unicas_whatsapp':42,'fotos_incorporadas':13,'traslados':[54,118,121,122,172],'liquidacion_conservada':True,'categorias':totals,'colecciones_generadas':collections,'precios_coincidentes':43,'comprobaciones':'Conservación de las 155 prendas y 251 fotos previas, 13 complementos, precio de 43 fichas actuales, datos y manifiesto, 155 JSON-LD y membresías de colecciones sin duplicados.'}
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(HERE/'verificacion-web.json',report)
print(json.dumps(report,ensure_ascii=True))
