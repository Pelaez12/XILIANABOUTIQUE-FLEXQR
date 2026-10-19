"""Contrastar las 33 fichas actuales y documentar identidades, precios y altas."""
from pathlib import Path
from collections import Counter
import json,re,unicodedata,html,base64

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=ROOT/'review/conciliacion-final-2026-10-15'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
norm=lambda s:''.join(c for c in unicodedata.normalize('NFD',s).lower() if c.isalnum())
products=read(ROOT/'review/publicados-confirmados.json')
by_id={p['id']:p for p in products}
source=read(HERE/'lista-actual.json')
old=read(HERE/'matriz-historica.json')
assert len(source)==len(old['filas'])==33
ids={1:10,2:180,3:181,4:185,5:186,6:187,7:63,8:188,9:64,10:187,11:189,12:65,13:66,14:190,15:66,16:67,17:68,18:130,19:191,20:131,21:192,22:84,23:85,24:86,25:79,26:193,27:80,28:81,29:194,30:82,31:195,32:69,33:83}
evidence={4:'F04-azul249',5:'F05-lila289',6:'F06-blanco329',8:'F08-verde299',10:'F10-blanco319',11:'F11-capa239',14:'F14-azul369',15:'F15-verde359',19:'F19-verde229',21:'F21-perlas389',26:'F26-azul389',29:'F29-negro289',31:'F31-perlas319',32:'F32-mangas379'}
rows=[]
for i,(live,previous) in enumerate(zip(source,old['filas']),1):
    text=live['texto']
    assert norm(text).startswith(norm(previous['nombre_oficial'])),i
    prices=[float(v) for v in re.findall(r'PEN[^0-9]*([0-9]+\.[0-9]{2})',text)]
    assert prices[0]==previous['precio_oficial'],i
    ident=ids[i]
    p=by_id.get(ident)
    name=live.get('nombre') or previous['nombre_oficial']
    # La celda de nombre puede virtualizarse; el nombre de la matriz conserva el texto observado completo.
    row={'fila':i,'nombre_whatsapp':name,'texto_actual_observado':text,'precio_whatsapp':prices[0],
         'id_web':ident if p else None,'id_reservado':ident,'nombre_web':p['name'] if p else 'Vestido blanco mini elegante con perlas',
         'categoria_web':p['category'] if p else 'Pendiente de publicar en Cortos',
         'precio_web':p['price'] if p else None,'precio_coincide':prices[0]==p['price'] if p else None,
         'foto':p['image'] if p else './'+(HERE/'F06-blanco329-1-foto.png').relative_to(ROOT).as_posix(),
         'estado':'Asociado a prenda publicada' if p else 'Identidad verificada; precio pendiente',
         'fecha':'2026-10-16'}
    if i in evidence:row['evidencia']=(HERE/(evidence[i]+'-ficha.png')).relative_to(ROOT).as_posix()
    if i in [6,10]:row['observacion']='Misma prenda y mismas dos fotografías: frente con modelo y frente sin modelo. Dos precios actuales de WhatsApp, S/329 y S/319; no se publica hasta confirmar cuál ficha prevalece.'
    elif i in [13,15]:row['observacion']='Las fotos corresponden al mismo XL-066. La ficha con su nombre completo actual muestra S/429; el alias drapeado muestra S/359. La web conserva el precio de la ficha de nombre exacto, S/429. Ambos precios de WhatsApp se registran para confirmar.'
    elif i==32:row['observacion']='La foto confirma XL-069 celeste, antes vinculado erróneamente al título/precio del XL-131 halter. Nombre corregido a Vestido corto drapeado de mangas y precio actual WhatsApp S/379. Se conserva su URL anterior.'
    rows.append(row)
