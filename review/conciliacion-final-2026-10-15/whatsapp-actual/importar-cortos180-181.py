"""Añadir dos referencias de Cortos verificadas en WhatsApp, conservando el catálogo anterior."""
from pathlib import Path
from collections import Counter
import json, re, hashlib, shutil
from PIL import Image

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ROOT=AUDIT.parents[1]
BACKUP=HERE/'importacion-XL180-181'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raw=(ROOT/'products.js').read_text(encoding='utf-8')
match=re.search(r'export const products = ([\s\S]*?);\s*export const categories',raw)
before=json.loads(match[1])
assert len(before)==140 and max(p['id'] for p in before)==179
assert {p['id']:p['category'] for p in before if p['id'] in [62,68,81,90,101,107]}=={62:'Gala',68:'Cortos',81:'Cortos',90:'Gala',101:'Gala',107:'Gala'}
assert not BACKUP.exists(), 'La importación ya tiene snapshot; comprobar el resultado antes de volver a ejecutarla.'
BACKUP.mkdir()
for source in ['products.js','review/publicados-confirmados.json','review/categorias-confirmadas.json','review/conciliacion-final-2026-10-15/resultado-aplicado.json','review/conciliacion-final-2026-10-15/CONCILIACION.md']:
    shutil.copy2(ROOT/source,BACKUP/Path(source).name)

def dhash(image):
    values=list(image.convert('L').resize((17,16)).getdata())
    return sum((values[y*17+x]>values[y*17+x+1])<<(y*16+x) for y in range(16) for x in range(16))

existing=[]
for p in before:
    for photo in p['photos']:
        with Image.open(ROOT/photo['src'].removeprefix('./')) as image:
            existing.append((p['id'],photo['src'],photo['sha256'],dhash(image)))

