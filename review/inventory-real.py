from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json, hashlib, math
root = Path(__file__).resolve().parents[1]
files = sorted((root/'images/imagenes-reales').rglob('*.jpeg'))
records = []
for i, file in enumerate(files, 1):
    with Image.open(file) as im:
        records.append({'index': i, 'path': file.relative_to(root).as_posix(), 'width': im.width, 'height': im.height, 'bytes': file.stat().st_size, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
(root/'review/real-inventory.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
def sheets(items, prefix, per_page=24):
    for offset in range(0, len(items), per_page):
        page = items[offset:offset+per_page]
        sheet = Image.new('RGB', (1000, math.ceil(len(page)/4)*300), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for j, item in enumerate(page):
            x, y = (j%4)*250, (j//4)*300
            with Image.open(root/item['path']) as raw:
                thumb = ImageOps.contain(ImageOps.exif_transpose(raw).convert('RGB'), (238, 270))
                sheet.paste(thumb, (x+(250-thumb.width)//2, y+20+(270-thumb.height)//2))
            draw.text((x+8,y+4), f"{prefix}{item['index']:03d}   {item.get('width','')}x{item.get('height','')}", fill='black')
        dest = root/f'review/{prefix.lower()}-sheet-{offset//per_page+1}.jpg'
        sheet.save(dest, quality=92)
        print(dest)
sheets(records, 'R')
old = [{'index':i,'path':f"images/{'dress' if i<=17 else 'catalog'}-{i:02d}.jpg"} for i in range(1,59)]
sheets(old, 'P')
print('Photos:',len(records),'Distinct bytes:',len(set(r['sha256'] for r in records)))