unique=set(ids.values())
published={r['id_web'] for r in rows if r['id_web']}
extra=[p for p in products if p['category']=='Cortos' and p['id'] not in published]
assert len(unique)==31 and len(published)==30
assert [p['id'] for p in extra]==[22,114,118,121,122,54,172]
assert sum(r['precio_coincide'] is True for r in rows)==30
assert [r['fila'] for r in rows if r['precio_coincide'] is False]==[15]
result={'fecha':'2026-10-16','fuente':'Catálogo Vestidos Cortos, misma pestaña WhatsApp del usuario 1748733514, +51 930 527 248',
        'prioridad_precios':'Precios actuales de WhatsApp según instrucción expresa del usuario. Si dos fichas actuales de la misma prenda se contradicen, registrar ambas sin inventar cuál es definitiva.',
        'fichas_observadas':33,'prendas_unicas_identificadas':31,'prendas_fuente_publicadas':30,
        'prendas_fuente_pendientes_precio':1,'referencias_sin_identidad':0,
        'duplicados':[{'filas':[6,10],'id_reservado':187,'precios':[329,319]}, {'filas':[13,15],'id':66,'precios':[429,359]}],
        'altas_publicadas':[185,186,188,189,190,191,192,193,194,195],
        'nuevos_modelos_detectados':11,'fotos_anadidas':15,
        'correccion':{'id':69,'nombre':'Vestido corto drapeado de mangas','precio_actual':379,'precio_anterior':389},
        'precios_fichas_coincidentes':30,'fichas_precio_pendiente':[6,10,15],
        'modelos_web_cortos':37,'modelos_web_cortos_fuera_lista':[p['id'] for p in extra],
        'conteo':'33 fichas − 2 fichas duplicadas = 31 modelos únicos en la colección WhatsApp. Treinta están publicados y uno espera aclarar su precio. La web tiene esos 30 más 7 Cortos procedentes de otras fuentes = 37.',
        'objetivo_indicado':30,'advertencia':'La colección actual contiene 31 modelos únicos, incluidos los tres modelos en oferta. No se excluyen ofertas del conteo ni se eliminan prendas existentes para forzar el objetivo de 30.',
        'totales_web':dict(Counter(p['category'] for p in products)),'prendas_web':155,'fotos_web':251,
        'matriz':rows}
save(HERE/'CONCILIACION-33.json',result)
save(HERE/'precios-actuales.json',[{k:r[k] for k in ['fila','nombre_whatsapp','precio_whatsapp','id_web','precio_web','precio_coincide']} for r in rows])

summary='''# Revisión de Vestidos Cortos — 16 de octubre de 2026

Se compararon las **33 fichas actuales** de la colección Vestidos Cortos en la misma pestaña de WhatsApp que abrió el usuario. Se registraron nombres y precios de todas las filas y se ampliaron las fotografías de las 14 referencias pendientes de asociación. Las 19 asociaciones anteriores conservan su evidencia previa; las cuatro vistas adicionales de miniaturas no llegaron a guardarse porque el control de la pestaña se desconectó al final. No se presenta esa comprobación adicional como completada.

## Conteo real de la colección

**33 fichas = 31 modelos únicos**, porque se repiten dos prendas:

- Blanco de mangas abiertas y perlas: filas 6 y 10, mismas dos fotos, **S/329 y S/319**. La segunda foto es el frente de la prenda sin modelo, no la espalda.
- Verde de terciopelo con escote: filas 13 y 15, mismo XL-066 con nombres distintos, **S/429 y S/359**.

Los tres vestidos en oferta de las filas 1–3 están incluidos en esos 31 modelos. No se restan por aparecer también en Liquidación. El objetivo de 30 no coincide exactamente con la colección observada; la cifra de 31 mencionada anteriormente sí coincide con las identidades identificadas.

## Cambios aplicados

Se publican **10 modelos nuevos y 15 fotografías reales** en Cortos. Un undécimo modelo identificado, el blanco repetido, queda preparado como **XL-187** sin publicar hasta resolver sus dos precios actuales de WhatsApp.

**XL-069:** la foto celeste de mangas amplias y escote en V corresponde a «Vestido corto drapeado de mangas», **S/379**. Se corrigieron su título y precio anteriores de S/389, que estaban asociados a la referencia del azul halter XL-131. XL-131 conserva su nombre, precio S/389 y fotos. La URL anterior de XL-069 se mantiene para no romper sus enlaces.

Se mantienen todas las categorías y fotografías previas. Las nuevas galerías muestran frente primero y espalda después cuando existe. No se inventan ángulos ni se altera modelo, vestido, fondo o color. En el lila se publican cuatro ángulos distintos, descartando capturas repetidas del mismo frente.

## Precios: WhatsApp es la fuente

Los precios de las altas y la corrección de XL-069 proceden de las fichas actuales. **30 filas coinciden con los precios publicados**. Dos filas del blanco tienen el precio pendiente y una fila del verde se contradice con la otra ficha de WhatsApp.

Para XL-066 se conserva S/429 porque figura actualmente en la ficha con su mismo nombre completo. También se registra la ficha alias de S/359: no se usa un precio histórico de la web para invalidar lo que muestra WhatsApp. El encargado debe indicar cuál ficha queda vigente.

## Web frente a colección WhatsApp

La web queda con **37 Cortos**: 30 modelos de la lista actual publicados más **7 modelos de otras referencias** (XL-022, XL-054, XL-114, XL-118, XL-121, XL-122 y XL-172). Estos siete conservan sus fotos y clasificación previa; esta revisión de Cortos no autoriza borrarlos ni moverlos para cuadrar una cifra.

El blanco pendiente sería el modelo 31 de WhatsApp y el 38 de la web si se publica. Por tanto no se anuncia que el inventario ya coincide con 30.

**Web completa: 155 prendas y 251 fotos.** Solo se revisó la colección Cortos en esta fase; los totales de las otras colecciones se conservaron.

La instrucción posterior del usuario de tomar los precios actuales de WhatsApp como referencia absoluta también resuelve la discrepancia ya investigada del XL-117: se aplica **S/379**, sustituyendo el histórico S/389, con la ficha de Brillos ya capturada. No se revisaron nuevas colecciones para hacerlo.

## Altas verificadas

| Código | Nombre | Precio WhatsApp | Fotos |
|---|---|---:|---:|
'''
for ident in result['altas_publicadas']:
    p=by_id[ident]
    summary+=f'| XL-{ident} | {p["name"]} | S/ {p["price"]:.2f} | {len(p["photos"])} |\n'
