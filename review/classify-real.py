from pathlib import Path
from PIL import Image
import json, shutil, hashlib, re, csv, html

root = Path(__file__).resolve().parents[1]
records = json.loads((root/'review/real-inventory.json').read_text(encoding='utf-8'))
by_id = {r['index']: r for r in records}
# Comparación visual con las capturas originales; no se asignan precios por parecido.
matches = {5:[33],6:[30,34],10:[155],14:[152],16:[31],17:[44],20:[128,129],22:[47,48],23:[51,56],24:[122,123],35:[6],36:[11],38:[125],39:[5],40:[14],49:[52],51:[147],52:[69,70,71],54:[135],57:[2]}
groups = [
([1],'Corto negro de tirantes cruzados','Cortos'),([3],'Corto gris con pedrería y bajo en punta','Cortos con brillo'),
([4],'Corto verde lima halter con transparencias','Cortos con brillo'),([7],'Corto negro asimétrico con volantes','Cortos con brillo'),
([8],'Corto negro y blanco asimétrico con brillo','Cortos con brillo'),([9,158],'Midi azul halter con abertura','Bandage'),
([10,159],'Corto amarillo de tirantes','Cortos'),([12],'Corto negro strapless con encaje','Cortos'),
([13],'Corto champagne de manga larga con pedrería','Cortos con brillo'),([15],'Largo azul de mangas amplias','Gala'),
([16],'Largo azul oscuro de hombros descubiertos','Gala'),([21,17],'Largo burdeos con brillo','Gala'),
([18,19],'Midi fucsia de tirantes con aberturas','Bandage'),([20],'Corto dorado strapless asimétrico','Cortos con brillo'),
([22],'Midi gris de hombros descubiertos con flecos','Cortos con brillo'),([23,24],'Largo rosa metálico plisado','Gala'),
([25],'Midi gris vista posterior por identificar','Por identificar'),([26,145],'Corto negro y blanco strapless con lazo','Bandage'),
([27,28,29],'Largo estampado cebra con degradado verde','Largos'),([32],'Corto burdeos con pieza estampada asimétrica','Cortos'),
([35,38],'Largo morado de mangas amplias con pedrería','Gala'),([36,37,41],'Largo verde lima de tirantes con abertura','Gala'),
([39,40,42],'Largo azul de hombros descubiertos con abertura','Gala'),([43,45,46],'Largo negro con lazo burdeos asimétrico','Gala'),
([49,50,156],'Midi celeste con capa corta','Cortos'),([53,54],'Midi negro con capa y pedrería','Cortos con brillo'),
([55,59,148],'Midi amarillo de tirantes','Bandage'),([57,58],'Corto amarillo de tirantes con costuras','Bandage'),
([60],'Largo negro con aplicaciones rosadas','Gala'),([61,63],'Midi plateado y negro de tirantes','Cortos con brillo'),
([62],'Largo rojo con pedrería y abertura','Gala'),([64,102,103],'Largo rojo con escote y tirantes de pedrería','Gala'),
([65,66,164],'Largo rosa de manga larga con botones','Largos'),([67],'Corto burdeos de manga larga con pedrería','Cortos con brillo'),
([73,68],'Largo azul de hombros descubiertos y falda amplia','Gala'),([72,78],'Largo fucsia asimétrico con volantes','Gala'),
([74,75],'Largo azul petróleo de terciopelo','Gala'),([76,77],'Largo rojo de manga larga con aplicaciones','Gala'),
([83,79],'Largo verde de terciopelo con pedrería y abertura','Gala'),([80,81,97,99],'Corto gris con cola y hombros descubiertos','Gala'),
([82,87,98,104],'Largo negro con degradado dorado','Gala'),([84,85],'Largo burdeos de manga larga con abertura','Gala'),
([86,92],'Largo azul y verde con pedrería','Gala'),([88,89],'Midi negro con busto estructurado','Bandage'),
([90,91],'Largo negro y champagne asimétrico con pedrería','Gala'),([96,93],'Corto verde de terciopelo asimétrico','Cortos'),
([94,95,166],'Corto verde de terciopelo de manga larga','Cortos'),([100,101],'Largo champagne asimétrico con pedrería','Gala'),
([105],'Largo verde halter con pedrería y abertura','Gala'),([106],'Largo blanco de tirantes con aplicaciones','Gala'),
([107],'Midi rojo strapless con escote corazón','Bandage'),([108,151],'Conjunto de top negro y falda blanca y rosa','Fuera de vestidos'),
([109],'Largo crema asimétrico con abertura','Largos'),([111,110],'Largo blanco de hombros descubiertos con diseño geométrico','Gala'),
([112,116],'Largo gris asimétrico con falda bordada','Largos'),([113,114],'Midi blanco con mangas capa y abertura','Cortos'),
([115,121],'Capa negra de tul y encaje','Fuera de vestidos'),([117,120],'Largo crema con diseño dorado','Gala'),
([119,118],'Largo champagne de cuello alto con pedrería','Gala'),([124,130],'Largo champagne de tirantes con abertura','Gala'),
([126,127],'Midi dorado de tirantes','Bandage'),([131],'Corto negro vista posterior por identificar','Por identificar'),
([132,133],'Midi blanco de hombros descubiertos y manga larga','Bandage'),([134,136],'Largo negro con tul y puños plateados','Largos'),
([141,137],'Largo blanco y azul de tirantes con pedrería','Gala'),([138,139],'Largo champagne de tirantes con estampado','Gala'),
([140],'Largo burdeos de tirantes con aplicaciones','Largos'),([142,153],'Corto celeste de mangas amplias','Cortos'),
([143],'Vestido dorado con flecos y abertura','Gala'),([144],'Midi fucsia con aberturas','Bandage'),
([146],'Conjunto negro y blanco con top peplum','Fuera de vestidos'),([149],'Corto amarillo de tirantes por confirmar','Cortos'),
([150],'Midi negro con tirantes cruzados de pedrería','Bandage'),([154],'Corto blanco y beige con transparencias','Cortos'),
([157],'Midi negro de manga larga con abertura y pedrería','Bandage'),([160],'Corto blanco asimétrico','Cortos'),
([161],'Midi crema halter con falda plisada','Cortos'),([162],'Corto champagne de manga larga con lentejuelas','Cortos con brillo'),
([163],'Corto negro de tul de manga larga','Cortos'),([165],'Midi dorado asimétrico satinado','Cortos')]

