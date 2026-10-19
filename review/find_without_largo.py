from pathlib import Path
import json
import re

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Let's inspect products where name does NOT say "largo"
candidates_without_largo = []
for p in products:
    name = p['name'].lower()
    cat = p['category']
    if cat in ('Gala', 'Largos') and 'largo' not in name:
        candidates_without_largo.append(p)

print(f"Products in Gala/Largos whose name does NOT include 'largo': {len(candidates_without_largo)}")
for p in candidates_without_largo:
    print(f"ID {p['id']:3d} | Cat: {p['category']:6s} | S/{p['price']:6.1f} | {p['name']}")
