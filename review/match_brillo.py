import json
import re
from pathlib import Path

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

with open('review/catalogo-whatsapp-2026-10-12/brillo-completo.json', encoding='utf-8') as f:
    brillo_wa = json.load(f)

print(f"Total in WhatsApp brillo-completo: {len(brillo_wa)}")

# Normalize helper
def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

by_norm = {norm(p['name']): p for p in products}

matched = []
unmatched = []

for text in brillo_wa:
    # Extract name before PEN or price
    name_clean = re.sub(r'(?:prenda[s]?\s+importada[s]?|\d+%\s+descuento|\(s\s+m\)|\(l\)|cod\s+\d+|\d+)?pen\s+[\d\.,]+.*$', '', text, flags=re.I).strip()
    name_clean = re.sub(r'ic-add$', '', name_clean).strip()
    # Find match
    found = None
    for p in products:
        if norm(p['name']) == norm(name_clean):
            found = p
            break
        elif norm(name_clean) in norm(p['name']) or norm(p['name']) in norm(name_clean):
            found = p
            break
    if found:
        matched.append((found['id'], found['name'], name_clean))
    else:
        unmatched.append(text)

print(f"Matched: {len(matched)}")
print(f"Unmatched: {len(unmatched)}")
if unmatched:
    for u in unmatched:
        print("  Unmatched:", u)

print("\nMatched IDs:")
seen = set()
unique_matched = []
for m in matched:
    if m[0] not in seen:
        seen.add(m[0])
        unique_matched.append(m)
    else:
        print("  Duplicate match in brillo:", m)

print(f"Unique matched: {len(unique_matched)}")
