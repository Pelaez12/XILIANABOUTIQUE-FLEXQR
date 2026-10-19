"""Conciliar las 43 fichas actuales con las prendas únicas de la web."""
from pathlib import Path
from collections import Counter
import json, re, unicodedata, base64, html

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=ROOT/'review/conciliacion-final-2026-10-15'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
norm=lambda s:''.join(c for c in unicodedata.normalize('NFD',s).lower() if c.isalnum())
products=read(ROOT/'review/publicados-confirmados.json')
by_id={p['id']:p for p in products}
source=read(HERE/'lista-tramo-final.json')
previous=read(HERE/'matriz-antes.json')['matriz']
assert len(source)==len(previous)==43
matrix=[]
for index,(live,old) in enumerate(zip(source,previous),1):
    text=live.get('textoDOM') or live['texto']
    assert norm(text).startswith(norm(old['nombre_catalogo'])),index
    prices=[float(v) for v in re.findall(r'PEN[^0-9]*([0-9]+\.[0-9]{2})',text)]
    assert prices and prices[0]==old['precio_catalogo']
    ident={28:183,30:184,33:39,39:117}.get(index,old.get('id'))
    assert ident in by_id
    p=by_id[ident]
    row=dict(old)
    row.update({'id':ident,'nombre_publicado':p['name'],'categoria_actual':p['category'],
                'precio_publicado':p['price'],'foto_actual':p['photos'][0]['src'],
                'precio_catalogo':prices[0],'texto_actual_observado':text,
                'nombre_verificado_actual':True,'precio_coincide':prices[0]==p['price'],
                'estado':'Asociado a prenda publicada','fecha_verificacion':'2026-10-15'})
    if index in [28,30]:row['observacion']='Ficha, código y foto oficial revisados; alta verificada, distinta de las prendas anteriores.'
    if index==33:row['observacion']='Alias duplicado de la fila 11: mismo código 644, mismo precio S/329 y misma fotografía de XL-039. No añadir otro vestido ni repetir su foto.'
    if index==39:row['observacion']='Misma prenda que XL-117, antes llamada Vestido negro brillante. Código actual 2062. Ficha Brillos S/379 frente a precio web/histórico Gala S/389. Se conserva S/389 pendiente de confirmación. Se añade la espalda oficial.'
    matrix.append(row)
unique=set(r['id'] for r in matrix)
assert len(unique)==42
conflicts=[r for r in matrix if not r['precio_coincide']]
assert [r['id'] for r in conflicts]==[117]
cortos=sorted({r['id'] for r in matrix if r['categoria_actual']=='Cortos'})
assert cortos==[54,118,121,122,172]
extra=[p for p in products if p['category']=='Cortos con brillo' and p['id'] not in unique]
assert [p['id'] for p in extra]==[127]
totals=dict(Counter(p['category'] for p in products))
result={'fecha':'2026-10-15','fuente':'WhatsApp Web del usuario, misma pestaña 1748733500, catálogo +51 930 527 248',
        'revision':'conciliacion-catalogo-2026-10-15-con-XL179-184',
        'fichas_actuales_observadas':43,'prendas_unicas_asociadas':42,'referencias_sin_asociar':0,
        'precios_coincidentes':42,'diferencias_precio':conflicts,
        'duplicacion_dentro_de_brillos':{'filas':[11,33],'id':39,'codigo':'644','precio':329},
        'ids_fuente_en_cortos':cortos,'ids_brillo_web_fuera_lista':[127],
        'conteo_brillo_web':'43 fichas − 1 alias duplicado − 5 prendas en Cortos + XL-127 = 38 prendas únicas en Cortos con brillo.',
        'altas':[183,184],'espalda_anadida':117,'totales_web':totals,'total_prendas':145,'total_fotos':236,
        'alcance':'Las 43 fichas de Brillos tienen nombre y precio actual observados y una asociación por identidad documentada. Las fotografías previas se conservan; se revisaron ampliadas las cuatro referencias pendientes, identificando dos altas y dos alias. La revisión completa de Cortos/Largos/Gala no se considera cerrada por esta comprobación de Brillos.',
        'matriz':matrix}
save(HERE/'CONCILIACION-43.json',result)

# Mantener actualizado el informe de conciliación anterior, conservando su estado previo.
if not (HERE/'matriz43-anterior.json').exists():save(HERE/'matriz43-anterior.json',read(OLD/'brillo/matriz43.json'))
updated=read(OLD/'brillo/matriz43.json')
updated.update({'referencias_asociadas':43,'referencias_sin_asociacion':0,'prendas_unicas':42,
                'asociadas_por_categoria_actual':dict(Counter(r['categoria_actual'] for r in matrix)),
                'brillo_actual_no_en_lista43':[{'id':127,'nombre':by_id[127]['name'],'precio':549,'foto':by_id[127]['image']}],
                'matriz':matrix,'advertencia':result['conteo_brillo_web']+' Hay una diferencia de precio pendiente en XL-117; no son cinco prendas nuevas faltantes.',
                'actualizacion':'Verificación actual de las 43 fichas en ../verificacion-brillo-whatsapp-2026-10-15/CONCILIACION-43.json.'})
