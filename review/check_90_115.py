import json
import re
from pathlib import Path
from PIL import Image

with open('products.js', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Check IDs 90 to 110
for pid in range(90, 115):
    p = next((x for x in products if x['id'] == pid), None)
    if p:
        photo = p['photos'][0]['src'].replace('./', '')
        im = Image.open(photo)
        print(f"ID {p['id']:3d} | Cat: {p['category']:17s} | {p['name']} | Img size: {im.size}")
