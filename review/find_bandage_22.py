import json
from pathlib import Path

root = Path('.')
source = root / 'products.js'
with open(source, encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Non-bandage products
non_bandage = [p for p in products if p['category'] != 'Bandage']

print(f"Total non-bandage: {len(non_bandage)}")

# Let's list dresses that are tight, bodycon, or have bandage-like characteristics
for p in non_bandage:
    n = p['name'].lower()
    # Let's check for keywords or prices typical of bandage (e.g., 349-449)
    if any(k in n for k in ['bellmet', 'ceñid', 'cenid', 'tubo', 'ajustad', 'manga larga color rosado', 'cuello cuadrado', 'verde terciopelo', 'strapless', 'asimétrica']):
        print(f"ID {p['id']:3d} | Cat: {p['category']:17s} | S/{p['price']:5.1f} | {p['name']}")
