"""Inventario reproducible de fotos publicadas y candidatos visuales a duplicados.

No consulta PENDIENTES de WhatsApp ni modifica el catálogo.
Los hashes perceptuales generan candidatos, no confirman identidad de prendas.
"""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy.fft import dctn

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def phash(image):
    pixels = np.asarray(image.convert('L').resize((32, 32), Image.Resampling.LANCZOS), dtype=float)
    coeff = dctn(pixels, norm='ortho')[:8, :8].ravel()[1:]
    return sum(int(v > np.median(coeff)) << i for i, v in enumerate(coeff))


def dhash(image):
    pixels = np.asarray(image.convert('L').resize((9, 8), Image.Resampling.LANCZOS))
    return sum(int(v) << i for i, v in enumerate((pixels[:, 1:] > pixels[:, :-1]).ravel()))


text = (ROOT / 'products.js').read_text(encoding='utf-8')
products = json.loads(text.split('export const products = ', 1)[1].split('];', 1)[0] + ']')
products = [p for p in products if p['category'].casefold() != 'pendientes']
photos = []
errors = []
for p in products:
    for index, photo in enumerate(p.get('photos') or [{'src': p['image']}], 1):
        path = ROOT / photo['src'].removeprefix('./')
        try:
            with Image.open(path) as raw:
                im = ImageOps.exif_transpose(raw).convert('RGB')
                w, h = im.size
                middle = im.crop((round(w * .15), round(h * .1), round(w * .85), round(h * .95)))
                hashes = {'phash': phash(im), 'dhash': dhash(im), 'phash_centro': phash(middle), 'phash_espejo': phash(ImageOps.mirror(im))}
                pixel_hash = hashlib.sha256(im.tobytes() + f'{w}x{h}'.encode()).hexdigest()
            actual_sha = hashlib.sha256(path.read_bytes()).hexdigest()
            photos.append({'id': p['id'], 'nombre': p['name'], 'categoria': p['category'], 'numero': index,
                           'src': photo['src'], 'vista': photo.get('view'), 'principal': p['image'] == photo['src'],
                           'dimensiones': [w, h], 'sha256': actual_sha, 'pixel_sha256': pixel_hash,
                           'sha_declarado_correcto': not photo.get('sha256') or photo['sha256'] == actual_sha, **hashes})
        except Exception as exc:
            errors.append({'id': p['id'], 'src': photo['src'], 'error': str(exc)})

groups = defaultdict(list)
for item in photos:
    groups[item['sha256']].append(item)
exact = [v for v in groups.values() if len(v) > 1]
groups = defaultdict(list)
for item in photos:
    groups[item['pixel_sha256']].append(item)
pixel_exact = [v for v in groups.values() if len(v) > 1 and len({p['sha256'] for p in v}) > 1]

def ref(item):
    return {k: item[k] for k in ('id', 'nombre', 'categoria', 'numero', 'src', 'vista', 'principal')}

pairs = []
for i, a in enumerate(photos):
    for b in photos[i+1:]:
        if a['sha256'] == b['sha256'] or a['pixel_sha256'] == b['pixel_sha256']:
            continue
        distances = {k: (a[k] ^ b[k]).bit_count() for k in ('phash', 'dhash', 'phash_centro')}
        distances['phash_espejo'] = (a['phash'] ^ b['phash_espejo']).bit_count()
        if (distances['phash'] <= 12 or distances['dhash'] <= 7 or distances['phash_centro'] <= 10 or distances['phash_espejo'] <= 8):
            pairs.append({'a': ref(a), 'b': ref(b), 'misma_ficha': a['id'] == b['id'], 'distancias': distances})
pairs.sort(key=lambda p: min(p['distancias'].values()))
result = {'fecha': '2026-10-20', 'alcance': 'Fotos de todas las fichas publicadas; excluida colección PENDIENTES de WhatsApp',
          'productos': len(products), 'fotos': len(photos), 'conteos_productos': dict(Counter(p['category'] for p in products)),
          'conteos_fotos': dict(Counter(p['categoria'] for p in photos)), 'errores': errors,
          'sha_incorrectos': [ref(p) for p in photos if not p['sha_declarado_correcto']],
          'grupos_archivo_identico': exact, 'grupos_pixeles_identicos': pixel_exact,
          'candidatos': pairs, 'inventario_fotos': photos}
(OUT/'analisis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
for group_name, selected in [('entre-fichas', [p for p in pairs if not p['misma_ficha']]), ('misma-ficha', [p for p in pairs if p['misma_ficha']])]:
    for page in range((len(selected)+11)//12):
        batch = selected[page*12:(page+1)*12]
        sheet = Image.new('RGB', (1200, 4*300), 'white')
        draw = ImageDraw.Draw(sheet)
        for idx, pair in enumerate(batch):
            x, y = (idx % 3)*400, (idx//3)*300
            for j, side in enumerate(('a','b')):
                item = pair[side]
                with Image.open(ROOT/item['src'].removeprefix('./')) as raw:
                    im = ImageOps.exif_transpose(raw).convert('RGB')
                    im.thumbnail((190, 230))
                    sheet.paste(im, (x+j*200+(190-im.width)//2, y))
                draw.text((x+j*200+3, y+232), f"XL-{item['id']:03d} foto {item['numero']}", fill='black', font=font)
                draw.text((x+j*200+3, y+253), item['categoria'], fill='black', font=small)
            draw.text((x+3, y+275), str(pair['distancias']), fill='black', font=small)
        sheet.save(OUT/f'candidatos-{group_name}-{page+1:02d}.jpg', quality=90)
print(json.dumps({k:result[k] for k in ('productos','fotos','conteos_productos','conteos_fotos')}, ensure_ascii=True))
print('errores',len(errors),'sha incorrectos',len(result['sha_incorrectos']),'exactos',len(exact),'pixeles',len(pixel_exact),'pares',len(pairs),'entre fichas',sum(not p['misma_ficha'] for p in pairs))
