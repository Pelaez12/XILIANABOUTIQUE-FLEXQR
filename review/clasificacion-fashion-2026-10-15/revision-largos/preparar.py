import json, re, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
items=json.loads(re.search(r'export const products = (.*?);\s*export const categories',(ROOT/'products.js').read_text(encoding='utf-8'),re.S).group(1))
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',21)
font2=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
groups={
    'gala': [(p,n,ph) for p in sorted(items,key=lambda p:p['id']) if p['category']=='Gala' for n,ph in enumerate(p['photos'],1)],
    'maxi-restaurar': [(p,n,ph) for p in sorted(items,key=lambda p:p['id']) if p['id'] in [89,101,103,137,140,160,161,164] for n,ph in enumerate(p['photos'],1)]
}
manifest={}
for name, entries in groups.items():
    manifest[name]=[]
    for off in range(0,len(entries),9):
        page=entries[off:off+9]
        w,h=440,650
        sheet=Image.new('RGB',(3*w,math.ceil(len(page)/3)*h),'#eeeeee')
        draw=ImageDraw.Draw(sheet)
        for idx,(p,n,ph) in enumerate(page):
            x,y=idx%3*w,idx//3*h
            pic=Image.open(ROOT/ph['src'].removeprefix('./')).convert('RGB')
            pic.thumbnail((w-12,h-64))
            sheet.paste(pic,(x+(w-pic.width)//2,y))
            draw.text((x+6,y+h-60),f"XL-{p['id']:03d} / {n} / {ph.get('view','')}",font=font,fill='black')
            draw.text((x+6,y+h-31),p['category'],font=font2,fill='black')
        file=OUT/f'{name}-{off//9+1}.jpg'
        sheet.save(file,quality=94)
        manifest[name].append({'archivo':str(file),'fotos':[{'id':p['id'],'n':n,'src':ph['src']} for p,n,ph in page]})
(OUT/'laminas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print({name:{'fotos':len(entries),'laminas':len(manifest[name])} for name,entries in groups.items()})
