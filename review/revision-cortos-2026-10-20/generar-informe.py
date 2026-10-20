"""Coteja las33 apariciones de Cortos sin contar anuncios repetidos como prendas nuevas."""
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TEMP = Path(r'C:/Users/USER/AppData/Local/Temp')
source = (ROOT / 'products.js').read_text(encoding='utf-8')
products = json.loads(source.split('export const products = ', 1)[1].split('];', 1)[0] + ']')
by_id = {f"XL-{p['id']:03d}": p for p in products}
matrix = json.loads((ROOT / 'review/revision-brillos-2026-10-20/matriz-177.json').read_text(encoding='utf-8'))
rows = [r for r in matrix['filas_whatsapp'] if r['coleccion'] == 'Vestidos Cortos']
assert len(rows) == 33 and all(r['id_web'] in by_id for r in rows)
shots = {
    'codex-clipboard-9374a3e2-6ce7-4a3f-94fc-96c49b4b9f42.png': list(range(21, 31)),
    'codex-clipboard-16a0227d-e784-45b9-9213-28a6ffc6afa5.png': list(range(1, 11)),
    'codex-clipboard-e27a76cd-7fad-4e91-9efd-f09bd473f6a7.png': list(range(11, 21)),
    'codex-clipboard-f19aa2f0-27a0-4241-b760-ad31521595a7.png': list(range(31, 34)),
}
for filename, row_ids in shots.items():
    dest = OUT / ('lista-' + str(min(row_ids)).zfill(2) + '-' + str(max(row_ids)).zfill(2) + '.png')
    shutil.copyfile(TEMP / filename, dest)
    for index, number in enumerate(row_ids, 1):
        row = next(r for r in rows if r['fila'] == number)
        row['captura_propietario'] = str(dest.relative_to(ROOT)).replace('\\', '/')
        row['fila_en_captura'] = index
        row['categoria_web'] = by_id[row['id_web']]['category']
        row['precio_web'] = by_id[row['id_web']]['price']

liquidacion_ids = {'XL-010', 'XL-180', 'XL-181'}
assert {r['id_web'] for r in rows if by_id[r['id_web']]['category'] == 'Liquidación'} == liquidacion_ids
main_rows = [r for r in rows if r['id_web'] not in liquidacion_ids]
unique = {r['id_web'] for r in main_rows}
web = {key for key, p in by_id.items() if p['category'] == 'Cortos'}
assert len(main_rows) == 30 and len(unique) == 28 and len(web) == 29
assert not unique - web
assert web - unique == {'XL-114'}
counts = Counter(r['id_web'] for r in main_rows)
duplicate_rows = {key: [r for r in main_rows if r['id_web'] == key] for key, n in counts.items() if n > 1}
assert set(duplicate_rows) == {'XL-066', 'XL-187'}

all_photos = [(p, photo, hashlib.sha256((ROOT / photo['src'].removeprefix('./')).read_bytes()).hexdigest())
              for p in products for photo in p['photos']]
exact_cross = []
for p, photo, sha in all_photos:
    if f"XL-{p['id']:03d}" not in liquidacion_ids:
        continue
    for q, other, other_sha in all_photos:
        if q['category'] != 'Liquidación' and (sha == other_sha or photo['src'] == other['src']):
            exact_cross.append([p['id'], q['id'], photo['src'], other['src']])
assert exact_cross == []
target_rows = []
for key in sorted(liquidacion_ids):
    p = by_id[key]
    page = next((ROOT / 'public/vestidos').glob(f"{p['id']}-*/index.html"))
    route = '/' + page.parent.relative_to(ROOT / 'public').as_posix() + '/'
    appearing = [html.parent.name for html in (ROOT / 'public/colecciones').glob('*/index.html') if route in html.read_text(encoding='utf-8')]
    assert appearing == ['liquidacion']
    target_rows.append({'id_web': key, 'nombre': p['name'], 'precio_pen': p['price'], 'colecciones_publicadas': appearing})

result = {
    'fecha': '2026-10-20', 'instruccion_propietario': 'Auditar Cortos, conservar los3 modelos señalados exclusivamente en Liquidación y distinguir apariciones repetidas de prendas únicas.',
    'entradas_capturadas': 33, 'entradas_liquidacion': 3, 'entradas_restantes': 30,
    'repeticiones_comerciales_adicionales': 2, 'modelos_unicos_de_lista_para_cortos': 28,
    'productos_web_cortos': 29, 'fotos_web_cortos_revisadas': 48,
    'duplicados_de_producto_detectados_dentro_de_cortos_web': [],
    'faltantes_de_los_modelos_unicos_identificados': sorted(unique - web),
    'fichas_cortos_fuera_de_lista': [by_id[key] for key in sorted(web - unique)],
    'duplicados_en_lista_whatsapp': duplicate_rows,
    'liquidacion_confirmada_exclusiva': target_rows,
    'archivos_identicos_de_los3_en_otra_categoria': exact_cross,
    'reconciliacion': '33 apariciones -3 Liquidación -2 repeticiones =28 modelos únicos de la lista. La web tiene esos28 y XL-114 adicional =29. No se ha demostrado un conjunto de30 modelos únicos en estas capturas.',
    'catalogo_modificado': False,
    'filas_conciliadas': rows,
}
(OUT / 'resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('33 entradas:3 Liquidación,30 apariciones restantes,28 modelos únicos. Web Cortos29 únicos =28 de la lista +XL-114. Ningún modelo único identificado falta.')