used = [i for ids in matches.values() for i in ids] + [i for ids,_,_ in groups for i in ids]
assert sorted(used) == list(range(1,167)), 'Cada foto debe clasificarse exactamente una vez'
source = (root/'products.js').read_text(encoding='utf-8')
prices = {int(i):(name,cat,float(price)) for i,name,cat,price in re.findall(r"id: (\d+), name: '([^']+)', category: '([^']+)', price: ([\d.]+)",source)}
manifest = {'sourceCount':len(records),'uniqueSourceCount':len({r['sha256'] for r in records}),'matched':[], 'pending':[], 'withoutNewPhotos':[]}
mapping = {}
def copy_group(indices, directory):
    directory.mkdir(parents=True,exist_ok=True)
    photos=[]; hashes=set()
    for i in indices:
        r=by_id[i]
        if r['sha256'] in hashes: continue
        hashes.add(r['sha256'])
        target=directory/f'{len(photos)+1:02d}-R{i:03d}.jpeg'
        shutil.copy2(root/r['path'],target)
        assert hashlib.sha256(target.read_bytes()).hexdigest()==r['sha256']
        photos.append({'src':'./'+target.relative_to(root).as_posix(),'width':r['width'],'height':r['height'],'sourceIndex':i,'sha256':r['sha256']})
    return photos
for pid,indices in matches.items():
    photos=copy_group(indices,root/f'images/productos-reales/XL-{pid:03d}')
    mapping[str(pid)]=photos
    name,cat,price=prices[pid]
    manifest['matched'].append({'productId':pid,'name':name,'category':cat,'price':price,'sourceIndices':indices,'photos':photos})
for n,(indices,name,cat) in enumerate(groups,1):
    slug=re.sub('[^a-z0-9]+','-',name.lower()).strip('-')
    folder=root/f'pendientes-dueno/PD-{n:03d}-{slug}'
    photos=copy_group(indices,folder)
    manifest['pending'].append({'code':f'PD-{n:03d}','name':name,'category':cat,'price':None,'sourceIndices':indices,'photos':photos,'status':'No publicar: falta confirmar nombre, precio y disponibilidad' if cat not in ['Fuera de vestidos','Por identificar'] else 'Revisar identificación; excluido del catálogo de vestidos'})