save(OLD/'brillo/matriz43.json',updated)
old_result=read(OLD/'resultado-aplicado.json')
if not (HERE/'resultado-anterior.json').exists():save(HERE/'resultado-anterior.json',old_result)
old_result.update({'revision':result['revision'],'total_prendas':145,'total_fotos':236,'totales':totals,
                   'diferencias_pendientes':{'Largos':0,'Cortos con brillo':5,'Cortos':3,'Bandage':0},
                   'conciliacion_brillo_actual':{k:result[k] for k in ['fichas_actuales_observadas','prendas_unicas_asociadas','referencias_sin_asociar','precios_coincidentes','conteo_brillo_web']},
                   'advertencia_diferencias':'La diferencia aritmética frente a 43 no representa prendas nuevas faltantes: hay un duplicado comercial, cinco referencias que van en Cortos y XL-127 adicional.',
                   'conservacion':'Las 143 prendas anteriores conservan sus campos. XL-117 añade su espalda. Dos altas nuevas, XL-183/184, con una foto real cada una. Total 145 prendas y 236 fotos.'})
old_result['altas']=[r for r in old_result['altas'] if r['id'] not in [183,184]]+[
    {'id':i,'nombre':by_id[i]['name'],'categoria':'Cortos con brillo','precio':389,'fotos':1,'evidencia':by_id[i]['priceSource']['evidencia']} for i in [183,184]]
old_result['pendientes']=['Confirmar el precio definitivo de XL-117: ficha actual Brillos S/379 y web/histórico Gala S/389.',
                         'El encargado debe confirmar las cinco discrepancias de colección Brillos/Cortos y el alias verde duplicado.',
                         'Continúa pendiente la conciliación de la lista definitiva de Cortos: fuente guardada 33 fichas, cantidad indicada 30, web 27.']
save(OLD/'resultado-aplicado.json',old_result)

