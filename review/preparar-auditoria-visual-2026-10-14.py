"""Láminas de inspección; no modifica fotos ni productos."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, re, textwrap

root=Path(__file__).resolve().parents[1]
out=root/'review/auditoria-visual-2026-10-14'
out.mkdir(exist_ok=True)
products=json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories',(root/'products.js').read_text(encoding='utf-8-sig'))[1])
snapshot=out/'productos-antes.json'
if not snapshot.exists():snapshot.write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',15)
boards=[]
def render(shots,prefix):
 for start in range(0,len(shots),25):
  chunk=shots[start:start+25];w,h=240,360
  board=Image.new('RGB',(w*5,h*((len(chunk)+4)//5)), '#eeeeee');draw=ImageDraw.Draw(board)
  for i,(p,photo,n) in enumerate(chunk):
   x=(i%5)*w;y=(i//5)*h
   image=Image.open(root/photo['src'].removeprefix('./')).convert('RGB')
   thumb=ImageOps.contain(image,(w-8,280))
   board.paste(thumb,(x+(w-thumb.width)//2,y))
   label=f"XL-{p['id']:03} / Foto {n+1} / {photo.get('view','')}"
   draw.text((x+6,y+282),label,font=bold,fill='#111111')
   for j,line in enumerate(textwrap.wrap(p['name'],31)[:3]):
    draw.text((x+6,y+303+j*15),line,font=font,fill='#333333')
   draw.text((x+6,y+348),p['category'],font=font,fill='#333333')
  path=out/f'{prefix}-{start//25+1}.jpg';board.save(path,quality=94)
  boards.append({'archivo':str(path.relative_to(root)),'fotos':[{'id':p['id'],'foto':n+1,'src':photo['src']} for p,photo,n in chunk]})
for cat in ['Gala','Largos','Cortos con brillo','Cortos','Bandage','Liquidación']:
 render([(p,p['photos'][0],0) for p in products if p['category']==cat], re.sub(r'[^a-z0-9]+','-',cat.lower()))
render([(p,photo,i) for p in products for i,photo in enumerate(p['photos']) if i>0],'vistas-adicionales')
(out/'laminas.json').write_text(json.dumps(boards,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'prendas':len(products),'fotos':sum(len(p['photos']) for p in products),'laminas':[b['archivo'] for b in boards]},ensure_ascii=False))
