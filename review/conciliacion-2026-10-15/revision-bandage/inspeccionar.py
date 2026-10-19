import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parents[3]
text = (root / 'products.js').read_text(encoding='utf-8')
products = json.loads(re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)[1])
print('ACTUALES BANDAGE')
for p in products:
    if p['category'] == 'Bandage':
        print(json.dumps({k:p[k] for k in ['id','name','price','photos']}, ensure_ascii=False))

print('\nBANDAGE EN CATALOGO VERIFICADO')
data = json.loads((root/'review/catalogo-verificado-2026-10-06.json').read_text(encoding='utf-8'))
print('keys', list(data))
for p in data['registros']:
    if 'bandage' in p.get('nombre','').lower():
        print(json.dumps(p, ensure_ascii=False))

print('\nCONFIRMACIONES RELEVANTES')
data = json.loads((root/'review/confirmaciones-usuario.json').read_text(encoding='utf-8'))
for p in data:
    if 'bandage' in str(p).lower() or 'pedrería plateada' in str(p).lower():
        print(json.dumps(p, ensure_ascii=False))

print('\nBANDAGE EN LISTA WHATSAPP ACTUAL')
data = json.loads((root/'review/catalogo-whatsapp-2026-10-12/todos-articulos.json').read_text(encoding='utf-8'))
for i,p in enumerate(data):
    if 'bandage' in str(p).lower():
        print(i, json.dumps(p, ensure_ascii=False))
