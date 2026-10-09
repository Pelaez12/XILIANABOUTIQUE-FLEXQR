from pathlib import Path
from zipfile import ZipFile
from PIL import Image, ImageOps, ImageDraw
import json, hashlib
r=Path(__file__).resolve().parent.parent
d=r/'review/importacion-2026-10-08'
d.mkdir(exist_ok=True)
sources=[]
for name in ['WhatsApp Unknown 2026-10-08 at 6.52.51 PM.zip','WhatsApp Unknown 2026-10-08 at 6.52.56 PM.zip','WhatsApp Unknown 2026-10-08 at 6.53.01 PM.zip']:
    with ZipFile(Path('C:/Users/USER/Downloads')/name) as z:
        for i in z.infolist():
            if not i.is_dir(): sources.append((name,i.filename,z.read(i)))
for name in ['WhatsApp Image 2026-10-07 at 5.59.06 PM.jpeg','WhatsApp Image 2026-10-07 at 6.01.47 PM.jpeg']:
    sources.append(('Adjunto',name,(Path('C:/Users/USER/Downloads')/name).read_bytes()))
entries=[]
for k,(z,name,raw) in enumerate(sources,1):
    p=d/f'N{k:03}.jpeg';p.write_bytes(raw)
    entries.append(dict(n=k,zip=z,nombre=name,path=p.relative_to(r).as_posix(),sha256=hashlib.sha256(raw).hexdigest()))
(d/'inventario.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
canvas=Image.new('RGB',(1200,((len(entries)+5)//6)*310),'white')
draw=ImageDraw.Draw(canvas)
for i,e in enumerate(entries):
    canvas.paste(ImageOps.contain(Image.open(r/e['path']).convert('RGB'),(190,275)),((i%6)*200+5,(i//6)*310+25))
    draw.text(((i%6)*200+8,(i//6)*310+5),f"N{e['n']:03}",fill='black')
canvas.save(d/'contacto.jpg')
print(len(entries),'fotos importadas')
