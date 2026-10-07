from pathlib import Path
import json,csv,html,os,unicodedata,re
root=Path(__file__).resolve().parents[1]
out=root/'review'
inventory=json.loads((out/'real-inventory.json').read_text(encoding='utf-8-sig'))
classification=json.loads((out/'real-classification.json').read_text(encoding='utf-8-sig'))
catalog=json.loads((out/'catalogo-verificado-2026-10-06.json').read_text(encoding='utf-8-sig'))
def norm(s):
 return re.sub('[^a-z0-9]+',' ',unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode()).strip()
new=[
 (5,'Vestido de gala en degradado',[27,28,29]),
 (5,'Vestido de gasa azul',[15]),
 (5,'Vestido largo morado claro',[35,38]),
 (5,'Vestido largo corte sirena negro con lazo y mangas',[43,45,46]),
 (3,'Vestido corto cuello diagonal, plisado y liso',[165]),
 (3,'Vestido corto celeste con corte sirena',[49,50,156]),
 (3,'Vestido Corto Bellmet asimétrica color verde',[93,96]),
 (3,'Vestido color verde terciopelo semi drapeado con manga y escote',[94,95,166]),
 (3,'Vestido corto blanco drapeado con mangas largas',[132,133]),
 (3,'Vestido de cuello cuadrado de manga larga color rosado',[65,66,164]),
 (3,'Vestido drapeado azul asimétrico',[142,153]),
 (4,'Bandage dress nude con blanco',[154]),
 (4,'Vestido Bandage Dorado',[126,127]),
 (4,'Vestido Bandage negro con aplicaciones plateadas',[150]),
 (4,'Vestido Bandage rojo',[107]),
 (4,'Vestido Bandage negro con rosado y perlas rosadas',[60]),
 (4,'Vestido Bandage negro con lazo blanco',[26,145]),
 (4,'Vestido Bandage Amarillo – mini',[149]),
 (4,'Vestido Bandage Amarillo – midi',[55,59,148]),
]
obs=catalog['observaciones_video']
matches=[]
for video,name,indices in new:
 candidates=[x for x in obs if x['video']==video and norm(x['nombre'])==norm(name)]
 assert len(candidates)==1,(name,candidates)
 x=candidates[0]
 matches.append(dict(nombre=x['nombre'],precio=x['precio_final_pen'],categoria={1:'Largos',2:'Cortos con brillo',3:'Cortos sin brillo',4:'Bandage',5:'Gala'}[video],video=video,indices=indices,estado='Coincidencia visual confirmada',origen='Nueva asociación mediante grabación'))
for x in classification['matched']:
 matches.append(dict(nombre=x['name'],precio=x['price'],categoria='Cortos sin brillo' if x['productId']==10 else x['category'],video=None,indices=x['sourceIndices'],estado='Asociación real previamente revisada',origen='Catálogo y revisión previa; no se atribuye evidencia nueva al video'))
confirmations=json.loads((out/'confirmaciones-usuario.json').read_text(encoding='utf-8-sig')) if (out/'confirmaciones-usuario.json').exists() else []
for x in confirmations:
 matches=[m for m in matches if not set(m['indices']).intersection(x['indices'])]
 matches.append(dict(nombre=x['nombre'],precio=x['precio'],categoria=x['categoria'],video=None,indices=x['indices'],estado='Nombre y precio confirmados por el usuario',origen='Confirmación del usuario · '+x['codigo']))
offers=json.loads((out/'liquidacion-confirmada.json').read_text(encoding='utf-8-sig'))
for m in matches:
 offer=next((o for o in offers if o['indice'] in m['indices']),None)
 if offer:
  m.update(etiquetas=['Liquidación'],precio_regular=offer['precio_regular'],descuento_porcentaje=offer['descuento_porcentaje'],precio=offer['precio_oferta'])
