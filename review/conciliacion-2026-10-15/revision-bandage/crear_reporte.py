import json, re
from pathlib import Path

root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
text=(root/'products.js').read_text(encoding='utf-8')
products=json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',text)[1])
bandage=[p for p in products if p['category']=='Bandage']
photos=sum(len(p['photos']) for p in bandage)
faltantes=[
  {
    'nombre':'Vestido largo Bandage color Rojo', 'precio_pen':549,
    'estado':'Registro visual distinto de XL-073; sin asociación segura a las 225 fotos actuales.',
    'fuente_texto':['review/catalogo-whatsapp-2026-10-12/largos-completo.json, entrada 13','review/catalogo-verificado-2026-10-06.json, registros: mismo nombre'],
    'fuente_visual':'review/grabaciones-2026-10-06/video-1.jpg, segundo panel, fila debajo del animal print',
    'recorte_inspeccion':'review/conciliacion-2026-10-15/revision-bandage/fuente-rojo-largo.png',
    'diferencias':'Miniatura de vestido largo rojo asimétrico con abertura y una pose de brazo elevado. XL-073 es midi rojo de tirantes y escote profundo, en una pose con los dos brazos bajados; su propia miniatura aparece en video-4 y bandage-precios a S/389. Los rojos largos actuales tienen otros escotes, mangas o decoración.',
    'id_asociado_seguro':None,
    'accion_recomendada':'Mantener como pendiente de foto original identificada. No reemplazar ni renombrar XL-073.'
  },
  {
    'nombre':'VESTIDO BANDAGE Rojo corto de pedrería plateada', 'precio_pen':379,
    'estado':'Nombre, precio y miniatura constan en video-4; sin asociación segura a una foto actual.',
    'fuente_texto':['review/catalogo-verificado-2026-10-06.json, registros: mismo nombre'],
    'fuente_visual':'review/grabaciones-2026-10-06/video-4.jpg, cuarto panel, tercera fila',
    'recorte_inspeccion':'review/conciliacion-2026-10-15/revision-bandage/fuente-rojo-corto.png',
    'diferencias':'Miniatura de vestido rojo corto con parte superior recta y detalles plateados, en fondo claro. No coincide visualmente con XL-049 (lentejuelas, una manga, foto de boutique), XL-152 (copas plateadas y cadenas, modelo pelirroja) o XL-166 (lentejuelas, una manga corta caída y encuadre sin cabeza). La miniatura no basta para identificar su archivo original.',
    'id_asociado_seguro':None,
    'accion_recomendada':'Mantener como pendiente de asociación/foto. No mover XL-049, XL-152 o XL-166 por parecido de color.'
  },
  {
    'nombre':'Vestido Bandage Negro/Amarillo', 'precio_pen':449,
    'estado':'Nombre, precio y miniatura documentados el 12 de octubre; sin foto actual asociable.',
    'fuente_texto':['review/catalogo-whatsapp-2026-10-12/todos-articulos.json, i=152'],
    'fuente_visual':'review/catalogo-whatsapp-2026-10-12/todos-final-panel.png, cuarta fila',
    'recorte_inspeccion':None,
    'diferencias':'Miniatura negra de mangas largas con líneas amarillas verticales y geométricas sobre fondo blanco. XL-126 es un conjunto visual negro/blanco de top strapless y parte inferior blanca; XL-147 es un vestido negro/blanco sin mangas. Ninguno comparte el diseño de la miniatura negro/amarillo.',
    'id_asociado_seguro':None,
    'accion_recomendada':'Mantener pendiente de foto original identificada. No tratar como alias de Negro/Blanco.'
  }
]
reporte={
  'fecha':'2026-10-15',
  'alcance':'Revisión independiente de Bandage. Vistas las 139 fotos principales en las láminas de auditoría, las 86 adicionales y las nuevas láminas grandes de Gala/Largos. Las categorías vigentes se toman de products.js, no de las etiquetas antiguas de las láminas.',
  'criterio':'Bandage requiere identificación de catálogo o usuario. Una silueta ajustada no prueba el tejido ni la categoría.',
  'resultado':'21 prendas Bandage publicadas válidas. Ningún producto de otra categoría tiene evidencia suficiente para convertirse en el número 22. Hay tres registros Bandage adicionales documentados sin asociación segura de foto original.',
  'cantidad_publicada':len(bandage),
  'cantidad_fotos_bandage':photos,
  'ids_validos':[p['id'] for p in bandage],
  'prendas_validas':[{'id':p['id'],'nombre':p['name'],'precio_pen':p['price'],'fotos':[{'src':q['src'],'vista':q.get('view'),'sourceIndex':q.get('sourceIndex'),'sourceAttachment':q.get('sourceAttachment')} for q in p['photos']]} for p in bandage],
  'faltantes_de_matching':faltantes,
  'duplicados':{
    'bandage_publicados':'No se observó un duplicado visual suficiente para eliminar un registro.',
    'amarillos':'XL-076 mini y XL-077 midi son modelos distintos, documentados con sus propias miniaturas y precios 389/429. XL-116 tiene confirmación explícita del usuario para R057/R058; se mantiene como tercer amarillo separado.',
    'negros_plateados':'XL-072 (R150, asimétrico de un hombro) y XL-124 (R088/R089, bustier y tirantes) son distintos.',
    'negro_blanco':'XL-126 y XL-147 son diseños distintos; ninguno es la miniatura negro/amarillo.',
    'conjunto':'XL-115 es un conjunto confirmado expresamente por el usuario. No se divide para aumentar el conteo.'
  },
  'accesorios':[
    {'nombre':'Falda Bandage Dress cruzada palo rosa, negro y melón','precio_pen':219,'fuente':'review/grabaciones-2026-10-06/video-4.jpg y bandage-precios.png; catalogo-verificado-2026-10-06.json solo_vestido=false','decision':'Registro de falda, no prueba de vestido adicional ni de un nuevo conjunto. No contarlo automáticamente como Bandage 22.'}
  ],
  'candidatos_ajustados_sin_evidencia_bandage':[65,67,68,80,84,119,121,122,157],
  'decision_candidatos':'Se mantienen en sus categorías actuales. Nombre, silueta, precio o drapeado no prueban Bandage; no se obtuvo asociación con una miniatura Bandage pendiente.',
  'limites':'No se establece qué modelo quiso incluir el encargado en su cifra de 22. Las miniaturas sí distinguen tres registros pendientes, pero no proporcionan una foto original recuperada ni una asociación segura a un ID actual. No inferir totales de vestidos a partir de todos-articulos.json, que incluye accesorios y tops.',
  'archivos_compartidos_modificados':False
}
(out/'reporte-bandage.json').write_text(json.dumps(reporte,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# Revisión de Bandage — 15 de octubre de 2026','',reporte['resultado'],'',
    'Se inspeccionaron las 139 fotografías principales y las 86 adicionales de las láminas de auditoría, contrastadas con las categorías actuales de `products.js`. Se revisaron además las láminas grandes de Gala y Largos y las miniaturas guardadas de WhatsApp. No se modificó el catálogo.','',
    '## Las 21 prendas actuales','',
    '| ID | Nombre actual | Precio S/ | Original principal |','| --- | --- | ---: | --- |']
for p in bandage:
    md.append(f"| XL-{p['id']:03d} | {p['name']} | {p['price']:.2f} | {p['photos'][0]['src']} |")
md+=['',f'Total: **21 prendas, {photos} fotos**. Los amarillos mini/midi XL-076/077 son diferentes; XL-116 tiene su propia confirmación R057/R058. Los negros plateados XL-072/124 y los negro/blanco XL-126/147 también son distintos. El conjunto XL-115 se conserva como una prenda publicada.','',
     '## Registros Bandage sin foto original asociada','',
     '| Nombre de catálogo | Precio S/ | Evidencia visual |','| --- | ---: | --- |']
for p in faltantes:
    md.append(f"| {p['nombre']} | {p['precio_pen']:.2f} | {p['fuente_visual']} |")
for p in faltantes:
    md+=['',f"### {p['nombre']}",'',p['diferencias'],'',p['accion_recomendada']]
md+=['','## Qué sostiene el conteo','',
     'No se encontró un producto de Cortos, Cortos con brillo, Largos o Gala con asociación confirmada a un modelo Bandage pendiente. Los ajustados XL-065/067/068/080/084/119/121/122/157 no se deben trasladar por silueta.','',
     'La falda Bandage de S/219 es un artículo separado documentado como falda. No demuestra un vestido 22 y no debe extraerse del conjunto XL-115 para aumentar el número.','',
     'La cifra 22 permanece sin conciliar. Existen tres registros adicionales distintos en el catálogo guardado, pero ninguna foto original actual se puede asociar de forma segura. El rojo largo de S/549 es claramente diferente del XL-073 de S/389. Con la evidencia disponible, convertir 21 en 22 por una reclasificación o un alias sería injustificado.','',
     'Los recortes `fuente-rojo-largo.png` y `fuente-rojo-corto.png` conservan el panel original de la grabación para revisión. `comparacion-rojos.jpg` permite compararlo con los diez rojos actuales más próximos. Las miniaturas distinguen diseños; su resolución no reemplaza una foto original.','']
(out/'REVISION-BANDAGE.md').write_text('\n'.join(md),encoding='utf-8')
print(f'Reporte listo: {len(bandage)} modelos, {photos} fotos, {len(faltantes)} registros pendientes.')
