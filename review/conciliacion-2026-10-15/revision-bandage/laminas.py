import json, re
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
source = (root/'products.js').read_text(encoding='utf-8')
products = json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories', source)[1])
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for f in ['video-1.jpg','video-4.jpg']:
    im=Image.open(root/'review/grabaciones-2026-10-06'/f)
    print(f, im.size)
    if f=='video-1.jpg':
        im.crop((420,0,840,670)).save(out/'fuente-rojo-largo.png')
    else:
        im.crop((1260,0,1680,640)).save(out/'fuente-rojo-corto.png')

ids=[73,20,90,100,101,142,152,162,163,166]
sheet=Image.new('RGB',(5*280,2*465),'#efefef')
d=ImageDraw.Draw(sheet)
for i,pid in enumerate(ids):
    p=next(p for p in products if p['id']==pid)
    im=Image.open(root/p['photos'][0]['src'])
    im=ImageOps.contain(im,(270,400))
    x=(i%5)*280+(280-im.width)//2; y=(i//5)*465
    sheet.paste(im,(x,y))
    d.text(((i%5)*280+5,y+405),f"XL-{pid:03d} / {p['category']} / S/ {p['price']}",font=font,fill='black')
sheet.save(out/'comparacion-rojos.jpg',quality=94)