used={i for m in matches for i in m['indices']}
assert sum(len(m['indices']) for m in matches)==len(used),'Foto asignada dos veces'
pending=[dict(codigo=x['code'],nombre_provisional=x['name'],categoria=x['category'],indices=[i for i in x['sourceIndices'] if i not in used],estado='Sin asociación exacta confirmada') for x in classification['pending']]
pending=[x for x in pending if x['indices']]
assert used|{i for x in pending for i in x['indices']}==set(range(1,167))
result=dict(criterio='Se compara diseño, escote, mangas, corte y aplicaciones. Una coincidencia de color no basta. Los archivos originales se conservan. Las miniaturas del video no permiten certificar detalles invisibles.',coincidencias=matches,pendientes=pending,total_archivos=166,fotos_asociadas=len(used),asociaciones_nuevas=len(new))
(out/'COMPARACION-FOTOS-VIDEOS-2026-10-06.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'COMPARACION-FOTOS-VIDEOS-2026-10-06.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Nombre','Precio PEN confirmado','Video','Fotos originales','Estado','Origen'])
 for m in matches:w.writerow([m['nombre'],m['precio'],m['video'] or '',', '.join(f'R{i:03}' for i in m['indices']),m['estado'],m['origen']])
 for p in pending:w.writerow([p['nombre_provisional'],'','',', '.join(f'R{i:03}' for i in p['indices']),p['estado'],p['codigo']])
def imgs(indices):
 s=''
 for i in indices:
  p=root/inventory[i-1]['path'];assert p.exists(),p
  rel=os.path.relpath(p,out).replace('\\','/')
  s+=f'<a href="{html.escape(rel)}" target="_blank"><img loading="lazy" src="{html.escape(rel)}" alt="Foto R{i:03}"><small>R{i:03}</small></a>'
 return s
page='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Xiliana · Comparación de fotos</title><style>body{font:16px system-ui;margin:32px;color:#222;background:#faf9f6}h1{font-size:30px}section{background:white;padding:24px;margin:20px 0;border:1px solid #ddd} .photos{display:flex;gap:12px;flex-wrap:wrap}.photos a{display:flex;flex-direction:column;color:#555}.photos img{width:180px;height:250px;object-fit:contain;background:#eee}small{margin:6px 0}p{max-width:900px;line-height:1.6}</style><body><h1>Comparación del catálogo con las fotos originales</h1>'''
page+=f'<p>166 archivos revisados · {len(new)} asociaciones nuevas · {len(matches)} modelos asociados en total · {len(used)} fotos asociadas. Las fotos restantes quedan pendientes de identificar; algunas son prendas fuera de las cinco categorías solicitadas.</p><p>{html.escape(result["criterio"])}</p><p>Videos: 1 largos (235800), 2 cortos con brillo (000256), 3 cortos (000349), 4 bandage (000657), 5 gala (235636). Las asociaciones previas se muestran por separado en su etiqueta.</p><p>Los confirmados ya están incorporados a la web. Este reporte muestra solo lo que falta asignar.</p><a href="http://127.0.0.1:8090/">Ver los vestidos confirmados en la web ↗</a>'
page+='<h2 id="sin-identificar">Sin identificar: productos del catálogo sin foto confirmada</h2>'
gala_missing=json.loads((out/'gala-sin-foto-confirmada.json').read_text(encoding='utf-8-sig'))
for item in gala_missing:page+=f'<section><h3>{html.escape(item["nombre"])}</h3><p>Gala · S/ {item["precio"]:.2f} · Falta asociar una foto original.</p></section>'
page+='<h2>Sin identificar: fotos pendientes de nombre y precio</h2><p>No se asigna un precio hasta confirmar el modelo correspondiente. Se mantiene la agrupación previa de vistas para revisión.</p>'
page+='<p><a href="AUDITORIA-FRENTE-ESPALDA-2026-10-07.html">Ver revisión de frente y espalda y las vistas que faltan ↗</a></p>'
if not pending:page+='<p>Ya no quedan fotos originales pendientes de identificar. Los modelos sin foto confirmada siguen listados arriba.</p>'
for p in pending:page+=f'<section><h3>{p["codigo"]} · {html.escape(p["nombre_provisional"])}</h3><p>{html.escape(p["categoria"])}</p><div class="photos">{imgs(p["indices"])}</div></section>'
suggestions={'Vestido vino strapless de tirantes con copas de pedrería':[64,102,103],'Vestido sirena palo rosa de lentejuelas':[17,21],'Vestido largo azul acero':[68,73],'Vestido corto blanco con capa':[113,114,160]}
confirmed={norm(m['nombre']) for m in matches}
choices=[]
for x in obs:
 if norm(x['nombre']) in confirmed or any(t in norm(x['nombre']) for t in ['bralette','falda','blusa','conjunto']):continue
 choices.append(dict(id=str(x['video'])+'-'+norm(x['nombre']),nombre=x['nombre'],precio=x['precio_final_pen'],suggested=suggestions.get(x['nombre'],[])))
for x in gala_missing:
 if not any(norm(c['nombre'])==norm(x['nombre']) for c in choices):choices.append(dict(id='gala-'+norm(x['nombre']),nombre=x['nombre'],precio=x['precio'],suggested=[]))
choices.sort(key=lambda x:not bool(x['suggested']))
payload={'products':choices,'photos':[dict(index=i,src=os.path.relpath(root/inventory[i-1]['path'],out).replace('\\','/')) for i in sorted(set(range(1,167))-used)]}
page+='<script type="application/json" id="selection-data">'+json.dumps(payload,ensure_ascii=False).replace('</','<\\/')+'</script><script src="seleccion-fotos.js"></script></body></html>'
(out/'COMPARACION-FOTOS-VIDEOS-2026-10-06.html').write_text(page,encoding='utf-8')
print(json.dumps({k:result[k] for k in ['total_archivos','fotos_asociadas','asociaciones_nuevas']}));print('Modelos asociados:',len(matches),'Fotos pendientes:',166-len(used))