for pid in range(1,59):
    if str(pid) not in mapping:
        name,cat,price=prices[pid]
        manifest['withoutNewPhotos'].append({'productId':pid,'name':name,'price':price,'reason':'Se conserva captura original real; no se encontró coincidencia segura entre las nuevas fotos'})
(root/'review/real-classification.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
js='const realPhotos = '+json.dumps(mapping,ensure_ascii=False,indent=2)+';\n\n'
source=re.sub(r'^const realPhotos = [\s\S]*?;\n\n(?=// Transcripci)', '',source)
source=source.replace("].map(product => ({ ...product, image: `./images/${product.id <= 17 ? 'dress' : 'catalog'}-${String(product.id).padStart(2, '0')}.jpg` }));", "].map(product => {\n  const originalImage = `./images/${product.id <= 17 ? 'dress' : 'catalog'}-${String(product.id).padStart(2, '0')}.jpg`;\n  const photos = realPhotos[product.id] || [];\n  return { ...product, originalImage, photos, image: photos[0]?.src || originalImage };\n});")
(root/'products.js').write_text(js+source,encoding='utf-8')
with (root/'pendientes-dueno/PRECIOS-POR-CONFIRMAR.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['Código','Nombre provisional','Categoría sugerida','Precio PEN (completar)','Disponible (completar)','Fotos','Observaciones'])
    for p in manifest['pending']:w.writerow([p['code'],p['name'],p['category'],'','',len(p['photos']),p['status']])
parts=['<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fotos pendientes · Xiliana Boutique</title><style>body{font:16px/1.5 Arial;margin:32px;color:#222}article{border-top:1px solid #ccc;padding:24px 0}.photos{display:flex;gap:12px;overflow-x:auto}img{height:300px;width:auto;max-width:90vw;object-fit:contain}h2{font-size:20px}small{color:#666}</style><h1>Fotos pendientes para el dueño</h1><p>Confirmar el nombre, precio y disponibilidad de cada prenda. Los nombres y categorías son provisionales. Estas fotos no se publican con precios inventados. Se conservan los archivos originales sin cambios.</p>']
for p in manifest['pending']:
    parts.append(f'<article><h2>{p["code"]} · {html.escape(p["name"])}</h2><p>{html.escape(p["category"])} · Precio: por confirmar</p><div class="photos">'+''.join(f'<a href="{html.escape(photo["src"].replace("./pendientes-dueno/",""),quote=True)}"><img loading="lazy" src="{html.escape(photo["src"].replace("./pendientes-dueno/",""),quote=True)}" alt="{html.escape(p["name"])}"></a>' for photo in p['photos'])+f'</div><small>{p["status"]}</small></article>')
(root/'pendientes-dueno/VER-FOTOS-PENDIENTES.html').write_text(''.join(parts)+'</html>',encoding='utf-8')
report=f'# Clasificación de fotografías reales\n\n{len(records)} archivos recibidos, {manifest["uniqueSourceCount"]} archivos únicos.\n\n- {len(matches)} productos identificados: fotos reales vinculadas y precios conservados.\n- {len(groups)} grupos para revisar con el dueño (incluye prendas fuera de vestidos y vistas sin frente identificable).\n- {len(manifest["withoutNewPhotos"])} productos conservan su captura original real, sin recreaciones de IA.\n\n## Productos identificados\n\n'
for p in manifest['matched']:report+=f'- XL-{p["productId"]:03d}: {p["name"]} — S/ {p["price"]:.2f} — {len(p["photos"])} foto(s).\n'
report+='\n## Pendientes de foto correspondiente\n\n'+''.join(f'- XL-{p["productId"]:03d}: {p["name"]}\n' for p in manifest['withoutNewPhotos'])
report+='\n## Observaciones\n\nXL-035 conserva el nombre del catálogo aunque la foto muestra un vestido sin mangas: el dueño debe corregir el nombre si corresponde. No se asociaron por color los modelos distintos. La carpeta imagenes-reales se conserva íntegra.\n'
(root/'review/CLASIFICACION-REAL.md').write_text(report,encoding='utf-8')
print(f'Clasificadas {len(records)} fotos: {len(matches)} productos asociados, {len(groups)} grupos pendientes, {len(manifest["withoutNewPhotos"])} productos con captura original.')
