import json,re,shutil,hashlib,html
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
source=root/'products.js'
text=source.read_text(encoding='utf-8-sig')
products=json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',text)[1])
categories=json.loads(re.search(r'export const categories = ([\s\S]*?);',text)[1])
byid={p['id']:p for p in products}
byid[117]['category']='Cortos con brillo'
byid[127].update(name='Vestido corto vino con pedrería y caída lateral',category='Cortos',price=None,pricePending=True,namePending=True,note='Un diseño coqueto con brillo y una caída lateral que acompaña cada paso. Consulta su precio con la boutique.')
byid[127].pop('originalPrice',None)
# Stable IDs preserve existing URLs; the long wine dress receives its own record.
definitions=[
 (136,'Vestido largo de gala verde agua de lentejuelas','Gala',649,[(1,'Frente'),(2,'Espalda')]),
 (137,'Vestido sirena palo rosa de lentejuelas','Gala',569,[(4,'Frente'),(5,'Frente · otra pose')]),
 (138,'Vestido palo rosa gasa y satín','Gala',649,[(6,'Frente'),(7,'Espalda')]),
 (139,'Vestido largo azul acero','Gala',699,[(8,'Frente'),(10,'Espalda'),(9,'Frente · otra pose')]),
 (140,'Vestido vino strapless de tirantes con copas de pedrería','Gala',549,[(11,'Frente'),(12,'Frente · otra pose')]),
 (141,'Vestido largo azul','Gala',349,[(13,'Frente')]),
 (142,'Vestido largo de gala rojo de malla con lentejuelas','Gala',719,[(14,'Frente'),(15,'Frente · otra pose')]),
 (143,'Vestido Bandage blanco y crema de perlas','Bandage',549,[(17,'Frente')]),
 (144,'VESTIDO BANDAGE Caqui ceñido','Bandage',379,[(20,'Frente')]),
 (145,'Bandage Dress negro con pedrería','Bandage',349,[(22,'Frente'),(23,'Espalda'),(24,'Frente · detalle')]),
 (146,'Bandage Dress de colores','Bandage',399,[(25,'Frente'),(26,'Espalda')]),
 (147,'Vestido Bandage negro con blanco','Bandage',None,[(27,'Frente')]),
 (148,'Vestido Bandage de franjas azules, celestes y rosadas','Bandage',None,[(28,'Frente')])]
manifest=json.loads((root/'review/importacion-2026-10-08/inventario.json').read_text())
for ident,name,cat,price,shots in definitions:
    photos=[]
    directory=root/f'images/productos-reales/XL-{ident:03}'
    directory.mkdir(parents=True,exist_ok=True)
    for position,(n,view) in enumerate(shots,1):
        item=manifest[n-1]; src=root/item['path']; dst=directory/f'{position:02}-N{n:03}.jpeg'
        shutil.copy2(src,dst)
        with Image.open(dst) as im: width,height=im.size
        photos.append(dict(src='./'+dst.relative_to(root).as_posix(),width=width,height=height,sha256=item['sha256'],view=view,sourceAttachment=item['path']))
    p=dict(id=ident,name=name,category=cat,price=price,note='Un look para sentirte preciosa y darle tu toque a la celebración. Combínalo con tus accesorios favoritos.',photos=photos,image=photos[0]['src'],photoPending=False)
    if price is None: p.update(pricePending=True,namePending=True)
    byid[ident]=p
products=list(byid.values())
video_confirmations=root/'review/video-catalogo-2026-10-08/confirmaciones.json'
if video_confirmations.exists():
    for confirmation in json.loads(video_confirmations.read_text(encoding='utf-8'))['confirmados']:
        if 'id' not in confirmation: continue
        p=byid[confirmation['id']]
        p.update(name=confirmation['nombre'],price=confirmation['precio'])
        p.pop('pricePending',None);p.pop('namePending',None)
        if confirmation.get('precio_regular'):p['originalPrice']=confirmation['precio_regular']
        p['priceSource']=confirmation.get('fuente',{'video':'20261009-0005-03.6416792.mp4','second':confirmation.get('segundo')})
        if confirmation['id']==127: p['note']='Haz de tu entrada un momento inolvidable. Su diseño asimétrico y caída lateral te acompañan para celebrar, posar y sentirte preciosa a tu manera.'
source.write_text('// Catálogo con fotografías originales. Los precios pendientes se consultan con la boutique.\nexport const products = '+json.dumps(products,ensure_ascii=False,indent=2)+';\nexport const categories = '+json.dumps(categories,ensure_ascii=False)+';\n',encoding='utf-8')
(root/'review/publicados-confirmados.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
pendingfile=root/'review/gala-sin-foto-confirmada.json'
pending=json.loads(pendingfile.read_text(encoding='utf-8-sig'))
known={name.casefold() for _,name,_,price,_ in definitions if price is not None}
if isinstance(pending,list):
    pending=[p for p in pending if p.get('nombre','').casefold() not in known]
    pendingfile.write_text(json.dumps(pending,ensure_ascii=False,indent=2),encoding='utf-8')
assignments={n:ident for ident,_,_,_,shots in definitions for n,_ in shots}
duplicates={3:103,16:128,18:115,19:124}
audit=[]
for item in manifest:
    n=item['n']; ident=assignments.get(n,duplicates.get(n))
    audit.append({**item,'productId':ident,'resultado':'Ya existente; no duplicada' if n in duplicates else ('Accesorio identificado: Bralette negro con pedrería de colores, S/199' if video_confirmations.exists() else 'Pendiente: top sin nombre ni precio') if n==21 else 'Incorporada a su prenda'})
(root/'review/auditoria-importacion-2026-10-08.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
cards=[]
for ident in [ident for ident in [127,147,148] if byid[ident]['price'] is None]:
    p=byid[ident]
    cards.append(f'<article><img src="../{p["image"].removeprefix("./")}"><h2>XL-{ident} · {html.escape(p["name"])}</h2><p>{p["category"]} · Precio por confirmar. Nombre descriptivo provisional.</p></article>')
if not video_confirmations.exists():
    cards.append('<article><img src="importacion-2026-10-08/N021.jpeg"><h2>Top negro con pedrería multicolor</h2><p>Faltan nombre oficial, precio y confirmación de su ficha. No se publicó como vestido.</p></article>')
missing='<h2>Modelos del catálogo que todavía no tienen foto original identificada</h2><ul>'+''.join(f'<li>{html.escape(p["nombre"])} · S/ {p["precio"]:.2f}</li>' for p in pending)+'</ul>'
report='<html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Pendientes · Xiliana</title><style>body{font:16px Arial;margin:40px;color:#25221d}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:30px}img{width:100%;height:360px;object-fit:contain}h2{font-size:18px}p,li{line-height:1.6}</style><h1>Solo pendientes de confirmación</h1><p>Revisión del 8 de octubre: 28 fotos revisadas; 4 corresponden a prendas existentes. Frente primero en todas las galerías.</p><main>'+''.join(cards)+'</main>'+missing+'</html>'
(root/'review/PENDIENTES-2026-10-08.html').write_text(report,encoding='utf-8')
print(f'{len(products)} vestidos; {sum(len(p["photos"]) for p in products)} fotos; {sum(p["price"] is None for p in products)} precios pendientes.')
