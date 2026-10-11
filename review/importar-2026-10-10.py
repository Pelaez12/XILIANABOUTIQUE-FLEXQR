from pathlib import Path
from zipfile import ZipFile
from PIL import Image,ImageOps,ImageDraw
import json,hashlib,re
r=Path(__file__).resolve().parents[1]; d=r/'review/importacion-2026-10-10';d.mkdir(exist_ok=True)
p=json.loads((r/'review/publicados-confirmados.json').read_text(encoding='utf-8'))
existing=[(x['id'],r/f['src'].removeprefix('./')) for x in p for f in x['photos']]
hashes={hashlib.sha256(f.read_bytes()).hexdigest():i for i,f in existing}
def dh(f):
 im=Image.open(f).convert('L').resize((17,16)); a=list(im.getdata());return [a[y*17+x]>a[y*17+x+1] for y in range(16) for x in range(16)]
eh=[(i,f,dh(f)) for i,f in existing]
sources=[]
for name in ['WhatsApp Unknown 2026-10-10 at 12.03.31 AM.zip','WhatsApp Unknown 2026-10-10 at 12.03.17 AM.zip']:
 with ZipFile(Path('C:/Users/USER/Downloads')/name) as z:
  for f in z.infolist():
   if not f.is_dir() and Path(f.filename).suffix.lower() in ('.jpg','.jpeg','.png','.webp'):sources.append((name,f.filename,z.read(f)))
name='WhatsApp Image 2026-10-09 at 12.41.48 PM.jpeg';sources.append(('Adjunto',name,(Path('C:/Users/USER/Downloads')/name).read_bytes()))
entries=[]
for n,(z,name,raw) in enumerate(sources,1):
 f=d/f'N{n:03}.jpeg';f.write_bytes(raw);sha=hashlib.sha256(raw).hexdigest();h=dh(f)
 near=sorted([(sum(a!=b for a,b in zip(h,v)),i,str(path.relative_to(r))) for i,path,v in eh])[:3]
 entries.append(dict(n=n,nombre=name,origen=z,path=str(f.relative_to(r)),sha256=sha,duplicado=hashes.get(sha),candidatos=near))
(d/'inventario.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
for offset in range(0,len(entries),20):
 batch=entries[offset:offset+20];canvas=Image.new('RGB',(1200,((len(batch)+4)//5)*330),'white');draw=ImageDraw.Draw(canvas)
 for j,e in enumerate(batch):
  x=j%5*240;y=j//5*330
  canvas.paste(ImageOps.contain(Image.open(r/e['path']).convert('RGB'),(230,290)),(x+5,y+30))
  draw.text((x+5,y+5),f"N{e['n']:03} dup:{e['duplicado']} near:{e['candidatos'][0][1]}",fill='black')
 canvas.save(d/f'contacto-{offset//20+1}.jpg')
print(len(entries),'fotos;',sum(e['duplicado'] is not None for e in entries),'duplicados exactos')
for offset in range(0,len(existing),40):
 batch=existing[offset:offset+40];canvas=Image.new('RGB',(1400,((len(batch)+7)//8)*240),'white');draw=ImageDraw.Draw(canvas)
 for j,(ident,f) in enumerate(batch):
  x=j%8*175;y=j//8*240
  canvas.paste(ImageOps.contain(Image.open(f).convert('RGB'),(165,210)),(x+5,y+25));draw.text((x+5,y+5),f'XL-{ident} {f.name[:9]}',fill='black')
 canvas.save(d/f'existentes-{offset//40+1}.jpg')
