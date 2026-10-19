import json
import re
from pathlib import Path

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

non_bandage = [p for p in products if p['category'] != 'Bandage']
print(f"Total non-bandage: {len(non_bandage)}")

# Let's inspect which ones are long vs short
for p in non_bandage:
    print(f"ID {p['id']:3d} | Current: {p['category']:17s} | S/{p['price']:5.1f} | {p['name']}")
