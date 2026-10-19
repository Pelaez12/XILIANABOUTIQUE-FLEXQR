import json
import re
from pathlib import Path

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Non-bandage dresses: 118
non_bandage = [p for p in products if p['category'] != 'Bandage']

# Let's inspect long dresses
# Let's check which dresses are clearly long:
# 1. Names with 'largo', 'sirena', 'cola', 'romano', 'novia'
# 2. Or dresses that were historically in Gala/Largos and show floor-length in photo
def is_definitely_long(p):
    n = p['name'].lower()
    # Exceptions that say 'corto'
    if 'corto' in n and 'largo' not in n:
        return False
    if any(w in n for w in ['largo', 'sirena', 'cola', 'romano', 'novia']):
        return True
    return False

def is_definitely_short(p):
    n = p['name'].lower()
    if 'largo' in n:
        return False
    if any(w in n for w in ['corto', '3/4', 'mini', 'midi']):
        return True
    return False

long_named = [p for p in non_bandage if is_definitely_long(p)]
short_named = [p for p in non_bandage if is_definitely_short(p)]
unclear = [p for p in non_bandage if not is_definitely_long(p) and not is_definitely_short(p)]

print(f"Clearly named long: {len(long_named)}")
print(f"Clearly named short: {len(short_named)}")
print(f"Unclear (neither 'largo' nor 'corto'): {len(unclear)}")

print("\n--- UNCLEAR DRESSES ---")
for p in unclear:
    print(f"ID {p['id']:3d} | Current: {p['category']:17s} | {p['name']} | Photo: {p['photos'][0]['src']}")