summary+='\n## Matriz completa\n\n| Fila WhatsApp | Nombre | Precio WhatsApp | Prenda | Estado |\n|---|---|---:|---|---|\n'
for r in rows:
    summary+=f'| {r["fila"]} | {r["nombre_whatsapp"]} | S/ {r["precio_whatsapp"]:.2f} | XL-{r["id_reservado"]:03d} | {r["estado"]} |\n'
(HERE/'REVISION.md').write_text(summary,encoding='utf-8')

message='''Hola, revisamos únicamente «Vestidos Cortos» en tu catálogo actual de WhatsApp, usando sus fotos, nombres y precios como referencia.

Encontramos 33 fichas que corresponden a 31 modelos únicos, incluidos los tres modelos en oferta. Hay dos prendas repetidas:

1. «Vestido blanco mini elegante con perlas» S/329 y «Vestido blanco con perlas» S/319 muestran las mismas dos fotos. ¿Cuál nombre y precio deben quedar vigentes? Lo tenemos preparado como XL-187 sin publicarlo todavía.

2. «Vestido color verde terciopelo semi drapeado con manga y escote» S/429 y «Vestido drapeado verde de mandas con escote» S/359 corresponden al mismo XL-066. La web conserva S/429 de la ficha que tiene su nombre completo. ¿Cuál de las dos fichas actuales de WhatsApp debe prevalecer?

Ya incorporamos diez modelos que faltaban con sus fotografías reales y precios actuales. También corregimos XL-069: el celeste de mangas amplias y escote en V es «Vestido corto drapeado de mangas», S/379. Es distinto del azul halter XL-131, que conserva S/389.

La web tiene ahora 37 Cortos: 30 modelos de esta lista publicados y siete modelos de otras referencias (XL-022, XL-054, XL-114, XL-118, XL-121, XL-122 y XL-172). Falta publicar el blanco cuando confirmes su precio. ¿Los siete deben conservarse en Cortos o cuál es la colección definitiva de cada uno?

La cantidad indicada fue 30 o 31. La colección actual contiene 31 modelos distintos. Confírmanos la lista definitiva y las dos fichas duplicadas para que WhatsApp y la web coincidan sin duplicar vestidos ni excluir ofertas de sus categorías principales.
'''
(HERE/'MENSAJE-PARA-ENCARGADO.txt').write_text(message,encoding='utf-8')

def data_image(src):
    path=ROOT/src
    mime='image/png' if path.suffix.lower()=='.png' else 'image/jpeg'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
cards=[]
for r in rows:
    label='Precio pendiente' if r['id_web'] is None else ('Dos precios en WhatsApp' if r['id_web']==66 else ('Alta verificada' if r['id_web']>=185 else 'Asociado'))
    cards.append(f'<article><img src="{data_image(r["foto"])}" alt="{html.escape(r["nombre_web"])}"><div><small>Ficha {r["fila"]} · XL-{r["id_reservado"]:03d} · {html.escape(label)}</small><h2>{html.escape(r["nombre_whatsapp"])}</h2><p>WhatsApp <b>S/ {r["precio_whatsapp"]:.2f}</b></p><p>{html.escape(r.get("observacion",r["estado"]))}</p></div></article>')