specs=[
    {'id':180,'name':'Vestido corto satín estampado','price':86.7,'code':'796','key':'cortos-satin8670','description':'Vestido mini de satín estampado floral azul, blanco y verde, escote cuadrado, tirantes con volantes y falda drapeada. La fotografía oficial reúne dos poses de frente del mismo modelo.'},
    {'id':181,'name':'Vestido corto con volantes de cuello redondo','price':115.6,'code':'1537','key':'cortos-volantes11560','description':'Vestido verde agua liso, cuello redondo, volantes en mangas cortas y abertura frontal. La foto de frente y la ficha actual coinciden con la colección Cortos.'}
]
products=before.copy()
dedup=[]
for spec in specs:
    attachment=HERE/f'{spec["key"]}-foto.png'
    digest=hashlib.sha256(attachment.read_bytes()).hexdigest()
    assert not any(row[2]==digest for row in existing)
    with Image.open(attachment) as image:
        width,height=image.size
        variants={'foto_completa':image.copy()}
        if spec['id']==180:
            variants['pose_izquierda']=image.crop((0,0,width//2,height))
            variants['pose_derecha']=image.crop((width//2,0,width,height))
        closest={key:[{'id':row[0],'foto':row[1],'distancia_dhash_256bits':distance} for distance,row in sorted(((dhash(v)^row[3]).bit_count(),row) for row in existing)[:5]] for key,v in variants.items()}
    folder=ROOT/f'images/productos-reales/XL-{spec["id"]}'
    assert not folder.exists()
    folder.mkdir()
    filename=f'01-WA{spec["code"]}-frente.png'
    shutil.copy2(attachment,folder/filename)
    src=f'./images/productos-reales/XL-{spec["id"]}/{filename}'
    photo={'src':src,'width':width,'height':height,'view':'Frente','sha256':digest,'sourceAttachment':attachment.relative_to(ROOT).as_posix(),'sourceType':'Captura de fotografía del catálogo WhatsApp Web','captureSource':{'pantalla':(HERE/f'{spec["key"]}-pantalla.png').relative_to(ROOT).as_posix(),'encuadre':(HERE/f'{spec["key"]}-encuadre.json').relative_to(ROOT).as_posix(),'edicion':'Recorte al área de la fotografía; sin cambiar modelo, vestido, colores ni fondo. Se conserva la composición original.'}}
    photos=[photo]
    if spec['id']==181:
        back=HERE/f'{spec["key"]}-foto2.png'
        backhash=hashlib.sha256(back.read_bytes()).hexdigest()
        assert not any(row[2]==backhash for row in existing)
        with Image.open(back) as image:backwidth,backheight=image.size
        backfilename=f'02-WA{spec["code"]}-espalda.png'
        shutil.copy2(back,folder/backfilename)
        photos.append({'src':f'./images/productos-reales/XL-{spec["id"]}/{backfilename}','width':backwidth,'height':backheight,'view':'Espalda','sha256':backhash,'sourceAttachment':back.relative_to(ROOT).as_posix(),'sourceType':'Captura de fotografía del catálogo WhatsApp Web','captureSource':{'pantalla':(HERE/f'{spec["key"]}-foto2-pantalla.png').relative_to(ROOT).as_posix(),'encuadre':(HERE/f'{spec["key"]}-foto2-encuadre.json').relative_to(ROOT).as_posix(),'edicion':'Recorte al área de la fotografía; sin cambiar modelo, vestido, colores ni fondo.'}})
    product={'id':spec['id'],'name':spec['name'],'category':'Cortos','price':spec['price'],'originalPrice':289,'photos':photos,'image':src,'photoPending':False,'note':'Elige tus accesorios favoritos y dale tu toque a este diseño. Podemos orientarte sobre medidas, ajustes y disponibilidad.','catalogName':spec['name'],'catalogCode':spec['code'],'catalogCategory':'Vestidos Cortos','priceSource':{'tipo':'WhatsApp Web','telefono':'+51 930 527 248','fecha':'2026-10-15','evidencia':(HERE/f'{spec["key"]}-ficha.png').relative_to(ROOT).as_posix()},'imageSource':{'tipo':'Captura del catálogo WhatsApp Web','fecha':'2026-10-15','codigo':spec['code'],'coleccion':'Vestidos Cortos','comparacion':spec['description']+' Distinto de las 140 prendas anteriores, comprobado contra las fotografías y los diseños existentes.','procedencia':'Capturas de las fotografías oficiales; no se altera la modelo ni la prenda. Se publica el frente primero y únicamente las vistas recuperadas de la misma ficha.'}}
    products.append(product)
    dedup.append({'id_nuevo':spec['id'],'nombre':spec['name'],'codigo_catalogo':spec['code'],'sha256':digest,'duplicados_exactos':[],'candidatos_perceptuales':closest,'decision_visual':'Prenda nueva, sin correspondencia entre los 140 modelos anteriores. Se comparó la silueta, escote, mangas, estampado, largo y aplicaciones. La similitud de fondo o pose no acredita duplicado.'})
assert products[:140]==before
assert len(products)==142 and len({p['id'] for p in products})==142
totals=dict(Counter(p['category'] for p in products))
assert totals=={'Gala':32,'Largos':25,'Cortos':27,'Bandage':21,'Cortos con brillo':36,'Liquidación':1}
assert sum(len(p['photos']) for p in products)==230
(ROOT/'products.js').write_text(raw[:match.start(1)]+json.dumps(products,ensure_ascii=False,indent=2)+raw[match.end(1):],encoding='utf-8')
save(ROOT/'review/publicados-confirmados.json',products)

manifest=read(ROOT/'review/categorias-confirmadas.json')
manifest['revision']='conciliacion-catalogo-2026-10-15-con-XL179-181'
for product in products[-2:]:
    manifest['prendas'].append({'id':product['id'],'nombre':product['name'],'categoria':product['category'],'fecha':'2026-10-15','fuente':product['priceSource']['evidencia'],'codigo_catalogo':product['catalogCode'],'motivo':'Referencia exacta de la colección comercial Cortos recuperada de WhatsApp actual, con nombre, precio de oferta y precio regular confirmados. Foto real distinta de las 140 prendas anteriores.','fotos':[{k:photo[k] for k in ['src','view','sha256']} for photo in product['photos']]})
manifest['referencias_actuales']='Tres altas verificadas XL-179–181 en review/conciliacion-final-2026-10-15/whatsapp-actual/; sin modificar las 140 prendas anteriores al incorporar XL-180 y XL-181.'
save(ROOT/'review/categorias-confirmadas.json',manifest)

result=read(AUDIT/'resultado-aplicado.json')
result.update({'revision':manifest['revision'],'total_prendas':142,'total_fotos':230,'totales':totals,'diferencias_pendientes':{'Largos':0,'Cortos con brillo':7,'Cortos':3},'conciliacion_inventario_cerrada':False,'conservacion':'Se mantienen las seis correcciones de categoría. Las 140 prendas anteriores a XL-180–181 conservan todos sus campos y las 227 fotos. Desde el inicio de esta conciliación se recuperaron tres referencias reales de WhatsApp: XL-179 con frente y espalda, XL-180 con una composición frontal y XL-181 con frente y espalda.','significado_cantidades':'El usuario aclaró que 25 Largos, 43 Cortos con brillo y 30 Cortos se refieren a colecciones del catálogo WhatsApp, no a un conteo de stock físico. La diferencia neta de modelos web y el número de referencias de la fuente sin foto asociada se documentan por separado.','referencias_fuente_sin_foto_asociada':{'Cortos con brillo':4,'Cortos':14}})
result['pendientes']=['Cortos con brillo: diferencia neta de siete entre 36 web y 43 indicados; cuatro referencias concretas de la lista de 43 siguen sin foto original asociada. No equivalen a stock faltante.','Cortos: diferencia neta de tres entre 27 web y 30 indicados; catorce filas de la lista histórica de 33 siguen sin foto asociada. Hay modelos web confirmados fuera de esa lista y un posible duplicado blanco con perlas.','Bandage conserva 21 modelos; el total histórico indicado fue 22.','XL-069 y XL-131 comparten nombre y precio pero son prendas distintas; la miniatura oficial Vestido drapeado azul asimétrico corresponde a XL-131. No fusionarlos ni cambiar el precio confirmado de XL-069 sin otra referencia.','XL-107 y XL-175 comparten nombre base y precio pero muestran modelos diferentes; no fusionarlos.']
for p in products[-2:]:result['altas'].append({'id':p['id'],'nombre':p['name'],'categoria':p['category'],'precio':p['price'],'precio_regular':p['originalPrice'],'codigo_catalogo':p['catalogCode'],'fotos':len(p['photos']),'evidencia':p['priceSource']['evidencia']})
save(AUDIT/'resultado-aplicado.json',result)
save(BACKUP/'deduplicacion.json',dedup)
save(BACKUP/'resultado.json',{'revision':manifest['revision'],'altas':[180,181],'prendas_anteriores_intactas':140,'fotos_anteriores_intactas':227,'prendas':142,'fotos':230,'totales':totals,'metas_completas':False})

matrix=read(AUDIT/'cortos/matriz-cortos.json')
for row in matrix['filas']:
    if row['fila_oficial'] in [2,3]:
        ident=180 if row['fila_oficial']==2 else 181
        p=next(p for p in products if p['id']==ident)
        row.update({'ids_candidatos':[ident],'estado':'Coincidencia visual y ficha actual confirmadas; incorporada al catálogo web','categorias_actuales':['Cortos'],'codigo_catalogo':p['catalogCode'],'evidencia_visual':p['priceSource']['evidencia']})
    row['categorias_actuales']=[next(p for p in products if p['id']==ident)['category'] for ident in row['ids_candidatos']]
matrix['ids_asociados_lista_oficial']=sorted({ident for row in matrix['filas'] for ident in row['ids_candidatos']})
matrix['filas_asociadas']=19
matrix['filas_no_asociadas']=[row['fila_oficial'] for row in matrix['filas'] if not row['ids_candidatos']]
matrix['cantidad_cortos_actual']=27
matrix['cantidad_cortos_tras_restaurar_68_81']=27
matrix['faltantes_para_meta30_tras_restaurar']=3
matrix['referencias_actuales_recuperadas']=[180,181]
matrix['advertencias_fuente']=[v.replace('Los16 registros','Los14 registros').replace('a16 prendas','a14 prendas').replace('No hay cinco candidatos adicionales','No hay tres candidatos adicionales') for v in matrix['advertencias_fuente']]
matrix['aclaracion_cantidades']='La meta de 30 se refiere a la colección comercial WhatsApp indicada por el usuario. Las 14 referencias históricas sin foto no representan 14 unidades de stock físico faltantes ni la diferencia neta de tres modelos web.'
save(AUDIT/'cortos/matriz-cortos.json',matrix)

report=(AUDIT/'CONCILIACION.md').read_text(encoding='utf-8')
report=re.sub(r'15 de octubre de 2026\. \*\*[^\n]*\*\*','15 de octubre de 2026. **Seis ubicaciones corregidas y tres prendas recuperadas del catálogo actual: 142 prendas y 230 fotos.**',report,count=1)
report=report.replace('| Cortos |25 |30 |5 |','| Cortos |27 |30 |3 |').replace('| Cortos | 25 | 30 | 5 |','| Cortos | 27 | 30 | 3 |')
report=report.replace('Se mantienen las seis correcciones de categoría. Las 139 prendas anteriores conservan todos sus campos, precios, nombres, identificadores, fotos y orden. Se añade XL-179 con dos capturas de fotografías verificadas del catálogo actual, frente primero.','Se mantienen las seis correcciones de categoría. Las 139 prendas iniciales conservan sus campos salvo esas categorías. Las 140 prendas existentes tras XL-179 y sus 227 fotos permanecen idénticas al incorporar XL-180 y XL-181. Las nuevas imágenes mantienen modelo, vestido, colores y composición oficial; no se inventan espaldas.')
report=report.replace('Brillo pasa de 35 a 36; la conciliación de 43 Brillo y 30 Cortos sigue abierta.','Brillo pasa de 35 a 36. Además se añaden dos referencias de Cortos recuperadas de la misma colección actual. La conciliación sigue abierta.')
report+='\n## Dos referencias de Cortos recuperadas\n\n| Código web | Nombre exacto de catálogo | Código catálogo | Precio actual | Precio regular | Fotos |\n|---|---|---|---:|---:|---|\n| XL-180 | Vestido corto satín estampado | 796 | S/ 86.70 | S/ 289.00 | Una composición oficial con dos poses de frente |\n| XL-181 | Vestido corto con volantes de cuello redondo | 1537 | S/ 115.60 | S/ 289.00 | Frente y espalda |\n\nSe comprobaron sus fichas actuales y la ausencia de estos diseños entre las 140 prendas previas. Cortos pasa de 25 a 27. Las ofertas conservan Cortos como categoría principal y se muestran también en la página de ofertas, que ahora reúne 10 registros con descuento sin duplicar prendas.\n\n## Alcance de los totales y referencias pendientes\n\nEl usuario aclaró que 25 Largos, 43 Cortos con brillo y 30 Cortos se refieren a las colecciones de WhatsApp. La web tiene 25, 36 y 27 respectivamente: diferencias netas 0, 7 y 3. La lista histórica de 33 Cortos ahora tiene 19 referencias asociadas y 14 sin foto original asociada; esas 14 no equivalen a 14 vestidos de stock faltantes. La lista de 43 Brillo conserva cuatro referencias concretas sin foto asociada. Los modelos web confirmados fuera de esas listas y las excepciones comerciales impiden igualar automáticamente los conjuntos solo por cantidades.\n'
(AUDIT/'CONCILIACION.md').write_text(report,encoding='utf-8')

cortosreport=(AUDIT/'cortos/REPORTE.md').read_text(encoding='utf-8')
cortosreport='**Actualización:** se incorporaron XL-180 y XL-181 desde fichas actuales de WhatsApp. Cortos tiene 27 modelos. La matriz de 33 tiene 19 filas asociadas y 14 pendientes de foto; diferencia neta a 30: tres. El cuerpo inicial de este informe se conserva como antecedente de la revisión anterior a estas altas. Ver matriz-cortos.json y CONCILIACION.md para el estado actual.\n\n'+cortosreport
(AUDIT/'cortos/REPORTE.md').write_text(cortosreport,encoding='utf-8')

# Los importadores históricos no deben deshacer esta conciliación posterior.
for filename,old,new in [
    ('aplicar-clasificacion-fashion-2026-10-15.py',"if read_json(MANIFEST).get('revision') == 'conciliacion-catalogo-2026-10-15':","if read_json(MANIFEST).get('revision', '').startswith('conciliacion-catalogo-2026-10-15'):"),
    ('conciliar-categorias-2026-10-15.py',"if read_json(MANIFEST).get('revision') in ('fashion-2026-10-15', 'conciliacion-catalogo-2026-10-15'):","if read_json(MANIFEST).get('revision') == 'fashion-2026-10-15' or read_json(MANIFEST).get('revision', '').startswith('conciliacion-catalogo-2026-10-15'):")
]:
    file=ROOT/'review'/filename
    text=file.read_text(encoding='utf-8')
    if old in text:file.write_text(text.replace(old,new),encoding='utf-8')
print(json.dumps({'revision':manifest['revision'],'altas':[180,181],'prendas':142,'fotos':230,'totales':totals},ensure_ascii=False))
