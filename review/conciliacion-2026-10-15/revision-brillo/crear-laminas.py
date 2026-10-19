import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
source = (ROOT / 'products.js').read_text(encoding='utf-8-sig')
products = json.JSONDecoder().raw_decode(source[source.index('['):])[0]
by_id = {p['id']: p for p in products}
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17)

def sheets(items, basename, cols=4, per_page=16):
    for start in range(0, len(items), per_page):
        page = items[start:start + per_page]
        rows = (len(page) + cols - 1) // cols
        canvas = Image.new('RGB', (cols * 360, rows * 590), '#f0f0ec')
        draw = ImageDraw.Draw(canvas)
        for i, (p, photo) in enumerate(page):
            x, y = (i % cols) * 360, (i // cols) * 590
            image = Image.open(ROOT / photo['src'].removeprefix('./')).convert('RGB')
            image = ImageOps.contain(image, (350, 510))
            canvas.paste(image, (x + (360-image.width)//2, y))
            draw.text((x+5, y+515), f"XL-{p['id']:03} | {photo.get('view', '?')}", font=font, fill='#111')
            draw.text((x+5, y+545), p['category'], font=small, fill='#111')
            draw.text((x+5, y+568), Path(photo['src']).name, font=small, fill='#111')
        canvas.save(OUT / f'{basename}-{start//per_page+1}.jpg', quality=94)

current = [p for p in products if p['category'] == 'Cortos con brillo']
sheets([(p, next(v for v in p['photos'] if v['src'] == p['image'])) for p in current], 'brillo-actual')
ids = [154, 101, 89, 103, 137, 140, 160, 161, 164, 110]
sheets([(by_id[i], by_id[i]['photos'][0]) for i in ids], 'similares', cols=3, per_page=12)
detail_ids = [82,83,85,86,114,118,123,127,130,153,172]
sheets([(by_id[i], photo) for i in detail_ids for photo in by_id[i]['photos']], 'detalles', cols=3, per_page=12)
(OUT / 'fuente-actual.json').write_text(json.dumps({'total':len(products), 'brillo':current, 'similares':[by_id[i] for i in ids]}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(current)} Brillo actuales; láminas en {OUT}')
