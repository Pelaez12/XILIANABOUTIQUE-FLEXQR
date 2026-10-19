"""Alinea las 14 categorías identificadas con las colecciones de WhatsApp."""

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
PRODUCTS = BASE.parent.parent / "products.js"
COMPARE = BASE / "comparacion_web_conservadora.json"
MAP = {
    "Gala Dresess": "Gala",
    "Vestidos Largos": "Largos",
    "Vestidos Cortos Brillos": "Cortos con brillo",
    "Vestidos Cortos": "Cortos",
    "Vestidos Bandage's": "Bandage",
}

records = json.loads(COMPARE.read_text(encoding="utf-8"))["vestidos"]
changes = [record for record in records if record["categoria_diferente"]]
assert len(changes) == 14, len(changes)
assert len({record["id_web"] for record in changes}) == 14

with PRODUCTS.open("r", encoding="utf-8", newline="") as handle:
    source = handle.read()

for record in changes:
    product_id = record["id_web"]
    pattern = re.compile(
        r'("id":\s*' + str(product_id) + r',\s*"name":\s*"[^"]+",\s*"category":\s*")([^"]+)(")'
    )
    matches = list(pattern.finditer(source))
    assert len(matches) == 1, (product_id, len(matches))
    old = matches[0].group(2)
    assert old == record["categoria_web"], (product_id, old, record["categoria_web"])
    target = MAP[record["grupo_whatsapp"]]
    source = pattern.sub(lambda m: m.group(1) + target + m.group(3), source, count=1)

with PRODUCTS.open("w", encoding="utf-8", newline="") as handle:
    handle.write(source)

print(json.dumps(
    [{"id": r["id_web"], "de": r["categoria_web"], "a": MAP[r["grupo_whatsapp"]]}
     for r in changes], ensure_ascii=False, indent=2
))
