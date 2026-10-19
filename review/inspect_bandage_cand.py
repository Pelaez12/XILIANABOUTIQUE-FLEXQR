import json
from pathlib import Path
from PIL import Image

root = Path('.')
source = root / 'products.js'
with open(source, encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

candidates = [65, 80, 119, 121, 122, 157, 84, 85, 68]
for cid in candidates:
    p = next((x for x in products if x['id'] == cid), None)
    if p:
        print(f"ID {p['id']:3d} | Cat: {p['category']:17s} | {p['name']} | Photo: {p['photos'][0]['src']}")
