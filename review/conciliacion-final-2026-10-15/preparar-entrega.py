"""Preparar una comparación revisable con nombres, precios y fotos existentes."""
from pathlib import Path
from collections import Counter
import json, re, html, base64
from PIL import Image

AUDIT=Path(__file__).resolve().parent
ROOT=AUDIT.parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
products=read(ROOT/'review/publicados-confirmados.json')
by_id={p['id']:p for p in products}
brillo=read(AUDIT/'brillo/matriz43.json')
cortos=read(AUDIT/'cortos/matriz-cortos.json')
totals=Counter(p['category'] for p in products)

lines=['# Referencias pendientes para confirmar con el encargado','',
    '15 de octubre de 2026. Cruce de nombres, precios, fotografías y colecciones de WhatsApp. Los totales indicados se refieren a colecciones, según aclaración del usuario. **La conciliación de identidades sigue abierta.**','',
    '| Colección | Web | Cantidad indicada | Diferencia neta |','|---|---:|---:|---:|']
for cat,target in [('Largos',25),('Cortos con brillo',43),('Cortos',30),('Bandage',22)]:
    lines.append(f'| {cat} | {totals[cat]} | {target} | {target-totals[cat]} |')
lines+=['','La diferencia neta no equivale al número de fotos o unidades de stock faltantes. La lista guardada de Cortos tiene 33 fichas, de las cuales 19 están asociadas y 14 siguen sin foto asociada; además hay ocho modelos web en Cortos procedentes de otras referencias. La lista de Brillo tiene 43 fichas: 39 asociadas, cuatro sin foto asociada, cinco asociadas hoy en Cortos y dos modelos Brillo procedentes de Gala.','',
    '## Cuatro referencias de Brillo sin foto asociada','',
    '| Nombre de catálogo | Precio |','|---|---:|']
for row in brillo['matriz']:
    if not row['id']:lines.append(f"| {row['nombre_catalogo']} | S/ {row['precio_catalogo']:.2f} |")
lines+=['','## Referencias históricas de Cortos sin foto asociada','',
    'Confirmar vigencia, nombre y foto; no convertir estas filas en altas nuevas por aritmética.','',
    '| Fila de la lista de 33 | Nombre visible | Precio |','|---|---|---:|']
for row in cortos['filas']:
    if not row['ids_candidatos']:lines.append(f"| {row['fila_oficial']} | {row['nombre_oficial']} | S/ {row['precio_oficial']:.2f} |")
lines+=['','Las filas 6 y 10 de los blancos con perlas tienen una miniatura histórica similar y precios distintos; falta confirmar si son variantes o una ficha duplicada.','',
    '## Colección de Brillo frente a las correcciones visuales','',
    '| Código web | Nombre | Precio | WhatsApp guardado | Web actual |','|---|---|---:|---|---|']
conflicts=[54,118,172,121,122]
for ident in conflicts:
    p=by_id[ident]
    lines.append(f"| XL-{ident:03d} | {p['name']} | S/ {p['price']:.2f} | Cortos con brillo | {p['category']} |")
lines+=['','XL-054 tiene una indicación específica del usuario de permanecer en Cortos. Los demás se mantienen conforme a la revisión visual previa hasta que se confirme la clasificación comercial definitiva.','',
    '## Nombres que necesitan distinguir diseños','',
    '- XL-069 y XL-131: dos vestidos azules distintos con el mismo nombre y precio. La miniatura oficial de «Vestido drapeado azul asimétrico» corresponde a XL-131. Falta la referencia exacta de XL-069.',
    '- XL-127 y XL-140: vestido vino corto con caída lateral y vestido vino de falda larga, ambos con el mismo nombre y S/ 549. Conservar ambos modelos y el precio; confirmar el nombre exacto de cada uno.',
    '- XL-107 y XL-175: dos modelos plomo diferentes con el mismo nombre base y S/ 529. Se conservan sus sufijos y registros separados.','',
    '## Revisión de la fuente Largos','',
    'La lista guardada tiene 22 entradas, incluidas una blusa y un Bandage largo. Por ello no es una lista cerrada de los 25 Largos indicados. Se necesita confirmar el conjunto definitivo; que la web muestre 25 no demuestra por sí solo que sean exactamente los mismos 25 modelos.','']

source=read(ROOT/'review/catalogo-whatsapp-2026-10-12/largos-completo.json')
known={2:5,3:6,6:20,8:22,9:23,10:24,11:113}
largos=[]
for n,value in enumerate(source,1):
    parts=value.split('PEN',1)
    price=float(re.search(r'[\d]+\.[\d]{2}',parts[1])[0])
    row={'fila_fuente':n,'texto_fuente':value,'nombre_visible':parts[0],'precio':price,'id_asociado':known.get(n),'estado':'Nombre, precio y referencia previamente asociados' if n in known else 'Referencia pendiente de asociación o vigencia'}
    if n==19:row['estado']='Blusa; fuera de vestidos'
    if n==13:row['estado']='Bandage largo; no asociar al XL-073 rojo midi por color'
    if n in known:row['categoria_web']=by_id[known[n]]['category']
    largos.append(row)
