from pathlib import Path
import json, re, unicodedata

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
raw = (root/'products.js').read_text(encoding='utf-8-sig')
products = json.loads(re.search(r'export const products = (\[.*?\]);', raw, re.S).group(1))
sources = {}
for cat, filename in [('Gala','gala-completo.json'),('Largos','largos-completo.json'),('Cortos','cortos-completo.json'),('Cortos con brillo','brillo-completo.json')]:
    sources[cat] = json.loads((root/'review/catalogo-whatsapp-2026-10-12'/filename).read_text(encoding='utf-8-sig'))

def norm(value):
    value = ''.join(c for c in unicodedata.normalize('NFD',value.casefold()) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+',' ',value).strip()

decisions = {
 62: ('Gala','Nombre y miniatura negra con lazo rosa en Gala. El brillo está localizado; la colección comercial distingue esta prenda formal del grupo de Largos estampados/lisos.','alta'),
 68: ('Cortos','Fila 17 de Cortos: mismo nombre y S/299. El bajo es al tobillo en la foto, pero la clasificación comercial oficial guardada es Cortos.','alta para colección comercial'),
 81: ('Cortos','Fila 28 de Cortos: mismo nombre que contiene largo y S/319. Foto marrón con filas de piedras coincide. El nombre largo por sí solo no invalida su ubicación comercial.','alta para colección comercial'),
 90: ('Gala','Nombre explícito de gala y S/589 en la lista Gala. Ambas fotos muestran vestido formal guinda hasta suelo.','alta'),
 101: ('Gala','Nombre explícito de gala, S/349 y miniatura roja con bandas plateadas en Gala. La abertura no lo convierte en corto.','alta'),
 107: ('Gala','Referencia histórica GALA-CAPTURA-R112 asocia ambas fotos R112/R116 a Gala y S/529. El nombre genérico de lentejuelas también corresponde a otra ficha plomo XL-175, por lo que identidad textual requiere conservar el sufijo modelo plomo.','media-alta; nombre genérico ambiguo'),
}
manual_rows = {62:('Gala',19),68:('Cortos',17),81:('Cortos',28),90:('Gala',25),101:('Gala',39),107:('Gala',47)}
matrix=[]
for p in products:
    if p['category'] not in ('Largos','Gala'): continue
    matches=[]
    for category, lines in sources.items():
        for n,line in enumerate(lines,1):
            name=norm(p['name'].split(' · ')[0])
            if norm(line).startswith(name):
                matches.append({'coleccion':category,'fila':n,'texto':line,'metodo':'prefijo exacto normalizado; no basta para certificar identidad'})
    entry={k:p[k] for k in ('id','name','category','price')}
    entry['photos']=[{'src':f['src'],'view':f.get('view')} for f in p['photos']]
    entry['coincidencias_nombre']=matches
    if p['id'] in decisions:
        dest,motivo,conf=decisions[p['id']]
        cat,n=manual_rows[p['id']]
        entry.update(propuesta=dest,motivo=motivo,confianza=conf,fuente_comercial={'archivo':f'review/catalogo-whatsapp-2026-10-12/{"gala" if cat=="Gala" else "cortos"}-completo.json','fila':n,'texto':sources[cat][n-1]})
    else: entry['propuesta']=p['category']
    matrix.append(entry)

result={'fecha':'2026-10-15','metodo':'Fotos + nombres + listas comerciales guardadas; se respeta la clasificación del catálogo cuando el nombre y la longitud son ambiguos. No se relabelan maxis por una abertura.','prendas_revisadas':len(matrix),'cambios':[p for p in matrix if p['id'] in decisions], 'matriz':matrix,'largos_tras_cambios':[p['id'] for p in matrix if p['propuesta']=='Largos'],'otros_candidatos':[{'id':i,'decision':'Gala','motivo':m} for i,m in [(87,'Falda de lentejuelas hasta tobillo, nombre Largo Color Pic Blue; no mini.'),(112,'Rayas doradas blancas, frente y espalda hasta tobillo; no mini.'),(136,'Falda de lentejuelas verticales hasta tobillo; no mini.'),(175,'Flecos plomos desde cintura hasta tobillo; no mini.')]],'no_se_modifico_catalogo':True}
(out/'matriz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'cambios':{p['id']:p['propuesta'] for p in result['cambios']},'largos':result['largos_tras_cambios'],'total_largos':len(result['largos_tras_cambios'])},ensure_ascii=False))