page='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Comparación de 33 fichas de Cortos</title><style>body{font:16px/1.5 system-ui,sans-serif;background:#f7f6f3;color:#292929;margin:0}main{max-width:1250px;margin:auto;padding:30px 20px}header{max-width:900px;margin-bottom:30px}h1{font-size:clamp(28px,5vw,42px);line-height:1.15}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}article{background:white;border:1px solid #ddd}article img{width:100%;height:320px;object-fit:contain;background:#f1f1ef}article div{padding:16px}h2{font-size:17px;line-height:1.35}small{color:#665b48}article p{font-size:14px}</style><main><header><p>XILIANA BOUTIQUE · 16 OCT 2026</p><h1>Cortos: 33 fichas, 31 modelos</h1><p>Precios actuales de WhatsApp como fuente. Se identificaron dos fichas duplicadas y once modelos que faltaban: diez publicados y el blanco pendiente por sus dos precios actuales.</p><p><b>Web: 37 Cortos.</b> Treinta modelos de esta lista publicados más siete de otras referencias. El modelo blanco preparado es el 31 de la lista actual y sigue sin publicar.</p><p><b>Dos contradicciones del propio catálogo:</b> blanco S/329 o S/319; verde XL-066 S/429 o S/359. Se registran ambas, sin inventar un precio definitivo.</p></header><section class="grid">'''+''.join(cards)+'</section></main></html>'
(HERE/'COMPARACION-33.html').write_text(page,encoding='utf-8')

# Actualizar la matriz anterior; el informe previo se conserva como antecedente.
historic=read(OLD/'cortos/matriz-cortos.json')
if not (HERE/'matriz-cortos-anterior.json').exists():save(HERE/'matriz-cortos-anterior.json',historic)
historic.update({'fecha_actualizacion':'2026-10-16','filas_asociadas':33,'filas_no_asociadas':[],
                 'prendas_unicas_fuente':31,'pendiente_precio':187,'cantidad_cortos_actual':37,
                 'prendas_actuales_cortos_fuera_de_lista_oficial':[p['id'] for p in extra],
                 'estado_actual':'Ver revisión actual en ../../verificacion-cortos-whatsapp-2026-10-15/REVISION.md. Las filas incluyen un borrador no publicado, XL-187.'})
historic['filas_actuales']=rows
save(OLD/'cortos/matriz-cortos.json',historic)
banner='> Actualización del 16/10/2026: **33 fichas actuales, 31 modelos únicos; 10 altas y 15 fotos nuevas. Cortos web: 37. Blanco XL-187 pendiente por dos precios.** Véase [revisión actual](../../verificacion-cortos-whatsapp-2026-10-15/REVISION.md). El cuerpo siguiente es histórico.\n\n'
old_report=(OLD/'cortos/REPORTE.md').read_text(encoding='utf-8')
if not old_report.startswith(banner):(OLD/'cortos/REPORTE.md').write_text(banner+old_report,encoding='utf-8')

main_result=read(OLD/'resultado-aplicado.json')
if not (HERE/'resultado-general-anterior.json').exists():save(HERE/'resultado-general-anterior.json',main_result)
main_result.update({'revision':read(ROOT/'review/categorias-confirmadas.json')['revision'],'total_prendas':155,
                    'total_fotos':251,'totales':result['totales_web'],
                    'diferencias_pendientes':{'Largos':0,'Cortos con brillo':5,'Cortos':-7,'Bandage':0},
                    'advertencia_diferencias':'Diferencias aritméticas con objetivos: positivo significa menos modelos web y negativo significa más. No son faltantes físicos. Cortos actual WhatsApp tiene 31 modelos únicos; web 37 y un blanco pendiente de precio.',
                    'conciliacion_cortos_actual':{k:result[k] for k in ['fichas_observadas','prendas_unicas_identificadas','prendas_fuente_publicadas','modelos_web_cortos','nuevos_modelos_detectados']},
                    'conservacion':'Las categorías y 236 fotos previas permanecen. Se añaden 10 Cortos y 15 fotos. XL-069 cambia nombre/precio por su ficha exacta y mantiene su URL; XL-117 adopta S/379 de WhatsApp por instrucción del usuario.'})
main_result['pendientes']=['Confirmar cuál ficha actual del blanco repetido prevalece: S/329 o S/319. XL-187 preparado sin publicar.',
                          'Confirmar cuál ficha actual del verde XL-066 prevalece: S/429 o S/359. La ficha con el nombre completo muestra S/429.',
                          'Conciliar los siete Cortos publicados que no figuran en la lista actual de Vestidos Cortos y las discrepancias comerciales de Brillos.']
