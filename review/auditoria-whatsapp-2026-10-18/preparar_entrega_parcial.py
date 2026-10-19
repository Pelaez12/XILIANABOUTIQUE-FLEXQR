import json
import re
from collections import Counter
from pathlib import Path


root = Path(__file__).parent
source = json.loads((root / "inventario_observado.json").read_text(encoding="utf-8"))
details = json.loads((root / "detalles_observados.json").read_text(encoding="utf-8"))
verified = {(row["group"], row["n"]): row for row in details if row.get("matched")}

rows = []
json_rows = []
by_group = Counter()
references = []
for item in source:
    group = item["grupo_fuente"]
    index = by_group[group]
    by_group[group] += 1
    detail = verified.get((group, index))
    count = len(detail["data"]["imgs"]) if detail else None
    state = "NO VERIFICADO"
    if detail:
        state = "SIN PRECIO" if item["precio_pen"] is None else "SIN FOTO" if count == 0 else "OK"
    elif item["precio_pen"] is None:
        state = "SIN PRECIO"
    collection = "PENDIENTES" if group.startswith("PENDIENTES") else group
    description = item["descripcion"]
    code = None
    if detail:
        match = re.search(r"\bCOD\s*\d+\b", detail["data"]["text"], re.IGNORECASE)
        if match:
            code = match.group(0)
    rows.append({
        "numero": len(rows) + 1,
        "coleccion": collection,
        "grupo_fuente": group,
        "nombre": item["nombre"],
        "precio_pen": item["precio_pen"],
        "precio_anterior_pen": item["precio_anterior_pen"],
        "descuento_pct": item["descuento_pct"],
        "descripcion": description,
        "codigo_explicito": code,
        "numero_fotos": count,
        "archivos_foto": [],
        "estado": state,
    })
    json_rows.append({
        "coleccion": collection,
        "nombre": item["nombre"],
        "precio_pen": item["precio_pen"],
        "precio_anterior_pen": item["precio_anterior_pen"],
        "descuento_pct": item["descuento_pct"],
        "descripcion": description,
        "fotos": [],
        "estado": state,
    })
    if code:
        references.append({"numero": len(rows), "codigo_explicito": code})

(root / "inventario_parcial.json").write_text(json.dumps(json_rows, ensure_ascii=False, indent=2), encoding="utf-8")
(root / "referencias_explicitas.json").write_text(json.dumps(references, ensure_ascii=False, indent=2), encoding="utf-8")

def show(value):
    if value is None:
        return "NO VERIFICADO"
    return str(value).replace("|", "\\|").replace("\n", " ")

lines = [
    "# Auditoría parcial del catálogo de WhatsApp — 18 de octubre de 2026",
    "",
    "El navegador Chrome dejó de estar disponible durante la inspección de PENDIENTES 2. Los conteos de abajo son fichas observadas, no artículos únicos: las tres secciones PENDIENTES pueden repetir productos. No se completó la descarga de fotos ni la comparación con la web.",
    "",
    "| N° | Colección | Nombre exacto | Precio PEN | Precio anterior | Descuento | Descripción/Talla | N° de fotos | Archivos de foto | Estado |",
    "| ---: | --- | --- | ---: | ---: | ---: | --- | ---: | --- | --- |",
]
for row in rows:
    lines.append("| " + " | ".join([
        str(row["numero"]), show(row["coleccion"]), show(row["nombre"]),
        show(row["precio_pen"]), show(row["precio_anterior_pen"]), show(row["descuento_pct"]),
        show(row["descripcion"]), show(row["numero_fotos"]), "—", row["estado"],
    ]) + " |")
lines.extend(["", "## Códigos expresamente rotulados en las fichas", "", "| N° | Código |", "| ---: | --- |"])
lines.extend(f"| {row['numero']} | {row['codigo_explicito']} |" for row in references)
(root / "inventario_parcial.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"fichas_observadas": len(rows), "fichas_verificadas_en_detalle": sum(r["estado"] != "NO VERIFICADO" for r in rows), "pendientes_de_detalle": sum(r["estado"] == "NO VERIFICADO" for r in rows), "sin_precio": sum(r["estado"] == "SIN PRECIO" for r in rows)}, ensure_ascii=False))
