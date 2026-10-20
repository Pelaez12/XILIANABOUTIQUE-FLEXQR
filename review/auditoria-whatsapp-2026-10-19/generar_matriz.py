"""Reconcilia referencias comerciales del 18/10 con prendas web, sin inferir identidad por conteos."""
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "review/auditoria-whatsapp-2026-10-20"
SRC = ROOT / "review/auditoria-whatsapp-2026-10-18"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(value):
    value = unicodedata.normalize("NFKD", value.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

products = json.loads((ROOT / "products.js").read_text(encoding="utf-8").split("export const products = ")[1].split("];")[0] + "]")
inventory = read(SRC / "inventario_actualizado.json")
historical = read(ROOT / "review/categorias-confirmadas.json")
previous = read(ROOT / "review/conciliacion-final-2026-10-15/resultado-aplicado.json")
conservative = read(SRC / "comparacion_web_conservadora.json")["vestidos"]
by_id = {p["id"]: p for p in products}
assert len(products) == len(by_id) == 178

# Fila comercial (1 basada) -> identidad estable. Estas asociaciones se apoyan
# en nombre, precio, código y las revisiones fotográficas citadas en el informe.
manual = {
    "Gala Dresess": {10: 140, 14: 59, 34: 97, 35: 98, 40: 102, 47: 175, 48: 108, 50: 110},
    "Vestidos Largos": {2: 5, 8: 22, 19: 217},
    "Vestidos Cortos Brillos": {7: 155, 9: 16, 14: 156, 21: 49, 33: 39, 38: 123, 39: 117},
    "Vestidos Cortos": {1: 10, 10: 187, 15: 66},
    "Vestidos Bandage's": {1: 14, 2: 182, 3: 144, 13: 116, 14: 77},
    "PRENDAS LIQUIDACIÓN 💃🏻👠👗": {1: 10, 2: 16, 6: 155},
}
groups = defaultdict(list)
for item in inventory:
    if item["coleccion"] != "PENDIENTES" and item["coleccion"] not in ("CALZADOS", "ACCESORIOS U OTROS"):
        groups[item["coleccion"]].append(item)

matches = defaultdict(list)
source_rows = []
for group, rows in groups.items():
    for index, item in enumerate(rows, 1):
        number = item.get("numero_visible")
        code = number if number and number != "1200" else None
        assigned = manual.get(group, {}).get(index)
        method = "revisión nominal, precio, código y evidencia previa" if assigned else None
        if group == "Vestidos Cortos" and index == 10:
            method = "foto idéntica a XL-187 entregada por el propietario; S/329 confirmado el 19/10"
        if group == "Vestidos Largos" and index == 19:
            method = "foto entregada por el propietario; inclusión expresa de la blusa en Largos el 20/10"
        if assigned is None:
            exact = [p for p in products if p["price"] == item["precio_pen"] and norm(p["name"]) == norm(item["nombre"])]
            if len(exact) == 1:
                assigned = exact[0]["id"]
                method = "nombre y precio exactos"
        if assigned is None:
            prior = [r for r in conservative if r["grupo_whatsapp"] == group and r["nombre_whatsapp"] == item["nombre"] and r["precio_whatsapp"] == item["precio_pen"] and r["numero_visible_whatsapp"] == number and r["id_web"] in by_id]
            if len(prior) == 1:
                assigned = prior[0]["id_web"]
                method = prior[0]["coincidencia"]
        row = {"coleccion": group, "fila": index, "codigo_whatsapp": code,
               "nombre": item["nombre"], "precio_pen": item["precio_pen"],
               "id_web": f"XL-{assigned:03d}" if assigned else None,
               "metodo": method, "estado": "asociado" if assigned else "sin identidad web demostrada"}
        source_rows.append(row)
        if assigned:
            matches[assigned].append(row)

old_by_id = {p["id"]: p for p in historical["prendas"]}
specific = {
    66: "Propietario: códigos 2024/2025 son una sola prenda; conservar XL-066, ficha 2025 a S/429 (duplicados_confirmados.json).",
    107: "GALA-CAPTURA-R112, frente y espalda; confirmación posterior para Gala (categorias-confirmadas.json).",
    117: "Propietario confirmó exclusivamente Gala a S/389 el 16/10, aunque también aparece en Brillos código 2062 (categorias-confirmadas.json).",
    154: "Excepción individual del propietario: Cortos con brillo aunque el nombre diga largo (categorias-confirmadas.json).",
    187: "Cortos códigos 1914 S/329 y 1894 S/319 son la misma prenda y foto; propietario confirmó S/329 el 19/10/2026. Foto nueva de alta resolución conservando las anteriores.",
    196: "Alta posterior de gala morado S/649 con frente y espalda (pendientes-incorporados-2026-10-18.json).",
    217: "Propietario pidió expresamente publicar la blusa de la fila 19 en Vestidos Largos el 20/10/2026; foto original entregada ese día.",
}
matrix = []
for p in products:
    old = old_by_id.get(p["id"])
    entries = matches[p["id"]]
    matrix.append({
        "id_web": f"XL-{p['id']:03d}",
        "codigos_whatsapp": sorted(set(r["codigo_whatsapp"] for r in entries if r["codigo_whatsapp"])),
        "nombre": p["name"], "precio_pen": p["price"],
        "fotos": [{"src": photo["src"], "vista": photo.get("view"), "sha256": photo.get("sha256")} for photo in p["photos"]],
        "origen_inventario_actualizado": [{"coleccion": r["coleccion"], "fila": r["fila"], "codigo": r["codigo_whatsapp"]} for r in entries],
        "categoria_web_actual": p["category"],
        "confirmaciones_posteriores": [specific[p["id"]]] if p["id"] in specific else [],
        "evidencia_historica": {"categoria": old["categoria"], "fecha": old["fecha"], "fuente": old.get("fuente")} if old else None,
        "categoria_final_propuesta": None if not entries and p["id"] not in (127, 173) else p["category"],
        "estado": "pendiente de confirmar colección/vigencia; conservar publicación provisional" if not entries and p["id"] not in (127, 173) else "conservar por evidencia",
    })

result = {
    "fecha": "2026-10-20", "total_web": len(products),
    "conteos_fuente": dict(Counter(r["coleccion"] for r in source_rows)),
    "conteos_web_final": dict(Counter(p["category"] for p in products)),
    "totales_conciliacion_15_oct": previous["totales"],
    "matriz_productos": matrix,
    "filas_whatsapp": source_rows,
    "sin_identidad_web_demostrada": [r for r in source_rows if not r["id_web"]],
}
(OUT / f"matriz-{len(products)}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("productos", len(matrix), "filas fuente", len(source_rows), "sin identidad", len(result["sin_identidad_web_demostrada"]))
for group in groups:
    rows = [r for r in source_rows if r["coleccion"] == group]
    print(group.encode("ascii", "backslashreplace").decode(), len(rows), "asociadas", sum(bool(r["id_web"]) for r in rows), "sin identidad", len([r for r in rows if not r["id_web"]]))
