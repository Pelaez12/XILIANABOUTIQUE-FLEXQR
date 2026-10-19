import json, re, html
from pathlib import Path
from collections import Counter
from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
source=json.loads((ROOT/'review/catalogo-whatsapp-2026-10-12/brillo-completo.json').read_text(encoding='utf-8'))
text=(ROOT/'products.js').read_text(encoding='utf-8')
products=json.loads(re.search(r'export const products = (\[.*?\]);',text,re.S).group(1))
byid={p['id']:p for p in products}
mapping=[179,169,170,17,166,35,155,172,16,38,39,40,151,156,168,149,157,152,171,154,49,153,51,52,150,54,134,None,57,None,118,120,None,119,167,135,78,123,None,133,132,121,122]
names='''Vestido corto azul
Vestido corto color verde (S M)
Vestido corto de lentejuelas verde
Vestido corto dorado de una manga
Vestido de lentejuelas corto rojo
Vestido corto de una manga color marrón
Vestido corto negro con plateado
Vestido corto negro con mangas plateadas
Vestido (L) transparente con diamantes de imitación
Vestido corto de lentejuelas rosado de una manga
Vestido verde de lentejuelas y mostacillas
Vestido corto 3/4 de lentejuelas con terciopelo en el busto
Vestido de lentejuelas palo rosa de transparencias
VESTIDO CORTO: Negro con tirantes y pedrería
Vestido corto champagne de lentejuelas con cuello alto
Vestido corto blanco de lentejuelas tornasoladas
Vestido corto de tirantes
Vestido corto rojo de pedreria
Vestido Corto Verde de Pedrería Plateadas y de Perlas
Vestido largo de lentejuelas con diamantes
Vestido corto rojo de lentejuelas rojas
Vestido corto blanco con dorado de lentejuelas
Vestido corto de lentejuelas celeste y azul
Vestido corto asimétrico de lentejuelas azul
Vestido corto azul de lentejuelas y flecos
Vestido corto de diamantes de imitación plateadas
Vestido de pedrería negro con plumas
Vestido corto azul pedrería y strass
Vestido corto Blanco de lentejuelas
Vestido dorado corto asimétrico de flecos
Vestido negro asimétrico con lentejuelas
Vestido corto dorado con negro
Vestido corto de lentejuelas verde
Vestido corto escotado
vestido corto dorado con negro de mangas negras
Vestido corto guinda de perlas
Vestido corto negro de brillos plateados
Vestido corto negro con plateado
Vestido elegante estraple negro con plateado
Vestido de lentejuelas vintage color azul
Vestido corto de lentejuelas con detalles de perlas
Vestido corto negro de tiras
Vestido corto negro'''.splitlines()
assert len(names)==43
assert len(mapping)==len(source)==43
pending_notes={
1:'Recuperado el 15/10/2026 en la ficha actual, código 182 y S/329. Dos capturas de frente/espalda incorporadas como XL-179, distintas de las 139 prendas previas. Evidencia en ../whatsapp-actual/brillo-azul329-ficha-completa.png.',
28:'No hay foto original asociada con certeza. No sustituir por XL-052 azul asimétrico ni por XL-150 azul con flecos por color/precio.',
30:'El catálogo contiene por separado el vestido dorado corto asimétrico de flecos y el Bandage dorado de flecos XL-129. XL-129 tiene confirmación explícita del usuario como Bandage, código 2070, R143. Se necesita miniatura/foto de esta referencia para confirmar si son dos prendas o un alias comercial.',
33:'Nombre igual al XL-170, pero S329 frente a S369. No se puede crear una segunda prenda sin comparar fotos; podría ser referencia distinta o duplicación/alias. XL-039 también verde S329 tiene nombre diferente y descripción mostacillas.',
39:'Nombre y precio no se asocian con certeza a una foto publicada. No fusionar por parecido con XL-117 negro brillante S389 ni otros negros plateados.'
}
rows=[]
for n,(raw,pid) in enumerate(zip(source,mapping),1):
    prices=[float(x) for x in re.findall(r'PEN\s*([0-9]+(?:\.[0-9]+)?)',raw)]
    p=byid.get(pid)
    row={'fila_catalogo':n,'nombre_catalogo':names[n-1],'texto_catalogo':raw,'precio_catalogo':prices[0] if prices else None,'id':pid,'nombre_publicado':p['name'] if p else None,'categoria_actual':p['category'] if p else None,'precio_publicado':p['price'] if p else None,'foto_actual':p['image'] if p else None,'estado':'Asociado a prenda publicada' if p else 'Sin asociación segura','observacion':pending_notes.get(n,'')}
    if pid==54: row['observacion']='El usuario indicó expresamente Cortos para esta foto. La lista histórica Brillo no prevalece sobre esa instrucción.'
    if pid in (118,172,121,122): row['observacion']='Referencia del catálogo histórico Brillo ubicada hoy en Cortos por revisión visual. Debe conciliarse la clasificación comercial con el criterio reciente de brillo dominante; no traslado automático solo para cuadrar una cifra.'
    if pid==154: row['observacion']='Excepción comercial individual: usuario confirmó Cortos con brillo aunque su nombre diga largo.'
    rows.append(row)
