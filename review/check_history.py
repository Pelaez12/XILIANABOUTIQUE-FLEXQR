from pathlib import Path
import json
import re

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Check past categories in products-antes-confirmados.json or review/real-classification.json
before_conf_file = root / 'review/products-antes-confirmados.json'
if before_conf_file.exists():
    before_conf = json.loads(before_conf_file.read_text(encoding='utf-8'))
    by_id_before = {p['id']: p['category'] for p in before_conf}
    print("Found products-antes-confirmados.json!")
    for p in products:
        old_cat = by_id_before.get(p['id'])
        if old_cat != p['category']:
            print(f"ID {p['id']:3d}: {p['name']} | Was: {old_cat} -> Now: {p['category']}")
else:
    print("No products-antes-confirmados.json")
