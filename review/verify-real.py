from pathlib import Path
import json, hashlib, subprocess, re
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'review/real-classification.json').read_text(encoding='utf-8'))
inventory=json.loads((root/'review/real-inventory.json').read_text(encoding='utf-8'))
classified=[i for group in manifest['matched']+manifest['pending'] for i in group['sourceIndices']]
assert sorted(classified)==list(range(1,167))
for photo in inventory:
    assert hashlib.sha256((root/photo['path']).read_bytes()).hexdigest()==photo['sha256'], 'Se alteró un original'
for group in manifest['matched']+manifest['pending']:
    for photo in group['photos']:
        assert hashlib.sha256((root/photo['src']).read_bytes()).hexdigest()==photo['sha256'], 'Copia distinta del original'
baseline=subprocess.check_output(['git','show','HEAD:products.js'],cwd=root).decode('utf-8')
current=(root/'products.js').read_text(encoding='utf-8')
fields=lambda text: re.findall(r"id: (\d+), name: '([^']+)', category: '([^']+)', price: ([\d.]+)(?:, originalPrice: ([\d.]+))?",text)
assert fields(baseline)==fields(current), 'Cambió un nombre, categoría o precio existente'
assert not any(re.match(r'^catalog-\d+-(ai|model|faithful[^.]*)\.png$',p.name) for p in (root/'images').iterdir())
assert not (root/'public/images/imagenes-reales').exists()
assert not (root/'public/pendientes-dueno').exists()
print('Verificado: 166 originales intactos; cada archivo tiene grupo; todas las copias son idénticas; nombres, categorías y precios conservados; ninguna foto IA de prendas publicada.')
