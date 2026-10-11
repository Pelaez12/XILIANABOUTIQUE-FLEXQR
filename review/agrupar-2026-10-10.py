from pathlib import Path
import json,html
r=Path(__file__).resolve().parents[1];d=r/'review/importacion-2026-10-10'
items=json.loads((d/'inventario.json').read_text(encoding='utf-8'));by={x['n']:x for x in items}
duplicates={3:16,14:17,26:122}
pairs=[[1,2],[4,5],[6,7],[8,9],[11,12],[18,19],[22,23],[24,25],[27,28],[30,49],[32,33],[35,36],[38,37],[39,40],[41,42],[43,44],[47,48]]
singles=[10,13,15,16,17,20,21,29,31,34,45,46,50]
names=['Blanco asimétrico con cadenas','Azul con pedrería y flecos','Rosado corsé con pedrería','Rojo corto con cadenas','Blanco y dorado de lentejuelas','Verde corsé largo con abertura','Negro geométrico con escote','Negro corsé con cadenas','Negro corto con copas y pedrería','Largo multicolor geométrico','Negro largo de cuello alto','Largo nude con pedrería','Azul largo con encaje','Rojo largo de hombros descubiertos','Rojo largo de encaje','Blanco de una manga con brillo','Palo rosa largo con tirantes cruzados']
single_names=['Rojo corto de hombros descubiertos','Negro corto con falda animal print','Crema corto con detalles dorados','Verde corto con transparencias','Verde corto de manga larga','Verde corto corsé con cadenas','Negro corto con mangas plateadas','Rosado largo floral','Negro largo satinado con cinturón','Plomo largo de tirantes con brillo','Blanco largo con escote de encaje','Nude largo con volantes','Verde largo asimétrico con manga capa']
groups=[]
for k,(indices,name) in enumerate(list(zip(pairs,names))+list(zip([[n] for n in singles],single_names)),1):
 groups.append({'grupo':f'NV-{k:03}','nombre_descriptivo':name,'fotos':[{'n':n,'path':by[n]['path'],'vista':('Frente' if j==0 else 'Frente · otra pose' if n==25 else 'Lateral' if n==23 else 'Espalda')} for j,n in enumerate(indices)],'estado':'Modelo nuevo: nombre de catálogo y precio por asociar'})
audit={'total_fotos':50,'duplicados_visuales':[{'n':n,'producto':f'XL-{ident:03}','motivo':'Misma fotografía, archivo recomprimido; no añadida'} for n,ident in duplicates.items()],'modelos_nuevos':groups,'parejas':17,'una_vista':13}
(d/'verificacion.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
out=['<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fotos nuevas · Xiliana</title><style>body{font:16px system-ui;background:#faf8f4;color:#222;margin:0;padding:24px}main{max-width:1100px;margin:auto}h1{font-size:32px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}article{background:white;padding:16px;border:1px solid #ddd}figure{margin:0;min-width:0}img{width:100%;height:300px;object-fit:contain}.photos{display:flex;gap:8px}.photos figure{flex:1}small{color:#666}h2{font-size:18px}figcaption{font-size:12px}</style><main><h1>Fotos nuevas organizadas</h1><p>50 fotos revisadas · 3 duplicados omitidos · 17 parejas · 13 modelos con una vista.</p><p>Los modelos siguientes no coinciden con las 109 prendas publicadas. Los nombres son descriptivos para facilitar su identificación; falta asociar nombre de catálogo y precio antes de incorporarlos a la tienda.</p><div class="grid">']
for g in groups:
 out.append(f'<article><small>{g["grupo"]}</small><h2>{html.escape(g["nombre_descriptivo"])}</h2><div class="photos">')
 for f in g['fotos']:out.append(f'<figure><a href="N{f["n"]:03}.jpeg"><img loading="lazy" src="N{f["n"]:03}.jpeg"></a><figcaption>N{f["n"]:03} · {f["vista"]}</figcaption></figure>')
 out.append('</div><p><small>Precio por asociar al catálogo.</small></p></article>')
out.append('</div><h2>Duplicados que ya están en la web</h2><p>N003 → XL-016 · N014 → XL-017 · N026 → XL-122. No se repiten en sus galerías.</p></main></html>')
(d/'REVISION-FOTOS.html').write_text(''.join(out),encoding='utf-8')
assert sorted([n for pair in pairs for n in pair]+singles+list(duplicates))==list(range(1,51))
print('50 fotos verificadas: 3 duplicadas; 30 modelos nuevos agrupados, frente primero.')
