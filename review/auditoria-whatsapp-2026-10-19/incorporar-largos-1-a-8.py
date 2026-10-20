"""Incorpora las ocho fotos entregadas en orden por el propietario el 19/10."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TEMP = Path(r"C:\Users\USER\AppData\Local\Temp")
FILES = [
    "codex-clipboard-e7bde1fc-a144-4cee-9c5d-6de4969dc462.png",
    "codex-clipboard-eaf3b1b5-5a71-41e9-ab5e-41aea37107b2.png",
    "codex-clipboard-58e1f506-45d3-4ad6-ac78-70c900f427aa.png",
    "codex-clipboard-caafbe29-a5ce-45fd-b586-f9c35e1f9337.png",
    "codex-clipboard-646693aa-a5b5-418d-9a33-ed16b54a9c76.png",
    "codex-clipboard-38b2c96b-e1fd-421d-8427-f88b0c5ae5c3.png",
    "codex-clipboard-6cc7d10c-9be9-416d-9e57-60c6e9f9142c.png",
    "codex-clipboard-655f752d-68a4-403e-985f-f4a3c360657c.png",
]
confirmation = json.loads((OUT / "confirmacion-largos-22.json").read_text(encoding="utf-8"))
missing = [row for row in confirmation["vestidos"] if not row["id_web"]]
assert len(missing) == 12
source = (ROOT / "products.js").read_text(encoding="utf-8")
prefix, tail = source.split("export const products = ", 1)
payload, suffix = tail.split("];", 1)
products = json.loads(payload + "]")
existing = {product["id"] for product in products}
assert all(number not in existing for number in range(203, 211))
added = []
for offset, row in enumerate(missing[:8]):
    number = 203 + offset
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
                        "fecha": "2026-10-19", "orden": offset + 1,
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
confirmation["publicados_en_largos"] = 18
confirmation["pendientes_de_ficha_y_foto"] = 4
(OUT / "confirmacion-largos-22.json").write_text(json.dumps(confirmation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Incorporados:", ", ".join(f"XL-{p['id']:03d}" for p in added))
