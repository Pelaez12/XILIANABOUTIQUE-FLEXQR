import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
GROUPS = [
    ("Gala Dresess", ["coleccion_1.txt", "gala_carga_completa.txt", "gala_inicio.txt", "gala_final.txt"]),
    ("Vestidos Largos", ["coleccion_2.txt", "largos_23.txt"]),
    ("Vestidos Cortos Brillos", ["brillos_20.txt", "brillos_medio.txt", "brillos_final.txt"]),
    ("Vestidos Cortos", ["cortos_20.txt", "cortos_final.txt"]),
    ("Vestidos Bandage's", ["bandage_20.txt", "bandage_23.txt"]),
    ("PENDIENTES 1", ["pendientes_1.txt"]),
    ("PENDIENTES 2", ["pendientes_2_20.txt", "pendientes_2_medio.txt", "pendientes_2_final.txt"]),
    ("PENDIENTES 3", ["pendientes_3.txt"]),
    ("CALZADOS", ["calzados.txt"]),
    ("ACCESORIOS U OTROS", ["accesorios.txt"]),
]


def extract(path, heading):
    text = path.read_text(encoding="utf-8")
    marker = f"heading {heading}, Value: 2"
    if marker not in text:
        return []
    text = text[text.rfind(marker):]
    items = []
    pattern = re.compile(r"^\s*\d+ button (?!Añadir 1 artículo)(.+Añadir 1 artículo)$", re.M)
    matches = list(pattern.finditer(text))
    for i, match in enumerate(matches):
        label = match.group(1)
        block = text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        children = re.findall(r"^\s*\d+ text (.+)$", block, re.M)
        if not children:
            continue
        prices = re.findall(r"PEN\s*([\d,.]+)", label)
        current = float(prices[0].replace(",", "")) if prices else None
        previous = float(prices[1].replace(",", "")) if len(prices) > 1 else None
        discount_match = re.search(r"(\d+)\s*%", label)
        discount = int(discount_match.group(1)) if discount_match else None
        # The first child is the catalog title. A description, when present,
        # follows it and precedes the visible price in the product button.
        name = children[0]
        last_text = children[-1]
        description = re.sub(r"(?:\s*PEN\s*[\d,.]+)+\s*$", "", last_text).strip()
        description = re.sub(r"^\s*\d+%\s*Descuento\.?\s*", "", description).strip()
        if description == name or description.startswith("PEN") or not description:
            description = ""
        items.append({
            "coleccion": heading,
            "nombre": name,
            "precio_pen": current,
            "precio_anterior_pen": previous,
            "descuento_pct": discount,
            "descripcion": description,
            "fotos": [],
            "estado": "NO VERIFICADO",
            "_etiqueta": label,
        })
    return items


inventory = []
counts = {}
for group, filenames in GROUPS:
    heading = "PENDIENTES" if group.startswith("PENDIENTES") else group
    seen = set()
    group_items = []
    for filename in filenames:
        for item in extract(ROOT / filename, heading):
            key = item["_etiqueta"]
            if key in seen:
                continue
            seen.add(key)
            item["grupo_fuente"] = group
            group_items.append(item)
    counts[group] = len(group_items)
    inventory.extend(group_items)

(ROOT / "inventario_observado.json").write_text(
    json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({"conteos_observados": counts, "total": len(inventory)}, ensure_ascii=False, indent=2))