assert len({x['id'] for x in rows if x['id']})==39
assert all(x['precio_catalogo']==x['precio_publicado'] for x in rows if x['id'])
matched={x['id'] for x in rows if x['id']}
extras=[{'id':p['id'],'nombre':p['name'],'precio':p['price'],'foto':p['image']} for p in products if p['category']=='Cortos con brillo' and p['id'] not in matched]
album=json.loads((ROOT/'review/clasificacion-2026-10-13/coincidencias.json').read_text(encoding='utf-8'))
album_rows=[x for x in album if x['categoria_indicada']=='Cortos con brillo']
album_ids=sorted({c['id'] for x in album_rows for c in x['coincidencias']})
report={'fecha':'2026-10-15','solo_lectura_catalogo':True,'referencias_fuente':43,'referencias_asociadas':39,'referencias_sin_asociacion':4,'asociadas_por_categoria_actual':dict(Counter(x['categoria_actual'] for x in rows if x['id'])),'brillo_actual_no_en_lista43':extras,'album_usuario_oct13':{'fotos':len(album_rows),'modelos':len(album_ids),'ids':album_ids},'advertencia':'Cuatro referencias sin asociación no equivalen a cuatro prendas nuevas confirmadas: se necesitan imágenes para descartar alias/duplicados y distinguir cambios de nombre/precio. La lista de 43 referencias incluye cinco modelos que ahora están en Cortos. No existe evidencia para trasladar modelos Gala a Brillo solo para alcanzar una cifra.','matriz':rows}
(OUT/'matriz43.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Conciliación de las 43 referencias de Cortos con brillo','', 'Se cruzaron los nombres y precios de brillo-completo.json contra las 140 prendas publicadas. La matriz incluye XL-179, recuperado del catálogo actual con dos fotos de frente/espalda. Se mantienen las seis correcciones previas.','', '**Resultado: 39 referencias asociadas a 39 prendas distintas: 34 están en Brillo y 5 en Cortos. Cuatro referencias todavía no tienen una foto original asociada con certeza.** Las 36 prendas Brillo actuales incluyen además XL-117 y XL-127, procedentes de referencias de la colección Gala histórica.','', 'La cuenta se explica así: 43 referencias − 4 sin asociación − 5 trasladadas a Cortos + 2 prendas reclasificadas desde Gala = 36 publicadas en Brillo.','', 'Las cuatro referencias sin asociación no demuestran cuatro prendas nuevas: pueden existir alias o duplicados. La cifra 43 de la colección histórica y el nuevo criterio visual no son intercambiables. XL-054 debe seguir Cortos por instrucción explícita del usuario.','', '## Referencias sin asociación segura','', '| Fila | Nombre/precio de fuente | Motivo |','| --- | --- | --- |']
for x in rows:
    if not x['id']:lines.append(f"| {x['fila_catalogo']} | {x['nombre_catalogo']} · S/ {x['precio_catalogo']:.2f} | {x['observacion']} |")
lines+=['','## Referencias presentes en Cortos','', '| ID | Nombre | Precio | Observación |','| --- | --- | ---: | --- |']
for x in rows:
    if x['categoria_actual']=='Cortos':lines.append(f"| XL-{x['id']:03d} | {x['nombre_publicado']} | {x['precio_publicado']:.2f} | {x['observacion']} |")
lines+=['','## Álbum enviado explícitamente como Brillo el 13 de octubre','',f"{len(album_rows)} fotos, {len(album_ids)} modelos únicos: "+', '.join(f'XL-{i:03d}' for i in album_ids)+'.','', 'Ese álbum sí incluye XL-122 y XL-172. XL-122 parece liso en la foto actual, por lo que conviene revisar identidad/material con el dueño si se aplica el criterio reciente. El álbum no añade 28 modelos nuevos: son 28 fotos de 19 modelos existentes.','', '## Matriz completa','', '| Fila | Referencia de catálogo | ID | Categoría actual | Precio |','| --- | --- | --- | --- | ---: |']
for x in rows:lines.append(f"| {x['fila_catalogo']} | {x['nombre_catalogo']} | {('XL-'+str(x['id']).zfill(3)) if x['id'] else 'Pendiente foto/identidad'} | {x['categoria_actual'] or '—'} | {x['precio_catalogo']:.2f} |")
(OUT/'REPORTE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
cards=[]
for x in rows:
    pic='<div class="empty">Foto original sin asociar</div>'
    if x['foto_actual']:
        path=ROOT/x['foto_actual'].removeprefix('./')
        pic=f'<img src="{path.as_uri()}" alt="{html.escape(x["nombre_publicado"])}">'
    cards.append(f'<article>{pic}<b>Fila {x["fila_catalogo"]} · '+(f'XL-{x["id"]:03d}' if x['id'] else 'Sin asociación')+'</b><p>'+html.escape(x['nombre_catalogo'])+' · S/ '+format(x['precio_catalogo'],'.2f')+'</p><p><strong>'+html.escape(x['categoria_actual'] or 'Pendiente foto/identidad')+'</strong></p><small>'+html.escape(x['observacion'])+'</small></article>')
(OUT/'MATRIZ-VISUAL.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>Conciliación43 Brillo</title><style>body{font:15px system-ui;margin:30px;background:#faf9f7}main{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}article{background:white;padding:15px;border:1px solid #ddd}img,.empty{width:100%;height:300px;object-fit:contain;background:#f2f2f2}.empty{display:grid;place-items:center;color:#777}b{display:block;margin-top:12px}small{color:#555}p{margin:8px 0}@media(max-width:800px){main{grid-template-columns:repeat(2,1fr)}}</style><h1>43 referencias de Cortos con brillo</h1><p>39 asociadas: 34 en Brillo, 5 en Cortos. 4 pendientes de asociar. Nombres y precios cotejados; no se editó el catálogo.</p><main>'+''.join(cards)+'</main></html>',encoding='utf-8')
im=Image.open(ROOT/'review/catalogo-whatsapp-2026-10-12/brillo-superior.png')
im.crop((1620,60,2298,162)).save(OUT/'fuente-azul329.png')
print(json.dumps({k:v for k,v in report.items() if k!='matriz'},ensure_ascii=False,indent=2))
