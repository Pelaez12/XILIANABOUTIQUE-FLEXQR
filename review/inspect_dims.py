from pathlib import Path
import json
import re

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Check all products in Gala and Largos
# What are their source photos or notes?
gala_largos = [p for p in products if p['category'] in ('Gala', 'Largos') or p['id'] == 154]

# Let's inspect their notes and source attachments
for p in gala_largos:
    first_photo = p['photos'][0]
    src = first_photo.get('src')
    w = first_photo.get('width')
    h = first_photo.get('height')
    view = first_photo.get('view')
    print(f"ID {p['id']:3d} | {p['category']:6s} | {p['name']} | W:{w} H:{h} | {src}")
