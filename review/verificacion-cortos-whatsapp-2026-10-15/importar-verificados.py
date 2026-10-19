"""Importar solo Cortos con identidad y precio actuales verificados."""
from pathlib import Path
from collections import Counter
import json, re, hashlib, shutil
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raw=(ROOT/'products.js').read_text(encoding='utf-8')
match=re.search(r'export const products = ([\s\S]*?);\s*export const categories',raw)
before=json.loads(match[1])
assert len(before)==145 and max(p['id'] for p in before)==184
assert before==read(HERE/'productos-antes.json')
manifest=read(ROOT/'review/categorias-confirmadas.json')
assert manifest['revision']=='conciliacion-catalogo-2026-10-15-con-XL179-184'
backup=HERE/'respaldo-importacion'
assert not backup.exists()
backup.mkdir()
for name in ['products.js','review/publicados-confirmados.json','review/categorias-confirmadas.json']:
    shutil.copy2(ROOT/name,backup/Path(name).name)
products=json.loads(json.dumps(before))
by_id={p['id']:p for p in products}
definitions=[
    (185,4,'Vestido corto licrado azul',249,'1758','F04-azul249',[(1,'Frente'),(3,'Espalda')],
     'Azul liso de tirantes, escote recto con ribete blanco y botones en diagonal. Distinto de los azules existentes.'),
    (186,5,'Vestido lila en rib',289,'1888','F05-lila289',[(1,'Frente'),(8,'Espalda'),(6,'Frente, otra pose'),(7,'Frente, otra pose')],
     'Mini lila de rib, escote cruzado, lazo lateral, mangas largas y perlas dispersas. Cuatro fotografías distintas de la misma ficha.'),
    (188,8,'Vestido corto verde agua con tirantes',299,None,'F08-verde299',[(1,'Frente')],
     'Verde agua de tirantes, cuerpo de transparencia estructurada y falda lisa a la rodilla; distinto de XL-181 de volantes.'),
    (189,11,'Vestido corto blanco con capa',239,None,'F11-capa239',[(1,'Frente'),(2,'Espalda')],
     'Blanco de escote en V con capa corta sobre hombros y brazos. Distinto de XL-083 de cuello alto y capas largas.'),
    (190,14,'Vestido corto azul con cinturón de Aplicaciones plateado',369,None,'F14-azul369',[(1,'Frente')],
     'Azul de terciopelo, escote Bardot y mangas largas con cinturón plateado; base lisa y detalle localizado.'),
    (191,19,'Vestido largo verde con estampado de rosas verdes',229,None,'F19-verde229',[(1,'Frente')],
     'Falda midi blanca con rosas verdes y tirantes. Se conserva Cortos según la ficha comercial, aunque el título diga largo.'),
    (192,21,'Vestido corto drapeado con perlas',389,None,'F21-perlas389',[(1,'Frente')],
     'Mini blanco drapeado con hombros descubiertos y perlas dispersas; no tiene las mangas largas de XL-067.'),
    (193,26,'Vestido azul con perlas blancas',389,None,'F26-azul389',[(1,'Frente')],
     'Azul liso de cuello alto y mangas largas, caída lateral y perlas localizadas en cuello y hombros. Ficha comercial Cortos.'),
    (194,29,'Vestido corto negro con aplicaciones plateadas',289,None,'F29-negro289',[(1,'Frente')],
     'Negro liso con hombros abiertos y aplicaciones plateadas en contornos. Distinto del negro con escote y strass XL-082 y del XL-114.'),
    (195,31,'Vestido corto drapeado de perlas',319,None,'F31-perlas319',[(1,'Frente')],
     'Vino de hombros descubiertos y mangas largas, perlas pequeñas dispersas sobre base lisa; distinto del XL-135 de pedrería densa.'),
]
def source(key):
    text=(HERE/(key+'-ficha-dom.txt')).read_text(encoding='utf-8')
    # El panel Detalles precede al listado de fondo durante su animación.
    start=text.index('- heading "Detalles"')
    return text[start:].split('- banner:')[0]