(AUDIT/'largos-fuente').mkdir(exist_ok=True)
(AUDIT/'largos-fuente/matriz.json').write_text(json.dumps({'fecha':'2026-10-15','fuente':'catalogo-whatsapp-2026-10-12/largos-completo.json','total_filas':22,'advertencia':'Nombres de una lista histórica; no prueban faltantes actuales ni autorizan mover modelos solo para igualar totales.','filas':largos},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines+=['| Fila | Nombre visible en la fuente | Precio | Asociación |','|---|---|---:|---|']
for row in largos:
    assoc=(f"XL-{row['id_asociado']:03d} · {row['categoria_web']}" if row['id_asociado'] else row['estado'])
    lines.append(f"| {row['fila_fuente']} | {row['nombre_visible']} | S/ {row['precio']:.2f} | {assoc} |")
lines+=['','## Evidencia y verificación','',
    '- [Mensaje preparado para el encargado](MENSAJE-PARA-ENCARGADO.txt).',
    '- [Comparación visual por nombre](COMPARACION-PARA-ENCARGADO.html).',
    '- [Clasificación y altas aplicadas](CONCILIACION.md).',
    '- [Verificación de fichas y fotos generadas](verificacion-web.json).',
    '- Las capturas actuales recuperadas están en `whatsapp-actual/`. Las fotos muestran los vestidos originales; solo se recortó la interfaz de WhatsApp.',
    '- WhatsApp mostró «Esperando red» y solo cargó las primeras tres referencias de cada colección durante esta revisión. Se recargó la página y se recuperaron las cuatro altas verificadas. El resto requiere una sesión que termine de cargar o las fotos originales del encargado.','']
(AUDIT/'PENDIENTES-CATALOGO.md').write_text('\n'.join(lines),encoding='utf-8')

def photo(p):
    path=ROOT/p['image']
    mime='image/png' if path.suffix.lower()=='.png' else 'image/jpeg'
    return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()

sections=[]
for title,ids,description in [
    ('Colección de Brillo frente a la revisión visual',conflicts,'En la lista guardada aparecen en Brillo; en la web están en Cortos. XL-054 tiene confirmación específica del usuario.'),
    ('Dos diseños azules con el mismo nombre',[69,131],'La miniatura oficial de Vestido drapeado azul asimétrico corresponde a XL-131. Confirmar el nombre exacto de XL-069.'),
    ('Dos diseños vino con el mismo nombre',[127,140],'Son prendas diferentes. El precio de S/549 se conserva en ambos; confirmar los nombres y colecciones.'),
    ('Dos diseños plomo con un nombre base genérico',[107,175],'Las fotos muestran modelos distintos; se mantienen sus sufijos y registros.'),
    ('Cuatro prendas recuperadas de WhatsApp',[179,180,181,182],'Nombre, precio y fotos de la misma ficha verificados. Frente primero; espalda segunda cuando existe.')]:
    cards=[]
    for ident in ids:
        p=by_id[ident]
        cards.append(f'<article><img src="{photo(p)}" alt="{html.escape(p["name"])}"><p class="code">XL-{ident:03d} · {html.escape(p["category"])}</p><h3>{html.escape(p["name"])}</h3><p>S/ {p["price"]:.2f}</p></article>')
    sections.append(f'<section><h2>{html.escape(title)}</h2><p>{html.escape(description)}</p><div class="grid">'+''.join(cards)+'</div></section>')
page='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Revisión de colecciones · Xiliana Boutique</title><style>body{margin:0;background:#faf9f6;color:#25231f;font:16px/1.5 Arial,sans-serif}main{max-width:1240px;margin:auto;padding:32px 20px}h1{font-size:32px;line-height:1.2}h2{font-size:23px}section{margin:48px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:20px}article{background:white;border:1px solid #dedad2;padding:12px}img{width:100%;height:310px;object-fit:contain;background:#fff}h3{font-size:17px;line-height:1.4;margin:8px 0}.code{font-size:13px;color:#6c5b3a;margin:12px 0 0}.notice{padding:16px;border:1px solid #dedad2;background:white}a{color:#66532b}@media(max-width:540px){.grid{grid-template-columns:1fr 1fr;gap:10px}img{height:240px}article{padding:8px}h3{font-size:15px}}@media print{section{break-inside:avoid}article{break-inside:avoid}main{padding:0}body{background:white}}</style><main><h1>Revisión de nombres y colecciones</h1><p>15 de octubre de 2026 · Xiliana Boutique</p><p class="notice">Web actual: 25 Largos · 36 Cortos con brillo · 27 Cortos · 22 Bandage · 32 Gala · 1 Liquidación. Las ofertas se muestran también en su página. La conciliación de los conjuntos definitivos sigue pendiente de confirmar con el encargado.</p>'''+''.join(sections)+'</main></html>'
(AUDIT/'COMPARACION-PARA-ENCARGADO.html').write_text(page,encoding='utf-8')

summary=read(AUDIT/'resultado-aplicado.json')
summary.update(mensaje_preparado='MENSAJE-PARA-ENCARGADO.txt',comparacion_visual='COMPARACION-PARA-ENCARGADO.html',referencias_pendientes='PENDIENTES-CATALOGO.md',cantidades_coincidentes=['Largos','Bandage'],identidades_por_coleccion_cerradas=False,limitacion_whatsapp='Esperando red; solo tres referencias iniciales cargadas por colección. Recargas y recuperación documentadas.')
(AUDIT/'resultado-aplicado.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with Image.open(AUDIT/'whatsapp-actual/largos25-web.png') as im:
    im.crop((350,0,1490,1075)).save(AUDIT/'largos25-verificado.png')
print(json.dumps({'prendas':len(products),'fotos':sum(len(p['photos']) for p in products),'totales':dict(totals),'entregables':['MENSAJE-PARA-ENCARGADO.txt','PENDIENTES-CATALOGO.md','COMPARACION-PARA-ENCARGADO.html']},ensure_ascii=False))
