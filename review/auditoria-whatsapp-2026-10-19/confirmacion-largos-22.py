"""Registra la confirmación expresa del propietario del 19/10."""
import json
from pathlib import Path

folder = Path(__file__).resolve().parent
data = json.loads((folder / "matriz-171.json").read_text(encoding="utf-8"))
rows = [row for row in data["filas_whatsapp"] if row["coleccion"] == "Vestidos Largos"]
assert len(rows) == 23
assert rows[18]["nombre"].lower().startswith("blusa cola de pato")
confirmed = []
for row in rows:
    if row["fila"] == 19:
        continue
    confirmed.append({
        "orden_confirmado": len(confirmed) + 1,
        "fila_whatsapp_18_oct": row["fila"],
        "codigo_whatsapp": row["codigo_whatsapp"],
        "nombre": row["nombre"],
        "precio_pen": row["precio_pen"],
        "id_web": row["id_web"],
        "categoria_confirmada_propietario": "Largos",
        "estado_web": "publicado en Largos" if row["id_web"] else "pendiente de ficha y foto original",
        "evidencia": "Lista expresa de 22 nombres y tres capturas del propietario, 19/10/2026",
    })
assert len(confirmed) == 22
assert sum(bool(row["id_web"]) for row in confirmed) == 18
result = {"fecha": "2026-10-19", "total_confirmados": 22,
          "publicados_en_largos": 18, "pendientes_de_ficha_y_foto": 4,
          "exclusion": {"fila_whatsapp_18_oct": 19, "nombre": rows[18]["nombre"],
                        "motivo": "Blusa, fuera de los 22 vestidos confirmados"},
          "vestidos": confirmed}
(folder / "confirmacion-largos-22.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
