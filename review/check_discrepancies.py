import json
import re
from pathlib import Path
from PIL import Image

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

print("Checking all products for category discrepancies...")

# Let's inspect each category
for p in products:
    name = p['name'].lower()
    cat = p['category']
    photo_rel = p['photos'][0]['src'].replace('./', '')
    photo_path = root / photo_rel
    
    # Check if name has 'corto' but cat is Gala or Largos
    if 'corto' in name and cat in ('Gala', 'Largos'):
        print(f"[CORTO in {cat}] ID {p['id']}: {p['name']}")
        
    # Check if name has 'largo' but cat is Cortos or Cortos con brillo or Bandage
    if 'largo' in name and cat in ('Cortos', 'Cortos con brillo', 'Bandage'):
        print(f"[LARGO in {cat}] ID {p['id']}: {p['name']}")

    # Check if name has 'bandage' but cat is not Bandage
    if 'bandage' in name and cat != 'Bandage':
        print(f"[BANDAGE in {cat}] ID {p['id']}: {p['name']}")

    # Check if name has 'brillo'/'lentejuela'/'pedrer'/'strass' in Cortos (sin brillo)
    if any(b in name for b in ['lentejuela', 'pedrer', 'strass', 'diamante', 'brillo']) and cat == 'Cortos':
        print(f"[BRILLO in Cortos] ID {p['id']}: {p['name']}")
