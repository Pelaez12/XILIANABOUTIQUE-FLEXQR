"""Incorpora la blusa de la fila 19 en Largos por indicación expresa del propietario."""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = Path(r"C:\Users\USER\AppData\Local\Temp\codex-clipboard-1d4a0875-5a10-464a-9119-b5837c2ffbff.png")
DEST = ROOT / "images/productos-reales/XL-217/01-frente.png"
PRODUCTS = ROOT / "products.js"
CURRENT = ROOT / "review/publicados-confirmados.json"

text = PRODUCTS.read_text(encoding="utf-8")
prefix, tail = text.split("export const products = ", 1)
payload, suffix = tail.split("];", 1)
products = json.loads(payload + "]")
assert len(products) == 177
assert len({p["id"] for p in products}) == 177
assert not any(p["id"] == 217 for p in products)

with Image.open(ORIGINAL) as image:
    image.verify()
with Image.open(ORIGINAL) as image:
    width, height = image.size
assert width >= 600 and height >= 700
DEST.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(ORIGINAL, DEST)
photo_path = "./images/productos-reales/XL-217/01-frente.png"
name = "Blusa cola de pato asimétrico blanco con negro"
product = {
    "id": 217,
    "name": name,
    "category": "Largos",
    "price": 239,
    "note": "Blusa asimétrica de cola de pato en blanco y negro. Consulta disponibilidad y medidas con la boutique.",
    "photos": [{
        "src": photo_path,
        "width": width,
        "height": height,
        "view": "Frente",
        "sha256": hashlib.sha256(DEST.read_bytes()).hexdigest(),
    }],
    "image": photo_path,
    "photoPending": False,
    "catalogName": name,
    "catalogCategory": "Vestidos Largos",
    "priceSource": {
        "tipo": "WhatsApp Web",
        "telefono": "+51 930 527 248",
        "fecha": "2026-10-18",
        "evidencia": "review/auditoria-whatsapp-2026-10-18/inventario_actualizado.json",
        "fila": 19,
    },
    "imageSource": {
        "tipo": "Imagen original entregada por el propietario",
        "fecha": "2026-10-20",
        "archivo": ORIGINAL.name,
    },
    "categoryConfirmation": "Propietario pidió expresamente colocar esta blusa en Vestidos Largos el 20/10/2026.",
}
serialized = "  " + json.dumps(product, ensure_ascii=False, indent=2).replace("\n", "\n  ")
PRODUCTS.write_text(prefix + "export const products = " + payload.rstrip() + ",\n" + serialized + "\n];" + suffix, encoding="utf-8")
products.append(product)
CURRENT.write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Incorporado XL-217", width, height)
