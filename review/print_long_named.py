import json
import re

with open('products.js', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

def is_definitely_long(p):
    n = p['name'].lower()
    if 'corto' in n and 'largo' not in n:
        return False
    if any(w in n for w in ['largo', 'sirena', 'cola', 'romano', 'novia']):
        return True
    return False

long_named = [p for p in products if p['category'] != 'Bandage' and is_definitely_long(p)]
print(f"Total long named: {len(long_named)}")
for p in long_named:
    print(f"ID {p['id']:3d}: {p['name']}")
