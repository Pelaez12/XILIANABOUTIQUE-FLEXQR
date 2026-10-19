from pathlib import Path
import json, re, textwrap
from PIL import Image, ImageOps, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
source = json.loads((root/'review/conciliacion-2026-10-15/revision-cortos/reporte-cortos.json').read_text(encoding='utf-8-sig'))
raw = (root/'products.js').read_text(encoding='utf-8')
products = json.loads(raw.split('export const products = ')[1].split(';\nexport const categories')[0])
byid = {p['id']: p for p in products}
rows = source['conciliacion_oficial']['filas_detalladas']
for r in rows:
    if r['fila_oficial'] == 20:
        r['ids_candidatos'] = [131]
        r['estado'] = 'Coincidencia visual resuelta: la miniatura oficial es XL-131'
        r['observacion'] = 'Captura cortos-precios.png y video F107 muestran escote halter y azul intenso, iguales a XL-131. XL-069 tiene mangas amplias, escote V y azul celeste; es otra prenda. El nombre y precio de XL-069 requieren otra referencia.'
    r['categorias_actuales'] = [byid[i]['category'] for i in r['ids_candidatos']]
    r.pop('categorias_guardadas', None)
    if r['fila_oficial'] <= 20:
        r['evidencia_visual'] = 'review/grabaciones-2026-10-06/cortos-precios.png; review/video-catalogo-2026-10-08/frames/F106.jpg–F110.jpg'
    else:
        r['evidencia_visual'] = 'Asociaciones de fotos recibidas en confirmaciones-usuario.json. No hay captura completa legible de las filas 21–33 en los dos PNG cortos-superior/inferior de octubre12.'

unique_ids = sorted({i for r in rows for i in r['ids_candidatos']})
unmatched = [r['fila_oficial'] for r in rows if not r['ids_candidatos']]
new = {
    'fecha':'2026-10-15',
    'criterio':'Cruce comercial de nombres, precios y miniaturas oficiales. La clasificación visual general no sustituye una coincidencia de prenda.',
    'recomendaciones_confirmadas':[
        {'id':68,'de':byid[68]['category'],'a':'Cortos','motivo':'Nombre exacto y miniatura coinciden con fila17 de la colección oficial Cortos. Fotografías R065/R066/R164 y precio S/299 coinciden. La falda casi al tobillo no invalida la ubicación comercial usada por el propietario.'},
        {'id':81,'de':byid[81]['category'],'a':'Cortos','motivo':'Nombre exacto de fila28 y confirmaciones-usuario.json R140 clasifican explícitamente Cortos sin brillo, S/319. Es una foto real asociada; no debe cambiar por la palabra largo aislada.'}
    ],
    'ids_asociados_lista_oficial':unique_ids,
    'filas_asociadas':len(rows)-len(unmatched),
    'filas_no_asociadas':unmatched,
    'prendas_actuales_cortos_fuera_de_lista_oficial':sorted({p['id'] for p in products if p['category']=='Cortos'} - set(unique_ids)),
    'cantidad_cortos_actual':sum(p['category']=='Cortos' for p in products),
    'cantidad_cortos_tras_restaurar_68_81':sum(p['category']=='Cortos' for p in products)+sum(byid[i]['category']!='Cortos' for i in [68,81]),
    'faltantes_para_meta30_tras_restaurar':30-(sum(p['category']=='Cortos' for p in products)+sum(byid[i]['category']!='Cortos' for i in [68,81])),
    'filas':rows,
    'advertencias_fuente':[
        'cortos-superior.png y cortos-inferior.png de octubre12 presentan los mismos primeros10 artículos. No verifican las miniaturas de las33 filas.',
        'Filas6y10: misma miniatura blanca con perlas, dos nombres y precios diferentes S/329 y S/319; posible duplicado de catálogo sin confirmar. No crear dos prendas usando la misma foto.',
        'Los16 registros sin asociación no equivalen a16 prendas nuevas seguras: una pareja parece duplicada y falta conocer el inventario vigente del dueño.',
        'XL-069 y XL-131 son prendas distintas. La ficha oficial Vestido drapeado azul asimétrico corresponde visualmente a131; no fusionar69con131.',
        'No hay cinco candidatos adicionales de Cortos demostrados entre las139 fotografías. Las miniaturas oficiales de azul con botones, lila rib, blanco perlas, verde agua tirantes, blanco capa, azul cinturón, verde escote y verde rosas son diferentes a los modelos publicados.'
    ]
}
(out/'matriz-cortos.json').write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

