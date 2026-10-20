"""Incorpora las cuatro fotos restantes, en el orden confirmado por el propietario."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TEMP = Path(r"C:\Users\USER\AppData\Local\Temp")
FILES = [
    "codex-clipboard-e5c217ab-4510-4c43-b088-f777cc78d3a8.png",
    "codex-clipboard-2122a2f2-6a3e-4d91-a2b4-0a86d2c1b23b.png",
    "codex-clipboard-40f9e8ca-d69b-42b1-a9b2-59747ba147b8.png",
    "codex-clipboard-01cce014-258a-4282-bd1f-04f8d1240a34.png",
]
confirmation = json.loads((OUT / "confirmacion-largos-22.json").read_text(encoding="utf-8"))
missing = [row for row in confirmation["vestidos"] if not row["id_web"]]
assert len(missing) == 4
source = (ROOT / "products.js").read_text(encoding="utf-8")
prefix, tail = source.split("export const products = ", 1)
payload, suffix = tail.split("];", 1)
products = json.loads(payload + "]")
assert len(products) == 171
assert all(number not in {p["id"] for p in products} for number in range(211, 215))
added = []
for offset, row in enumerate(missing):
    number = 211 + offset
    original = TEMP / FILES[offset]
    assert original.is_file(), original
    with Image.open(original) as image:
        image.verify()
    with Image.open(original) as image:
        width, height = image.size
    assert width >= 600 and height >= 800, (original, width, height)
    folder = ROOT / "images" / "productos-reales" / f"XL-{number:03d}"
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / "01-frente.png"
    shutil.copyfile(original, dest)
    photo = f"./images/productos-reales/XL-{number:03d}/01-frente.png"
    code = row["codigo_whatsapp"]
    price_source = {"tipo": "WhatsApp Web", "telefono": "+51 930 527 248",
                    "fecha": "2026-10-18", "evidencia": "review/auditoria-whatsapp-2026-10-18/inventario_actualizado.json"}
    if code:
        price_source["codigoCatalogo"] = code
    product = {
        "id": number, "name": row["nombre"], "category": "Largos",
        "price": row["precio_pen"],
        "note": "Consulta disponibilidad y medidas con la boutique.",
        "photos": [{"src": photo, "width": width, "height": height,
                    "view": "Frente", "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}],
        "image": photo, "photoPending": False,
        "catalogName": row["nombre"], "catalogCategory": "Vestidos Largos",
        "priceSource": price_source,
        "imageSource": {"tipo": "Imagen original entregada por el propietario",
                        "fecha": "2026-10-19", "orden": offset + 9,
                        "archivo": FILES[offset]},
    }
    if code:
        product["catalogCode"] = code
    added.append(product)
    row["id_web"] = f"XL-{number:03d}"
    row["estado_web"] = "publicado en Largos"
serialized = ",\n" + ",\n".join("  " + json.dumps(p, ensure_ascii=False, indent=2).replace("\n", "\n  ") for p in added)
assert payload.rstrip().endswith("}")
(ROOT / "products.js").write_text(prefix + "export const products = " + payload.rstrip() + serialized + "\n];" + suffix, encoding="utf-8")
products.extend(added)
(ROOT / "review" / "publicados-confirmados.json").write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
confirmation["publicados_en_largos"] = 22
confirmation["pendientes_de_ficha_y_foto"] = 0
(OUT / "confirmacion-largos-22.json").write_text(json.dumps(confirmation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Incorporados:", ", ".join(f"XL-{p['id']:03d}" for p in added))
