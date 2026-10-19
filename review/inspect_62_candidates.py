import json
import re
from pathlib import Path

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Let's inspect all dresses currently in Gala (43) and Largos (18) and ID 154 (1)
candidates = [p for p in products if p['category'] in ('Gala', 'Largos') or p['id'] == 154]

print(f"Total candidates in Gala/Largos/154: {len(candidates)}")

# We know 17 of them should move to Cortos (12), Cortos con brillo (4), Bandage (1)
# Let's identify which of these 62 are actually short or bandage!
for p in candidates:
    print(f"ID {p['id']:3d} | {p['category']:6s} | S/{p['price']:6.1f} | {p['name']}")
