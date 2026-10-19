import hashlib
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / "products.js").read_text(encoding="utf-8")
products = json.loads(source.split("export const products = ", 1)[1].split(";\nexport const categories", 1)[0])


def dhash(path):
    with Image.open(path) as image:
        gray = ImageOps.exif_transpose(image).convert("L").resize((9, 8), Image.Resampling.LANCZOS)
        pixels = list(gray.getdata())
    bits = 0
    for y in range(8):
        for x in range(8):
            bits = (bits << 1) | (pixels[y * 9 + x] > pixels[y * 9 + x + 1])
    return bits


images = []
missing = []
for product in products:
    photos = product.get("photos") or [{"src": product.get("image", "")}]
    for i, photo in enumerate(photos, 1):
        src = photo.get("src") or ""
        path = ROOT / src.removeprefix("./")
        if not path.is_file():
            missing.append({"id": product["id"], "name": product["name"], "src": src})
            continue
        images.append({
            "id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "number": i,
            "src": src,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "dhash": dhash(path),
        })

exact = defaultdict(list)
for item in images:
    exact[item["sha256"]].append(item)
exact_groups = [group for group in exact.values() if len({item["id"] for item in group}) > 1]
near_pairs = []
for i, a in enumerate(images):
    for b in images[i + 1:]:
        if a["id"] == b["id"] or a["sha256"] == b["sha256"]:
            continue
        distance = (a["dhash"] ^ b["dhash"]).bit_count()
        if distance <= 5:
            near_pairs.append({
                "distance": distance,
                "a": {k: a[k] for k in ("id", "name", "category", "number", "src")},
                "b": {k: b[k] for k in ("id", "name", "category", "number", "src")},
            })

result = {
    "products": len(products),
    "images": len(images),
    "missing_files": missing,
    "exact_groups": exact_groups,
    "near_pairs": sorted(near_pairs, key=lambda x: x["distance"]),
}
output = Path(__file__).with_name("fotos_web_duplicadas.json")
output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({
    "products": result["products"],
    "images": result["images"],
    "missing_files": len(missing),
    "exact_groups": len(exact_groups),
    "near_pairs": len(near_pairs),
    "output": str(output),
}, ensure_ascii=False))
for group in exact_groups:
    print("EXACTO", [(item["id"], item["name"], item["number"]) for item in group])
for pair in result["near_pairs"][:40]:
    print("SIMILAR", pair["distance"], (pair["a"]["id"], pair["a"]["name"], pair["a"]["number"]), (pair["b"]["id"], pair["b"]["name"], pair["b"]["number"]))
