"""Comparación conservadora de fichas observadas en WhatsApp con products.js."""

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


BASE = Path(__file__).resolve().parent
SITE = BASE.parent.parent


def norm(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


source = (SITE / "products.js").read_text(encoding="utf-8")
web = json.loads(source[source.index("[") : source.index("];") + 1])
wa = json.loads((BASE / "inventario_observado.json").read_text(encoding="utf-8"))
details = json.loads((BASE / "detalles_observados.json").read_text(encoding="utf-8"))
detail_by_position = {(x["group"], x["n"]): x for x in details}
wa_name_counts = defaultdict(int)
for item in wa:
    if (item.get("grupo_fuente") or item["coleccion"]) in {
        "Gala Dresess", "Vestidos Largos", "Vestidos Cortos Brillos",
        "Vestidos Cortos", "Vestidos Bandage's",
    }:
        wa_name_counts[norm(item["nombre"])] += 1

web_by_code = defaultdict(list)
web_by_name = defaultdict(list)
for product in web:
    if product.get("catalogCode"):
        web_by_code[str(product["catalogCode"])].append(product)
    for field in ("catalogName", "name"):
        if product.get(field):
            web_by_name[norm(product[field])].append(product)

category_map = {
    "Gala Dresess": "Gala",
    "Vestidos Largos": "Largos",
    "Vestidos Cortos Brillos": "Cortos con brillo",
    "Vestidos Cortos": "Cortos",
    "Vestidos Bandage's": "Bandage",
}
position = defaultdict(int)
results = []
matched_ids = set()
for item in wa:
    group = item.get("grupo_fuente") or item["coleccion"]
    n = position[group]
    position[group] += 1
    if group not in category_map:
        continue
    detail = detail_by_position.get((group, n), {})
    text = detail.get("data", {}).get("text", "")
    explicit_code = re.search(r"\bCOD\s*(\d+)\b", text, re.I)
    isolated_number = re.search(r"(?m)^(\d{3,5})\s*$", text)
    code = explicit_code.group(1) if explicit_code else (
        isolated_number.group(1) if isolated_number else None
    )
    # La ficha 2024 comparte las mismas dos fotos que la 2025. El usuario
    # confirmó que es un solo vestido y eligió 2025 a S/ 429 como referencia.
    if group == "Vestidos Cortos" and code == "2024":
        continue
    candidates = list(web_by_code.get(code, [])) if code else []
    match_type = "numero visible coincide con catalogCode web" if len(candidates) == 1 else None
    if len(candidates) != 1 and wa_name_counts[norm(item["nombre"])] == 1:
        unique = {p["id"]: p for p in web_by_name.get(norm(item["nombre"]), [])}
        candidates = list(unique.values())
        match_type = "nombre exacto normalizado" if len(candidates) == 1 else None
    row = {
        "grupo_whatsapp": group,
        "nombre_whatsapp": item["nombre"],
        "precio_whatsapp": item["precio_pen"],
        "numero_visible_whatsapp": code,
        "coincidencia": match_type or ("ambigua" if candidates else "no encontrada"),
        "id_web": candidates[0]["id"] if len(candidates) == 1 else None,
        "nombre_web": candidates[0]["name"] if len(candidates) == 1 else None,
        "precio_web": candidates[0]["price"] if len(candidates) == 1 else None,
        "categoria_web": candidates[0]["category"] if len(candidates) == 1 else None,
        "precio_diferente": len(candidates) == 1
        and candidates[0].get("price") is not None
        and item["precio_pen"] is not None
        and float(candidates[0]["price"]) != float(item["precio_pen"]),
        "categoria_diferente": len(candidates) == 1
        and candidates[0]["category"] not in (category_map[group], "Liquidación"),
        "web_en_liquidacion": len(candidates) == 1
        and candidates[0]["category"] == "Liquidación",
        "foto_comparada": False,
    }
    if len(candidates) == 1:
        matched_ids.add(candidates[0]["id"])
    results.append(row)

extra_web = [
    {"id": p["id"], "nombre": p["name"], "categoria": p["category"], "precio": p["price"]}
    for p in web
    if p["id"] not in matched_ids
]
summary = {
    "entradas_vestidos_whatsapp": len(results),
    "productos_web": len(web),
    "emparejamientos_por_codigo_o_nombre_unico": sum(r["id_web"] is not None for r in results),
    "sin_emparejamiento_unico": sum(r["id_web"] is None for r in results),
    "precios_diferentes_en_coincidencias": sum(r["precio_diferente"] for r in results),
    "categorias_diferentes_en_coincidencias": sum(r["categoria_diferente"] for r in results),
    "productos_web_sin_emparejamiento_unico": len(extra_web),
    "pendientes_web": sum("pendient" in norm(p["name"]) or "arete" in norm(p["name"]) for p in web),
    "nota": "El nombre único es un indicio, no una identificación visual. Una ausencia de emparejamiento no demuestra que falte el vestido.",
}
output = {"resumen": summary, "vestidos": results, "web_sin_coincidencia": extra_web}
(BASE / "comparacion_web_conservadora.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(summary, ensure_ascii=False, indent=2))
