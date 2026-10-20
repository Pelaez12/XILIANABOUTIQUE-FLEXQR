"""Retira XL-173 por instrucción del propietario y conserva XL-214 a S/549."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
source = ROOT / 'products.js'
text = source.read_text(encoding='utf-8')
products = json.loads(text.split('export const products = ', 1)[1].split('];', 1)[0] + ']')
retired = next(p for p in products if p['id'] == 173)
canonical = next(p for p in products if p['id'] == 214)
assert len(products) == 178 and canonical['price'] == 549 and canonical['category'] == 'Largos'

start = text.index('  {\n    "id": 173,')
end = text.index('  {\n    "id": 179,', start)
source.write_text(text[:start] + text[end:], encoding='utf-8')
products = [p for p in products if p['id'] != 173]
(ROOT / 'review/publicados-confirmados.json').write_text(json.dumps(products, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

entry = {
    'id_retirado': 173, 'id_vigente': 214, 'fecha': '2026-10-20',
    'motivo': 'Mismo modelo y misma fotografía en dos codificaciones. El propietario ordenó borrar XL-173 y conservar la ficha confirmada más recientemente, XL-214 a S/549.',
    'instruccion_propietario': 'BORRA-XL173',
    'precio_vigente_pen': 549, 'categoria_vigente': 'Largos',
    'codigo_whatsapp_vigente': '2083',
    'evidencia': 'review/duplicados-fotos-2026-10-20/gala-largos/duplicado-173-214.jpg',
    'fotos_identidad': [{'src': p['src'], 'sha256': p['sha256']} for item in (retired, canonical) for p in item['photos']],
}
(ROOT / 'review/identidades-consolidadas.json').write_text(json.dumps({'version': 1, 'consolidaciones': [entry]}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(OUT / 'resolucion-xl173.json').write_text(json.dumps({**entry, 'ficha_retirada': retired, 'ficha_vigente': canonical, 'total_publicados': 177, 'largos_publicados': 25}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Retirado XL-173; vigente XL-214 a S/549. Total177, Largos25. Fotos históricas conservadas.')