save(OLD/'resultado-aplicado.json',main_result)
main_banner='> Actualización del 16/10/2026: **155 prendas y 251 fotos. Cortos: 37 publicados; la colección WhatsApp tiene 31 modelos únicos, uno pendiente de precio.** Véase [revisión de Cortos](../verificacion-cortos-whatsapp-2026-10-15/REVISION.md). Los conteos siguientes son históricos.\n\n'
main_md=(OLD/'CONCILIACION.md').read_text(encoding='utf-8')
if not main_md.startswith(main_banner):(OLD/'CONCILIACION.md').write_text(main_banner+main_md,encoding='utf-8')
pending=(OLD/'PENDIENTES-CATALOGO.md').read_text(encoding='utf-8')
pending=pending.replace('| Cortos | 27 | 30 | 3 |','| Cortos | 37 | 30 | −7 |')
pending=re.sub(r'La lista guardada de Cortos tiene 33 fichas[^\n]*?La revisión actual de Brillos', 'La revisión actual de Cortos tiene 33 fichas, 31 modelos únicos, cero identidades desconocidas y un blanco pendiente de precio. Se publicaron diez altas; web Cortos 37. La revisión actual de Brillos',pending)
pending=re.sub(r'## Referencias históricas de Cortos sin foto asociada[\s\S]*?(?=## Colección de Brillo)', '## Cortos: identidades conciliadas\n\nSe identificaron las 33 fichas actuales: 31 modelos únicos, dos duplicados. Diez altas publicadas, blanco XL-187 preparado sin publicar por S/329 o S/319. El verde XL-066 aparece a S/429 y S/359. La web tiene 37 Cortos, incluidos siete de otras referencias. Véase la [revisión actual](../verificacion-cortos-whatsapp-2026-10-15/REVISION.md).\n\n',pending)
pending=re.sub(r'- XL-069 y XL-131:[^\n]*', '- XL-069 quedó identificado con su foto como Vestido corto drapeado de mangas, S/379; XL-131 conserva el azul halter a S/389. La asociación de nombre y precio ya está corregida.',pending)
pending=pending.replace('XL-117 tiene un conflicto de precio S/379 frente a S/389 pendiente de confirmar.','XL-117 adopta S/379 de la ficha actual de WhatsApp según la instrucción posterior del usuario.')
(OLD/'PENDIENTES-CATALOGO.md').write_text(pending,encoding='utf-8')

# El precio de XL-117 ya no queda pendiente después de la instrucción del usuario.
for path in [ROOT/'review/verificacion-brillo-whatsapp-2026-10-15/CONCILIACION-43.json',OLD/'brillo/matriz43.json']:
    data=read(path)
    for row in data['matriz']:
        if row['id']==117:
            row['precio_publicado']=379
            row['precio_coincide']=True
            row['observacion']='Mismo XL-117, código 2062. S/379 aplicado desde la ficha actual de WhatsApp por instrucción posterior del usuario. Frente y espalda conservados.'
    data['actualizacion_precios']='16/10/2026: XL-117 S/379 de WhatsApp aplicado como referencia absoluta, según instrucción del usuario.'
    if 'precios_coincidentes' in data:data['precios_coincidentes']=43
    if 'diferencias_precio' in data:data['diferencias_precio']=[]
    save(path,data)
price_banner='> Actualización de precio del 16/10/2026: **XL-117 ahora S/379**, tomado de WhatsApp como referencia absoluta por instrucción del usuario. La discrepancia con el histórico S/389 ya no queda pendiente.\n\n'
for path in [ROOT/'review/verificacion-brillo-whatsapp-2026-10-15/REVISION.md',OLD/'brillo/REPORTE.md']:
    text=path.read_text(encoding='utf-8')
    if not text.startswith(price_banner):path.write_text(price_banner+text,encoding='utf-8')

# Conservar borrador general anterior como histórico y entregar el mensaje actualizado de Cortos.
previous_message=(OLD/'MENSAJE-PARA-ENCARGADO.txt').read_text(encoding='utf-8')
if not (HERE/'mensaje-general-anterior.txt').exists():(HERE/'mensaje-general-anterior.txt').write_text(previous_message,encoding='utf-8')
(OLD/'MENSAJE-PARA-ENCARGADO.txt').write_text(message+'\nAdicionalmente, siguen pendientes las diferencias de colección de Brillos documentadas en su revisión. XL-117 ya se actualizó a S/379 de WhatsApp según la instrucción del usuario.\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['fichas_observadas','prendas_unicas_identificadas','prendas_fuente_publicadas','modelos_web_cortos','nuevos_modelos_detectados']},ensure_ascii=True))
