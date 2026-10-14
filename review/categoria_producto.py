"""Prioridad de categorías acordada con el usuario para el catálogo."""
import re
import json
from pathlib import Path


confirmed_file = Path(__file__).with_name('categorias-confirmadas.json')
confirmed = json.loads(confirmed_file.read_text(encoding='utf-8')) if confirmed_file.exists() else {'prendas': []}
confirmed_by_id = {p['id']: p['categoria'] for p in confirmed['prendas']}


def categoria_por_nombre(nombre, actual, ident=None):
    # Una clasificación explícita del usuario prevalece sobre palabras del nombre.
    if ident in confirmed_by_id:
        return confirmed_by_id[ident]
    if actual in ('Bandage', 'Liquidación'):
        return actual
    if re.search(r'\bgala\b', nombre, re.IGNORECASE):
        return 'Gala'
    if re.search(r'\blargos?\b', nombre, re.IGNORECASE):
        return 'Largos'
    if actual != 'Cortos con brillo' and re.search(r'\bcortos?\b', nombre, re.IGNORECASE):
        return 'Cortos'
    return actual
