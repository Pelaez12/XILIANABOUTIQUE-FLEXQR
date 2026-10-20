"""Concilia el blanco duplicado e incorpora dos prendas Bandage con fotos del propietario."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TEMP = Path(r"C:\Users\USER\AppData\Local\Temp")
INPUTS = [
    "codex-clipboard-03905a6d-32f8-4a1a-b2a1-5294251a88dc.png",
    "codex-clipboard-905ff86a-808f-4e38-93e7-4a9eb7b2ec37.png",
    "codex-clipboard-64421c5d-55af-463a-8fec-85cd8e07f275.png",
]
SRC = ROOT / "products.js"
text = SRC.read_text(encoding="utf-8")
prefix, tail = text.split("export const products = ", 1)
payload, suffix = tail.split("];", 1)
products = json.loads(payload + "]")
assert len(products) == 175
assert all(i not in {p["id"] for p in products} for i in (215, 216))

def copy_photo(filename, product_id, dest_name):
    original = TEMP / filename
    assert original.is_file(), original
    with Image.open(original) as image:
        image.verify()
    with Image.open(original) as image:
        width, height = image.size
    assert width >= 600 and height >= 700
    folder = ROOT / "images" / "productos-reales" / f"XL-{product_id:03d}"
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / dest_name
    shutil.copyfile(original, dest)
    return {"src": f"./images/productos-reales/XL-{product_id:03d}/{dest_name}",
            "width": width, "height": height, "view": "Frente",
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}

white = copy_photo(INPUTS[0], 187, "03-propietario-frente.png")
white["sourceAttachment"] = INPUTS[0]
white["sourceType"] = "Foto original entregada por el propietario el 19/10/2026; corresponde también al código comercial 1894."
product187 = next(p for p in products if p["id"] == 187)
assert product187["price"] == 329 and product187["category"] == "Cortos"
product187["photos"].insert(0, white)
product187["image"] = white["src"]
product187["catalogCode"] = "1914"
product187["catalogDuplicate"] = {"codigo": "1894", "nombre": "Vestido blanco con perlas",
                                  "precio_listado_pen": 319,
                                  "resolucion": "Misma prenda y foto; el propietario confirmó conservar S/329 el 19/10/2026."}

start = text.index('  {\n    "id": 187,')
end = text.index('  {\n    "id": 196,', start)
block = text[start:end]
photo_json = json.dumps(white, ensure_ascii=False, indent=2).replace("\n", "\n      ")
block = block.replace('    "photos": [\n', '    "photos": [\n      ' + photo_json + ',\n', 1)
block = block.replace('    "image": "./images/productos-reales/XL-187/01-WA-Cortos-blanco-frente.png",',
                      '    "image": "' + white["src"] + '",', 1)
block = block.replace('    "catalogCategory": "Vestidos Cortos",\n',
                      '    "catalogCategory": "Vestidos Cortos",\n    "catalogCode": "1914",\n', 1)
assert block.endswith('    }\n  },\n')
alias_json = json.dumps(product187["catalogDuplicate"], ensure_ascii=False, indent=2).replace("\n", "\n    ")
block = block.removesuffix('    }\n  },\n') + '    },\n    "catalogDuplicate": ' + alias_json + '\n  },\n'
text = text[:start] + block + text[end:]

new = []
for product_id, name, price, code, filename in [
    (215, "Falda Bandage Dress", 219, "1733", INPUTS[1]),
    (216, "Vestido Bandage Negro/Amarillo", 449, "2074", INPUTS[2]),
]:
    photo = copy_photo(filename, product_id, "01-frente.png")
    product = {
        "id": product_id, "name": name, "category": "Bandage", "price": price,
        "note": "Consulta disponibilidad y medidas con la boutique.",
        "photos": [photo], "image": photo["src"], "photoPending": False,
        "catalogName": name, "catalogCategory": "Vestidos Bandage's", "catalogCode": code,
        "priceSource": {"tipo": "WhatsApp Web", "telefono": "+51 930 527 248",
                        "fecha": "2026-10-18", "codigoCatalogo": code,
                        "evidencia": "review/auditoria-whatsapp-2026-10-18/inventario_actualizado.json"},
        "imageSource": {"tipo": "Imagen original entregada por el propietario",
                        "fecha": "2026-10-19", "archivo": filename},
    }
    new.append(product)

prefix2, tail2 = text.split("export const products = ", 1)
payload2, suffix2 = tail2.split("];", 1)
serialized = ",\n" + ",\n".join("  " + json.dumps(p, ensure_ascii=False, indent=2).replace("\n", "\n  ") for p in new)
SRC.write_text(prefix2 + "export const products = " + payload2.rstrip() + serialized + "\n];" + suffix2, encoding="utf-8")
products.extend(new)
(ROOT / "review" / "publicados-confirmados.json").write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Actualizado XL-187; incorporados XL-215 y XL-216")
