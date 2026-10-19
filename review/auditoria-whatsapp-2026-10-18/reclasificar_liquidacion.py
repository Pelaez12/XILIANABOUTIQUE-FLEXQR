"""Asigna Liquidación como categoría exclusiva a las fichas web verificadas."""

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent.parent / "products.js"
EXPECT = {
    10: 68.70,
    16: 164.50,
    17: 194.50,
    155: 75.60,
    169: 114.50,
    172: 119.50,
    180: 86.70,
    181: 115.60,
}

with SOURCE.open("r", encoding="utf-8", newline="") as handle:
    source = handle.read()
products = json.loads(source[source.index("["):source.index("];") + 1])
by_id = {item["id"]: item for item in products}
for product_id, price in EXPECT.items():
    item = by_id[product_id]
    assert item["category"] != "Liquidación", product_id
    assert float(item["price"]) == price, (product_id, item["price"])
    pattern = re.compile(
        r'("id":\s*' + str(product_id)
        + r',\s*"name":\s*"[^"]+",\s*"category":\s*")([^"]+)(")'
    )
    assert len(pattern.findall(source)) == 1, product_id
    source = pattern.sub(lambda m: m.group(1) + "Liquidación" + m.group(3), source, count=1)

with SOURCE.open("w", encoding="utf-8", newline="") as handle:
    handle.write(source)
print(json.dumps({"movidos": list(EXPECT), "cantidad": len(EXPECT)}))