fontpath = 'C:/Windows/Fonts/arial.ttf'
font = ImageFont.truetype(fontpath,19)
small = ImageFont.truetype(fontpath,17)
canvas = Image.new('RGB',(1500,900),'white')
draw = ImageDraw.Draw(canvas)
draw.text((20,12),'La miniatura oficial corresponde a XL-131; XL-069 es otro modelo',fill='#111111',font=font)
ref = Image.open(root/'review/grabaciones-2026-10-06/cortos-precios.png').convert('RGB')
refcrop = ref.crop((0,830,560,906))
refcrop.thumbnail((680,140))
canvas.paste(refcrop,(20,60))
for index,ident in enumerate([69,131,68,81]):
    p=byid[ident]
    picture=Image.open(root/p['photos'][0]['src'].removeprefix('./')).convert('RGB')
    picture=ImageOps.contain(picture,(335,600))
    x=20+index*370
    canvas.paste(picture,(x+(335-picture.width)//2,200))
    draw.text((x,808),f'XL-{ident:03d} | S/{p["price"]}',fill='#111111',font=small)
    lines=textwrap.wrap(p['name'],width=32)
    for j,line in enumerate(lines[:3]):draw.text((x,833+j*20),line,fill='#333333',font=small)
canvas.save(out/'referencias-cortos.jpg',quality=93)

lines = [
    '# Conciliación de Cortos por nombre y fotografía — 15 de octubre de 2026','',
    '## Correcciones con evidencia','',
    '- **XL-068 → Cortos**: fila17 de la colección oficial, misma miniatura rosa de cuello cuadrado y mangas, S/299. La clasificación comercial de la boutique incluye esta falda casi al tobillo.',
    '- **XL-081 → Cortos**: fila28, mismo nombre y S/319. `confirmaciones-usuario.json` lo ubica explícitamente en Cortos sin brillo, fotografía R140. La palabra «largo» no basta para contradecir esa fuente.',
    '- **Fila20 → XL-131**, ya en Cortos. La miniatura muestra azul intenso y escote halter. **XL-069** es celeste, escote V y mangas amplias: no es duplicado, pero su mismo nombre y precio necesitan otra referencia de catálogo. No se cambia el precio confirmado de ninguno.','',
    '## Conteo que se puede sostener','',
    f'Actuales: **{new["cantidad_cortos_actual"]} Cortos**. Restaurando 68 y81: **{new["cantidad_cortos_tras_restaurar_68_81"]}**. Para30 faltan **{new["faltantes_para_meta30_tras_restaurar"]} identidades**. Esta revisión no demuestra cinco prendas existentes mal ubicadas que puedan trasladarse automáticamente.','',
    'La lista histórica contiene33 filas. Se asocian17 con17 modelos publicados;16 filas quedan sin original asociado. Las filas6y10 parecen compartir miniatura, por lo que no representan automáticamente16 vestidos nuevos. Ocho Cortos actuales quedan fuera de esa lista histórica: '+', '.join(f'XL-{i:03d}' for i in new['prendas_actuales_cortos_fuera_de_lista_oficial'])+'. Esos ocho no deben borrarse: tienen fotos y otras confirmaciones.','',
    '## Evidencia visual adicional','',
    'Las miniaturas oficiales de azul con botones, lila en rib, blanco con perlas, verde agua de tirantes, blanco con capa, azul con cinturón, verde con escote y verde de rosas son diferentes de los139 modelos publicados. Se revisaron las láminas completas actuales además de las miniaturas. Para completar30 habrá que recuperar/confirmar cinco identidades del inventario vigente; no extraer cinco al azar de Gala.','',
    'El PNG `cortos-inferior.png` de octubre12 repite la parte superior. Por tanto no sirve para certificar por imagen las filas21–33. Las capturas de octubre6 y frames F106–F110 sí permiten comprobar las primeras20.','',
    '## Matriz de las33 filas','',
    '| Fila | Nombre del catálogo | Precio S/ | Prenda publicada | Estado |',
    '|---|---|---:|---|---|'
]
for r in rows:
    ident=', '.join(f'XL-{i:03d}' for i in r['ids_candidatos']) or '—'
    estado='Asociada' if r['ids_candidatos'] else 'Sin original asociado'
    if r['fila_oficial'] in [6,10]:estado+='; miniatura repetida6/10'
    if r['fila_oficial']==20:estado='Resuelta a131 por escote y color'
    lines.append(f'| {r["fila_oficial"]} | {r["nombre_oficial"]} | {r["precio_oficial"]:.2f} | {ident} | {estado} |')
(out/'REPORTE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in new.items() if k in ['filas_asociadas','cantidad_cortos_actual','cantidad_cortos_tras_restaurar_68_81','faltantes_para_meta30_tras_restaurar','prendas_actuales_cortos_fuera_de_lista_oficial']},ensure_ascii=False))
