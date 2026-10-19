"""Recuperar la ficha Bandage roja de S/379 y conservar las 142 prendas existentes."""
from pathlib import Path
from collections import Counter
import json, re, hashlib, shutil
from PIL import Image

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ROOT=AUDIT.parents[1]
BACKUP=HERE/'importacion-XL182'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raw=(ROOT/'products.js').read_text(encoding='utf-8')
match=re.search(r'export const products = ([\s\S]*?);\s*export const categories',raw)
before=json.loads(match[1])
assert len(before)==142 and max(p['id'] for p in before)==181
assert not BACKUP.exists()
BACKUP.mkdir()
for source in ['products.js','review/publicados-confirmados.json','review/categorias-confirmadas.json','review/conciliacion-final-2026-10-15/resultado-aplicado.json','review/conciliacion-final-2026-10-15/CONCILIACION.md']:
    shutil.copy2(ROOT/source,BACKUP/Path(source).name)
existing={photo['sha256'] for p in before for photo in p['photos']}
folder=ROOT/'images/productos-reales/XL-182'
assert not folder.exists()
folder.mkdir()
photos=[]
for position,key,view,filename in [(1,'foto','Frente','01-WA-rojo379-frente.png'),(2,'foto3','Espalda','02-WA-rojo379-espalda.png'),(3,'foto2','Frente 3/4','03-WA-rojo379-frente-tres-cuartos.png')]:
    attachment=HERE/f'bandage-rojo379-{key}.png'
    digest=hashlib.sha256(attachment.read_bytes()).hexdigest()
    assert digest not in existing
    with Image.open(attachment) as image:width,height=image.size
    shutil.copy2(attachment,folder/filename)
    capturekey='' if key=='foto' else f'-{key}'
    photos.append({'src':f'./images/productos-reales/XL-182/{filename}','width':width,'height':height,'view':view,'sha256':digest,'sourceAttachment':attachment.relative_to(ROOT).as_posix(),'sourceType':'Captura de fotografía del catálogo WhatsApp Web','captureSource':{'pantalla':(HERE/f'bandage-rojo379{capturekey}-pantalla.png').relative_to(ROOT).as_posix(),'encuadre':(HERE/f'bandage-rojo379{capturekey}-encuadre.json').relative_to(ROOT).as_posix(),'edicion':'Recorte al área de la fotografía; sin cambiar modelo, vestido, colores ni fondo.'}})
new={'id':182,'name':'Vestido Bandage rojo corto de pedrería plateada','category':'Bandage','price':379,'photos':photos,'image':photos[0]['src'],'photoPending':False,'note':'Elige tus accesorios favoritos y dale tu toque a este diseño. Podemos orientarte sobre medidas, ajustes y disponibilidad.','catalogName':'VESTIDO BANDAGE','catalogDescription':'Rojo corto de pedrería plateada','catalogCategory':"Vestidos Bandage's",'priceSource':{'tipo':'WhatsApp Web','telefono':'+51 930 527 248','fecha':'2026-10-15','evidencia':(HERE/'bandage-rojo379-ficha.png').relative_to(ROOT).as_posix()},'imageSource':{'tipo':'Capturas del catálogo WhatsApp Web','fecha':'2026-10-15','coleccion':"Vestidos Bandage's",'comparacion':'Vestido mini rojo liso con tirantes y ribetes de pedrería plateada en escote y bajo. Frente, espalda y pose de tres cuartos pertenecen a la misma ficha. Es distinto de XL-073 rojo midi sin ribetes, XL-049 de una manga con lentejuelas, XL-152 de corsé y cadenas y XL-166 de lentejuelas sin tirantes, y de las demás 142 prendas.','procedencia':'Se conserva la fotografía oficial. Se recorta únicamente la interfaz de WhatsApp sin alterar vestido, modelo ni fondo.'}}
products=before+[new]
assert products[:142]==before
totals=dict(Counter(p['category'] for p in products))
assert totals=={'Gala':32,'Largos':25,'Cortos':27,'Bandage':22,'Cortos con brillo':36,'Liquidación':1}
assert sum(len(p['photos']) for p in products)==233
(ROOT/'products.js').write_text(raw[:match.start(1)]+json.dumps(products,ensure_ascii=False,indent=2)+raw[match.end(1):],encoding='utf-8')
save(ROOT/'review/publicados-confirmados.json',products)
manifest=read(ROOT/'review/categorias-confirmadas.json')
manifest['revision']='conciliacion-catalogo-2026-10-15-con-XL179-182'
manifest['prendas'].append({'id':182,'nombre':new['name'],'categoria':'Bandage','fecha':'2026-10-15','fuente':new['priceSource']['evidencia'],'motivo':'La ficha oficial VESTIDO BANDAGE, descripción Rojo corto de pedrería plateada, confirma la colección Bandage y S/379. Identidad nueva verificada contra los 142 modelos anteriores. Frente, espalda y tres cuartos son del mismo vestido.','fotos':[{k:photo[k] for k in ['src','view','sha256']} for photo in photos]})
manifest['referencias_actuales']='Cuatro altas verificadas XL-179–182 en review/conciliacion-final-2026-10-15/whatsapp-actual/. Las 139 prendas iniciales y sus 225 fotos se conservan, con las seis correcciones de categoría documentadas. Se añaden ocho fotos reales de cuatro prendas recuperadas.'
save(ROOT/'review/categorias-confirmadas.json',manifest)
result=read(AUDIT/'resultado-aplicado.json')
result.update({'revision':manifest['revision'],'total_prendas':143,'total_fotos':233,'totales':totals,'diferencias_pendientes':{'Largos':0,'Cortos con brillo':7,'Cortos':3,'Bandage':0},'conservacion':'Se mantienen las seis correcciones de categoría y todos los campos de las 139 prendas iniciales salvo esas categorías. Las cuatro altas reales XL-179–182 añaden ocho fotografías. Las 142 prendas anteriores a XL-182 y sus 230 fotos permanecen idénticas.','bandage_confirmado':{'modelos':22,'alta_verificada':182,'evidencia':new['priceSource']['evidencia']}})
result['pendientes']=[row for row in result['pendientes'] if not row.startswith('Bandage conserva')]
result['altas'].append({'id':182,'nombre':new['name'],'categoria':'Bandage','precio':379,'nombre_catalogo':'VESTIDO BANDAGE','descripcion_catalogo':new['catalogDescription'],'fotos':3,'evidencia':new['priceSource']['evidencia']})
save(AUDIT/'resultado-aplicado.json',result)
save(BACKUP/'resultado.json',{'revision':manifest['revision'],'alta':182,'prendas_previas_intactas':142,'fotos_previas_intactas':230,'prendas':143,'fotos':233,'totales':totals})

