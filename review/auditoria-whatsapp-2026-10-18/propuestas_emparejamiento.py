"""Muestra posibles pares por precio sin convertirlos en ausencias confirmadas."""
import json
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

base = Path(__file__).parent
comparison = json.loads((base / 'comparacion_web_conservadora.json').read_text(encoding='utf-8'))
source = (base.parent.parent / 'products.js').read_text(encoding='utf-8')
web = json.loads(source[source.index('['):source.index('];') + 1])

def norm(value):
    value = unicodedata.normalize('NFD', value.lower())
    value = ''.join(c for c in value if unicodedata.category(c) != 'Mn')
    return ' '.join(re.findall('[a-z0-9]+', value))

matched = {x['id_web'] for x in comparison['vestidos'] if x['id_web'] is not None}
remaining = [x for x in web if x['id'] not in matched]
for row in comparison['vestidos']:
    if row['id_web'] is not None:
        continue
    price = row['precio_whatsapp']
    same_price = [p for p in remaining if p['price'] == price] if price is not None else []
    candidates = sorted(same_price, key=lambda p: SequenceMatcher(None, norm(row['nombre_whatsapp']), norm(p.get('catalogName', p['name']))).ratio(), reverse=True)
    print(row['grupo_whatsapp'], price, row['nombre_whatsapp'].encode('ascii','backslashreplace').decode())
    for p in candidates[:4]:
        score = SequenceMatcher(None, norm(row['nombre_whatsapp']), norm(p.get('catalogName', p['name']))).ratio()
        print('  ',p['id'],p['category'],round(score,2),p['name'].encode('ascii','backslashreplace').decode())
