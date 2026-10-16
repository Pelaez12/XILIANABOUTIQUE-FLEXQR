"""Aplicar la clasificación visual confirmada, sin inferirla del nombre."""
import json
from pathlib import Path


confirmed_file = Path(__file__).with_name('categorias-confirmadas.json')
confirmed = json.loads(confirmed_file.read_text(encoding='utf-8')) if confirmed_file.exists() else {'prendas': []}
confirmed_by_id = {p['id']: p['categoria'] for p in confirmed['prendas']}


def categoria_por_nombre(nombre, actual, ident=None):
    # Nombre conservado por compatibilidad con los importadores existentes.
    # Un nombre puede decir «largo» o «gala» sin describir el brillo real.
    if ident in confirmed_by_id:
        return confirmed_by_id[ident]
    return actual
