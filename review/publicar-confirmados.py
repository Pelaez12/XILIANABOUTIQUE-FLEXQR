from pathlib import Path
import json,shutil,subprocess,hashlib
from PIL import Image
r=Path(__file__).resolve().parents[1]
report=json.loads((r/'review/COMPARACION-FOTOS-VIDEOS-2026-10-06.json').read_text(encoding='utf-8-sig'))
inv=json.loads((r/'review/real-inventory.json').read_text(encoding='utf-8-sig'))
confirmations=json.loads((r/'review/confirmaciones-usuario.json').read_text(encoding='utf-8-sig'))
replacements={int(i):source for item in confirmations for i,source in item.get('fotos_reemplazo',{}).items()}
gallery_review={x['id']:x for x in json.loads((r/'review/galerias-verificadas-2026-10-07.json').read_text(encoding='utf-8'))} if (r/'review/galerias-verificadas-2026-10-07.json').exists() else {}
old=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from 'node:fs';const {products}=await import('data:text/javascript;base64,'+fs.readFileSync('products.js').toString('base64'));console.log(JSON.stringify(products));"],cwd=r,text=True,encoding='utf-8'))
(r/'review/products-antes-confirmados.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
texts={
'Gala':['Haz de tu entrada un momento inolvidable. Un look para celebrar, posar y sentirte preciosa a tu manera.','Tu próxima noche especial merece un vestido que te haga sonreír frente al espejo. Dale tu toque con tus accesorios favoritos.','Para esas ocasiones que quieres recordar con una sonrisa. Elige este look y disfruta siendo tú.'],
'Cortos':['Una cita, una celebración o un plan con amigas: tú eliges la ocasión y este vestido acompaña tu estilo.','Un look para sentirte bonita, arreglarte con ilusión y disfrutar cada foto de tu próximo plan.','Hazlo tuyo con tus zapatos favoritos y sal a disfrutar. Tu estilo empieza por cómo te sientes.'],
'Cortos con brillo':['Hoy tienes permiso para brillar. Un look para celebrar con actitud y sentirte preciosa en cada foto.','Un toque de brillo para tu próxima noche especial. Combínalo a tu gusto y deja que tu sonrisa complete el look.','Para las chicas que disfrutan arreglarse y hacerse notar. Lleva este look con confianza y tu toque personal.'],
'Bandage':['Un look con actitud para una noche que promete. Combínalo con tus accesorios favoritos y disfruta tu momento.','Coqueto y con personalidad: un vestido para arreglarte a tu manera y salir sintiéndote fabulosa.'],
'Largos':['Un vestido para disfrutar una celebración con estilo propio. Añade tus accesorios favoritos y haz del look algo muy tuyo.','Para una ocasión especial y una entrada con encanto. Elige cómo combinarlo y luce tu personalidad.'],
'Liquidación':['Tu próximo look especial también puede ser una bonita oportunidad. Consulta disponibilidad y encuentra tu favorito.']}
products=[];next_id=max(p['id'] for p in old)+1
for index,m in enumerate(report['coincidencias']):
 if m['categoria']=='Fuera de vestidos':continue
 previous=next((p for p in old if p['photos'] and {x['sourceIndex'] for x in p['photos'] if x.get('sourceIndex')}==set(i for i in m['indices'] if not (i==18 and 144 in m['indices']))),None)
 if previous is None:
  candidates=[p for p in old if set(x.get('sourceIndex') for x in p['photos']).intersection(m['indices'])]
  assert len(candidates)<=1,('Asociación ambigua de productos publicados',m['nombre'])
  previous=candidates[0] if candidates else None
 id=previous['id'] if previous else next_id
 if not previous:next_id+=1
 category=m['categoria'].replace('Cortos sin brillo','Cortos')
 if previous and previous['category']=='Liquidación':category='Liquidación'
 photos=[]
 gallery_indices=[i for i in m['indices'] if not (i==18 and 144 in m['indices'])]
 for j,i in enumerate(gallery_indices,1):
  x=inv[i-1];source=r/replacements.get(i,x['path'])
  dest=r/f'images/productos-reales/XL-{id:03}/{j:02}-R{i:03}{source.suffix.lower()}'
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
  width,height=Image.open(source).size
  photo=dict(src='./'+dest.relative_to(r).as_posix(),width=width,height=height,sourceIndex=i,sha256=hashlib.sha256(source.read_bytes()).hexdigest())
  photo['view']=gallery_review.get(id,{}).get('vistas',{}).get(str(i),'Frente')
  if i in replacements:photo['sourceAttachment']=replacements[i]
  photos.append(photo)
 for j,extra in enumerate(gallery_review.get(id,{}).get('fotos_adicionales',[]),1):
  source=r/extra['path'];dest=r/f'images/productos-reales/XL-{id:03}/extra-{j:02}{source.suffix.lower()}'
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
  width,height=Image.open(source).size
  photos.append(dict(src='./'+dest.relative_to(r).as_posix(),width=width,height=height,sourceAttachment=extra['sourceAttachment'],view=extra['view'],sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
 photos.sort(key=lambda x:{'Frente':0,'Frente y espalda':0,'Frente y lateral':0,'Espalda':1,'Lateral':2,'Detalle':3}.get(x['view'],4))
 seen=set();unique=[]
 for photo in photos:
  if photo['sha256'] not in seen:unique.append(photo);seen.add(photo['sha256'])
 photos=unique
 name=m['nombre'].rstrip('…. ')
 product=dict(id=id,name=name,category=category,price=m['precio'],note=texts[category][index%len(texts[category])],photos=photos,image=photos[0]['src'],photoPending=False)
 if m.get('precio_regular'):product['originalPrice']=m['precio_regular']
 elif previous and previous.get('originalPrice'):product['originalPrice']=previous['originalPrice']
 if m.get('etiquetas'):product['tags']=m['etiquetas']
 products.append(product)
(r/'products.js').write_text('// Catálogo confirmado con fotografías reales. Disponibilidad y medidas se coordinan con la boutique.\nexport const products = '+json.dumps(products,ensure_ascii=False,indent=2)+';\nexport const categories = ["Todos", "Gala", "Largos", "Cortos con brillo", "Cortos", "Bandage", "Liquidación"];\n',encoding='utf-8')
(r/'review/publicados-confirmados.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
print('Publicados:',len(products),'Fotos:',sum(len(p['photos']) for p in products))