for ident,row,name,price,code,key,views,reason in definitions:
    detail=source(key)
    assert f'- generic: PEN {price:.2f}' in detail
    if code:assert code in detail
    folder=ROOT/f'images/productos-reales/XL-{ident:03d}'
    assert not folder.exists()
    folder.mkdir()
    photos=[]
    seen=set()
    for position,(capture,view) in enumerate(views,1):
        attachment=HERE/f'{key}-{capture}-foto.png'
        digest=hashlib.sha256(attachment.read_bytes()).hexdigest()
        assert digest not in seen
        seen.add(digest)
        with Image.open(attachment) as im:width,height=im.size
        filename=f'{position:02d}-WA-Cortos-F{row:02d}-{capture}.png'
        shutil.copy2(attachment,folder/filename)
        photos.append({'src':'./'+(folder/filename).relative_to(ROOT).as_posix(),'width':width,'height':height,
                       'view':view,'sha256':digest,'sourceAttachment':attachment.relative_to(ROOT).as_posix(),
                       'sourceType':'Captura de fotografía del catálogo WhatsApp Web',
                       'captureSource':{'pantalla':(HERE/f'{key}-{capture}-pantalla.png').relative_to(ROOT).as_posix(),
                                        'encuadre':(HERE/f'{key}-{capture}-encuadre.json').relative_to(ROOT).as_posix(),
                                        'edicion':'Recorte de interfaz; sin alterar vestido, modelo, color ni fondo.'}})
    p={'id':ident,'name':name,'category':'Cortos','price':price,'photos':photos,'image':photos[0]['src'],
       'photoPending':False,'catalogName':name,'catalogCategory':'Vestidos Cortos',
       'note':'Elige tus accesorios favoritos y dale tu toque a este diseño. Podemos orientarte sobre medidas, ajustes y disponibilidad.',
       'priceSource':{'tipo':'WhatsApp Web','telefono':'+51 930 527 248','fecha':'2026-10-16',
                      'evidencia':(HERE/(key+'-ficha.png')).relative_to(ROOT).as_posix()},
       'imageSource':{'tipo':'Fotografías ampliadas del catálogo en la misma sesión del usuario','fecha':'2026-10-16',
                      'comparacion':reason,'procedencia':'Fotografías oficiales recortadas a su área de imagen. Frente primero y espalda después cuando existe.'}}
    if code:p['catalogCode']=code
    products.append(p)
    manifest['prendas'].append({'id':ident,'nombre':name,'categoria':'Cortos','fecha':'2026-10-16',
                               'fuente':p['priceSource']['evidencia'],'motivo':reason+' Ficha actual en Vestidos Cortos.',
                               'fotos':[{k:ph[k] for k in ['src','view','sha256']} for ph in photos]})

# La foto celeste XL-069 estaba vinculada al título/precio del azul halter XL-131.
# La ficha actual F32 aporta la referencia exacta del celeste.
p69=by_id[69]
assert p69['price']==389 and p69['name']=='Vestido drapeado azul asimétrico'
assert '- generic: PEN 379.00' in source('F32-mangas379')
p69.update(name='Vestido corto drapeado de mangas',price=379,catalogName='vestido corto drapeado de mangas',urlSlug='vestido-drapeado-azul-asimetrico',
           priceSource={'tipo':'WhatsApp Web','telefono':'+51 930 527 248','fecha':'2026-10-16',
                        'evidencia':(HERE/'F32-mangas379-ficha.png').relative_to(ROOT).as_posix()})
row69=next(r for r in manifest['prendas'] if r['id']==69)
row69.update(nombre=p69['name'],verificacion_adicional='F32 actual confirma por fotografía el celeste de mangas amplias y escote en V, S/379. Se corrige la asociación anterior al título/precio del XL-131 halter, que permanece intacto a S/389.')

# Instrucción posterior: el precio actual de WhatsApp prevalece sobre el histórico web.
by_id[117]['price']=379
by_id[117]['priceSource']={'tipo':'WhatsApp Web','telefono':'+51 930 527 248','fecha':'2026-10-16',
                         'evidencia':'review/verificacion-brillo-whatsapp-2026-10-15/negro379-ficha.png',
                         'prioridad':'Precio de WhatsApp como verdad absoluta, según instrucción del usuario.'}
