import json, math, re
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
products = json.loads(re.search(r'export const products = (.*?);\s*export const categories', (ROOT / 'products.js').read_text(encoding='utf-8'), re.S).group(1))
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 21)
bold = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 23)

def sheets(name, entries, per=9, cols=3, w=440, h=650):
    result = []
    for offset in range(0, len(entries), per):
        page = entries[offset:offset+per]
        canvas = Image.new('RGB', (cols*w, math.ceil(len(page)/cols)*h), '#eeeeee')
        draw = ImageDraw.Draw(canvas)
        for i, (p, n, photo) in enumerate(page):
            x, y = (i%cols)*w, (i//cols)*h
            pic = Image.open(ROOT / photo['src'].removeprefix('./')).convert('RGB')
            pic.thumbnail((w-12, h-62))
            canvas.paste(pic, (x+(w-pic.width)//2, y))
            draw.text((x+8, y+h-58), f"XL-{p['id']:03d} / {n} / {photo.get('view','')}", fill='black', font=bold)
            draw.text((x+8, y+h-29), p['category'], fill='black', font=font)
        file = OUT / f'{name}-{offset//per+1}.jpg'
        canvas.save(file, quality=94)
        result.append(str(file))
    return result

extras = [(p,n,ph) for p in sorted(products,key=lambda p:p['id']) if p['category']=='Largos' for n,ph in enumerate(p['photos'],1) if n>1]
candidate_ids = [62,68,81,87,90,91,106,112,136,140,141,159,161,174,175,176,177]
candidates = [(p,n,ph) for p in sorted(products,key=lambda p:p['id']) if p['id'] in candidate_ids for n,ph in enumerate(p['photos'],1)]
manifest = {'adicionales_largos': sheets('adicionales-largos',extras), 'candidatos': sheets('candidatos',candidates)}
(OUT / 'laminas-locales.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
