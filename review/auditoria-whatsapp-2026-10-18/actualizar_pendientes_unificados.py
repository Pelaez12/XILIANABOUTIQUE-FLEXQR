"""Actualiza el consolidado de aretes con el conteo completo de fotos."""

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read(path):
    return json.loads((BASE / path).read_text(encoding="utf-8"))


groups = {
    "PENDIENTES 1": read("fotos_pendientes_1/pendientes_1_verificados.json"),
    "PENDIENTES 2": read("fotos_pendientes_2/pendientes_2_verificados.json"),
    "PENDIENTES 3": read("fotos_pendientes_3/pendientes_3_verificados.json"),
}
items = {}

for group, records in groups.items():
    folder = f"fotos_pendientes_{group[-1]}"
    for record in records:
        detail = record.get("detalle_visible") or ""
        match = re.search(r'(?:generic: )?["“]?(\d{3,5})["”]?', detail)
        number = match.group(1) if match else None
        key = number or (record["nombre"].casefold(), record["precio_pen"])
        photos = [f"{folder}/{record['archivo']}"] + [
            f"{folder}/{name}" for name in record.get("fotos_adicionales", [])
        ]
        if key not in items:
            items[key] = {
                "coleccion": "PENDIENTES",
                "nombre": record["nombre"],
                "precio_pen": record["precio_pen"],
                "precio_anterior_pen": None,
                "descuento_pct": None,
                "descripcion": "",
                "numero_fotos_catalogo": record.get("numero_fotos", 1),
                "fotos": photos,
                "grupos_fuente": [group],
                "estado": "OK; FOTOS VERIFICADAS MEDIANTE CAPTURAS DE FICHA",
                "numero_visible": number,
            }
        else:
            item = items[key]
            item["grupos_fuente"].append(group)
            if record.get("numero_fotos", 1) > item["numero_fotos_catalogo"]:
                item["numero_fotos_catalogo"] = record["numero_fotos"]
                item["fotos"] = photos

result = list(items.values())
assert len(result) == 56, len(result)
(BASE / "pendientes_unificados.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)

lines = [
    "# PENDIENTES unificados",
    "",
    "83 entradas observadas en tres secciones; 56 artículos únicos y 27 repeticiones. Todas las fotos del carrusel fueron recorridas. Los archivos son capturas de evidencia de la ficha de WhatsApp, no imágenes originales descargadas.",
    "",
    "| N° | Nombre exacto | Precio PEN | Código visible | N° de fotos | Secciones | Archivos de evidencia |",
    "| ---: | --- | ---: | --- | ---: | --- | --- |",
]
for index, item in enumerate(result, 1):
    esc = lambda value: str(value or "—").replace("|", "\\|")
    lines.append(
        f"| {index} | {esc(item['nombre'])} | {item['precio_pen']} | "
        f"{esc(item['numero_visible'])} | {item['numero_fotos_catalogo']} | "
        f"{', '.join(item['grupos_fuente'])} | {', '.join(item['fotos'])} |"
    )
(BASE / "PENDIENTES-UNIFICADOS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(json.dumps({
    "entradas": sum(len(v) for v in groups.values()),
    "unicos": len(result),
    "con_multiples_fotos": sum(i["numero_fotos_catalogo"] > 1 for i in result),
    "total_fotos_unicas": sum(i["numero_fotos_catalogo"] for i in result),
}, ensure_ascii=False, indent=2))