report=(AUDIT/'CONCILIACION.md').read_text(encoding='utf-8')
report=report.replace('tres prendas recuperadas del catálogo actual: 142 prendas y 230 fotos','cuatro prendas recuperadas del catálogo actual: 143 prendas y 233 fotos').replace('| Bandage | 21 | 22 | 1 |','| Bandage | 22 | 22 | 0 |')
report+='\n## Bandage recuperado y total confirmado\n\n**XL-182 · Vestido Bandage rojo corto de pedrería plateada · S/ 379.** La ficha actual se llama «VESTIDO BANDAGE» y describe «Rojo corto de pedrería plateada». Es un mini rojo liso con tirantes y ribetes plateados, distinto de XL-073, XL-049, XL-152, XL-166 y las demás prendas previas. Se recuperaron tres imágenes de la misma ficha; la galería muestra **frente, espalda y frente de tres cuartos**. No se modificaron vestido, modelo, color ni fondo.\n\nBandage queda en **22 modelos**, coincidiendo con la cantidad indicada. El catálogo web completo contiene **143 prendas y 233 fotos**. Largos también coincide en 25; la conciliación de Brillo y Cortos sigue abierta por las referencias concretas pendientes documentadas.\n'
(AUDIT/'CONCILIACION.md').write_text(report,encoding='utf-8')
(AUDIT/'bandage').mkdir(exist_ok=True)
(AUDIT/'bandage/REPORTE.md').write_text('# Conciliación de Bandage — 15 de octubre de 2026\n\nSe recuperó la referencia que faltaba para la cantidad indicada de 22 modelos: **XL-182, Vestido Bandage rojo corto de pedrería plateada, S/379**. La ficha «VESTIDO BANDAGE» y su descripción oficial verifican familia y precio.\n\nLas tres fotografías se revisaron antes de incorporarlas: frente, frente de tres cuartos y espalda del mismo mini rojo liso con ribetes plateados en tirantes, escote y bajo. Son distintas de los vestidos rojos XL-073, XL-049, XL-152 y XL-166. La galería publicada ordena frente, espalda y tres cuartos. Las 142 prendas anteriores permanecen idénticas.\n\nEl total Bandage es **22**, sin trasladar vestidos de otras colecciones ni contar accesorios como vestidos. La evidencia está en ../whatsapp-actual/bandage-rojo379-ficha.png y las fotos capturadas contiguas.\n',encoding='utf-8')
print(json.dumps({'revision':manifest['revision'],'prendas':143,'fotos':233,'totales':totals},ensure_ascii=False))