report='''# Verificación de Cortos con brillo — 15 de octubre de 2026

Se revisaron las **43 fichas actuales** en la misma pestaña de WhatsApp del usuario, contrastando sus nombres y precios con la web. Se ampliaron las fotos de las cuatro referencias que seguían pendientes de asociación.

## Cambios aplicados

- **XL-183 · Vestido corto azul pedrería y strass · S/389 · código 2008.** Una fotografía de frente. Diseño nuevo, distinto del azul de S/329 y de los otros azules guardados.
- **XL-184 · Vestido dorado corto asimétrico de flecos · S/389 · código 1965.** Una fotografía de frente. Es distinto del Bandage dorado XL-129, código 2070.
- **XL-117 · Vestido negro brillante:** se añadió la espalda oficial de la ficha «Vestido elegante estraple negro con plateado», código 2062, conservando el frente existente primero.
- La ficha verde «Vestido corto de lentejuelas verde» de S/329 es el mismo XL-039 que «Vestido verde de lentejuelas y mostacillas»: ambas usan código 644, mismo precio y misma foto. Se asoció sin duplicarlo.

Las imágenes son fotografías reales del catálogo, recortadas únicamente para retirar la interfaz. No se cambió el vestido, la modelo, el color ni el fondo. No se añadió una espalda inexistente a los dos modelos nuevos.

## Conteo conciliado

**43 fichas comerciales = 42 prendas únicas**, porque el verde código 644 aparece dos veces.

Cinco de esas prendas están en **Cortos** siguiendo la separación entre base lisa con detalles y brillo predominante: XL-054, XL-118, XL-121, XL-122 y XL-172. XL-054 tiene además indicación individual explícita del usuario. Debe confirmarse con el encargado la colección comercial definitiva de estos cinco modelos.

La colección web queda en **38 Cortos con brillo**: 43 fichas − 1 duplicado − 5 Cortos + XL-127, confirmado por el usuario y que no figura en esa lista de 43. Las 43 referencias de Brillos tienen asociación; no quedan cuatro vestidos desconocidos como en la revisión anterior.

| Colección web | Prendas únicas |
|---|---:|
| Largos | 25 |
| Gala | 32 |
| Cortos con brillo | 38 |
| Cortos | 27 |
| Bandage | 22 |
| Liquidación (categoría principal) | 1 |

**Total web: 145 prendas y 236 fotos.** La cifra de cada colección comercial no equivale automáticamente a stock físico. La conciliación completa de Cortos continúa pendiente.

## Precios

**42 de las 43 referencias coinciden con los precios publicados después de las dos altas.** La excepción es XL-117: la ficha actual de Brillos muestra **S/379**, mientras la web y el registro histórico de Gala muestran **S/389**. Se conserva S/389 hasta que el encargado confirme cuál corresponde; no se presenta como un precio definitivamente verificado. Todos los vestidos web mantienen precio numérico.

## Evidencia

- `CONCILIACION-43.json`: las 43 filas, nombre, precio, ID web, colección y observaciones.
- `lista-tramo-final.json`: texto DOM de las 43 fichas observadas en la misma sesión.
- `43-fichas-final-pantalla.png`: final de la lista, con la última ficha negra de S/219.
- `azul389-ficha.png`, `dorado389-ficha.png`, `verde329-ficha.png`, `negro379-ficha.png`: fichas y códigos.
- `*-pantalla.png` y `*-encuadre.json`: origen de los recortes oficiales.
- `respaldo-importacion/`: datos anteriores a las dos altas y la espalda añadida.
'''
(HERE/'REVISION.md').write_text(report,encoding='utf-8')
(OLD/'brillo/REPORTE.md').write_text(report+'\n## Matriz actual\n\n| Fila | Nombre WhatsApp | ID web | Categoría web | Precio WhatsApp | Precio web |\n|---|---|---|---|---:|---:|\n'+''.join(f'| {r["fila_catalogo"]} | {r["nombre_catalogo"]} | XL-{r["id"]:03d} | {r["categoria_actual"]} | S/ {r["precio_catalogo"]:.2f} | S/ {r["precio_publicado"]:.2f} |\n' for r in matrix),encoding='utf-8')
pending=(OLD/'PENDIENTES-CATALOGO.md').read_text(encoding='utf-8')
pending=pending.replace('| Cortos con brillo | 36 | 43 | 7 |','| Cortos con brillo | 38 | 43 | 5 |')
pending=re.sub(r'La lista de Brillo tiene 43 fichas:[^\n]+','La revisión actual de Brillos confirmó 43 fichas, 42 prendas únicas y cero referencias sin asociación. La diferencia con 38 prendas web se explica por un alias verde duplicado, cinco prendas en Cortos y XL-127 adicional. XL-117 tiene un conflicto de precio S/379 frente a S/389 pendiente de confirmar.',pending)
pending=re.sub(r'## Cuatro referencias de Brillo sin foto asociada[\s\S]*?(?=## Referencias históricas de Cortos)', '## Brillos: identidades conciliadas\n\nLas cuatro referencias anteriores están resueltas: azul de strass → XL-183; dorado asimétrico de flecos → XL-184; verde código 644 → alias de XL-039; negro estraple código 2062 → XL-117, con espalda añadida. Confirmar con el encargado el precio de XL-117 y las discrepancias de colección. Véase la [revisión actual](../verificacion-brillo-whatsapp-2026-10-15/REVISION.md).\n\n',pending)
(OLD/'PENDIENTES-CATALOGO.md').write_text(pending,encoding='utf-8')
old_md=(OLD/'CONCILIACION.md').read_text(encoding='utf-8')
banner='> Actualización posterior: **145 prendas y 236 fotos**. Se verificaron las 43 fichas de Brillos: 42 prendas únicas, dos altas y dos alias. Véase [revisión actual](../verificacion-brillo-whatsapp-2026-10-15/REVISION.md). Los conteos anteriores que siguen abajo son históricos.\n\n'
if not old_md.startswith(banner):(OLD/'CONCILIACION.md').write_text(banner+old_md,encoding='utf-8')

