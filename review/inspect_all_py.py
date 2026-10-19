import json
import re
from pathlib import Path

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

print(f"Loaded {len(products)} products.")

# Group products by current category
by_cat = {}
for p in products:
    by_cat.setdefault(p['category'], []).append(p)

for cat, items in by_cat.items():
    print(f"\n--- {cat} ({len(items)}) ---")
    for p in items:
        print(f"  {p['id']:3d}: {p['name']} (S/ {p['price']})")
