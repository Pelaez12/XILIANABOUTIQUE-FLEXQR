import json
import re
from pathlib import Path

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

# Let's inspect all dresses currently in Gala and Largos, plus ID 154
long_candidates = [p for p in products if p['category'] in ('Gala', 'Largos') or p['id'] == 154]

brillo_keywords = [
    'lentejuela', 'pedrería', 'pedreria', 'diamante', 'strass', 'perla',
    'platead', 'dorad', 'gold', 'brillante', 'brillos', 'copas de pedrería',
    'tejido brillante'
]

sin_brillo_keywords = [
    'estampad', 'floral', 'flores', 'rayas', 'campo', 'fucsia', 'gasa',
    'satín', 'satin', 'gamuz', 'gamusa', 'bruselas', 'amarillo', 'morado claro',
    'crema de mangas', 'azul acero', 'azul'
]

con_brillo = []
sin_brillo = []

for p in long_candidates:
    name_lower = p['name'].lower()
    has_b = any(k in name_lower for k in brillo_keywords)
    is_sin_b = any(k in name_lower for k in sin_brillo_keywords)
    
    # Check specific exceptions
    # e.g. ID 93 "Vestido fucsia con escote y pliegue izquierdo" -> sin brillo, user said "fucsia" goes to largos
    # ID 173 "Vestido rosado largo con estampado floral, mangas al codo y una rosa en la cintura" -> estampado floral
    # ID 108 "Vestido de gala de lentejuelas · modelo estampado" -> has lentejuelas
    # ID 110 "Vestido largo de gala blanco con rayas moradas y morado y de cap" -> rayas moradas (estampado)
    # ID 112 "Vestido largo de gala dorado con rayas doradas y blanco" -> dorado con rayas
    
    if has_b and not ('fucsia' in name_lower or 'estampado floral' in name_lower or 'rayas moradas' in name_lower):
        con_brillo.append(p)
    else:
        sin_brillo.append(p)

print(f"Total long candidates: {len(long_candidates)}")
print(f"Con brillo (Gala): {len(con_brillo)}")
print(f"Sin brillo / Estampados / Fucsia (Largos): {len(sin_brillo)}")

print("\n--- CON BRILLO ---")
for p in con_brillo:
    print(f"ID {p['id']:3d}: {p['name']}")

print("\n--- SIN BRILLO / ESTAMPADOS / FUCSIA ---")
for p in sin_brillo:
    print(f"ID {p['id']:3d}: {p['name']}")