message='''Hola, terminamos de contrastar las 43 fichas de «Vestidos Cortos Brillos» de WhatsApp con las fotos, nombres y precios de la web.

Encontramos estas diferencias para confirmar:

1. Hay 43 fichas, pero 42 vestidos distintos: «Vestido verde de lentejuelas y mostacillas» y «Vestido corto de lentejuelas verde», ambos a S/329 y código 644, tienen la misma foto. ¿Dejamos una sola ficha y cuál nombre prefieres?

2. «Vestido elegante estraple negro con plateado», código 2062, es el mismo que tenemos como «Vestido negro brillante» (XL-117). La ficha de Brillos dice S/379 y la web/registro anterior de Gala dicen S/389. ¿Cuál es el nombre y precio definitivo? Ya añadimos su foto de espalda, sin duplicar el vestido.

3. Estos cinco aparecen en Brillos de WhatsApp y en Cortos de la web porque el vestido es principalmente liso con decoración localizada:
• XL-054, Vestido corto de diamantes de imitación plateadas — S/349.
• XL-118, Vestido negro asimétrico con lentejuelas — S/369.
• XL-172, Vestido corto negro con mangas plateadas — S/119.50.
• XL-121, Vestido corto negro de tiras — S/79.
• XL-122, Vestido corto negro — S/219.
¿Confirmas la colección definitiva de cada uno?

4. Ya incorporamos dos modelos que sí faltaban: azul de pedrería y strass, código 2008, S/389; y dorado corto asimétrico de flecos, código 1965, S/389. Este dorado es distinto del Bandage dorado código 2070.

Con las referencias identificadas y las categorías corregidas, Brillos web tiene 38 vestidos: 43 fichas menos un duplicado, menos los cinco que van en Cortos, más el vino XL-127 de S/549 confirmado previamente. Necesitamos confirmar las diferencias anteriores antes de hacer coincidir los números.

La web queda en 25 Largos, 32 Gala, 38 Cortos con brillo, 27 Cortos, 22 Bandage y 1 Liquidación como categoría principal. Para cerrar Cortos, la lista guardada tiene 33 fichas y la cantidad indicada fue 30: ¿nos compartes la lista definitiva de los 30 modelos y cómo se cuentan las ofertas?

También hay dos azules distintos llamados «Vestido drapeado azul asimétrico» a S/389 (XL-069/131) y dos diseños vino con el nombre «Vestido vino strapless de tirantes con copas de pedrería» a S/549 (XL-127/140). Necesitamos los nombres definitivos para distinguirlos correctamente.
'''
(HERE/'MENSAJE-PARA-ENCARGADO.txt').write_text(message,encoding='utf-8')
(OLD/'MENSAJE-PARA-ENCARGADO.txt').write_text(message,encoding='utf-8')

def data_image(src):
    path=ROOT/src
    mime='image/png' if path.suffix.lower()=='.png' else 'image/jpeg'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
cards=[]
for r in matrix:
    label='Precio por confirmar' if not r['precio_coincide'] else ('Alias de fila 11' if r['fila_catalogo']==33 else ('Añadido' if r['id'] in [183,184] else 'Asociado'))
    cards.append(f'<article><img src="{data_image(r["foto_actual"])}" alt="{html.escape(r["nombre_publicado"])}"><div><small>Ficha {r["fila_catalogo"]} · XL-{r["id"]:03d} · {html.escape(label)}</small><h2>{html.escape(r["nombre_catalogo"])}</h2><p>WhatsApp S/ {r["precio_catalogo"]:.2f} · Web S/ {r["precio_publicado"]:.2f}</p><p>Colección web: <b>{html.escape(r["categoria_actual"])}</b></p></div></article>')
page='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>43 fichas de Brillos — verificación</title><style>body{font:16px/1.5 system-ui,sans-serif;color:#292929;background:#f7f6f3;margin:0}main{max-width:1250px;margin:auto;padding:30px 20px}h1{font-size:clamp(26px,5vw,42px);line-height:1.15}header{max-width:900px;margin-bottom:36px}header p{margin:12px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}article{background:white;border:1px solid #ddd}article img{width:100%;height:330px;object-fit:contain;background:#f1f1ef}article div{padding:16px}h2{font-size:17px;line-height:1.4;margin:8px 0}article p{font-size:14px}small{color:#665b48}a{color:#65512c}</style><main><header><p>XILIANA BOUTIQUE · 15 OCT 2026</p><h1>43 fichas, 42 vestidos distintos</h1><p>Revisión en la misma pestaña de WhatsApp. Todas las fichas de Brillos tienen una asociación. Se añadieron XL-183 y XL-184 y la espalda de XL-117.</p><p><b>Brillos web: 38 prendas.</b> 43 fichas − 1 verde duplicado − 5 prendas que van en Cortos + XL-127. El encargado debe confirmar esas diferencias de colección.</p><p><b>Precio pendiente:</b> XL-117, S/379 en la ficha actual de Brillos y S/389 en la web y el registro anterior de Gala. Se conserva S/389.</p><p>Fotos de frente primero. Las fotografías oficiales se conservan sin alterar modelo ni vestido. Las etiquetas «Asociado» expresan la relación con las prendas guardadas; esta revisión no confirma stock físico.</p></header><section class="grid">'''+''.join(cards)+'</section></main></html>'
(HERE/'COMPARACION-43.html').write_text(page,encoding='utf-8')
print(json.dumps({k:result[k] for k in ['fichas_actuales_observadas','prendas_unicas_asociadas','referencias_sin_asociar','precios_coincidentes','conteo_brillo_web','totales_web']},ensure_ascii=True))