next(r for r in manifest['prendas'] if r['id']==117)['verificacion_adicional']='S/379 aplicado desde la ficha actual código 2062. El usuario indicó tomar los precios de WhatsApp como referencia absoluta; se sustituye el precio histórico web S/389. Frente y espalda conservados.'

assert [ph['view'] for ph in by_id[64]['photos']]==['Frente','Frente','Espalda']
by_id[64]['photos']=[by_id[64]['photos'][i] for i in [0,2,1]]
row64=next(r for r in manifest['prendas'] if r['id']==64)
row64['fotos']=[{k:ph[k] for k in ['src','view','sha256']} for ph in by_id[64]['photos']]

for old,current in zip(before,products[:145]):
    if old['id']==69:
        trimmed=dict(current)
        for key in ['catalogName','priceSource','urlSlug']:trimmed.pop(key,None)
        trimmed.update(name=old['name'],price=old['price'])
        assert trimmed==old
    elif old['id']==64:
        expected=dict(old)
        expected['photos']=[old['photos'][i] for i in [0,2,1]]
        assert current==expected
    elif old['id']==117:
        trimmed=dict(current)
        trimmed['price']=old['price']
        trimmed.pop('priceSource',None)
        assert trimmed==old
    else:assert current==old
assert len(products)==155 and sum(len(p['photos']) for p in products)==251
totals=dict(Counter(p['category'] for p in products))
assert totals=={'Gala':32,'Largos':25,'Cortos':37,'Bandage':22,'Cortos con brillo':38,'Liquidación':1}
manifest['revision']='conciliacion-catalogo-2026-10-15-cortos-revisados-2026-10-16'
manifest['verificacion_cortos_actual']='33 fichas actuales: el blanco F06/F10 y el verde F13/F15 están repetidos. F32 se asocia a XL-069 y corrige su nombre/precio. Diez altas publicadas, quince fotos nuevas; el blanco F06/F10 sigue preparado sin publicar hasta confirmar S/329 o S/319.'
(ROOT/'products.js').write_text(raw[:match.start(1)]+json.dumps(products,ensure_ascii=False,indent=2)+raw[match.end(1):],encoding='utf-8')
save(ROOT/'review/publicados-confirmados.json',products)
save(ROOT/'review/categorias-confirmadas.json',manifest)
pending={'id_reservado':187,'nombre':'Vestido blanco mini elegante con perlas','categoria':'Cortos',
         'estado':'No publicado: precio pendiente de confirmar','precios_catalogo':[329,319],'filas_catalogo':[6,10],
         'fotos':[{'archivo':'F06-blanco329-1-foto.png','vista':'Frente con modelo'},
                  {'archivo':'F06-blanco329-2-foto.png','vista':'Frente de la prenda, sin modelo'}],
         'evidencias':['F06-blanco329-ficha.png','F10-blanco319-ficha.png'],
         'observacion':'Ambas fichas usan las mismas fotografías; no son dos prendas. La segunda imagen es un frente de la prenda sin modelo, no una espalda.'}
save(HERE/'XL-187-PENDIENTE.json',pending)
save(HERE/'resultado-importacion.json',{'fecha':'2026-10-16','revision':manifest['revision'],'prendas':155,'fotos':251,
     'totales':totals,'altas':[d[0] for d in definitions],'modelos_nuevos_detectados':11,'modelo_pendiente':pending,
     'correccion':{'id':69,'nombre_anterior':before[next(i for i,p in enumerate(before) if p['id']==69)]['name'],
                   'nombre_actual':p69['name'],'precio_anterior':389,'precio_actual':379},
     'conservacion':'Las 145 prendas anteriores se conservan; solo XL-069 cambia nombre y precio por su ficha exacta. Ninguna categoría anterior ni fotografía previa se modifica.'})
print(json.dumps({'prendas':155,'fotos':251,'totales':totals,'pendiente':187},ensure_ascii=True))
