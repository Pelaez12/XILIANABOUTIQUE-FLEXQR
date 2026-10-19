"""Consolida el inventario observado sin alterar la tienda ni WhatsApp."""

import json
import re
from collections import defaultdict
from pathlib import Path


BASE = Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


observed = read("inventario_observado.json")
details = read("detalles_observados.json")
detail_by_position = {(r["group"], r["n"]): r for r in details}
earrings = {
    "PENDIENTES 1": read("fotos_pendientes_1/pendientes_1_verificados.json"),
    "PENDIENTES 2": read("fotos_pendientes_2/pendientes_2_verificados.json"),
    "PENDIENTES 3": read("fotos_pendientes_3/pendientes_3_verificados.json"),
}
other = read("fotos_otros/otros_verificados.json")
liquidation = read("liquidacion_lista.json")
other_by_name = {r["nombre"]: r for r in other}
positions = defaultdict(int)
rows = []

for raw in observed:
    group = raw["grupo_fuente"]
    n = positions[group]
    positions[group] += 1
    record = {
        "coleccion": raw["coleccion"],
        "grupo_fuente": group,
        "nombre": raw["nombre"],
        "precio_pen": raw["precio_pen"],
        "precio_anterior_pen": raw["precio_anterior_pen"],
        "descuento_pct": raw["descuento_pct"],
        "descripcion": raw["descripcion"],
        "numero_visible": None,
        "numero_fotos": None,
        "fotos": [],
        "tipo_archivo": None,
        "estado": "NO VERIFICADO",
    }
    detail = detail_by_position.get((group, n))
    if detail:
        data = detail.get("data", {})
        imgs = data.get("imgs") or []
        if imgs:
            record["numero_fotos"] = len(imgs)
        match = re.search(r"(?m)^(?:COD\s*)?(\d{3,5})\s*$", data.get("text", ""), re.I)
        if match:
            record["numero_visible"] = match.group(1)
        if detail.get("matched") and imgs:
            record["estado"] = "OK"

    if group in earrings:
        item = earrings[group][n]
        assert item["nombre"] == record["nombre"], (group, n)
        folder = f"fotos_pendientes_{group[-1]}"
        record["fotos"] = [f"{folder}/{item['archivo']}"] + [
            f"{folder}/{name}" for name in item.get("fotos_adicionales", [])
        ]
        record["tipo_archivo"] = "captura de ficha; no foto original"
        record["numero_fotos"] = item.get("numero_fotos")
        record["numero_visible"] = (item.get("detalle_visible") or "")
        match = re.search(r'generic: "(\d+)"', record["numero_visible"])
        record["numero_visible"] = match.group(1) if match else None
        if all((BASE / path).is_file() for path in record["fotos"]) and record["numero_fotos"] is not None:
            record["estado"] = "OK; FOTOS VERIFICADAS MEDIANTE CAPTURAS DE FICHA"
    elif group == "CALZADOS":
        record["fotos"] = ["fotos_otros/calzados_sandalias-color-fucsia-talla-38_01.jpg"]
        record["tipo_archivo"] = "captura de ficha; no foto original"
        record["numero_visible"] = "748"
        record["estado"] = "FOTO PRINCIPAL VERIFICADA; N° TOTAL DE FOTOS NO VERIFICADO"
    elif group == "ACCESORIOS U OTROS" and record["nombre"] in other_by_name:
        item = other_by_name[record["nombre"]]
        record["fotos"] = ["fotos_otros/" + item["archivo"]]
        record["tipo_archivo"] = "captura de ficha; no foto original"
        record["estado"] = "FOTO PRINCIPAL VERIFICADA; N° TOTAL DE FOTOS NO VERIFICADO"

    if record["precio_pen"] is None:
        record["estado"] = "SIN PRECIO"
    rows.append(record)

for item in liquidation:
    rows.append({
        "coleccion": item["coleccion"],
        "grupo_fuente": item["coleccion"],
        "nombre": item["nombre"],
        "precio_pen": item["precio_pen"],
        "precio_anterior_pen": item["precio_anterior_pen"],
        "descuento_pct": item["descuento_pct"],
        "descripcion": item.get("descripcion", ""),
        "numero_visible": item.get("numero_visible"),
        "numero_fotos": item.get("numero_fotos"),
        "fotos": [],
        "tipo_archivo": None,
        "estado": item.get("estado", "NO VERIFICADO"),
    })

assert len(rows) == 272
(BASE / "inventario_actualizado.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
)


def display(value):
    return "—" if value is None or value == "" else str(value).replace("|", "\\|").replace("\n", " ")


headers = [
    "N°", "Colección", "Nombre exacto", "Precio PEN", "Precio anterior",
    "Descuento", "Descripción/Talla", "N° de fotos", "Archivos de foto", "Estado",
]
lines = [
    "# Inventario actualizado de WhatsApp — 18 de octubre de 2026",
    "",
    "272 entradas de catálogo observadas, incluidas 11 entradas de Liquidación que se mantienen como lista adicional y pueden repetir productos de las colecciones principales. PENDIENTES contiene 83 entradas en tres grupos y 56 productos únicos tras eliminar 27 repeticiones. Los archivos nuevos de aretes, calzados y accesorios son capturas de ficha; WhatsApp no permitió descargar el blob como imagen original.",
    "",
    "| " + " | ".join(headers) + " |",
    "| " + " | ".join(["---:"] + ["---"] * (len(headers) - 1)) + " |",
]
for index, item in enumerate(rows, start=1):
    vals = [
        index, item["grupo_fuente"], item["nombre"], item["precio_pen"],
        item["precio_anterior_pen"], item["descuento_pct"], item["descripcion"],
        item["numero_fotos"], ", ".join(item["fotos"]), item["estado"],
    ]
    lines.append("| " + " | ".join(display(v) for v in vals) + " |")
(BASE / "inventario_actualizado.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(json.dumps({
    "entradas": len(rows),
    "sin_precio": [r["nombre"] for r in rows if r["precio_pen"] is None],
    "capturas_nuevas": sum(bool(r["fotos"]) for r in rows),
    "numero_fotos_verificado": sum(r["numero_fotos"] is not None for r in rows),
}, ensure_ascii=False, indent=2))
