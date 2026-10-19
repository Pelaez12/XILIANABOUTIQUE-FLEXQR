from pathlib import Path
import json
import re
from PIL import Image

root = Path('.')
source = root / 'products.js'
text = source.read_text(encoding='utf-8')
match = re.search(r'export const products = ([\s\S]*?);\s*export const categories', text)
products = json.loads(match[1])

gala_largos = [p for p in products if p['category'] in ('Gala', 'Largos')]

print(f"Total to examine: {len(gala_largos)}")

# Let's create an HTML contact sheet to visually inspect all 61 dresses
html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body { font-family: system-ui; background: #18181b; color: #f4f4f5; margin: 0; padding: 20px; }
h1 { font-size: 20px; margin-bottom: 20px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.card { background: #27272a; border-radius: 8px; overflow: hidden; border: 1px solid #3f3f46; display: flex; flex-direction: column; }
.card img { width: 100%; height: 320px; object-fit: contain; background: #09090b; }
.info { padding: 12px; font-size: 13px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-bottom: 6px; }
.badge-Gala { background: #eab308; color: #000; }
.badge-Largos { background: #3b82f6; color: #fff; }
.id { font-weight: bold; color: #a1a1aa; }
.name { margin: 4px 0; font-size: 13px; line-height: 1.4; }
.price { font-weight: bold; color: #22c55e; margin-top: 6px; }
</style>
</head><body>
<h1>Revisión de 61 prendas en Gala y Largos</h1>
<div class="grid">
"""

for p in gala_largos:
    photo_src = p['photos'][0]['src'].replace('./', '../')
    html += f"""
    <div class="card" id="card-{p['id']}">
        <img src="{photo_src}" loading="lazy">
        <div class="info">
            <div>
                <span class="badge badge-{p['category']}">{p['category']}</span>
                <span class="id">XL-{p['id']:03d}</span>
                <div class="name">{p['name']}</div>
            </div>
            <div class="price">S/ {p['price']}</div>
        </div>
    </div>
    """

html += "</div></body></html>"
(root / 'review/gala_largos_review.html').write_text(html, encoding='utf-8')
print("Saved review/gala_largos_review.html")
